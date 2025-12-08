"""Create scheduler_config table

Revision ID: 003
Revises: 002
Create Date: 2024-12-07 12:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP, JSON


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Crear tabla scheduler_config
    op.create_table(
        'scheduler_config',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('update_interval_minutes', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('market_hours_start', sa.String(length=5), nullable=False, server_default='09:00'),
        sa.Column('market_hours_end', sa.String(length=5), nullable=False, server_default='16:00'),
        sa.Column('symbols', JSON(), nullable=False, server_default='[]'),
        sa.Column('timeframes', JSON(), nullable=False, server_default='["1min"]'),
        sa.Column('last_run', TIMESTAMP(timezone=True), nullable=True),
        sa.Column('next_run', TIMESTAMP(timezone=True), nullable=True),
        sa.Column('created_at', TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Crear índice
    op.create_index('ix_scheduler_config_id', 'scheduler_config', ['id'], unique=False)
    
    # Insertar configuración por defecto
    op.execute("""
        INSERT INTO scheduler_config (enabled, update_interval_minutes, market_hours_start, 
                                     market_hours_end, symbols, timeframes, created_at, updated_at)
        VALUES (false, 1, '09:00', '16:00', '["ES", "NQ"]'::json, '["1min"]'::json, NOW(), NOW())
    """)


def downgrade() -> None:
    op.drop_index('ix_scheduler_config_id', table_name='scheduler_config')
    op.drop_table('scheduler_config')

