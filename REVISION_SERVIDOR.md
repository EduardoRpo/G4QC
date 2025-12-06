# Revisión de Configuración del Servidor

## Servidor: 45.137.192.196

## Comandos para Ejecutar en el Servidor

Conéctate al servidor con:
```bash
ssh root@45.137.192.196
# Password: G4QC2026
```

Luego ejecuta estos comandos para revisar la configuración:

### 1. Verificar Sistema y Docker

```bash
# Información del sistema
uname -a
cat /etc/os-release

# Verificar Docker
docker --version
docker compose version
docker-compose --version

# Estado del servicio Docker
systemctl status docker
```

### 2. Revisar Proyecto G4QC

```bash
# Ir al directorio del proyecto
cd /opt/proyectos/G4QC

# Ver estructura
ls -la

# Ver docker-compose.yml
cat docker-compose.yml

# Ver estructura del backend
ls -la backend/
```

### 3. Verificar Archivos de Configuración

```bash
# Ver si existe .env
ls -la backend/.env*

# Si existe .env.example, ver su contenido
cat backend/.env.example

# Si existe .env, ver nombres de variables (sin valores sensibles)
if [ -f backend/.env ]; then
    echo "Variables configuradas:"
    grep -E "^[A-Z_]+=" backend/.env | cut -d'=' -f1
fi
```

### 4. Verificar Contenedores y Puertos

```bash
# Ver contenedores
docker ps -a

# Ver puertos en uso
netstat -tulpn | grep -E ":(5432|6379|8000)" || ss -tulpn | grep -E ":(5432|6379|8000)"

# Ver logs de contenedores si existen
docker logs g4qc_postgres 2>/dev/null
docker logs g4qc_redis 2>/dev/null
docker logs g4qc_backend 2>/dev/null
```

### 5. Verificar Recursos del Sistema

```bash
# Espacio en disco
df -h

# Memoria
free -h

# CPU
nproc
```

## Script Automático

Alternativamente, puedes copiar y ejecutar este script completo en el servidor:

```bash
#!/bin/bash
echo "=========================================="
echo "REVISIÓN COMPLETA DEL SERVIDOR"
echo "=========================================="

echo ""
echo "1. SISTEMA"
echo "----------"
uname -a
cat /etc/os-release 2>/dev/null

echo ""
echo "2. DOCKER"
echo "---------"
docker --version 2>/dev/null || echo "Docker NO instalado"
docker compose version 2>/dev/null || echo "Docker Compose plugin NO disponible"
docker-compose --version 2>/dev/null || echo "docker-compose NO instalado"
systemctl status docker --no-pager -l 2>/dev/null | head -5

echo ""
echo "3. PROYECTO G4QC"
echo "----------------"
cd /opt/proyectos/G4QC 2>/dev/null && pwd || echo "Directorio no encontrado"
ls -la 2>/dev/null
echo ""
echo "docker-compose.yml:"
cat docker-compose.yml 2>/dev/null || echo "No encontrado"

echo ""
echo "4. BACKEND"
echo "----------"
ls -la backend/ 2>/dev/null
echo ""
echo "Archivos .env:"
ls -la backend/.env* 2>/dev/null || echo "No encontrados"

echo ""
echo "5. CONTENEDORES"
echo "---------------"
docker ps -a 2>/dev/null || echo "No se pueden listar"

echo ""
echo "6. PUERTOS"
echo "----------"
netstat -tulpn 2>/dev/null | grep -E ":(5432|6379|8000)" || ss -tulpn 2>/dev/null | grep -E ":(5432|6379|8000)" || echo "Puertos no encontrados"

echo ""
echo "7. RECURSOS"
echo "-----------"
df -h | head -3
free -h
```

## Después de la Revisión

Una vez que tengas la información, podemos:
1. Instalar Docker/Docker Compose si falta
2. Configurar el archivo .env
3. Levantar los servicios con docker-compose
4. Verificar que todo funciona correctamente

