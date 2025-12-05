# 📡 Endpoints Disponibles y Cómo Probarlos

## 🎯 Resumen

Actualmente tenemos **6 endpoints** disponibles en la API:

1. `GET /` - Información de la API
2. `GET /health` - Health check
3. `POST /api/v1/data/extract` - Extraer datos desde IB
4. `GET /api/v1/data/data/{symbol}` - Consultar datos históricos
5. `GET /api/v1/data/symbols` - Listar símbolos disponibles
6. `GET /api/v1/data/timeframes/{symbol}` - Listar timeframes disponibles

---

## 📋 Endpoint 1: `GET /` - Información de la API

### ¿Qué hace?
Retorna información básica sobre la API (nombre, versión, link a documentación).

### Cómo probarlo:

**Opción A: Navegador**
```
http://localhost:8000/
```

**Opción B: curl (PowerShell)**
```powershell
curl http://localhost:8000/
```

**Respuesta esperada:**
```json
{
  "message": "G4QC Trading Platform API",
  "version": "0.1.0",
  "docs": "/docs"
}
```

---

## 📋 Endpoint 2: `GET /health` - Health Check

### ¿Qué hace?
Verifica que el servicio esté funcionando correctamente. Útil para monitoreo.

### Cómo probarlo:

**Opción A: Navegador**
```
http://localhost:8000/health
```

**Opción B: curl**
```powershell
curl http://localhost:8000/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy"
}
```

**✅ Este endpoint SIEMPRE funciona** (no requiere IB TWS ni datos en la DB).

---

## 📋 Endpoint 3: `POST /api/v1/data/extract` - Extraer Datos desde IB

### ¿Qué hace?
1. Se conecta a Interactive Brokers TWS/Gateway
2. Solicita datos históricos para un símbolo (ES, NQ, EC, etc.)
3. Procesa los datos (normaliza timezones a UTC)
4. Guarda en PostgreSQL
5. Genera timeframes adicionales (5min, 15min, etc.) en background

### Parámetros:

| Parámetro | Tipo | Requerido | Descripción | Ejemplo |
|-----------|------|-----------|-------------|---------|
| `symbol` | string | ✅ Sí | Símbolo del instrumento | `"ES"`, `"NQ"`, `"EC"` |
| `duration` | string | ❌ No | Duración por bloque | `"1 M"`, `"1 D"`, `"3600 S"` |
| `bar_size` | string | ❌ No | Tamaño de barra | `"1 min"`, `"5 mins"`, `"1 hour"` |
| `contract_month` | string | ❌ No | Mes de vencimiento | `"202512"` |
| `num_blocks` | integer | ❌ No | Número de bloques (1-12) | `1`, `3`, `12` |
| `save_to_db` | boolean | ❌ No | Guardar en base de datos | `true`, `false` |

### Cómo probarlo:

**Opción A: Swagger UI (Recomendado)**
1. Abre: http://localhost:8000/docs
2. Busca: `POST /api/v1/data/extract`
3. Haz clic en "Try it out"
4. Ingresa estos datos:
   ```json
   {
     "symbol": "ES",
     "duration": "1 D",
     "bar_size": "1 min",
     "num_blocks": 1,
     "save_to_db": true
   }
   ```
5. Haz clic en "Execute"

**Opción B: curl (PowerShell)**
```powershell
curl -X POST "http://localhost:8000/api/v1/data/extract" `
  -H "Content-Type: application/json" `
  -d '{
    "symbol": "ES",
    "duration": "1 D",
    "bar_size": "1 min",
    "num_blocks": 1,
    "save_to_db": true
  }'
```

**Respuesta esperada (éxito):**
```json
{
  "status": "success",
  "records": 1440,
  "symbol": "ES",
  "date_range": {
    "start": "2024-12-02T00:00:00+00:00",
    "end": "2024-12-02T23:59:00+00:00"
  },
  "message": "Datos extraídos y guardados correctamente"
}
```

**⚠️ Requisitos:**
- ✅ `ibapi` instalado
- ✅ IB TWS/Gateway ejecutándose
- ✅ IB Gateway conectado a Interactive Brokers

**❌ Si no tienes IB TWS:**
Verás un error `503` con mensaje explicativo.

---

## 📋 Endpoint 4: `GET /api/v1/data/data/{symbol}` - Consultar Datos Históricos

### ¿Qué hace?
Consulta datos históricos que ya están guardados en PostgreSQL. No requiere IB TWS.

### Parámetros:

