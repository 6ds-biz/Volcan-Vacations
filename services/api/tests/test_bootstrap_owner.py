"""Console bootstrap/recovery against isolated databases, never development records."""
import os
from datetime import date, timedelta
from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4
import warnings

import pytest
from sqlalchemy import create_engine, event, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

os.environ.setdefault('DATABASE_URL', 'sqlite://')
from app import bootstrap_owner as bootstrap
from app import models as m
from app.availability_rules import utcnow
from app.config import settings
from app.internal_auth import HASHER, digest, verify_password

OLD = 'isolated-old-password-12345'
NEW = 'isolated-new-password-67890'


@pytest.fixture(params=['sqlite', 'postgresql'])
def database(request, monkeypatch, tmp_path):
    admin = None
    schema = None
    if request.param == 'postgresql':
        if os.environ.get('VV_TEST_POSTGRES') != '1':
            pytest.skip('Explicit PostgreSQL integration opt-in required')
        assert settings.environment == 'development' and settings.database_url.startswith('postgresql')
        schema = 'vv_bootstrap_test_' + uuid4().hex
        admin = create_engine(settings.database_url)
        with admin.begin() as db:
            db.execute(text(f'CREATE SCHEMA {schema}'))
        engine = create_engine(settings.database_url, connect_args={'options': f'-csearch_path={schema}'})
    else:
        engine = create_engine('sqlite:///' + str(tmp_path / 'bootstrap.db'))
    try:
        m.Base.metadata.create_all(engine)
        factory = sessionmaker(bind=engine)
        monkeypatch.setattr(bootstrap, 'SessionLocal', factory)
        monkeypatch.setattr(bootstrap.sys, 'stdin', SimpleNamespace(isatty=lambda: True))
        # Seed actual booking economics using Core, without triggering unrelated tasks.
        with engine.begin() as db:
            db.execute(m.Customer.__table__.insert().values(id=1, first_name='Isolated', last_name='Customer', email='customer@example.invalid'))
            db.execute(m.Supplier.__table__.insert().values(id=1, name='Isolated supplier', supplier_type='tour_operator'))
            db.execute(m.Product.__table__.insert().values(id=1, supplier_id=1, name='Isolated tour', slug='isolated-tour', product_type='tour', retail_price=Decimal('95'), supplier_cost=Decimal('50')))
            db.execute(m.Trip.__table__.insert().values(id=1, customer_id=1, reference='ISOLATED-BOOTSTRAP', party_size=2))
            db.execute(m.Reservation.__table__.insert().values(id=1, trip_id=1, product_id=1, supplier_id=1, reservation_date=date(2027, 1, 1), quantity=2, unit_price=Decimal('85'), supplier_unit_cost=Decimal('50')))
            db.execute(m.Payment.__table__.insert().values(id=1, trip_id=1, reservation_id=1, amount=Decimal('170'), payment_method='manual'))
        before = business_snapshot(factory)
        yield factory
        assert business_snapshot(factory) == before
    finally:
        engine.dispose()
        if admin:
            with admin.begin() as db:
                db.execute(text(f'DROP SCHEMA {schema} CASCADE'))
            admin.dispose()


def business_snapshot(factory):
    with factory() as db:
        return {t.name: [tuple(row) for row in db.execute(select(t).order_by(*t.primary_key.columns))]
                for t in m.Base.metadata.sorted_tables
                if t.name not in {'internal_users', 'internal_sessions', 'internal_audit', 'login_guards'}}


def add_owner(factory, email='owner@example.invalid', active=True, role='owner_admin'):
    with factory.begin() as db:
        user = m.InternalUser(email=email, display_name='Isolated user', role=role,
                              active=active, dashboard_profile='Owner', password_hash=HASHER.hash(OLD),
                              must_change_password=True)
        db.add(user)
        db.flush()
        identifier = user.id
        db.add(m.InternalSession(token_hash=digest(email), user_id=identifier, csrf_token='isolated', expires_at=utcnow()+timedelta(hours=1)))
        return identifier


