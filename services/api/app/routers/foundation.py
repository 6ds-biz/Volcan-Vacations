"""Authenticated foundation API. Hosted mounting requires explicit Operations opt-in."""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..database import get_db
from .. import foundation_service as service
from ..foundation_schemas import DestinationInput, DestinationRead, DestinationLinks, SupplierFoundation, AgreementInput, AgreementRead, RateInput, RateRead, DocumentInput, DocumentRead
from ..models import Destination, Supplier, SupplierAgreement, ProductRate, SupplierDocument
from .ops import private_response

router = APIRouter(prefix='/ops', tags=['Internal platform reference data'], dependencies=[Depends(private_response)])


def command(db, function, *args):
    try:
        return function(db, *args)
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, 'Reference data conflicts with an existing record or relationship') from None


@router.get('/destinations', response_model=list[DestinationRead])
def destinations(db: Session = Depends(get_db)):
    return db.scalars(select(Destination).order_by(Destination.sort_order, Destination.id)).all()


@router.post('/destinations', response_model=DestinationRead, status_code=201)
def create_destination(payload: DestinationInput, db: Session = Depends(get_db)):
    return command(db, service.save_destination, payload)


@router.put('/destinations/{destination_id}', response_model=DestinationRead)
def update_destination(destination_id: int, payload: DestinationInput, db: Session = Depends(get_db)):
    return command(db, service.save_destination, payload, destination_id)


@router.get('/products/{product_id}/destinations', response_model=list[DestinationRead])
def product_destinations(product_id: int, db: Session = Depends(get_db)):
    return service.product_destinations(db, product_id)


@router.put('/products/{product_id}/destinations', response_model=list[DestinationRead])
def map_destinations(product_id: int, payload: DestinationLinks, db: Session = Depends(get_db)):
    return command(db, service.map_destinations, product_id, payload)


@router.get('/suppliers/{supplier_id}/foundation', response_model=SupplierFoundation)
def supplier_profile(supplier_id: int, db: Session = Depends(get_db)):
    return service.supplier_profile(db, supplier_id)


@router.put('/suppliers/{supplier_id}/foundation', response_model=SupplierFoundation)
def update_supplier_profile(supplier_id: int, payload: SupplierFoundation, db: Session = Depends(get_db)):
    return command(db, service.save_supplier_profile, supplier_id, payload)


@router.get('/suppliers/{supplier_id}/agreements', response_model=list[AgreementRead])
def agreements(supplier_id: int, db: Session = Depends(get_db)):
    service.required(db, Supplier, supplier_id)
    return db.scalars(select(SupplierAgreement).where(SupplierAgreement.supplier_id == supplier_id).order_by(SupplierAgreement.id)).all()


@router.post('/suppliers/{supplier_id}/agreements', response_model=AgreementRead, status_code=201)
def create_agreement(supplier_id: int, payload: AgreementInput, request: Request, db: Session = Depends(get_db)):
    if payload.status == 'approved':
        from ..permissions import demand
        demand(request.state.actor, 'commercial.approve')
    return command(db, service.create_agreement, supplier_id, payload)


@router.get('/agreements/{agreement_id}/rates', response_model=list[RateRead])
def rates(agreement_id: int, db: Session = Depends(get_db)):
    service.required(db, SupplierAgreement, agreement_id)
    return db.scalars(select(ProductRate).where(ProductRate.agreement_id == agreement_id).order_by(ProductRate.id)).all()


@router.post('/agreements/{agreement_id}/rates', response_model=RateRead, status_code=201)
def create_rate(agreement_id: int, payload: RateInput, db: Session = Depends(get_db)):
    return command(db, service.create_rate, agreement_id, payload)


@router.get('/suppliers/{supplier_id}/documents', response_model=list[DocumentRead])
def documents(supplier_id: int, db: Session = Depends(get_db)):
    service.required(db, Supplier, supplier_id)
    return db.scalars(select(SupplierDocument).where(SupplierDocument.supplier_id == supplier_id).order_by(SupplierDocument.id)).all()


@router.post('/suppliers/{supplier_id}/documents', response_model=DocumentRead, status_code=201)
def create_document(supplier_id: int, payload: DocumentInput, db: Session = Depends(get_db)):
    return command(db, service.create_document, supplier_id, payload)
