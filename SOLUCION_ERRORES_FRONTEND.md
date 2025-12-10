# 🔧 Solución de Errores del Frontend

## 🚨 Problemas Comunes y Soluciones

### **Error 1: "Error al activar el scheduler"**
### **Error 2: "Error al actualizar la configuración"**
### **Error 3: "0 registros guardados" en extracción manual**

---

## 📋 Pasos de Diagnóstico

### **Paso 1: Verificar que el Backend esté corriendo**

En el servidor, ejecuta:

```bash
cd /opt/proyectos/G4QC
docker compose ps
```

Debes ver:
- ✅ `g4qc_backend` - Status: `Up`
- ✅ `g4qc_postgres` - Status: `Up (healthy)`
- ✅ `g4qc_redis` - Status: `Up (healthy)`
- ✅ `g4qc_ibgateway` - Status: `Up`

Si algún contenedor no está corriendo:

```bash
docker compose up -d
```

---

### **Paso 2: Verificar logs del Backend**

```bash
docker compose logs backend --tail=50
```

**Busca errores como:**
- ❌ `Connection refused` → IB Gateway no está corriendo
- ❌ `Database connection error` → Problema con PostgreSQL
- ❌ `Module not found` → Faltan dependencias
- ❌ `Scheduler initialization error` → Error al inicializar el scheduler

---

### **Paso 3: Verificar que el Backend responda**

Abre en tu navegador:
- **API Docs**: `http://45.137.192.196:8000/docs`
- **Health Check**: `http://45.137.192.196:8000/health`

Si no responde, el backend no está accesible.

---

### **Paso 4: Verificar conexión con IB Gateway**

```bash
docker compose logs ibgateway --tail=20
```

Debe mostrar que IB Gateway está corriendo y escuchando en el puerto 4000 (interno).

**Verificar desde el backend:**

```bash
docker compose exec backend python -c "
from app.core.config import settings
print(f'IB_HOST: {settings.IB_HOST}')
print(f'IB_PORT: {settings.IB_PORT}')
"
```

Debe mostrar:
```
IB_HOST: ibgateway
IB_PORT: 4000
```

---

### **Paso 5: Verificar la Base de Datos**

```bash
docker compose exec backend python -c "
from app.core.database import SessionLocal
from app.models.data import MarketData
db = SessionLocal()
try:
    count = db.query(MarketData).count()
    print(f'✅ Base de datos conectada. Registros: {count}')
except Exception as e:
    print(f'❌ Error: {e}')
finally:
    db.close()
"
```

---

### **Paso 6: Verificar logs del Frontend**

Abre la consola del navegador (F12) y busca:
- 🔧 `API Base URL: http://45.137.192.196:8000` (debe aparecer al cargar)
- ❌ Errores de red (CORS, conexión rechazada, timeout)

---

## 🔨 Soluciones por Problema

### **Problema: Backend no responde**

**Solución:**

```bash
cd /opt/proyectos/G4QC
docker compose restart backend
docker compose logs backend --tail=50
```

Si sigue sin funcionar:

```bash
docker compose down
docker compose up -d --build
```

---

### **Problema: IB Gateway no está conectado**

**Solución:**

1. Verificar que IB Gateway esté corriendo:
```bash
docker compose ps ibgateway
```

2. Si no está corriendo:
```bash
docker compose up -d ibgateway
docker compose logs ibgateway --tail=50
```

3. Esperar 30-60 segundos para que IB Gateway se inicie completamente.

4. Verificar desde el backend:
```bash
docker compose exec backend python -c "
from app.services.data_extraction.ib_extractor import IBDataExtractor
extractor = IBDataExtractor()
try:
    extractor.connect()
    print('✅ Conectado a IB Gateway')
    extractor.disconnect()
except Exception as e:
    print(f'❌ Error: {e}')
"
```

---

### **Problema: Base de datos no conectada**

**Solución:**

1. Verificar que PostgreSQL esté corriendo:
```bash
docker compose ps postgres
```

2. Si no está corriendo:
```bash
docker compose up -d postgres
```

3. Verificar migraciones:
```bash
docker compose exec backend alembic upgrade head
```

4. Si hay errores, inicializar la BD:
```bash
docker compose exec backend python scripts/init_db.py
```

---

### **Problema: Scheduler no se inicializa**

**Solución:**

1. Verificar logs del backend al iniciar:
```bash
docker compose logs backend | grep -i scheduler
```