def prompts(monkeypatch, email='real@example.invalid', passwords=None):
    answers = iter([email, 'Real owner'])
    secrets = iter(passwords if passwords is not None else [NEW, NEW])
    seen = []
    def password(prompt):
        seen.append(prompt)
        return next(secrets)
    monkeypatch.setattr('builtins.input', lambda prompt: next(answers))
    monkeypatch.setattr(bootstrap, 'getpass', password)
    return seen


def test_first_owner_ignores_disabled_validation_accounts(database, monkeypatch, capsys):
    disabled = add_owner(database, 'ops2-validation-owner@example.invalid', active=False)
    seen = prompts(monkeypatch, email=' REAL@Example.invalid ')
    bootstrap.main([])
    with database() as db:
        user = db.scalar(select(m.InternalUser).where(m.InternalUser.active.is_(True)))
        assert user.email == 'real@example.invalid'
        assert user.role == 'owner_admin' and user.dashboard_profile == 'Owner'
        assert user.active and not user.must_change_password
        assert user.password_hash.startswith('$argon2id$') and verify_password(user.password_hash, NEW)
        assert not db.get(m.InternalUser, disabled).active
        assert verify_password(db.get(m.InternalUser, disabled).password_hash, OLD)
        event = db.scalar(select(m.InternalAudit))
        assert event.action == 'owner_bootstrapped' and event.entity_id == user.id
        assert event.actor_user_id is None
    assert seen == ['New password (15–128 characters): ', 'Confirm new password: ']
    output = capsys.readouterr().out
    assert NEW not in output and '$argon2' not in output


def test_existing_owner_protected_before_any_prompt(database, monkeypatch):
    owner = add_owner(database)
    def forbidden(*args):
        pytest.fail('Existing-owner check must happen before prompting')
    monkeypatch.setattr('builtins.input', forbidden)
    monkeypatch.setattr(bootstrap, 'getpass', forbidden)
    with pytest.raises(SystemExit, match='Active owner already exists: owner@example.invalid'):
        bootstrap.main([])
    with database() as db:
        assert verify_password(db.get(m.InternalUser, owner).password_hash, OLD)
        assert db.scalar(select(m.InternalSession))
        assert not db.scalar(select(m.InternalAudit))


def test_explicit_recovery_revokes_only_target_sessions_and_audits(database, monkeypatch, capsys):
    owner = add_owner(database)
    other = add_owner(database, 'other@example.invalid', role='staff')
    with database.begin() as db:
        db.add(m.InternalSession(token_hash=digest('second'), user_id=owner, csrf_token='second', expires_at=utcnow()+timedelta(hours=1)))
        other_before = tuple(db.execute(select(m.InternalUser.__table__).where(m.InternalUser.id == other)).one())
    seen = prompts(monkeypatch)
    bootstrap.main(['--reset-password', ' OWNER@Example.invalid '])
    with database() as db:
        user = db.get(m.InternalUser, owner)
        assert verify_password(user.password_hash, NEW) and not verify_password(user.password_hash, OLD)
        assert user.active and user.role == 'owner_admin' and user.dashboard_profile == 'Owner'
        assert not user.must_change_password
        assert not db.scalar(select(m.InternalSession).where(m.InternalSession.user_id == owner))
        assert db.scalar(select(m.InternalSession).where(m.InternalSession.user_id == other))
        assert tuple(db.execute(select(m.InternalUser.__table__).where(m.InternalUser.id == other)).one()) == other_before
        event = db.scalar(select(m.InternalAudit))
        assert event.entity_id == owner and event.action == 'password_recovered'
        assert event.actor_user_id is None and 'console' in event.summary
        assert NEW not in event.summary and OLD not in event.summary and '$argon2' not in event.summary
    assert len(seen) == 2 and all('current' not in s.lower() for s in seen)
    assert NEW not in capsys.readouterr().out


@pytest.mark.parametrize('kind', ['disabled', 'staff', 'missing'])
def test_recovery_rejects_invalid_target_without_reactivating(database, monkeypatch, kind):
    if kind != 'missing':
        add_owner(database, active=kind != 'disabled', role='staff' if kind == 'staff' else 'owner_admin')
    def forbidden(*args):
        pytest.fail('Invalid target must not prompt for a password')
    monkeypatch.setattr(bootstrap, 'getpass', forbidden)
    with pytest.raises(SystemExit, match='existing active owner_admin'):
        bootstrap.main(['--reset-password', 'owner@example.invalid'])
    with database() as db:
        user = db.scalar(select(m.InternalUser))
        if user:
            assert verify_password(user.password_hash, OLD)
            assert user.active == (kind != 'disabled')
        assert not db.scalar(select(m.InternalAudit))


