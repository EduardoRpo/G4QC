#!/bin/bash
# Script para diagnosticar por qué la extracción devuelve 0 registros

echo "🔍 Diagnóstico de Extracción de Datos"
echo "======================================"
echo ""

cd /opt/proyectos/G4QC

echo "1️⃣ Verificando contenedores..."
docker compose ps | grep -E "ibgateway|backend"

echo ""
echo "2️⃣ Verificando logs de IB Gateway..."
docker compose logs ibgateway --tail=20 | grep -i "error\|connection\|login"

echo ""
echo "3️⃣ Verificando logs del backend (últimas extracciones)..."
docker compose logs backend --tail=50 | grep -i "extract\|error\|ib\|connection" | tail -20

echo ""
echo "4️⃣ Probando conexión con IB Gateway..."
docker compose exec backend python -c "
from app.services.data_extraction.ib_extractor import IBDataExtractor
from app.core.config import settings
import sys

print(f'📍 Configuración IB:')
print(f'   Host: {settings.IB_HOST}')
print(f'   Port: {settings.IB_PORT}')
print(f'   Client ID: {settings.IB_CLIENT_ID}')
print('')

try:
    extractor = IBDataExtractor()
    print('🔄 Intentando conectar...')
    extractor.connect()
    print('✅ Conectado exitosamente a IB Gateway')
    extractor.disconnect()
    print('✅ Desconectado correctamente')
except ImportError as e:
    print(f'❌ ibapi no está instalado: {e}')
    sys.exit(1)
except Exception as e:
    print(f'❌ Error de conexión: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

echo ""
echo "5️⃣ Verificando datos en la base de datos..."
docker compose exec postgres psql -U g4qc -d g4qc_db -c "SELECT COUNT(*) as total_registros FROM market_data;"

echo ""
echo "✅ Diagnóstico completado"