2. Si hay errores, reiniciar el backend:
```bash
docker compose restart backend
docker compose logs backend --tail=100
```

3. Verificar que el scheduler se pueda crear:
```bash
docker compose exec backend python -c "
from app.core.database import SessionLocal
from app.services.scheduler.data_scheduler import DataScheduler
db = SessionLocal()
try:
    scheduler = DataScheduler(db)
    status = scheduler.get_status()
    print('✅ Scheduler creado correctamente')
    print(f'Estado: {status}')
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
finally:
    db.close()
"
```

---

### **Problema: Frontend no puede conectar al Backend**

**Solución:**

1. **Verificar la URL del API en el frontend:**
   - Abre la consola del navegador (F12)
   - Busca: `🔧 API Base URL: ...`
   - Debe ser: `http://45.137.192.196:8000`

2. **Si la URL es incorrecta:**
   - Reconstruir el frontend:
   ```bash
   cd /opt/proyectos/G4QC
   docker compose build frontend
   docker compose up -d frontend
   ```

3. **Verificar CORS:**
   - El backend debe permitir `http://45.137.192.196:5173`
   - Verificar en `backend/app/core/config.py` que `CORS_ORIGINS` incluya esta URL

---

### **Problema: "0 registros guardados" en extracción manual**

**Posibles causas:**

1. **IB Gateway no está conectado:**
   - Verificar logs: `docker compose logs backend | grep -i "ib\|connection"`
   - Verificar que IB Gateway esté corriendo: `docker compose ps ibgateway`

2. **Símbolo incorrecto o contract_month inválido:**
   - Para futuros (ES, NQ): requiere `contract_month` válido (ej: `202512`)
   - Para ETFs (SPY, QQQ): no requiere `contract_month`
   - Para Forex (EURUSD): no requiere `contract_month`

3. **No hay datos disponibles para ese período:**
   - IB Gateway puede no tener datos históricos para ese símbolo/período
   - Intentar con un período más reciente (ej: `1 D` en lugar de `1 M`)

4. **Error en la extracción:**
   - Verificar logs del backend:
   ```bash
   docker compose logs backend --tail=100 | grep -i "extract\|error"
   ```

---

## 🧪 Pruebas Rápidas

### **Test 1: Health Check del Backend**

```bash
curl http://45.137.192.196:8000/health
```

Debe responder: `{"status":"healthy"}`

---

### **Test 2: Estado del Scheduler**

```bash
curl http://45.137.192.196:8000/api/v1/scheduler/status
```

Debe responder con el estado del scheduler en JSON.

---

### **Test 3: Extracción Manual (desde terminal)**

```bash
curl -X POST http://45.137.192.196:8000/api/v1/data/extract \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "ES",
    "duration": "1 D",
    "bar_size": "1 min",
    "num_blocks": 1,
    "contract_month": "202512"
  }'
```

Si funciona desde terminal pero no desde el frontend, el problema es de CORS o de la URL del frontend.

---

## 📝 Checklist de Verificación

Antes de reportar un problema, verifica:

- [ ] Backend está corriendo (`docker compose ps`)
- [ ] Backend responde (`http://45.137.192.196:8000/health`)
- [ ] IB Gateway está corriendo (`docker compose ps ibgateway`)
- [ ] PostgreSQL está corriendo (`docker compose ps postgres`)
- [ ] Frontend muestra la URL correcta del API en la consola
- [ ] No hay errores en los logs del backend
- [ ] No hay errores de CORS en la consola del navegador
- [ ] El símbolo y parámetros son correctos

---

## 🆘 Si Nada Funciona

1. **Reiniciar todo:**
```bash
cd /opt/proyectos/G4QC
docker compose down
docker compose up -d --build
```

2. **Esperar 1-2 minutos** para que todos los servicios se inicien

3. **Verificar logs:**
```bash
docker compose logs --tail=50
```

4. **Probar desde la API directamente:**
   - Abre `http://45.137.192.196:8000/docs`
   - Prueba los endpoints manualmente

---

## 📞 Información para Reportar Problemas

Si necesitas ayuda, proporciona:

1. **Salida de:**
   ```bash
   docker compose ps
   docker compose logs backend --tail=100
   docker compose logs frontend --tail=50
   ```

2. **Screenshot de la consola del navegador** (F12 → Console)

3. **URL exacta** que estás usando para acceder al frontend

4. **Mensaje de error exacto** que aparece en el frontend

