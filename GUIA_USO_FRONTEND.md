# 📖 Guía de Uso del Frontend - G4QC Trading Platform

## 🚀 Acceso al Frontend

El frontend está disponible en: **`http://45.137.192.196:5173`**

---

## 📊 Secciones del Dashboard

El frontend tiene **3 secciones principales**:

### 1️⃣ **Estado del Sistema** (Panel Superior)

Muestra el estado actual del scheduler y del sistema:

- **Scheduler**: 
  - ✅ **Activo** (verde) = El scheduler está corriendo automáticamente
  - ❌ **Inactivo** (rojo) = El scheduler está detenido

- **Jobs Activos**: Número de trabajos de extracción de datos en ejecución

- **Última Ejecución**: Fecha y hora de la última vez que el scheduler extrajo datos

- **Próxima Ejecución**: Fecha y hora programada para la próxima extracción automática

- **Configuración Actual**: Muestra el intervalo, horario, símbolos y timeframes configurados

---

### 2️⃣ **Control del Scheduler** (Panel Central Izquierdo)

Permite controlar el scheduler automático:

#### **Botones Principales:**

- **▷ Activar Scheduler**: 
  - Inicia el scheduler automático
  - El scheduler comenzará a extraer datos según la configuración establecida

- **⏹ Desactivar Scheduler**: 
  - Detiene el scheduler automático
  - Los datos dejarán de actualizarse automáticamente

- **🔄 Ejecutar Ahora**: 
  - Ejecuta una extracción inmediata sin esperar el intervalo programado
  - Solo funciona si el scheduler está activo

#### **Configuración del Scheduler:**

Haz clic en **"Mostrar Configuración"** para ver/editar:

- **Intervalo (minutos)**: 
  - Cada cuántos minutos se ejecutará el scheduler
  - Ejemplo: `1` = cada 1 minuto, `5` = cada 5 minutos

- **Inicio (HH:MM)**: 
  - Hora de inicio del horario de mercado
  - Ejemplo: `09:00` = 9:00 AM

- **Fin (HH:MM)**: 
  - Hora de fin del horario de mercado
  - Ejemplo: `16:00` = 4:00 PM

- **Símbolos (separados por comas)**: 
  - Lista de instrumentos a monitorear
  - Ejemplos:
    - **Futuros**: `ES, NQ, YM, GC, CL`
    - **ETFs**: `SPY, QQQ, TLT`
    - **Forex**: `EURUSD, GBPUSD, AUDUSD`

- **Timeframes (separados por comas)**: 
  - Intervalos de tiempo para los datos
  - Ejemplos: `1min, 5min, 15min, 1hour`

**⚠️ Importante**: Después de cambiar la configuración, haz clic en **"Actualizar Configuración"** para guardar los cambios.

---

### 3️⃣ **Extracción Manual de Datos** (Panel Derecho)

Permite extraer datos históricos manualmente sin esperar al scheduler:

#### **Campos del Formulario:**

- **Símbolo**: 
  - Símbolo del instrumento a extraer
  - Ejemplos: `ES`, `NQ`, `SPY`, `EURUSD`
  - Se convierte automáticamente a mayúsculas

- **Duración**: 
  - Período de tiempo histórico a extraer
  - Opciones: `1 Día`, `1 Semana`, `1 Mes`, `3 Meses`

- **Tamaño de Barra**: 
  - Granularidad de los datos
  - Opciones: `1 minuto`, `5 minutos`, `15 minutos`, `1 hora`

- **Bloques**: 
  - Número de bloques a extraer (máximo 12)
  - Cada bloque es igual a la duración especificada
  - Ejemplo: Si duración = `1 Día` y bloques = `3`, extraerá 3 días de datos

- **Mes de Contrato (opcional)**: 
  - Solo necesario para **Futuros**
  - Formato: `YYYYMM` (ejemplo: `202512` = Diciembre 2025)
  - Para ETFs y Forex, dejar vacío

#### **Ejemplos de Uso:**

**Ejemplo 1: Extraer datos de ES (Futuro)**
```
Símbolo: ES
Duración: 1 Día
Tamaño de Barra: 1 minuto
Bloques: 1
Mes de Contrato: 202512
```

**Ejemplo 2: Extraer datos de SPY (ETF)**
```
Símbolo: SPY
Duración: 1 Semana
Tamaño de Barra: 5 minutos
Bloques: 1
Mes de Contrato: (dejar vacío)
```

