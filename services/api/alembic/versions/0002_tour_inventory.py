"""Tour inventory and URL-based galleries; preserve all existing rows.

Revision ID: 0002_tour_inventory
Revises: 0001_initial_schema
"""
from alembic import op
import sqlalchemy as sa

revision = '0002_tour_inventory'
down_revision = '0001_initial_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('suppliers', sa.Column('website', sa.String(2048), nullable=True))
    op.add_column('suppliers', sa.Column('notes', sa.Text(), nullable=True))
    op.add_column('products', sa.Column('slug', sa.String(240), nullable=True))
    op.execute("UPDATE products SET slug = 'legacy-product-' || id::text")
    op.alter_column('products', 'slug', nullable=False)
    op.create_unique_constraint('uq_products_slug', 'products', ['slug'])
    for column in [
        sa.Column('short_description', sa.String(500), nullable=False, server_default=''),
        sa.Column('category', sa.String(80), nullable=False, server_default='Uncategorized'),
        sa.Column('duration', sa.String(120), nullable=False, server_default=''),
        sa.Column('featured', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('location', sa.String(220), nullable=True),
        sa.Column('minimum_age', sa.Integer(), nullable=True),
        sa.Column('difficulty', sa.String(80), nullable=True),
    ]:
        op.add_column('products', column)
    op.create_check_constraint('ck_products_retail_nonnegative', 'products', 'retail_price >= 0')
    op.create_check_constraint('ck_products_cost_nonnegative', 'products', 'supplier_cost >= 0')
    op.create_check_constraint('ck_products_age_nonnegative', 'products', 'minimum_age IS NULL OR minimum_age >= 0')
    op.create_index('ix_products_supplier_id', 'products', ['supplier_id'])
    op.create_index('ix_products_public', 'products', ['product_type', 'active', 'featured'])
    op.create_table(
        'product_images',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('image_url', sa.String(2048), nullable=False),
        sa.Column('alt_text', sa.String(300), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_primary', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint('sort_order >= 0', name='ck_product_images_order_nonnegative'),
    )
    op.create_index('ix_product_images_order', 'product_images', ['product_id', 'sort_order', 'id'])
    op.create_index('uq_product_images_primary', 'product_images', ['product_id'], unique=True, postgresql_where=sa.text('is_primary'))


def downgrade() -> None:
    op.drop_table('product_images')
    op.drop_index('ix_products_public', table_name='products')
    op.drop_index('ix_products_supplier_id', table_name='products')
    for name in ['ck_products_retail_nonnegative', 'ck_products_cost_nonnegative', 'ck_products_age_nonnegative']:
        op.drop_constraint(name, 'products', type_='check')
    op.drop_constraint('uq_products_slug', 'products', type_='unique')
    for name in ['slug', 'short_description', 'category', 'duration', 'featured', 'location', 'minimum_age', 'difficulty']:
        op.drop_column('products', name)
    op.drop_column('suppliers', 'notes')
    op.drop_column('suppliers', 'website')
