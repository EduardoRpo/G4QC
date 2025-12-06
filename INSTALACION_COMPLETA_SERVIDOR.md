# Guía de Instalación Completa - Servidor G4QC

## 📋 Estado Actual del Servidor

Basado en la revisión realizada:

- ✅ Proyecto encontrado en `/opt/proyectos/G4QC`
- ✅ `docker-compose.yml` existe y está correcto
- ✅ Estructura del backend completa
- ❌ Docker NO está instalado
- ❌ Docker Compose NO está instalado
- ❌ Archivo `.env` no existe (pero no es crítico, docker-compose tiene las variables)

## 🚀 Instalación Paso a Paso

### Opción 1: Instalación Automática (Recomendada)

1. **Conectarse al servidor:**
   ```bash
   ssh root@45.137.192.196
   # Contraseña: G4QC2026
   ```

2. **Ir al directorio del proyecto:**
   ```bash
   cd /opt/proyectos/G4QC
   ```

3. **Ejecutar el script de instalación:**
   ```bash
   bash instalar_en_servidor.sh
   ```

   El script instalará:
   - Docker Engine
   - Docker Compose (plugin o standalone)
   - Creará el archivo `.env` si no existe
   - Verificará la estructura del proyecto

### Opción 2: Instalación Manual

#### Paso 1: Instalar Docker

```bash
# Actualizar paquetes
apt update

# Instalar dependencias
apt install -y ca-certificates curl gnupg lsb-release

# Agregar clave GPG de Docker
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Configurar repositorio
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Iniciar y habilitar Docker
systemctl start docker
systemctl enable docker

# Verificar instalación
docker --version
docker compose version
```

#### Paso 2: Verificar Docker Compose

Si `docker compose version` funciona, ya está listo. Si no:

```bash
# Instalar docker-compose standalone
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

#### Paso 3: Crear archivo .env

```bash
cd /opt/proyectos/G4QC

# Si existe .env.example, copiarlo
if [ -f backend/.env.example ]; then
    cp backend/.env.example backend/.env
else
    # Crear .env básico
    cat > backend/.env << EOF
DEBUG=False
DATABASE_URL=postgresql://g4qc:g4qc_dev@postgres:5432/g4qc_db
REDIS_URL=redis://redis:6379
IB_HOST=127.0.0.1
IB_PORT=7497
IB_CLIENT_ID=1
EOF
fi

# Editar si es necesario
nano backend/.env
```

## 🎯 Después de la Instalación

### 1. Levantar los Servicios

```bash
cd /opt/proyectos/G4QC

# Levantar todos los servicios
docker compose up -d

# O si usas docker-compose (con guión):
docker-compose up -d
```

Esto iniciará:
- **PostgreSQL** (TimescaleDB) en el puerto 5432
- **Redis** en el puerto 6379
- **Backend API** en el puerto 8000

### 2. Verificar que los Servicios Estén Corriendo

```bash
# Ver estado de los contenedores
docker compose ps

# Ver logs en tiempo real
docker compose logs -f

# Ver logs de un servicio específico
docker compose logs -f backend
docker compose logs -f postgres
docker compose logs -f redis
```

### 3. Aplicar Migraciones de Base de Datos

```bash
# Esperar a que PostgreSQL esté listo (puede tomar unos segundos)
sleep 10

# Aplicar migraciones
docker compose exec backend alembic upgrade head
```

### 4. Verificar que la API Funciona

```bash
# Health check
curl http://localhost:8000/health

# O desde fuera del servidor
curl http://45.137.192.196:8000/health

# Ver documentación
# Abrir en navegador: http://45.137.192.196:8000/docs
```

## 🔧 Comandos Útiles

### Gestionar Servicios

```bash
# Levantar servicios
docker compose up -d

# Detener servicios
docker compose down

# Detener y eliminar volúmenes (¡CUIDADO! Elimina datos)
docker compose down -v

# Reiniciar un servicio específico
docker compose restart backend

# Ver logs
docker compose logs -f backend

# Entrar al contenedor del backend
docker compose exec backend bash
```

### Gestionar Base de Datos

```bash
# Conectar a PostgreSQL desde el contenedor
docker compose exec postgres psql -U g4qc -d g4qc_db

# Hacer backup de la base de datos
docker compose exec postgres pg_dump -U g4qc g4qc_db > backup.sql

# Verificar conexión a Redis
docker compose exec redis redis-cli ping
```

### Actualizar el Proyecto

```bash
cd /opt/proyectos/G4QC

# Actualizar código desde git (si usas git)
git pull

# Reconstruir y reiniciar servicios
docker compose down
docker compose build --no-cache
docker compose up -d

# Aplicar nuevas migraciones si las hay
docker compose exec backend alembic upgrade head
```

## 🐛 Solución de Problemas

### Error: "Cannot connect to Docker daemon"

```bash
# Iniciar servicio Docker
systemctl start docker
systemctl enable docker

# Verificar estado
systemctl status docker
```

### Error: "Port already in use"

Si los puertos 5432, 6379 o 8000 están en uso:

```bash
# Ver qué está usando los puertos
netstat -tulpn | grep -E ":(5432|6379|8000)"
ss -tulpn | grep -E ":(5432|6379|8000)"

# Detener procesos que los usan o cambiar puertos en docker-compose.yml
```

### Error: "Service 'backend' failed to build"

```bash
# Ver logs detallados
docker compose build --no-cache backend

# Verificar Dockerfile
cat backend/Dockerfile

# Verificar requirements.txt
cat backend/requirements.txt
```

### Error: "Database connection failed"

```bash
# Verificar que PostgreSQL esté corriendo
docker compose ps postgres

# Ver logs de PostgreSQL
docker compose logs postgres

# Verificar conectividad desde backend
docker compose exec backend ping postgres
```

### Los contenedores se reinician constantemente

```bash
# Ver logs para identificar el error
docker compose logs backend

# Verificar recursos del sistema
df -h  # Espacio en disco
free -h  # Memoria
```

## 📝 Verificación Final

Después de la instalación, verifica:

- [ ] Docker está instalado: `docker --version`
- [ ] Docker Compose funciona: `docker compose version`
- [ ] Todos los servicios están corriendo: `docker compose ps`
- [ ] La API responde: `curl http://localhost:8000/health`
- [ ] La documentación es accesible: `http://45.137.192.196:8000/docs`
- [ ] Las migraciones están aplicadas (verificar en logs)

## 🔒 Seguridad

**IMPORTANTE**: Después de la instalación, considera:

1. **Cambiar la contraseña del servidor** o configurar autenticación por claves SSH
2. **Configurar firewall** para proteger los puertos
3. **Cambiar las contraseñas de la base de datos** en producción
4. **Configurar HTTPS** para la API en producción
5. **Revisar permisos de archivos** sensibles (`.env`)

## 📞 Siguiente Paso

Una vez que todo esté funcionando, puedes:

1. Configurar Interactive Brokers TWS/Gateway
2. Probar la extracción de datos
3. Configurar el frontend (cuando esté listo)
4. Configurar backups automáticos de la base de datos

---

**Servidor**: 45.137.192.196  
**Ubicación del proyecto**: `/opt/proyectos/G4QC`

