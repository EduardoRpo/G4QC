"""
Scheduler API Endpoints - Control del scheduler de actualización automática
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from app.core.database import get_db
from app.services.scheduler.data_scheduler import DataScheduler

router = APIRouter()


class SchedulerConfigRequest(BaseModel):
    """Request para actualizar configuración del scheduler"""
    update_interval_minutes: Optional[int] = None
    market_hours_start: Optional[str] = None  # Formato: "HH:MM"
    market_hours_end: Optional[str] = None  # Formato: "HH:MM"
    symbols: Optional[List[str]] = None
    timeframes: Optional[List[str]] = None


class SchedulerStatusResponse(BaseModel):
    """Response con estado del scheduler"""
    enabled: bool
    update_interval_minutes: int
    market_hours_start: str
    market_hours_end: str
    symbols: List[str]
    timeframes: List[str]
    last_run: Optional[str]
    next_run: Optional[str]
    jobs_count: int


# Variable global para el scheduler (se inicializa en main.py)
_scheduler_instance: Optional[DataScheduler] = None


def get_scheduler(db: Session = Depends(get_db)) -> DataScheduler:
    """Dependency para obtener instancia del scheduler"""
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = DataScheduler(db)
    return _scheduler_instance


def set_scheduler_instance(instance: DataScheduler):
    """Establecer instancia global del scheduler (usado en main.py)"""
    global _scheduler_instance
    _scheduler_instance = instance


@router.get("/status", response_model=SchedulerStatusResponse)
async def get_scheduler_status(scheduler: DataScheduler = Depends(get_scheduler)):
    """
    Obtener estado actual del scheduler
    """
    status = scheduler.get_status()
    return status


@router.post("/enable")
async def enable_scheduler(scheduler: DataScheduler = Depends(get_scheduler)):
    """
    Activar el scheduler de actualización automática
    """
    scheduler.enable()
    return {
        "status": "success",
        "message": "Scheduler activado",
        "scheduler_status": scheduler.get_status()
    }


@router.post("/disable")
async def disable_scheduler(scheduler: DataScheduler = Depends(get_scheduler)):
    """
    Desactivar el scheduler de actualización automática
    """
    scheduler.disable()
    return {
        "status": "success",
        "message": "Scheduler desactivado",
        "scheduler_status": scheduler.get_status()
    }


@router.put("/config")
async def update_scheduler_config(
    config: SchedulerConfigRequest,
    scheduler: DataScheduler = Depends(get_scheduler)
):
    """
    Actualizar configuración del scheduler
    
    - **update_interval_minutes**: Intervalo de actualización en minutos (ej: 1, 5, 15)
    - **market_hours_start**: Hora de inicio del mercado (formato: "HH:MM", ej: "09:00")
    - **market_hours_end**: Hora de fin del mercado (formato: "HH:MM", ej: "16:00")
    - **symbols**: Lista de símbolos a actualizar (ej: ["ES", "NQ", "YM"])
    - **timeframes**: Lista de timeframes a extraer (ej: ["1min", "5min"])
    """
    try:
        scheduler.update_config(
            update_interval_minutes=config.update_interval_minutes,
            market_hours_start=config.market_hours_start,
            market_hours_end=config.market_hours_end,
            symbols=config.symbols,
            timeframes=config.timeframes
        )
        
        return {
            "status": "success",
            "message": "Configuración actualizada",
            "scheduler_status": scheduler.get_status()
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Error al actualizar configuración",
                "message": str(e)
            }
        )


@router.post("/run-now")
async def run_scheduler_now(scheduler: DataScheduler = Depends(get_scheduler)):
    """
    Ejecutar el scheduler manualmente ahora (sin esperar al próximo intervalo)
    Útil para pruebas o ejecuciones inmediatas
    """
    try:
        scheduler._update_market_data()
        return {
            "status": "success",
            "message": "Actualización ejecutada manualmente",
            "scheduler_status": scheduler.get_status()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Error al ejecutar actualización",
                "message": str(e)
            }
        )

