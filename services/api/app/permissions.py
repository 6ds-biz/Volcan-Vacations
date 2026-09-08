"""One capability map; profiles never participate in authorization."""
from fastapi import HTTPException

COMMON = {'transport.read','tasks.read','tasks.create','tasks.update_own','profile.read'}
BUSINESS = {'transport.manage','transport.rates','bookings.read','bookings.write','bookings.assign','customers.read','trips.read',
    'tours.read','tours.write','suppliers.read','suppliers.write','availability.read','availability.write',
    'payments.read','payments.write','commercial.read','commercial.write','tasks.assign','tasks.update_all','audit.read','directory.read'}
PERMISSIONS = {
    'owner_admin': COMMON | BUSINESS | {'users.manage','settings.read','commercial.approve','website.manage'},
    'operations_partner': COMMON | BUSINESS,
    'staff': COMMON | {'bookings.read_assigned','bookings.followup','availability.read_assigned','availability.write_assigned'},
}
DEFAULT_PROFILES = {'owner_admin':'Owner','operations_partner':'Operations','staff':'Staff'}

def can(actor, permission):
    return permission in PERMISSIONS.get(actor['role'],set())

def demand(actor, permission):
    if not can(actor,permission):
        raise HTTPException(403,'You do not have permission for this action')

def route_permission(path, method):
    read = method in ('GET','HEAD')
    parts = path.strip('/').split('/')
    group = parts[1] if len(parts)>1 else ''
    if group == 'transportation': return 'transport.read' if read else 'transport.manage'
    if group == 'auth': return 'profile.read'
    if group == 'website': return 'website.manage'
    if group == 'users': return 'users.manage'
    if group == 'settings': return 'settings.read'
    if group == 'directory': return 'directory.read'
    if group == 'tasks': return 'tasks.read' if read else 'tasks.create' if method=='POST' else 'tasks.update_own'
    if group == 'work': return 'profile.read'  # resource-scoped checks in work endpoints
    if group == 'page-layouts': return 'profile.read'  # page context and Owner writes checked in endpoints
    if group == 'dashboard': return 'profile.read'  # aggregated from authorized queries only
    if group == 'audit': return 'audit.read'
    if group == 'booking-summary': return 'bookings.read'
    if group == 'bookings':
        if len(parts)>3 and parts[3].startswith('payment'): return 'payments.read' if read else 'payments.write'
        if len(parts)>3 and parts[3]=='assignment': return 'bookings.assign'
        return 'bookings.read' if read else 'bookings.write'
    if group in ('agreements','destinations','products'): return 'commercial.read' if read else 'commercial.write'
    if group == 'suppliers' and len(parts)>3 and parts[3] in ('agreements','documents'):
        return 'commercial.read' if read else 'commercial.write'
    if group in ('tours','suppliers','availability','payments','customers','trips'):
        return group + ('.read' if read else '.write')
    return 'DENIED'  # every new route needs an explicit policy
