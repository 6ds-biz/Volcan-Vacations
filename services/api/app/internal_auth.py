"""Argon2id credentials + opaque database sessions; no browser bearer storage."""
import hashlib
import secrets
from datetime import timedelta
from urllib.parse import urlsplit

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, InvalidHashError
from fastapi import Depends, HTTPException, Request
from sqlalchemy import select, delete

from .database import get_db
from .models import InternalUser, InternalSession, LoginGuard
from .availability_rules import utcnow, aware
from .internal_schemas import UserRead
from .permissions import PERMISSIONS, demand, route_permission

COOKIE = 'vv_ops_session'
HASHER = PasswordHasher()
DUMMY_HASH = HASHER.hash(secrets.token_urlsafe(32))

def digest(token): return hashlib.sha256(token.encode()).hexdigest()

def verify_password(encoded, password):
    try: return HASHER.verify(encoded,password)
    except (VerificationError,InvalidHashError): return False

def actor_for(user):
    result=UserRead.model_validate(user).model_dump(mode='json')
    result['permissions']=sorted(PERMISSIONS[user.role])
    return result

def allowed_origin(request):
    config=request.app.state.config
    origins=[config.ops_web_url] if config.ops_web_url else []
    if config.environment=='development':
        origins += ['http://localhost:3001'] + [o for o in config.allowed_origins_list
            if urlsplit(o).hostname and urlsplit(o).hostname.endswith('-3001.app.github.dev')]
    origin=request.headers.get('origin')
    if not origin or origin not in origins:
        raise HTTPException(403,'Operations origin is not allowed')

def cookie(response, token, request):
    config=request.app.state.config
    response.set_cookie(COOKIE,token,httponly=True,secure=config.environment!='development',
        samesite='strict',path='/',max_age=config.ops_session_hours*3600)
    response.headers['Cache-Control']='no-store'

def new_session(db,user,request):
    token=secrets.token_urlsafe(32)
    csrf=secrets.token_urlsafe(32)
    db.add(InternalSession(token_hash=digest(token),user_id=user.id,csrf_token=csrf,
        expires_at=utcnow()+timedelta(hours=request.app.state.config.ops_session_hours)))
    return token,csrf

def require_ops(request: Request, db=Depends(get_db)):
    value=request.cookies.get(COOKIE,'')
    if len(value)!=43: raise HTTPException(401,'Sign in to Operations')
    with db.begin():
        session=db.get(InternalSession,digest(value))
        user=db.get(InternalUser,session.user_id) if session else None
        if not session or aware(session.expires_at)<=utcnow() or not user or not user.active:
            raise HTTPException(401,'Your session has expired. Sign in again')
        actor=actor_for(user)
        if request.method not in ('GET','HEAD','OPTIONS'):
            allowed_origin(request)
            if not secrets.compare_digest(request.headers.get('x-csrf-token','').encode(),session.csrf_token.encode()):
                raise HTTPException(403,'Invalid CSRF token')
        if user.must_change_password and request.url.path not in ('/ops/auth/me','/ops/auth/logout','/ops/auth/password'):
            raise HTTPException(403,'Change your temporary password before continuing')
        demand(actor,route_permission(request.url.path,request.method))
        request.state.actor=actor
        request.state.csrf_token=session.csrf_token
    db.info['actor_id']=actor['id']
    return actor

def guard(db,key):
    values=dict(key=digest(key),attempts=0,window_started_at=utcnow())
    if db.bind.dialect.name=='postgresql':
        from sqlalchemy.dialects.postgresql import insert
    else:
        from sqlalchemy.dialects.sqlite import insert
    db.execute(insert(LoginGuard).values(**values).on_conflict_do_nothing(index_elements=['key']))
    row=db.scalar(select(LoginGuard).where(LoginGuard.key==values['key']).with_for_update())
    if aware(row.window_started_at)+timedelta(minutes=15)<=utcnow():
        row.attempts=0;row.window_started_at=utcnow()
    return row

def login(db,payload,request,response):
    allowed_origin(request)
    denied=False;throttled=False
    with db.begin():
        # Email and proxy-peer limits are DB-backed across workers/restarts.
        peer=guard(db,'peer:'+(request.client.host if request.client else 'unknown'))
        account=guard(db,'email:'+payload.email) if peer.attempts<80 else None
        if account is None or account.attempts>=8:
            peer.attempts+=1
            throttled=True
        else:
            account.attempts+=1;peer.attempts+=1
            user=db.scalar(select(InternalUser).where(InternalUser.email==payload.email).with_for_update())
            valid=verify_password(user.password_hash if user else DUMMY_HASH,payload.password)
            if not user or not valid or not user.active:
                denied=True
            else:
                if HASHER.check_needs_rehash(user.password_hash): user.password_hash=HASHER.hash(payload.password)
                account.attempts=0
                user.last_login_at=utcnow()
                db.execute(delete(InternalSession).where(InternalSession.expires_at<=utcnow()))
                old=request.cookies.get(COOKIE,'')
                if old: db.execute(delete(InternalSession).where(InternalSession.token_hash==digest(old)))
                token,csrf=new_session(db,user,request)
                db.flush()
                result=dict(user=actor_for(user),csrf_token=csrf)
    if throttled: raise HTTPException(429,'Too many sign-in attempts. Try again in 15 minutes')
    if denied: raise HTTPException(401,'Email or password is incorrect')
    cookie(response,token,request)
    return result
