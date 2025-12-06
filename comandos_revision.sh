#!/bin/bash
# Script para ejecutar comandos de revisión en el servidor
# Uso: ./comandos_revision.sh

SERVER="45.137.192.196"
USER="root"
PASSWORD="G4QC2026"

echo "Conectándose al servidor $SERVER..."
echo ""

# Crear un script temporal en el servidor
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no $USER@$SERVER << 'EOF'

echo "=========================================="
echo "INFORMACIÓN DEL SISTEMA"
echo "=========================================="
uname -a
echo ""

echo "=========================================="
echo "VERIFICACIÓN DE DOCKER"
echo "=========================================="
docker --version 2>/dev/null || echo "Docker NO instalado"
docker compose version 2>/dev/null || echo "Docker Compose plugin NO disponible"
docker-compose --version 2>/dev/null || echo "docker-compose NO instalado"
echo ""

echo "=========================================="
echo "CONTENIDO DEL PROYECTO"
echo "=========================================="
cd /opt/proyectos/G4QC 2>/dev/null && pwd || echo "Directorio no encontrado"
ls -la 2>/dev/null || echo "No se puede listar contenido"
echo ""

echo "=========================================="
echo "CONFIGURACIÓN DOCKER-COMPOSE"
echo "=========================================="
cat docker-compose.yml 2>/dev/null || echo "docker-compose.yml no encontrado"
echo ""

echo "=========================================="
echo "ESTRUCTURA BACKEND"
echo "=========================================="
ls -la backend/ 2>/dev/null || echo "Directorio backend no encontrado"
echo ""

echo "=========================================="
echo "ARCHIVOS DE CONFIGURACIÓN"
echo "=========================================="
ls -la backend/.env* 2>/dev/null || echo "No se encontraron archivos .env"
echo ""

echo "=========================================="
echo "CONTENEDORES DOCKER"
echo "=========================================="
docker ps -a 2>/dev/null || echo "No se pueden listar contenedores"
echo ""

echo "=========================================="
echo "PUERTOS EN USO"
echo "=========================================="
netstat -tulpn 2>/dev/null | grep -E ":(5432|6379|8000)" || ss -tulpn 2>/dev/null | grep -E ":(5432|6379|8000)" || echo "Puertos no encontrados"
echo ""

EOF

echo ""
echo "Revisión completada"

