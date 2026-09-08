"""Versioned presentation layouts and immutable Owner publication history."""
from alembic import op
import sqlalchemy as sa
revision='0010_page_builder'
down_revision='0009_ops_appearance'
branch_labels=None
depends_on=None

def upgrade():
 op.create_table('page_layouts',sa.Column('id',sa.Integer(),primary_key=True),sa.Column('page_type',sa.String(80),nullable=False,unique=True),sa.Column('schema_version',sa.Integer(),nullable=False,server_default='1'),sa.Column('version',sa.Integer(),nullable=False,server_default='0'),sa.Column('draft',sa.JSON(),nullable=True),sa.Column('published',sa.JSON(),nullable=True),sa.Column('updated_by_user_id',sa.Integer(),sa.ForeignKey('internal_users.id'),nullable=True),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()))
 op.create_table('page_layout_revisions',sa.Column('id',sa.Integer(),primary_key=True),sa.Column('layout_id',sa.Integer(),sa.ForeignKey('page_layouts.id'),nullable=False),sa.Column('number',sa.Integer(),nullable=False),sa.Column('schema_version',sa.Integer(),nullable=False,server_default='1'),sa.Column('content',sa.JSON(),nullable=False),sa.Column('actor_user_id',sa.Integer(),sa.ForeignKey('internal_users.id'),nullable=False),sa.Column('action',sa.String(20),nullable=False),sa.Column('restored_from_id',sa.Integer(),sa.ForeignKey('page_layout_revisions.id'),nullable=True),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),sa.UniqueConstraint('layout_id','number',name='uq_page_layout_revision_number'))
 if op.get_bind().dialect.name=='postgresql':
  op.execute("CREATE FUNCTION vv_layout_revision_immutable() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'Page layout revisions are immutable'; END; $$")
  op.execute('CREATE TRIGGER vv_layout_revision_immutable BEFORE UPDATE OR DELETE ON page_layout_revisions FOR EACH ROW EXECUTE FUNCTION vv_layout_revision_immutable()')

def downgrade():
 if op.get_bind().dialect.name=='postgresql':
  op.execute('DROP TRIGGER vv_layout_revision_immutable ON page_layout_revisions')
  op.execute('DROP FUNCTION vv_layout_revision_immutable()')
 op.drop_table('page_layout_revisions');op.drop_table('page_layouts')
