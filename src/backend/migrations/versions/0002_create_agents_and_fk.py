"""create agents table and add fk to conversations

Revision ID: 0002_create_agents
Revises: 0001_initial
Create Date: 2025-08-03 04:18:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_create_agents'
down_revision = '0001_initial'
branch_labels = None
depends_on = None

def upgrade():
    # Create agents table
    op.create_table(
        'agents',
        sa.Column('uuid', sa.String(length=36), primary_key=True, index=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('prompt', sa.Text(), nullable=True),
        sa.Column('image', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    # Add foreign key constraint from conversations.agent_uuid to agents.uuid
    op.create_foreign_key(
        'fk_conversations_agent_uuid_agents',
        'conversations',
        'agents',
        ['agent_uuid'],
        ['uuid']
    )
    # Remove deprecated agent_name column
    op.drop_column('conversations', 'agent_name')


def downgrade():
    # Re-add agent_name column
    op.add_column(
        'conversations',
        sa.Column('agent_name', sa.String(length=50), nullable=False, server_default='bunny')
    )
    # Remove foreign key constraint
    op.drop_constraint('fk_conversations_agent_uuid_agents', 'conversations', type_='foreignkey')
    # Drop agents table
    op.drop_table('agents')