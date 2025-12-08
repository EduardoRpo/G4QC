# 📖 Explicación de Parámetros - Extracción de Datos

## 🎯 ¿Qué estás pidiendo con este JSON?

```json
{
  "symbol": "ES",
  "duration": "1 D",
  "bar_size": "1 min",
  "num_blocks": 1,
  "save_to_db": true
}
```

Este JSON le dice a la API: **"Quiero extraer datos históricos del futuro E-mini S&P 500 (ES) del último día, con barras de 1 minuto, en 1 bloque, y guardar los datos en la base de datos."**

---

## 📋 Explicación Detallada de Cada Parámetro

### 1. `"symbol": "ES"` ⭐ **REQUERIDO**

**¿Qué es?**
- El símbolo del instrumento financiero que quieres obtener.

**¿Qué significa "ES"?**
- **ES** = E-mini S&P 500 Futures
- Es un futuro del índice S&P 500
- Es uno de los instrumentos más negociados del mundo

**Otros símbolos disponibles:**
- `"NQ"` - E-mini NASDAQ-100 Futures
- `"EC"` - Euro Currency Futures  
- `"6B"` - British Pound Futures
- `"RB"` - RBOB Gasoline Futures
- `"GC"` - Gold Futures
- `"CL"` - Crude Oil Futures
- Y muchos más...

**Ejemplo:**
```json
"symbol": "ES"  // Futuro del S&P 500
```

---

### 2. `"duration": "1 D"` ⏱️

**¿Qué es?**
- La cantidad de tiempo hacia atrás desde ahora que quieres obtener.
- Es la duración por cada bloque de datos.

**¿Qué significa "1 D"?**
- **"1 D"** = 1 Día
- Obtiene datos de las últimas 24 horas

**Formatos disponibles:**
- `"1 D"` - 1 día
- `"1 W"` - 1 semana  
- `"1 M"` - 1 mes
- `"1 Y"` - 1 año
- `"3600 S"` - 3600 segundos (1 hora)
- `"30 D"` - 30 días

**Ejemplos:**
```json
"duration": "1 D"    // Último día
"duration": "1 M"    // Último mes
"duration": "1 W"    // Última semana
```

**Nota:** Interactive Brokers tiene límites en cuánto tiempo puedes solicitar dependiendo del `bar_size`:
- Para barras de 1 minuto: máximo ~1 mes por solicitud
- Para barras de 5 minutos: máximo ~3 meses por solicitud
- Por eso se usan "bloques" (ver `num_blocks`)

---

### 3. `"bar_size": "1 min"` 📊

**¿Qué es?**
- El tamaño de cada barra/candlestick de datos.
- Define cada cuánto tiempo se agrupa la información.

**¿Qué significa "1 min"?**
- **"1 min"** = 1 minuto
- Cada registro representa 1 minuto de trading
- Si pides 1 día (1 D), obtendrás aproximadamente 1440 barras (24 horas × 60 minutos)

**Formatos disponibles:**
- `"1 min"` - 1 minuto (más detallado)
- `"5 mins"` - 5 minutos
- `"15 mins"` - 15 minutos
- `"30 mins"` - 30 minutos
- `"1 hour"` - 1 hora
- `"1 day"` - 1 día

**Ejemplos:**
```json
"bar_size": "1 min"     // Cada minuto (más datos, más detalle)
"bar_size": "5 mins"    // Cada 5 minutos (menos datos, más rápido)
"bar_size": "1 hour"    // Cada hora (mucho menos datos)
```

**¿Qué datos contiene cada barra?**
Cada barra tiene:
- **Open** (Apertura): Precio al inicio del período
- **High** (Máximo): Precio más alto del período
- **Low** (Mínimo): Precio más bajo del período
- **Close** (Cierre): Precio al final del período
- **Volume** (Volumen): Cantidad de contratos negociados

---

### 4. `"num_blocks": 1` 🔢

**¿Qué es?**
- Número de bloques consecutivos que quieres extraer.
- Cada bloque tiene la duración especificada en `duration`.

**¿Qué significa `1`?**
- Solo extrae **1 bloque** de datos
- Con `"duration": "1 D"` y `"num_blocks": 1`, obtienes 1 día de datos

**Ejemplos prácticos:**

```json
// Obtener 1 día de datos
{
  "duration": "1 D",
  "num_blocks": 1
}
// Resultado: 1 día de datos

// Obtener 4 días de datos (4 bloques de 1 día cada uno)
{
  "duration": "1 D",
  "num_blocks": 4
}
// Resultado: 4 días de datos (últimos 4 días)

// Obtener 1 mes de datos (4 bloques de 1 semana cada uno)
{
  "duration": "1 W",
  "num_blocks": 4
}
// Resultado: 4 semanas = aproximadamente 1 mes

// Obtener 3 meses de datos (3 bloques de 1 mes cada uno)
{
  "duration": "1 M",
  "num_blocks": 3
}
// Resultado: 3 meses de datos
```

