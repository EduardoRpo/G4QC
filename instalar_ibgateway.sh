#!/bin/bash

# Script de instalación automática de IB Gateway en Linux
# Ejecutar como root: bash instalar_ibgateway.sh

set -e

echo "=========================================="
echo "INSTALACIÓN DE IB GATEWAY"
echo "=========================================="
echo ""

# Verificar que estamos como root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Por favor ejecuta este script como root"
    exit 1
fi

# Variables
IB_GATEWAY_DIR="/opt/ibgateway"
IB_GATEWAY_CONFIG_DIR="$IB_GATEWAY_DIR/ibgateway"

echo "Paso 1: Verificando Java..."
if ! command -v java &> /dev/null; then
    echo "Java no está instalado. Instalando..."
    apt update
    apt install -y openjdk-17-jre-headless
    echo "✓ Java instalado"
else
    echo "✓ Java ya está instalado"
    java -version
fi
echo ""

echo "Paso 2: Creando directorio para IB Gateway..."
mkdir -p "$IB_GATEWAY_DIR"
mkdir -p "$IB_GATEWAY_CONFIG_DIR"
echo "✓ Directorios creados"
echo ""

echo "Paso 3: Descarga de IB Gateway"
echo "⚠️  IMPORTANTE: Necesitas descargar IB Gateway manualmente"
echo ""
echo "1. Visita: https://www.interactivebrokers.com/en/index.php?f=16457"
echo "2. Descarga 'IB Gateway' para Linux"
echo "3. Transfiere el archivo .sh al servidor"
echo ""
read -p "¿Ya descargaste el archivo? (s/n): " respuesta

if [ "$respuesta" != "s" ] && [ "$respuesta" != "S" ]; then
    echo "Por favor descarga IB Gateway y vuelve a ejecutar este script"
    exit 1
fi

echo ""
read -p "Ruta completa del archivo .sh descargado: " archivo_ibgateway

if [ ! -f "$archivo_ibgateway" ]; then
    echo "❌ Archivo no encontrado: $archivo_ibgateway"
    exit 1
fi

# Copiar archivo al directorio de instalación
cp "$archivo_ibgateway" "$IB_GATEWAY_DIR/"
chmod +x "$IB_GATEWAY_DIR/$(basename $archivo_ibgateway)"
echo "✓ Archivo copiado"
echo ""

echo "Paso 4: Instalando IB Gateway..."
cd "$IB_GATEWAY_DIR"
./$(basename $archivo_ibgateway) -q -dir "$IB_GATEWAY_DIR"
echo "✓ IB Gateway instalado"
echo ""

echo "Paso 5: Creando archivo de configuración..."
cat > "$IB_GATEWAY_CONFIG_DIR/ibgateway.ini" << 'EOF'
# IB Gateway Configuration
[Settings]
EnableAPI=true
ApiPort=7497
TrustedIPs=127.0.0.1
Headless=true
Paper=Y
EOF
echo "✓ Archivo de configuración creado"
echo ""

echo "Paso 6: Configurando credenciales..."
echo "⚠️  Necesitas tus credenciales de Interactive Brokers"
read -p "Usuario de IB: " ib_username
read -sp "Contraseña de IB: " ib_password
echo ""

cat > "$IB_GATEWAY_CONFIG_DIR/credentials.txt" << EOF
USERNAME=$ib_username
PASSWORD=$ib_password
EOF
chmod 600 "$IB_GATEWAY_CONFIG_DIR/credentials.txt"
echo "✓ Credenciales guardadas (archivo protegido)"
echo ""

echo "Paso 7: Creando script de inicio..."
# Nota: El comando exacto puede variar según la versión de IB Gateway
# Ajusta según la estructura de tu instalación
cat > "$IB_GATEWAY_DIR/start_ibgateway.sh" << 'EOF'
#!/bin/bash
cd /opt/ibgateway
# Ajusta este comando según la estructura de tu instalación de IB Gateway
# Busca el archivo .jar principal en el directorio de instalación
java -cp "$(find /opt/ibgateway -name "*.jar" | tr '\n' ':')" \
     -Dsun.java2d.noddraw=true \
     -Dswing.boldMetal=false \
     ibgateway.GWClient \
     /opt/ibgateway/ibgateway/ibgateway.ini
EOF
chmod +x "$IB_GATEWAY_DIR/start_ibgateway.sh"
echo "✓ Script de inicio creado"
echo ""

echo "Paso 8: Creando servicio systemd..."
cat > /etc/systemd/system/ibgateway.service << EOF
[Unit]
Description=Interactive Brokers Gateway
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$IB_GATEWAY_DIR
ExecStart=$IB_GATEWAY_DIR/start_ibgateway.sh
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable ibgateway
echo "✓ Servicio systemd creado"
echo ""

echo "=========================================="
echo "INSTALACIÓN COMPLETADA"
echo "=========================================="
echo ""
echo "Próximos pasos:"
echo ""
echo "1. Verificar la estructura de archivos de IB Gateway:"
echo "   ls -la $IB_GATEWAY_DIR"
echo ""
echo "2. Ajustar el script de inicio si es necesario:"
echo "   nano $IB_GATEWAY_DIR/start_ibgateway.sh"
echo ""
echo "3. Iniciar IB Gateway:"
echo "   systemctl start ibgateway"
echo ""
echo "4. Verificar que está corriendo:"
echo "   systemctl status ibgateway"
echo "   netstat -tulpn | grep 7497"
echo ""
echo "5. Ver logs:"
echo "   journalctl -u ibgateway -f"
echo ""
echo "=========================================="

