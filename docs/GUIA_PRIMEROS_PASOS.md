# 🚀 Guía de Primeros Pasos - Qué Probar Ahora

## ✅ Lo que YA está implementado y listo para probar

1. **Backend FastAPI** con endpoints básicos
2. **Servicio de extracción IB** (refactorizado del notebook)
3. **Modelos de base de datos**
4. **Procesamiento de datos** con normalización de timezone
5. **API REST** para extracción y consulta de datos

---

## 📋 Paso 1: Configurar el Entorno

### Opción A: Con Docker (Recomendado - Más fácil)

```bash
# 1. Ir al directorio del proyecto
cd G4QC

# 2. Crear archivo .env (si no existe)
# En Windows PowerShell:
if (!(Test-Path backend\.env)) { Copy-Item backend\.env.example backend\.env }

# O manualmente: copia backend/.env.example a backend/.env
```

### Opción B: Sin Docker (Desarrollo Local)

Requiere PostgreSQL y Redis instalados localmente.

---

## 📋 Paso 2: Iniciar los Servicios

### Con Docker:

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver los logs para verificar que todo está funcionando
docker-compose logs -f
```

Deberías ver:
- ✅ PostgreSQL iniciado
- ✅ Redis iniciado  
- ✅ Backend iniciado en puerto 8000

### Sin Docker:

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configurar .env con tu DATABASE_URL local
# Luego:
uvicorn app.main:app --reload
```

---

## 📋 Paso 3: Inicializar la Base de Datos

### Con Docker:

```bash
# Aplicar migraciones para crear las tablas
docker-compose exec backend alembic upgrade head
```

### Sin Docker:

```bash
cd backend
alembic upgrade head
```

**Esto creará:**
- Tabla `market_data` para almacenar datos históricos
- Índices optimizados
- TimescaleDB hypertable (si está disponible)

---

## 📋 Paso 4: Probar que Todo Funciona

### 4.1 Health Check (Prueba Básica)

```bash
# Con PowerShell
Invoke-WebRequest -Uri http://localhost:8000/health -Method GET

# O con curl
curl http://localhost:8000/health
```

**Debería retornar:**
```json
{"status":"healthy"}
```

### 4.2 Ver Documentación de la API

Abre en tu navegador:
```
http://localhost:8000/docs
```

Verás la documentación interactiva de Swagger con todos los endpoints disponibles.

### 4.3 Probar Endpoints Sin IB (No requiere TWS)

```powershell
# Listar símbolos (vacío inicialmente)
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/data/symbols" -Method GET

# Debería retornar: {"symbols": [], "count": 0}
```

---

## 📋 Paso 5: Probar Extracción de Datos (Requiere IB TWS/Gateway)

### ⚠️ IMPORTANTE: Antes de esto

1. **Abre Interactive Brokers TWS o IB Gateway**
2. **Configura para Paper Trading** (puerto 7497) o Live (7496)
3. **Asegúrate de que esté conectado**

### 5.1 Extraer Datos de Prueba

```powershell
# Preparar el request
$body = @{
    symbol = "ES"
    duration = "3600 S"
    bar_size = "1 min"
    num_blocks = 1
} | ConvertTo-Json

# Enviar request
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/data/extract" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

**O con curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/data/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "ES",
    "duration": "3600 S",
    "bar_size": "1 min",
    "num_blocks": 1
  }'
```

**Debería retornar:**
```json
{
  "status": "success",
  "records": 60,
  "symbol": "ES",
  "date_range": {
    "start": "2024-01-15T10:00:00+00:00",
    "end": "2024-01-15T11:00:00+00:00"
  },
  "message": "Datos extraídos y guardados correctamente"
}
```

### 5.2 Consultar los Datos Guardados

```powershell
# Obtener datos guardados
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/data/data/ES?timeframe=1min&limit=10" -Method GET

# Listar símbolos disponibles (ahora debería mostrar ES)
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/data/symbols" -Method GET
```

---

## 📋 Paso 6: Verificar en la Base de Datos (Opcional)

### Con Docker:

```bash
# Conectarse a PostgreSQL
docker-compose exec postgres psql -U g4qc -d g4qc_db

# Dentro de PostgreSQL:
SELECT COUNT(*) FROM market_data;
SELECT symbol, timeframe, COUNT(*) 
FROM market_data 
GROUP BY symbol, timeframe;
SELECT * FROM market_data ORDER BY timestamp DESC LIMIT 5;

# Salir
\q
```

---

## 🎯 Checklist de Verificación

- [ ] Servicios iniciados (PostgreSQL, Redis, Backend)
- [ ] Health check retorna `{"status":"healthy"}`
- [ ] Documentación accesible en `/docs`
- [ ] Base de datos inicializada (migraciones aplicadas)
- [ ] Endpoint de símbolos funciona (retorna lista vacía)
- [ ] (Opcional) Extracción de datos funciona (si tienes IB TWS)
- [ ] (Opcional) Datos se guardan y se pueden consultar

---

## 🐛 Solución de Problemas Comunes

### Error: "Cannot connect to IB"

**Causa**: IB TWS/Gateway no está ejecutándose o en puerto incorrecto.

**Solución**:
1. Abre TWS/Gateway
2. Ve a Configuración → API → Settings
3. Verifica que "Enable ActiveX and Socket Clients" esté marcado
4. Verifica el puerto (7497 para paper, 7496 para live)
5. Verifica en `backend/.env` que `IB_HOST=127.0.0.1` y `IB_PORT=7497`

### Error: "Table does not exist"

**Causa**: Migraciones no aplicadas.

**Solución**:
```bash
docker-compose exec backend alembic upgrade head
```

### Error: "Connection refused" a PostgreSQL

**Causa**: PostgreSQL no está iniciado.

**Solución**:
```bash
docker-compose up -d postgres
docker-compose logs postgres
```

---

## 📊 Endpoints Disponibles para Probar

### Sin Requerir IB TWS:

1. `GET /health` - Health check
2. `GET /docs` - Documentación interactiva
3. `GET /api/v1/data/symbols` - Listar símbolos (vacío inicialmente)
4. `GET /api/v1/data/data/{symbol}` - Consultar datos (requiere datos previos)

### Requieren IB TWS:

1. `POST /api/v1/data/extract` - Extraer datos históricos
2. `GET /api/v1/data/timeframes/{symbol}` - Listar timeframes (requiere datos previos)

---

## 🎉 Siguiente Paso

Una vez que hayas probado exitosamente:

1. ✅ **Extraer datos de múltiples símbolos** (ES, NQ, EC, etc.)
2. ✅ **Verificar normalización de timezone** (todos en UTC)
3. ✅ **Generar timeframes adicionales** automáticamente
4. 🚧 **Implementar frontend React** para visualizar datos
5. 🚧 **Agregar motor de backtesting**

---

## 📚 Documentación de Referencia

- **Setup completo**: Ver `SETUP.md`
- **Arquitectura**: Ver `PROPUESTA_ARQUITECTURA.md`
- **Análisis de decisiones**: Ver `ANALISIS_DATOS_MT5_VS_IB.md`

---

**¿Tienes algún problema? Revisa los logs:**
```bash
docker-compose logs -f backend
```

