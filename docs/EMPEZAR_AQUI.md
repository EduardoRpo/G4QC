# 🚀 EMPEZAR AQUÍ - Pasos Exactos para Probar

## ⚡ Pasos Rápidos (En Orden)

### Paso 1: Verificar que tienes Docker (1 minuto)

Abre PowerShell y ejecuta:
```powershell
docker --version
docker-compose --version
```

Si no tienes Docker instalado, descárgalo de: https://www.docker.com/products/docker-desktop

---

### Paso 2: Ir al directorio del proyecto

```powershell
cd C:\D\Trabajo\G4QC\G4QC
```

---

### Paso 3: Iniciar los servicios con Docker

```powershell
docker-compose up -d
```

**Esto iniciará:**
- PostgreSQL (puerto 5432)
- Redis (puerto 6379)  
- Backend API (puerto 8000)

**Espera 30 segundos** para que todo se inicie.

---

### Paso 4: Verificar que los servicios están corriendo

```powershell
docker-compose ps
```

Deberías ver 3 servicios con estado "Up":
- ✅ g4qc_postgres
- ✅ g4qc_redis
- ✅ g4qc_backend

Si alguno no está "Up", revisa los logs:
```powershell
docker-compose logs nombre_del_servicio
```

---

### Paso 5: Inicializar la base de datos

```powershell
docker-compose exec backend alembic upgrade head
```

Esto creará las tablas necesarias. Deberías ver mensajes como:
- `Running upgrade  -> 001, Initial migration...`
- `INFO [alembic.runtime.migration] Running upgrade ...`

---

### Paso 6: Probar que la API funciona

**Opción A: Abrir en el navegador**
```
http://localhost:8000/docs
```

Deberías ver la documentación interactiva de la API (Swagger UI).

**Opción B: Probar con PowerShell**

```powershell
Invoke-WebRequest -Uri http://localhost:8000/health
```

Debería retornar algo como:
```
StatusCode        : 200
Content           : {"status":"healthy"}
```

---

## 🎉 ¡Ya puedes usar la API!

### Probar los endpoints disponibles:

#### 1. Ver documentación completa:
Abre: **http://localhost:8000/docs**

#### 2. Listar símbolos (vacío inicialmente):
```powershell
Invoke-WebRequest -Uri http://localhost:8000/api/v1/data/symbols
```

#### 3. Health check:
```powershell
Invoke-WebRequest -Uri http://localhost:8000/health
```

---

## 📊 Probar Extracción de Datos (Opcional - Requiere IB TWS)

**IMPORTANTE:** Solo funciona si tienes Interactive Brokers TWS o IB Gateway ejecutándose.

### Antes de probar:
1. Abre **Interactive Brokers TWS** o **IB Gateway**
2. Configúralo para **Paper Trading** (puerto 7497) o Live (7496)
3. Asegúrate de que esté **conectado**

### Extraer datos de prueba:

```powershell
$body = @{
    symbol = "ES"
    duration = "3600 S"
    bar_size = "1 min"
    num_blocks = 1
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/v1/data/extract" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

Si funciona, deberías ver una respuesta con:
- `"status": "success"`
- Número de registros extraídos
- Rango de fechas

---

## 🔍 Ver Logs si algo falla

### Ver todos los logs:
```powershell
docker-compose logs -f
```

### Ver solo logs del backend:
```powershell
docker-compose logs -f backend
```

### Ver solo logs de PostgreSQL:
```powershell
docker-compose logs -f postgres
```

---

## 🛑 Detener los servicios

Cuando termines de probar:
```powershell
docker-compose down
```

Para detener y eliminar volúmenes:
```powershell
docker-compose down -v
```

---

## ❌ Solución de Problemas

### Error: "Cannot connect to Docker daemon"
- **Solución**: Abre Docker Desktop y espera a que inicie completamente.

### Error: "Port already in use"
- **Solución**: Algo está usando el puerto 8000, 5432 o 6379. Detén esos servicios o cambia los puertos en `docker-compose.yml`.

### Error: "Module not found" en el backend
- **Solución**: 
```powershell
docker-compose exec backend pip install -r requirements.txt
```

### Backend no inicia
```powershell
docker-compose logs backend
# Revisa los errores y compártelos para ayuda
```

---

## ✅ Checklist de Verificación

Marca cuando completes cada paso:

- [ ] Docker está instalado y corriendo
- [ ] `docker-compose up -d` ejecutado sin errores
- [ ] Los 3 servicios están "Up" (`docker-compose ps`)
- [ ] Migraciones aplicadas (`alembic upgrade head`)
- [ ] `/docs` se abre en el navegador
- [ ] Health check retorna `{"status":"healthy"}`
- [ ] (Opcional) Extracción de datos funciona

---

## 📚 Próximos Pasos

Una vez que todo funciona:

1. ✅ Explorar la documentación en `/docs`
2. ✅ Probar todos los endpoints desde la interfaz web
3. ✅ Extraer datos de múltiples símbolos
4. 🚧 Implementar frontend React
5. 🚧 Agregar motor de backtesting

---

## 💡 Tips

- **Usa la interfaz `/docs`**: Es la forma más fácil de probar la API, puedes hacer requests directamente desde el navegador
- **Los logs son tus amigos**: Si algo falla, siempre revisa `docker-compose logs`
- **No necesitas IB TWS para probar**: La API funciona sin IB, solo algunos endpoints requieren datos previos

---

**¿Tienes algún error?** Compárteme el mensaje exacto y te ayudo a resolverlo.

