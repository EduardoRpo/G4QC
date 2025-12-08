# 🚀 Instalación y Configuración de IB Gateway en Linux

## 📋 Resumen

IB Gateway es la versión sin interfaz gráfica de Interactive Brokers TWS, ideal para servidores Linux. Se conecta a Interactive Brokers y permite acceso a través de la API.

---

## 🔧 Requisitos Previos

- **Java**: IB Gateway requiere Java 8 o superior
- **Cuenta de Interactive Brokers**: Paper Trading o Live
- **Acceso root o sudo** en el servidor

---

## 📥 Paso 1: Instalar Java

IB Gateway requiere Java. Verifica si ya está instalado:

```bash
java -version
```

Si no está instalado, instálalo:

```bash
# Ubuntu/Debian
apt update
apt install -y openjdk-11-jre-headless

# O para Java 17 (recomendado)
apt install -y openjdk-17-jre-headless

# Verificar instalación
java -version
```

---

## 📥 Paso 2: Descargar IB Gateway

### Opción A: Descarga Manual

1. **Visita el sitio de Interactive Brokers:**
   - Paper Trading: https://www.interactivebrokers.com/en/index.php?f=16457
   - Live Trading: https://www.interactivebrokers.com/en/index.php?f=16457

2. **Descarga IB Gateway para Linux:**
   - Busca "IB Gateway" en la sección de descargas
   - Selecciona la versión para Linux
   - Descarga el archivo `.sh` (ej: `ibgateway-stable-linux-x64.sh`)

3. **Transferir al servidor:**
   ```bash
   # Desde tu máquina local (si descargaste allí)
   scp ibgateway-stable-linux-x64.sh root@45.137.192.196:/tmp/
   ```

### Opción B: Descarga Directa (si tienes el enlace)

```bash
# Crear directorio para IB Gateway
mkdir -p /opt/ibgateway
cd /opt/ibgateway

# Descargar (reemplaza la URL con la versión actual)
wget https://download2.interactivebrokers.com/installers/ibgateway-stable/ibgateway-stable-linux-x64.sh

# Dar permisos de ejecución
chmod +x ibgateway-stable-linux-x64.sh
```

---

## 🔧 Paso 3: Instalar IB Gateway

```bash
cd /opt/ibgateway

# Ejecutar instalador (modo no interactivo)
./ibgateway-stable-linux-x64.sh -q

# O si necesitas especificar el directorio de instalación:
./ibgateway-stable-linux-x64.sh -q -dir /opt/ibgateway
```

Esto instalará IB Gateway en `/opt/ibgateway` (o el directorio que especifiques).

---

## ⚙️ Paso 4: Configurar IB Gateway

### 4.1. Crear archivo de configuración

IB Gateway usa archivos de configuración para ejecutarse sin interfaz gráfica:

```bash
# Crear directorio de configuración
mkdir -p /opt/ibgateway/ibgateway

# Crear archivo de configuración
cat > /opt/ibgateway/ibgateway/ibgateway.ini << 'EOF'
# IB Gateway Configuration
# Este archivo configura IB Gateway para ejecutarse en modo headless

[Settings]
# Habilitar API
EnableAPI=true

# Puerto para API (7497 = Paper Trading, 7496 = Live Trading)
ApiPort=7497

# Permitir conexiones desde localhost
TrustedIPs=127.0.0.1

# Modo headless (sin interfaz gráfica)
Headless=true

# Credenciales (se pueden dejar vacías y se pedirán al iniciar)
# Username=
# Password=

# Modo de trading (Paper o Live)
# Paper=Y para Paper Trading, Paper=N para Live Trading
Paper=Y
EOF
```

### 4.2. Crear archivo de credenciales (opcional pero recomendado)

**⚠️ IMPORTANTE**: Este archivo contiene credenciales sensibles. Asegúrate de protegerlo:

