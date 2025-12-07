#!/bin/bash
# Script de verificación de modo Paper Trading
# Verifica que IB Gateway esté configurado para Paper Trading (NO Live Trading)

set -e

echo "============================================================"
echo "🔍 Verificación de Configuración Paper Trading"
echo "============================================================"
echo ""

ERROR_COUNT=0
WARNING_COUNT=0

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mostrar errores
error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
    ((ERROR_COUNT++))
}

# Función para mostrar advertencias
warning() {
    echo -e "${YELLOW}⚠️  ADVERTENCIA: $1${NC}"
    ((WARNING_COUNT++))
}

# Función para mostrar éxito
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# 1. Verificar docker-compose.yml
echo "1️⃣  Verificando docker-compose.yml..."
if [ ! -f "docker-compose.yml" ]; then
    error "No se encuentra docker-compose.yml"
else
    if grep -q "IB_LOGINTYPE=Paper Trading" docker-compose.yml; then
        success "docker-compose.yml tiene IB_LOGINTYPE=Paper Trading configurado"
    else
        if grep -q "IB_LOGINTYPE=Live Trading" docker-compose.yml; then
            error "docker-compose.yml tiene IB_LOGINTYPE=Live Trading (PELIGRO!)"
        else
            warning "No se encontró IB_LOGINTYPE en docker-compose.yml"
        fi
    fi
    
    # Verificar puerto
    if grep -q '"7497:4000"' docker-compose.yml || grep -q "'7497:4000'" docker-compose.yml; then
        success "Puerto 7497 (Paper Trading) configurado en docker-compose.yml"
    else
        if grep -q '"7496:' docker-compose.yml || grep -q "'7496:" docker-compose.yml; then
            error "Puerto 7496 (Live Trading) detectado en docker-compose.yml (PELIGRO!)"
        else
            warning "No se pudo verificar el puerto en docker-compose.yml"
        fi
    fi
fi

echo ""

# 2. Verificar puertos en uso
echo "2️⃣  Verificando puertos en uso..."
if ss -tulpn 2>/dev/null | grep -q ":7497"; then
    success "Puerto 7497 (Paper Trading) está en uso"
else
    warning "Puerto 7497 (Paper Trading) NO está en uso"
fi

if ss -tulpn 2>/dev/null | grep -q ":7496"; then
    error "Puerto 7496 (Live Trading) está en uso (PELIGRO!)"
else
    success "Puerto 7496 (Live Trading) NO está en uso"
fi

echo ""

# 3. Verificar logs de IB Gateway
echo "3️⃣  Verificando logs de IB Gateway..."
if docker compose ps | grep -q "ibgateway.*Up"; then
    success "IB Gateway está corriendo"
    
    # Verificar logs para Paper Trading
    if docker compose logs ibgateway 2>/dev/null | grep -qi "paper trading"; then
        success "Logs muestran 'Paper Trading'"
    else
        warning "No se encontró 'Paper Trading' en los logs"
    fi
    
    # Verificar que NO esté en Live Trading
    if docker compose logs ibgateway 2>/dev/null | grep -qi "live trading"; then
        error "Logs muestran 'Live Trading' (PELIGRO!)"
    else
        success "Logs NO muestran 'Live Trading'"
    fi
else
    warning "IB Gateway NO está corriendo"
fi

echo ""

# 4. Verificar configuración del backend
echo "4️⃣  Verificando configuración del backend..."
if docker compose ps | grep -q "backend.*Up"; then
    BACKEND_PORT=$(docker compose exec -T backend python -c "from app.core.config import settings; print(settings.IB_PORT)" 2>/dev/null || echo "")
    if [ "$BACKEND_PORT" = "4000" ] || [ "$BACKEND_PORT" = "7497" ]; then
        success "Backend configurado para puerto correcto (4000/7497 = Paper Trading)"
    else
        if [ "$BACKEND_PORT" = "7496" ]; then
            error "Backend configurado para puerto 7496 (Live Trading - PELIGRO!)"
        else
            warning "No se pudo verificar el puerto del backend (puerto actual: $BACKEND_PORT)"
        fi
    fi
else
    warning "Backend NO está corriendo"
fi

echo ""
echo "============================================================"
echo "📊 Resumen"
echo "============================================================"

if [ $ERROR_COUNT -eq 0 ] && [ $WARNING_COUNT -eq 0 ]; then
    echo -e "${GREEN}✅ Todo está configurado correctamente para Paper Trading${NC}"
    exit 0
elif [ $ERROR_COUNT -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Hay $WARNING_COUNT advertencia(s), pero no hay errores críticos${NC}"
    exit 0
else
    echo -e "${RED}❌ Se encontraron $ERROR_COUNT error(es) y $WARNING_COUNT advertencia(s)${NC}"
    echo ""
    echo "⚠️  ACCIÓN REQUERIDA:"
    echo "   - Revisa los errores arriba"
    echo "   - Asegúrate de que docker-compose.yml tenga IB_LOGINTYPE=Paper Trading"
    echo "   - Verifica que el puerto sea 7497 (Paper), NO 7496 (Live)"
    exit 1
fi

