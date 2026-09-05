from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from .models import Product, ProductImage, Supplier


def commit(db: Session):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, 'Inventory conflict. Check the unique slug and referenced supplier.')


def supplier_or_404(db: Session, supplier_id: int):
    supplier = db.get(Supplier, supplier_id)
    if supplier is None:
        raise HTTPException(404, 'Supplier not found')
    return supplier


def tours_query():
    return select(Product).where(Product.product_type == 'tour').options(selectinload(Product.images), selectinload(Product.supplier))


def tour_or_404(db: Session, tour_id: int, lock: bool = False):
    query = tours_query().where(Product.id == tour_id)
    if lock:
        # Serialize gallery mutations per product; partial unique index is the backstop.
        query = query.with_for_update()
    tour = db.scalar(query)
    if tour is None:
        raise HTTPException(404, 'Tour not found')
    return tour


def save_tour(db: Session, payload, tour_id: int | None = None):
    supplier_or_404(db, payload.supplier_id)
    tour = tour_or_404(db, tour_id, lock=True) if tour_id else Product()
    for key, value in payload.model_dump().items():
        setattr(tour, key, value)
    db.add(tour)
    commit(db)
    return tour_or_404(db, tour.id)


def owned_image(tour, image_id):
    image = next((image for image in tour.images if image.id == image_id), None)
    if image is None:
        raise HTTPException(404, 'Image not found for this tour')
    return image


def save_image(db: Session, tour_id, payload, image_id=None):
    tour = tour_or_404(db, tour_id, lock=True)
    image = owned_image(tour, image_id) if image_id else ProductImage(product_id=tour.id)
    # Galleries always have one primary while nonempty. Unchecking the primary
    # alone retains it; select a different image to switch primary atomically.
    make_primary = payload.is_primary or not tour.images or bool(image.is_primary)
    if make_primary:
        for other in tour.images:
            other.is_primary = False
        db.flush()  # clear old primary before setting the new one (unique index)
    for key, value in payload.model_dump().items():
        setattr(image, key, value)
    image.is_primary = make_primary
    db.add(image)
    commit(db)
    db.refresh(image)
    return image


def remove_image(db: Session, tour_id, image_id):
    tour = tour_or_404(db, tour_id, lock=True)
    image = owned_image(tour, image_id)
    remaining = [other for other in tour.images if other.id != image.id]
    was_primary = image.is_primary
    db.delete(image)
    db.flush()
    if was_primary and remaining:
        remaining[0].is_primary = True
    commit(db)
