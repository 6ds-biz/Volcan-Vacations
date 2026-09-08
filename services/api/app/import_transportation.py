"""Reviewed official RideCR universe; explicit insert-only import, dry-run by default."""
import argparse,json
from pathlib import Path
from datetime import datetime,time
from sqlalchemy import select,text
from .database import SessionLocal
from . import models as m
from .transport_schemas import RouteInput
DATA=Path(__file__).parent/'data/transportation-2026-09-07.json'

def load_catalog():return json.loads(DATA.read_text())
def import_catalog(db,data):
    # Serialize catalog applications; also protects vendor/node deduplication.
    if db.bind.dialect.name=='postgresql': db.execute(text("SELECT pg_advisory_xact_lock(860008)"))
    report=dict(nodes_created=0,routes_created=0,services_created=0,schedules_created=0,suppliers_created=0)
    checked=datetime.fromisoformat(data['checked_at'].replace('Z','+00:00'))
    suppliers={}
    for name in ('RideCR','Interbus'):
        matches=[s for s in db.scalars(select(m.Supplier)) if ''.join(s.name.lower().split())==name.lower()]
        if len(matches)>1:raise ValueError('Ambiguous supplier identity; resolve duplicate vendor names before import')
        row=matches[0] if matches else None
        if not row:
            row=m.Supplier(name=name,supplier_type='transportation',website='https://ridecr.com/' if name=='RideCR' else 'https://www.interbusonline.com/',notes='Existing vendor relationship reported by VV; commercial status and rates require operator entry.')
            db.add(row);db.flush();report['suppliers_created']+=1
        if not db.scalar(select(m.SupplierService).where(m.SupplierService.supplier_id==row.id,m.SupplierService.service_type=='transportation')):db.add(m.SupplierService(supplier_id=row.id,service_type='transportation'))
        suppliers[name]=row
    nodes={}
    for n in data['nodes']:
        matches=db.scalars(select(m.TransportNode).where((m.TransportNode.slug==n['slug']) | (m.TransportNode.name==n['name']))).all()
        if len(matches)>1:raise ValueError('Ambiguous transport node identity')
        row=matches[0] if matches else None
        if not row:
            dest=db.scalar(select(m.Destination).where(m.Destination.slug==n['destination_slug'])) if n['destination_slug'] else None
            row=m.TransportNode(slug=n['slug'],name=n['name'],node_type=n['node_type'],destination_id=dest.id if dest else None)
            db.add(row);db.flush();report['nodes_created']+=1
        nodes[n['slug']]=row
    for item in data['routes']:
        origin=nodes[item['origin']];destination=nodes[item['destination']]
        evidence=RouteInput(origin_node_id=origin.id,destination_node_id=destination.id,source_url=data['ridecr_source'],source_checked_at=checked,review_notes=item['review_notes'])
        route=db.scalar(select(m.CanonicalTransportRoute).where(m.CanonicalTransportRoute.origin_node_id==origin.id,m.CanonicalTransportRoute.destination_node_id==destination.id))
        if not route:
            route=m.CanonicalTransportRoute(**evidence.model_dump(exclude={'expected_version'}));db.add(route);db.flush();report['routes_created']+=1
        if route.source!='RideCR':raise ValueError('Canonical route conflicts with RideCR provenance')
        for name in ('RideCR','Interbus'):
            if name=='Interbus' and not item.get('interbus'):continue
            source=data['ridecr_source'] if name=='RideCR' else data['interbus_source']
            service=db.scalar(select(m.VendorTransportService).where(m.VendorTransportService.route_id==route.id,m.VendorTransportService.supplier_id==suppliers[name].id,m.VendorTransportService.service_type=='shared_shuttle'))
            if not service:
                service=m.VendorTransportService(route_id=route.id,supplier_id=suppliers[name].id,service_type='shared_shuttle',source_url=source,last_verified_at=checked)
                db.add(service);db.flush();report['services_created']+=1
            times=item['ridecr_departures'] if name=='RideCR' else [item['interbus']['departure']]
            for departure in times:
                key=f'{name}:{item["origin"]}:{item["destination"]}:{departure}'
                if db.scalar(select(m.TransportSchedule.id).where(m.TransportSchedule.import_key==key)):continue
                # Never overlay a matching operator-entered departure.
                if db.scalar(select(m.TransportSchedule.id).where(m.TransportSchedule.vendor_service_id==service.id,m.TransportSchedule.departure_time==time.fromisoformat(departure))):continue
                db.add(m.TransportSchedule(vendor_service_id=service.id,departure_time=time.fromisoformat(departure),days_mask=127 if name=='RideCR' else 0,source_url=source,last_verified_at=checked,import_key=key,estimated_duration_minutes=item['interbus']['duration_minutes'] if name=='Interbus' else None,seasonal_notes='Daily routes stated on RideCR shuttle page; publication effective dates not supplied.' if name=='RideCR' else 'Weekdays/effective period not published in route table. Confirm recurrence before date-specific recommendation.'))
                report['schedules_created']+=1
    db.flush()
    return report

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    data=load_catalog()
    with SessionLocal() as db:
        report=import_catalog(db,data)
        report.update(mode='apply' if args.apply else 'dry-run',canonical_routes=len(data['routes']),interbus_overlap=sum(bool(r['interbus']) for r in data['routes']),vendor_rates_imported=0)
        if args.apply:
            db.add(m.InternalAudit(actor_user_id=None,entity_type='transport_import',entity_id=0,action='catalog_import',summary='Reviewed RideCR catalog and Interbus overlap applied from trusted console; insert-only.'))
            db.commit()
        else:db.rollback()
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
