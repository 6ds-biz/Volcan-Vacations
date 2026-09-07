"""Authenticated identity, user administration and scoped work APIs."""
from datetime import date, timedelta
from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy import select, delete, func, text
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from .. import models as m
from ..internal_auth import require_ops, login, COOKIE, digest, HASHER, verify_password
from ..internal_schemas import Credentials, UserCreate, UserUpdate, UserRead, PasswordChange, TaskInput, TaskUpdate, Assignment, Followup, TaskStatus, Priority
from ..permissions import can, demand, DEFAULT_PROFILES
from ..availability_rules import utcnow, aware
from .. import task_service as tasks

login_router=APIRouter(prefix='/ops/auth',tags=['Internal authentication'])
router=APIRouter(prefix='/ops',tags=['Authenticated Operations'])

@login_router.post('/login')
def sign_in(payload: Credentials,request: Request,response: Response,db=Depends(get_db)):
    return login(db,payload,request,response)

@router.get('/auth/me')
def me(request: Request):
    return dict(user=request.state.actor,csrf_token=request.state.csrf_token)

@router.post('/auth/logout',status_code=204)
def logout(request: Request,response: Response,db=Depends(get_db)):
    with db.begin(): db.execute(delete(m.InternalSession).where(m.InternalSession.token_hash==digest(request.cookies.get(COOKIE,''))))
    response.delete_cookie(COOKIE,path='/',secure=request.app.state.config.environment!='development',httponly=True,samesite='strict')

@router.post('/auth/password',status_code=204)
def password(payload: PasswordChange,request: Request,response: Response,db=Depends(get_db)):
    with db.begin():
        user=db.scalar(select(m.InternalUser).where(m.InternalUser.id==request.state.actor['id']).with_for_update())
        if not verify_password(user.password_hash,payload.current_password): raise HTTPException(400,'Current password is incorrect')
        user.password_hash=HASHER.hash(payload.new_password);user.must_change_password=False
        db.execute(delete(m.InternalSession).where(m.InternalSession.user_id==user.id))
    response.delete_cookie(COOKIE,path='/')

@router.get('/users',response_model=list[UserRead])
def users(db=Depends(get_db)):
    return db.scalars(select(m.InternalUser).order_by(m.InternalUser.display_name)).all()

@router.get('/directory')
def directory(db=Depends(get_db)):
    return [dict(id=u.id,display_name=u.display_name,role=u.role) for u in db.scalars(select(m.InternalUser).where(m.InternalUser.active.is_(True)).order_by(m.InternalUser.display_name))]

@router.post('/users',response_model=UserRead,status_code=201)
def create_user(payload: UserCreate,db=Depends(get_db)):
    try:
        with db.begin():
            user=m.InternalUser(email=payload.email,display_name=payload.display_name.strip(),role=payload.role,
                dashboard_profile=payload.dashboard_profile or DEFAULT_PROFILES[payload.role],password_hash=HASHER.hash(payload.password),must_change_password=True)
            db.add(user);db.flush()
        return user
    except IntegrityError:
        raise HTTPException(409,'A user with this email already exists') from None

@router.put('/users/{user_id}',response_model=UserRead)
def update_user(user_id:int,payload:UserUpdate,db=Depends(get_db)):
    with db.begin():
        # Serialize owner membership changes, including concurrent demotions.
        if db.bind.dialect.name=='postgresql': db.execute(text('LOCK TABLE internal_users IN SHARE ROW EXCLUSIVE MODE'))
        user=db.get(m.InternalUser,user_id)
        if not user: raise HTTPException(404,'User not found')
        owners=db.scalar(select(func.count()).select_from(m.InternalUser).where(m.InternalUser.active.is_(True),m.InternalUser.role=='owner_admin'))
        if user.active and user.role=='owner_admin' and (not payload.active or payload.role!='owner_admin') and owners<=1:
            raise HTTPException(409,'The last active owner must remain active')
        for key,value in payload.model_dump().items(): setattr(user,key,value)
        db.execute(delete(m.InternalSession).where(m.InternalSession.user_id==user_id))
    return user

