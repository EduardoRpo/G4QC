"""
G4QC Trading Platform - FastAPI Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import SessionLocal
from app.api.v1.endpoints import data, scheduler

app = FastAPI(
    title="G4QC Trading Platform API",
    description="API para plataforma de trading automatizado",
    version="0.1.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(data.router, prefix="/api/v1/data", tags=["data"])
app.include_router(scheduler.router, prefix="/api/v1/scheduler", tags=["scheduler"])

# Inicializar scheduler al arrancar la aplicación
@app.on_event("startup")
async def startup_event():
    """Inicializar scheduler si está habilitado en la configuración"""
    db = SessionLocal()
    try:
        from app.services.scheduler.data_scheduler import DataScheduler
        scheduler_instance = DataScheduler(db)
        
        # Si está habilitado, activar automáticamente
        if scheduler_instance.is_enabled():
            scheduler_instance.enable()
            print("✅ Scheduler iniciado y activado")
        else:
            print("ℹ️  Scheduler iniciado pero desactivado (activar desde API)")
        
        # Guardar instancia global para los endpoints
        scheduler.set_scheduler_instance(scheduler_instance)
    except Exception as e:
        print(f"⚠️  Error al inicializar scheduler: {e}")
    finally:
        db.close()


@app.on_event("shutdown")
async def shutdown_event():
    """Cerrar scheduler al apagar la aplicación"""
    if hasattr(scheduler, '_scheduler_instance') and scheduler._scheduler_instance:
        scheduler._scheduler_instance.shutdown()
        print("✅ Scheduler cerrado")


@app.get("/")
async def root():
    return {
        "message": "G4QC Trading Platform API",
        "version": "0.1.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

