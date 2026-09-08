"""Reference management and schedule matching; never asserts seat availability."""
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from . import models as m
from .availability_rules import utcnow, aware
from .permissions import can
from .task_service import system_task
ZONE=ZoneInfo('America/Costa_Rica')
FRESH_DAYS=30

def get(db,model,id):
    row=db.get(model,id)
    if not row: raise HTTPException(404,'Transportation record not found')
    return row

def stale(value,now=None):
    return value is None or aware(value)<(now or utcnow())-timedelta(days=FRESH_DAYS)

def fields(row):
    return {c.name:str(getattr(row,c.name)) if isinstance(getattr(row,c.name),Decimal) else getattr(row,c.name) for c in row.__table__.columns}

def schedule_view(row):
    out=fields(row);out.pop('days_mask');out.pop('import_key')
    out.update(days_of_week=[i for i in range(7) if row.days_mask & (1<<i)],timezone=str(ZONE),needs_review=stale(row.last_verified_at) or row.days_mask==0)
    return out

def route_view(db,row,commercial=False,detail=False):
    out=fields(row)
    out['origin']=fields(get(db,m.TransportNode,row.origin_node_id))
    out['destination']=fields(get(db,m.TransportNode,row.destination_node_id))
    for endpoint in ('origin','destination'):
        destination_id=out[endpoint]['destination_id']
        out[endpoint]['destination_name']=get(db,m.Destination,destination_id).name if destination_id else None
    out['name']=out['origin']['name']+' → '+out['destination']['name']
    out['services']=[]
    review=stale(row.source_checked_at) or bool(row.review_notes)
    for s in db.scalars(select(m.VendorTransportService).where(m.VendorTransportService.route_id==row.id).order_by(m.VendorTransportService.id)):
        supplier=get(db,m.Supplier,s.supplier_id)
        schedules=[schedule_view(x) for x in db.scalars(select(m.TransportSchedule).where(m.TransportSchedule.vendor_service_id==s.id).order_by(m.TransportSchedule.departure_time))]
        service=fields(s);service.update(supplier_name=supplier.name,supplier_active=supplier.active,schedules=schedules)
        service['needs_review']=stale(s.last_verified_at) or not schedules or any(x['needs_review'] for x in schedules if x['active'])
        review=review or service['needs_review']
        if commercial:
            rates=list(db.scalars(select(m.TransportRate).where(m.TransportRate.vendor_service_id==s.id).order_by(m.TransportRate.id.desc())))
            superseded={r.supersedes_id for r in rates if r.supersedes_id}
            today=utcnow().astimezone(ZONE).date()
            current=[r for r in rates if r.id not in superseded and r.rate_kind=='vendor_rate' and r.effective_from<=today<=r.effective_to]
            service['rates_missing']=not any(r.vendor_cost is not None for r in current)
            if detail: service['rates']=[dict(fields(r),superseded=r.id in superseded) for r in rates]
        elif not detail:
            for key in ('pickup_notes','dropoff_notes','luggage_notes','child_policy','booking_method'): service.pop(key,None)
        out['services'].append(service)
    out['needs_review']=review or not out['services']
    if not commercial:
        for key in ('notes','review_notes'): out.pop(key,None)
        for key in ('origin','destination'): out[key].pop('notes',None)
    return out

def save(db,model,payload,actor,id=None):
    values=payload.model_dump(exclude={'expected_version'})
    try:
        with db.begin():
            row=db.scalar(select(model).where(model.id==id).with_for_update()) if id else None
            if id and not row: raise HTTPException(404,'Transportation record not found')
            if row and (payload.expected_version is None or payload.expected_version!=row.version): raise HTTPException(409,'Record changed. Reload before saving')
            if model==m.TransportNode:
                if values['destination_id']: get(db,m.Destination,values['destination_id'])
                if row and values['slug']!=row.slug: raise HTTPException(422,'Node slug is stable; edit its display name instead')
            elif model==m.CanonicalTransportRoute:
                get(db,m.TransportNode,values['origin_node_id']);get(db,m.TransportNode,values['destination_node_id'])
                if row and (row.origin_node_id,row.destination_node_id)!=(values['origin_node_id'],values['destination_node_id']): raise HTTPException(422,'Route direction is immutable')
            elif model==m.VendorTransportService:
                get(db,m.CanonicalTransportRoute,values['route_id']);get(db,m.Supplier,values['supplier_id'])
                if not db.scalar(select(m.SupplierService).where(m.SupplierService.supplier_id==values['supplier_id'],m.SupplierService.service_type=='transportation')): raise HTTPException(422,'Supplier needs transportation capability')
                if row and (row.supplier_id,row.route_id,row.service_type)!=(values['supplier_id'],values['route_id'],values['service_type']): raise HTTPException(422,'Vendor/service identity is immutable')
            elif model==m.TransportSchedule:
                get(db,m.VendorTransportService,values['vendor_service_id'])
                if row and row.vendor_service_id!=values['vendor_service_id']: raise HTTPException(422,'Schedule service is immutable')
                values['days_mask']=sum(1<<d for d in values.pop('days_of_week'))
            elif model==m.TransportRate:
                service=get(db,m.VendorTransportService,values['vendor_service_id'])
                expected='per_vehicle' if service.service_type=='private_transfer' else 'per_person'
                if service.service_type!='other' and values['unit_basis']!=expected: raise HTTPException(422,'Rate unit does not match service type')
                if values['agreement_id']:
                    agreement=get(db,m.SupplierAgreement,values['agreement_id'])
                    if agreement.supplier_id!=service.supplier_id or agreement.currency!=values['currency'] or values['effective_from']<agreement.effective_from or (agreement.effective_to and values['effective_to']>agreement.effective_to): raise HTTPException(422,'Rate must match supplier, currency and agreement dates')
                if values['supersedes_id']:
                    old=get(db,m.TransportRate,values['supersedes_id'])
                    if old.vendor_service_id!=service.id or old.rate_kind!=values['rate_kind']: raise HTTPException(422,'Superseded rate must belong to this service and pricing kind')
            if not row:
                row=model(**values);db.add(row)
            else:
                for k,v in values.items(): setattr(row,k,v)
                row.version+=1
            db.flush()
            route_id=row.id if model==m.CanonicalTransportRoute else row.route_id if model==m.VendorTransportService else get(db,m.VendorTransportService,row.vendor_service_id).route_id if model in (m.TransportRate,m.TransportSchedule) else None
            db.add(m.InternalAudit(actor_user_id=actor['id'],entity_type='transport_route' if route_id else 'transport_node',entity_id=route_id or row.id,action='updated' if id else 'created',summary=f'{model.__name__} '+('updated' if id else 'created')))
            result=schedule_view(row) if model==m.TransportSchedule else fields(row)
        return result
    except IntegrityError:
        raise HTTPException(409,'Duplicate or conflicting transportation record') from None

