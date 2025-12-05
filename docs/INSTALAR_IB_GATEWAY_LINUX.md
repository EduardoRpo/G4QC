# 🐧 Instalar IB Gateway en Linux - Guía Completa

## 🎯 Resumen

En Linux puedes hacer todo desde la terminal usando comandos. Esta guía te muestra cómo.

---

## 📋 Parte 1: Crear Cuenta Paper Trading (Mismo Proceso)

**Nota:** Crear la cuenta Paper Trading se hace desde el navegador web (igual que en Windows).

### Opción A: Desde Navegador en Linux

```bash
# Abre Firefox o tu navegador favorito
firefox https://www.interactivebrokers.com/en/index.php?f=16042

# O si usas Chrome/Chromium
google-chrome https://www.interactivebrokers.com/en/index.php?f=16042

# O si usas un navegador basado en texto (lynx, w3m)
lynx https://www.interactivebrokers.com/en/index.php?f=16042
```

**O simplemente:**
1. Abre tu navegador en Linux
2. Ve a: https://www.interactivebrokers.com/en/index.php?f=16042
3. Busca "Paper Trading Account" y créala
4. Recibe Username y Password

**El proceso es igual que en Windows (es una página web).**

---

## 📥 Parte 2: Descargar IB Gateway para Linux

### Paso 1: Identificar tu Sistema

```bash
# Ver arquitectura de tu sistema
uname -m

# Ver distribución Linux
cat /etc/os-release
```

**Resultados típicos:**
- `x86_64` = 64 bits (la mayoría)
- `i386` o `i686` = 32 bits (menos común)

---

### Paso 2: Descargar IB Gateway

**Opción A: Descargar desde Terminal (wget)**

```bash
# Crear directorio para descargas
mkdir -p ~/ibgateway
cd ~/ibgateway

# Descargar IB Gateway para Linux (última versión)
wget https://download2.interactivebrokers.com/installers/ibgateway-stable-latest-linux-x64.sh

# O si tu sistema es 32 bits
# wget https://download2.interactivebrokers.com/installers/ibgateway-stable-latest-linux-i686.sh
```

**Opción B: Descargar con curl**

```bash
cd ~/ibgateway

# Descargar con curl
curl -L -o ibgateway-stable-latest-linux-x64.sh \
  https://download2.interactivebrokers.com/installers/ibgateway-stable-latest-linux-x64.sh
```

**Opción C: Buscar la URL más reciente**

```bash
# Puedes buscar la URL más reciente en el sitio web de IB
# O usar esta URL genérica (reemplaza VERSION con la versión actual)
wget https://download2.interactivebrokers.com/installers/ibgateway-stable-VERSION-linux-x64.sh
```

---

### Paso 3: Dar Permisos de Ejecución

```bash
cd ~/ibgateway

# Dar permisos de ejecución al instalador
chmod +x ibgateway-stable-latest-linux-x64.sh

# Verificar que tiene permisos
ls -lh ibgateway-stable-latest-linux-x64.sh
```

**Deberías ver algo como:**
```
-rwxr-xr-x 1 usuario usuario 50M fecha ibgateway-stable-latest-linux-x64.sh
```
(La `x` significa ejecutable)

---

## 🔧 Parte 3: Instalar IB Gateway

### Instalación Interactiva (Recomendado)

```bash
cd ~/ibgateway

# Ejecutar instalador
./ibgateway-stable-latest-linux-x64.sh
```

**El instalador te preguntará:**
- Dónde instalar (default: `~/Jts`)
- Si quieres crear accesos directos
- Etc.

**Sigue las instrucciones en pantalla.**

---

### Instalación Silenciosa (Sin Preguntas)

```bash
cd ~/ibgateway

# Instalación silenciosa (usa valores por defecto)
./ibgateway-stable-latest-linux-x64.sh -q

# O especificar directorio de instalación
./ibgateway-stable-latest-linux-x64.sh -q -dir ~/IBGateway
```

**Después de la instalación, IB Gateway estará en:**
- Default: `~/Jts/ibgateway` o `~/IBGateway/ibgateway`

---

## 🚀 Parte 4: Ejecutar IB Gateway

### Ejecutar desde Terminal

```bash
# Navegar al directorio de instalación
cd ~/Jts

# Ejecutar IB Gateway
./ibgateway

# O si está en otro directorio
cd ~/IBGateway
./ibgateway
```

