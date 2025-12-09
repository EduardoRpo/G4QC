# 📊 Instrumentos Soportados por IB Gateway

## ✅ Confirmación: Todos los Instrumentos se Obtienen desde IB Gateway

**Interactive Brokers Gateway** (y TWS) soporta **todos** los tipos de instrumentos que mencionaste a través de su API.

---

## 🔷 FUTUROS (FUT)

### ✅ Soportado por IB Gateway

**Todos los futuros que mencionaste:**
- **ES** (E-mini S&P 500) - CME
- **NQ** (E-mini NASDAQ-100) - CME
- **CL** (Crude Oil) - NYMEX

**Y muchos más:**
- CME: YM, RTY, EC, 6B, 6E, 6J, etc.
- NYMEX: NG, RB, HO, GC, SI, HG, etc.
- CBOT: ZB, ZN, ZF, ZT, ZS, ZW, ZC, KE, etc.

**Exchange**: CME, NYMEX, COMEX, CBOT, etc.
**Requisito**: Necesita `contract_month` (mes de vencimiento)

---

## 📈 ETFs y STOCKS (STK)

### ✅ Soportado por IB Gateway

**Todos los ETFs que mencionaste:**
- **SPY** - SPDR S&P 500 ETF
- **QQQ** - Invesco QQQ Trust
- **TLT** - iShares 20+ Year Treasury Bond ETF

**Y cualquier stock/ETF listado en:**
- NYSE (New York Stock Exchange)
- NASDAQ
- AMEX
- Y otros exchanges principales

**Exchange**: "SMART" (IB encuentra automáticamente el mejor exchange)
**Requisito**: No necesita `contract_month`

---

## 💱 FOREX (CASH)

### ✅ Soportado por IB Gateway

**Todos los pares de forex que mencionaste:**
- **EURUSD** - Euro / US Dollar
- **GBPUSD** - British Pound / US Dollar
- **AUDUSD** - Australian Dollar / US Dollar

**Y muchos más:**
- USDJPY, USDCAD, USDCHF, NZDUSD
- EURGBP, EURJPY, GBPJPY, AUDJPY
- Y prácticamente cualquier par de divisas mayor

**Exchange**: "IDEALPRO" (plataforma de forex de IB)
**Requisito**: No necesita `contract_month`

**Nota**: Para forex, el símbolo debe ser de 6 letras (CURRENCY1CURRENCY2)

---

## 🔌 Cómo Funciona con IB Gateway

### IB Gateway vs TWS

- **IB Gateway**: Versión ligera, solo para API (lo que estás usando)
- **TWS (Trader Workstation)**: Versión completa con interfaz gráfica

**Ambos soportan los mismos tipos de instrumentos a través de la API.**

### Requisitos de Cuenta

Para obtener datos históricos de IB Gateway necesitas:

1. **Cuenta de IB activa** (Paper Trading o Live)
2. **IB Gateway ejecutándose** (ya lo tienes configurado)
3. **Permisos de datos**:
   - **Futuros**: Requiere suscripción a datos de futuros (normalmente incluida)
   - **Stocks/ETFs**: Requiere suscripción a datos de mercado (puede tener costos)
   - **Forex**: Datos de forex generalmente incluidos

### Suscripciones de Datos

**Gratis (incluidas):**
- Datos de futuros (CME, NYMEX, etc.)
- Datos de forex (IDEALPRO)
- Algunos datos de stocks básicos

**Pueden tener costo:**
- Datos de stocks/ETFs en tiempo real de ciertos exchanges
- Datos históricos de algunos exchanges premium

**Nota**: Para Paper Trading, generalmente tienes acceso a datos de prueba que son suficientes para desarrollo.

---

## 📋 Resumen de Soporte

| Tipo | Ejemplos | Exchange IB | Requiere Suscripción | Soportado |
|------|----------|-------------|---------------------|-----------|
| **Futuros** | ES, NQ, CL | CME, NYMEX, etc. | ✅ Incluida | ✅ Sí |
| **ETFs** | SPY, QQQ, TLT | SMART | ⚠️ Puede tener costo | ✅ Sí |
| **Forex** | EURUSD, GBPUSD | IDEALPRO | ✅ Incluida | ✅ Sí |

---

## 🧪 Cómo Verificar Disponibilidad

### Opción 1: Probar desde el Frontend

1. Inicia el frontend
2. Ve a "Extracción Manual de Datos"
3. Prueba cada símbolo:
   - ES (futuro)
   - SPY (ETF)
   - EURUSD (forex)
4. Si obtienes datos, está disponible

### Opción 2: Verificar en IB Gateway

1. Abre IB Gateway
2. Ve a "Market Data Subscriptions"
3. Verifica qué suscripciones tienes activas

### Opción 3: Probar desde Swagger

```bash
# Probar ETF
curl -X POST "http://localhost:8000/api/v1/data/extract" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "SPY", "duration": "1 D", "bar_size": "1 min", "num_blocks": 1}'

# Probar Forex
curl -X POST "http://localhost:8000/api/v1/data/extract" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "EURUSD", "duration": "1 D", "bar_size": "1 min", "num_blocks": 1}'
```

---

## ⚠️ Consideraciones Importantes

### 1. Suscripciones de Datos

- **Futuros**: Generalmente incluidos ✅
- **Forex**: Generalmente incluidos ✅
- **Stocks/ETFs**: Pueden requerir suscripción adicional ⚠️

### 2. Límites de Datos Históricos

IB tiene límites en la cantidad de datos históricos que puedes solicitar:
- **1 minuto**: Máximo ~1 año de datos
- **5 minutos**: Más datos disponibles
- **1 hora/día**: Datos históricos extensos

### 3. Horarios de Mercado

- **Futuros**: Disponibles casi 24/7 (depende del contrato)
- **Stocks/ETFs**: Solo durante horario de mercado (9:30 AM - 4:00 PM ET)
- **Forex**: Disponible 24/5 (lunes a viernes)

### 4. Paper Trading vs Live

- **Paper Trading**: Datos de prueba (suficientes para desarrollo)
- **Live Trading**: Datos reales (pueden requerir suscripciones adicionales)

---

## ✅ Conclusión

**SÍ, todos los instrumentos que mencionaste se pueden obtener desde IB Gateway:**

- ✅ **Futuros (ES, NQ, CL)**: Soportados
- ✅ **ETFs (SPY, QQQ, TLT)**: Soportados
- ✅ **Forex (EURUSD, GBPUSD, AUDUSD)**: Soportados

El código que implementamos detecta automáticamente el tipo y configura los parámetros correctos para cada uno.

---

## 🧪 Próximo Paso: Probar

Te recomiendo probar cada tipo desde el frontend para confirmar que:
1. IB Gateway está respondiendo
2. Tienes las suscripciones necesarias
3. Los datos se extraen correctamente

¿Quieres que probemos algún símbolo específico ahora? 🚀

