# ⚡ Configuración Rápida - Paso a Paso

## 🎯 Resumen Ultra Rápido

**2 cosas que hacer:**
1. **Tu app**: Crear `.env` (opcional, ya tiene defaults)
2. **IB Gateway**: Habilitar API en puerto 7497

---

## 📝 PARTE 1: Tu Aplicación (2 minutos)

### Opción A: Usar valores por defecto (más fácil)

**No necesitas hacer nada.** La aplicación ya tiene valores por defecto:
- `IB_HOST=127.0.0.1`
- `IB_PORT=7497`
- `IB_CLIENT_ID=1`

**Solo instala ibapi:**
```powershell
docker-compose exec backend pip install ibapi
docker-compose restart backend
```

---

### Opción B: Crear archivo `.env` (si quieres personalizar)

1. **Crea archivo** `backend/.env`:

```powershell
cd backend
# Crea archivo .env con este contenido:
```

```env
IB_HOST=127.0.0.1
IB_PORT=7497
IB_CLIENT_ID=1
DEBUG=False
```

2. **Reinicia contenedores:**
```powershell
docker-compose restart backend
```

---

## 🔧 PARTE 2: IB Gateway (5 minutos)

### Paso 1: Descargar IB Gateway

1. Ve a: https://www.interactivebrokers.com/en/index.php?f=16042
2. Descarga **IB Gateway** (no TWS completo)
3. Instálalo y ábrelo

---

### Paso 2: Iniciar Sesión

- Si tienes cuenta IB → inicia sesión
- Si no tienes cuenta → crea cuenta **Paper Trading** (gratis)

---

### Paso 3: Habilitar API ⚠️ IMPORTANTE

1. En IB Gateway:
   - **File** → **Global Configuration** → **API** → **Settings**
   - O busca "API Settings"

2. **Marca estas opciones:**
   - ✅ **"Enable ActiveX and Socket Clients"** (MÁS IMPORTANTE)
   - ✅ **"Read-Only API"** (opcional)

3. **Configura puerto:**
   - **Socket port**: `7497` (Paper Trading)
   - O `7496` (Live Trading)

4. **Guarda** y **reinicia IB Gateway**

---

### Paso 4: Verificar Conexión

En IB Gateway debe mostrar:
- ✅ **"Connected"** o **"Conectado"**

---

## ✅ Verificar que Todo Funciona

### 1. Verificar puerto:
```powershell
Test-NetConnection -ComputerName localhost -Port 7497
```
Debería mostrar: `TcpTestSucceeded : True`

### 2. Probar API:
1. Abre: http://localhost:8000/docs
2. Busca: `POST /api/v1/data/extract`
3. Haz clic en "Try it out"
4. Ingresa:
   ```json
   {
     "symbol": "ES",
     "duration": "1 D",
     "bar_size": "1 min",
     "num_blocks": 1
   }
   ```
5. Haz clic en "Execute"

**Si funciona:** Verás `200 OK` con datos ✅

---

## 🎯 Checklist Rápido

### Tu Aplicación:
- [ ] `ibapi` instalado: `docker-compose exec backend pip install ibapi`
- [ ] Aplicación ejecutándose: `docker-compose up -d`
- [ ] (Opcional) Archivo `.env` creado

### IB Gateway:
- [ ] IB Gateway instalado y ejecutándose
- [ ] Sesión iniciada (conectado)
- [ ] API habilitada: "Enable ActiveX and Socket Clients" ✅
- [ ] Puerto configurado: `7497` ✅

### Verificación:
- [ ] Puerto 7497 abierto
- [ ] `/docs` funciona
- [ ] Prueba de extracción funciona

---

## 🚨 Si Algo No Funciona

### Error: "Connection refused"
→ IB Gateway no está ejecutándose o API no habilitada

### Error: "ibapi no está instalado"
→ Ejecuta: `docker-compose exec backend pip install ibapi`

### Error: "Timeout"
→ Verifica que IB Gateway esté conectado y puerto sea 7497

---

**¡Listo! Con estos pasos deberías poder extraer datos.**