@router.get('/tasks')
def task_list(request:Request,mine:bool=False,shared:bool=False,assigned_user_id:int|None=None,
    status:TaskStatus|None=None,priority:Priority|None=None,overdue:bool=False,due:date|None=None,
    related_entity_type:str|None=None,related_entity_id:int|None=None,search:str='',db=Depends(get_db)):
    actor=request.state.actor;q=select(m.OpsTask).where(tasks.task_scope(actor))
    if mine: q=q.where(m.OpsTask.assigned_user_id==actor['id'])
    if shared: q=q.where(m.OpsTask.assigned_user_id.is_(None))
    if assigned_user_id: q=q.where(m.OpsTask.assigned_user_id==assigned_user_id)
    if status: q=q.where(m.OpsTask.status==status)
    if priority: q=q.where(m.OpsTask.priority==priority)
    if overdue: q=q.where(m.OpsTask.due_at<utcnow(),m.OpsTask.status.in_(tasks.OPEN))
    if due: q=q.where(func.date(m.OpsTask.due_at)==due)
    if related_entity_type: q=q.where(m.OpsTask.related_entity_type==related_entity_type)
    if related_entity_id: q=q.where(m.OpsTask.related_entity_id==related_entity_id)
    if search: q=q.where(m.OpsTask.title.ilike('%'+search[:200]+'%'))
    return [tasks.present_task(db,t) for t in db.scalars(q.order_by(m.OpsTask.created_at.desc(),m.OpsTask.id.desc())).all()]

@router.get('/tasks/{task_id}')
def task_detail(task_id:int,request:Request,db=Depends(get_db)):
    return tasks.present_task(db,tasks.task_read(db,request.state.actor,task_id))

@router.post('/tasks',status_code=201)
def create_task(payload:TaskInput,request:Request,db=Depends(get_db)):
    with db.begin():
        values=payload.model_dump();tasks.validate_task(db,request.state.actor,values)
        task=m.OpsTask(**values,created_by_user_id=request.state.actor['id'],source='manual')
        if task.status=='completed': task.completed_at=utcnow();task.completed_by_user_id=request.state.actor['id']
        db.add(task);db.flush()
    return tasks.present_task(db,task)

@router.put('/tasks/{task_id}')
def update_task(task_id:int,payload:TaskUpdate,request:Request,db=Depends(get_db)):
    with db.begin():
        task=tasks.task_read(db,request.state.actor,task_id,lock=True)
        if task.version!=payload.expected_version: raise HTTPException(409,'Task changed. Reload before saving')
        values=payload.model_dump(exclude={'expected_version'});tasks.validate_task(db,request.state.actor,values,task)
        for key,value in values.items(): setattr(task,key,value)
        task.version+=1
        if task.status=='completed' and task.completed_at is None:
            task.completed_at=utcnow();task.completed_by_user_id=request.state.actor['id']
        elif task.status!='completed':
            task.completed_at=None;task.completed_by_user_id=None
    return tasks.present_task(db,task)

@router.get('/work/bookings')
def work_bookings(request:Request,db=Depends(get_db)):
    return [safe_booking(row) for row in db.scalars(select(m.Reservation).where(tasks.booking_scope(request.state.actor)).order_by(m.Reservation.id.desc()))]

def safe_booking(row):
    return dict(id=row.id,reference=row.trip.reference,tour_name=row.tour_name_snapshot or row.product.name,
        requested_date=row.reservation_date,quantity=row.quantity,status=row.status,version=row.version,
        supplier_confirmation_status=row.supplier_confirmation_status,availability_status=row.availability_status,assigned_user_id=row.assigned_user_id,
        internal_notes=row.internal_notes,customer_notes=row.customer_notes,
        contact=row.contact_snapshot,product_id=row.product_id)

@router.get('/work/bookings/{booking_id}')
def work_booking(booking_id:int,request:Request,db=Depends(get_db)):
    return safe_booking(tasks.scoped_booking(db,request.state.actor,booking_id))

@router.put('/work/bookings/{booking_id}/followup')
def work_followup(booking_id:int,payload:Followup,request:Request,db=Depends(get_db)):
    with db.begin():
        row=tasks.scoped_booking(db,request.state.actor,booking_id,True)
        if row.version!=payload.expected_version: raise HTTPException(409,'Booking changed. Reload before saving')
        row.internal_notes=payload.internal_notes;row.version+=1
    return safe_booking(row)

