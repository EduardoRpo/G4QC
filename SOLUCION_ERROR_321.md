# 🔧 Solución al Error 321 - Contract Month

## ⚠️ Problema Identificado

El error que estás viendo es:

```
Error reqId=1, code=321, msg=Error validating request.-'bL' : cause - Please enter a local symbol or an expiry
```

**Significado:** IB Gateway necesita que especifiques el mes de vencimiento (`contract_month`) para futuros.

---

## ✅ Solución Inmediata

### Opción 1: Especificar contract_month manualmente (RECOMENDADO)

En tu petición, agrega el parámetro `contract_month`:

```json
{
  "symbol": "ES",
  "duration": "1 D",
  "bar_size": "1 min",
  "contract_month": "202512",
  "num_blocks": 1,
  "save_to_db": true
}
```

**Formatos de contract_month:**
- `"202512"` = Diciembre 2025
- `"202601"` = Enero 2026
- `"202602"` = Febrero 2026

### Opción 2: Usar el mes actual

Como estamos en diciembre 2025, usa:

```json
{
  "symbol": "ES",
  "duration": "1 D",
  "bar_size": "1 min",
  "contract_month": "202512",
  "num_blocks": 1,
  "save_to_db": true
}
```

---

## 🔍 Cómo Encontrar el Contract Month Correcto

Para futuros como ES, los meses de vencimiento típicos son:
- **Marzo (H)**: H = March
- **Junio (M)**: M = June
- **Septiembre (U)**: U = September
- **Diciembre (Z)**: Z = December

Ejemplos:
- `"202503"` = Marzo 2025
- `"202506"` = Junio 2025
- `"202509"` = Septiembre 2025
- `"202512"` = Diciembre 2025

---

## 🧪 Prueba Rápida

Prueba con estos valores:

```json
{
  "symbol": "ES",
  "duration": "3600 S",
  "bar_size": "1 min",
  "contract_month": "202512",
  "num_blocks": 1,
  "save_to_db": false
}
```

- `duration: "3600 S"` = 1 hora (prueba rápida)
- `contract_month: "202512"` = Diciembre 2025 (mes actual)
- `save_to_db: false` = No guardar (solo probar)

---

## 📝 Notas

- El cálculo automático de `contract_month` puede no funcionar si el contrato no existe
- Es mejor especificar manualmente el `contract_month` para asegurar que funcione
- Los futuros tienen meses de vencimiento específicos (normalmente trimestrales)

