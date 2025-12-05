# 🔧 Habilitar API en IB Gateway - Guía Completa

## 📋 ¿Qué Significa "Habilitar la API"?

**Habilitar la API = Activar la conexión API en IB Gateway/TWS**

Es simplemente **marcar una casilla** en la configuración de IB Gateway para permitir que tu aplicación se conecte.

**NO es:**
- ❌ Instalar nada adicional
- ❌ Programar nada
- ❌ Configurar código

**SÍ es:**
- ✅ Abrir configuración de IB Gateway
- ✅ Marcar una casilla: "Enable ActiveX and Socket Clients"
- ✅ Configurar el puerto (7497)

---

## 👤 ¿Necesitas Cuenta (Usuario y Contraseña)?

**SÍ, necesitas una cuenta de Interactive Brokers**, pero:

### ✅ Opción 1: Paper Trading (GRATIS) - Recomendado para Pruebas

**¿Qué es?**
- Cuenta de **simulación** (no es dinero real)
- **100% GRATIS**
- Usa datos reales pero con dinero virtual
- Perfecto para pruebas y desarrollo

**Cómo obtenerla:**
1. Ve a: https://www.interactivebrokers.com/en/index.php?f=16042
2. Busca "Paper Trading Account" o "Demo Account"
3. Regístrate (es gratis)
4. Te darán:
   - Username (tu nombre de usuario)
   - Password (tu contraseña)

**Ventajas:**
- ✅ Gratis
- ✅ Sin riesgo (dinero virtual)
- ✅ Mismos datos reales
- ✅ Perfecto para desarrollo

---

### ⚠️ Opción 2: Cuenta Real (Requiere Fondos)

**¿Qué es?**
- Cuenta real con dinero de verdad
- Puede ser gratis la cuenta, pero necesitas fondos para operar
- Requiere verificación de identidad
- Solo si vas a hacer trading real

**No recomendado para:**
- Desarrollo inicial
- Pruebas
- Aprender a usar la API

---

## 💰 ¿Es Gratis o Pago?

### Paper Trading: **GRATIS** ✅

- ✅ Crear cuenta: **GRATIS**
- ✅ Usar IB Gateway: **GRATIS**
- ✅ Extraer datos: **GRATIS**
- ✅ Datos históricos: **GRATIS**
- ✅ Trading simulado: **GRATIS**

**No pagas nada por Paper Trading.**

---

### Cuenta Real: Depende

- ✅ Crear cuenta: **GRATIS**
- ✅ Usar IB Gateway: **GRATIS**
- ⚠️ Trading real: Requiere fondos (dinero real)
- ⚠️ Comisiones: Se cobran por operaciones reales

---

## 🔧 Paso a Paso: Habilitar API en IB Gateway

### Paso 1: Crear Cuenta Paper Trading (Gratis)

1. Ve a: https://www.interactivebrokers.com/en/index.php?f=16042
2. Busca **"Paper Trading Account"** o **"Demo Account"**
3. Haz clic en **"Create Account"** o **"Sign Up"**
4. Completa el formulario:
   - Email
   - Nombre
   - País
   - etc.
5. Confirma tu email
6. Te darán:
   - **Username**: `DU123456` (ejemplo)
   - **Password**: `tu_contraseña`

**⏱️ Tiempo:** 5-10 minutos

---

### Paso 2: Instalar IB Gateway

1. Mismo sitio: https://www.interactivebrokers.com/en/index.php?f=16042
2. Descarga **"IB Gateway"** (no TWS completo)
3. Instálalo en tu computadora
4. Ejecuta IB Gateway

---

### Paso 3: Iniciar Sesión

1. **Abre IB Gateway**
2. **Ingresa tus credenciales:**
   - **Username**: Tu usuario (ej: `DU123456`)
   - **Password**: Tu contraseña
   - **Account Type**: Paper Trading (si te pregunta)
3. Haz clic en **"Login"**
4. Espera a que conecte (verás "Connected")

---

### Paso 4: Habilitar API (La Configuración)

Esta es la parte importante:

#### Opción A: Desde IB Gateway (Recomendado)

1. **En IB Gateway**, ve a:
   - **File** → **Global Configuration** → **API** → **Settings**
   - O busca en el menú: "Configuration" → "API" → "Settings"

2. **Busca estas opciones:**

   ```
   ┌─────────────────────────────────────────┐
   │  API Settings                           │
   ├─────────────────────────────────────────┤
   │                                         │
   │  ☑ Enable ActiveX and Socket Clients    │
   │  ☐ Read-Only API                        │
   │                                         │
   │  Socket port: [7497]                    │
   │                                         │
   │  Trusted IPs:                           │
   │  [127.0.0.1]                            │
   │                                         │
   │  [Apply] [OK]                           │
   └─────────────────────────────────────────┘
   ```

