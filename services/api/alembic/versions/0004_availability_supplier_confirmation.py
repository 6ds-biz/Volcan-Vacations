"""Manual availability and append-only supplier confirmation history."""
from alembic import op
import sqlalchemy as sa

revision = '0004_availability_confirmation'
down_revision = '0003_booking_requests'
branch_labels = None
depends_on = None


def upgrade():
    # Preserve every existing record. Ambiguous legacy inventory needs review,
    # never silent merging, deletion, or invented freshness/confirmation.
    op.add_column('availabilities', sa.Column('source', sa.String(30), nullable=False, server_default='manual'))
    op.add_column('availabilities', sa.Column('notes', sa.Text(), nullable=True))
    op.add_column('availabilities', sa.Column('last_checked_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('availabilities', sa.Column('version', sa.Integer(), nullable=False, server_default='1'))
    op.alter_column('availabilities', 'status', server_default='unknown')
    op.create_unique_constraint('uq_availability_product_date', 'availabilities', ['product_id', 'date'])
    for name, expression in [
        ('status', "status IN ('unknown','available','limited','unavailable','closed')"),
        ('source', "source IN ('manual','supplier','api','inventory')"),
        ('capacity', 'capacity IS NULL OR capacity >= 0'),
        ('remaining', 'remaining_capacity IS NULL OR remaining_capacity >= 0'),
        ('remaining_capacity', 'capacity IS NULL OR remaining_capacity IS NULL OR remaining_capacity <= capacity'),
        ('positive_inventory', "status NOT IN ('available','limited') OR ((capacity IS NULL OR capacity > 0) AND (remaining_capacity IS NULL OR remaining_capacity > 0))"),
        ('version', 'version > 0'),
    ]:
        op.create_check_constraint(f'ck_availability_{name}', 'availabilities', expression)
    op.create_index('ix_availability_date_status', 'availabilities', ['date', 'status'])
    op.add_column('reservations', sa.Column('supplier_id', sa.Integer(), nullable=True))
    op.execute('UPDATE reservations SET supplier_id = products.supplier_id FROM products WHERE products.id = reservations.product_id')
    op.alter_column('reservations', 'supplier_id', nullable=False)
    op.create_foreign_key('fk_reservation_supplier', 'reservations', 'suppliers', ['supplier_id'], ['id'])
    for column in [
        sa.Column('availability_status', sa.String(30), nullable=False, server_default='unknown'),
        sa.Column('supplier_confirmation_status', sa.String(30), nullable=False, server_default='not_requested'),
        sa.Column('supplier_confirmation_reference', sa.String(200), nullable=True),
        sa.Column('supplier_confirmed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('supplier_contacted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('supplier_response_notes', sa.Text(), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
    ]:
        op.add_column('reservations', column)
    for name, expression in [
        ('availability_status', "availability_status IN ('unknown','available','limited','unavailable','closed')"),
        ('supplier_status', "supplier_confirmation_status IN ('not_requested','awaiting_supplier','confirmed','declined','alternative_offered')"),
        ('confirmation_available', "supplier_confirmation_status != 'confirmed' OR availability_status = 'available'"),
        ('version', 'version > 0'),
    ]:
        op.create_check_constraint(f'ck_reservation_{name}', 'reservations', expression)
    op.create_table('supplier_confirmation_events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('reservation_id', sa.Integer(), sa.ForeignKey('reservations.id'), nullable=False),
        sa.Column('supplier_id', sa.Integer(), sa.ForeignKey('suppliers.id'), nullable=False),
        sa.Column('event_type', sa.String(30), nullable=False),
        sa.Column('contact_method', sa.String(30), nullable=True),
        sa.Column('operator_identifier', sa.String(120), nullable=True),
        sa.Column('status', sa.String(30), nullable=False),
        sa.Column('reservation_status', sa.String(80), nullable=False),
        sa.Column('availability_status', sa.String(30), nullable=False),
        sa.Column('reference', sa.String(200), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('alternative_product_id', sa.Integer(), sa.ForeignKey('products.id'), nullable=True),
        sa.Column('alternative_date', sa.Date(), nullable=True),
        sa.Column('alternative_time', sa.Time(), nullable=True),
        sa.Column('occurred_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('command_id', sa.String(36), nullable=False),
        sa.Column('command_hash', sa.String(64), nullable=False),
        sa.UniqueConstraint('reservation_id', 'command_id', name='uq_supplier_event_command'),
        sa.CheckConstraint("event_type IN ('contacted','follow_up','confirmed','declined','alternative_offered','availability_checked','note')", name='ck_supplier_event_type'),
        sa.CheckConstraint("contact_method IS NULL OR contact_method IN ('phone','email','whatsapp','supplier_portal','other')", name='ck_supplier_event_method'),
    )
    op.create_index('ix_supplier_event_timeline', 'supplier_confirmation_events', ['reservation_id', 'id'])


def downgrade():
    raise RuntimeError('Supplier history must be preserved. Downgrade requires a reviewed data migration or verified backup.')