**Primera vez:**
- Se abrirá una ventana de login
- Ingresa tu Username y Password de Paper Trading
- Selecciona "Paper Trading" si te pregunta

---

### Ejecutar en Background (Segundo Plano)

```bash
# Ejecutar en background
cd ~/Jts
./ibgateway > /dev/null 2>&1 &

# O guardar logs
./ibgateway > ~/ibgateway.log 2>&1 &

# Ver proceso
ps aux | grep ibgateway
```

---

### Ejecutar como Servicio (Opcional - Avanzado)

Puedes crear un servicio systemd para que IB Gateway se inicie automáticamente:

**Crear archivo de servicio:**

```bash
sudo nano /etc/systemd/system/ibgateway.service
```

**Contenido:**

```ini
[Unit]
Description=Interactive Brokers Gateway
After=network.target

[Service]
Type=simple
User=tu_usuario
WorkingDirectory=/home/tu_usuario/Jts
ExecStart=/home/tu_usuario/Jts/ibgateway
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Habilitar servicio:**

```bash
# Recargar systemd
sudo systemctl daemon-reload

# Habilitar servicio (inicia al boot)
sudo systemctl enable ibgateway

# Iniciar servicio
sudo systemctl start ibgateway

# Ver estado
sudo systemctl status ibgateway

# Ver logs
sudo journalctl -u ibgateway -f
```

---

## ⚙️ Parte 5: Configurar API (Desde Terminal)

### Opción A: Editar Archivo de Configuración

IB Gateway guarda configuración en archivos de texto. Puedes editarlos directamente:

```bash
# Buscar archivo de configuración
find ~/Jts -name "*.ini" -o -name "*config*" | head -5

# Generalmente está en:
nano ~/Jts/jts.ini

# O en:
nano ~/.ibgateway/jts.ini
```

**Buscar sección `[API]` y agregar/modificar:**

```ini
[API]
EnableActiveX=true
SocketPort=7497
TrustedIPs=127.0.0.1
ReadOnlyAPI=false
```

**O desde terminal (agregar si no existe):**

```bash
# Crear o editar configuración
mkdir -p ~/.ibgateway
cat >> ~/.ibgateway/jts.ini << EOF
[API]
EnableActiveX=true
SocketPort=7497
TrustedIPs=127.0.0.1
ReadOnlyAPI=false
EOF
```

---

### Opción B: Usar IB Gateway una vez para Configurar

1. Ejecuta IB Gateway normalmente
2. Configura API desde la interfaz gráfica
3. La configuración se guarda automáticamente

---

## ✅ Parte 6: Verificar Instalación

### Verificar que IB Gateway está Instalado

```bash
# Verificar instalación
ls -la ~/Jts/ibgateway

# O donde lo instalaste
ls -la ~/IBGateway/ibgateway
```

---

### Verificar que el Puerto está Abierto

```bash
# Verificar puerto 7497 después de ejecutar IB Gateway
netstat -tlnp | grep 7497

# O con ss
ss -tlnp | grep 7497

# O con telnet (debe conectar)
telnet localhost 7497
```

**Si está funcionando, deberías ver:**
```
tcp   0   0 127.0.0.1:7497   0.0.0.0:*   LISTEN   12345/ibgateway
```

---

### Verificar desde tu Aplicación

```bash
# Desde tu aplicación Docker
docker-compose exec backend python -c "
from app.services.data_extraction.ib_extractor import IBDataExtractor
extractor = IBDataExtractor()
extractor.connect_to_ib()
print('✅ Conexión exitosa')
"
```

---

## 🔍 Script Completo de Instalación

Aquí tienes un script completo que hace todo automáticamente:

```bash
#!/bin/bash
# install_ibgateway.sh

set -e

echo "🚀 Instalando IB Gateway para Linux..."

# 1. Crear directorio
INSTALL_DIR="$HOME/IBGateway"
DOWNLOADS_DIR="$HOME/ibgateway"
mkdir -p "$DOWNLOADS_DIR"
cd "$DOWNLOADS_DIR"

# 2. Descargar IB Gateway
echo "📥 Descargando IB Gateway..."
wget -q --show-progress \
  https://download2.interactivebrokers.com/installers/ibgateway-stable-latest-linux-x64.sh \
  -O ibgateway-installer.sh

