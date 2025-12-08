# 🚀 ¿Qué Hacer Ahora? - Guía Rápida

## ✅ Estado Actual

- ✅ IB Gateway configurado y corriendo en modo Paper Trading
- ✅ Backend configurado para conectarse a IB Gateway
- ✅ Base de datos y Redis funcionando
- ✅ Scripts de verificación creados

---

## 🎯 Próximos Pasos Recomendados

### **Paso 1: Validar que Todo Funciona** (15 minutos)

Ejecuta el script de validación completa desde el servidor:

```bash
cd /opt/proyectos/G4QC

# Opción A: Validación completa automática
bash validar_completo.sh

# Opción B: Validación paso a paso manual
```

**O sigue estos pasos manuales:**

#### 1.1 Verificar Servicios
```bash
docker compose ps
# Debe mostrar: postgres, redis, backend, ibgateway todos "Up"
```

#### 1.2 Verificar Paper Trading
```bash
bash verificar_paper_trading.sh
# Debe mostrar que todo está configurado para Paper Trading
```

#### 1.3 Probar Conexión a IB Gateway

Primero, asegúrate de que el script de prueba esté en el backend:

```bash
# Copiar el script al backend si no está
cp test_ib_connection.py backend/

# Probar conexión
docker compose exec backend python test_ib_connection.py
```

#### 1.4 Probar Endpoints Básicos

Desde tu máquina local o servidor:

```bash
# Ver información de la API
curl http://TU_SERVIDOR:8000/

# Ver health check
curl http://TU_SERVIDOR:8000/health

# Abrir documentación Swagger en navegador
# http://TU_SERVIDOR:8000/docs
```

---

### **Paso 2: Probar Extracción de Datos** (10-15 minutos)

Una vez que las validaciones básicas pasen, prueba extraer datos reales.

#### Opción A: Usar Swagger UI (Más Fácil)

1. Abre en navegador: `http://TU_SERVIDOR:8000/docs`
2. Busca el endpoint: `POST /api/v1/data/extract`
3. Haz clic en "Try it out"
4. Usa estos datos de ejemplo:
   ```json
   {
     "symbol": "ES",
     "duration": "1 D",
     "bar_size": "1 min",
     "num_blocks": 1,
     "save_to_db": true
   }
   ```
5. Haz clic en "Execute"
6. Espera la respuesta (puede tardar 30 segundos a varios minutos)

#### Opción B: Usar curl

```bash
curl -X POST "http://TU_SERVIDOR:8000/api/v1/data/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "ES",
    "duration": "1 D",
    "bar_size": "1 min",
    "num_blocks": 1,
    "save_to_db": true
  }'
```

**Símbolos disponibles para probar:**
- `ES` - E-mini S&P 500
- `NQ` - E-mini NASDAQ-100
- `EC` - Euro Currency Futures
- `6B` - British Pound Futures

---

### **Paso 3: Verificar Datos Guardados** (2 minutos)

Una vez que hayas extraído datos, verifica que se guardaron:

```bash
# Ver símbolos disponibles
curl http://TU_SERVIDOR:8000/api/v1/data/symbols

# Ver datos del símbolo ES
curl "http://TU_SERVIDOR:8000/api/v1/data/data/ES?timeframe=1min&limit=10"

# Ver timeframes disponibles
curl http://TU_SERVIDOR:8000/api/v1/data/timeframes/ES
```

---

## 📋 Orden Recomendado de Validación

1. ✅ **Validar infraestructura** (servicios Docker, Paper Trading)
2. ✅ **Probar conexión IB Gateway** (test_ib_connection.py)
3. ✅ **Probar endpoints básicos** (GET /, GET /health)
4. ✅ **Probar extracción de datos** (POST /api/v1/data/extract)
5. ✅ **Verificar datos guardados** (GET /api/v1/data/data/{symbol})

---

## 🎯 Después de Validar

Una vez que todo funcione:

1. ✅ **Continúa desarrollando endpoints adicionales**
2. ✅ **Implementa estrategias de trading**
3. ✅ **Implementa backtesting**
4. ✅ **Crea el frontend**

---

## 🔧 Comandos Útiles

### Ver logs de servicios
```bash
# Logs de IB Gateway
docker compose logs ibgateway --tail 50

# Logs del backend
docker compose logs backend --tail 50

# Logs de todos los servicios
docker compose logs --tail 50
```

### Reiniciar servicios
```bash
# Reiniciar todo
docker compose restart

# Reiniciar solo el backend
docker compose restart backend

# Reiniciar solo IB Gateway
docker compose restart ibgateway
```

### Ver estado de servicios
```bash
docker compose ps
```

---

## 📚 Documentación Relacionada

- **Plan de Validación Completo**: `PLAN_VALIDACION.md`
- **Endpoints y Pruebas**: `docs/ENDPOINTS_Y_PRUEBAS.md`
- **Verificación Paper Trading**: `docs/VERIFICAR_PAPER_TRADING.md`

---

## ⚠️ Problemas Comunes

### "No se puede conectar a IB Gateway"
- Verifica que IB Gateway esté corriendo: `docker compose ps ibgateway`
- Verifica logs: `docker compose logs ibgateway --tail 50`
- Verifica puerto: `ss -tulpn | grep 7497`

### "ibapi no está instalado"
```bash
docker compose exec backend pip install ibapi
docker compose restart backend
```

### "Error 503 Service Unavailable"
- Verifica que el backend esté corriendo: `docker compose ps backend`
- Verifica logs: `docker compose logs backend --tail 50`

---

## ✅ Checklist Final

Antes de continuar, asegúrate de que:

- [ ] Todos los servicios Docker están corriendo
- [ ] IB Gateway está configurado para Paper Trading
- [ ] La conexión a IB Gateway funciona (test_ib_connection.py)
- [ ] Los endpoints básicos responden (GET /, GET /health)
- [ ] Puedes extraer datos desde IB Gateway
- [ ] Los datos se guardan en la base de datos
- [ ] Puedes consultar los datos guardados

**Si todos los checkboxes están marcados, ¡estás listo para continuar! 🎉**

