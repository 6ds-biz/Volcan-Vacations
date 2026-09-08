from datetime import timedelta
from sqlalchemy import select, delete
import pytest
from app import models as m
from app.internal_auth import HASHER, COOKIE, digest
from app.availability_rules import utcnow
from test_inventory import client, create_tour
from test_bookings import inspect_db, submit

PASSWORD='isolated-test-password-12345'

def add_user(role='staff',profile=None,active=True):
    def save(db):
        user=m.InternalUser(email=role+'@example.invalid',display_name=role,role=role,dashboard_profile=profile or {'staff':'Staff','operations_partner':'Operations','owner_admin':'Owner'}[role],active=active,password_hash=HASHER.hash(PASSWORD))
        db.add(user);db.commit();return user.id
    return inspect_db(save)

def signin(client,role='staff'):
    client.cookies.clear()
    response=client.post('/ops/auth/login',json={'email':role+'@example.invalid','password':PASSWORD})
    if response.status_code==200: client.headers['X-CSRF-Token']=response.json()['csrf_token']
    return response

def test_anonymous_internal_denied_public_works(client):
    create_tour(client);client.cookies.clear()
    for path in ['/ops/tours','/ops/bookings','/ops/users','/ops/tasks','/ops/auth/me','/ops/payments','/ops/destinations']:
        assert client.get(path).status_code==401
    assert client.get('/public/tours').status_code==200
    assert submit(client).status_code==201

def test_login_cookie_session_hash_and_logout(client):
    response=client.get('/ops/auth/me');assert response.status_code==200
    assert 'password_hash' not in response.text and 'test-only-password' not in response.text
    cookie=client.cookies.get(COOKIE)
    def verify(db):
        assert db.get(m.InternalSession,digest(cookie))
        assert not db.get(m.InternalSession,cookie)
    inspect_db(verify)
    assert client.post('/ops/auth/logout',json={}).status_code==204
    client.cookies.set(COOKIE,cookie)
    assert client.get('/ops/auth/me').status_code==401

@pytest.mark.parametrize('mode',['inactive','expired'])
def test_session_enforced_each_request(client,mode):
    def change(db):
        if mode=='inactive': db.scalar(select(m.InternalUser)).active=False
        else: db.scalar(select(m.InternalSession)).expires_at=utcnow()-timedelta(seconds=1)
        db.commit()
    inspect_db(change)
    assert client.get('/ops/bookings').status_code==401

def test_invalid_inactive_login_and_rate_limit(client):
    add_user(active=False)
    assert signin(client).status_code==401
    for _ in range(7): assert signin(client).status_code==401
    assert signin(client).status_code==429

def test_csrf_and_origin(client):
    assert client.post('/ops/tasks',json={'title':'test'},headers={'X-CSRF-Token':'wrong'}).status_code==403
    assert client.post('/ops/tasks',json={'title':'test'},headers={'Origin':'https://evil.example'}).status_code==403
    assert client.post('/ops/auth/login',json={'email':'owner@example.invalid','password':PASSWORD},headers={'Origin':'https://evil.example'}).status_code==403
    assert client.post('/ops/auth/login',json={'email':'invalid','password':'secret-marker'}).status_code==422
    assert 'secret-marker' not in client.post('/ops/auth/login',json={'email':'invalid','password':'secret-marker'}).text

@pytest.mark.parametrize('role,profile',[('staff','Owner'),('operations_partner','Owner')])
def test_profiles_never_grant_permissions(client,role,profile):
    add_user(role,profile);assert signin(client,role).status_code==200
    assert client.get('/ops/users').status_code==403
    assert client.post('/ops/users',json={}).status_code==403
    assert client.get('/ops/tours').status_code==(403 if role=='staff' else 200)
    assert client.get('/ops/payments').status_code==(403 if role=='staff' else 200)

def test_last_owner_and_user_admin(client):
    owner=client.get('/ops/users').json()[0]
    update={k:owner[k] for k in ['display_name','role','dashboard_profile','active']};update['active']=False
    assert client.put('/ops/users/'+str(owner['id']),json=update).status_code==409
    result=client.post('/ops/users',json={'email':'NEW@Example.invalid','display_name':'New user','role':'staff','password':PASSWORD})
    assert result.status_code==201 and result.json()['email']=='new@example.invalid' and 'password_hash' not in result.text
    client.cookies.clear();login=client.post('/ops/auth/login',json={'email':'new@example.invalid','password':PASSWORD})
    assert login.status_code==200
    client.headers['X-CSRF-Token']=login.json()['csrf_token']
    assert client.get('/ops/tasks').status_code==403
    assert client.post('/ops/auth/password',json={'current_password':'incorrect-current-password','new_password':'new-isolated-password-12345'}).status_code==400
    assert client.get('/ops/auth/me').status_code==200
    assert client.post('/ops/auth/password',json={'current_password':PASSWORD,'new_password':'new-isolated-password-12345'}).status_code==204
    assert client.get('/ops/auth/me').status_code==401

