#!/bin/bash
# Script para resolver el conflicto de git pull

echo "🔍 Verificando estado de git..."
git status

echo ""
echo "📦 Eliminando archivos __pycache__ del índice de git..."
git rm -r --cached backend/app/__pycache__/ 2>/dev/null || true
git rm -r --cached backend/app/api/v1/endpoints/__pycache__/ 2>/dev/null || true
git rm -r --cached backend/app/models/__pycache__/ 2>/dev/null || true
git rm -r --cached backend/app/services/data_extraction/__pycache__/ 2>/dev/null || true

echo ""
echo "💾 Guardando cambios de docker-compose.yml temporalmente..."
git stash push -m "Cambios locales en docker-compose.yml antes de pull" docker-compose.yml

echo ""
echo "🔄 Haciendo pull desde origin/main..."
git pull origin main

echo ""
echo "📥 Recuperando cambios de docker-compose.yml..."
git stash pop

echo ""
echo "✅ Verificando estado final..."
git status

echo ""
echo "🎉 ¡Proceso completado!"
echo "Si hay conflictos en docker-compose.yml, resuélvelos manualmente."