**Ejemplo 3: Extraer datos de EURUSD (Forex)**
```
Símbolo: EURUSD
Duración: 1 Mes
Tamaño de Barra: 1 hora
Bloques: 1
Mes de Contrato: (dejar vacío)
```

Haz clic en **"Extraer Datos"** para iniciar la extracción. Verás un mensaje con el número de registros guardados.

---

### 4️⃣ **Visualización de Datos** (Panel Inferior)

Muestra gráficos y tablas de los datos almacenados en la base de datos:

#### **Controles:**

- **Símbolo**: Selecciona el símbolo a visualizar (se cargan automáticamente desde la BD)

- **Timeframe**: Selecciona el intervalo de tiempo (se cargan automáticamente según el símbolo)

- **🔄 Actualizar**: Recarga los datos desde la base de datos

#### **Visualizaciones:**

- **Gráfico de Líneas**: Muestra el precio de cierre (`close`) de los últimos 50 registros
- **Tabla de Datos**: Muestra los últimos 20 registros con:
  - Timestamp (fecha y hora)
  - Open (precio de apertura)
  - High (precio máximo)
  - Low (precio mínimo)
  - Close (precio de cierre)
  - Volume (volumen)

---

## 🎯 Flujo de Trabajo Recomendado

### **Paso 1: Configurar el Scheduler**

1. Haz clic en **"Mostrar Configuración"** en el panel "Control del Scheduler"
2. Configura:
   - Intervalo: `1` minuto (para pruebas rápidas) o `5` minutos (producción)
   - Horario: `09:00` - `16:00` (horario de mercado)
   - Símbolos: `ES, NQ` (o los que necesites)
   - Timeframes: `1min`
3. Haz clic en **"Actualizar Configuración"**

### **Paso 2: Activar el Scheduler**

1. Haz clic en **"▷ Activar Scheduler"**
2. Verifica en "Estado del Sistema" que el scheduler esté **Activo**
3. El scheduler comenzará a extraer datos automáticamente según la configuración

### **Paso 3: Verificar los Datos**

1. Espera unos minutos para que se acumulen datos
2. En "Visualización de Datos", selecciona un símbolo
3. Haz clic en **"Actualizar"** para ver los datos más recientes
4. Verifica el gráfico y la tabla de datos

### **Paso 4: Extracción Manual (Opcional)**

Si necesitas datos históricos específicos:
1. Usa el panel "Extracción Manual de Datos"
2. Configura los parámetros
3. Haz clic en **"Extraer Datos"**
4. Espera el mensaje de confirmación

---

## ⚠️ Notas Importantes

### **Símbolos Soportados:**

- **Futuros**: `ES`, `NQ`, `CL`, `YM`, `GC`, `RB`, `LE`, `HE`, `KE`, `ZS`, `MBT`, `6B`, `EC`
  - ⚠️ Requieren `contract_month` (ejemplo: `202512`)

- **ETFs/Stocks**: `SPY`, `QQQ`, `TLT`
  - ✅ No requieren `contract_month`

- **Forex**: `EURUSD`, `GBPUSD`, `AUDUSD`
  - ✅ No requieren `contract_month`

### **Requisitos:**

- ✅ IB Gateway debe estar corriendo (verifica en Docker: `docker compose ps`)
- ✅ Backend debe estar corriendo (verifica en `http://45.137.192.196:8000/docs`)
- ✅ Base de datos debe estar accesible

### **Solución de Problemas:**

- **Scheduler no se activa**: Verifica que IB Gateway esté corriendo
- **No hay datos en la visualización**: 
  - Espera unos minutos después de activar el scheduler
  - O haz una extracción manual primero
- **Error al extraer datos**: 
  - Verifica que el símbolo sea correcto
  - Para futuros, asegúrate de incluir el `contract_month`
  - Verifica los logs del backend: `docker compose logs backend`

---

## 🔄 Actualización del Estado

El frontend se actualiza automáticamente cada vez que:
- Activas/desactivas el scheduler
- Actualizas la configuración
- Ejecutas una extracción manual
- Haces clic en "Actualizar" en la visualización

---

## 📞 Soporte

Si encuentras problemas:
1. Verifica los logs: `docker compose logs backend`
2. Verifica el estado de los contenedores: `docker compose ps`
3. Revisa la documentación de la API: `http://45.137.192.196:8000/docs`

