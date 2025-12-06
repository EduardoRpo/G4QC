# 🚀 Pasos Inmediatos para Configurar el Servidor

## 📊 Análisis de la Situación Actual

Basado en la revisión realizada en el servidor **45.137.192.196**:

### ✅ Lo que está bien:
- ✅ Proyecto encontrado en `/opt/proyectos/G4QC`
- ✅ `docker-compose.yml` existe y está correctamente configurado
- ✅ Estructura del backend completa
- ✅ Todos los archivos necesarios están presentes

### ❌ Lo que falta:
- ❌ **Docker NO está instalado**
- ❌ **Docker Compose NO está instalado**
- ❌ Archivo `.env` no existe (pero no es crítico ahora)

## 🎯 Solución: Instalación Automática

### Paso 1: Conectarse al Servidor

```bash
ssh root@45.137.192.196
# Contraseña: G4QC2026
```

### Paso 2: Ir al Directorio del Proyecto

```bash
cd /opt/proyectos/G4QC
```

### Paso 3: Copiar el Script de Instalación

El script `instalar_en_servidor.sh` ya debería estar en el servidor (fue transferido con git). Si no está, copia este contenido:

```bash
# Crear el script
cat > instalar_en_servidor.sh << 'SCRIPT_END'
# [El contenido del script estará aquí - se copiará desde el archivo local]
SCRIPT_END

# Dar permisos de ejecución
chmod +x instalar_en_servidor.sh
```

O simplemente ejecuta los comandos manualmente (ver siguiente sección).

### Paso 4: Ejecutar el Script de Instalación

```bash
bash instalar_en_servidor.sh
```

## 🔧 Alternativa: Instalación Manual Rápida

Si prefieres hacerlo manualmente, ejecuta estos comandos en orden:

### 1. Instalar Docker

```bash
apt update
apt install -y ca-certificates curl gnupg lsb-release
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
systemctl start docker
systemctl enable docker
docker --version
```

### 2. Verificar Docker Compose

```bash
docker compose version
```

Si no funciona, instalar standalone:

```bash
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

### 3. Crear archivo .env (opcional)

```bash
cd /opt/proyectos/G4QC
cat > backend/.env << EOF
DEBUG=False
DATABASE_URL=postgresql://g4qc:g4qc_dev@postgres:5432/g4qc_db
REDIS_URL=redis://redis:6379
IB_HOST=127.0.0.1
IB_PORT=7497
IB_CLIENT_ID=1
EOF
```

### 4. Levantar los Servicios

```bash
cd /opt/proyectos/G4QC
docker compose up -d
```

### 5. Verificar que Todo Funciona

```bash
# Ver estado
docker compose ps

# Ver logs
docker compose logs -f

# Verificar API
sleep 10  # Esperar a que los servicios inicien
curl http://localhost:8000/health
```

## ✅ Verificación Final

Después de la instalación, verifica que todo esté funcionando:

```bash
# 1. Docker funciona
docker --version
docker compose version

# 2. Servicios corriendo
docker compose ps

# 3. API responde
curl http://localhost:8000/health

# 4. Documentación accesible (desde navegador)
# http://45.137.192.196:8000/docs
```

## 📝 Próximos Pasos

Una vez que los servicios estén corriendo:

1. **Aplicar migraciones de base de datos:**
   ```bash
   docker compose exec backend alembic upgrade head
   ```

2. **Configurar Interactive Brokers** (si es necesario):
   - Asegúrate de que TWS o IB Gateway esté corriendo
   - Ajusta `IB_HOST` y `IB_PORT` en `backend/.env` si es necesario

3. **Probar la API:**
   ```bash
   curl http://45.137.192.196:8000/health
   ```

## 🐛 Si Algo Sale Mal

### Docker no se instala:
- Verifica conexión a internet: `ping 8.8.8.8`
- Verifica que apt esté funcionando: `apt update`

### Los servicios no inician:
- Ver logs: `docker compose logs`
- Verifica recursos: `df -h` y `free -h`
- Verifica puertos: `netstat -tulpn | grep -E ":(5432|6379|8000)"`

### La API no responde:
- Verifica que el backend esté corriendo: `docker compose ps backend`
- Ver logs del backend: `docker compose logs backend`
- Espera un poco más (puede tardar en compilar)

## 📚 Documentación Adicional

- Ver `INSTALACION_COMPLETA_SERVIDOR.md` para guía detallada
- Ver `INSTALACION_DOCKER.md` para problemas con Docker
- Ver `README.md` para uso general de la plataforma

---

**Recuerda**: Todos estos comandos deben ejecutarse en el servidor remoto, no en tu máquina local.