3. **Marca la casilla:**
   - ✅ **"Enable ActiveX and Socket Clients"** (MÁS IMPORTANTE)

4. **Configura el puerto:**
   - **Socket port**: `7497` (Paper Trading)
   - O `7496` (Live Trading)

5. **Trusted IPs (Opcional pero recomendado):**
   - Agrega: `127.0.0.1` (solo permite conexiones desde tu PC)

6. **Guarda:**
   - Haz clic en **"Apply"** o **"OK"**

7. **Reinicia IB Gateway** si te lo pide

---

#### Opción B: Desde Archivo de Configuración

Si no encuentras el menú, puedes editar el archivo de configuración:

1. Cierra IB Gateway
2. Busca el archivo de configuración (generalmente en):
   - Windows: `C:\Users\TuUsuario\Documents\IB Gateway\`
   - Busca archivo: `ibgateway.ini` o similar
3. Abre con editor de texto
4. Busca sección `[API]`
5. Agrega o modifica:
   ```ini
   [API]
   EnableActiveX=true
   SocketPort=7497
   TrustedIPs=127.0.0.1
   ```
6. Guarda y abre IB Gateway de nuevo

---

### Paso 5: Verificar que Funcionó

1. **IB Gateway debe mostrar:**
   - ✅ "Connected" (conectado)
   - ✅ Estado verde o activo

2. **Desde PowerShell, verifica puerto:**
   ```powershell
   Test-NetConnection -ComputerName localhost -Port 7497
   ```
   
   Debería mostrar: `TcpTestSucceeded : True`

3. **Si no funciona:**
   - Verifica que la casilla esté marcada
   - Verifica que el puerto sea 7497
   - Reinicia IB Gateway
   - Verifica que no haya firewall bloqueando

---

## 📸 Visualización de la Configuración

### Pantalla de Login:
```
┌─────────────────────────────┐
│  IB Gateway                 │
├─────────────────────────────┤
│                             │
│  Username: [DU123456    ]   │
│  Password: [********    ]   │
│                             │
│  Account Type:              │
│  ○ Paper Trading            │
│  ● Live Trading             │
│                             │
│  [Login]                    │
└─────────────────────────────┘
```

### Pantalla Configuración API:
```
┌─────────────────────────────────────────┐
│  Configuration - API Settings           │
├─────────────────────────────────────────┤
│                                         │
│  ☑ Enable ActiveX and Socket Clients   │  ← MARCAR ESTA
│  ☐ Read-Only API                        │
│                                         │
│  Socket port:                           │
│  [7497]                                 │  ← PUERTO
│                                         │
│  Trusted IPs:                           │
│  [127.0.0.1]                            │  ← OPCIONAL
│                                         │
│  [Apply]  [Cancel]  [OK]                │
└─────────────────────────────────────────┘
```

---

## ✅ Checklist Completo

### 1. Cuenta Paper Trading:
- [ ] Crear cuenta en Interactive Brokers (gratis)
- [ ] Recibir Username y Password
- [ ] Verificar email (si es necesario)

### 2. Instalar IB Gateway:
- [ ] Descargar IB Gateway
- [ ] Instalar en tu computadora
- [ ] Ejecutar IB Gateway

### 3. Iniciar Sesión:
- [ ] Abrir IB Gateway
- [ ] Ingresar Username y Password
- [ ] Seleccionar "Paper Trading"
- [ ] Verificar que muestre "Connected"

### 4. Habilitar API:
- [ ] Ir a: File → Global Configuration → API → Settings
- [ ] Marcar: "Enable ActiveX and Socket Clients" ✅
- [ ] Configurar puerto: 7497
- [ ] (Opcional) Agregar Trusted IP: 127.0.0.1
- [ ] Guardar y reiniciar si es necesario

### 5. Verificar:
- [ ] IB Gateway muestra "Connected"
- [ ] Puerto 7497 está abierto
- [ ] Listo para conectar desde tu aplicación

---

## 🎯 Resumen

### ¿Qué es "Habilitar API"?
- ✅ Marcar una casilla en configuración de IB Gateway
- ✅ Configurar puerto (7497)
- ✅ Eso es todo

### ¿Necesitas cuenta?
- ✅ SÍ, pero puedes usar **Paper Trading** (GRATIS)

### ¿Es gratis?
- ✅ Paper Trading: **100% GRATIS**
- ✅ No pagas nada por:
  - Crear cuenta
  - Usar IB Gateway
  - Extraer datos
  - Trading simulado

---

## 🚀 Siguiente Paso

Una vez que tengas:
- ✅ Cuenta Paper Trading (gratis)
- ✅ IB Gateway instalado
- ✅ API habilitada (casilla marcada)

Puedes:
1. Instalar `ibapi`: `docker-compose exec backend pip install ibapi`
2. Probar extracción: http://localhost:8000/docs

---

**¿Necesitas ayuda con algún paso específico? Puedo guiarte paso a paso.**

