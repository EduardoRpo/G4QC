#!/bin/bash
# Script para verificar y corregir la conexión a la base de datos

echo "=========================================="
echo "VERIFICACIÓN DE BASE DE DATOS"
echo "=========================================="
echo ""

# 1. Verificar que la base de datos existe
echo "1. Verificando bases de datos disponibles..."
docker compose exec postgres psql -U g4qc -l
echo ""

# 2. Verificar que podemos conectarnos a g4qc_db
echo "2. Verificando conexión a g4qc_db..."
docker compose exec postgres psql -U g4qc -d g4qc_db -c "SELECT version();" || echo "❌ No se pudo conectar"
echo ""

# 3. Verificar qué DATABASE_URL está usando el backend
echo "3. Verificando DATABASE_URL en el contenedor backend..."
docker compose exec backend env | grep DATABASE_URL
echo ""

# 4. Verificar logs del backend para ver errores de conexión
echo "4. Últimos logs del backend (buscando errores de DB)..."
docker compose logs backend | grep -i "database\|error\|fatal" | tail -10
echo ""

# 5. Aplicar migraciones
echo "5. Aplicando migraciones..."
docker compose exec backend alembic upgrade head
echo ""

# 6. Verificar que la API funciona
echo "6. Verificando API..."
curl -s http://localhost:8000/health || echo "❌ API no responde"
echo ""

echo "=========================================="
echo "VERIFICACIÓN COMPLETA"
echo "=========================================="

