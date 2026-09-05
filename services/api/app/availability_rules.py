"""Shared vocabulary; supplier adapters must use the same transactional commands."""
from datetime import datetime, timedelta, timezone

AVAILABILITY_STATUSES = ('unknown', 'available', 'limited', 'unavailable', 'closed')
SOURCES = ('manual', 'supplier', 'api', 'inventory')
SUPPLIER_STATUSES = ('not_requested', 'awaiting_supplier', 'confirmed', 'declined', 'alternative_offered')
CONTACT_METHODS = ('phone', 'email', 'whatsapp', 'supplier_portal', 'other')
EVENT_TYPES = ('contacted', 'follow_up', 'confirmed', 'declined', 'alternative_offered', 'availability_checked', 'note')
FRESHNESS_HOURS = 24


def utcnow():
    return datetime.now(timezone.utc)


def aware(value):
    # SQLite test timestamps are naive; all production inputs require an offset.
    return value.replace(tzinfo=timezone.utc) if value and value.tzinfo is None else value


def is_stale(checked_at):
    return checked_at is None or aware(checked_at) < utcnow() - timedelta(hours=FRESHNESS_HOURS)
