"""Internal identity, opaque sessions, tasks and authenticated audit actors."""
from alembic import op
import sqlalchemy as sa

revision = "0007_internal_users_tasks"
down_revision = "0006_platform_foundation"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('internal_login_guards',
    sa.Column('key', sa.String(length=64), nullable=False),
    sa.Column('attempts', sa.Integer(), server_default='0', nullable=False),
    sa.Column('window_started_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('key')
    )
    op.create_table('internal_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=180), nullable=False),
    sa.Column('display_name', sa.String(length=140), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=30), nullable=False),
    sa.Column('active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.Column('dashboard_profile', sa.String(length=30), nullable=False),
    sa.Column('must_change_password', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("dashboard_profile IN ('Owner','Operations','Staff')", name='ck_internal_user_profile'),
    sa.CheckConstraint("role IN ('owner_admin','operations_partner','staff')", name='ck_internal_user_role'),
    sa.CheckConstraint('email = lower(trim(email))', name='ck_internal_user_email'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('internal_audit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('actor_user_id', sa.Integer(), nullable=True),
    sa.Column('entity_type', sa.String(length=40), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('action', sa.String(length=30), nullable=False),
    sa.Column('summary', sa.String(length=240), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['actor_user_id'], ['internal_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_internal_audit_actor_user_id'), 'internal_audit', ['actor_user_id'], unique=False)
    op.create_index(op.f('ix_internal_audit_entity_id'), 'internal_audit', ['entity_id'], unique=False)
    op.create_table('internal_sessions',
    sa.Column('token_hash', sa.String(length=64), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('csrf_token', sa.String(length=64), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['internal_users.id'], ),
    sa.PrimaryKeyConstraint('token_hash')
    )
    op.create_index(op.f('ix_internal_sessions_expires_at'), 'internal_sessions', ['expires_at'], unique=False)
    op.create_index(op.f('ix_internal_sessions_user_id'), 'internal_sessions', ['user_id'], unique=False)
    op.create_table('ops_tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=220), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('assigned_user_id', sa.Integer(), nullable=True),
    sa.Column('created_by_user_id', sa.Integer(), nullable=True),
    sa.Column('completed_by_user_id', sa.Integer(), nullable=True),
    sa.Column('related_entity_type', sa.String(length=30), nullable=True),
    sa.Column('related_entity_id', sa.Integer(), nullable=True),
    sa.Column('priority', sa.String(length=20), server_default='normal', nullable=False),
    sa.Column('status', sa.String(length=20), server_default='open', nullable=False),
    sa.Column('source', sa.String(length=30), server_default='manual', nullable=False),
    sa.Column('queue_role', sa.String(length=30), server_default='operations', nullable=False),
    sa.Column('system_key', sa.String(length=180), nullable=True),
    sa.Column('due_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('version', sa.Integer(), server_default='1', nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("(related_entity_type IS NULL AND related_entity_id IS NULL) OR (related_entity_type IN ('booking','supplier','tour','payment','availability','agreement','customer') AND related_entity_id IS NOT NULL AND related_entity_id > 0)", name='ck_ops_task_related'),
    sa.CheckConstraint("priority IN ('low','normal','high','urgent')", name='ck_ops_task_priority'),
    sa.CheckConstraint("queue_role IN ('operations','owner_admin')", name='ck_ops_task_queue'),
    sa.CheckConstraint("source IN ('manual','system_generated')", name='ck_ops_task_source'),
    sa.CheckConstraint("status IN ('open','in_progress','waiting','completed','cancelled')", name='ck_ops_task_status'),
    sa.CheckConstraint('version > 0', name='ck_ops_task_version'),
    sa.ForeignKeyConstraint(['assigned_user_id'], ['internal_users.id'], ),
    sa.ForeignKeyConstraint(['completed_by_user_id'], ['internal_users.id'], ),
    sa.ForeignKeyConstraint(['created_by_user_id'], ['internal_users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('system_key')
    )
    op.create_index(op.f('ix_ops_tasks_assigned_user_id'), 'ops_tasks', ['assigned_user_id'], unique=False)
    op.create_index(op.f('ix_ops_tasks_related_entity_id'), 'ops_tasks', ['related_entity_id'], unique=False)
    op.add_column('reservations', sa.Column('assigned_user_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_reservations_assigned_user_id'), 'reservations', ['assigned_user_id'], unique=False)
    op.create_foreign_key('fk_reservations_assignee', 'reservations', 'internal_users', ['assigned_user_id'], ['id'])
    op.add_column('supplier_confirmation_events', sa.Column('actor_user_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_supplier_events_actor', 'supplier_confirmation_events', 'internal_users', ['actor_user_id'], ['id'])

def downgrade():
    op.drop_constraint('fk_supplier_events_actor', 'supplier_confirmation_events', type_='foreignkey')
    op.drop_column('supplier_confirmation_events', 'actor_user_id')
    op.drop_constraint('fk_reservations_assignee', 'reservations', type_='foreignkey')
    op.drop_index(op.f('ix_reservations_assigned_user_id'), table_name='reservations')
    op.drop_column('reservations', 'assigned_user_id')
    op.drop_index(op.f('ix_ops_tasks_related_entity_id'), table_name='ops_tasks')
    op.drop_index(op.f('ix_ops_tasks_assigned_user_id'), table_name='ops_tasks')
    op.drop_table('ops_tasks')
    op.drop_index(op.f('ix_internal_sessions_user_id'), table_name='internal_sessions')
    op.drop_index(op.f('ix_internal_sessions_expires_at'), table_name='internal_sessions')
    op.drop_table('internal_sessions')
    op.drop_index(op.f('ix_internal_audit_entity_id'), table_name='internal_audit')
    op.drop_index(op.f('ix_internal_audit_actor_user_id'), table_name='internal_audit')
    op.drop_table('internal_audit')
    op.drop_table('internal_users')
    op.drop_table('internal_login_guards')