@pytest.mark.parametrize('passwords', [[NEW, OLD], ['short', 'short']])
def test_invalid_new_password_rolls_back_recovery(database, monkeypatch, passwords):
    owner = add_owner(database)
    prompts(monkeypatch, passwords=passwords)
    with pytest.raises(SystemExit):
        bootstrap.main(['--reset-password', 'owner@example.invalid'])
    with database() as db:
        assert verify_password(db.get(m.InternalUser, owner).password_hash, OLD)
        assert db.scalar(select(m.InternalSession))
        assert not db.scalar(select(m.InternalAudit))


def test_existing_disabled_email_not_overwritten(database, monkeypatch):
    owner = add_owner(database, active=False)
    prompts(monkeypatch, email='owner@example.invalid', passwords=[])
    with pytest.raises(SystemExit, match='already belongs'):
        bootstrap.main([])
    with database() as db:
        user = db.get(m.InternalUser, owner)
        assert not user.active and verify_password(user.password_hash, OLD)


def test_owner_created_during_prompts_is_detected(database, monkeypatch):
    prompts(monkeypatch)
    def interrupted_prompt(prompt):
        if prompt.startswith('Confirm'):
            add_owner(database)
        return NEW
    monkeypatch.setattr(bootstrap, 'getpass', interrupted_prompt)
    with pytest.raises(SystemExit, match='Active owner already exists'):
        bootstrap.main([])
    with database() as db:
        assert len(db.scalars(select(m.InternalUser)).all()) == 1
        assert not db.scalar(select(m.InternalAudit))


def test_requires_console_and_rejects_password_argument(database, monkeypatch, capsys):
    monkeypatch.setattr(bootstrap.sys, 'stdin', SimpleNamespace(isatty=lambda: False))
    with pytest.raises(SystemExit, match='interactive trusted console'):
        bootstrap.main([])
    with pytest.raises(SystemExit) as result:
        bootstrap.main(['--reset-password', 'owner@example.invalid', '--password', NEW])
    assert result.value.code == 2
    assert NEW not in capsys.readouterr().err


def test_hidden_input_failure_leaves_no_account(database, monkeypatch):
    prompts(monkeypatch)
    def no_terminal(prompt):
        warnings.warn('Cannot control echo on the terminal.', bootstrap.GetPassWarning)
        pytest.fail('Must not fall back to echoed stdin')
    monkeypatch.setattr(bootstrap, 'getpass', no_terminal)
    with pytest.raises(SystemExit, match='hidden password input is unavailable'):
        bootstrap.main([])
    with database() as db:
        assert not db.scalar(select(m.InternalUser))


@pytest.mark.parametrize('recover', [False, True])
def test_audit_failure_rolls_back_and_database_errors_are_sanitized(database, monkeypatch, recover):
    owner = add_owner(database) if recover else None
    prompts(monkeypatch)
    engine = database.kw['bind']
    def fail_audit(connection, cursor, statement, parameters, context, executemany):
        if statement.startswith('INSERT INTO internal_audit'):
            raise SQLAlchemyError('simulated-private-database-parameters')
    event.listen(engine, 'before_cursor_execute', fail_audit)
    try:
        with pytest.raises(SystemExit, match='Database operation failed') as error:
            bootstrap.main(['--reset-password', 'owner@example.invalid'] if recover else [])
        assert 'simulated-private' not in str(error.value)
    finally:
        event.remove(engine, 'before_cursor_execute', fail_audit)
    with database() as db:
        assert not db.scalar(select(m.InternalAudit))
        if recover:
            assert verify_password(db.get(m.InternalUser, owner).password_hash, OLD)
            assert db.scalar(select(m.InternalSession).where(m.InternalSession.user_id == owner))
        else:
            assert not db.scalar(select(m.InternalUser))
