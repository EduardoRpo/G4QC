# 🎯 COMENZAR AQUÍ - Pasos Inmediatos

## ✅ Resumen: Qué tienes listo

- ✅ Backend FastAPI funcionando
- ✅ Endpoints de extracción y consulta de datos
- ✅ Base de datos configurada
- ✅ Servicio IB refactorizado

## 🚀 Pasos para Probar (En Orden)

### 1️⃣ Iniciar Servicios (5 minutos)

```powershell
# Ir al directorio del proyecto
cd C:\D\Trabajo\G4QC\G4QC

# Iniciar Docker Compose
docker-compose up -d

# Verificar que todo esté funcionando
docker-compose ps
```

**Deberías ver 3 servicios:**
- ✅ g4qc_postgres (PostgreSQL)
- ✅ g4qc_redis (Redis)  
- ✅ g4qc_backend (Backend API)

### 2️⃣ Inicializar Base de Datos (2 minutos)

```powershell
# Aplicar migraciones para crear tablas
docker-compose exec backend alembic upgrade head
```

### 3️⃣ Probar que Funciona (1 minuto)

**Abre en tu navegador:**
```
http://localhost:8000/docs
```

Verás la documentación interactiva de la API.

**O prueba el health check:**
```powershell
Invoke-WebRequest http://localhost:8000/health
```

**Debería retornar:** `{"status":"healthy"}`

### 4️⃣ Probar Endpoints Sin IB (Opcional - No requiere TWS)

```powershell
# Listar símbolos (vacío inicialmente)
Invoke-WebRequest http://localhost:8000/api/v1/data/symbols
```

**Debería retornar:** `{"symbols":[],"count":0}`

### 5️⃣ Probar Extracción de Datos (Requiere IB TWS)

**Antes:** Abre Interactive Brokers TWS/Gateway

```powershell
$body = '{
    "symbol": "ES",
    "duration": "3600 S",
    "bar_size": "1 min",
    "num_blocks": 1
}'

Invoke-WebRequest -Uri "http://localhost:8000/api/v1/data/extract" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

---

## 📚 Documentación Completa

Para más detalles, ver: **`GUIA_PRIMEROS_PASOS.md`**

---

## ⚠️ Problemas Comunes

**Error al iniciar Docker:**
```powershell
docker-compose logs -f
```

**Backend no inicia:**
```powershell
docker-compose logs backend
```

**No se puede conectar a IB:**
- Verifica que TWS/Gateway esté abierto
- Verifica puerto 7497 (paper) o 7496 (live)
- Verifica configuración API en TWS

---

## 🎉 ¡Listo!

Una vez que veas la documentación en `/docs`, ya puedes:
1. Probar todos los endpoints desde la interfaz web
2. Ver la estructura de requests/responses
3. Probar extraer datos (si tienes IB TWS)

**Siguiente paso:** Ver `GUIA_PRIMEROS_PASOS.md` para pruebas más detalladas.

