# ⚙️ Configuración Completa: Aplicación + IB TWS

## 📋 Resumen

Necesitas configurar **2 cosas**:
1. **Tu aplicación** (variables de entorno)
2. **IB TWS/Gateway** (habilitar API)

---

## 🔧 PARTE 1: Configuración en tu Aplicación

### Opción A: Usando Docker (Recomendado)

#### 1. Crear archivo `.env` en `backend/`

```powershell
# Navegar a la carpeta backend
cd backend

# Crear archivo .env
# (Puedes usar cualquier editor de texto)
```

Crea el archivo `backend/.env` con este contenido:

```env
# ============================================
# INTERACTIVE BROKERS CONFIGURATION
# ============================================

# Host donde está IB TWS (localhost si está en la misma máquina)
IB_HOST=127.0.0.1

# Puerto de IB TWS
# 7497 = Paper Trading (recomendado para pruebas)
# 7496 = Live Trading (cuenta real)
IB_PORT=7497

# Client ID (debe ser único, no debe estar en uso)
# Si tienes múltiples conexiones, usa IDs diferentes (1, 2, 3, etc.)
IB_CLIENT_ID=1

# ============================================
# DATABASE CONFIGURATION
# ============================================
# (Ya está configurado en docker-compose.yml, pero puedes sobrescribir aquí)
DATABASE_URL=postgresql://g4qc:g4qc_dev@postgres:5432/g4qc_db

# ============================================
# REDIS CONFIGURATION
# ============================================
# (Ya está configurado en docker-compose.yml)
REDIS_URL=redis://redis:6379

# ============================================
# DEBUG MODE
# ============================================
DEBUG=False
```

#### 2. Verificar que Docker Compose use el `.env`

El `docker-compose.yml` ya está configurado para leer variables de entorno:

```yaml
environment:
  IB_HOST: ${IB_HOST:-127.0.0.1}      # Lee de .env o usa default
  IB_PORT: ${IB_PORT:-7497}           # Lee de .env o usa default
  IB_CLIENT_ID: ${IB_CLIENT_ID:-1}    # Lee de .env o usa default
```

**Nota**: Si no creas el `.env`, usará los valores por defecto (que están bien para empezar).

#### 3. Reiniciar contenedores

```powershell
# Desde la raíz del proyecto (G4QC)
docker-compose down
docker-compose up -d
```

---

### Opción B: Desarrollo Local (Sin Docker)

Si ejecutas la aplicación directamente (sin Docker):

#### 1. Crear archivo `.env` en `backend/`

Mismo contenido que arriba, pero con URLs locales:

```env
# Interactive Brokers
IB_HOST=127.0.0.1
IB_PORT=7497
IB_CLIENT_ID=1

# Database (si PostgreSQL está en localhost)
DATABASE_URL=postgresql://g4qc:g4qc_dev@localhost:5432/g4qc_db

# Redis (si Redis está en localhost)
REDIS_URL=redis://localhost:6379

DEBUG=True
```

#### 2. Instalar dependencias

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
pip install ibapi  # Instalar ibapi manualmente
```

#### 3. Ejecutar aplicación

```powershell
uvicorn app.main:app --reload
```

---

## 🔧 PARTE 2: Configuración en IB TWS/Gateway

### Paso 1: Descargar e Instalar IB Gateway (Recomendado)

**IB Gateway** es más liviano que TWS (recomendado para automatización).

1. Ve a: https://www.interactivebrokers.com/en/index.php?f=16042
2. Descarga **IB Gateway** (no TWS completo)
3. Instálalo en tu computadora Windows
4. Ejecuta **IB Gateway**

---

### Paso 2: Iniciar Sesión

1. **Abre IB Gateway**
2. **Inicia sesión** con tu cuenta:
   - Si tienes cuenta real → usa tus credenciales
   - Si no tienes cuenta → crea una cuenta de **Paper Trading** (gratis, sin riesgo)

**Para crear cuenta Paper Trading:**
- Ve a: https://www.interactivebrokers.com/en/index.php?f=16042
- Busca "Paper Trading Account"
- Regístrate (es gratis)

---

### Paso 3: Habilitar API en IB Gateway

**⚠️ IMPORTANTE: Este paso es crítico**

1. **En IB Gateway**, ve a:
   - **File** → **Global Configuration** → **API** → **Settings**
   - O busca "API Settings" en la configuración

2. **Habilita las siguientes opciones:**
   - ✅ **"Enable ActiveX and Socket Clients"** (MÁS IMPORTANTE)
   - ✅ **"Read-Only API"** (opcional, para solo lectura)

3. **Configura el puerto:**
   - **Socket port**: `7497` (para Paper Trading)
   - O `7496` (para Live Trading)
   
   **⚠️ Debe coincidir con `IB_PORT` en tu `.env`**

4. **Trusted IPs (Opcional pero recomendado):**
   - Agrega: `127.0.0.1` (solo permite conexiones desde localhost)
   - O deja vacío para permitir cualquier IP (menos seguro)

5. **Guarda** y **reinicia IB Gateway** si es necesario

---

### Paso 4: Verificar que IB Gateway está Conectado

1. **En IB Gateway**, verifica que muestre:
   - ✅ **"Connected"** o **"Conectado"** (en la parte superior)
   - ✅ Estado verde o indicador de conexión activa

2. **Si no está conectado:**
   - Verifica tu conexión a internet
   - Verifica tus credenciales
   - Espera unos segundos (puede tardar en conectar)

---

## ✅ Verificación: Probar la Conexión

### 1. Verificar que el puerto está abierto

```powershell
# Windows PowerShell
Test-NetConnection -ComputerName localhost -Port 7497
```

**Debería mostrar:**
```
TcpTestSucceeded : True
```

Si muestra `False`, IB Gateway no está escuchando en ese puerto.

---

### 2. Probar desde la API

#### Opción A: Desde el navegador (Swagger UI)

1. Asegúrate de que tu aplicación esté ejecutándose:
   ```powershell
   docker-compose up -d
   ```

2. Abre: http://localhost:8000/docs

3. Busca el endpoint: `POST /api/v1/data/extract`

4. Haz clic en **"Try it out"**

5. Ingresa estos datos de prueba:
   ```json
   {
     "symbol": "ES",
     "duration": "1 D",
     "bar_size": "1 min",
     "num_blocks": 1,
     "save_to_db": true
   }
   ```

6. Haz clic en **"Execute"**

**Si funciona:**
- Verás `200 OK` con datos
- Los datos se guardarán en PostgreSQL

**Si falla:**
- Verás un error con detalles
- Revisa los logs: `docker-compose logs backend`

---

#### Opción B: Desde terminal (curl)

```powershell
curl -X POST "http://localhost:8000/api/v1/data/extract" `
  -H "Content-Type: application/json" `
  -d '{
    "symbol": "ES",
    "duration": "1 D",
    "bar_size": "1 min",
    "num_blocks": 1
  }'
