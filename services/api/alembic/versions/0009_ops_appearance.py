"""Authenticated user's Operations appearance preference."""
from alembic import op
import sqlalchemy as sa

revision = '0009_ops_appearance'
down_revision = '0008_transportation_foundation'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('internal_users', sa.Column('appearance', sa.String(10), nullable=False, server_default='dark'))
    op.create_check_constraint('ck_internal_user_appearance', 'internal_users', "appearance IN ('light','dark','system')")

def downgrade():
    op.drop_constraint('ck_internal_user_appearance', 'internal_users', type_='check')
    op.drop_column('internal_users', 'appearance')