# 3. Dar permisos
chmod +x ibgateway-installer.sh

# 4. Instalar
echo "⚙️ Instalando IB Gateway..."
./ibgateway-installer.sh -q -dir "$INSTALL_DIR"

# 5. Configurar API
echo "🔧 Configurando API..."
mkdir -p "$INSTALL_DIR"
cat > "$INSTALL_DIR/jts.ini" << EOF
[API]
EnableActiveX=true
SocketPort=7497
TrustedIPs=127.0.0.1
ReadOnlyAPI=false
EOF

echo "✅ IB Gateway instalado en: $INSTALL_DIR"
echo ""
echo "Para ejecutar:"
echo "  cd $INSTALL_DIR && ./ibgateway"
```

**Guardar y ejecutar:**

```bash
# Guardar script
nano install_ibgateway.sh

# Pegar el contenido del script
# Guardar (Ctrl+O, Enter, Ctrl+X)

# Dar permisos
chmod +x install_ibgateway.sh

# Ejecutar
./install_ibgateway.sh
```

---

## 🎯 Resumen de Comandos

### Instalación Rápida:

```bash
# 1. Descargar
mkdir -p ~/ibgateway && cd ~/ibgateway
wget https://download2.interactivebrokers.com/installers/ibgateway-stable-latest-linux-x64.sh
chmod +x ibgateway-stable-latest-linux-x64.sh

# 2. Instalar
./ibgateway-stable-latest-linux-x64.sh -q

# 3. Ejecutar
cd ~/Jts
./ibgateway
```

### Configurar API:

```bash
# Editar configuración
nano ~/Jts/jts.ini

# Agregar:
[API]
EnableActiveX=true
SocketPort=7497
```

### Verificar:

```bash
# Ver puerto
ss -tlnp | grep 7497

# O desde tu app
docker-compose exec backend python -c "from app.services.data_extraction.ib_extractor import IBDataExtractor; IBDataExtractor().connect_to_ib(); print('OK')"
```

---

## 🐧 Consideraciones Especiales para Linux

### Sin Interfaz Gráfica (Headless)

Si tu servidor Linux no tiene interfaz gráfica:

**Opción 1: Usar X11 Forwarding (SSH)**

```bash
# Desde tu PC local, conectar con X11 forwarding
ssh -X usuario@servidor-linux

# En el servidor, exportar display
export DISPLAY=:10.0

# Ejecutar IB Gateway
cd ~/Jts
./ibgateway
```

**Opción 2: Usar VNC**

```bash
# Instalar VNC server
sudo apt-get install tigervnc-standalone-server

# Iniciar servidor VNC
vncserver :1

# Conectar con cliente VNC y ejecutar IB Gateway
```

**Opción 3: Ejecutar IB Gateway en Otra Máquina**

- Ejecuta IB Gateway en Windows/macOS o Linux con GUI
- Conecta desde tu servidor Linux usando el IP de esa máquina
- Cambia `IB_HOST` en tu `.env` a la IP de esa máquina

---

## 🔧 Troubleshooting

### Error: "Permission denied"

```bash
# Dar permisos de ejecución
chmod +x ibgateway-stable-latest-linux-x64.sh
```

### Error: "No space left on device"

```bash
# Verificar espacio
df -h

# Limpiar si es necesario
sudo apt-get clean
```

### Error: "Cannot connect to display"

```bash
# Si no tienes GUI, usa X11 forwarding o VNC
# O ejecuta IB Gateway en otra máquina
```

### Error: Puerto 7497 ya en uso

```bash
# Ver qué está usando el puerto
sudo lsof -i :7497

# O
sudo netstat -tlnp | grep 7497

# Matar proceso si es necesario
sudo kill -9 PID
```

---

## ✅ Checklist Completo

- [ ] Crear cuenta Paper Trading (desde navegador)
- [ ] Descargar IB Gateway para Linux
- [ ] Dar permisos de ejecución al instalador
- [ ] Ejecutar instalador
- [ ] Ejecutar IB Gateway
- [ ] Iniciar sesión con Paper Trading
- [ ] Configurar API (habilitar socket, puerto 7497)
- [ ] Verificar puerto 7497 abierto
- [ ] Probar conexión desde tu aplicación

---

**¿Necesitas ayuda con algún paso específico en Linux?**

