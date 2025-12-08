#!/bin/bash
# Script para verificar la arquitectura del servidor

echo "Verificando arquitectura del servidor..."
echo ""

# Método 1: uname
echo "Arquitectura (uname -m):"
uname -m
echo ""

# Método 2: dpkg
if command -v dpkg &> /dev/null; then
    echo "Arquitectura (dpkg):"
    dpkg --print-architecture
    echo ""
fi

# Método 3: arch
if command -v arch &> /dev/null; then
    echo "Arquitectura (arch):"
    arch
    echo ""
fi

# Interpretación
ARCH=$(uname -m)
echo "=========================================="
echo "RECOMENDACIÓN:"
echo "=========================================="

if [[ "$ARCH" == "x86_64" ]]; then
    echo "✅ Tu servidor es X86_64"
    echo "📥 Descarga: Linux (X86_64)"
elif [[ "$ARCH" == "aarch64" ]] || [[ "$ARCH" == "arm64" ]]; then
    echo "✅ Tu servidor es ARM64"
    echo "📥 Descarga: Linux (ARM64)"
else
    echo "⚠️  Arquitectura detectada: $ARCH"
    echo "Por favor verifica manualmente"
fi

echo "=========================================="

