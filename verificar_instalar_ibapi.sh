#!/bin/bash
# Script para verificar e instalar ibapi correctamente

echo "============================================================"
echo "🔍 Verificando instalación de ibapi"
echo "============================================================"
echo ""

# Verificar si está instalado
echo "1. Verificando si ibapi está instalado..."
docker compose exec -T backend python -c "import ibapi; print('✅ ibapi está instalado')" 2>/dev/null || {
    echo "❌ ibapi NO está instalado. Instalando..."
    
    echo ""
    echo "2. Instalando ibapi..."
    docker compose exec -T backend pip install ibapi
    
    echo ""
    echo "3. Verificando instalación..."
    docker compose exec -T backend python -c "import ibapi; print('✅ ibapi instalado correctamente')"
}

echo ""
echo "4. Reiniciando backend para que recargue los módulos..."
docker compose restart backend

echo ""
echo "============================================================"
echo "✅ Proceso completado"
echo "============================================================"
echo ""
echo "Espera 10 segundos para que el backend reinicie..."
sleep 10

echo ""
echo "5. Verificando que el backend esté corriendo..."
docker compose ps backend

echo ""
echo "📝 Ahora puedes probar el endpoint nuevamente"

