"""Small internal reference-data commands; no inventory activation or pricing resolution."""
from fastapi import HTTPException
from sqlalchemy import delete, select, text

from .models import Destination, Product, ProductDestination, Supplier, SupplierService, SupplierAgreement, ProductRate, SupplierDocument


def required(db, model, identifier, lock=False):
    query = select(model).where(model.id == identifier)
    row = db.scalar(query.with_for_update() if lock else query)
    if row is None:
        raise HTTPException(404, 'Reference record not found')
    return row


def save_destination(db, payload, identifier=None):
    with db.begin():
        # Serialize tree edits, including two simultaneous reciprocal reparentings.
        # PostgreSQL is the supported deployed database; SQLite unit tests are sequential.
        if db.bind.dialect.name == 'postgresql':
            db.execute(text('LOCK TABLE destinations IN SHARE ROW EXCLUSIVE MODE'))
        row = required(db, Destination, identifier) if identifier else Destination()
        parent_id = payload.parent_id
        seen = {identifier} if identifier else set()
        while parent_id is not None:
            if parent_id in seen:
                raise HTTPException(409, 'A destination cannot be its own ancestor')
            seen.add(parent_id)
            parent_id = required(db, Destination, parent_id).parent_id
        for key, value in payload.model_dump().items():
            setattr(row, key, value)
        db.add(row)
        db.flush()
    return row


def product_destinations(db, product_id):
    required(db, Product, product_id)
    return db.scalars(select(Destination).join(ProductDestination).where(ProductDestination.product_id == product_id)
                      .order_by(Destination.sort_order, Destination.id)).all()


def map_destinations(db, product_id, payload):
    with db.begin():
        required(db, Product, product_id, lock=True)
        for identifier in payload.destination_ids:
            required(db, Destination, identifier)
        db.execute(delete(ProductDestination).where(ProductDestination.product_id == product_id))
        db.add_all([ProductDestination(product_id=product_id, destination_id=i) for i in payload.destination_ids])
    return product_destinations(db, product_id)


def supplier_profile(db, supplier_id):
    supplier = required(db, Supplier, supplier_id)
    return dict(relationship_status=supplier.relationship_status, service_types=list(db.scalars(
        select(SupplierService.service_type).where(SupplierService.supplier_id == supplier_id).order_by(SupplierService.service_type))))


def save_supplier_profile(db, supplier_id, payload):
    with db.begin():
        supplier = required(db, Supplier, supplier_id, lock=True)
        supplier.relationship_status = payload.relationship_status
        db.execute(delete(SupplierService).where(SupplierService.supplier_id == supplier_id))
        db.add_all([SupplierService(supplier_id=supplier_id, service_type=s) for s in payload.service_types])
    return supplier_profile(db, supplier_id)


def create_agreement(db, supplier_id, payload):
    with db.begin():
        required(db, Supplier, supplier_id)
        row = SupplierAgreement(supplier_id=supplier_id, **payload.model_dump())
        db.add(row)
        db.flush()
    return row


def create_rate(db, agreement_id, payload):
    with db.begin():
        agreement = required(db, SupplierAgreement, agreement_id)
        product = required(db, Product, payload.product_id, lock=True)
        if product.supplier_id != agreement.supplier_id:
            raise HTTPException(422, 'Product must belong to the agreement supplier when recording a rate')
        if payload.effective_from < agreement.effective_from or (agreement.effective_to and payload.effective_to > agreement.effective_to):
            raise HTTPException(422, 'Rate dates must fall within the agreement period')
        row = ProductRate(agreement_id=agreement_id, **payload.model_dump())
        db.add(row)
        db.flush()
    return row


def create_document(db, supplier_id, payload):
    with db.begin():
        required(db, Supplier, supplier_id)
        if payload.agreement_id:
            agreement = required(db, SupplierAgreement, payload.agreement_id)
            if agreement.supplier_id != supplier_id:
                raise HTTPException(422, 'Document and agreement must belong to the same supplier')
        row = SupplierDocument(supplier_id=supplier_id, **payload.model_dump())
        db.add(row)
        db.flush()
    return row
