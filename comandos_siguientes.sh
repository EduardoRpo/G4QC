#!/bin/bash
# Script con los comandos siguientes después de la instalación

echo "=========================================="
echo "LEVANTANDO SERVICIOS G4QC"
echo "=========================================="
echo ""

# Paso 1: Ir al directorio
cd /opt/proyectos/G4QC

# Paso 2: Levantar servicios
echo "Levantando servicios con Docker Compose..."
docker compose up -d

echo ""
echo "Esperando a que los servicios inicien..."
sleep 10

# Paso 3: Verificar estado
echo ""
echo "Estado de los servicios:"
docker compose ps

# Paso 4: Verificar PostgreSQL
echo ""
echo "Verificando PostgreSQL..."
sleep 5
docker compose exec postgres pg_isready -U g4qc || echo "PostgreSQL aún iniciando..."

# Paso 5: Aplicar migraciones
echo ""
echo "Aplicando migraciones de base de datos..."
sleep 5
docker compose exec backend alembic upgrade head

# Paso 6: Verificar API
echo ""
echo "Verificando API..."
sleep 5
curl http://localhost:8000/health || echo "API aún iniciando..."

echo ""
echo "=========================================="
echo "VERIFICACIÓN COMPLETA"
echo "=========================================="
echo ""
echo "Para ver los logs:"
echo "  docker compose logs -f"
echo ""
echo "Para ver el estado:"
echo "  docker compose ps"
echo ""
echo "Acceder a la API:"
echo "  http://45.137.192.196:8000"
echo "  http://45.137.192.196:8000/docs"
echo ""

