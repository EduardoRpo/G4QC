# Arquitectura Simplificada - G4QC Trading Platform

## Cambios Realizados

### ✅ Eliminado: MT5 Extractor
- **Razón**: Los datos históricos de IB son universales y suficientes para backtesting
- **Beneficio**: Arquitectura más simple, menos mantenimiento, menos puntos de fallo

### ✅ Reforzado: Manejo de Timezones
- Todos los datos se normalizan a **UTC** antes de almacenar
- Soporte para diferentes zonas horarias de exchanges (CME: Chicago, NYMEX: NY, etc.)
- Validación automática de timezone en el Data Processor

### ✅ Mantenido: MT5 Executor (Opcional)
- Solo para ejecución de trading en vivo
- NO para extracción de datos
- Puede implementarse más adelante si es necesario

## Arquitectura de Datos Actualizada

```
┌─────────────────────────────────────────────────────────────┐
│              EXTRACCIÓN DE DATOS                            │
└─────────────────────────────────────────────────────────────┘

Interactive Brokers (IB) → IB Extractor → Data Processor → PostgreSQL
                                                              (UTC)
                                      ↓
                          Normalización de Timezone
                          (CME, NYMEX, etc. → UTC)
```

## Flujo Simplificado

### 1. Extracción de Datos
- **Fuente única**: Interactive Brokers (IB)
- **Normalización**: Todos los datos a UTC
- **Almacenamiento**: PostgreSQL con TimescaleDB

### 2. Backtesting
- Usa datos históricos de IB (normalizados a UTC)
- Independiente del broker donde se ejecutará después

### 3. Trading en Vivo (Opcional)
- IB Executor: Ejecuta órdenes en Interactive Brokers
- MT5 Executor: Opcional, ejecuta órdenes en MetaTrader 5
- Ambos usan los mismos datos históricos de IB para análisis

## Ventajas de la Arquitectura Simplificada

1. ✅ **Menos complejidad**: Una sola fuente de datos
2. ✅ **Menos mantenimiento**: Un solo sistema de extracción
3. ✅ **Datos más universales**: IB tiene acceso directo a exchanges
4. ✅ **Timezone handling robusto**: Normalización automática a UTC
5. ✅ **Mejor para backtesting**: Datos consistentes y universales

## Manejo de Timezones

El sistema ahora maneja automáticamente:

- **CME Futures** (ES, NQ, etc.): Timezone America/Chicago → UTC
- **NYMEX/COMEX** (GC, CL, RB, etc.): Timezone America/New_York → UTC
- **Detecta automáticamente** la zona horaria según el símbolo
- **Normaliza todo a UTC** para consistencia

## Implementación

Los cambios ya están implementados en:
- `backend/app/services/data_extraction/data_processor.py` - Normalización de timezone
- Documentación actualizada en `PROPUESTA_ARQUITECTURA.md`

---

**Fecha**: Enero 2024  
**Decisión**: Simplificación basada en análisis crítico de necesidades