def search(db,origin,destination,travel_date,party_size,ready_time=None,buffer_minutes=0):
    if ready_time and ready_time.tzinfo: raise HTTPException(422,'Ready time must be Costa Rica local time without an offset')
    threshold=datetime.combine(travel_date,ready_time or time.min,ZONE)+timedelta(minutes=buffer_minutes)
    route=db.scalar(select(m.CanonicalTransportRoute).where(m.CanonicalTransportRoute.origin_node_id==origin,m.CanonicalTransportRoute.destination_node_id==destination,m.CanonicalTransportRoute.active.is_(True)))
    if not route or not all(get(db,m.TransportNode,id).active for id in (origin,destination)): return []
    result=[]
    for service in db.scalars(select(m.VendorTransportService).where(m.VendorTransportService.route_id==route.id,m.VendorTransportService.active.is_(True))):
        supplier=get(db,m.Supplier,service.supplier_id)
        if not supplier.active or (service.capacity is not None and service.capacity<party_size): continue
        for schedule in db.scalars(select(m.TransportSchedule).where(m.TransportSchedule.vendor_service_id==service.id,m.TransportSchedule.active.is_(True))):
            if not schedule.days_mask & (1<<travel_date.weekday()): continue
            if schedule.effective_from and travel_date<schedule.effective_from or schedule.effective_to and travel_date>schedule.effective_to: continue
            departure=datetime.combine(travel_date,schedule.departure_time,ZONE)
            if departure<threshold: continue
            result.append(dict(route_id=route.id,vendor_service_id=service.id,supplier_name=supplier.name,service_type=service.service_type,schedule=schedule_view(schedule),departure_at=departure,availability='unknown',confirmation_required=True,needs_review=stale(route.source_checked_at) or bool(route.review_notes) or stale(service.last_verified_at) or stale(schedule.last_verified_at)))
    return sorted(result,key=lambda r:r['departure_at'])

def generate_review_tasks(db,actor):
    created_before=set(db.scalars(select(m.OpsTask.id)))
    now=utcnow();today=now.astimezone(ZONE).date()
    for s in db.scalars(select(m.TransportSchedule).where(m.TransportSchedule.active.is_(True))):
        service=get(db,m.VendorTransportService,s.vendor_service_id);route=get(db,m.CanonicalTransportRoute,service.route_id)
        if not service.active or not route.active or not get(db,m.Supplier,service.supplier_id).active: continue
        if stale(s.last_verified_at,now) or not s.days_mask:
            stamp=s.last_verified_at.date().isoformat() if s.last_verified_at else 'unverified'
            name=get(db,m.TransportNode,route.origin_node_id).name+' → '+get(db,m.TransportNode,route.destination_node_id).name
            system_task(db,f'transport-schedule:{s.id}:{stamp}',f'Review {get(db,m.Supplier,service.supplier_id).name} schedule for {name}','transport_route',route.id)
    rates=list(db.scalars(select(m.TransportRate)));superseded={r.supersedes_id for r in rates}
    for r in rates:
        if r.id not in superseded and r.rate_kind=='vendor_rate' and today<=r.effective_to<=today+timedelta(days=30):
            service=get(db,m.VendorTransportService,r.vendor_service_id)
            if service.active and get(db,m.CanonicalTransportRoute,service.route_id).active and get(db,m.Supplier,service.supplier_id).active: system_task(db,f'transport-rate:{r.id}','Request updated transport rate','transport_route',service.route_id)
    added=len(set(db.scalars(select(m.OpsTask.id)))-created_before)
    db.add(m.InternalAudit(actor_user_id=actor['id'],entity_type='transport_review',entity_id=0,action='review_tasks',summary=f'Controlled transportation review generated {added} tasks'))
    db.commit()
    return {'tasks_created':added}
