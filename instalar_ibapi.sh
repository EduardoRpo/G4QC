#!/bin/bash
# Script para instalar ibapi en el contenedor del backend

echo "============================================================"
echo "📦 Instalando ibapi en el contenedor del backend"
echo "============================================================"
echo ""

# Instalar ibapi directamente en el contenedor
echo "Instalando ibapi..."
docker compose exec -T backend pip install ibapi

echo ""
echo "============================================================"
echo "✅ Instalación completada"
echo "============================================================"
echo ""
echo "Verificando instalación..."
docker compose exec -T backend python -c "import ibapi; print(f'✅ ibapi instalado: versión {ibapi.__version__ if hasattr(ibapi, \"__version__\") else \"OK\"}')"

echo ""
echo "📝 Nota: Para que esta instalación persista en futuras reconstrucciones,"
echo "   ya está agregado en backend/requirements.txt"