@router.put('/bookings/{booking_id}/assignment')
def assign_booking(booking_id:int,payload:Assignment,request:Request,db=Depends(get_db)):
    with db.begin():
        row=tasks.scoped_booking(db,request.state.actor,booking_id,True)
        if row.version!=payload.expected_version: raise HTTPException(409,'Booking changed. Reload before saving')
        if payload.assigned_user_id:
            user=db.get(m.InternalUser,payload.assigned_user_id)
            if not user or not user.active: raise HTTPException(422,'Choose an active user')
        row.assigned_user_id=payload.assigned_user_id;row.version+=1
    return safe_booking(row)

@router.get('/work/bookings/{booking_id}/availability')
def work_availability(booking_id:int,request:Request,db=Depends(get_db)):
    from ..availability_service import public_availability
    row=tasks.scoped_booking(db,request.state.actor,booking_id)
    return public_availability(db,row.product.slug,row.reservation_date)

@router.get('/audit')
def audit(entity_type:str,entity_id:int,request:Request,db=Depends(get_db)):
    if entity_type=='user': demand(request.state.actor,'users.manage')
    if entity_type=='task': tasks.task_read(db,request.state.actor,entity_id)
    rows=db.execute(select(m.InternalAudit,m.InternalUser.display_name).outerjoin(m.InternalUser,m.InternalAudit.actor_user_id==m.InternalUser.id)
        .where(m.InternalAudit.entity_type==entity_type,m.InternalAudit.entity_id==entity_id).order_by(m.InternalAudit.id.desc())).all()
    return [dict(id=r.id,summary=r.summary,action=r.action,actor_name=name or 'System',created_at=r.created_at) for r,name in rows]

from ..availability_schemas import SupplierEventInput
@router.post('/work/bookings/{booking_id}/availability')
def work_check(booking_id:int,payload:SupplierEventInput,request:Request,db=Depends(get_db)):
    from ..availability_service import record_supplier_event
    if payload.event_type!='availability_checked': raise HTTPException(403,'Only availability checks are permitted here')
    record_supplier_event(db,booking_id,payload,work_actor=request.state.actor)
    return safe_booking(tasks.scoped_booking(db,request.state.actor,booking_id))

@router.get('/customers')
def customers(db=Depends(get_db)):
    from ..booking_schemas import CustomerRead
    return [dict(**CustomerRead.model_validate(c).model_dump(),trip_ids=list(db.scalars(select(m.Trip.id).where(m.Trip.customer_id==c.id)))) for c in db.scalars(select(m.Customer).order_by(m.Customer.last_name,m.Customer.id))]

@router.get('/trips')
def trips(db=Depends(get_db)):
    from ..booking_schemas import TripRead
    return [dict(**TripRead.model_validate(t).model_dump(),customer_id=t.customer_id,customer_name=f'{t.customer.first_name} {t.customer.last_name}',
        bookings=[dict(id=r.id,tour=r.tour_name_snapshot or r.product.name,status=r.status) for r in db.scalars(select(m.Reservation).where(m.Reservation.trip_id==t.id))]) for t in db.scalars(select(m.Trip).order_by(m.Trip.id.desc()))]

@router.get('/agreements')
def agreement_list(db=Depends(get_db)):
    from ..foundation_schemas import AgreementRead
    return [dict(**AgreementRead.model_validate(a).model_dump(),supplier_name=db.get(m.Supplier,a.supplier_id).name,
        rate_count=db.scalar(select(func.count()).select_from(m.ProductRate).where(m.ProductRate.agreement_id==a.id))) for a in db.scalars(select(m.SupplierAgreement).order_by(m.SupplierAgreement.id.desc()))]

@router.get('/directory/inventory')
def inventory_context(db=Depends(get_db)):
    destinations={d.id:d.name for d in db.scalars(select(m.Destination))}
    links={}
    for link in db.scalars(select(m.ProductDestination)):
        links.setdefault(link.product_id,[]).append(dict(id=link.destination_id,name=destinations[link.destination_id]))
    suppliers=[]
    for s in db.scalars(select(m.Supplier)):
        products=list(db.scalars(select(m.Product.id).where(m.Product.supplier_id==s.id)))
        dest={d['id']:d for p in products for d in links.get(p,[])}
        suppliers.append(dict(id=s.id,relationship_status=s.relationship_status,
            services=list(db.scalars(select(m.SupplierService.service_type).where(m.SupplierService.supplier_id==s.id))),
            agreement_count=db.scalar(select(func.count()).select_from(m.SupplierAgreement).where(m.SupplierAgreement.supplier_id==s.id)),destinations=list(dest.values())))
    return dict(product_destinations=links,suppliers=suppliers,destinations=[dict(id=id,name=name) for id,name in destinations.items()])

