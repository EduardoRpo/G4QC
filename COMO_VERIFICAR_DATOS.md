# 📊 Cómo Verificar que el Scheduler Esté Guardando Datos

## 🔍 1. Verificar Ejecuciones Exitosas del Scheduler

### **A. Desde los Logs del Backend**

En el servidor, ejecuta:

```bash
cd /opt/proyectos/G4QC

# Ver logs del scheduler (últimas 100 líneas)
docker compose logs backend | grep -i "scheduler\|actualización\|completada" | tail -50

# O ver todos los logs recientes
docker compose logs backend --tail=100
```

**Busca mensajes como:**
- ✅ `✅ Actualización automática completada` → Ejecución exitosa
- ✅ `✅ Datos guardados: X registros` → Datos guardados correctamente
- ❌ `❌ Error en actualización automática` → Hubo un error
- ❌ `Connection refused` → IB Gateway no está conectado

### **B. Desde el Frontend**

En el panel **"Estado del Sistema"**:
- **Última Ejecución**: Debe mostrar la fecha/hora de la última ejecución (no "Nunca")
- **Próxima Ejecución**: Debe mostrar cuándo se ejecutará la próxima vez
- **Jobs Activos**: Debe mostrar el número de jobs programados

---

## 📈 2. Ver los Datos Guardados en la Base de Datos

### **A. Desde el Frontend (Visualización de Datos)**

1. **Selecciona un Símbolo**:
   - En la sección "Visualización de Datos" (abajo)
   - Selecciona el símbolo que configuraste en el scheduler (ej: `ES`)

2. **Selecciona un Timeframe**:
   - Selecciona el timeframe que configuraste (ej: `1min`)

3. **Haz clic en "Actualizar"**:
   - Esto recargará los datos desde la base de datos
   - Deberías ver:
     - **Registros**: Número de registros encontrados
     - **Gráfico**: Línea de precios de cierre
     - **Tabla**: Últimos 20 registros con OHLCV

**⚠️ Si no ves datos:**
- Verifica que el símbolo sea exactamente el mismo que configuraste
- Verifica que el timeframe sea correcto (ej: `1min` no `1 min`)
- Espera unos minutos después de activar el scheduler (necesita tiempo para acumular datos)

### **B. Desde la Base de Datos Directamente**

En el servidor, ejecuta:

```bash
cd /opt/proyectos/G4QC

# Conectarse a PostgreSQL
docker compose exec postgres psql -U g4qc -d g4qc_db

# Ver todos los símbolos disponibles
SELECT DISTINCT symbol FROM market_data ORDER BY symbol;

# Ver cuántos registros hay por símbolo
SELECT symbol, COUNT(*) as total_registros 
FROM market_data 
GROUP BY symbol 
ORDER BY total_registros DESC;

# Ver los últimos registros de un símbolo específico
SELECT symbol, timeframe, timestamp, open, high, low, close, volume
FROM market_data
WHERE symbol = 'ES' AND timeframe = '1min'
ORDER BY timestamp DESC
LIMIT 20;

# Ver el rango de fechas de los datos
SELECT 
    symbol,
    timeframe,
    MIN(timestamp) as fecha_inicio,
    MAX(timestamp) as fecha_fin,
    COUNT(*) as total_registros
FROM market_data
GROUP BY symbol, timeframe
ORDER BY symbol, timeframe;

# Salir de PostgreSQL
\q
```

### **C. Desde la API Directamente**

Puedes probar los endpoints directamente:

```bash
# Ver todos los símbolos disponibles
curl http://45.137.192.196:8000/api/v1/data/symbols

# Ver timeframes disponibles para un símbolo
curl http://45.137.192.196:8000/api/v1/data/timeframes/ES

# Ver datos de un símbolo específico
curl "http://45.137.192.196:8000/api/v1/data/data/ES?timeframe=1min&limit=10"
```

---

## 🎯 3. Por Qué Puede No Mostrarse la Gráfica

### **Problema 1: No hay datos en la base de datos**

**Causas posibles:**
- El scheduler no se ha ejecutado aún (espera al próximo intervalo)
- Hubo errores en las ejecuciones (revisa los logs)
- IB Gateway no está conectado
- El símbolo o timeframe no coincide

**Solución:**
1. Revisa los logs: `docker compose logs backend | grep -i error`
2. Verifica que IB Gateway esté corriendo: `docker compose ps ibgateway`
3. Haz una extracción manual primero para verificar que funciona

### **Problema 2: El símbolo o timeframe no coincide**

**Importante:**
- El símbolo debe ser **exactamente igual** (mayúsculas/minúsculas)
- El timeframe debe coincidir exactamente:
  - Si configuraste `1min` en el scheduler, busca `1min` (no `1 min`)
  - Si configuraste `5min`, busca `5min`

**Solución:**
1. Verifica qué símbolos hay en la BD:
   ```bash
   docker compose exec postgres psql -U g4qc -d g4qc_db -c "SELECT DISTINCT symbol FROM market_data;"
   ```

2. Verifica qué timeframes hay para ese símbolo:
   ```bash
   docker compose exec postgres psql -U g4qc -d g4qc_db -c "SELECT DISTINCT timeframe FROM market_data WHERE symbol = 'ES';"
   ```

### **Problema 3: Los datos están en otro timeframe**

