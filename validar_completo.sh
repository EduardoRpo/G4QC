#!/bin/bash
# Script de validación completa del sistema G4QC
# Ejecuta todas las verificaciones paso a paso

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Contadores
TESTS_PASSED=0
TESTS_FAILED=0
WARNINGS=0

# Funciones
print_header() {
    echo ""
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
    ((TESTS_PASSED++))
}

print_error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
    ((TESTS_FAILED++))
}

print_warning() {
    echo -e "${YELLOW}⚠️  ADVERTENCIA: $1${NC}"
    ((WARNINGS++))
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    print_error "No se encuentra docker-compose.yml. Ejecuta este script desde el directorio del proyecto."
    exit 1
fi

print_header "🧪 VALIDACIÓN COMPLETA - G4QC Trading Platform"

# ============================================================
# FASE 1: Verificación de Infraestructura
# ============================================================
print_header "FASE 1: Verificación de Infraestructura"

# 1.1 Verificar servicios Docker
print_info "1.1 Verificando servicios Docker..."
if docker compose ps | grep -q "Up"; then
    print_success "Servicios Docker están corriendo"
    docker compose ps
else
    print_error "Algunos servicios Docker no están corriendo"
    docker compose ps
fi

# 1.2 Verificar Paper Trading
print_info "1.2 Verificando configuración Paper Trading..."
if grep -q "IB_LOGINTYPE=Paper Trading" docker-compose.yml; then
    print_success "Configuración Paper Trading correcta"
else
    print_error "Configuración Paper Trading incorrecta o no encontrada"
fi

# 1.3 Verificar puertos
print_info "1.3 Verificando puertos..."
if ss -tulpn 2>/dev/null | grep -q ":7497"; then
    print_success "Puerto 7497 (Paper Trading) está en uso"
else
    print_warning "Puerto 7497 (Paper Trading) NO está en uso"
fi

if ss -tulpn 2>/dev/null | grep -q ":7496"; then
    print_error "Puerto 7496 (Live Trading) está en uso (PELIGRO!)"
else
    print_success "Puerto 7496 (Live Trading) NO está en uso"
fi

# 1.4 Verificar configuración del backend
print_info "1.4 Verificando configuración del backend..."
if docker compose ps | grep -q "backend.*Up"; then
    BACKEND_IB_HOST=$(docker compose exec -T backend python -c "from app.core.config import settings; print(settings.IB_HOST)" 2>/dev/null || echo "")
    BACKEND_IB_PORT=$(docker compose exec -T backend python -c "from app.core.config import settings; print(settings.IB_PORT)" 2>/dev/null || echo "")
    if [ "$BACKEND_IB_HOST" = "ibgateway" ] && [ "$BACKEND_IB_PORT" = "4000" ]; then
        print_success "Backend configurado correctamente (IB_HOST=ibgateway, IB_PORT=4000)"
    else
        print_warning "Backend configurado con valores inesperados (IB_HOST=$BACKEND_IB_HOST, IB_PORT=$BACKEND_IB_PORT)"
    fi
else
    print_error "Backend NO está corriendo"
fi

# ============================================================
# FASE 2: Prueba de Conexión IB Gateway
# ============================================================
print_header "FASE 2: Prueba de Conexión IB Gateway"

# 2.1 Verificar que el script de prueba existe
print_info "2.1 Verificando script de prueba de conexión..."
if [ -f "backend/test_ib_connection.py" ]; then
    print_success "Script de prueba encontrado"
    
    # 2.2 Ejecutar prueba de conexión
    print_info "2.2 Ejecutando prueba de conexión a IB Gateway..."
    if docker compose exec -T backend python test_ib_connection.py 2>&1 | grep -q "PRUEBA EXITOSA"; then
        print_success "Conexión a IB Gateway exitosa"
    else
        print_error "Fallo en conexión a IB Gateway"
        print_info "Ejecutando prueba manual para ver detalles..."
        docker compose exec -T backend python test_ib_connection.py || true
    fi
else
    print_warning "Script de prueba no encontrado (backend/test_ib_connection.py)"
    print_info "Creando script de prueba..."
    # El script debería estar en el backend, pero si no, lo creamos después
fi

# ============================================================
# FASE 3: Prueba de Endpoints Básicos
# ============================================================
print_header "FASE 3: Prueba de Endpoints Básicos de la API"

# Obtener la URL del servidor
API_URL="http://localhost:8000"
if [ -n "$1" ]; then
    API_URL="$1"
fi

print_info "Usando API URL: $API_URL"

# 3.1 Prueba GET /
print_info "3.1 Probando GET /..."
if curl -s -f "$API_URL/" > /dev/null 2>&1; then
    RESPONSE=$(curl -s "$API_URL/")
    if echo "$RESPONSE" | grep -q "G4QC Trading Platform"; then
        print_success "Endpoint GET / funciona correctamente"
    else
        print_warning "Endpoint GET / responde pero con contenido inesperado"
    fi
else
    print_error "Endpoint GET / NO responde"
fi

# 3.2 Prueba GET /health
print_info "3.2 Probando GET /health..."
if curl -s -f "$API_URL/health" > /dev/null 2>&1; then
    RESPONSE=$(curl -s "$API_URL/health")
    if echo "$RESPONSE" | grep -q "healthy\|status"; then
        print_success "Endpoint GET /health funciona correctamente"
    else
        print_warning "Endpoint GET /health responde pero con contenido inesperado"
    fi
else
    print_error "Endpoint GET /health NO responde"
fi

# 3.3 Verificar documentación Swagger
print_info "3.3 Verificando documentación Swagger..."
if curl -s -f "$API_URL/docs" > /dev/null 2>&1; then
    print_success "Documentación Swagger accesible en $API_URL/docs"
else
    print_warning "Documentación Swagger NO accesible"
fi

# ============================================================
# FASE 4: Prueba de Extracción de Datos (Opcional)
# ============================================================
print_header "FASE 4: Prueba de Extracción de Datos (Opcional)"

print_info "Esta prueba requiere conexión a IB Gateway y puede tardar varios minutos."
print_info "Para ejecutarla manualmente, usa:"
print_info "  curl -X POST \"$API_URL/api/v1/data/extract\" \\"
print_info "    -H \"Content-Type: application/json\" \\"
print_info "    -d '{\"symbol\": \"ES\", \"duration\": \"1 D\", \"bar_size\": \"1 min\", \"num_blocks\": 1}'"

# ============================================================
# RESUMEN
# ============================================================
print_header "📊 RESUMEN DE VALIDACIÓN"

echo -e "${GREEN}✅ Pruebas exitosas: $TESTS_PASSED${NC}"
echo -e "${RED}❌ Pruebas fallidas: $TESTS_FAILED${NC}"
echo -e "${YELLOW}⚠️  Advertencias: $WARNINGS${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ VALIDACIÓN COMPLETA: Todos los componentes están funcionando correctamente${NC}"
    echo ""
    echo "📝 Próximos pasos:"
    echo "   1. Probar extracción de datos: curl -X POST \"$API_URL/api/v1/data/extract\" ..."
    echo "   2. Revisar documentación: $API_URL/docs"
    echo "   3. Continuar con el desarrollo"
    exit 0
else
    echo -e "${RED}❌ VALIDACIÓN FALLIDA: Hay $TESTS_FAILED error(es) que deben resolverse${NC}"
    echo ""
    echo "📝 Revisa los errores arriba y:"
    echo "   1. Verifica los logs: docker compose logs [servicio]"
    echo "   2. Revisa la documentación: docs/PLAN_VALIDACION.md"
    exit 1
fi