@router.get('/dashboard')
def dashboard(request:Request,db=Depends(get_db)):
    from ..availability_rules import is_stale
    actor=request.state.actor;now=utcnow();today=now.date()
    work=list(db.scalars(select(m.OpsTask).where(tasks.task_scope(actor))))
    mine=[t for t in work if t.assigned_user_id==actor['id'] and t.status in tasks.OPEN]
    def rank(t):
        due=aware(t.due_at)
        return (0 if t.priority=='urgent' else 1 if due and due<now else 2 if due and due.date()==today else 3,due or now+timedelta(days=36500),t.id)
    bookings=list(db.scalars(select(m.Reservation).where(tasks.booking_scope(actor))))
    active=[b for b in bookings if b.status not in ('cancelled','completed')]
    attention=[]
    def item(key,label,count,href):
        if count: attention.append(dict(key=key,label=label,count=count,href=href))
    own_overdue=[t for t in work if t.status in tasks.OPEN and t.due_at and aware(t.due_at)<now]
    item('tasks','Overdue tasks',len(own_overdue),'/tasks?overdue=true')
    result=dict(profile=actor['dashboard_profile'],my_tasks=[tasks.present_task(db,t) for t in sorted(mine,key=rank)[:6]],
        task_counts=dict(my_open=len(mine),due_today=sum(bool(t.due_at and aware(t.due_at).date()==today and t.status in tasks.OPEN) for t in work),
            overdue=len(own_overdue),waiting=sum(t.status=='waiting' for t in work),shared=sum(t.assigned_user_id is None and t.status in tasks.OPEN for t in work)),
        attention=attention,assigned_bookings=[safe_booking(b) for b in active[:8]])
    if not can(actor,'bookings.read'): return result
    paid=lambda b: bool(b.payment and b.payment.paid_at)
    result['booking_counts']=dict(new=sum(b.status=='new' for b in bookings),awaiting_supplier=sum(b.supplier_confirmation_status=='awaiting_supplier' for b in active),
        ready=sum(b.ready_for_payment and b.trip.status not in ('cancelled','completed') and not paid(b) for b in active),paid=sum(paid(b) for b in bookings))
    # Mutually exclusive booking attention reasons; never add a misleading combined total.
    declined=[b for b in active if b.supplier_confirmation_status=='declined']
    item('declined','Supplier declined · alternatives needed',len(declined),'/bookings?view=declined')
    item('new','New booking requests',sum(b.status=='new' and b not in declined for b in active),'/bookings?view=new')
    item('awaiting','Awaiting supplier response',sum(b.supplier_confirmation_status=='awaiting_supplier' and b.status!='new' for b in active),'/bookings?view=awaiting_supplier')
    availability=list(db.scalars(select(m.Availability).where(m.Availability.date>=today)))
    stale=sum(is_stale(a.last_checked_at) for a in availability)
    item('availability','Upcoming availability needs rechecking',stale,'/availability')
    payments=list(db.scalars(select(m.Payment)))
    item('payments','Payment exceptions',sum(p.status=='failed' or p.reconciliation_required for p in payments),'/payments?view=exceptions')
    agreements=list(db.scalars(select(m.SupplierAgreement)))
    item('agreements','Agreements in review',sum(a.status=='in_review' for a in agreements),'/agreements?status=in_review')
    suppliers=list(db.scalars(select(m.Supplier).where(m.Supplier.active.is_(True))))
    result['vendor_counts']={status:sum(s.relationship_status==status for s in suppliers) for status in ('prospect','contacted','rates_requested','rates_received','contracted')}
    tours=list(db.scalars(select(m.Product).where(m.Product.product_type=='tour')))
    result['inventory_counts']=dict(active=sum(t.active for t in tours),needs_review=sum(t.active and (not t.primary_image or not t.short_description) for t in tours),suppliers=len(suppliers),stale_availability=stale)
    result['recent_payments']=[dict(id=p.id,amount=str(p.amount),currency=p.currency,status=p.status,paid_at=p.paid_at,
        reservation_id=p.reservation_id) for p in sorted((p for p in payments if p.paid_at),key=lambda p:aware(p.paid_at),reverse=True)[:5]]
    return result
