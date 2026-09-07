"""Append-only, sanitized audit entries; historical records are untouched."""
from sqlalchemy import event, inspect
from sqlalchemy.orm import Session
from . import models as m

KINDS={m.Reservation:'booking',m.SupplierConfirmationEvent:'supplier_confirmation',m.OpsTask:'task',
    m.InternalUser:'user',m.Supplier:'supplier',m.Availability:'availability',m.SupplierAgreement:'agreement'}

@event.listens_for(Session,'before_flush')
def actors(db,context,instances):
    actor=db.info.get('actor_id')
    for row in db.new:
        if isinstance(row,m.SupplierConfirmationEvent): row.actor_user_id=actor

@event.listens_for(Session,'after_flush')
def history(db,context):
    actor=db.info.get('actor_id')
    for row in list(db.new)+list(db.dirty):
        kind=KINDS.get(type(row))
        if not kind or (row not in db.new and not db.is_modified(row,include_collections=False)): continue
        if actor is None: continue
        state=inspect(row)
        changes=[k for k in ('status','active','role','dashboard_profile','assigned_user_id') if k in state.attrs and state.attrs[k].history.has_changes()]
        action='created' if row in db.new else 'updated'
        summary=f'{kind.replace("_"," ").capitalize()} {action}'
        if changes: summary+=': '+', '.join(changes)
        db.add(m.InternalAudit(actor_user_id=actor,entity_type=kind,entity_id=row.id,action=action,summary=summary))

@event.listens_for(Session,'after_flush')
def generated_work(db,context):
    from .task_service import system_task
    for row in list(db.new)+list(db.dirty):
        if isinstance(row,m.Reservation) and row in db.new:
            system_task(db,f'booking-review:{row.id}','Review booking and check availability','booking',row.id)
        elif isinstance(row,m.SupplierConfirmationEvent) and row in db.new and row.event_type=='declined':
            system_task(db,f'booking-declined:{row.reservation_id}','Contact customer with alternative','booking',row.reservation_id)
        elif isinstance(row,m.Payment) and row.status=='failed':
            system_task(db,f'payment-failed:{row.id}','Review payment issue','payment',row.id,owner=True)
        elif isinstance(row,m.SupplierAgreement) and row.status=='in_review':
            system_task(db,f'agreement-review:{row.id}','Review vendor rates','agreement',row.id,owner=True)
