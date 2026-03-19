"""initial migration: create temporal_records and api_keys tables

Revision ID: 001_initial
Revises: 
Create Date: 2026-03-19

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── temporal_records ──────────────────────────────────────────────────────
    op.create_table(
        'temporal_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('entity_type', sa.String(length=100), nullable=False),
        sa.Column('entity_id', sa.String(length=255), nullable=False),
        sa.Column('valid_from', sa.DateTime(timezone=True), nullable=False),
        sa.Column('valid_to', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=True),
        sa.Column('data', sa.JSON(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_temporal_records_id', 'temporal_records', ['id'])
    op.create_index('ix_temporal_records_entity_type', 'temporal_records', ['entity_type'])
    op.create_index('ix_temporal_records_entity_id', 'temporal_records', ['entity_id'])

    # Composite index for fast time-travel queries
    op.create_index(
        'ix_temporal_records_lookup',
        'temporal_records',
        ['entity_type', 'entity_id', 'valid_from'],
    )

    # ── api_keys ──────────────────────────────────────────────────────────────
    op.create_table(
        'api_keys',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('hashed_key', sa.String(length=255), nullable=False),
        sa.Column('prefix', sa.String(length=20), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('hashed_key'),
    )
    op.create_index('ix_api_keys_id', 'api_keys', ['id'])


def downgrade() -> None:
    op.drop_index('ix_api_keys_id', table_name='api_keys')
    op.drop_table('api_keys')

    op.drop_index('ix_temporal_records_lookup', table_name='temporal_records')
    op.drop_index('ix_temporal_records_entity_id', table_name='temporal_records')
    op.drop_index('ix_temporal_records_entity_type', table_name='temporal_records')
    op.drop_index('ix_temporal_records_id', table_name='temporal_records')
    op.drop_table('temporal_records')
