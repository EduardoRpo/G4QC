# 🚀 Levantar Servicios G4QC - Pasos Siguientes

## ✅ Instalación Completada

Ahora que Docker y Docker Compose están instalados, es momento de levantar los servicios.

## 📝 Pasos a Ejecutar (en orden)

### Paso 1: Verificar que estás en el directorio correcto

```bash
cd /opt/proyectos/G4QC
pwd  # Debe mostrar: /opt/proyectos/G4QC
```

### Paso 2: Levantar los servicios con Docker Compose

```bash
docker compose up -d
```

Esto iniciará:
- **PostgreSQL** (TimescaleDB) en el puerto 5432
- **Redis** en el puerto 6379  
- **Backend API** en el puerto 8000

**Nota**: La primera vez puede tardar varios minutos mientras descarga las imágenes y construye el contenedor del backend.

### Paso 3: Verificar que los servicios están corriendo

```bash
docker compose ps
```

Deberías ver 3 servicios con estado "Up":
- g4qc_postgres
- g4qc_redis
- g4qc_backend

### Paso 4: Ver los logs (opcional pero recomendado)

```bash
# Ver todos los logs
docker compose logs -f

# O ver logs de un servicio específico
docker compose logs -f backend
docker compose logs -f postgres
```

**Tip**: Presiona `Ctrl+C` para salir de los logs.

### Paso 5: Esperar a que PostgreSQL esté completamente listo

```bash
# Esperar unos segundos y verificar que PostgreSQL responda
sleep 10
docker compose exec postgres pg_isready -U g4qc
```

Debería mostrar: `/var/run/postgresql/.s.PGSQL.5432: accepting connections`

### Paso 6: Aplicar migraciones de base de datos

```bash
docker compose exec backend alembic upgrade head
```

Esto creará las tablas necesarias en la base de datos.

### Paso 7: Verificar que la API funciona

```bash
# Health check
curl http://localhost:8000/health

# Debe responder: {"status":"healthy"}
```

### Paso 8: Acceder a la documentación (desde navegador)

Abre en tu navegador:
- **API**: http://45.137.192.196:8000
- **Documentación interactiva**: http://45.137.192.196:8000/docs

## 🔧 Comandos Útiles

### Ver estado de los servicios
```bash
docker compose ps
```

### Ver logs en tiempo real
```bash
docker compose logs -f
```

### Reiniciar un servicio específico
```bash
docker compose restart backend
```

### Detener todos los servicios
```bash
docker compose down
```

### Detener y eliminar volúmenes (¡CUIDADO! Elimina datos)
```bash
docker compose down -v
```

### Entrar al contenedor del backend
```bash
docker compose exec backend bash
```

## ⚠️ Solución de Problemas

### Si un servicio no inicia:

1. **Ver logs del servicio:**
   ```bash
   docker compose logs backend
   ```

2. **Verificar recursos del sistema:**
   ```bash
   df -h  # Espacio en disco
   free -h  # Memoria
   ```

3. **Verificar puertos:**
   ```bash
   netstat -tulpn | grep -E ":(5432|6379|8000)"
   ```

### Si el backend falla al iniciar:

- Puede ser que falten dependencias
- Verifica los logs: `docker compose logs backend`
- Verifica que el Dockerfile esté correcto

### Si PostgreSQL no responde:

- Espera un poco más (puede tardar en inicializarse)
- Verifica logs: `docker compose logs postgres`
- Verifica el healthcheck: `docker compose ps postgres`

## ✅ Verificación Final

Después de seguir estos pasos, deberías tener:

- ✅ Todos los servicios corriendo
- ✅ Base de datos con tablas creadas
- ✅ API respondiendo en http://45.137.192.196:8000
- ✅ Documentación accesible en http://45.137.192.196:8000/docs

---

**¡Listo para empezar!** 🎉

