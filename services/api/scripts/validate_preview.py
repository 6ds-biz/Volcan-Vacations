"""Validate hosted behavior on a uniquely named, disposable local PostgreSQL DB.

Run inside the development API container. No provider calls, records copied,
create_all(), changes to existing tables, or changes to historical migrations.
"""
import argparse
from datetime import date, timedelta
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from uuid import uuid4

import httpx
from sqlalchemy import create_engine, select, text
from sqlalchemy.engine import make_url

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.config import settings
from app.models import Base


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--confirm-isolated', action='store_true', required=True)
    parser.parse_args()
    source_url = make_url(settings.database_url)
    if settings.environment != 'development' or source_url.host not in ('postgres', 'localhost', '127.0.0.1'):
        raise SystemExit('Refused: run against local development PostgreSQL only.')
    name = 'vv_preview_validation_' + uuid4().hex
    target_url = source_url.set(database=name)
    source = create_engine(source_url)
    admin = create_engine(source_url.set(database='postgres'), isolation_level='AUTOCOMMIT')
    target = None
    server = None
    created = False
    stage = 'baseline'
    result = {'scope': 'local disposable PostgreSQL, not Render/Vercel acceptance'}

    def fingerprints():
        with source.connect() as db:
            db.execute(text('SET TRANSACTION READ ONLY'))
            values = {}
            for table in Base.metadata.sorted_tables:
                rows = db.execute(select(table).order_by(*table.primary_key.columns)).all()
                values[table.name] = {'rows': len(rows), 'sha256': hashlib.sha256(
                    repr([tuple(row) for row in rows]).encode()).hexdigest()}
            return values

    before = fingerprints()
    env = dict(os.environ, DATABASE_URL=target_url.render_as_string(hide_password=False),
               ENVIRONMENT='preview', ALLOWED_ORIGINS='https://preview.example.invalid', ALLOWED_ORIGIN_REGEX='',
               PUBLIC_WEB_URL='https://preview.example.invalid', PAYPAL_ENVIRONMENT='sandbox',
               PAYPAL_CLIENT_ID='', PAYPAL_CLIENT_SECRET='', PAYPAL_WEBHOOK_ID='', PAYPAL_CURRENCY='USD')
    api_root = Path(__file__).resolve().parents[1]

    def command(args, expected=0):
        run = subprocess.run(args, env=env, cwd=api_root, capture_output=True, text=True)
        # Never echo process output containing DB URLs or payment tokens.
        if run.returncode != expected:
            diagnostics = (run.stdout + run.stderr)[-6000:]
            diagnostics = diagnostics.replace(env['DATABASE_URL'], '[DATABASE_URL]')
            if source_url.password:
                diagnostics = diagnostics.replace(source_url.password, '[DB_PASSWORD]')
            result['diagnostics'] = diagnostics
            raise AssertionError(f'{stage}: subprocess failed')
        return run

    def counts():
        with target.connect() as db:
            return {table.name: db.scalar(select(text('count(*)')).select_from(table)) for table in Base.metadata.sorted_tables}

    def start_server():
        # Select an unused local port; never replace the development API.
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        child_env = dict(env, PORT=str(port))
        proc = subprocess.Popen(['sh', '-c', 'uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --no-access-log'],
                                env=child_env, cwd=api_root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        base = f'http://127.0.0.1:{port}'
        for _ in range(100):
            if proc.poll() is not None:
                raise RuntimeError('Validation API exited during startup')
            try:
                if httpx.get(base + '/health', timeout=1).status_code == 200:
                    return proc, base
            except httpx.HTTPError:
                pass
            time.sleep(0.1)
        proc.terminate(); proc.wait(timeout=10)
        raise RuntimeError('Validation API startup timed out')

    try:
        stage = 'create isolated database'
        with admin.connect() as db:
            db.execute(text(f'CREATE DATABASE "{name}"'))
        created = True
        target = create_engine(target_url)
        stage = 'sequential migrations'
        revisions = ['0001_initial_schema', '0002_tour_inventory', '0003_booking_requests',
                     '0004_availability_confirmation', '0005_paypal_payments', '0006_platform_foundation', '0007_internal_users_tasks', '0008_transportation_foundation', '0009_ops_appearance', 'head']
        for revision in revisions:
            command(['alembic', 'upgrade', revision])
        with target.connect() as db:
            assert db.scalar(text('SELECT version_num FROM alembic_version')) == '0009_ops_appearance'
        assert all(count == 0 for count in counts().values())
        result['migrations'] = revisions
        stage = 'preview inventory seed'
        command([sys.executable, '-m', 'app.seed_inventory', '--confirm-demo', '--preview'])
        initial = counts()
        assert initial['suppliers'] == 2 and initial['products'] == 6 and initial['product_images'] == 6
        assert all(count == 0 for table, count in initial.items() if table not in ('suppliers', 'products', 'product_images'))
        command([sys.executable, '-m', 'app.seed_inventory', '--confirm-demo', '--preview'], expected=1)
        assert counts() == initial
        result['seed_counts'] = initial
        result['seed_refuses_nonempty_database'] = True
        stage = 'hosted API smoke'
        server, base = start_server()
        with httpx.Client(base_url=base, timeout=10) as http:
            assert http.get('/health').json() == {'status': 'ok', 'service': 'volcan-vacations-api'}
            tours = http.get('/public/tours').json()
            assert len(tours) == 6 and all(tour['name'].startswith('DEMO') for tour in tours)
            assert all('DEMO ONLY' in tour['short_description'] for tour in tours)
            assert all('supplier_cost' not in tour and 'supplier_id' not in tour for tour in tours)
            assert all(tour['primary_image']['image_url'].startswith('/images/') for tour in tours)
            paths = http.get('/openapi.json').json()['paths']
            assert not any(path.startswith('/ops') for path in paths)
            assert http.get('/ops/bookings').status_code == 404
            assert http.post('/ops/suppliers', json={}).status_code == 404
            preflight = {'Origin': env['ALLOWED_ORIGINS'], 'Access-Control-Request-Method': 'POST',
                         'Access-Control-Request-Headers': 'authorization,content-type'}
            assert http.options('/public/booking-requests', headers=preflight).headers['access-control-allow-origin'] == env['ALLOWED_ORIGINS']
            assert http.options('/public/booking-requests', headers=preflight | {'Origin': 'https://unlisted.example.invalid'}).status_code == 400
            day = str(date.today() + timedelta(days=30))
            payload = dict(idempotency_key=str(uuid4()), tour_slug=tours[0]['slug'], requested_date=day,
                           party_size=1, customer={'first_name': 'DEMO', 'last_name': 'Validation', 'email': 'preview@example.invalid'},
                           travelers=[{'first_name': 'DEMO', 'last_name': 'Validation'}])
            receipt = http.post('/public/booking-requests', json=payload)
            assert receipt.status_code == 201
            receipt = receipt.json()
            assert http.get(f"/public/tours/{tours[0]['slug']}/availability", params={'date': day}).json()['status'] == 'unknown'
        stage = 'private availability and payment-link preparation (no provider call)'
        # A private process uses existing domain services. Hosted /ops stays absent.
        prepared = command([sys.executable, '-c', '''
from datetime import date, datetime, timezone
import json
from uuid import uuid4
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Product, Reservation
from app.availability_schemas import AvailabilityInput, SupplierEventInput
from app.availability_service import save_availability, record_supplier_event
from app.payment_schemas import LinkInput
from app.payment_service import issue_link
with SessionLocal() as db:
    booking = db.scalar(select(Reservation))
    booking_id, product_id, day, version = booking.id, booking.product_id, booking.reservation_date, booking.version
with SessionLocal() as db:
    save_availability(db, AvailabilityInput(product_id=product_id, date=day, status='available', source='manual', last_checked_at=datetime.now(timezone.utc)))
with SessionLocal() as db:
    booking = record_supplier_event(db, booking_id, SupplierEventInput(command_id=uuid4(), expected_version=version, event_type='confirmed'))
with SessionLocal() as db:
    link = issue_link(db, booking_id, LinkInput(expected_version=booking['version']))
    print(json.dumps(link, default=str))
'''])
        link = json.loads(prepared.stdout)
        assert link['path'].startswith(env['PUBLIC_WEB_URL'] + '/pay#token=')
        token = link['path'].split('#token=')[1]
        stage = 'persistence after API restart'
        server.terminate(); server.wait(timeout=10); server = None
        server, base = start_server()
        with httpx.Client(base_url=base, timeout=10) as http:
            assert len(http.get('/public/tours').json()) == 6
            assert http.post('/public/booking-requests', json=payload).json() == receipt
            assert http.get(f"/public/tours/{tours[0]['slug']}/availability", params={'date': day}).json()['status'] == 'available'
            payment = http.get('/public/payments/session', headers={'Authorization': 'Bearer ' + token})
            assert payment.status_code == 200
            assert payment.json()['environment'] == 'sandbox'
            assert payment.json()['checkout_available'] is False  # no provider credentials
        final = counts()
        assert final['reservations'] == final['trips'] == final['customers'] == 1
        assert final['payments'] == final['payment_webhook_events'] == 0
        result['smoke_checks'] = ['health', 'demo inventory and images', 'private API absence', 'exact CORS',
                                  'booking request', 'availability', 'public payment session', 'API restart persistence', 'booking idempotency']
        result['provider_calls'] = 0
        result['result'] = 'PASS'
    except Exception as exc:
        result.update(result='FAIL', failed_stage=stage, error_type=type(exc).__name__)
    finally:
        if server is not None:
            server.terminate(); server.wait(timeout=10)
        if target is not None:
            target.dispose()
        if created:
            # Only the unique database created by this invocation is removed.
            with admin.connect() as db:
                db.execute(text(f'DROP DATABASE "{name}" WITH (FORCE)'))
        result['validation_database_removed'] = created
        result['development_database_unchanged'] = fingerprints() == before
        if not result['development_database_unchanged']:
            result['result'] = 'FAIL'
        source.dispose(); admin.dispose()
    print(json.dumps(result, indent=2))
    return 0 if result['result'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
