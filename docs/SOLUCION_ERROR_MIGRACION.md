# 🔧 Solución al Error de Migración

## Problema

La migración falló al intentar crear el hypertable de TimescaleDB, dejando la transacción en un estado inconsistente.

## ✅ Solución Aplicada

He simplificado la migración para que **NO intente crear el hypertable automáticamente**. La tabla funciona perfectamente sin TimescaleDB.

## 🚀 Pasos para Resolver

### Paso 1: Limpiar el estado de migración fallido

Primero, necesitamos resetear el estado de Alembic:

```powershell
# Entrar al contenedor
docker-compose exec backend bash

# Dentro del contenedor, verificar estado
alembic current

# Si hay un estado inconsistente, resetearlo
# Salir del contenedor primero
exit
```

### Paso 2: Eliminar la tabla si existe (empezar limpio)

```powershell
# Conectarse a PostgreSQL y eliminar tabla si existe
docker-compose exec postgres psql -U g4qc -d g4qc_db -c "DROP TABLE IF EXISTS market_data CASCADE;"
docker-compose exec postgres psql -U g4qc -d g4qc_db -c "DROP TABLE IF EXISTS alembic_version CASCADE;"
```

### Paso 3: Reconstruir el backend con la migración corregida

```powershell
# Reconstruir solo el backend
docker-compose up -d --build backend
```

### Paso 4: Ejecutar la migración corregida

```powershell
docker-compose exec backend alembic upgrade head
```

Ahora debería funcionar sin errores.

---

## ✅ Alternativa Más Rápida (Recomendada)

Si quieres empezar completamente limpio:

```powershell
# Detener todo
docker-compose down -v

# Esto eliminará TODOS los volúmenes (base de datos incluida)
# Luego reinicia todo limpio
docker-compose up -d --build

# Espera que se inicie, luego aplica migraciones
docker-compose exec backend alembic upgrade head
```

---

## 🎯 Verificar que Funcionó

```powershell
# Verificar que la tabla existe
docker-compose exec postgres psql -U g4qc -d g4qc_db -c "\dt"

# Deberías ver: market_data
```

---

## 📝 Nota sobre TimescaleDB

- **La tabla funciona perfectamente sin TimescaleDB**
- Los índices optimizados están creados
- Si más adelante quieres usar TimescaleDB, puedes convertirlo manualmente
- Para desarrollo y pruebas, no es necesario

---

**Recomendación:** Usa la alternativa más rápida (`docker-compose down -v`) para empezar limpio.