```bash
# Crear archivo con credenciales (cambia USERNAME y PASSWORD)
cat > /opt/ibgateway/ibgateway/credentials.txt << 'EOF'
USERNAME=tu_usuario_ib
PASSWORD=tu_contraseña_ib
EOF

# Proteger el archivo (solo root puede leerlo)
chmod 600 /opt/ibgateway/ibgateway/credentials.txt
```

**Nota**: Puedes dejar las credenciales vacías y se pedirán al iniciar, pero para automatización es mejor tenerlas configuradas.

---

## 🚀 Paso 5: Crear Script de Inicio

Crea un script para iniciar IB Gateway fácilmente:

```bash
cat > /opt/ibgateway/start_ibgateway.sh << 'EOF'
#!/bin/bash

# Script para iniciar IB Gateway
# Uso: /opt/ibgateway/start_ibgateway.sh

IB_GATEWAY_DIR="/opt/ibgateway"
JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"  # Ajusta según tu instalación de Java

# Verificar que Java está instalado
if ! command -v java &> /dev/null; then
    echo "❌ Java no está instalado. Instálalo con: apt install openjdk-17-jre-headless"
    exit 1
fi

# Cambiar al directorio de IB Gateway
cd "$IB_GATEWAY_DIR"

# Iniciar IB Gateway
echo "🚀 Iniciando IB Gateway..."
java -cp "$IB_GATEWAY_DIR/jts.jar:$IB_GATEWAY_DIR/total.2013.jar" \
     -Dsun.java2d.noddraw=true \
     -Dswing.boldMetal=false \
     ibgateway.GWClient \
     "$IB_GATEWAY_DIR/ibgateway/ibgateway.ini"
EOF

chmod +x /opt/ibgateway/start_ibgateway.sh
```

**Nota**: El comando exacto puede variar según la versión de IB Gateway. Verifica la estructura de directorios después de la instalación.

---

## 🔄 Paso 6: Crear Servicio Systemd (Recomendado)

Para que IB Gateway se ejecute automáticamente al iniciar el servidor:

```bash
cat > /etc/systemd/system/ibgateway.service << 'EOF'
[Unit]
Description=Interactive Brokers Gateway
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/ibgateway
ExecStart=/usr/bin/java -cp /opt/ibgateway/jts.jar:/opt/ibgateway/total.2013.jar -Dsun.java2d.noddraw=true -Dswing.boldMetal=false ibgateway.GWClient /opt/ibgateway/ibgateway/ibgateway.ini
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Recargar systemd
systemctl daemon-reload

# Habilitar para que inicie automáticamente
systemctl enable ibgateway

# Iniciar el servicio
systemctl start ibgateway

# Verificar estado
systemctl status ibgateway
```

---

## 🔍 Paso 7: Verificar que IB Gateway Está Corriendo

### Verificar proceso:

```bash
# Ver si el proceso está corriendo
ps aux | grep ibgateway

# Ver si está escuchando en el puerto 7497
netstat -tulpn | grep 7497
# O con ss:
ss -tulpn | grep 7497
```

### Verificar logs:

```bash
# Si usas systemd
journalctl -u ibgateway -f

# O ver logs del servicio
tail -f /opt/ibgateway/logs/ibgateway.log
```

### Probar conexión:

```bash
# Desde el servidor
telnet localhost 7497

# O con nc (netcat)
nc -zv localhost 7497
```

---

## 🔧 Paso 8: Configurar Firewall (si es necesario)

Si tienes firewall activo, asegúrate de que el puerto esté abierto localmente:

```bash
# Verificar si hay firewall
ufw status

# Si está activo, el puerto 7497 solo debe ser accesible desde localhost
# (no necesitas abrirlo al exterior, solo localhost)
```

---

## 🧪 Paso 9: Probar Conexión desde la Aplicación

Una vez que IB Gateway esté corriendo, prueba la conexión desde tu aplicación:

