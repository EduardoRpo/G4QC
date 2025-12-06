# Instrucciones para Revisar el Servidor por SSH

## 🔐 Información de Conexión

- **Servidor**: 45.137.192.196
- **Usuario**: root
- **Contraseña**: G4QC2026

## 🚀 Método Rápido: Script Automático

### Paso 1: Conectarse al servidor

```bash
ssh root@45.137.192.196
# Ingresa la contraseña: G4QC2026
```

### Paso 2: Copiar y ejecutar el script completo

Una vez conectado, copia y pega TODO este bloque de código:

```bash
#!/bin/bash
echo "=========================================="
echo "REVISIÓN COMPLETA DEL SERVIDOR G4QC"
echo "Fecha: $(date)"
echo "=========================================="
echo ""

echo "1. INFORMACIÓN DEL SISTEMA"
echo "==========================="
uname -a
echo ""
cat /etc/os-release 2>/dev/null | head -10
echo ""

echo "2. VERIFICACIÓN DE DOCKER"
echo "=========================="
echo "Docker:"
docker --version 2>/dev/null || echo "❌ Docker NO está instalado"
echo ""

echo "Docker Compose (plugin):"
docker compose version 2>/dev/null || echo "❌ Docker Compose plugin NO disponible"
echo ""

echo "Docker Compose (standalone):"
docker-compose --version 2>/dev/null || echo "❌ docker-compose NO está instalado"
echo ""

echo "Estado del servicio Docker:"
systemctl status docker --no-pager -l 2>/dev/null | head -5 || echo "No se pudo verificar"
echo ""

echo "3. PROYECTO G4QC"
echo "================="
if [ -d "/opt/proyectos/G4QC" ]; then
    cd /opt/proyectos/G4QC
    echo "✓ Directorio encontrado: $(pwd)"
    echo ""
    echo "Contenido del directorio:"
    ls -la
    echo ""
    
    if [ -f "docker-compose.yml" ]; then
        echo "✓ docker-compose.yml encontrado"
        echo ""
        echo "--- Contenido de docker-compose.yml ---"
        cat docker-compose.yml
        echo "--- Fin de docker-compose.yml ---"
        echo ""
    else
        echo "❌ docker-compose.yml NO encontrado"
    fi
    
    if [ -d "backend" ]; then
        echo "✓ Directorio backend encontrado"
        echo ""
        echo "Estructura del backend:"
        ls -la backend/ | head -15
        echo ""
        
        echo "Archivos de configuración:"
        ls -la backend/.env* 2>/dev/null || echo "No se encontraron archivos .env"
        echo ""
        
        if [ -f "backend/.env.example" ]; then
            echo "Contenido de .env.example:"
            cat backend/.env.example
        fi
        
        if [ -f "backend/.env" ]; then
            echo "Variables configuradas en .env (solo nombres):"
            grep -E "^[A-Z_]+=" backend/.env | cut -d'=' -f1 || echo "No se encontraron variables"
        fi
    else
        echo "❌ Directorio backend NO encontrado"
    fi
else
    echo "❌ Directorio /opt/proyectos/G4QC NO encontrado"
    echo ""
    echo "Buscando el proyecto en otras ubicaciones:"
    find / -name "G4QC" -type d 2>/dev/null | head -5
fi
echo ""

echo "4. CONTENEDORES DOCKER"
echo "======================"
docker ps -a 2>/dev/null || echo "No se pueden listar contenedores"
echo ""

echo "5. PUERTOS EN USO"
echo "=================="
echo "Puertos relevantes (5432, 6379, 8000):"
netstat -tulpn 2>/dev/null | grep -E ":(5432|6379|8000)" || \
ss -tulpn 2>/dev/null | grep -E ":(5432|6379|8000)" || \
echo "No se encontraron puertos en uso"
echo ""

echo "6. RECURSOS DEL SISTEMA"
echo "======================="
echo "Espacio en disco:"
df -h | head -5
echo ""
echo "Memoria:"
free -h
echo ""
echo "CPU:"
nproc
echo ""

echo "=========================================="
echo "FIN DE LA REVISIÓN"
echo "=========================================="
```

### Paso 3: Compartir los resultados

Después de ejecutar el script, copia toda la salida y compártela para que pueda analizar la configuración.

## 📋 Método Alternativo: Usar el Script desde Archivo

### Desde tu máquina local (Windows):

```powershell
# 1. Copiar el script al servidor
scp verificar_servidor.sh root@45.137.192.196:/tmp/

# 2. Conectarse y ejecutar
ssh root@45.137.192.196
bash /tmp/verificar_servidor.sh
```

## 🔍 Revisión Manual Paso a Paso

Si prefieres revisar manualmente, sigue estos comandos en orden:

```bash
# Conectarse
ssh root@45.137.192.196

# 1. Sistema
uname -a
cat /etc/os-release

# 2. Docker
docker --version
docker compose version
docker-compose --version

# 3. Proyecto
cd /opt/proyectos/G4QC
ls -la
cat docker-compose.yml

# 4. Backend
ls -la backend/
cat backend/.env.example 2>/dev/null

# 5. Contenedores
docker ps -a

# 6. Puertos
netstat -tulpn | grep -E ":(5432|6379|8000)"
```

## ⚠️ Notas Importantes

1. **Seguridad**: Después de la revisión, considera cambiar la contraseña o configurar autenticación por claves SSH
2. **Permisos**: Si no puedes ejecutar comandos, verifica que estés como usuario `root`
3. **Conexión**: Si no puedes conectarte, verifica:
   - Que el servidor esté accesible: `ping 45.137.192.196`
   - Que el puerto SSH (22) esté abierto
   - Que tengas acceso de red

## 📝 Próximos Pasos Después de la Revisión

Una vez que tengamos la información del servidor, podremos:

1. ✅ Instalar Docker/Docker Compose si falta
2. ✅ Configurar el archivo `.env` con las variables necesarias
3. ✅ Levantar los servicios con `docker-compose up -d`
4. ✅ Verificar que todos los servicios estén funcionando
5. ✅ Configurar autenticación SSH por claves (recomendado)

## 🆘 Solución de Problemas

### Error: "Permission denied"
- Verifica que la contraseña sea correcta
- Asegúrate de usar el usuario `root`

### Error: "Connection refused"
- El servidor puede estar apagado o el firewall bloqueando
- Verifica la conectividad con `ping 45.137.192.196`

### Error: "Docker not found"
- Necesitaremos instalar Docker (ver `INSTALACION_DOCKER.md`)

