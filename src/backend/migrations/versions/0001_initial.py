"""Initial migration

Revision ID: 0001_initial
Revises: 
Create Date: 2025-08-03 02:58:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Tabela de configurações de provedores
    op.create_table(
        "configs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider", sa.String(length=255), nullable=False),
        sa.Column("api_key_encrypted", sa.LargeBinary(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    # Tabela de conversas com thread_uuid, agent_uuid e lista de ferramentas
    op.create_table(
        "conversations",
        sa.Column("thread_uuid", sa.String(length=36), primary_key=True),
        sa.Column("agent_uuid", sa.String(length=36), nullable=True),
        sa.Column("tools_enabled", ARRAY(sa.String()), nullable=False, server_default="{}"),
        sa.Column("messages", JSONB(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table("conversations")
    op.drop_table("configs")