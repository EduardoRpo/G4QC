"""
Configuration settings for G4QC Trading Platform
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # App
    APP_NAME: str = "G4QC Trading Platform"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://g4qc:g4qc_dev@localhost:5432/g4qc_db"
    )
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # CORS - Permitir todos los orígenes en desarrollo
    # En producción, especificar solo los orígenes permitidos
    _cors_origins_env = os.getenv("CORS_ORIGINS", "")
    CORS_ORIGINS: List[str] = (
        _cors_origins_env.split(",") if _cors_origins_env 
        else [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "http://45.137.192.196:5173",
            "*"  # Permitir todos en desarrollo
        ]
    )
    
    # Interactive Brokers
    IB_HOST: str = os.getenv("IB_HOST", "127.0.0.1")
    IB_PORT: int = int(os.getenv("IB_PORT", "7497"))
    IB_CLIENT_ID: int = int(os.getenv("IB_CLIENT_ID", "1"))
    
    # MetaTrader 5
    MT5_PATH: str = os.getenv("MT5_PATH", "")
    MT5_LOGIN: int = int(os.getenv("MT5_LOGIN", "0"))
    MT5_PASSWORD: str = os.getenv("MT5_PASSWORD", "")
    MT5_SERVER: str = os.getenv("MT5_SERVER", "")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

