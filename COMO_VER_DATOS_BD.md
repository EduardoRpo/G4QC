# 📊 Cómo Ver los Datos en la Base de Datos

## ✅ Estado Actual

Has extraído exitosamente:
- **1,380 registros** del símbolo **ES**
- Rango de fechas: **5 de diciembre 2025** (00:00 - 22:59)
- Datos guardados en PostgreSQL

---

## 🎯 Opción 1: Usar los Endpoints de la API (Más Fácil)

### 1.1 Ver los últimos 10 registros

**En Swagger UI:**
1. Abre: `http://TU_IP_SERVIDOR:8000/docs`
2. Busca: `GET /api/v1/data/data/{symbol}`
3. Haz clic en "Try it out"
4. Ingresa:
   - `symbol`: `ES`
   - `timeframe`: `1min`
   - `limit`: `10`
5. Haz clic en "Execute"

**O directamente en el navegador:**
```
http://TU_IP_SERVIDOR:8000/api/v1/data/data/ES?timeframe=1min&limit=10
```

**O con curl:**
```bash
curl "http://TU_IP_SERVIDOR:8000/api/v1/data/data/ES?timeframe=1min&limit=10"
```

### 1.2 Ver más registros (los primeros 100)

```
http://TU_IP_SERVIDOR:8000/api/v1/data/data/ES?timeframe=1min&limit=100
```

### 1.3 Ver los símbolos disponibles

```
http://TU_IP_SERVIDOR:8000/api/v1/data/symbols
```

### 1.4 Ver los timeframes disponibles para ES

```
http://TU_IP_SERVIDOR:8000/api/v1/data/timeframes/ES
```

---

## 🗄️ Opción 2: Consultar Directamente PostgreSQL

### 2.1 Conectarse a PostgreSQL

Desde el servidor:

```bash
# Opción A: Desde el contenedor de postgres
docker compose exec postgres psql -U g4qc -d g4qc_db

# Opción B: Usando psql desde el backend
docker compose exec backend psql postgresql://g4qc:g4qc_dev@postgres:5432/g4qc_db
```

### 2.2 Consultas SQL Útiles

Una vez conectado a PostgreSQL, ejecuta estas consultas:

```sql
-- Ver cuántos registros hay en total
SELECT COUNT(*) FROM market_data;

-- Ver los últimos 10 registros
SELECT * FROM market_data 
WHERE symbol = 'ES' 
ORDER BY timestamp DESC 
LIMIT 10;

-- Ver el rango de fechas de los datos
SELECT 
    MIN(timestamp) as fecha_inicio,
    MAX(timestamp) as fecha_fin,
    COUNT(*) as total_registros
FROM market_data 
WHERE symbol = 'ES';

-- Ver estadísticas por símbolo
SELECT 
    symbol,
    timeframe,
    COUNT(*) as registros,
    MIN(timestamp) as primera_fecha,
    MAX(timestamp) as ultima_fecha
FROM market_data
GROUP BY symbol, timeframe
ORDER BY symbol, timeframe;

-- Ver los primeros registros del día
SELECT * FROM market_data 
WHERE symbol = 'ES' 
  AND timestamp >= '2025-12-05 00:00:00'
ORDER BY timestamp ASC 
LIMIT 20;

-- Ver los últimos registros del día
SELECT * FROM market_data 
WHERE symbol = 'ES' 
  AND timestamp <= '2025-12-05 23:59:59'
ORDER BY timestamp DESC 
LIMIT 20;

-- Ver un resumen estadístico
SELECT 
    symbol,
    COUNT(*) as total_registros,
    MIN(open) as precio_minimo,
    MAX(high) as precio_maximo,
    AVG(close) as precio_promedio,
    SUM(volume) as volumen_total
FROM market_data
WHERE symbol = 'ES'
GROUP BY symbol;
```

### 2.3 Salir de PostgreSQL

```sql
\q
```

---

## 📋 Opción 3: Script de Consulta Rápida

Puedes crear este script para ver los datos fácilmente:

