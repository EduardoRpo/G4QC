#!/bin/bash
# Script para ver los logs del backend y diagnosticar el error 500

echo "============================================================"
echo "🔍 Ver logs del backend (últimas 50 líneas)"
echo "============================================================"
echo ""

docker compose logs backend --tail 50

echo ""
echo "============================================================"
echo "🔍 Buscando errores específicos"
echo "============================================================"
echo ""

docker compose logs backend --tail 100 | grep -i -E "(error|exception|traceback|failed|500)"

echo ""
echo "============================================================"
echo "📝 Para ver logs en tiempo real:"
echo "   docker compose logs -f backend"
echo "============================================================"

