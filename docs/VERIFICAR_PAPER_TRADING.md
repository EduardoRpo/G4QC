# 🧪 Verificación de Modo Paper Trading

## ⚠️ IMPORTANTE: Seguridad en Pruebas

Este documento explica cómo verificar y asegurar que **IB Gateway está configurado en modo Paper Trading** (cuenta de prueba) y **NO en modo Live Trading** (cuenta real con dinero).

---

## 🔍 Verificación Rápida

### 1. **Verificar Configuración en Docker Compose**

El archivo `docker-compose.yml` debe tener:

```yaml
ibgateway:
  environment:
    - IB_LOGINTYPE=Paper Trading  # ✅ CORRECTO - Paper Trading
    # ❌ NUNCA usar: IB_LOGINTYPE=Live Trading
```

**Ubicación**: `/opt/proyectos/G4QC/docker-compose.yml` (línea 40)

### 2. **Verificar Puerto**

- ✅ **Paper Trading**: Puerto **7497**
- ❌ **Live Trading**: Puerto **7496**

**Verificar en docker-compose.yml**:
```yaml
ports:
  - "7497:4000"  # ✅ Puerto 7497 = Paper Trading
```

**Verificar en el servidor**:
```bash
ss -tulpn | grep 7497  # Debe mostrar que está escuchando
```

### 3. **Verificar Logs de IB Gateway**

Los logs deben mostrar que está usando **Paper Trading**:

```bash
docker compose logs ibgateway | grep -i "paper\|trading\|login"
```

Debe mostrar mensajes como:
- `Paper Trading`
- `Logged into Paper Trading account`
- `IB_LOGINTYPE=Paper Trading`

---

## 📋 Checklist de Verificación Completa

Ejecuta estos comandos para verificar que TODO está configurado para Paper Trading:

```bash
cd /opt/proyectos/G4QC

# 1. Verificar configuración en docker-compose.yml
echo "=== 1. Configuración Docker Compose ==="
grep -A 2 "IB_LOGINTYPE" docker-compose.yml
grep -A 1 "ports:" docker-compose.yml | grep 7497

# 2. Verificar puerto en uso
echo ""
echo "=== 2. Puerto en Uso ==="
ss -tulpn | grep 7497

# 3. Verificar logs de IB Gateway
echo ""
echo "=== 3. Logs de IB Gateway (últimas 50 líneas) ==="
docker compose logs ibgateway --tail 50 | grep -i -E "(paper|trading|login|live)"

# 4. Verificar configuración del backend
echo ""
echo "=== 4. Configuración del Backend ==="
docker compose exec backend python -c "
from app.core.config import settings
print(f'IB_HOST: {settings.IB_HOST}')
print(f'IB_PORT: {settings.IB_PORT}')
print(f'NOTA: Puerto 7497 = Paper Trading, Puerto 7496 = Live Trading')
"
```

---

## 🚨 Señales de Alerta

### ❌ **SEÑALES DE QUE ESTÁS EN MODO LIVE (PELIGROSO)**

1. **Puerto 7496** en uso
   ```bash
   ss -tulpn | grep 7496  # ❌ NO debe aparecer nada
   ```

2. **IB_LOGINTYPE=Live Trading** en docker-compose.yml
   ```bash
   grep "Live Trading" docker-compose.yml  # ❌ NO debe aparecer
   ```

3. **Logs muestran "Live Trading"**
   ```bash
   docker compose logs ibgateway | grep -i "live trading"  # ❌ NO debe aparecer
   ```

### ✅ **SEÑALES DE QUE ESTÁS EN MODO PAPER (CORRECTO)**

1. **Puerto 7497** en uso
   ```bash
   ss -tulpn | grep 7497  # ✅ Debe mostrar docker-proxy
   ```

2. **IB_LOGINTYPE=Paper Trading** en docker-compose.yml
   ```bash
   grep "Paper Trading" docker-compose.yml  # ✅ Debe aparecer
   ```

3. **Logs muestran "Paper Trading"**
   ```bash
   docker compose logs ibgateway | grep -i "paper"  # ✅ Debe aparecer
   ```

---

## 🔧 Cómo Corregir si Está en Modo Live

**Si por error está configurado en modo Live, sigue estos pasos inmediatamente:**

1. **Detener IB Gateway**
   ```bash
   docker compose stop ibgateway
   ```

2. **Editar docker-compose.yml**
   ```bash
   cd /opt/proyectos/G4QC
   nano docker-compose.yml  # o el editor que prefieras
   ```

3. **Cambiar a Paper Trading**
   ```yaml
   environment:
     - IB_LOGINTYPE=Paper Trading  # Cambiar si dice "Live Trading"
   ```

4. **Verificar puerto**
   ```yaml
   ports:
     - "7497:4000"  # Asegurar que sea 7497 (Paper), NO 7496 (Live)
   ```

5. **Reiniciar servicios**
   ```bash
   docker compose up -d ibgateway
   ```

6. **Verificar que está en Paper Trading**
   ```bash
   docker compose logs ibgateway --tail 50 | grep -i paper
   ```

---

## 📝 Notas Importantes

### Diferencia entre Paper y Live Trading

| Característica | Paper Trading | Live Trading |
|----------------|---------------|--------------|
| **Puerto** | 7497 | 7496 |
| **Dinero** | Virtual (simulado) | Real |
| **Riesgo** | Ninguno | REAL - Puedes perder dinero |
| **Uso** | Pruebas, desarrollo | Producción |
| **Configuración** | `IB_LOGINTYPE=Paper Trading` | `IB_LOGINTYPE=Live Trading` |

### Por Qué Es Importante

- ❌ **En modo Live**: Cualquier orden se ejecuta con dinero REAL
- ✅ **En modo Paper**: Todas las órdenes son simuladas, no hay riesgo

**Siempre usa Paper Trading durante el desarrollo y las pruebas.**

---

## 🧪 Script de Verificación Automática

Crea este script para verificar automáticamente:

```bash
#!/bin/bash
# verificar_paper_trading.sh

echo "🔍 Verificando configuración de Paper Trading..."
echo ""

# Verificar docker-compose.yml
if grep -q "IB_LOGINTYPE=Paper Trading" /opt/proyectos/G4QC/docker-compose.yml; then
    echo "✅ docker-compose.yml: Paper Trading configurado"
else
    echo "❌ ERROR: docker-compose.yml NO tiene Paper Trading configurado"
    exit 1
fi

# Verificar puerto
if ss -tulpn | grep -q ":7497"; then
    echo "✅ Puerto 7497 (Paper Trading) está en uso"
else
    echo "❌ ERROR: Puerto 7497 no está en uso"
    exit 1
fi

# Verificar que NO esté usando puerto 7496 (Live)
if ss -tulpn | grep -q ":7496"; then
    echo "❌ PELIGRO: Puerto 7496 (Live Trading) está en uso!"
    exit 1
else
    echo "✅ Puerto 7496 (Live Trading) NO está en uso"
fi

echo ""
echo "✅ Todo está configurado correctamente para Paper Trading"
```

---

## 📞 Soporte

Si tienes dudas sobre la configuración, verifica:
1. Este documento
2. Los logs de IB Gateway
3. La configuración en `docker-compose.yml`

**NUNCA uses Live Trading sin estar 100% seguro de lo que estás haciendo.**

