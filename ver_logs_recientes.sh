#!/bin/bash
# Script para ver los logs más recientes del backend

echo "============================================================"
echo "🔍 Últimos logs del backend (últimas 100 líneas)"
echo "============================================================"
echo ""

docker compose logs backend --tail 100

echo ""
echo "============================================================"
echo "🔍 Buscando errores específicos"
echo "============================================================"
echo ""

docker compose logs backend --tail 200 | grep -i -A 10 -B 5 "error\|exception\|traceback\|321\|extrayendo\|timeout"

echo ""
echo "============================================================"
echo "📝 Para ver logs en tiempo real:"
echo "   docker compose logs -f backend"
echo "============================================================"