| Parámetro | Tipo | Ubicación | Descripción | Ejemplo |
|-----------|------|-----------|-------------|---------|
| `symbol` | string | Path | Símbolo del instrumento | `ES`, `NQ` |
| `timeframe` | string | Query | Timeframe | `1min`, `5min`, `15min` |
| `start_date` | datetime | Query | Fecha inicio (opcional) | `2024-12-01T00:00:00` |
| `end_date` | datetime | Query | Fecha fin (opcional) | `2024-12-02T23:59:59` |
| `limit` | integer | Query | Límite de registros | `100`, `1000` |

### Cómo probarlo:

**Opción A: Swagger UI**
1. Abre: http://localhost:8000/docs
2. Busca: `GET /api/v1/data/data/{symbol}`
3. Haz clic en "Try it out"
4. Ingresa:
   - `symbol`: `ES`
   - `timeframe`: `1min`
   - `limit`: `100`
5. Haz clic en "Execute"

**Opción B: Navegador**
```
http://localhost:8000/api/v1/data/data/ES?timeframe=1min&limit=100
```

**Opción C: curl**
```powershell
curl "http://localhost:8000/api/v1/data/data/ES?timeframe=1min&limit=100"
```

**Respuesta esperada:**
```json
{
  "symbol": "ES",
  "timeframe": "1min",
  "records": 100,
  "data": [
    {
      "timestamp": "2024-12-02T00:00:00+00:00",
      "open": 4567.25,
      "high": 4568.50,
      "low": 4566.75,
      "close": 4568.00,
      "volume": 12345,
      "count": 234
    },
    {
      "timestamp": "2024-12-02T00:01:00+00:00",
      "open": 4568.00,
      "high": 4569.25,
      "low": 4567.50,
      "close": 4568.75,
      "volume": 12350,
      "count": 235
    }
    // ... más registros
  ]
}
```

**✅ Este endpoint funciona SIN IB TWS** (solo necesita datos en la DB).

---

## 📋 Endpoint 5: `GET /api/v1/data/symbols` - Listar Símbolos Disponibles

### ¿Qué hace?
Lista todos los símbolos que tienen datos guardados en la base de datos.

### Cómo probarlo:

**Opción A: Navegador**
```
http://localhost:8000/api/v1/data/symbols
```

**Opción B: curl**
```powershell
curl http://localhost:8000/api/v1/data/symbols
```

**Respuesta esperada:**
```json
{
  "symbols": ["ES", "NQ", "EC", "6B"],
  "count": 4
}
```

**Si no hay datos:**
```json
{
  "symbols": [],
  "count": 0
}
```

**✅ Este endpoint funciona SIN IB TWS** (solo consulta la DB).

---

## 📋 Endpoint 6: `GET /api/v1/data/timeframes/{symbol}` - Listar Timeframes Disponibles

### ¿Qué hace?
Lista todos los timeframes disponibles para un símbolo específico.

### Parámetros:

| Parámetro | Tipo | Ubicación | Descripción | Ejemplo |
|-----------|------|-----------|-------------|---------|
| `symbol` | string | Path | Símbolo del instrumento | `ES`, `NQ` |

### Cómo probarlo:

**Opción A: Navegador**
```
http://localhost:8000/api/v1/data/timeframes/ES
```

**Opción B: curl**
```powershell
curl http://localhost:8000/api/v1/data/timeframes/ES
```

**Respuesta esperada:**
```json
{
  "symbol": "ES",
  "timeframes": ["1min", "5min", "15min", "30min", "1h", "4h", "1d"],
  "count": 7
}
```

**Si no hay datos para ese símbolo:**
```json
{
  "symbol": "ES",
  "timeframes": [],
  "count": 0
}
```

**✅ Este endpoint funciona SIN IB TWS** (solo consulta la DB).

---

## 🧪 Pruebas Paso a Paso

### Escenario 1: Sin IB TWS (Solo Consultas)

**Puedes probar estos endpoints sin IB TWS:**

1. **Health Check:**
   ```powershell
   curl http://localhost:8000/health
   ```
   ✅ Debería funcionar

2. **Información API:**
   ```powershell
   curl http://localhost:8000/
   ```
   ✅ Debería funcionar

3. **Listar símbolos:**
   ```powershell
   curl http://localhost:8000/api/v1/data/symbols
   ```
   ✅ Funciona (puede retornar lista vacía si no hay datos)

4. **Consultar datos (si hay datos en DB):**
   ```powershell
   curl "http://localhost:8000/api/v1/data/data/ES?timeframe=1min&limit=10"
   ```
   ✅ Funciona si hay datos, sino retorna lista vacía

---

### Escenario 2: Con IB TWS (Extracción Completa)

**Para probar extracción necesitas IB TWS:**

