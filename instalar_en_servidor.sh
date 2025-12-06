#!/bin/bash

# Script de instalación completa para el servidor G4QC
# Ejecutar como root en el servidor: bash instalar_en_servidor.sh

set -e  # Salir si hay algún error

# Configurar modo no interactivo para evitar diálogos
export DEBIAN_FRONTEND=noninteractive
export DEBIAN_PRIORITY=critical

echo "=========================================="
echo "INSTALACIÓN G4QC - SERVIDOR"
echo "=========================================="
echo ""

# Verificar que estamos como root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Por favor ejecuta este script como root"
    exit 1
fi

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ No se encontró docker-compose.yml"
    echo "Por favor ejecuta este script desde /opt/proyectos/G4QC"
    exit 1
fi

echo "✓ Directorio correcto detectado"
echo ""

# Paso 1: Instalar Docker
echo "=========================================="
echo "PASO 1: Instalando Docker"
echo "=========================================="

if command -v docker &> /dev/null; then
    echo "✓ Docker ya está instalado"
    docker --version
else
    echo "Instalando Docker..."
    
    # Actualizar paquetes (modo no interactivo)
    apt update -y
    
    # Instalar dependencias (modo no interactivo)
    apt install -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" ca-certificates curl gnupg lsb-release
    
    # Agregar clave GPG oficial de Docker
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # Configurar repositorio
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Instalar Docker Engine (modo no interactivo)
    apt update -y
    apt install -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # Iniciar y habilitar Docker
    systemctl start docker
    systemctl enable docker
    
    echo "✓ Docker instalado correctamente"
    docker --version
fi

echo ""

# Paso 2: Verificar Docker Compose
echo "=========================================="
echo "PASO 2: Verificando Docker Compose"
echo "=========================================="

if docker compose version &> /dev/null; then
    echo "✓ Docker Compose plugin está disponible"
    docker compose version
elif command -v docker-compose &> /dev/null; then
    echo "✓ docker-compose está instalado"
    docker-compose --version
else
    echo "Instalando docker-compose standalone..."
    
    # Descargar docker-compose
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    
    echo "✓ docker-compose instalado correctamente"
    docker-compose --version
fi

echo ""

# Paso 3: Crear archivo .env si no existe
echo "=========================================="
echo "PASO 3: Configurando archivo .env"
echo "=========================================="

if [ -f "backend/.env" ]; then
    echo "✓ El archivo backend/.env ya existe"
else
    if [ -f "backend/.env.example" ]; then
        echo "Copiando .env.example a .env..."
        cp backend/.env.example backend/.env
        echo "✓ Archivo .env creado desde .env.example"
        echo "⚠️  IMPORTANTE: Revisa y edita backend/.env con tus configuraciones"
    elif [ -f "backend/env.example" ]; then
        echo "Copiando env.example a .env..."
        cp backend/env.example backend/.env
        echo "✓ Archivo .env creado desde env.example"
        echo "⚠️  IMPORTANTE: Revisa y edita backend/.env con tus configuraciones"
    else
        echo "⚠️  No se encontró .env.example, creando .env básico..."
        cat > backend/.env << EOF
# Configuración G4QC
DEBUG=False

# Base de Datos (usando valores de docker-compose.yml)
DATABASE_URL=postgresql://g4qc:g4qc_dev@postgres:5432/g4qc_db

# Redis
REDIS_URL=redis://redis:6379

# Interactive Brokers
IB_HOST=127.0.0.1
IB_PORT=7497
IB_CLIENT_ID=1

# MetaTrader 5 (opcional)
MT5_PATH=
MT5_LOGIN=0
MT5_PASSWORD=
MT5_SERVER=
EOF
        echo "✓ Archivo .env básico creado"
        echo "⚠️  IMPORTANTE: Revisa y edita backend/.env con tus configuraciones"
    fi
fi

echo ""

# Paso 4: Verificar estructura del proyecto
echo "=========================================="
echo "PASO 4: Verificando estructura del proyecto"
echo "=========================================="

echo "Verificando archivos necesarios..."

if [ ! -f "docker-compose.yml" ]; then
    echo "❌ ERROR: docker-compose.yml no encontrado"
    exit 1
fi
echo "✓ docker-compose.yml encontrado"

if [ ! -d "backend" ]; then
    echo "❌ ERROR: directorio backend no encontrado"
    exit 1
fi
echo "✓ directorio backend encontrado"

if [ ! -f "backend/Dockerfile" ]; then
    echo "❌ ERROR: backend/Dockerfile no encontrado"
    exit 1
fi
echo "✓ backend/Dockerfile encontrado"

if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ ERROR: backend/requirements.txt no encontrado"
    exit 1
fi
echo "✓ backend/requirements.txt encontrado"

echo ""

# Paso 5: Mostrar resumen
echo "=========================================="
echo "INSTALACIÓN COMPLETADA"
echo "=========================================="
echo ""
echo "✓ Docker instalado y funcionando"
echo "✓ Docker Compose disponible"
echo "✓ Archivo .env configurado"
echo "✓ Estructura del proyecto verificada"
echo ""
echo "=========================================="
echo "PRÓXIMOS PASOS"
echo "=========================================="
echo ""
echo "1. Revisar y editar el archivo .env si es necesario:"
echo "   nano backend/.env"
echo ""
echo "2. Levantar los servicios con Docker Compose:"
echo "   docker compose up -d"
echo ""
echo "3. Ver los logs de los servicios:"
echo "   docker compose logs -f"
echo ""
echo "4. Verificar que los servicios estén corriendo:"
echo "   docker compose ps"
echo ""
echo "5. Aplicar migraciones de base de datos:"
echo "   docker compose exec backend alembic upgrade head"
echo ""
echo "6. Acceder a la API:"
echo "   http://tu-servidor:8000"
echo "   Documentación: http://tu-servidor:8000/docs"
echo ""
echo "=========================================="

