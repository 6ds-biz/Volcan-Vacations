"""Add optional geography and internal supplier commercial reference data."""
from alembic import op
import sqlalchemy as sa

revision = '0006_platform_foundation'
down_revision = '0005_paypal_payments'
branch_labels = None
depends_on = None


def timestamps():
    return [sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)]


def upgrade():
    op.add_column('suppliers', sa.Column('relationship_status', sa.String(30), server_default='prospect', nullable=False))
    op.create_check_constraint('ck_supplier_relationship_status', 'suppliers', "relationship_status IN ('prospect','contacted','rates_requested','rates_received','negotiating','contracted','active','inactive','declined')")
    op.create_table('destinations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('parent_id', sa.Integer(), sa.ForeignKey('destinations.id'), nullable=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('slug', sa.String(240), unique=True, nullable=False),
        sa.Column('destination_type', sa.String(30), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('sort_order', sa.Integer(), server_default='0', nullable=False),
        *timestamps(),
        sa.CheckConstraint('parent_id IS NULL OR parent_id != id', name='ck_destination_parent'),
        sa.CheckConstraint("destination_type IN ('country','region','destination','city','zone','airport')", name='ck_destination_type'),
        sa.CheckConstraint('sort_order >= 0', name='ck_destination_sort'))
    op.create_index('ix_destinations_parent_id', 'destinations', ['parent_id'])
    op.create_table('product_destinations',
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id'), primary_key=True),
        sa.Column('destination_id', sa.Integer(), sa.ForeignKey('destinations.id'), primary_key=True))
    op.create_table('supplier_services',
        sa.Column('supplier_id', sa.Integer(), sa.ForeignKey('suppliers.id'), primary_key=True),
        sa.Column('service_type', sa.String(30), primary_key=True),
        sa.CheckConstraint("service_type IN ('tour','transportation','hotel')", name='ck_supplier_service_type'))
    op.create_table('supplier_agreements',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('supplier_id', sa.Integer(), sa.ForeignKey('suppliers.id'), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('effective_from', sa.Date(), nullable=False),
        sa.Column('effective_to', sa.Date(), nullable=True),
        sa.Column('currency', sa.String(3), server_default='USD', nullable=False),
        sa.Column('status', sa.String(30), server_default='draft', nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        *timestamps(),
        sa.CheckConstraint('effective_to IS NULL OR effective_to >= effective_from', name='ck_agreement_dates'),
        sa.CheckConstraint("status IN ('draft','in_review','approved','expired','terminated')", name='ck_agreement_status'),
        sa.CheckConstraint("currency IN ('USD','CRC')", name='ck_agreement_currency'))
    op.create_index('ix_supplier_agreements_supplier_id', 'supplier_agreements', ['supplier_id'])
    op.create_table('product_rates',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('agreement_id', sa.Integer(), sa.ForeignKey('supplier_agreements.id'), nullable=False),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id'), nullable=False),
        sa.Column('label', sa.String(200), nullable=False),
        sa.Column('effective_from', sa.Date(), nullable=False),
        sa.Column('effective_to', sa.Date(), nullable=False),
        sa.Column('unit_type', sa.String(30), nullable=False),
        sa.Column('net_amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('retail_amount', sa.Numeric(12, 2), nullable=True),
        *timestamps(),
        sa.CheckConstraint('effective_to >= effective_from', name='ck_product_rate_dates'),
        sa.CheckConstraint('net_amount >= 0 AND (retail_amount IS NULL OR retail_amount >= 0)', name='ck_product_rate_money'),
        sa.CheckConstraint("unit_type IN ('per_person','per_vehicle','per_night')", name='ck_product_rate_unit'))
    op.create_index('ix_product_rates_agreement_id', 'product_rates', ['agreement_id'])
    op.create_index('ix_product_rates_product_id', 'product_rates', ['product_id'])
    op.create_table('supplier_documents',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('supplier_id', sa.Integer(), sa.ForeignKey('suppliers.id'), nullable=False),
        sa.Column('agreement_id', sa.Integer(), sa.ForeignKey('supplier_agreements.id'), nullable=True),
        sa.Column('document_type', sa.String(30), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('external_url', sa.String(2048), nullable=True),
        sa.Column('storage_key', sa.String(500), nullable=True),
        sa.Column('effective_date', sa.Date(), nullable=True),
        sa.Column('expiration_date', sa.Date(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        *timestamps(),
        sa.CheckConstraint("document_type IN ('contract','rate_sheet','terms','cancellation_policy','media_kit')", name='ck_supplier_document_type'),
        sa.CheckConstraint('effective_date IS NULL OR expiration_date IS NULL OR expiration_date >= effective_date', name='ck_supplier_document_dates'))
    op.create_index('ix_supplier_documents_supplier_id', 'supplier_documents', ['supplier_id'])


def downgrade():
    raise RuntimeError('Preserve geography and commercial records; use a reviewed forward recovery migration.')
