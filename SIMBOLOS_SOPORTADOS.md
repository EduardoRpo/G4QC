# 📊 Símbolos Soportados - G4QC Trading Platform

## ✅ Símbolos Actualmente Soportados

La aplicación detecta **automáticamente** el tipo de instrumento basado en el símbolo. No necesitas especificar el tipo manualmente.

---

## 🔷 FUTUROS (FUT)

### CME (Chicago Mercantile Exchange)
- **ES** - E-mini S&P 500
- **NQ** - E-mini NASDAQ-100
- **YM** - E-mini Dow Jones
- **RTY** - E-mini Russell 2000
- **EC** - Euro FX Futures
- **6E** - Euro FX Futures (alternativo)
- **6B** - British Pound Futures
- **6J** - Japanese Yen Futures
- **6A** - Australian Dollar Futures
- **6C** - Canadian Dollar Futures
- **6S** - Swiss Franc Futures
- **6N** - New Zealand Dollar Futures
- **6M** - Mexican Peso Futures

### NYMEX (New York Mercantile Exchange)
- **CL** - Crude Oil Futures
- **NG** - Natural Gas Futures
- **RB** - RBOB Gasoline Futures
- **HO** - Heating Oil Futures

### COMEX (Commodity Exchange)
- **GC** - Gold Futures
- **SI** - Silver Futures
- **HG** - Copper Futures
- **PA** - Palladium Futures
- **PL** - Platinum Futures

### CBOT (Chicago Board of Trade)
- **ZB** - 30-Year Treasury Bond Futures
- **ZN** - 10-Year Treasury Note Futures
- **ZF** - 5-Year Treasury Note Futures
- **ZT** - 2-Year Treasury Note Futures
- **ZS** - Soybean Futures
- **ZW** - Wheat Futures
- **ZC** - Corn Futures
- **KE** - Hard Red Winter Wheat Futures

### Otros
- **LE** - Live Cattle Futures
- **HE** - Lean Hogs Futures

**Nota para Futuros**: Se calcula automáticamente el `contract_month` (mes de vencimiento) si no se especifica.

---

## 📈 ETFs y STOCKS (STK)

- **SPY** - SPDR S&P 500 ETF
- **QQQ** - Invesco QQQ Trust (NASDAQ-100)
- **TLT** - iShares 20+ Year Treasury Bond ETF
- **IWM** - iShares Russell 2000 ETF
- **DIA** - SPDR Dow Jones Industrial Average ETF
- **GLD** - SPDR Gold Trust
- **SLV** - iShares Silver Trust
- **USO** - United States Oil Fund
- **XLF** - Financial Select Sector SPDR Fund
- **XLE** - Energy Select Sector SPDR Fund

**Nota para ETFs/Stocks**: 
- No requieren `contract_month`
- Usan exchange "SMART" (IB encuentra automáticamente el mejor exchange)
- Cualquier símbolo de hasta 5 letras se trata como stock/ETF

---

## 💱 FOREX (CASH)

- **EURUSD** - Euro / US Dollar
- **GBPUSD** - British Pound / US Dollar
- **AUDUSD** - Australian Dollar / US Dollar
- **USDJPY** - US Dollar / Japanese Yen
- **USDCAD** - US Dollar / Canadian Dollar
- **USDCHF** - US Dollar / Swiss Franc
- **NZDUSD** - New Zealand Dollar / US Dollar
- **EURGBP** - Euro / British Pound
- **EURJPY** - Euro / Japanese Yen
- **GBPJPY** - British Pound / Japanese Yen
- **AUDJPY** - Australian Dollar / Japanese Yen
- **EURAUD** - Euro / Australian Dollar
- **EURCAD** - Euro / Canadian Dollar

**Nota para Forex**:
- Formato: CURRENCY1CURRENCY2 (6 letras, ej: EURUSD)
- No requieren `contract_month`
- Usan exchange "IDEALPRO"
- El símbolo se divide automáticamente (EURUSD → symbol=EUR, currency=USD)

---

## 🎯 Cómo Funciona la Detección Automática

1. **Forex**: Si el símbolo tiene 6 letras y es un par conocido → `CASH`
2. **ETFs/Stocks**: Si el símbolo tiene ≤5 letras y es conocido o alfanumérico → `STK`
3. **Futuros**: Si el símbolo está en la lista de futuros conocidos → `FUT`
4. **Por defecto**: Si no se reconoce, se asume `FUT` en CME

---

## 📝 Ejemplos de Uso

### Futuro (ES)
```json
{
  "symbol": "ES",
  "duration": "1 D",
  "bar_size": "1 min",
  "num_blocks": 1
}
```
✅ `contract_month` se calcula automáticamente

### ETF (SPY)
```json
{
  "symbol": "SPY",
  "duration": "1 D",
  "bar_size": "1 min",
  "num_blocks": 1
}
```
✅ No necesita `contract_month`

### Forex (EURUSD)
```json
{
  "symbol": "EURUSD",
  "duration": "1 D",
  "bar_size": "1 min",
  "num_blocks": 1
}
```
✅ No necesita `contract_month`

---

## ⚙️ Configuración del Scheduler

Puedes configurar el scheduler para actualizar automáticamente cualquier combinación:

```json
{
  "symbols": ["ES", "NQ", "SPY", "QQQ", "EURUSD", "GBPUSD"],
  "timeframes": ["1min"],
  "update_interval_minutes": 1,
  "market_hours_start": "09:00",
  "market_hours_end": "16:00"
}
```

El scheduler detectará automáticamente el tipo de cada símbolo y usará los parámetros correctos.

---

## 🔧 Agregar Nuevos Símbolos

Si quieres agregar soporte para nuevos símbolos, edita el método `detect_instrument_type()` en:
`backend/app/services/data_extraction/ib_extractor.py`

Agrega el símbolo a la lista correspondiente (futures_cme, futures_nymex, etfs, forex_pairs).

---

## ✅ Resumen

| Tipo | Símbolos Ejemplo | Requiere contract_month | Exchange |
|------|------------------|-------------------------|----------|
| **Futuros** | ES, NQ, CL | ✅ Sí (auto) | CME, NYMEX, COMEX, CBOT |
| **ETFs/Stocks** | SPY, QQQ, TLT | ❌ No | SMART |
| **Forex** | EURUSD, GBPUSD | ❌ No | IDEALPRO |

---

¡La aplicación ahora soporta todos los tipos de instrumentos que mencionaste! 🎉