**¿Por qué se usan bloques?**
- Interactive Brokers limita cuántos datos puedes solicitar en una sola petición
- Para obtener más datos, se hacen múltiples peticiones (bloques)
- Cada bloque se solicita de forma secuencial y se combinan

**Límite:**
- Máximo `12 bloques` (por seguridad y tiempo)

---

### 5. `"save_to_db": true` 💾

**¿Qué es?**
- Indica si quieres guardar los datos en la base de datos PostgreSQL.

**¿Qué significa `true`?**
- **`true`** = Sí, guarda los datos en la base de datos
- **`false`** = No, solo devuelve los datos sin guardarlos

**Ejemplos:**
```json
"save_to_db": true   // Guarda en PostgreSQL
"save_to_db": false  // Solo devuelve datos, no guarda
```

**¿Qué pasa si guardas?**
- Los datos se guardan en PostgreSQL
- Puedes consultarlos después sin volver a extraerlos de IB
- Si `bar_size` es "1 min", también se generan timeframes adicionales automáticamente (5min, 15min, 30min, etc.) en background

---

## 📝 Parámetro Opcional: `contract_month`

No está en tu ejemplo, pero también puedes especificar:

```json
{
  "symbol": "ES",
  "contract_month": "202512",
  ...
}
```

**¿Qué es?**
- El mes de vencimiento del contrato futuro.

**¿Qué significa "202512"?**
- **2025** = Año 2025
- **12** = Diciembre
- Especifica que quieres el contrato que vence en diciembre 2025

**Si no lo especificas:**
- IB Gateway usa el contrato más cercano (el más líquido/activo)

---

## 🎯 Ejemplo Completo Explicado

```json
{
  "symbol": "ES",           // Futuro E-mini S&P 500
  "duration": "1 D",        // Último día (24 horas)
  "bar_size": "1 min",      // Barras de 1 minuto cada una
  "num_blocks": 1,          // Solo 1 bloque (1 día)
  "save_to_db": true        // Guardar en PostgreSQL
}
```

**Esto significa:**
- "Dame los datos del futuro ES del último día"
- "Cada registro debe ser de 1 minuto"
- "Solo necesito 1 bloque (1 día)"
- "Guarda todo en la base de datos para consultarlo después"

**Resultado esperado:**
- Aproximadamente **1,440 barras** de 1 minuto (24 horas × 60 minutos)
- Cada barra con: Open, High, Low, Close, Volume
- Datos guardados en PostgreSQL para consultarlos después

---

## 📊 Ejemplos Prácticos

### Ejemplo 1: Datos de Última Hora (Prueba Rápida)
```json
{
  "symbol": "ES",
  "duration": "3600 S",
  "bar_size": "1 min",
  "num_blocks": 1,
  "save_to_db": false
}
```
- **Duración:** 3600 segundos = 1 hora
- **Resultado:** ~60 barras de 1 minuto

### Ejemplo 2: Una Semana de Datos
```json
{
  "symbol": "ES",
  "duration": "1 W",
  "bar_size": "5 mins",
  "num_blocks": 1,
  "save_to_db": true
}
```
- **Duración:** 1 semana
- **Bar size:** 5 minutos
- **Resultado:** ~2,016 barras de 5 minutos

### Ejemplo 3: Un Mes de Datos (Múltiples Bloques)
```json
{
  "symbol": "ES",
  "duration": "1 W",
  "bar_size": "1 min",
  "num_blocks": 4,
  "save_to_db": true
}
```
- **4 bloques de 1 semana cada uno = ~1 mes**
- **Resultado:** ~10,080 barras de 1 minuto (aproximadamente)

---

## ⚠️ Consideraciones Importantes

1. **Tiempo de ejecución:**
   - Más datos = más tiempo
   - 1 día con 1 minuto: ~30 segundos a 2 minutos
   - 1 mes con 1 minuto: ~5 a 10 minutos

2. **Límites de IB:**
   - IB tiene límites en cuántos datos puedes solicitar
   - Por eso se usan bloques para extracciones grandes

3. **Espacio en base de datos:**
   - Cada barra de 1 minuto ocupa espacio
   - 1 mes de datos de 1 minuto = ~10,000 registros
   - Asegúrate de tener espacio suficiente

---

## ✅ Resumen Rápido

| Parámetro | Tu Valor | Significado |
|-----------|----------|-------------|
| `symbol` | `"ES"` | Futuro E-mini S&P 500 |
| `duration` | `"1 D"` | Último día (24 horas) |
| `bar_size` | `"1 min"` | Barras de 1 minuto |
| `num_blocks` | `1` | 1 bloque = 1 día |
| `save_to_db` | `true` | Guardar en PostgreSQL |

**En palabras simples:** "Dame los datos del ES del último día, cada minuto, y guárdalos en la base de datos" 📊

