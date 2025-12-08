#!/bin/bash
# Script para ver los datos guardados en la base de datos

echo "============================================================"
echo "📊 Datos en la Base de Datos"
echo "============================================================"
echo ""

# Resumen general
echo "1️⃣ Resumen General:"
echo "-------------------"
docker compose exec -T postgres psql -U g4qc -d g4qc_db << 'EOF'
SELECT 
    'Total registros: ' || COUNT(*)::text as info
FROM market_data;

SELECT 
    'Símbolos: ' || STRING_AGG(DISTINCT symbol, ', ') as info
FROM market_data;

SELECT 
    'Timeframes: ' || STRING_AGG(DISTINCT timeframe, ', ') as info
FROM market_data;
EOF

echo ""
echo "2️⃣ Detalles por Símbolo:"
echo "------------------------"
docker compose exec -T postgres psql -U g4qc -d g4qc_db << 'EOF'
SELECT 
    symbol,
    timeframe,
    COUNT(*) as registros,
    TO_CHAR(MIN(timestamp), 'YYYY-MM-DD HH24:MI:SS') as primera_fecha,
    TO_CHAR(MAX(timestamp), 'YYYY-MM-DD HH24:MI:SS') as ultima_fecha
FROM market_data
GROUP BY symbol, timeframe
ORDER BY symbol, timeframe;
EOF

echo ""
echo "3️⃣ Últimos 10 Registros:"
echo "------------------------"
docker compose exec -T postgres psql -U g4qc -d g4qc_db << 'EOF'
SELECT 
    TO_CHAR(timestamp, 'YYYY-MM-DD HH24:MI:SS') as fecha,
    open,
    high,
    low,
    close,
    volume
FROM market_data
ORDER BY timestamp DESC
LIMIT 10;
EOF

echo ""
echo "============================================================"
echo "✅ Para consultas más complejas, usa SQL directamente:"
echo "   docker compose exec postgres psql -U g4qc -d g4qc_db"
echo "============================================================"

