# G4QC Frontend

Frontend de la plataforma G4QC Trading Platform construido con React + TypeScript + Vite.

## 🚀 Inicio Rápido

### Desarrollo Local (sin Docker)

```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

### Con Docker

```bash
# Desde la raíz del proyecto
docker compose up frontend
```

## 📦 Características

- ✅ Dashboard con estado del sistema
- ✅ Control del scheduler (activar/desactivar, configurar)
- ✅ Extracción manual de datos
- ✅ Visualización de datos en tiempo real (tabla y gráfico)
- ✅ Actualización automática del estado cada 5 segundos

## 🔧 Configuración

Crea un archivo `.env` basado en `.env.example`:

```env
VITE_API_URL=http://localhost:8000
```

## 📝 Scripts Disponibles

- `npm run dev` - Inicia servidor de desarrollo
- `npm run build` - Construye para producción
- `npm run preview` - Previsualiza build de producción
- `npm run lint` - Ejecuta linter

## 🎨 Tecnologías

- **React 18** - Framework UI
- **TypeScript** - Tipado estático
- **Vite** - Build tool rápido
- **Tailwind CSS** - Estilos
- **Recharts** - Gráficos
- **Axios** - Cliente HTTP
- **Lucide React** - Iconos

