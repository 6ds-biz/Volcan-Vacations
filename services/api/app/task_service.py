"""Scoped work queues; idempotent tasks are committed with their business event."""
from fastapi import HTTPException
from sqlalchemy import select, func, or_
from . import models as m
from .permissions import can, demand
from .availability_rules import utcnow, aware

OPEN = ('open','in_progress','waiting')
ENTITIES = {'booking':m.Reservation,'supplier':m.Supplier,'tour':m.Product,'payment':m.Payment,
    'transport_route':m.CanonicalTransportRoute,'availability':m.Availability,'agreement':m.SupplierAgreement,'customer':m.Customer}

def booking_scope(actor):
    if can(actor,'bookings.read'): return True
    return or_(m.Reservation.assigned_user_id==actor['id'],m.Reservation.id.in_(select(m.OpsTask.related_entity_id).where(
        m.OpsTask.assigned_user_id==actor['id'],m.OpsTask.related_entity_type=='booking',m.OpsTask.status.in_(OPEN))))

def scoped_booking(db,actor,id,lock=False):
    query=select(m.Reservation).where(m.Reservation.id==id,booking_scope(actor))
    row=db.scalar(query.with_for_update() if lock else query)
    if not row: raise HTTPException(404,'Booking not found')
    return row

def task_scope(actor):
    if can(actor,'users.manage'): return True
    if can(actor,'tasks.update_all'): return m.OpsTask.queue_role=='operations'
    return (m.OpsTask.assigned_user_id==actor['id']) & (m.OpsTask.queue_role=='operations')

def task_read(db,actor,id,lock=False):
    q=select(m.OpsTask).where(m.OpsTask.id==id,task_scope(actor))
    task=db.scalar(q.with_for_update() if lock else q)
    if not task: raise HTTPException(404,'Task not found')
    return task

def related_allowed(db,actor,kind,id):
    if kind is None: return
    model=ENTITIES[kind]
    if not db.get(model,id): raise HTTPException(422,'Related record does not exist')
    if can(actor,'bookings.read'): return
    if kind=='booking': scoped_booking(db,actor,id); return
    if kind=='availability':
        row=db.get(model,id)
        if db.scalar(select(m.Reservation.id).where(booking_scope(actor),m.Reservation.product_id==row.product_id,m.Reservation.reservation_date==row.date)): return
    raise HTTPException(403,'This related record is outside your work scope')

def validate_task(db,actor,values,previous=None):
    if values['queue_role']=='owner_admin': demand(actor,'users.manage')
    target=values['assigned_user_id']
    if not can(actor,'tasks.assign'):
        if target!=actor['id']: raise HTTPException(403,'You may only manage your own tasks')
        if previous and (values['related_entity_type'],values['related_entity_id'])!=(previous.related_entity_type,previous.related_entity_id):
            raise HTTPException(403,'Only an Operations manager can change task relationships')
    related_allowed(db,actor,values['related_entity_type'],values['related_entity_id'])
    if target:
        user=db.get(m.InternalUser,target)
        if not user or not user.active: raise HTTPException(422,'Choose an active assignee')
        if values['queue_role']=='owner_admin' and user.role!='owner_admin': raise HTTPException(422,'Owner queue requires an owner assignee')
        if user.role=='staff' and values['related_entity_type'] not in (None,'booking','availability'):
            raise HTTPException(422,'Staff may only receive tasks within their work scope')
        # Assigning a booking task explicitly grants relevant-booking scope.
        if user.role=='staff' and values['related_entity_type']=='availability':
            related_allowed(db,{'id':user.id,'role':user.role},values['related_entity_type'],values['related_entity_id'])

def present_task(db,task):
    fields=('id','title','description','assigned_user_id','created_by_user_id','completed_by_user_id',
        'related_entity_type','related_entity_id','priority','status','source','queue_role','due_at','created_at','updated_at','completed_at','version')
    result={key:getattr(task,key) for key in fields}
    for key in ('assigned','created_by','completed_by'):
        user=db.get(m.InternalUser,result[key+'_user_id']) if result[key+'_user_id'] else None
        result[key+'_name']=user.display_name if user else None
    return result

def system_task(db,key,title,kind,id,owner=False):
    role='owner_admin' if owner else 'operations_partner'
    users=db.scalars(select(m.InternalUser).where(m.InternalUser.active.is_(True),m.InternalUser.role==role).order_by(m.InternalUser.id)).all()
    loads={u.id:db.scalar(select(func.count()).select_from(m.OpsTask).where(m.OpsTask.assigned_user_id==u.id,m.OpsTask.status.in_(OPEN))) for u in users}
    assignee=min(users,key=lambda u:(loads[u.id],u.id)).id if users else None
    if db.bind.dialect.name=='postgresql':
        from sqlalchemy.dialects.postgresql import insert
    else:
        from sqlalchemy.dialects.sqlite import insert
    db.execute(insert(m.OpsTask).values(title=title,source='system_generated',system_key=key,
        related_entity_type=kind,related_entity_id=id,assigned_user_id=assignee,
        queue_role='owner_admin' if owner else 'operations',priority='high' if owner else 'normal',status='open',version=1)
        .on_conflict_do_nothing(index_elements=['system_key']))
