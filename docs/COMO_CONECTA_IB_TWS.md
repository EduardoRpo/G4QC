# 🔌 ¿Cómo se Conecta la Aplicación a IB TWS?

## 📋 Resumen Rápido

La aplicación se conecta a IB TWS usando la librería **`ibapi`** de Python, que se comunica con IB TWS/Gateway a través de un **socket TCP** en el puerto local.

---

## 🔄 Flujo de Conexión Completo

```
┌─────────────────────────────────────────────────────────────────┐
│  1. TU APLICACIÓN (FastAPI)                                      │
│     └── backend/app/services/data_extraction/ib_extractor.py    │
│         └── IBDataExtractor (clase)                              │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        │ Usa ibapi (librería Python)
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. IBAPI (Librería Python)                                      │
│     └── ibapi.client.EClient                                     │
│     └── ibapi.wrapper.EWrapper                                   │
│                                                                   │
│     Método: self.connect(host, port, client_id)                 │
│     • host: "127.0.0.1" (localhost)                              │
│     • port: 7497 (paper trading) o 7496 (live)                    │
│     • client_id: 1 (identificador único)                          │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        │ Socket TCP (localhost:7497)
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. IB TWS / IB GATEWAY (Ejecutándose en tu PC)                 │
│     └── Debe estar:                                              │
│         • Abierto y ejecutándose                                 │
│         • Conectado a Interactive Brokers                        │
│         • API habilitada en puerto 7497                          │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        │ Conexión segura a servidores IB
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. INTERACTIVE BROKERS (Servidores en la nube)                 │
│     └── Proporciona datos históricos                             │
│     └── Ejecuta órdenes (futuro)                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💻 Código Técnico: Cómo Funciona

### 1. **Configuración de Conexión**

La configuración está en `backend/app/core/config.py`:

```python
# Interactive Brokers
IB_HOST: str = os.getenv("IB_HOST", "127.0.0.1")      # localhost
IB_PORT: int = int(os.getenv("IB_PORT", "7497"))      # Puerto (7497 = paper, 7496 = live)
IB_CLIENT_ID: int = int(os.getenv("IB_CLIENT_ID", "1"))  # ID único
```

**Valores por defecto:**
- **Host**: `127.0.0.1` (localhost - IB TWS debe estar en la misma máquina)
- **Puerto**: `7497` (Paper Trading) o `7496` (Live Trading)
- **Client ID**: `1` (identificador único para esta conexión)

---

### 2. **Clase IBDataExtractor**

La clase `IBDataExtractor` hereda de `EClient` y `EWrapper` de ibapi:

```python
class IBDataExtractor(EClient, EWrapper):
    """
    EClient: Cliente que envía comandos a IB TWS
    EWrapper: Callbacks que reciben respuestas de IB TWS
    """
    
    def __init__(self, host=None, port=None, client_id=None):
        EClient.__init__(self, self)  # Inicializa el cliente
        
        # Configuración de conexión
        self.host = host or settings.IB_HOST      # "127.0.0.1"
        self.port = port or settings.IB_PORT      # 7497
        self.client_id = client_id or settings.IB_CLIENT_ID  # 1
        
        # Estado de conexión
        self.connected = False
        self.evento = threading.Event()  # Para sincronización
```

---

### 3. **Método de Conexión**

El método `connect_to_ib()` establece la conexión:

```python
def connect_to_ib(self):
    """Conectar a Interactive Brokers"""
    if not self.connected:
        try:
            # 1. Establecer conexión socket TCP
            self.connect(self.host, self.port, self.client_id)
            
            # 2. Iniciar thread para procesar mensajes
            self.api_thread = threading.Thread(target=self.run, daemon=True)
            self.api_thread.start()
            
            # 3. Esperar confirmación de conexión (timeout 10 seg)
            if not self.evento.wait(timeout=10):
                raise ConnectionError("Timeout al conectar con Interactive Brokers")
            
            self.evento.clear()
            self.connected = True
            
        except Exception as e:
            raise ConnectionError(f"Error al conectar con IB: {str(e)}")
```

**¿Qué hace `self.connect()`?**
- Abre un socket TCP hacia `127.0.0.1:7497`
- Envía mensaje de handshake a IB TWS
- Espera confirmación de IB TWS

**¿Qué hace `self.run()`?**
- Procesa mensajes entrantes de IB TWS en un thread separado
- Llama a los callbacks (`historicalData()`, `error()`, etc.)

---

### 4. **Callback de Confirmación**

Cuando IB TWS acepta la conexión, llama a `nextValidId()`:

```python
def nextValidId(self, orderId):
    """Callback cuando se recibe el ID válido (conexión establecida)"""
    self.evento.set()  # Señaliza que la conexión está lista
