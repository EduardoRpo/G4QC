# Guía de Instalación de Docker y Docker Compose

## Verificación Inicial

Primero, verifica si Docker está instalado:

```bash
docker --version
```

Si Docker está instalado, intenta usar el comando moderno:

```bash
docker compose up -d
```

## Opción 1: Instalar Docker Compose Standalone (más rápido)

Si Docker ya está instalado pero falta docker-compose:

```bash
# Descargar la última versión de docker-compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Dar permisos de ejecución
chmod +x /usr/local/bin/docker-compose

# Verificar instalación
docker-compose --version
```

## Opción 2: Instalar Docker Completo desde Cero

### Para Ubuntu/Debian:

```bash
# Actualizar paquetes
apt update

# Instalar dependencias
apt install -y ca-certificates curl gnupg lsb-release

# Agregar clave GPG oficial de Docker
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Configurar repositorio
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker Engine, CLI y Docker Compose Plugin
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verificar instalación
docker --version
docker compose version

# Iniciar y habilitar Docker
systemctl start docker
systemctl enable docker

# Agregar usuario actual al grupo docker (opcional, para no usar sudo)
# usermod -aG docker $USER
```

### Instalación Rápida con Script Oficial (Recomendado):

```bash
# Ejecutar script oficial de instalación
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Agregar Docker Compose Plugin si no viene incluido
apt update
apt install -y docker-compose-plugin

# Verificar
docker --version
docker compose version
```

## Usar Docker Compose

Una vez instalado, puedes usar cualquiera de estas opciones:

### Opción A: Comando moderno (recomendado)
```bash
docker compose up -d
```

### Opción B: Comando clásico
```bash
docker-compose up -d
```

Ambos comandos funcionan igual. El comando moderno (`docker compose`) es un plugin de Docker y está más actualizado.

## Verificar Instalación

```bash
# Verificar Docker
docker --version

# Verificar Docker Compose (método moderno)
docker compose version

# Verificar Docker Compose (método clásico)
docker-compose --version
```

## Notas Importantes

- Si estás como usuario `root`, no necesitas `sudo`
- Si usas otro usuario, puede que necesites agregarlo al grupo `docker` o usar `sudo`
- El comando moderno `docker compose` (sin guión) es un plugin y es el estándar actual
- El comando clásico `docker-compose` (con guión) sigue funcionando pero es standalone

## Problemas Comunes

### Error: "Permission denied"
```bash
# Si no eres root, agregar tu usuario al grupo docker
sudo usermod -aG docker $USER
# Luego cerrar sesión y volver a iniciar sesión
```

### Error: "Cannot connect to Docker daemon"
```bash
# Iniciar el servicio Docker
systemctl start docker
systemctl enable docker
```