1. **Asegúrate de que:**
   - ✅ IB Gateway está ejecutándose
   - ✅ IB Gateway está conectado
   - ✅ API habilitada (puerto 7497)
   - ✅ `ibapi` instalado: `docker-compose exec backend pip install ibapi`

2. **Extraer datos:**
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
   ✅ Debería extraer y guardar datos

3. **Verificar que se guardaron:**
   ```powershell
   curl "http://localhost:8000/api/v1/data/symbols"
   ```
   ✅ Debería mostrar `["ES"]`

4. **Consultar los datos guardados:**
   ```powershell
   curl "http://localhost:8000/api/v1/data/data/ES?timeframe=1min&limit=10"
   ```
   ✅ Debería retornar los datos extraídos

---

## 📊 Estructura de Datos

### Modelo `MarketData` (Base de Datos):

```python
{
  "id": 1,
  "symbol": "ES",              # Símbolo (ES, NQ, EC, etc.)
  "timeframe": "1min",         # Timeframe (1min, 5min, etc.)
  "timestamp": "2024-12-02T00:00:00+00:00",  # Fecha/hora (UTC)
  "open": 4567.25,            # Precio apertura
  "high": 4568.50,            # Precio máximo
  "low": 4566.75,             # Precio mínimo
  "close": 4568.00,           # Precio cierre
  "volume": 12345,           # Volumen
  "count": 234               # Número de transacciones
}
```

---

## 🎯 Ejemplos de Uso Real

### Ejemplo 1: Extraer 1 día de datos de ES (1 minuto)

```json
POST /api/v1/data/extract
{
  "symbol": "ES",
  "duration": "1 D",
  "bar_size": "1 min",
  "num_blocks": 1,
  "save_to_db": true
}
```

**Resultado:**
- Extrae ~1440 barras (1 día × 24 horas × 60 minutos)
- Guarda en PostgreSQL
- Genera timeframes adicionales (5min, 15min, etc.) en background

---

### Ejemplo 2: Extraer 1 mes de datos (en bloques)

```json
POST /api/v1/data/extract
{
  "symbol": "ES",
  "duration": "1 M",
  "bar_size": "1 min",
  "num_blocks": 3,
  "save_to_db": true
}
```

**Resultado:**
- Extrae 3 bloques de 1 mes cada uno
- Total: ~3 meses de datos
- Guarda en PostgreSQL

---

### Ejemplo 3: Consultar últimos 100 registros de ES (5 minutos)

```
GET /api/v1/data/data/ES?timeframe=5min&limit=100
```

**Resultado:**
- Retorna los últimos 100 registros de ES en timeframe de 5 minutos
- Ordenados cronológicamente (más antiguo primero)

---

### Ejemplo 4: Consultar datos en un rango de fechas

```
GET /api/v1/data/data/ES?timeframe=1min&start_date=2024-12-01T00:00:00&end_date=2024-12-02T23:59:59&limit=1000
```

**Resultado:**
- Retorna datos de ES entre el 1 y 2 de diciembre
- Máximo 1000 registros

---

## 🔍 Verificación de Estado

### Verificar que los servicios están ejecutándose:

```powershell
docker-compose ps
```

**Debería mostrar:**
```
NAME            STATUS
g4qc_backend    Up
g4qc_postgres   Up (healthy)
g4qc_redis      Up (healthy)
```

### Ver logs del backend:

```powershell
docker-compose logs -f backend
```

### Verificar conexión a base de datos:

```powershell
docker-compose exec backend python -c "from app.core.database import engine; print('DB OK' if engine else 'DB Error')"
```

---

## 📝 Resumen de Endpoints

| Endpoint | Método | Requiere IB TWS | Requiere Datos en DB | Descripción |
|----------|--------|-----------------|----------------------|-------------|
| `/` | GET | ❌ | ❌ | Info de la API |
| `/health` | GET | ❌ | ❌ | Health check |
| `/api/v1/data/extract` | POST | ✅ | ❌ | Extraer datos desde IB |
| `/api/v1/data/data/{symbol}` | GET | ❌ | ✅ | Consultar datos históricos |
| `/api/v1/data/symbols` | GET | ❌ | ❌ | Listar símbolos |
| `/api/v1/data/timeframes/{symbol}` | GET | ❌ | ✅ | Listar timeframes |

---

## 🚀 Próximos Pasos

Una vez que tengas datos en la base de datos, puedes:
1. ✅ Consultar datos históricos
2. ✅ Ver qué símbolos y timeframes están disponibles
3. 📋 (Próximo) Hacer backtesting con esos datos
4. 📋 (Próximo) Optimizar parámetros
5. 📋 (Próximo) Analizar portfolios

---

**¿Quieres probar algún endpoint específico o necesitas ayuda con algo?**

