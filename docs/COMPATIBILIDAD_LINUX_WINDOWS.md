# 🐧 Compatibilidad: Windows vs Linux

## ✅ Respuesta Corta

**Sí, funciona en Linux también.** De hecho, Linux es muy común para aplicaciones de trading en producción.

---

## 📊 Compatibilidad por Componente

### 1. **Tu Aplicación (FastAPI + Python)** ✅ Multiplataforma

- ✅ **Windows**: Funciona
- ✅ **Linux**: Funciona
- ✅ **macOS**: Funciona

**Razón**: Python es multiplataforma. El código no tiene dependencias específicas de Windows.

---

### 2. **Docker y Docker Compose** ✅ Multiplataforma

- ✅ **Windows**: Docker Desktop
- ✅ **Linux**: Docker Engine (nativo)
- ✅ **macOS**: Docker Desktop

**Razón**: Docker es multiplataforma. Los contenedores funcionan igual en todas las plataformas.

---

### 3. **IB TWS / IB Gateway** ✅ Multiplataforma

- ✅ **Windows**: Disponible
- ✅ **Linux**: Disponible (versión para Linux)
- ✅ **macOS**: Disponible

**Razón**: Interactive Brokers proporciona versiones para todas las plataformas.

**Descarga para Linux:**
- Ve a: https://www.interactivebrokers.com/en/index.php?f=16042
- Descarga la versión para Linux

---

### 4. **ibapi (Librería Python)** ✅ Multiplataforma

- ✅ **Windows**: Funciona
- ✅ **Linux**: Funciona
- ✅ **macOS**: Funciona

**Razón**: Es una librería Python pura, multiplataforma.

---

### 5. **Conexión Socket TCP** ✅ Multiplataforma

- ✅ **Windows**: `127.0.0.1:7497`
- ✅ **Linux**: `127.0.0.1:7497`
- ✅ **macOS**: `127.0.0.1:7497`

**Razón**: Los sockets TCP funcionan igual en todas las plataformas.

---

## 🔄 Diferencias entre Windows y Linux

### Configuración de IB Gateway

#### Windows:
- Descarga `.exe` o instalador
- Instalación gráfica estándar
- Configuración API: File → Global Configuration → API → Settings

#### Linux:
- Descarga `.sh` (script de instalación)
- Instalación desde terminal:
  ```bash
  chmod +x ibgateway-stable-*.sh
  ./ibgateway-stable-*.sh
  ```
- Configuración API: Mismo proceso (interfaz gráfica o archivo de configuración)

---

### Comandos de Terminal

#### Windows (PowerShell):
```powershell
# Verificar puerto
Test-NetConnection -ComputerName localhost -Port 7497

# Docker
docker-compose up -d
docker-compose exec backend pip install ibapi
```

#### Linux (Bash):
```bash
# Verificar puerto
nc -zv localhost 7497
# O
telnet localhost 7497

# Docker
docker-compose up -d
docker-compose exec backend pip install ibapi
```

---

### Rutas y Archivos

#### Windows:
- Archivo `.env`: `backend\.env`
- Rutas: `C:\D\Trabajo\G4QC\G4QC\`

#### Linux:
- Archivo `.env`: `backend/.env`
- Rutas: `/home/usuario/proyectos/G4QC/G4QC/`

**Nota**: El código usa rutas relativas, así que funciona igual en ambas plataformas.

---

## 🐧 Configuración Específica para Linux

### 1. Instalar IB Gateway en Linux

```bash
# Descargar desde IB
wget https://download2.interactivebrokers.com/installers/ibgateway-stable-latest-linux-x64.sh

# Dar permisos de ejecución
chmod +x ibgateway-stable-latest-linux-x64.sh

# Ejecutar instalador
./ibgateway-stable-latest-linux-x64.sh

# Seguir instrucciones del instalador
```

### 2. Ejecutar IB Gateway en Linux

```bash
# Navegar a la carpeta de instalación (típicamente)
cd ~/Jts

