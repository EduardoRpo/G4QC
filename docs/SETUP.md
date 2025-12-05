# Guía de Setup - G4QC Trading Platform

## 🚀 Inicio Rápido

### Opción 1: Docker (Recomendado)

1. **Configurar variables de entorno**

```bash
cd G4QC
cp backend/.env.example backend/.env
```

Editar `backend/.env` con tus configuraciones (especialmente IB_HOST, IB_PORT si no usas defaults).

2. **Iniciar servicios**

```bash
docker-compose up -d
```

3. **Inicializar base de datos**

```bash
# Opción A: Usar Alembic (recomendado)
docker-compose exec backend alembic upgrade head

# Opción B: Usar script Python
docker-compose exec backend python scripts/init_db.py
```

4. **Verificar que todo funciona**

```bash
# Health check
curl http://localhost:8000/health

# Ver logs
docker-compose logs -f backend
```

### Opción 2: Desarrollo Local (sin Docker)

1. **Instalar PostgreSQL y Redis localmente**

- PostgreSQL 15+ con extensión TimescaleDB
- Redis 7+

2. **Crear entorno virtual**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configurar .env**

```bash
cp .env.example .env
# Editar .env con tu DATABASE_URL local
```

4. **Inicializar base de datos**

```bash
# Con Alembic
alembic upgrade head

# O con script
python scripts/init_db.py
```

5. **Ejecutar servidor**

```bash
uvicorn app.main:app --reload
```

## 📋 Verificación

### 1. Verificar que la API funciona

```bash
curl http://localhost:8000/health
```

Debería retornar: `{"status":"healthy"}`

### 2. Ver documentación de la API

Abrir en navegador: http://localhost:8000/docs

### 3. Probar extracción de datos (requiere IB TWS/Gateway)

```bash
curl -X POST "http://localhost:8000/api/v1/data/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "ES",
    "duration": "3600 S",
    "bar_size": "1 min",
    "num_blocks": 1
  }'
```

**Nota**: Asegúrate de que Interactive Brokers TWS o IB Gateway esté ejecutándose en el puerto configurado (7497 por defecto para paper trading).

## 🔧 Troubleshooting

### Error: "Connection refused" al conectar con IB

- Verifica que TWS o IB Gateway esté ejecutándose
- Verifica el puerto en `backend/.env` (7497 para paper, 7496 para live)
- Verifica que el host sea correcto (127.0.0.1 para local)

### Error: "TimescaleDB extension not found"

- No es crítico, la aplicación funcionará sin TimescaleDB
- Para habilitarlo, instala TimescaleDB en PostgreSQL:
  ```bash
  # En PostgreSQL
  CREATE EXTENSION IF NOT EXISTS timescaledb;
  ```

### Error: "Table already exists" en migraciones

```bash
# Ver estado de migraciones
docker-compose exec backend alembic current

# Si hay conflictos, puedes marcar como aplicada
docker-compose exec backend alembic stamp head
```

### Error: "Module not found" en Python

```bash
# Reinstalar dependencias
docker-compose exec backend pip install -r requirements.txt
```

## 📝 Próximos Pasos

Una vez que el setup esté completo:

1. ✅ Extraer datos de prueba desde IB
2. ✅ Verificar que se guardan en PostgreSQL
3. ✅ Consultar datos vía API
4. 🚧 Implementar frontend React
5. 🚧 Agregar motor de backtesting

## 🔗 Enlaces Útiles

- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Interactive Brokers API: https://interactivebrokers.github.io/tws-api/

