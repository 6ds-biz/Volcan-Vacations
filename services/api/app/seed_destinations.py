"""Explicit reference geography seed. No product mappings or inventory activation."""
import argparse
import json
from pathlib import Path

from sqlalchemy import select, text

from .config import settings
from .database import SessionLocal
from .foundation_schemas import DestinationInput
from .models import Destination


def seed_reference(db):
    records = json.loads((Path(__file__).parent / 'data/costa-rica-destinations.json').read_text())
    inserted = 0
    with db.begin():
        if db.bind.dialect.name == 'postgresql':
            db.execute(text('LOCK TABLE destinations IN SHARE ROW EXCLUSIVE MODE'))
        for position, record in enumerate(records):
            values = dict(record)
            parent_slug = values.pop('parent_slug')
            parent = db.scalar(select(Destination).where(Destination.slug == parent_slug)) if parent_slug else None
            if parent_slug and parent is None:
                raise ValueError('Reference parent must already exist; no changes committed')
            payload = DestinationInput(**values, parent_id=parent.id if parent else None, sort_order=position)
            existing = db.scalar(select(Destination).where(Destination.slug == payload.slug))
            if existing:
                if existing.parent_id != payload.parent_id or existing.destination_type != payload.destination_type:
                    raise ValueError('Existing reference hierarchy differs; review manually. No changes committed')
                continue  # Preserve names, descriptions, active flags and sort edits.
            db.add(Destination(**payload.model_dump()))
            db.flush()
            inserted += 1
    return inserted


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--confirm-reference-data', action='store_true', required=True)
    parser.parse_args()
    if settings.environment not in ('development', 'preview'):
        raise SystemExit('Reference seed requires development or preview environment')
    with SessionLocal() as db:
        print(f'Reference destinations inserted: {seed_reference(db)}. No inventory mapped or published.')


if __name__ == '__main__':
    main()
