"""Scoped, expiring Owner handoff to the public website canvas."""
from alembic import op
import sqlalchemy as sa
revision='0011_website_edit_sessions'
down_revision='0010_page_builder'
branch_labels=None
depends_on=None

def upgrade():
 op.create_table('website_edit_sessions',
  sa.Column('ticket_hash',sa.String(64),primary_key=True),
  sa.Column('canvas_hash',sa.String(64),unique=True,nullable=True),
  sa.Column('internal_session_hash',sa.String(64),sa.ForeignKey('internal_sessions.token_hash',ondelete='CASCADE'),nullable=False),
  sa.Column('user_id',sa.Integer(),sa.ForeignKey('internal_users.id'),nullable=False),
  sa.Column('page_type',sa.String(80),nullable=False),
  sa.Column('ticket_expires_at',sa.DateTime(timezone=True),nullable=False),
  sa.Column('expires_at',sa.DateTime(timezone=True),nullable=False),
  sa.Column('redeemed_at',sa.DateTime(timezone=True),nullable=True))

def downgrade():
 op.drop_table('website_edit_sessions')