```

---

## 🔍 Troubleshooting: Problemas Comunes

### Error: "Connection refused" o "Cannot connect to IB"

**Causas posibles:**
1. IB Gateway no está ejecutándose
2. API no está habilitada
3. Puerto incorrecto

**Solución:**
1. ✅ Abre IB Gateway
2. ✅ Verifica que esté conectado
3. ✅ Verifica configuración API (puerto 7497)
4. ✅ Reinicia IB Gateway

---

### Error: "ibapi no está instalado"

**Solución:**
```powershell
# Si usas Docker
docker-compose exec backend pip install ibapi
docker-compose restart backend

# Si es local
pip install ibapi
```

---

### Error: "Client ID already in use"

**Causa:** Otra aplicación está usando el mismo Client ID

**Solución:**
1. Cambia `IB_CLIENT_ID` en tu `.env`:
   ```env
   IB_CLIENT_ID=2  # O 3, 4, etc.
   ```
2. Reinicia la aplicación

---

### Error: "Timeout al conectar"

**Causas posibles:**
1. IB Gateway no responde
2. Firewall bloqueando
3. Puerto incorrecto

**Solución:**
1. ✅ Verifica que IB Gateway esté ejecutándose
2. ✅ Verifica puerto en IB Gateway (7497)
3. ✅ Verifica puerto en `.env` (debe coincidir)
4. ✅ Desactiva firewall temporalmente para probar

---

## 📝 Checklist de Configuración

### ✅ En tu Aplicación:
- [ ] Archivo `.env` creado en `backend/` (o usar defaults)
- [ ] Variables configuradas:
  - [ ] `IB_HOST=127.0.0.1`
  - [ ] `IB_PORT=7497` (o 7496 para live)
  - [ ] `IB_CLIENT_ID=1`
- [ ] `ibapi` instalado
- [ ] Aplicación ejecutándose (`docker-compose up -d`)

### ✅ En IB Gateway/TWS:
- [ ] IB Gateway instalado y ejecutándose
- [ ] Sesión iniciada (conectado a IB)
- [ ] API habilitada:
  - [ ] "Enable ActiveX and Socket Clients" ✅
  - [ ] Puerto configurado: `7497` (o `7496`)
- [ ] IB Gateway muestra "Connected"

### ✅ Verificación:
- [ ] Puerto 7497 está abierto (`Test-NetConnection`)
- [ ] Endpoint `/docs` funciona
- [ ] Prueba de extracción funciona

---

## 🎯 Resumen Rápido

### En tu Aplicación:
1. Crea `backend/.env` con:
   ```env
   IB_HOST=127.0.0.1
   IB_PORT=7497
   IB_CLIENT_ID=1
   ```
2. Instala `ibapi`: `docker-compose exec backend pip install ibapi`

### En IB Gateway:
1. Abre IB Gateway
2. Inicia sesión
3. Settings → API → Enable "ActiveX and Socket Clients"
4. Puerto: `7497`
5. Guarda y reinicia

### Probar:
1. `docker-compose up -d`
2. Abre: http://localhost:8000/docs
3. Prueba `POST /api/v1/data/extract`

---

**¿Necesitas ayuda con algún paso específico?**

