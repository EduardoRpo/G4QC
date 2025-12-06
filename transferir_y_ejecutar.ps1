# Script PowerShell para transferir y ejecutar el script de verificación en el servidor
# Requiere: ssh y scp disponibles

$server = "45.137.192.196"
$user = "root"
$scriptLocal = "verificar_servidor.sh"
$scriptRemote = "/tmp/verificar_servidor.sh"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Transferencia y Ejecución Remota" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que el script local existe
if (-not (Test-Path $scriptLocal)) {
    Write-Host "ERROR: No se encontró el archivo $scriptLocal" -ForegroundColor Red
    Write-Host "Asegúrate de estar en el directorio G4QC" -ForegroundColor Yellow
    exit 1
}

Write-Host "Paso 1: Transferir script al servidor..." -ForegroundColor Yellow
Write-Host "Ejecuta este comando manualmente (te pedirá la contraseña):" -ForegroundColor White
Write-Host ""
Write-Host "scp $scriptLocal ${user}@${server}:$scriptRemote" -ForegroundColor Green
Write-Host ""

Write-Host "Paso 2: Conectarse y ejecutar el script..." -ForegroundColor Yellow
Write-Host "Ejecuta estos comandos:" -ForegroundColor White
Write-Host ""
Write-Host "ssh ${user}@${server}" -ForegroundColor Green
Write-Host "chmod +x $scriptRemote" -ForegroundColor Green
Write-Host "bash $scriptRemote" -ForegroundColor Green
Write-Host ""

Write-Host "Paso 3: Después de ver los resultados, comparte la salida completa" -ForegroundColor Yellow
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "NOTA: La contraseña es: G4QC2026" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan

# Opción alternativa: intentar ejecutar comandos directamente (requiere expect o sshpass)
Write-Host ""
Write-Host "Alternativa: Ejecutar todo en un solo comando (si tienes sshpass instalado):" -ForegroundColor Cyan
Write-Host ""
Write-Host '$env:SSHPASS="G4QC2026"' -ForegroundColor Gray
Write-Host 'sshpass -e scp verificar_servidor.sh root@45.137.192.196:/tmp/' -ForegroundColor Gray
Write-Host 'sshpass -e ssh root@45.137.192.196 "chmod +x /tmp/verificar_servidor.sh && bash /tmp/verificar_servidor.sh"' -ForegroundColor Gray

