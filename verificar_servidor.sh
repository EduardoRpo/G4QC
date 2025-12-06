#!/bin/bash

echo "=========================================="
echo "VERIFICACIÓN DE CONFIGURACIÓN DEL SERVIDOR"
echo "=========================================="
echo ""

echo "1. INFORMACIÓN DEL SISTEMA"
echo "---------------------------"
uname -a
echo ""
lsb_release -a 2>/dev/null || cat /etc/os-release
echo ""

echo "2. VERIFICACIÓN DE DOCKER"
echo "---------------------------"
echo "Docker version:"
docker --version 2>/dev/null || echo "Docker NO está instalado"
echo ""

echo "Docker Compose (método moderno):"
docker compose version 2>/dev/null || echo "Docker Compose plugin NO está disponible"
echo ""

echo "Docker Compose (método clásico):"
docker-compose --version 2>/dev/null || echo "docker-compose NO está instalado"
echo ""

echo "Estado del servicio Docker:"
systemctl status docker --no-pager -l 2>/dev/null || service docker status 2>/dev/null || echo "No se pudo verificar el servicio Docker"
echo ""

echo "3. VERIFICACIÓN DEL PROYECTO G4QC"
echo "-----------------------------------"
if [ -d "/opt/proyectos/G4QC" ]; then
    echo "✓ Directorio del proyecto encontrado"
    cd /opt/proyectos/G4QC
    echo ""
    echo "Contenido del directorio:"
    ls -la
    echo ""
    
    if [ -f "docker-compose.yml" ]; then
        echo "✓ docker-compose.yml encontrado"
        echo ""
        echo "Contenido de docker-compose.yml:"
        cat docker-compose.yml
        echo ""
    else
        echo "✗ docker-compose.yml NO encontrado"
    fi
    
    if [ -d "backend" ]; then
        echo "✓ Directorio backend encontrado"
        echo ""
        echo "Estructura del backend:"
        find backend -maxdepth 2 -type f -name "*.py" -o -name "*.txt" -o -name "*.env*" | head -20
        echo ""
        
        if [ -f "backend/.env" ]; then
            echo "✓ Archivo .env encontrado (mostrando solo nombres de variables):"
            grep -E "^[A-Z_]+=" backend/.env | cut -d'=' -f1 || echo "No se encontraron variables de entorno"
        elif [ -f "backend/.env.example" ]; then
            echo "ℹ Archivo .env.example encontrado (pero no .env):"
            cat backend/.env.example
        else
            echo "✗ No se encontró .env ni .env.example"
        fi
    else
        echo "✗ Directorio backend NO encontrado"
    fi
else
    echo "✗ Directorio /opt/proyectos/G4QC NO encontrado"
    echo ""
    echo "Buscando el proyecto en otras ubicaciones:"
    find / -name "G4QC" -type d 2>/dev/null | head -5
fi
echo ""

echo "4. VERIFICACIÓN DE PUERTOS"
echo "---------------------------"
echo "Puertos en uso (5432, 6379, 8000):"
netstat -tulpn 2>/dev/null | grep -E ":(5432|6379|8000)" || ss -tulpn 2>/dev/null | grep -E ":(5432|6379|8000)" || echo "No se encontraron puertos relevantes en uso"
echo ""

echo "5. VERIFICACIÓN DE CONTENEDORES DOCKER"
echo "----------------------------------------"
echo "Contenedores en ejecución:"
docker ps -a 2>/dev/null || echo "No se pueden listar contenedores (Docker no disponible o sin permisos)"
echo ""

echo "6. VERIFICACIÓN DE RED Y CONECTIVIDAD"
echo "--------------------------------------"
echo "Dirección IP del servidor:"
hostname -I || ip addr show | grep "inet " | grep -v 127.0.0.1
echo ""

echo "7. ESPACIO EN DISCO"
echo "--------------------"
df -h
echo ""

echo "8. MEMORIA DISPONIBLE"
echo "---------------------"
free -h
echo ""

echo "=========================================="
echo "FIN DE LA VERIFICACIÓN"
echo "=========================================="