def test_staff_task_scope_assignment_booking_privacy_and_audit(client):
    create_tour(client);submit(client);booking=client.get('/ops/bookings').json()[0]
    staff=add_user()
    own=client.post('/ops/tasks',json={'title':'Follow up','assigned_user_id':staff,'related_entity_type':'booking','related_entity_id':booking['id']}).json()
    secret=client.post('/ops/tasks',json={'title':'Private owner issue','queue_role':'owner_admin'}).json()
    assert signin(client).status_code==200
    assert client.get('/ops/tasks/'+str(secret['id'])).status_code==404
    assert len(client.get('/ops/tasks').json())==1
    safe=client.get('/ops/work/bookings/'+str(booking['id']));assert safe.status_code==200
    for key in ['supplier_unit_cost','unit_price','gross_margin','payment_token','supplier','travelers']: assert key not in safe.json()
    assert client.get('/ops/bookings/'+str(booking['id'])).status_code==403
    assert client.post('/ops/tasks',json={'title':'Delegate','assigned_user_id':1}).status_code==403
    update={k:own[k] for k in ['title','description','assigned_user_id','related_entity_type','related_entity_id','priority','status','queue_role','due_at']}
    update.update(status='completed',expected_version=own['version'])
    saved=client.put('/ops/tasks/'+str(own['id']),json=update);assert saved.status_code==200,saved.text
    assert saved.json()['completed_by_user_id']==staff
    assert client.put('/ops/tasks/'+str(own['id']),json=update).status_code==409
    # Completed task no longer grants booking relevance.
    assert client.get('/ops/work/bookings/'+str(booking['id'])).status_code==404
    def audit(db): assert db.scalar(select(m.InternalAudit).where(m.InternalAudit.entity_type=='task',m.InternalAudit.action=='updated')).actor_user_id==staff
    inspect_db(audit)

def test_system_booking_tasks_idempotent_and_balanced(client):
    from test_bookings import payload
    create_tour(client);partner=add_user('operations_partner')
    data=payload();submit(client,data);submit(client,data)
    tasks=client.get('/ops/tasks').json()
    assert len(tasks)==1 and tasks[0]['source']=='system_generated' and tasks[0]['assigned_user_id']==partner
    from app.task_service import system_task
    def retry(db):
        system_task(db,'booking-review:1','duplicate','booking',1);db.commit()
    inspect_db(retry)
    assert len(client.get('/ops/tasks').json())==1

def test_partner_cannot_approve_agreement_or_read_owner_queue(client):
    tour=create_tour(client);add_user('operations_partner')
    private_task=client.post('/ops/tasks',json={'title':'Owner issue','queue_role':'owner_admin'}).json()
    signin(client,'operations_partner')
    assert client.get('/ops/tasks').json()==[]
    assert client.get('/ops/audit?entity_type=user&entity_id=1').status_code==403
    assert client.get('/ops/audit?entity_type=task&entity_id='+str(private_task['id'])).status_code==404
    response=client.post('/ops/suppliers/'+str(tour['supplier_id'])+'/agreements',json={'title':'Approval','effective_from':'2026-01-01','status':'approved'})
    assert response.status_code==403,response.text

def test_staff_availability_write_only_for_assigned_booking(client):
    from uuid import uuid4
    create_tour(client);submit(client);booking=client.get('/ops/bookings').json()[0];staff=add_user()
    assert client.put(f"/ops/bookings/{booking['id']}/assignment",json={'assigned_user_id':staff,'expected_version':booking['version']}).status_code==200
    signin(client)
    row=client.get(f"/ops/work/bookings/{booking['id']}").json()
    payload={'command_id':str(uuid4()),'expected_version':row['version'],'event_type':'availability_checked','availability_status':'available'}
    response=client.post(f"/ops/work/bookings/{booking['id']}/availability",json=payload)
    assert response.status_code==200,response.text
    assert response.json()['status']=='new'
    assert response.json()['availability_status']=='available'
    payload.update(command_id=str(uuid4()),expected_version=response.json()['version'],event_type='confirmed')
    assert client.post(f"/ops/work/bookings/{booking['id']}/availability",json=payload).status_code==403

def test_secure_hosted_cookie_and_opt_in(client):
    from app.main import create_app,app
    from app.config import Settings
    from app.database import get_db
    from fastapi.testclient import TestClient
    config=Settings(_env_file=None,database_url='postgresql://test:test@db.invalid/test',environment='production',ops_enabled=True,
        ops_web_url='https://ops.example.invalid',public_web_url='https://www.example.invalid',allowed_origins='https://www.example.invalid')
    hosted=create_app(config);hosted.dependency_overrides[get_db]=app.dependency_overrides[get_db]
    with TestClient(hosted,base_url='https://ops.example.invalid') as http:
        response=http.post('/ops/auth/login',headers={'Origin':'https://ops.example.invalid'},json={'email':'owner@example.invalid','password':'test-only-password-12345'})
        assert response.status_code==200,response.text
        cookie=response.headers['set-cookie'].lower()
        assert 'secure' in cookie and 'httponly' in cookie and 'samesite=strict' in cookie
        assert http.get('/ops/bookings').status_code==200

