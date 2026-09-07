"""Interactive first-owner bootstrap; never reads credentials from source/env/argv."""
from getpass import getpass
from sqlalchemy import select, func, text
from .database import SessionLocal
from .models import InternalUser
from .internal_schemas import UserCreate
from .internal_auth import HASHER

def main():
    email=input('Owner email: ').strip().lower()
    name=input('Display name: ').strip()
    password=getpass('Password (15–128 characters): ')
    if password!=getpass('Confirm password: '): raise SystemExit('Passwords did not match')
    try: data=UserCreate(email=email,display_name=name,password=password,role='owner_admin')
    except Exception: raise SystemExit('Invalid email, name or password length') from None
    with SessionLocal.begin() as db:
        if db.bind.dialect.name=='postgresql': db.execute(text('LOCK TABLE internal_users IN SHARE ROW EXCLUSIVE MODE'))
        if db.scalar(select(func.count()).select_from(InternalUser).where(InternalUser.role=='owner_admin',InternalUser.active.is_(True))):
            raise SystemExit('An active owner already exists. Use authenticated user administration.')
        if db.scalar(select(InternalUser.id).where(InternalUser.email==data.email)): raise SystemExit('This email already exists')
        db.add(InternalUser(email=data.email,display_name=data.display_name,role='owner_admin',dashboard_profile='Owner',password_hash=HASHER.hash(data.password)))
    print('First owner created. Sign in to Operations.')

if __name__=='__main__': main()
