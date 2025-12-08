# 🧪 Plan de Validación - G4QC Trading Platform

## 🎯 Objetivo

Validar que todos los componentes funcionan correctamente antes de continuar con el desarrollo.

---

## 📋 Checklist de Validación

### ✅ Paso 1: Verificar Configuración Básica
- [ ] Verificar que todos los servicios Docker estén corriendo
- [ ] Verificar configuración de Paper Trading
- [ ] Verificar conexión a base de datos

### ✅ Paso 2: Verificar Conexión a IB Gateway
- [ ] Probar conexión básica a IB Gateway
- [ ] Verificar que IB Gateway esté respondiendo

### ✅ Paso 3: Verificar Endpoints Básicos de la API
- [ ] `GET /` - Información de la API
- [ ] `GET /health` - Health check
- [ ] `GET /docs` - Documentación Swagger

### ✅ Paso 4: Validar Extracción de Datos
- [ ] Probar endpoint `POST /api/v1/data/extract` con datos simples
- [ ] Verificar que se conecte a IB Gateway
- [ ] Verificar que extraiga datos correctamente
- [ ] Verificar que guarde en base de datos

### ✅ Paso 5: Validar Consulta de Datos
- [ ] Probar endpoint `GET /api/v1/data/symbols`
- [ ] Probar endpoint `GET /api/v1/data/data/{symbol}`
- [ ] Probar endpoint `GET /api/v1/data/timeframes/{symbol}`

---

## 🚀 Orden de Ejecución Recomendado

### **Fase 1: Verificación de Infraestructura** (5 minutos)

```bash
# 1. Verificar servicios Docker
cd /opt/proyectos/G4QC
docker compose ps

# 2. Verificar Paper Trading
bash verificar_paper_trading.sh

# 3. Verificar conectividad básica
docker compose exec backend python -c "
from app.core.config import settings
print(f'IB_HOST: {settings.IB_HOST}')
print(f'IB_PORT: {settings.IB_PORT}')
"
```

### **Fase 2: Prueba de Conexión IB Gateway** (2 minutos)

```bash
# Probar conexión a IB Gateway
docker compose exec backend python test_ib_connection.py
```

### **Fase 3: Prueba de Endpoints Básicos** (3 minutos)

```bash
# Desde tu máquina local o servidor
curl http://TU_SERVIDOR:8000/
curl http://TU_SERVIDOR:8000/health
```

O abre en navegador:
- `http://TU_SERVIDOR:8000/docs` - Documentación Swagger

### **Fase 4: Prueba de Extracción de Datos** (5-10 minutos)

**Opción A: Usar Swagger UI** (Recomendado)
1. Abre: `http://TU_SERVIDOR:8000/docs`
2. Busca: `POST /api/v1/data/extract`
3. Usa este ejemplo:
   ```json
   {
     "symbol": "ES",
     "duration": "1 D",
     "bar_size": "1 min",
     "num_blocks": 1,
     "save_to_db": true
   }
   ```

**Opción B: Usar curl**
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

### **Fase 5: Validar Datos Guardados** (2 minutos)

```bash
# Verificar símbolos disponibles
curl http://TU_SERVIDOR:8000/api/v1/data/symbols

# Verificar datos del símbolo
curl "http://TU_SERVIDOR:8000/api/v1/data/data/ES?timeframe=1min&limit=10"

# Verificar timeframes disponibles
curl http://TU_SERVIDOR:8000/api/v1/data/timeframes/ES
```

---

## 🔧 Script de Validación Automática

Ejecuta el script `validar_completo.sh` para hacer todas las validaciones automáticamente:

```bash
cd /opt/proyectos/G4QC
bash validar_completo.sh
```

---

## ⚠️ Problemas Comunes y Soluciones

### Problema 1: "No se puede conectar a IB Gateway"
**Solución:**
- Verificar que IB Gateway esté corriendo: `docker compose ps ibgateway`
- Verificar logs: `docker compose logs ibgateway --tail 50`
- Verificar puerto: `ss -tulpn | grep 7497`

### Problema 2: "ibapi no está instalado"
**Solución:**
```bash
docker compose exec backend pip install ibapi
docker compose restart backend
```

### Problema 3: "No se obtuvieron datos"
**Solución:**
- Verificar que IB Gateway esté completamente conectado
- Verificar que el símbolo sea correcto (ES, NQ, etc.)
- Verificar logs de IB Gateway para errores

### Problema 4: "Error de base de datos"
**Solución:**
- Verificar que PostgreSQL esté corriendo: `docker compose ps postgres`
- Verificar que las migraciones estén aplicadas:
  ```bash
  docker compose exec backend alembic upgrade head
  ```

---

## ✅ Criterios de Éxito

La validación es exitosa cuando:

1. ✅ Todos los servicios Docker están corriendo
2. ✅ IB Gateway está conectado y funcionando
3. ✅ Los endpoints básicos responden correctamente
4. ✅ Se puede extraer datos desde IB Gateway
5. ✅ Los datos se guardan en la base de datos
6. ✅ Se pueden consultar los datos guardados

---

## 📝 Notas Importantes

- **Paper Trading**: Asegúrate de que siempre estés en modo Paper Trading durante las pruebas
- **Tiempo**: La extracción de datos puede tardar 30 segundos a varios minutos dependiendo de la cantidad
- **Límites de IB**: Interactive Brokers tiene límites en la cantidad de datos históricos que puedes solicitar

---

## 🎯 Próximos Pasos Después de la Validación

Una vez que todo esté validado:

1. ✅ Continuar desarrollando nuevos endpoints
2. ✅ Implementar estrategias de trading
3. ✅ Implementar backtesting
4. ✅ Crear frontend

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs: `docker compose logs [servicio]`
2. Ejecuta el script de validación: `bash validar_completo.sh`
3. Revisa la documentación: `docs/ENDPOINTS_Y_PRUEBAS.md`

