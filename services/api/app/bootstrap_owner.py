"""Trusted-console owner creation/recovery; passwords never come from argv/env."""
import argparse
from getpass import GetPassWarning, getpass
import sys
import warnings

from pydantic import ValidationError
from sqlalchemy import delete, select, text
from sqlalchemy.exc import SQLAlchemyError

from .database import SessionLocal
from .internal_auth import HASHER
from .internal_schemas import UserCreate
from .models import InternalAudit, InternalSession, InternalUser


class ConsoleParser(argparse.ArgumentParser):
    def error(self, message):
        # Do not echo unexpected argv: an operator might accidentally put a
        # password there even though this command accepts none.
        self.print_usage(sys.stderr)
        self.exit(2, 'Invalid arguments. Use --help. Enter passwords only at hidden prompts.\n')


def lock_users(db):
    # Recheck after interactive prompts under the owner-administration lock.
    if db.bind.dialect.name == 'postgresql':
        db.execute(text('LOCK TABLE internal_users IN SHARE ROW EXCLUSIVE MODE'))


def check_first_owner(db, email=None):
    owners = db.scalars(select(InternalUser.email).where(
        InternalUser.role == 'owner_admin', InternalUser.active.is_(True)
    ).order_by(InternalUser.email)).all()
    if owners:
        raise SystemExit(
            'Active owner already exists: ' + ', '.join(owners) + '. '
            'No account changed. Sign in normally, or use the explicit '
            '--reset-password EMAIL console command for emergency recovery.'
        )
    if email and db.scalar(select(InternalUser.id).where(InternalUser.email == email)):
        raise SystemExit('This email already belongs to an internal account. '
                         'No account was changed or reactivated. Use a new owner email.')


def recovery_owner(db, email):
    user = db.scalar(select(InternalUser).where(InternalUser.email == email))
    if not user or user.role != 'owner_admin' or not user.active:
        raise SystemExit('Recovery requires an existing active owner_admin account. '
                         'Disabled accounts are not reactivated. No account changed.')
    return user


def new_credentials(email, name):
    # Refuse getpass's echoed-stdin fallback if terminal control fails.
    with warnings.catch_warnings():
        warnings.simplefilter('error', GetPassWarning)
        password = getpass('New password (15–128 characters): ')
        confirmation = getpass('Confirm new password: ')
    if password != confirmation:
        raise SystemExit('New passwords did not match. No account changed.')
    try:
        return UserCreate(email=email, display_name=name, password=password,
                          role='owner_admin', dashboard_profile='Owner')
    except ValidationError:
        raise SystemExit('Invalid email, display name or new password '
                         '(15–128 characters). No account changed.') from None


def run(reset_email):
    if reset_email is not None:
        email = reset_email.strip().lower()
        with SessionLocal() as db:
            user = recovery_owner(db, email)
            name = user.display_name
        print(f'Console password recovery for {email}. All sessions for this owner will be revoked.')
        data = new_credentials(email, name)
        encoded = HASHER.hash(data.password)
        with SessionLocal.begin() as db:
            lock_users(db)
            user = recovery_owner(db, email)
            user.password_hash = encoded
            user.must_change_password = False
            db.execute(delete(InternalSession).where(InternalSession.user_id == user.id))
            db.add(InternalAudit(
                actor_user_id=None, entity_type='user', entity_id=user.id,
                action='password_recovered',
                summary='Owner password recovered through trusted server console; all user sessions revoked.',
            ))
        print('Owner password recovered. All sessions for this owner revoked. Sign in with the new password.')
        return

    with SessionLocal() as db:
        check_first_owner(db)
    print('No active owner exists. Create the first owner with a NEW password; no current password is required.')
    email = input('Owner email: ').strip().lower()
    name = input('Display name: ').strip()
    with SessionLocal() as db:
        check_first_owner(db, email)
    data = new_credentials(email, name)
    encoded = HASHER.hash(data.password)
    with SessionLocal.begin() as db:
        lock_users(db)
        check_first_owner(db, data.email)
        user = InternalUser(email=data.email, display_name=data.display_name,
                            role='owner_admin', dashboard_profile='Owner', active=True,
                            must_change_password=False, password_hash=encoded)
        db.add(user)
        db.flush()
        db.add(InternalAudit(
            actor_user_id=None, entity_type='user', entity_id=user.id,
            action='owner_bootstrapped', summary='First owner created through trusted server console.',
        ))
    print('First owner created. Sign in to Operations with the new password.')


def main(argv=None):
    parser = ConsoleParser(description=__doc__)
    parser.add_argument('--reset-password', metavar='EMAIL',
                        help='Explicit emergency recovery for an active owner; revokes their sessions.')
    args = parser.parse_args(argv)
    if not sys.stdin.isatty():
        raise SystemExit('An interactive trusted console is required. '
                         'Use docker compose exec api python -m app.bootstrap_owner (without -T).')
    try:
        run(args.reset_password)
    except (EOFError, KeyboardInterrupt):
        raise SystemExit('Cancelled. No account changed.') from None
    except GetPassWarning:
        raise SystemExit('Secure hidden password input is unavailable. No account changed.') from None
    except SQLAlchemyError:
        # SQLAlchemy errors can include bound parameters (including a new hash).
        raise SystemExit('Database operation failed. Account changes were not confirmed. '
                         'Check database health before retrying; no database details are printed.') from None


if __name__ == '__main__':
    main()
