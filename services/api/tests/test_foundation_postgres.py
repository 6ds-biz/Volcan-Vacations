"""Actual PostgreSQL tree locking; isolated schema, no provider calls."""
import os
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Base, Destination, Supplier
from app.foundation_schemas import DestinationInput
from app.foundation_service import save_destination


@pytest.mark.skipif(os.environ.get('VV_TEST_POSTGRES') != '1', reason='Explicit PostgreSQL integration opt-in required')
def test_postgres_reciprocal_tree_edits_and_reference_constraints():
    assert settings.environment == 'development' and settings.database_url.startswith('postgresql')
    schema = 'vv_foundation_test_' + uuid4().hex
    admin = create_engine(settings.database_url)
    isolated = None
    try:
        with admin.begin() as db:
            db.execute(text(f'CREATE SCHEMA {schema}'))
        isolated = create_engine(settings.database_url, connect_args={'options': f'-csearch_path={schema}'})
        Base.metadata.create_all(isolated)
        identifiers = []
        for slug in ('a', 'b'):
            with Session(isolated) as db:
                row = save_destination(db, DestinationInput(name=slug, slug=slug, destination_type='region'))
                identifiers.append(row.id)
        def move(index):
            with Session(isolated) as db:
                try:
                    save_destination(db, DestinationInput(name=str(index), slug=('a','b')[index],
                        parent_id=identifiers[1-index], destination_type='region'), identifiers[index])
                    return 200
                except HTTPException as error:
                    return error.status_code
        with ThreadPoolExecutor(max_workers=2) as pool:
            assert sorted(pool.map(move, (0,1))) == [200,409]
        with Session(isolated) as db:
            rows = db.scalars(select(Destination)).all()
            assert sum(r.parent_id is None for r in rows) == 1
        with Session(isolated) as db, pytest.raises(IntegrityError):
            db.add(Destination(name='Bad',slug='bad',destination_type='region',parent_id=999999))
            db.commit()
        with Session(isolated) as db, pytest.raises(IntegrityError):
            db.add(Supplier(name='Bad status', supplier_type='other', relationship_status='published'))
            db.commit()
    finally:
        if isolated:
            isolated.dispose()
        with admin.begin() as db:
            db.execute(text(f'DROP SCHEMA IF EXISTS {schema} CASCADE'))
        admin.dispose()