def test_dashboard_counts_and_staff_privacy(client):
    assert client.get('/ops/dashboard').json()['booking_counts']==dict(new=0,awaiting_supplier=0,ready=0,paid=0)
    create_tour(client);submit(client);booking=client.get('/ops/bookings').json()[0];staff=add_user(profile='Owner')
    task=client.post('/ops/tasks',json={'title':'Assigned follow-up','assigned_user_id':staff,'related_entity_type':'booking','related_entity_id':booking['id']}).json()
    owner=client.get('/ops/dashboard');assert owner.status_code==200,owner.text
    assert owner.json()['booking_counts']['new']==1
    signin(client)
    data=client.get('/ops/dashboard').json()
    for key in ['booking_counts','vendor_counts','inventory_counts','recent_payments']: assert key not in data
    assert len(data['assigned_bookings'])==1
    assert data['my_tasks'][0]['id']==task['id']
    for text in ['supplier_cost','supplier_unit_cost','gross_margin','password_hash','payment_token']: assert text not in str(data)
    for path in ['/ops/customers','/ops/trips','/ops/agreements','/ops/directory/inventory']: assert client.get(path).status_code==403

def test_business_directories_and_actor_projection(client):
    from uuid import uuid4
    create_tour(client);submit(client);booking=client.get('/ops/bookings').json()[0]
    result=client.post(f"/ops/bookings/{booking['id']}/supplier-events",json={'command_id':str(uuid4()),'expected_version':booking['version'],'event_type':'contacted','contact_method':'email','operator_identifier':'Unverified label'})
    assert result.status_code==200,result.text
    event=result.json()['supplier_events'][0]
    assert event['actor_display_name']=='Test owner' and event['actor_user_id']==1
    for path in ['/ops/customers','/ops/trips','/ops/agreements','/ops/directory/inventory']:
        response=client.get(path);assert response.status_code==200,response.text
    trip=client.get('/ops/trips').json()[0]
    assert trip['bookings'][0]['id']==booking['id'] and trip['customer_id']==1

def test_completed_task_retains_completion_actor_on_metadata_edit(client):
    owner=client.get('/ops/auth/me').json()['user']['id']
    task=client.post('/ops/tasks',json={'title':'Review','assigned_user_id':owner,'status':'completed'}).json()
    add_user('operations_partner');signin(client,'operations_partner')
    payload={k:task[k] for k in ['title','description','assigned_user_id','related_entity_type','related_entity_id','priority','status','queue_role','due_at']}
    payload.update(title='Reviewed title',expected_version=task['version'])
    response=client.put('/ops/tasks/'+str(task['id']),json=payload)
    assert response.status_code==200,response.text
    assert response.json()['completed_by_user_id']==owner

@pytest.mark.parametrize('role',['owner_admin','operations_partner','staff'])
def test_appearance_persists_for_authenticated_user_only(client,role):
    user_id=add_user(role)
    other_id=add_user('staff' if role!='staff' else 'operations_partner')
    assert signin(client,role).json()['user']['appearance']=='dark'
    for value in ['light','system','dark']:
        response=client.put('/ops/auth/appearance',json={'appearance':value})
        assert response.status_code==200
        assert client.get('/ops/auth/me').json()['user']['appearance']==value
        inspect_db(lambda db: (assert_appearance(db,user_id,value),assert_appearance(db,other_id,'dark')))
    client.put('/ops/auth/appearance',json={'appearance':'light'})
    client.post('/ops/auth/logout',json={})
    assert signin(client,role).json()['user']['appearance']=='light'
    assert client.put('/ops/auth/appearance',json={'appearance':'invalid'}).status_code==422
    assert client.put('/ops/auth/appearance',json={'appearance':'dark','user_id':other_id}).status_code==422

def assert_appearance(db,user_id,value):
    assert db.get(m.InternalUser,user_id).appearance==value

def test_appearance_requires_session_origin_and_csrf(client):
    headers=dict(client.headers)
    client.headers.pop('X-CSRF-Token',None)
    assert client.put('/ops/auth/appearance',json={'appearance':'light'}).status_code==403
    client.headers.update(headers)
    assert client.put('/ops/auth/appearance',json={'appearance':'light'},headers={'Origin':'https://invalid.example'}).status_code==403
    client.cookies.clear()
    assert client.put('/ops/auth/appearance',json={'appearance':'light'}).status_code==401
