# 📖 Guía: ¿Qué es IB TWS y Cómo Configurarlo?

## ¿Qué es IB TWS?

**IB TWS** = **Interactive Brokers Trader Workstation**

Es el software oficial de Interactive Brokers que necesitas tener ejecutándose en tu computadora para que la aplicación pueda conectarse y extraer datos históricos.

---

## 🎯 Dos Opciones Disponibles

### Opción 1: TWS (Trader Workstation) - Interfaz Completa
- Software completo con gráficos, análisis, etc.
- Más pesado, usa más recursos
- Ideal si también quieres usar la interfaz gráfica

### Opción 2: IB Gateway - Versión Ligera
- Solo la conexión API, sin interfaz gráfica
- Más liviano, usa menos recursos
- Ideal para automatización (recomendado para tu caso)

---

## 📥 Cómo Obtener IB TWS o IB Gateway

### Paso 1: Descargar

1. Ve a: https://www.interactivebrokers.com/en/index.php?f=16042
2. Descarga **IB Gateway** (recomendado) o **TWS**
3. Instálalo en tu computadora Windows

### Paso 2: Crear Cuenta (si no tienes)

- Puedes crear una cuenta de **Paper Trading** (simulación, gratis)
- O usar una cuenta real (si ya la tienes)

### Paso 3: Configurar para API

1. **Abre IB Gateway o TWS**
2. **Inicia sesión** (con tu cuenta de paper trading o real)
3. **Ve a Configuración** (Settings/Configuration)
4. **Busca "API Settings"** o "Configuración API"
5. **Habilita**: "Enable ActiveX and Socket Clients"
6. **Configura el puerto**:
   - **7497** para Paper Trading (recomendado para pruebas)
   - **7496** para Live Trading (cuenta real)
7. **Guarda** y reinicia si es necesario

---

## ✅ Verificar que Está Configurado Correctamente

### 1. IB Gateway/TWS debe estar:
- ✅ Ejecutándose (abierto)
- ✅ Conectado (verás "Connected" o "Conectado" en la interfaz)
- ✅ API habilitada en el puerto correcto

### 2. Verificar desde tu aplicación:

```powershell
# Verificar que el puerto está abierto
Test-NetConnection -ComputerName localhost -Port 7497
```

Debería mostrar: `TcpTestSucceeded : True`

---

## 🔧 Configuración en tu Aplicación

Tu aplicación ya está configurada para conectarse a:
- **Host**: `127.0.0.1` (localhost)
- **Puerto**: `7497` (paper trading) o `7496` (live)

Esto está en `backend/.env` o en las variables de entorno de Docker.

---

## 🚀 Flujo Completo para Extraer Datos

### 1. Instalar ibapi (si no lo hiciste)
```powershell
docker-compose exec backend pip install ibapi
docker-compose restart backend
```

### 2. Abrir IB Gateway/TWS
- Inicia sesión
- Asegúrate de que esté conectado
- Verifica que API esté habilitada

### 3. Probar extracción desde `/docs`
- Ve a: http://localhost:8000/docs
- Prueba el endpoint `POST /api/v1/data/extract`
- Debería funcionar ahora

---

## ⚠️ Problemas Comunes

### Error: "Connection refused"
**Causa**: IB Gateway/TWS no está ejecutándose o API no está habilitada

**Solución**:
1. Abre IB Gateway/TWS
2. Verifica que esté conectado
3. Verifica configuración API (puerto 7497)
4. Reinicia IB Gateway/TWS

### Error: "Cannot connect to IB"
**Causa**: Puerto incorrecto o firewall bloqueando

**Solución**:
1. Verifica el puerto en IB Gateway (7497 para paper)
2. Verifica que no haya firewall bloqueando
3. Prueba cambiar el puerto en `backend/.env` si es necesario

### Error: "Timeout"
**Causa**: IB Gateway no responde o está ocupado

**Solución**:
1. Cierra y vuelve a abrir IB Gateway
2. Espera unos segundos después de abrirlo
3. Intenta de nuevo

---

## 📝 Resumen Rápido

**Para que funcione la extracción de datos necesitas:**

1. ✅ **ibapi instalado** → `docker-compose exec backend pip install ibapi`
2. ✅ **IB Gateway/TWS ejecutándose** → Descargar e instalar desde IB
3. ✅ **API habilitada** → Configurar en IB Gateway (puerto 7497)
4. ✅ **IB Gateway conectado** → Debe mostrar "Connected"

---

## 🎯 ¿Puedo Probar Sin IB TWS?

**Sí, pero limitado:**

- ✅ Todos los endpoints funcionan
- ✅ Puedes consultar datos que ya estén en la base de datos
- ✅ La documentación funciona
- ❌ **NO puedes extraer datos nuevos** sin IB TWS/Gateway

---

## 💡 Recomendación

**Para desarrollo y pruebas:**
1. Usa **IB Gateway** (más liviano que TWS)
2. Usa cuenta de **Paper Trading** (gratis, sin riesgo)
3. Configura puerto **7497** (paper trading)

---

**¿Necesitas ayuda con algún paso específico?** Puedo guiarte en la instalación o configuración.

