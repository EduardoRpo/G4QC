"""Initial migration - Create market_data table

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Crear tabla market_data
    op.create_table(
        'market_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(length=10), nullable=False),
        sa.Column('timeframe', sa.String(length=10), nullable=False),
        sa.Column('timestamp', TIMESTAMP(timezone=True), nullable=False),
        sa.Column('open', sa.Float(), nullable=False),
        sa.Column('high', sa.Float(), nullable=False),
        sa.Column('low', sa.Float(), nullable=False),
        sa.Column('close', sa.Float(), nullable=False),
        sa.Column('volume', sa.Integer(), nullable=False),
        sa.Column('count', sa.Integer(), server_default='0', nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Crear índices
    op.create_index('ix_market_data_id', 'market_data', ['id'], unique=False)
    op.create_index('ix_market_data_symbol', 'market_data', ['symbol'], unique=False)
    op.create_index('ix_market_data_timestamp', 'market_data', ['timestamp'], unique=False)
    op.create_index('idx_symbol_timeframe_timestamp', 'market_data', 
                   ['symbol', 'timeframe', 'timestamp'], unique=False)
    
    # Nota: TimescaleDB hypertable es opcional
    # La tabla funciona perfectamente como tabla normal de PostgreSQL
    # Si deseas usar TimescaleDB, puedes convertirla después manualmente:
    #   CREATE EXTENSION IF NOT EXISTS timescaledb;
    #   SELECT create_hypertable('market_data', 'timestamp', chunk_time_interval => INTERVAL '1 day');


def downgrade() -> None:
    op.drop_index('idx_symbol_timeframe_timestamp', table_name='market_data')
    op.drop_index('ix_market_data_timestamp', table_name='market_data')
    op.drop_index('ix_market_data_symbol', table_name='market_data')
    op.drop_index('ix_market_data_id', table_name='market_data')
    op.drop_table('market_data')

