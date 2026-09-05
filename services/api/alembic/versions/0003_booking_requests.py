"""Customer intake and booking requests, preserving existing records."""
from alembic import op
import sqlalchemy as sa

revision = '0003_booking_requests'
down_revision = '0002_tour_inventory'
branch_labels = None
depends_on = None


def upgrade():
    # Stop for human review of ambiguous existing emails; never merge/delete.
    op.execute("""DO $$ BEGIN
      IF EXISTS (SELECT lower(btrim(email)) FROM customers GROUP BY lower(btrim(email)) HAVING count(*) > 1)
      THEN RAISE EXCEPTION 'Duplicate normalized customer emails: review manually before migrating'; END IF;
    END $$""")
    op.execute('UPDATE customers SET email = lower(btrim(email))')
    op.create_check_constraint('ck_customers_normalized_email', 'customers', 'email = lower(trim(email))')
    op.add_column('customers', sa.Column('preferred_contact_method', sa.String(30), nullable=True))
    op.add_column('customers', sa.Column('notes', sa.Text(), nullable=True))
    op.add_column('travelers', sa.Column('traveler_type', sa.String(30), nullable=True))
    op.add_column('travelers', sa.Column('notes', sa.Text(), nullable=True))
    op.add_column('trips', sa.Column('reference', sa.String(40), nullable=True))
    op.execute("UPDATE trips SET reference = 'VV-LEGACY-' || id::text")
    op.alter_column('trips', 'reference', nullable=False)
    op.create_unique_constraint('uq_trips_reference', 'trips', ['reference'])
    for name in ['name', 'start_date', 'end_date']:
        op.alter_column('trips', name, nullable=True)
    op.add_column('trips', sa.Column('party_size', sa.Integer(), nullable=False, server_default='1'))
    op.add_column('trips', sa.Column('notes', sa.Text(), nullable=True))
    op.alter_column('trips', 'status', server_default='inquiry')
    op.create_check_constraint('ck_trips_party_size', 'trips', 'party_size > 0')
    op.create_check_constraint('ck_trips_dates', 'trips', 'start_date IS NULL OR end_date IS NULL OR end_date >= start_date')
    op.create_table('trip_travelers',
        sa.Column('trip_id', sa.Integer(), sa.ForeignKey('trips.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('traveler_id', sa.Integer(), sa.ForeignKey('travelers.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('position', sa.Integer(), nullable=False),
    )
    for column in [
        sa.Column('requested_time', sa.Time(), nullable=True),
        sa.Column('customer_notes', sa.Text(), nullable=True),
        sa.Column('internal_notes', sa.Text(), nullable=True),
        sa.Column('tour_name_snapshot', sa.String(220), nullable=True),
        sa.Column('contact_snapshot', sa.JSON(), nullable=True),
        sa.Column('submission_key', sa.String(36), nullable=True),
        sa.Column('submission_hash', sa.String(64), nullable=True),
        sa.Column('submission_receipt', sa.JSON(), nullable=True),
    ]:
        op.add_column('reservations', column)
    op.create_unique_constraint('uq_reservations_submission_key', 'reservations', ['submission_key'])
    op.create_check_constraint('ck_reservations_quantity', 'reservations', 'quantity > 0')
    op.create_index('ix_reservations_inbox', 'reservations', ['status', 'created_at'])
    op.alter_column('reservations', 'status', server_default='new')


def downgrade():
    # Returning to NOT NULL trip dates could destroy/invent intake data.
    raise RuntimeError('Booking intake downgrade requires a reviewed data migration; restore from a verified backup if needed.')
