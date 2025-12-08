"""Add unique constraint to market_data

Revision ID: 002
Revises: 001
Create Date: 2024-12-07 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Primero, eliminar duplicados existentes si los hay
    # Mantener solo el registro con menor ID para cada combinación única
    op.execute("""
        DELETE FROM market_data
        WHERE id IN (
            SELECT id
            FROM (
                SELECT id,
                    ROW_NUMBER() OVER (
                        PARTITION BY symbol, timeframe, timestamp 
                        ORDER BY id
                    ) as rn
                FROM market_data
            ) t
            WHERE t.rn > 1
        )
    """)
    
    # Agregar constraint UNIQUE
    op.create_unique_constraint(
        'uq_market_data_symbol_tf_ts',
        'market_data',
        ['symbol', 'timeframe', 'timestamp']
    )


def downgrade() -> None:
    # Eliminar constraint UNIQUE
    op.drop_constraint(
        'uq_market_data_symbol_tf_ts',
        'market_data',
        type_='unique'
    )

