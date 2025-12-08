"""
Market Data Models
"""
from sqlalchemy import Column, String, DateTime, Float, Integer, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP
from app.core.database import Base
from datetime import datetime


class MarketData(Base):
    """
    Modelo para almacenar datos de mercado históricos
    """
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False, index=True)
    timeframe = Column(String(10), nullable=False)  # 1min, 5min, 15min, etc.
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, index=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    count = Column(Integer, default=0)
    
    # Índices compuestos para queries eficientes
    # Constraint UNIQUE para prevenir duplicados
    __table_args__ = (
        Index('idx_symbol_timeframe_timestamp', 'symbol', 'timeframe', 'timestamp'),
        UniqueConstraint('symbol', 'timeframe', 'timestamp', name='uq_market_data_symbol_tf_ts'),
    )
    
    def __repr__(self):
        return f"<MarketData(symbol={self.symbol}, timeframe={self.timeframe}, timestamp={self.timestamp})>"

