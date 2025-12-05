# Instalación de IB API (ibapi)

## Problema

El paquete `ibapi` no está disponible en PyPI de forma estándar. Interactive Brokers proporciona el paquete pero debe instalarse de forma especial.

## Solución Rápida (Para Desarrollo Local)

Si vas a usar el sistema sin Docker o necesitas ibapi:

### Opción 1: Instalar desde el wheel de IB

1. Descarga el paquete desde: https://interactivebrokers.github.io/tws-api/
2. O usa pip con el wheel directo:
```bash
pip install https://github.com/stoicmike/ib_insync/raw/master/ibapi-10.19.01-py3-none-any.whl
```

### Opción 2: Instalar versión disponible

```bash
pip install ibapi
# Esto instalará la versión disponible (puede ser 9.81.1)
```

### Opción 3: Hacer opcional en el código

Por ahora, he hecho que ibapi sea opcional. El sistema funcionará sin él, pero la extracción de datos requerirá que se instale manualmente.

## Para Docker

El Dockerfile ahora intenta instalar ibapi pero no falla si no está disponible. Para instalar en Docker:

1. Descarga el wheel file de IB
2. Agrégelo al proyecto
3. Modifica el Dockerfile para instalarlo localmente

O instala manualmente después de iniciar el contenedor:

```bash
docker-compose exec backend pip install ibapi
```

## Nota Importante

**Para probar la API sin IB TWS**, no necesitas ibapi instalado. Solo los endpoints de extracción de datos lo requieren.

El sistema funcionará correctamente para:
- ✅ Health check
- ✅ Documentación API
- ✅ Consultar datos existentes
- ✅ Todos los endpoints excepto extracción

## Próximos Pasos

Si necesitas extraer datos de IB:
1. Instala ibapi manualmente (Opción 2 arriba)
2. O descarga el paquete oficial de IB
3. O usa el sistema sin Docker en desarrollo local

