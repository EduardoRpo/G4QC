"""
Script para verificar y limpiar datos duplicados en market_data
Ejecutar: python -m app.scripts.clean_duplicates [--dry-run] [--delete]
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy import text
from app.core.database import engine
from app.models.data import MarketData
from sqlalchemy.orm import Session
from app.core.database import SessionLocal


def find_duplicates(db: Session):
    """Encontrar registros duplicados"""
    print("🔍 Buscando duplicados...")
    
    # Query para encontrar duplicados
    query = text("""
        SELECT 
            symbol, 
            timeframe, 
            timestamp, 
            COUNT(*) as count
        FROM market_data
        GROUP BY symbol, timeframe, timestamp
        HAVING COUNT(*) > 1
        ORDER BY count DESC, symbol, timeframe, timestamp
    """)
    
    result = db.execute(query)
    duplicates = result.fetchall()
    
    if not duplicates:
        print("✅ No se encontraron duplicados")
        return []
    
    print(f"\n⚠️  Se encontraron {len(duplicates)} grupos de duplicados:\n")
    
    total_duplicates = 0
    for row in duplicates:
        symbol, timeframe, timestamp, count = row
        extra = count - 1  # Uno es válido, los demás son duplicados
        total_duplicates += extra
        print(f"  {symbol} | {timeframe} | {timestamp} | {count} registros ({extra} duplicados)")
    
    print(f"\n📊 Total de registros duplicados a eliminar: {total_duplicates}")
    return duplicates


def delete_duplicates(db: Session, dry_run: bool = True):
    """Eliminar duplicados, manteniendo solo el registro con menor ID"""
    duplicates = find_duplicates(db)
    
    if not duplicates:
        return 0
    
    if dry_run:
        print("\n🔍 MODO DRY-RUN: No se eliminarán registros")
        print("   Ejecuta con --delete para eliminar realmente")
        return 0
    
    print("\n🗑️  Eliminando duplicados...")
    
    # Query para eliminar duplicados, manteniendo el registro con menor ID
    delete_query = text("""
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
    
    result = db.execute(delete_query)
    deleted_count = result.rowcount
    db.commit()
    
    print(f"✅ Eliminados {deleted_count} registros duplicados")
    return deleted_count


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Verificar y limpiar duplicados en market_data')
    parser.add_argument('--dry-run', action='store_true', help='Solo mostrar, no eliminar')
    parser.add_argument('--delete', action='store_true', help='Eliminar duplicados realmente')
    
    args = parser.parse_args()
    
    db = SessionLocal()
    try:
        if args.delete:
            delete_duplicates(db, dry_run=False)
        else:
            find_duplicates(db)
            if not args.dry_run:
                print("\n💡 Para eliminar duplicados, ejecuta: python -m app.scripts.clean_duplicates --delete")
    finally:
        db.close()


if __name__ == "__main__":
    main()