El scheduler guarda datos en el timeframe que configuraste. Si configuraste `1min`, los datos estarán en `1min`, no en `5min` o `1hour`.

**Solución:**
- Selecciona el timeframe correcto en el selector del frontend
- O verifica qué timeframes están disponibles para ese símbolo

### **Problema 4: El frontend no está cargando los datos**

**Solución:**
1. Abre la consola del navegador (F12)
2. Busca errores en la pestaña "Console"
3. Busca errores en la pestaña "Network" cuando haces clic en "Actualizar"
4. Verifica que la URL del API sea correcta: `http://45.137.192.196:8000`

---

## 🧪 4. Prueba Rápida: Verificar que Todo Funciona

### **Paso 1: Hacer una Extracción Manual**

1. En el frontend, ve a "Extracción Manual de Datos"
2. Configura:
   - Símbolo: `ES`
   - Duración: `1 Día`
   - Tamaño de Barra: `1 minuto`
   - Bloques: `1`
   - Mes de Contrato: `202512`
3. Haz clic en "Extraer Datos"
4. Deberías ver: "Extracción completada: X registros guardados"

### **Paso 2: Verificar en la Visualización**

1. Ve a "Visualización de Datos"
2. Selecciona símbolo: `ES`
3. Selecciona timeframe: `1min`
4. Haz clic en "Actualizar"
5. Deberías ver:
   - **Registros**: Número > 0
   - **Gráfico**: Línea de precios
   - **Tabla**: Datos OHLCV

### **Paso 3: Verificar en la Base de Datos**

```bash
docker compose exec postgres psql -U g4qc -d g4qc_db -c "SELECT COUNT(*) FROM market_data WHERE symbol = 'ES' AND timeframe = '1min';"
```

Debería mostrar un número > 0.

---

## 📋 5. Checklist de Verificación

Usa este checklist para verificar que todo funciona:

- [ ] **Scheduler está activo**: Panel "Estado del Sistema" muestra "Activo" (verde)
- [ ] **Última ejecución**: Muestra una fecha/hora (no "Nunca")
- [ ] **Próxima ejecución**: Muestra una fecha/hora futura
- [ ] **Logs sin errores**: `docker compose logs backend | grep -i error` no muestra errores recientes
- [ ] **Datos en BD**: `SELECT COUNT(*) FROM market_data WHERE symbol = 'ES';` > 0
- [ ] **Símbolo disponible**: Aparece en el selector de "Visualización de Datos"
- [ ] **Timeframe disponible**: Aparece en el selector de timeframe
- [ ] **Gráfico muestra datos**: Se ve una línea de precios
- [ ] **Tabla muestra datos**: Se ven filas con datos OHLCV

---

## 🔧 6. Solución de Problemas Comunes

### **Problema: "No hay datos disponibles para ES (1min)"**

**Posibles causas:**
1. El scheduler no se ha ejecutado aún
2. Hubo errores en las ejecuciones
3. El símbolo o timeframe no coincide

**Solución:**
```bash
# 1. Verificar si hay datos en la BD
docker compose exec postgres psql -U g4qc -d g4qc_db -c "SELECT COUNT(*) FROM market_data;"

# 2. Ver qué símbolos hay
docker compose exec postgres psql -U g4qc -d g4qc_db -c "SELECT DISTINCT symbol FROM market_data;"

# 3. Ver logs del scheduler
docker compose logs backend | grep -i "scheduler\|actualización" | tail -20
```

### **Problema: El gráfico está vacío pero hay registros**

**Causa:** El formato de los datos puede estar incorrecto

**Solución:**
1. Verifica en la consola del navegador (F12) si hay errores
2. Verifica que los datos tengan el formato correcto:
   ```bash
   docker compose exec postgres psql -U g4qc -d g4qc_db -c "SELECT timestamp, open, high, low, close, volume FROM market_data WHERE symbol = 'ES' LIMIT 5;"
   ```

### **Problema: Los datos no se actualizan automáticamente**

**Causa:** El frontend no está recargando automáticamente

**Solución:**
- Haz clic manualmente en "Actualizar" en la sección "Visualización de Datos"
- El frontend no se actualiza automáticamente, necesitas hacer clic en "Actualizar" para ver los nuevos datos

---

## 💡 7. Tips Importantes

1. **El scheduler guarda datos en el timeframe configurado**: Si configuraste `1min`, busca `1min` en la visualización

2. **Los datos se acumulan con el tiempo**: Después de activar el scheduler, espera unos minutos para que se acumulen datos

3. **La visualización muestra los últimos 50 registros en el gráfico** y los últimos 20 en la tabla

4. **Puedes verificar directamente en la BD** si tienes dudas sobre qué datos hay guardados

5. **Los logs son tu mejor amigo**: Siempre revisa los logs si algo no funciona

---

## 📞 Si Nada Funciona

1. **Revisa los logs completos**:
   ```bash
   docker compose logs backend --tail=200
   ```

2. **Verifica que IB Gateway esté corriendo**:
   ```bash
   docker compose ps ibgateway
   ```

3. **Haz una extracción manual** para verificar que la conexión funciona

4. **Verifica la base de datos directamente** para ver si hay datos

5. **Comparte los logs y el resultado de las consultas SQL** para diagnóstico

