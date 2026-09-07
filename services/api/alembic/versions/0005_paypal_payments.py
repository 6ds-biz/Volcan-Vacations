"""Sandbox payment intents, secure links and provider reconciliation receipts."""
from alembic import op
import sqlalchemy as sa

revision = '0005_paypal_payments'
down_revision = '0004_availability_confirmation'
branch_labels = None
depends_on = None


def upgrade():
    for column in [sa.Column('payment_token_hash', sa.String(64), nullable=True),
                   sa.Column('payment_token_expires_at', sa.DateTime(timezone=True), nullable=True),
                   sa.Column('payment_due_at', sa.DateTime(timezone=True), nullable=True)]:
        op.add_column('reservations', column)
    op.create_unique_constraint('uq_reservation_payment_token', 'reservations', ['payment_token_hash'])
    for column in [
        sa.Column('reservation_id', sa.Integer(), nullable=True),
        sa.Column('currency', sa.String(3), nullable=False, server_default='USD'),
        sa.Column('provider', sa.String(30), nullable=False, server_default='manual'),
        sa.Column('provider_environment', sa.String(20), nullable=True),
        sa.Column('provider_order_id', sa.String(80), nullable=True),
        sa.Column('provider_capture_id', sa.String(80), nullable=True),
        sa.Column('idempotency_key', sa.String(36), nullable=True),
        sa.Column('capture_request_id', sa.String(36), nullable=True),
        sa.Column('create_started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('capture_started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('failure_code', sa.String(80), nullable=True),
        sa.Column('failure_message', sa.String(500), nullable=True),
        sa.Column('paid_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('refunded_amount', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('reconciliation_required', sa.Boolean(), nullable=False, server_default=sa.text('false')),
    ]:
        op.add_column('payments', column)
    op.create_foreign_key('fk_payment_reservation', 'payments', 'reservations', ['reservation_id'], ['id'])
    for field in ['reservation_id', 'provider_order_id', 'provider_capture_id', 'idempotency_key', 'capture_request_id']:
        op.create_unique_constraint(f'uq_payment_{field}', 'payments', [field])
    for name, expression in [
        ('amount', 'amount >= 0'), ('refunded_amount', 'refunded_amount >= 0 AND refunded_amount <= amount'),
        ('status', "status IN ('pending','created','approved','captured','failed','cancelled','refunded','partially_refunded')"),
        ('paypal_scope', "provider != 'paypal' OR (reservation_id IS NOT NULL AND currency = 'USD' AND provider_environment = 'sandbox' AND amount > 0)"),
    ]:
        op.create_check_constraint(f'ck_payment_{name}', 'payments', expression)
    op.create_index('ix_payment_status_created', 'payments', ['status', 'created_at'])
    op.create_table('payment_webhook_events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('provider_event_id', sa.String(100), unique=True, nullable=False),
        sa.Column('event_type', sa.String(100), nullable=False),
        sa.Column('payment_id', sa.Integer(), sa.ForeignKey('payments.id'), nullable=True),
        sa.Column('resource_id', sa.String(100), nullable=True),
        sa.Column('outcome', sa.String(30), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_table('payment_refunds',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('payment_id', sa.Integer(), sa.ForeignKey('payments.id'), nullable=False),
        sa.Column('provider_refund_id', sa.String(80), unique=True, nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('currency', sa.String(3), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint('amount > 0', name='ck_payment_refund_positive'))
    op.create_index('ix_payment_refunds_payment_id', 'payment_refunds', ['payment_id'])


def downgrade():
    raise RuntimeError('Payment and refund audit data must be preserved; use reviewed recovery instead of automatic downgrade.')
