# 📅 ¿Cómo Funciona `num_blocks`? - Explicación Simple

## 🎯 Respuesta Rápida

**`num_blocks` extrae datos hacia atrás desde HOY, día por día.**

---

## 📆 Ejemplo: `num_blocks: 3` con `duration: "1 D"`

Imagina que hoy es **7 de diciembre de 2025**:

### ¿Qué días trae?

```
Bloque 1: Desde HOY (7 dic) hacia atrás 1 día
          → Datos del 6-7 de diciembre

Bloque 2: Desde 6 dic hacia atrás 1 día  
          → Datos del 5-6 de diciembre

Bloque 3: Desde 5 dic hacia atrás 1 día
          → Datos del 4-5 de diciembre
```

**Resultado final:** Datos de los días **4, 5, 6 y 7 de diciembre** (últimos 4 días)

---

## 🎬 Visualización Paso a Paso

```
HOY = 7 de diciembre 2025

num_blocks: 3, duration: "1 D"

┌─────────────────────────────────────────┐
│ BLOQUE 1                                │
│ end_date: 7 dic                         │
│ duration: 1 D (hacia atrás)            │
│ Resultado: Datos del 6-7 dic           │
└─────────────────────────────────────────┘
         ↓ (retrocede 1 día)
┌─────────────────────────────────────────┐
│ BLOQUE 2                                │
│ end_date: 6 dic                         │
│ duration: 1 D (hacia atrás)            │
│ Resultado: Datos del 5-6 dic           │
└─────────────────────────────────────────┘
         ↓ (retrocede 1 día)
┌─────────────────────────────────────────┐
│ BLOQUE 3                                │
│ end_date: 5 dic                         │
│ duration: 1 D (hacia atrás)            │
│ Resultado: Datos del 4-5 dic           │
└─────────────────────────────────────────┘

RESULTADO FINAL:
Datos de: 4 dic, 5 dic, 6 dic, 7 dic
```

---

## 📊 Ejemplos Prácticos

### Ejemplo 1: `num_blocks: 1`
```json
{
  "duration": "1 D",
  "num_blocks": 1
}
```
**Resultado:** Solo el día de ayer y hoy (último día completo)

---

### Ejemplo 2: `num_blocks: 3`
```json
{
  "duration": "1 D",
  "num_blocks": 3
}
```
**Resultado:** Últimos 4 días (hay solapamiento entre bloques)

**Días:** 
- Día 1: 6-7 dic
- Día 2: 5-6 dic  
- Día 3: 4-5 dic

---

### Ejemplo 3: `num_blocks: 7`
```json
{
  "duration": "1 D",
  "num_blocks": 7
}
```
**Resultado:** Última semana completa

**Días:** Desde hace 7 días hasta hoy

---

## ⚠️ Nota Importante: Solapamiento

**Los bloques se solapan un poco** porque cada bloque incluye datos desde su fecha final hacia atrás.

Por ejemplo:
- Bloque 1: 6-7 dic
- Bloque 2: 5-6 dic ← El día 6 aparece en ambos bloques

**Pero no te preocupes:** El sistema elimina duplicados automáticamente, así que no tendrás datos repetidos.

---

## 🔍 ¿De qué fecha empieza?

**Siempre empieza desde HOY (fecha actual UTC)**

El código hace:
```python
end_date = datetime.utcnow()  # Fecha de HOY
```

Luego para cada bloque:
1. Extrae datos desde `end_date` hacia atrás por `duration`
2. Retrocede `end_date` por la duración
3. Repite para el siguiente bloque

---

## 📝 Resumen

| num_blocks | duration | ¿Qué días trae? |
|------------|----------|-----------------|
| 1 | "1 D" | Último día (ayer-hoy) |
| 3 | "1 D" | Últimos 4 días |
| 7 | "1 D" | Última semana |
| 1 | "1 M" | Último mes |
| 3 | "1 M" | Últimos 3 meses |

**Fórmula simple:**
```
Días totales ≈ num_blocks × días_por_bloque
```

Pero recuerda: **siempre empieza desde HOY y va hacia atrás.**

---

## ✅ Tu Caso Específico

Si ejecutaste:
```json
{
  "duration": "1 D",
  "num_blocks": 1
}
```

**Trajo:** Datos del último día completo (probablemente 5-6 de diciembre, dependiendo de cuándo lo ejecutaste)

Si ejecutaras:
```json
{
  "duration": "1 D",
  "num_blocks": 3
}
```

**Traería:** Datos de los últimos 4 días (desde hace 3 días hasta hoy)

