"""
Data Scheduler Service - Actualización automática de datos de mercado
Usa APScheduler para programar tareas periódicas
"""
import logging
from datetime import datetime, time as dt_time
from typing import List, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
import pytz

from app.services.data_extraction.ib_extractor import IBDataExtractor
from app.services.data_extraction.data_processor import DataProcessor
from app.models.scheduler import SchedulerConfig
from app.core.config import settings

logger = logging.getLogger(__name__)


class DataScheduler:
    """
    Servicio para programar actualizaciones automáticas de datos de mercado
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.scheduler = BackgroundScheduler(timezone=pytz.UTC)
        self.scheduler.start()
        self._load_config()
    
    def _load_config(self):
        """Cargar configuración desde la base de datos"""
        config = self.db.query(SchedulerConfig).first()
        if not config:
            # Crear configuración por defecto
            config = SchedulerConfig(
                enabled=False,
                update_interval_minutes=1,
                market_hours_start="09:00",
                market_hours_end="16:00",
                symbols=["ES", "NQ"],
                timeframes=["1min"]
            )
            self.db.add(config)
            self.db.commit()
        
        self.config = config
        logger.info(f"Scheduler configurado: enabled={config.enabled}, symbols={config.symbols}")
    
    def _update_config(self):
        """Recargar configuración desde BD"""
        self.db.refresh(self.config)
    
    def is_enabled(self) -> bool:
        """Verificar si el scheduler está activado"""
        self._update_config()
        return self.config.enabled
    
    def enable(self):
        """Activar el scheduler"""
        if self.is_enabled():
            logger.info("Scheduler ya está activado")
            return
        
        self.config.enabled = True
        self.config.updated_at = datetime.utcnow()
        self.db.commit()
        
        self._schedule_jobs()
        logger.info("✅ Scheduler activado")
    
    def disable(self):
        """Desactivar el scheduler"""
        if not self.is_enabled():
            logger.info("Scheduler ya está desactivado")
            return
        
        self.config.enabled = False
        self.config.updated_at = datetime.utcnow()
        self.db.commit()
        
        self.scheduler.remove_all_jobs()
        logger.info("✅ Scheduler desactivado")
    
    def update_config(
        self,
        update_interval_minutes: Optional[int] = None,
        market_hours_start: Optional[str] = None,
        market_hours_end: Optional[str] = None,
        symbols: Optional[List[str]] = None,
        timeframes: Optional[List[str]] = None
    ):
        """Actualizar configuración del scheduler"""
        if update_interval_minutes is not None:
            self.config.update_interval_minutes = update_interval_minutes
        if market_hours_start is not None:
            self.config.market_hours_start = market_hours_start
        if market_hours_end is not None:
            self.config.market_hours_end = market_hours_end
        if symbols is not None:
            self.config.symbols = symbols
        if timeframes is not None:
            self.config.timeframes = timeframes
        
        self.config.updated_at = datetime.utcnow()
        self.db.commit()
        
        # Re-programar jobs si está activado
        if self.is_enabled():
            self.scheduler.remove_all_jobs()
            self._schedule_jobs()
        
        logger.info("✅ Configuración del scheduler actualizada")
    
    def _schedule_jobs(self):
        """Programar jobs según la configuración"""
        if not self.is_enabled():
            return
        
        self._update_config()
        
        # Programar job con intervalo configurado
        # La verificación de horario de mercado se hace dentro del job
        self.scheduler.add_job(
            self._update_market_data,
            trigger=IntervalTrigger(minutes=self.config.update_interval_minutes),
            id='update_market_data',
            replace_existing=True,
            max_instances=1  # Solo una instancia a la vez
        )
        
        logger.info(
            f"Job programado: cada {self.config.update_interval_minutes} min, "
            f"de {self.config.market_hours_start} a {self.config.market_hours_end}"
        )
    
    def _update_market_data(self):
        """Tarea que se ejecuta periódicamente para actualizar datos"""
        try:
            self._update_config()
            
            if not self.is_enabled():
                logger.info("Scheduler desactivado, cancelando actualización")
                return
            
            # Verificar si estamos en horario de mercado
            now = datetime.now(pytz.UTC)
            start_hour, start_minute = map(int, self.config.market_hours_start.split(':'))
            end_hour, end_minute = map(int, self.config.market_hours_end.split(':'))
            
            current_time = now.time()
            market_start = dt_time(start_hour, start_minute)
            market_end = dt_time(end_hour, end_minute)
            
            # Si no estamos en horario de mercado, omitir
            if current_time < market_start or current_time > market_end:
                logger.debug(f"Fuera de horario de mercado ({current_time}), omitiendo actualización")
                return
            
            logger.info(f"🔄 Iniciando actualización automática de datos...")
            logger.info(f"   Símbolos: {self.config.symbols}")
            logger.info(f"   Timeframes: {self.config.timeframes}")
            
            processor = DataProcessor(self.db)
            extractor = None
            
            for symbol in self.config.symbols:
                for timeframe in self.config.timeframes:
                    try:
                        # Convertir timeframe a formato IB (ej: "1min" -> "1 min")
                        bar_size = timeframe.replace("min", " min").replace("h", " hour").replace("d", " day")
                        
                        extractor = IBDataExtractor()
                        
                        # Extraer solo último día de datos
                        df = extractor.extract_historical_data(
                            symbol=symbol,
                            duration="1 D",
                            bar_size=bar_size,
                            num_blocks=1
                        )
                        
                        if not df.empty:
                            # Guardar con UPSERT (previene duplicados)
                            saved = processor.save_market_data(df, symbol, timeframe)
                            
                            # Si es 1min, actualizar timeframes incrementalmente
                            if timeframe == "1min":
                                processor.update_timeframes_incremental(symbol, "1min")
                            
                            logger.info(f"✅ {symbol} ({timeframe}): {saved} registros nuevos")
                        else:
                            logger.warning(f"⚠️  {symbol} ({timeframe}): No se obtuvieron datos")
                        
                        if extractor:
                            extractor.disconnect()
                            extractor = None
                    
                    except Exception as e:
                        logger.error(f"❌ Error actualizando {symbol} ({timeframe}): {str(e)}")
                        if extractor:
                            try:
                                extractor.disconnect()
                            except:
                                pass
                            extractor = None
                        continue
            
            # Actualizar timestamp de última ejecución
            self.config.last_run = datetime.utcnow()
            self.db.commit()
            
            logger.info("✅ Actualización automática completada")
        
        except Exception as e:
            logger.error(f"❌ Error en actualización automática: {str(e)}")
    
    def get_status(self) -> dict:
        """Obtener estado actual del scheduler"""
        self._update_config()
        
        jobs = self.scheduler.get_jobs()
        next_run = jobs[0].next_run_time if jobs else None
        
        return {
            "enabled": self.config.enabled,
            "update_interval_minutes": self.config.update_interval_minutes,
            "market_hours_start": self.config.market_hours_start,
            "market_hours_end": self.config.market_hours_end,
            "symbols": self.config.symbols,
            "timeframes": self.config.timeframes,
            "last_run": self.config.last_run.isoformat() if self.config.last_run else None,
            "next_run": next_run.isoformat() if next_run else None,
            "jobs_count": len(jobs)
        }
    
    def shutdown(self):
        """Cerrar el scheduler"""
        self.scheduler.shutdown()
        logger.info("Scheduler cerrado")

