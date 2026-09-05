from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..inventory_schemas import PublicTour
from ..inventory_service import tours_query
from ..models import Product

router = APIRouter(prefix='/public', tags=['Public inventory'])


@router.get('/tours', response_model=list[PublicTour])
def list_tours(response: Response, category: str | None = Query(default=None, max_length=80), featured: bool | None = None, db: Session = Depends(get_db)):
    response.headers['Cache-Control'] = 'no-store'
    query = tours_query().where(Product.active.is_(True))
    if category is not None:
        query = query.where(Product.category == category)
    if featured is not None:
        query = query.where(Product.featured == featured)
    return db.scalars(query.order_by(Product.id)).all()


@router.get('/tours/{slug}', response_model=PublicTour)
def tour_detail(slug: str, response: Response, db: Session = Depends(get_db)):
    response.headers['Cache-Control'] = 'no-store'
    tour = db.scalar(tours_query().where(Product.active.is_(True), Product.slug == slug))
    if tour is None:
        raise HTTPException(404, 'Tour not found')
    return tour