```bash
#!/bin/bash
# ver_datos.sh - Ver datos de la base de datos

echo "============================================================"
echo "📊 Resumen de Datos en la Base de Datos"
echo "============================================================"
echo ""

docker compose exec -T postgres psql -U g4qc -d g4qc_db << EOF

-- Resumen general
SELECT 
    'Total registros: ' || COUNT(*)::text as info
FROM market_data;

SELECT 
    'Símbolos: ' || STRING_AGG(DISTINCT symbol, ', ') as info
FROM market_data;

SELECT 
    'Timeframes: ' || STRING_AGG(DISTINCT timeframe, ', ') as info
FROM market_data;

-- Detalles por símbolo
SELECT 
    symbol,
    timeframe,
    COUNT(*) as registros,
    MIN(timestamp) as primera_fecha,
    MAX(timestamp) as ultima_fecha
FROM market_data
GROUP BY symbol, timeframe
ORDER BY symbol, timeframe;

-- Últimos 5 registros
SELECT 
    timestamp,
    open,
    high,
    low,
    close,
    volume
FROM market_data
ORDER BY timestamp DESC
LIMIT 5;

EOF
```

---

## 🧪 Ejemplos Prácticos

### Ejemplo 1: Ver los últimos 20 registros del día

**Navegador:**
```
http://TU_IP_SERVIDOR:8000/api/v1/data/data/ES?timeframe=1min&limit=20
```

**SQL:**
```sql
SELECT * FROM market_data 
WHERE symbol = 'ES' 
ORDER BY timestamp DESC 
LIMIT 20;
```

### Ejemplo 2: Ver datos de una hora específica

**API (con filtros de fecha):**
```
http://TU_IP_SERVIDOR:8000/api/v1/data/data/ES?timeframe=1min&start_date=2025-12-05T09:00:00&end_date=2025-12-05T10:00:00
```

**SQL:**
```sql
SELECT * FROM market_data 
WHERE symbol = 'ES'
  AND timestamp >= '2025-12-05 09:00:00'
  AND timestamp < '2025-12-05 10:00:00'
ORDER BY timestamp ASC;
```

### Ejemplo 3: Ver estadísticas de precios

**SQL:**
```sql
SELECT 
    DATE_TRUNC('hour', timestamp) as hora,
    COUNT(*) as barras,
    MIN(low) as precio_minimo,
    MAX(high) as precio_maximo,
    AVG(close) as precio_promedio,
    SUM(volume) as volumen_total
FROM market_data
WHERE symbol = 'ES'
  AND timestamp >= '2025-12-05 00:00:00'
GROUP BY DATE_TRUNC('hour', timestamp)
ORDER BY hora;
```

---

## 📊 Estructura de la Tabla

Los datos se guardan en la tabla `market_data` con esta estructura:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id` | Integer | ID único del registro |
| `symbol` | String | Símbolo (ES, NQ, etc.) |
| `timeframe` | String | Timeframe (1min, 5min, etc.) |
| `timestamp` | Timestamp | Fecha y hora (UTC) |
| `open` | Float | Precio de apertura |
| `high` | Float | Precio máximo |
| `low` | Float | Precio mínimo |
| `close` | Float | Precio de cierre |
| `volume` | Integer | Volumen |
| `count` | Integer | Cantidad de trades |

---

## 🚀 Comandos Rápidos

### Desde el servidor:

```bash
# Ver resumen rápido
docker compose exec -T postgres psql -U g4qc -d g4qc_db -c "SELECT symbol, COUNT(*) FROM market_data GROUP BY symbol;"

# Ver últimos 5 registros
docker compose exec -T postgres psql -U g4qc -d g4qc_db -c "SELECT * FROM market_data ORDER BY timestamp DESC LIMIT 5;"

# Ver rango de fechas
docker compose exec -T postgres psql -U g4qc -d g4qc_db -c "SELECT MIN(timestamp), MAX(timestamp), COUNT(*) FROM market_data WHERE symbol='ES';"
```

---

## 💡 Consejos

1. **Usa los endpoints de la API** para consultas rápidas y estructuradas
2. **Usa SQL directo** para consultas complejas o análisis
3. **Los datos están en UTC**, tenlo en cuenta al filtrar por fechas
4. **Los timeframes adicionales** (5min, 15min, etc.) se generan automáticamente en background si extrajiste con "1min"

---

## ✅ Verificación Rápida

Para verificar rápidamente que los datos están guardados:

```bash
# Desde el servidor
curl http://TU_IP_SERVIDOR:8000/api/v1/data/symbols
```

Deberías ver:
```json
{
  "symbols": ["ES"],
  "count": 1
}
```