```

Este callback confirma que la conexión está establecida.

---

### 5. **Solicitud de Datos Históricos**

Una vez conectado, puedes solicitar datos:

```python
def extract_historical_data(self, symbol, duration, bar_size, ...):
    # Conectar si no está conectado
    if not self.connected:
        self.connect_to_ib()
    
    # Crear contrato
    contrato = self.create_contract(symbol=symbol, ...)
    
    # Solicitar datos históricos
    self.reqHistoricalData(
        reqId=1,                    # ID único de la solicitud
        contract=contrato,          # Contrato (ES, NQ, etc.)
        endDateTime="20251203-16:00:00",  # Fecha final
        durationStr="1 M",          # Duración (1 mes)
        barSizeSetting="1 min",     # Tamaño de barra
        whatToShow="TRADES",        # Tipo de datos
        useRTH=0,                   # Incluir fuera de horas regulares
        formatDate=1,               # Formato de fecha
        keepUpToDate=False,         # No mantener actualizado
        chartOptions=[]             # Opciones adicionales
    )
    
    # Esperar respuesta (timeout 60 seg)
    if not self.evento.wait(timeout=60):
        print("⚠️ Timeout esperando datos")
```

---

### 6. **Callbacks de Respuesta**

IB TWS envía los datos a través de callbacks:

```python
def historicalData(self, reqId, bar):
    """Callback cuando se recibe un bar de datos históricos"""
    # Cada bar (vela) llega aquí
    self.datos_historicos[reqId].append({
        "Date": bar.date,
        "Open": bar.open,
        "High": bar.high,
        "Low": bar.low,
        "Close": bar.close,
        "Volume": bar.volume,
        "Count": bar.barCount
    })

def historicalDataEnd(self, reqId, start, end):
    """Callback cuando termina la solicitud"""
    print(f"✅ Fin de datos históricos para ID: {reqId}")
    self.evento.set()  # Señaliza que terminó
```

---

## 🔧 Requisitos para que Funcione

### 1. **IB TWS/Gateway debe estar:**
- ✅ Ejecutándose en tu computadora
- ✅ Conectado a Interactive Brokers (verás "Connected" en la interfaz)
- ✅ API habilitada en configuración:
  - Settings → API Settings
  - "Enable ActiveX and Socket Clients" ✅
  - Puerto configurado: **7497** (paper) o **7496** (live)

### 2. **ibapi debe estar instalado:**
```powershell
# En el contenedor Docker
docker-compose exec backend pip install ibapi

# O localmente
pip install ibapi
```

### 3. **Configuración correcta:**
- Host: `127.0.0.1` (IB TWS en la misma máquina)
- Puerto: `7497` (debe coincidir con IB TWS)
- Client ID: `1` (único, no debe estar en uso)

---

## 📊 Diagrama de Secuencia

```
Tu App              ibapi              IB TWS          Interactive Brokers
  │                   │                   │                    │
  │──connect()───────▶│                   │                    │
  │                   │──socket TCP──────▶│                    │
  │                   │                   │                    │
  │                   │                   │──conectado────────▶│
  │                   │◀──nextValidId─────│                    │
  │◀──connected───────│                   │                    │
  │                   │                   │                    │
  │──reqHistoricalData()─────────────────▶│                    │
  │                   │                   │                    │
  │                   │                   │──solicita datos───▶│
  │                   │                   │◀──datos────────────│
  │◀──historicalData()│◀──historicalData()│                    │
  │◀──historicalData()│◀──historicalData()│                    │
  │◀──historicalData()│◀──historicalData()│                    │
  │                   │                   │                    │
  │◀──historicalDataEnd()─────────────────│                    │
  │                   │                   │                    │
```

---

## 🔍 Verificación de Conexión

### Verificar que IB TWS está escuchando:

```powershell
# Windows PowerShell
Test-NetConnection -ComputerName localhost -Port 7497
```

**Debería mostrar:**
```
TcpTestSucceeded : True
```

### Verificar desde la aplicación:

```python
# En Python
from app.services.data_extraction.ib_extractor import IBDataExtractor

extractor = IBDataExtractor()
extractor.connect_to_ib()  # Debe conectar sin errores
print(f"Conectado: {extractor.connected}")  # True
```

---

## ⚠️ Errores Comunes

### Error: "Connection refused"
**Causa**: IB TWS no está ejecutándose o puerto incorrecto
**Solución**: 
- Abre IB TWS/Gateway
- Verifica que esté conectado
- Verifica puerto en configuración API

### Error: "Timeout al conectar"
**Causa**: IB TWS no responde o API no está habilitada
**Solución**:
- Verifica configuración API en IB TWS
- Reinicia IB TWS
- Verifica que no haya firewall bloqueando

### Error: "Client ID already in use"
**Causa**: Otra aplicación está usando el mismo Client ID
**Solución**:
- Cambia `IB_CLIENT_ID` en configuración
- O cierra otras conexiones

---

## 🎯 Resumen

**La aplicación se conecta a IB TWS así:**

1. **Usa ibapi** (librería Python oficial de IB)
2. **Abre socket TCP** a `localhost:7497`
3. **IB TWS debe estar ejecutándose** y escuchando en ese puerto
4. **Comunicación bidireccional**:
   - Tu app → IB TWS: Solicitudes (`reqHistoricalData`)
   - IB TWS → Tu app: Respuestas (callbacks: `historicalData`, `error`)

**Es como una conversación:**
- Tu app pregunta: "Dame datos de ES del último mes"
- IB TWS responde: "Aquí están los datos" (bar por bar)
- Tu app procesa los datos y los guarda en PostgreSQL

---

**¿Tienes alguna duda sobre el proceso de conexión?**

