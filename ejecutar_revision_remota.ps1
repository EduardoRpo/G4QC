# Script PowerShell para ejecutar revisión en servidor remoto
# Requiere: ssh disponible y capacidad de ejecutar comandos remotos

$server = "45.137.192.196"
$user = "root"
$password = "G4QC2026"

Write-Host "Intentando conectar al servidor $server..." -ForegroundColor Cyan

# Crear script de revisión que se ejecutará en el servidor remoto
$remoteScript = @"
#!/bin/bash
echo "=========================================="
echo "REVISIÓN DEL SERVIDOR - $(date)"
echo "=========================================="
echo ""
echo "1. INFORMACIÓN DEL SISTEMA"
echo "---------------------------"
uname -a
cat /etc/os-release 2>/dev/null | head -5
echo ""
echo "2. VERIFICACIÓN DE DOCKER"
echo "---------------------------"
docker --version 2>/dev/null || echo "Docker NO instalado"
docker compose version 2>/dev/null || echo "Docker Compose plugin NO disponible"  
docker-compose --version 2>/dev/null || echo "docker-compose NO instalado"
systemctl status docker --no-pager -l 2>/dev/null | head -3 || echo "No se pudo verificar servicio Docker"
echo ""
echo "3. PROYECTO G4QC"
echo "---------------------------"
if [ -d "/opt/proyectos/G4QC" ]; then
    cd /opt/proyectos/G4QC
    echo "Directorio encontrado: $(pwd)"
    echo ""
    echo "Contenido:"
    ls -la
    echo ""
    echo "docker-compose.yml:"
    cat docker-compose.yml 2>/dev/null || echo "No encontrado"
    echo ""
    echo "Backend:"
    ls -la backend/ 2>/dev/null | head -10 || echo "Directorio backend no encontrado"
    echo ""
    echo "Archivos .env:"
    ls -la backend/.env* 2>/dev/null || echo "No encontrados"
else
    echo "Directorio /opt/proyectos/G4QC NO encontrado"
    echo "Buscando en otras ubicaciones:"
    find / -name "G4QC" -type d 2>/dev/null | head -3
fi
echo ""
echo "4. CONTENEDORES DOCKER"
echo "---------------------------"
docker ps -a 2>/dev/null || echo "No se pueden listar contenedores"
echo ""
echo "5. PUERTOS"
echo "---------------------------"
netstat -tulpn 2>/dev/null | grep -E ":(5432|6379|8000)" || ss -tulpn 2>/dev/null | grep -E ":(5432|6379|8000)" || echo "Puertos no encontrados"
echo ""
echo "6. RECURSOS"
echo "---------------------------"
df -h | head -3
free -h
echo ""
echo "=========================================="
echo "FIN DE LA REVISIÓN"
echo "=========================================="
"@

Write-Host "`nPara ejecutar la revisión, usa uno de estos métodos:`n" -ForegroundColor Yellow
Write-Host "OPCIÓN 1: Conectarse manualmente y ejecutar comandos" -ForegroundColor Green
Write-Host "ssh root@45.137.192.196" -ForegroundColor White
Write-Host "# Luego ejecuta los comandos del archivo REVISION_SERVIDOR.md`n" -ForegroundColor Gray

Write-Host "OPCIÓN 2: Copiar y pegar este script completo en el servidor:" -ForegroundColor Green
Write-Host $remoteScript -ForegroundColor White

Write-Host "`nOPCIÓN 3: Ejecutar script desde archivo local:" -ForegroundColor Green
Write-Host "scp verificar_servidor.sh root@45.137.192.196:/tmp/" -ForegroundColor White
Write-Host "ssh root@45.137.192.196 'bash /tmp/verificar_servidor.sh'" -ForegroundColor White

Write-Host "`nNOTA: Para conexión automática se requiere sshpass o configuración de claves SSH" -ForegroundColor Yellow

