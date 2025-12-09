# 🎨 Frontend G4QC - Instrucciones de Uso

## ✅ Frontend Creado Exitosamente

Se ha creado un frontend completo con React + TypeScript que te permite:

1. **Controlar el Scheduler** - Activar/desactivar y configurar
2. **Extraer Datos Manualmente** - Desde IB Gateway
3. **Visualizar Datos** - Ver datos en tiempo real con gráficos
4. **Validar Visualmente** - Confirmar que los datos se están llenando

---

## 🚀 Cómo Iniciar

### Opción 1: Con Docker (Recomendado)

```bash
# Desde la raíz del proyecto
docker compose up frontend

# O iniciar todo junto
docker compose up
```

El frontend estará disponible en: **http://localhost:5173**

### Opción 2: Desarrollo Local

```bash
cd frontend
npm install
npm run dev
```

---

## 📋 Funcionalidades del Frontend

### 1. Dashboard
- Estado del scheduler (activo/inactivo)
- Jobs activos
- Última ejecución
- Próxima ejecución programada
- Configuración actual (intervalo, horario, símbolos, timeframes)

### 2. Control del Scheduler
- **Activar/Desactivar** - Botón para controlar el scheduler
- **Ejecutar Ahora** - Forzar ejecución inmediata
- **Configuración** - Editar:
  - Intervalo de actualización (minutos)
  - Horario de mercado (inicio/fin)
  - Símbolos a actualizar
  - Timeframes a extraer

### 3. Extracción Manual
- Formulario para extraer datos manualmente
- Campos:
  - Símbolo (ES, NQ, YM, etc.)
  - Duración (1 D, 1 W, 1 M, 3 M)
  - Tamaño de barra (1 min, 5 mins, 15 mins, 1 hour)
  - Número de bloques
  - Mes de contrato (opcional)

### 4. Visualización de Datos
- **Gráfico en tiempo real** - Muestra últimos 50 registros
- **Tabla de datos** - Últimos 20 registros con OHLCV
- **Selector de símbolo** - Ver datos de diferentes símbolos
- **Selector de timeframe** - Cambiar entre 1min, 5min, etc.
- **Actualización automática** - Botón para refrescar datos

---

## 🎯 Flujo de Validación

### Paso 1: Activar el Scheduler
1. Abre el frontend en http://localhost:5173
2. Ve a "Control del Scheduler"
3. Haz clic en "Activar Scheduler"
4. Verifica que el estado cambie a "Activo"

### Paso 2: Configurar el Scheduler
1. Haz clic en "Mostrar Configuración"
2. Ajusta los parámetros:
   - Intervalo: 1 minuto (para pruebas rápidas)
   - Horario: 09:00 - 16:00
   - Símbolos: ES, NQ
   - Timeframes: 1min
3. Haz clic en "Actualizar Configuración"

### Paso 3: Validar que se Llenan Datos
1. Ve a "Visualización de Datos"
2. Selecciona un símbolo (ej: ES)
3. Selecciona timeframe (ej: 1min)
4. Observa que los datos aparecen en la tabla y gráfico
5. Haz clic en "Actualizar" periódicamente para ver nuevos datos

### Paso 4: Extracción Manual (Opcional)
1. Ve a "Extracción Manual de Datos"
2. Completa el formulario:
   - Símbolo: ES
   - Duración: 1 D
   - Tamaño: 1 min
   - Bloques: 1
3. Haz clic en "Extraer Datos"
4. Espera la confirmación
5. Verifica en "Visualización de Datos" que aparecen los nuevos datos

---

## 🔧 Configuración

### Variables de Entorno

Crea un archivo `.env` en la carpeta `frontend/`:

```env
VITE_API_URL=http://localhost:8000
```

Para producción, cambia a la URL de tu servidor.

### Proxy en Desarrollo

El frontend está configurado para hacer proxy de `/api` al backend en desarrollo.

---

## 🐛 Solución de Problemas

### El frontend no se conecta al backend
- Verifica que el backend esté corriendo en el puerto 8000
- Revisa la variable `VITE_API_URL` en `.env`
- Verifica los logs: `docker compose logs frontend`

### No se ven datos
- Verifica que el scheduler esté activo
- Asegúrate de que haya datos en la base de datos
- Revisa los logs del backend: `docker compose logs backend`

### Error de CORS
- El backend ya tiene CORS configurado para `localhost:5173`
- Si usas otra URL, actualiza `CORS_ORIGINS` en el backend

---

## 📝 Próximos Pasos

Una vez que valides que:
- ✅ El scheduler funciona
- ✅ Los datos se llenan automáticamente
- ✅ Puedes visualizar los datos

**Estaremos listos para implementar el motor de backtesting!** 🚀

---

## 🎨 Tecnologías Usadas

- **React 18** - Framework UI
- **TypeScript** - Tipado estático
- **Vite** - Build tool
- **Tailwind CSS** - Estilos
- **Recharts** - Gráficos
- **Axios** - Cliente HTTP
- **Lucide React** - Iconos

---

¡Listo para usar! 🎉