# Ejecutar IB Gateway
./ibgateway
```

### 3. Configuración API (igual que Windows)

- File → Global Configuration → API → Settings
- Habilitar "Enable ActiveX and Socket Clients"
- Puerto: `7497`

---

## 🚀 Ventajas de Linux para Trading

### 1. **Rendimiento**
- Linux generalmente tiene mejor rendimiento
- Menor uso de recursos
- Ideal para servidores

### 2. **Estabilidad**
- Menos reinicios necesarios
- Mejor para ejecución 24/7

### 3. **Docker Nativo**
- Docker funciona nativamente en Linux
- No necesita Docker Desktop (más liviano)

### 4. **Scripts y Automatización**
- Bash es más potente que PowerShell
- Mejor para cron jobs y automatización

---

## ⚙️ Configuración Docker en Linux

### Instalación de Docker en Linux:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# O usar Docker oficial
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
```

### Comandos (igual que Windows):

```bash
# Iniciar servicios
docker-compose up -d

# Instalar ibapi
docker-compose exec backend pip install ibapi

# Ver logs
docker-compose logs backend

# Reiniciar
docker-compose restart backend
```

---

## 🔍 Verificación en Linux

### 1. Verificar puerto:

```bash
# Opción 1: netcat
nc -zv localhost 7497

# Opción 2: telnet
telnet localhost 7497

# Opción 3: ss
ss -tlnp | grep 7497
```

### 2. Verificar que IB Gateway está ejecutándose:

```bash
# Ver procesos
ps aux | grep ibgateway

# Ver puertos abiertos
netstat -tlnp | grep 7497
```

---

## 📝 Ejemplo: Configuración Completa en Linux

### Paso 1: Instalar Docker

```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo usermod -aG docker $USER
# Cerrar sesión y volver a entrar
```

### Paso 2: Instalar IB Gateway

```bash
# Descargar
wget https://download2.interactivebrokers.com/installers/ibgateway-stable-latest-linux-x64.sh

# Instalar
chmod +x ibgateway-stable-latest-linux-x64.sh
./ibgateway-stable-latest-linux-x64.sh
```

### Paso 3: Configurar IB Gateway

1. Ejecutar: `~/Jts/ibgateway`
2. Iniciar sesión
3. Habilitar API (puerto 7497)

### Paso 4: Configurar Aplicación

```bash
# Clonar proyecto
git clone <tu-repo> G4QC
cd G4QC/G4QC

# Iniciar servicios
docker-compose up -d

# Instalar ibapi
docker-compose exec backend pip install ibapi
docker-compose restart backend
```

### Paso 5: Probar

```bash
# Verificar puerto
nc -zv localhost 7497

# Probar API
curl http://localhost:8000/health
```

---

## 🎯 Resumen

### ✅ Funciona en:
- ✅ **Windows** (probado y documentado)
- ✅ **Linux** (compatible, muy común en producción)
- ✅ **macOS** (compatible)

### 🔄 Diferencias:
- **Comandos de terminal**: PowerShell vs Bash
- **Instalación IB Gateway**: `.exe` vs `.sh`
- **Rutas**: `\` vs `/` (pero el código usa rutas relativas)

### 💡 Recomendación:
- **Desarrollo**: Windows está bien
- **Producción**: Linux es mejor (mejor rendimiento, estabilidad)

---

## 🚨 Consideraciones Especiales

### 1. **IB Gateway en Linux sin GUI**

Si ejecutas Linux sin interfaz gráfica (servidor headless):

**Opción A: Usar X11 forwarding (SSH)**
```bash
ssh -X usuario@servidor
export DISPLAY=:10.0
./ibgateway
```

**Opción B: Usar VNC**
```bash
# Instalar VNC server
sudo apt-get install tigervnc-standalone-server

# Ejecutar IB Gateway a través de VNC
```

**Opción C: Usar IB Gateway en otra máquina**
- Ejecutar IB Gateway en Windows/macOS
- Conectar desde Linux usando el IP de esa máquina
- Cambiar `IB_HOST` en `.env` a la IP de la máquina con IB Gateway

### 2. **Firewall en Linux**

```bash
# Permitir puerto 7497
sudo ufw allow 7497/tcp

# O con iptables
sudo iptables -A INPUT -p tcp --dport 7497 -j ACCEPT
```

---

## ✅ Conclusión

**Tu aplicación funciona perfectamente en Linux.** De hecho, Linux es muy común para aplicaciones de trading en producción debido a su estabilidad y rendimiento.

**La única diferencia real es:**
- Cómo instalas IB Gateway (`.exe` vs `.sh`)
- Comandos de terminal (PowerShell vs Bash)

**Todo lo demás es idéntico.**

---

**¿Necesitas ayuda con la configuración en Linux específicamente?**

