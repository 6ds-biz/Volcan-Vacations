from datetime import date,time
from fastapi import APIRouter,Depends,Query,Request
from sqlalchemy import select
from ..database import get_db
from .. import models as m
from ..permissions import can,demand
from ..transport_schemas import NodeInput,RouteInput,ServiceInput,ScheduleInput,RateInput
from .. import transport_service as service
router=APIRouter(prefix='/ops/transportation',tags=['Internal transportation'])

@router.get('/nodes')
def nodes(request:Request,db=Depends(get_db)):
    result=[service.fields(n) for n in db.scalars(select(m.TransportNode).order_by(m.TransportNode.name))]
    if not can(request.state.actor,'transport.manage'):
        for r in result:r.pop('notes',None)
    return result

@router.get('/context')
def context(request:Request,db=Depends(get_db)):
    demand(request.state.actor,'transport.manage')
    return dict(destinations=[dict(id=d.id,name=d.name) for d in db.scalars(select(m.Destination))],suppliers=[dict(id=s.id,name=s.name) for s in db.scalars(select(m.Supplier).where(m.Supplier.id.in_(select(m.SupplierService.supplier_id).where(m.SupplierService.service_type=='transportation'))))],agreements=[dict(id=a.id,supplier_id=a.supplier_id,title=a.title,currency=a.currency) for a in db.scalars(select(m.SupplierAgreement))])

@router.get('/routes')
def routes(request:Request,db=Depends(get_db)):
    return [service.route_view(db,r,can(request.state.actor,'transport.rates')) for r in db.scalars(select(m.CanonicalTransportRoute).order_by(m.CanonicalTransportRoute.id))]

@router.get('/routes/{id}')
def detail(id:int,request:Request,db=Depends(get_db)):
    return service.route_view(db,service.get(db,m.CanonicalTransportRoute,id),can(request.state.actor,'transport.rates'),True)

@router.get('/search')
def search(origin:int,destination:int,travel_date:date,party_size:int=Query(ge=1,le=1000),ready_time:time|None=None,buffer_minutes:int=Query(default=0,ge=0,le=720),db=Depends(get_db)):
    return service.search(db,origin,destination,travel_date,party_size,ready_time,buffer_minutes)

@router.post('/nodes',status_code=201)
def create_node(payload:NodeInput,request:Request,db=Depends(get_db)):return service.save(db,m.TransportNode,payload,request.state.actor)
@router.put('/nodes/{id}')
def edit_node(id:int,payload:NodeInput,request:Request,db=Depends(get_db)):return service.save(db,m.TransportNode,payload,request.state.actor,id)
@router.post('/routes',status_code=201)
def create_route(payload:RouteInput,request:Request,db=Depends(get_db)):return service.save(db,m.CanonicalTransportRoute,payload,request.state.actor)
@router.put('/routes/{id}')
def edit_route(id:int,payload:RouteInput,request:Request,db=Depends(get_db)):return service.save(db,m.CanonicalTransportRoute,payload,request.state.actor,id)
@router.post('/services',status_code=201)
def create_service(payload:ServiceInput,request:Request,db=Depends(get_db)):return service.save(db,m.VendorTransportService,payload,request.state.actor)
@router.put('/services/{id}')
def edit_service(id:int,payload:ServiceInput,request:Request,db=Depends(get_db)):return service.save(db,m.VendorTransportService,payload,request.state.actor,id)
@router.post('/schedules',status_code=201)
def create_schedule(payload:ScheduleInput,request:Request,db=Depends(get_db)):return service.save(db,m.TransportSchedule,payload,request.state.actor)
@router.put('/schedules/{id}')
def edit_schedule(id:int,payload:ScheduleInput,request:Request,db=Depends(get_db)):return service.save(db,m.TransportSchedule,payload,request.state.actor,id)
@router.post('/rates',status_code=201)
def create_rate(payload:RateInput,request:Request,db=Depends(get_db)):
    demand(request.state.actor,'transport.rates')
    return service.save(db,m.TransportRate,payload,request.state.actor)
@router.post('/review-tasks')
def review_tasks(request:Request,db=Depends(get_db)):return service.generate_review_tasks(db,request.state.actor)
