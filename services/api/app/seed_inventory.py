"""Explicit, insert-only development seed. Never runs during app startup."""
import argparse
from decimal import Decimal

from sqlalchemy import select

from .config import settings
from .database import SessionLocal
from .models import Product, ProductImage, Supplier

SAMPLES = [
    ('whitewater-rafting', 'Whitewater Rafting', 'Adventure', 'Half day', '85.00', '50.00', 'rafting', 'Paddle rainforest rapids with local river guides.'),
    ('arenal-volcano-hike', 'Arenal Volcano Hike', 'Nature', '4 hours', '72.00', '42.00', 'arenal', 'Explore forest trails and views of Arenal.'),
    ('hot-springs-experience', 'Hot Springs Experience', 'Relaxation', 'Evening', '95.00', '60.00', 'springs', 'Relax in warm mineral pools and tropical gardens.'),
    ('wildlife-hanging-bridges', 'Wildlife & Hanging Bridges', 'Family', '3 hours', '68.00', '40.00', 'bridges', 'Discover the rainforest canopy on hanging bridges.'),
    ('waterfall-adventure', 'Waterfall Adventure', 'Adventure', '3 hours', '55.00', '30.00', 'waterfall', 'Explore a lush waterfall canyon near La Fortuna.'),
    ('coffee-chocolate-tour', 'Coffee & Chocolate Tour', 'Culture', '2.5 hours', '48.00', '25.00', 'coffee', 'Discover Costa Rican coffee and cacao traditions.'),
]


def seed():
    if settings.environment != 'development':
        raise SystemExit('Seed refused: ENVIRONMENT must be development.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--confirm-demo', action='store_true', required=True, help='Acknowledge sample suppliers, pricing and imagery are not production data')
    parser.parse_args()
    with SessionLocal.begin() as db:
        suppliers = []
        for name in ['DEMO Arenal Adventures', 'DEMO Costa Rica Experiences']:
            supplier = db.scalar(select(Supplier).where(Supplier.name == name))
            if supplier is None:
                supplier = Supplier(name=name, supplier_type='tour_operator', contact_name='Demo Contact', email='demo@example.invalid', phone=None, notes='Development sample only. Not a real supplier or current quote.', active=True)
                db.add(supplier)
                db.flush()
            suppliers.append(supplier)
        inserted = 0
        for index, (slug, name, category, duration, retail, cost, image, summary) in enumerate(SAMPLES):
            if db.scalar(select(Product.id).where(Product.slug == slug)) is not None:
                print(f'Skipped existing slug (no overwrite): {slug}')
                continue
            tour = Product(supplier_id=suppliers[index % 2].id, name=name, slug=slug, short_description=summary,
                           description=f'DEVELOPMENT DEMO ONLY — sample pricing and illustrative imagery, not a current supplier offer. {summary}',
                           product_type='tour', category=category, duration=duration, retail_price=Decimal(retail), supplier_cost=Decimal(cost),
                           active=True, featured=True, location='La Fortuna / Arenal', difficulty=None, minimum_age=None)
            tour.images = [ProductImage(image_url=f'/images/{image}.webp', alt_text=f'Illustrative demo: {name}', sort_order=0, is_primary=True)]
            db.add(tour)
            inserted += 1
        print(f'Demo seed completed: {inserted} tours inserted; 2 demo suppliers available. Existing records preserved.')


if __name__ == '__main__':
    seed()
