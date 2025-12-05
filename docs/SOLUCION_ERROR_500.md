# 🔧 Solución al Error 500 - ibapi no instalado

## Problema Identificado

El error 500 ocurre porque **ibapi no está instalado** en el contenedor Docker. El endpoint de extracción de datos lo requiere.

## ✅ Solución: Instalar ibapi

### Opción 1: Instalar ibapi en el contenedor (Recomendado)

```powershell
docker-compose exec backend pip install ibapi
```

Esto instalará la versión disponible de ibapi.

### Opción 2: Verificar qué versión está disponible

```powershell
docker-compose exec backend pip search ibapi
```

O simplemente intenta instalar:
```powershell
docker-compose exec backend pip install ibapi
```

---

## 📋 Pasos Completos

### 1. Instalar ibapi

```powershell
docker-compose exec backend pip install ibapi
```

### 2. Verificar instalación

```powershell
docker-compose exec backend python -c "import ibapi; print('ibapi instalado correctamente')"
```

### 3. Reiniciar el backend (para cargar el módulo)

```powershell
docker-compose restart backend
```

### 4. Probar de nuevo

Vuelve a `/docs` y prueba el endpoint de extracción.

---

## ⚠️ Nota Importante

**Para que la extracción funcione completamente, también necesitas:**

1. ✅ ibapi instalado (lo estás haciendo ahora)
2. ⏸️ Interactive Brokers TWS o IB Gateway ejecutándose
3. ⏸️ Configurado en el puerto correcto (7497 para paper, 7496 para live)

---

## 🎯 Estado Actual

- ✅ API funcionando
- ✅ Base de datos lista
- ⏸️ ibapi necesita instalarse
- ⏸️ IB TWS necesita estar ejecutándose (para extraer datos)

---

## 💡 Alternativa: Probar otros endpoints

Mientras instalas ibapi, puedes probar:

- ✅ `GET /health` - Funciona
- ✅ `GET /api/v1/data/symbols` - Funciona (retorna lista vacía)
- ✅ `GET /docs` - Funciona
- ⏸️ `POST /api/v1/data/extract` - Requiere ibapi

---

**Ejecuta:** `docker-compose exec backend pip install ibapi`