```bash
# Verificar que el backend puede conectarse
docker compose exec backend python -c "
from app.services.data_extraction.ib_extractor import IBDataExtractor
extractor = IBDataExtractor()
try:
    extractor.connect_to_ib()
    print('✅ Conexión exitosa a IB Gateway')
    print(f'Conectado: {extractor.connected}')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

---

## 📝 Paso 10: Configurar Variables de Entorno (si es necesario)

Si IB Gateway está en otro servidor o necesitas cambiar la configuración:

```bash
# Editar .env del backend
nano /opt/proyectos/G4QC/backend/.env
```

Asegúrate de que tenga:
```
IB_HOST=127.0.0.1
IB_PORT=7497
IB_CLIENT_ID=1
```

Si IB Gateway está en otro servidor, cambia `IB_HOST` a la IP del servidor donde está IB Gateway.

---

## 🔄 Comandos Útiles

### Iniciar IB Gateway manualmente:

```bash
/opt/ibgateway/start_ibgateway.sh
```

### Iniciar como servicio:

```bash
systemctl start ibgateway
```

### Detener IB Gateway:

```bash
systemctl stop ibgateway
```

### Ver estado:

```bash
systemctl status ibgateway
```

### Ver logs en tiempo real:

```bash
journalctl -u ibgateway -f
```

### Reiniciar:

```bash
systemctl restart ibgateway
```

---

## ⚠️ Solución de Problemas

### Error: "Java not found"

```bash
# Instalar Java
apt install -y openjdk-17-jre-headless

# Verificar instalación
java -version
```

### Error: "Cannot connect to IB Gateway"

1. **Verificar que IB Gateway está corriendo:**
   ```bash
   ps aux | grep ibgateway
   systemctl status ibgateway
   ```

2. **Verificar que está escuchando en el puerto correcto:**
   ```bash
   netstat -tulpn | grep 7497
   ```

3. **Verificar configuración de API:**
   - Asegúrate de que `EnableAPI=true` en `ibgateway.ini`
   - Verifica que el puerto es correcto (7497 para Paper, 7496 para Live)

### Error: "Connection refused"

- IB Gateway no está corriendo
- Puerto incorrecto en la configuración
- Firewall bloqueando la conexión

### Error: "Client ID already in use"

- Otra aplicación está usando el mismo Client ID
- Cambia `IB_CLIENT_ID` en la configuración del backend

### IB Gateway se cierra constantemente

- Revisa los logs: `journalctl -u ibgateway -n 50`
- Verifica que las credenciales son correctas
- Verifica que hay suficiente memoria: `free -h`

---

## 🔒 Seguridad

**IMPORTANTE**:

1. **Protege las credenciales:**
   ```bash
   chmod 600 /opt/ibgateway/ibgateway/credentials.txt
   ```

2. **No expongas el puerto al exterior:**
   - IB Gateway solo debe ser accesible desde localhost (127.0.0.1)
   - No configures port forwarding para el puerto 7497

3. **Usa Paper Trading para pruebas:**
   - Siempre prueba primero con Paper Trading (puerto 7497)
   - Solo usa Live Trading cuando estés seguro

---

## 📚 Referencias

- [IB Gateway Documentation](https://www.interactivebrokers.com/en/index.php?f=16457)
- [IB API Documentation](https://interactivebrokers.github.io/tws-api/)
- [IB Gateway Download](https://www.interactivebrokers.com/en/index.php?f=16457)

---

## ✅ Verificación Final

Después de la instalación, verifica:

- [ ] Java está instalado: `java -version`
- [ ] IB Gateway está instalado: `ls /opt/ibgateway`
- [ ] Archivo de configuración existe: `ls /opt/ibgateway/ibgateway/ibgateway.ini`
- [ ] Servicio está corriendo: `systemctl status ibgateway`
- [ ] Puerto 7497 está escuchando: `netstat -tulpn | grep 7497`
- [ ] Backend puede conectarse: Probar conexión desde la aplicación

---

**¿Necesitas ayuda con algún paso específico?**
