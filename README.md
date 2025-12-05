# G4QC Trading Platform

Plataforma web para desarrollo, backtesting, optimización y ejecución de estrategias de trading automatizado.

## 🏗️ Arquitectura

- **Backend**: FastAPI (Python)
- **Frontend**: React + TypeScript (próximamente)
- **Base de Datos**: PostgreSQL + TimescaleDB
- **Cache**: Redis
- **Brokers**: Interactive Brokers, MetaTrader 5

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker y Docker Compose
- Python 3.11+ (para desarrollo local)
- Interactive Brokers TWS o IB Gateway ejecutándose (puerto 7497 para paper trading)

### Instalación

1. **Clonar y configurar entorno**

```bash
cd G4QC
cp backend/.env.example backend/.env
# Editar backend/.env con tus configuraciones
```

2. **Iniciar servicios con Docker**

```bash
docker-compose up -d
```

Esto iniciará:
- PostgreSQL (puerto 5432)
- Redis (puerto 6379)
- Backend API (puerto 8000)

3. **Crear base de datos y tablas**

```bash
# Entrar al contenedor del backend
docker-compose exec backend bash

# Crear migraciones
alembic revision --autogenerate -m "Initial migration"

# Aplicar migraciones
alembic upgrade head
```

4. **Acceder a la API**

- API: http://localhost:8000
- Documentación: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## 📖 Uso de la API

### Extraer datos históricos

```bash
curl -X POST "http://localhost:8000/api/v1/data/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "ES",
    "duration": "1 M",
    "bar_size": "1 min",
    "contract_month": "202512",
    "num_blocks": 1
  }'
```

### Consultar datos

```bash
# Obtener datos de un símbolo
curl "http://localhost:8000/api/v1/data/data/ES?timeframe=1min&limit=100"

# Listar símbolos disponibles
curl "http://localhost:8000/api/v1/data/symbols"

# Listar timeframes disponibles
curl "http://localhost:8000/api/v1/data/timeframes/ES"
```

## 📁 Estructura del Proyecto

```
G4QC/
├── backend/              # Backend FastAPI
│   ├── app/
│   │   ├── api/         # Endpoints API
│   │   ├── core/        # Configuración y base de datos
│   │   ├── models/      # Modelos SQLAlchemy
│   │   └── services/    # Lógica de negocio
│   ├── alembic/         # Migraciones de base de datos
│   └── requirements.txt
├── frontend/            # Frontend React (próximamente)
├── Data/                # Datos y notebooks originales
└── docker-compose.yml   # Configuración Docker
```

## 🔧 Desarrollo

### Backend local (sin Docker)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configurar .env
cp .env.example .env

# Ejecutar
uvicorn app.main:app --reload
```

### Migraciones de base de datos

```bash
# Crear nueva migración
alembic revision --autogenerate -m "Description"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1
```

## 📝 Estado del Proyecto

### ✅ Completado (MVP Fase 1)
- [x] Estructura base del proyecto
- [x] Configuración Docker
- [x] Modelos de base de datos
- [x] Servicio de extracción IB (refactorizado del notebook)
- [x] API REST para extracción y consulta de datos
- [x] Procesamiento de timeframes

### 🚧 En desarrollo
- [ ] Migraciones Alembic
- [ ] Testing
- [ ] Frontend React

### 📋 Próximos pasos
- [ ] Backtesting engine
- [ ] Optimización de parámetros
- [ ] Análisis de portfolio
- [ ] Trading en vivo

## 📚 Documentación

- [Propuesta de Arquitectura](PROPUESTA_ARQUITECTURA.md)
- [Plan de Implementación](PLAN_IMPLEMENTACION.md)

## ⚠️ Notas Importantes

- Asegúrate de que Interactive Brokers TWS/Gateway esté ejecutándose antes de extraer datos
- El puerto por defecto es 7497 (paper trading) o 7496 (live trading)
- Los datos se almacenan en PostgreSQL con particionado temporal (TimescaleDB)

## 📄 Licencia

[Especificar licencia]

