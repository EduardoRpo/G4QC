"""
Scheduler Configuration Models
"""
from sqlalchemy import Column, String, Boolean, Integer, DateTime, JSON
from sqlalchemy.dialects.postgresql import TIMESTAMP
from app.core.database import Base
from datetime import datetime


class SchedulerConfig(Base):
    """
    Configuración del scheduler de actualización automática de datos
    """
    __tablename__ = "scheduler_config"
    
    id = Column(Integer, primary_key=True, index=True)
    enabled = Column(Boolean, default=False, nullable=False)  # Activar/desactivar scheduler
    update_interval_minutes = Column(Integer, default=1, nullable=False)  # Intervalo de actualización
    market_hours_start = Column(String(5), default="09:00", nullable=False)  # Hora inicio (HH:MM)
    market_hours_end = Column(String(5), default="16:00", nullable=False)  # Hora fin (HH:MM)
    symbols = Column(JSON, default=list, nullable=False)  # Lista de símbolos a actualizar
    timeframes = Column(JSON, default=["1min"], nullable=False)  # Timeframes a extraer
    last_run = Column(TIMESTAMP(timezone=True), nullable=True)  # Última ejecución
    next_run = Column(TIMESTAMP(timezone=True), nullable=True)  # Próxima ejecución programada
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<SchedulerConfig(enabled={self.enabled}, interval={self.update_interval_minutes}min)>"

