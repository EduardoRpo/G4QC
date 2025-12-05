# 🚀 Pasos Simples para Configurar IB Gateway

## ¿Qué Necesitas Hacer?

Para extraer datos históricos, necesitas tener **IB Gateway** ejecutándose en tu computadora. Es como un "puente" entre tu aplicación y los datos de Interactive Brokers.

---

## 📋 Pasos (En Orden)

### Paso 1: Descargar IB Gateway

1. Ve a: https://www.interactivebrokers.com/en/index.php?f=16042
2. Busca "IB Gateway" (no TWS, Gateway es más simple)
3. Descarga la versión para Windows
4. Instálalo (siguiente, siguiente, instalar)

### Paso 2: Crear Cuenta de Paper Trading (Gratis)

1. Si no tienes cuenta, crea una en: https://www.interactivebrokers.com/
2. Elige "Paper Trading Account" (simulación, gratis)
3. Completa el registro

### Paso 3: Abrir IB Gateway

1. Abre IB Gateway desde el menú de inicio
2. Inicia sesión con tu cuenta de paper trading
3. Espera a que se conecte (verás "Connected" o "Conectado")

### Paso 4: Habilitar API

1. En IB Gateway, ve a: **Configuración** → **API Settings** (o "Configuración API")
2. Marca: **"Enable ActiveX and Socket Clients"**
3. Configura el puerto: **7497** (para paper trading)
4. Guarda y cierra la ventana de configuración

### Paso 5: Verificar

Deberías ver en IB Gateway que está:
- ✅ Conectado (Connected)
- ✅ API habilitada (puerto 7497)

---

## ✅ Ahora Puedes Probar

1. **Instala ibapi** (si no lo hiciste):
   ```powershell
   docker-compose exec backend pip install ibapi
   docker-compose restart backend
   ```

2. **Abre tu aplicación**: http://localhost:8000/docs

3. **Prueba extraer datos** desde el endpoint de extracción

---

## ⚠️ Importante

- **IB Gateway debe estar ABIERTO y CONECTADO** mientras usas la aplicación
- Si cierras IB Gateway, la extracción de datos no funcionará
- El puerto 7497 es para paper trading (simulación), 7496 es para cuenta real

---

## 🎯 Resumen Ultra Simple

1. Descarga IB Gateway
2. Inicia sesión
3. Habilita API en puerto 7497
4. Déjalo abierto
5. Prueba tu aplicación

---

**¿Tienes alguna duda sobre algún paso?** Puedo ayudarte con la instalación o configuración específica.

