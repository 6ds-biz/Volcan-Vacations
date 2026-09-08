"""Concurrency and the migrated immutable-history trigger, using isolated records."""
import os
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4
import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine,select,text,func
from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from app.config import settings
from app import models as m
from app.internal_auth import HASHER
from app.routers.page_layouts import lock_layout,publish
from test_page_layouts import page

@pytest.mark.skipif(os.environ.get('VV_TEST_POSTGRES')!='1',reason='Explicit PostgreSQL integration opt-in required')
@pytest.mark.parametrize('page_type',['owner-dashboard','public-home'])
def test_concurrent_first_publish_and_migrated_immutable_trigger(page_type):
 assert settings.environment=='development'
 schema='vv_layout_test_'+uuid4().hex;admin=create_engine(settings.database_url);isolated=None
 try:
  with admin.begin() as db:
   assert db.scalar(text("SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON p.pronamespace=n.oid WHERE p.proname='vv_layout_revision_immutable' AND n.nspname='public'"))==1,'Apply Alembic head before PostgreSQL tests.'
   db.execute(text(f'CREATE SCHEMA {schema}'))
  isolated=create_engine(settings.database_url,connect_args={'options':f'-csearch_path={schema}'})
  m.Base.metadata.create_all(isolated)
  with Session(isolated) as db:
   u=m.InternalUser(email='layout-review@example.invalid',display_name='Isolated owner',role='owner_admin',dashboard_profile='Owner',password_hash=HASHER.hash('isolated-layout-test-only-password'))
   db.add(u);db.commit();actor=u.id
  def attempt(_):
   with Session(isolated) as db:
    try:
     with db.begin():
      from test_public_website import layout
      content=layout() if page_type=='public-home' else page()
      row=lock_layout(db,page_type,0);publish(db,row,content,actor)
     return 200
    except HTTPException as e:return e.status_code
  with ThreadPoolExecutor(max_workers=2) as pool:assert sorted(pool.map(attempt,[0,1]))==[200,409]
  with isolated.begin() as db:
   assert db.scalar(select(func.count()).select_from(m.PageLayoutRevision))==1
   db.execute(text('CREATE TRIGGER test_immutable BEFORE UPDATE OR DELETE ON page_layout_revisions FOR EACH ROW EXECUTE FUNCTION public.vv_layout_revision_immutable()'))
  for sql in ["UPDATE page_layout_revisions SET action='changed'",'DELETE FROM page_layout_revisions']:
   with pytest.raises(DBAPIError,match='immutable'),isolated.begin() as db:db.execute(text(sql))
  with isolated.connect() as db:assert db.scalar(select(func.count()).select_from(m.PageLayoutRevision))==1
 finally:
  if isolated:isolated.dispose()
  with admin.begin() as db:db.execute(text(f'DROP SCHEMA IF EXISTS {schema} CASCADE'))
  admin.dispose()
