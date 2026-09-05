"""INTERNAL DEVELOPMENT API. No authentication yet; do not expose in production."""
from fastapi import APIRouter, Depends, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..inventory_schemas import ImageInput, ImageRead, OpsTour, SupplierInput, SupplierRead, TourInput
from ..inventory_service import commit, remove_image, save_image, save_tour, supplier_or_404, tour_or_404, tours_query
from ..models import Product, Supplier


def private_response(response: Response):
    response.headers['Cache-Control'] = 'no-store'


router = APIRouter(prefix='/ops', tags=['Internal inventory — unauthenticated development only'], dependencies=[Depends(private_response)])


@router.get('/suppliers', response_model=list[SupplierRead])
def suppliers(db: Session = Depends(get_db)):
    return db.scalars(select(Supplier).order_by(Supplier.name, Supplier.id)).all()


@router.get('/suppliers/{supplier_id}', response_model=SupplierRead)
def supplier_detail(supplier_id: int, db: Session = Depends(get_db)):
    return supplier_or_404(db, supplier_id)


@router.post('/suppliers', response_model=SupplierRead, status_code=201)
def supplier_create(payload: SupplierInput, db: Session = Depends(get_db)):
    supplier = Supplier(**payload.model_dump())
    db.add(supplier)
    commit(db)
    db.refresh(supplier)
    return supplier


@router.put('/suppliers/{supplier_id}', response_model=SupplierRead)
def supplier_update(supplier_id: int, payload: SupplierInput, db: Session = Depends(get_db)):
    supplier = supplier_or_404(db, supplier_id)
    for key, value in payload.model_dump().items():
        setattr(supplier, key, value)
    commit(db)
    db.refresh(supplier)
    return supplier


@router.get('/tours', response_model=list[OpsTour])
def tours(db: Session = Depends(get_db)):
    return db.scalars(tours_query().order_by(Product.id)).all()


@router.get('/tours/{tour_id}', response_model=OpsTour)
def tour_detail(tour_id: int, db: Session = Depends(get_db)):
    return tour_or_404(db, tour_id)


@router.post('/tours', response_model=OpsTour, status_code=201)
def tour_create(payload: TourInput, db: Session = Depends(get_db)):
    return save_tour(db, payload)


@router.put('/tours/{tour_id}', response_model=OpsTour)
def tour_update(tour_id: int, payload: TourInput, db: Session = Depends(get_db)):
    return save_tour(db, payload, tour_id)


@router.get('/tours/{tour_id}/images', response_model=list[ImageRead])
def images(tour_id: int, db: Session = Depends(get_db)):
    return tour_or_404(db, tour_id).images


@router.post('/tours/{tour_id}/images', response_model=ImageRead, status_code=201)
def image_create(tour_id: int, payload: ImageInput, db: Session = Depends(get_db)):
    return save_image(db, tour_id, payload)


@router.put('/tours/{tour_id}/images/{image_id}', response_model=ImageRead)
def image_update(tour_id: int, image_id: int, payload: ImageInput, db: Session = Depends(get_db)):
    return save_image(db, tour_id, payload, image_id)


@router.delete('/tours/{tour_id}/images/{image_id}', status_code=204)
def image_delete(tour_id: int, image_id: int, db: Session = Depends(get_db)):
    remove_image(db, tour_id, image_id)
    return Response(status_code=204, headers={'Cache-Control': 'no-store'})
