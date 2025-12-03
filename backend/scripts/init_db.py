"""
Script para inicializar la base de datos
Ejecutar después de crear los contenedores Docker
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.database import engine, Base
from app.models.data import MarketData


def init_db():
    """Crear todas las tablas"""
    print("🔧 Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente")
    
    # Intentar habilitar TimescaleDB
    from sqlalchemy import text
    with engine.connect() as conn:
        try:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb;"))
            conn.commit()
            print("✅ Extensión TimescaleDB habilitada")
            
            # Verificar si la tabla existe y convertir a hypertable
            result = conn.execute(text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'market_data')"
            ))
            if result.scalar():
                try:
                    conn.execute(text(
                        "SELECT create_hypertable('market_data', 'timestamp', "
                        "chunk_time_interval => INTERVAL '1 day');"
                    ))
                    conn.commit()
                    print("✅ Tabla market_data convertida a hypertable")
                except Exception as e:
                    print(f"⚠️ No se pudo convertir a hypertable: {e}")
        except Exception as e:
            print(f"⚠️ TimescaleDB no disponible: {e}")
            print("ℹ️ La base de datos funcionará como PostgreSQL normal")


if __name__ == "__main__":
    init_db()

