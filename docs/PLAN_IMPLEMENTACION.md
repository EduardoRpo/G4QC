# Plan de Implementación Detallado - G4QC Trading Platform

## 🎯 Objetivo Inmediato: MVP (Minimum Viable Product)

### MVP Scope
1. ✅ Extracción automática de datos (IB) → PostgreSQL
2. ✅ API REST para consultar datos
3. ✅ Backtesting básico de una estrategia simple
4. ✅ Visualización de resultados
5. ✅ Interfaz web básica

## 📦 Paso 1: Setup de Infraestructura Base

### 1.1 Estructura de Proyecto
```
G4QC/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   └── services/
│   │       └── data_extraction/
│   │           └── ib_extractor.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   └── (se crea después)
└── docker-compose.yml
```

### 1.2 Docker Compose (Desarrollo)
```yaml
version: '3.8'
services:
  postgres:
    image: timescale/timescaledb:latest-pg15
    environment:
      POSTGRES_USER: g4qc
      POSTGRES_PASSWORD: g4qc_dev
      POSTGRES_DB: g4qc_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  backend:
    build: ./backend
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://g4qc:g4qc_dev@postgres:5432/g4qc_db
      REDIS_URL: redis://redis:6379

volumes:
  postgres_data:
```

## 🔧 Paso 2: Refactorizar Código de Extracción

### 2.1 Servicio de Extracción IB

**Archivo: `backend/app/services/data_extraction/ib_extractor.py`**

```python
import threading
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.data import MarketData

class IBDataExtractor(EClient, EWrapper):
    """
    Servicio refactorizado basado en Data_Extract.ipynb
    """
    
    def __init__(self, host: str = "127.0.0.1", port: int = 7497, client_id: int = 1):
        EClient.__init__(self, self)
        self.host = host
        self.port = port
        self.client_id = client_id
        self.datos_historicos: Dict[int, List] = {}
        self.evento = threading.Event()
        self.connected = False
    
    def connect_to_ib(self):
        """Conectar a Interactive Brokers"""
        if not self.connected:
            self.connect(self.host, self.port, self.client_id)
            api_thread = threading.Thread(target=self.run, daemon=True)
            api_thread.start()
            self.evento.wait(timeout=10)
            self.evento.clear()
            self.connected = True
    
    def nextValidId(self, orderId):
        self.evento.set()
    
    def historicalData(self, reqId, bar):
        if reqId not in self.datos_historicos:
            self.datos_historicos[reqId] = []
        
        self.datos_historicos[reqId].append({
            "Date": bar.date,
            "Open": float(bar.open),
            "High": float(bar.high),
            "Low": float(bar.low),
            "Close": float(bar.close),
            "Volume": int(bar.volume),
            "Count": int(bar.barCount)
        })
    
    def historicalDataEnd(self, reqId, start, end):
        print(f"✅ Fin de datos históricos para ID: {reqId}")
        self.evento.set()
    
    def error(self, reqId, code, msg):
        if code not in [2104, 2106, 2158]:  # Ignorar mensajes informativos
            print(f"❗ Error reqId={reqId}, code={code}, msg={msg}")
    
    def create_contract(
        self, 
        symbol: str, 
        sec_type: str = "FUT",
        exchange: str = "CME",
        currency: str = "USD",
        contract_month: Optional[str] = None
    ) -> Contract:
        """Crear contrato IB"""
        contrato = Contract()
        contrato.symbol = symbol
        contrato.secType = sec_type
        contrato.exchange = exchange
        contrato.currency = currency
        if contract_month:
            contrato.lastTradeDateOrContractMonth = contract_month
        return contrato
    
    def extract_historical_data(
        self,
        symbol: str,
        duration: str = "1 M",
        bar_size: str = "1 min",
        end_date: Optional[datetime] = None,
        contract_month: Optional[str] = None,
        num_blocks: int = 1
    ) -> pd.DataFrame:
        """
        Extraer datos históricos (refactorizado del notebook)
        
        Args:
            symbol: Símbolo del instrumento (ES, NQ, etc.)
            duration: Duración por bloque (ej: "1 M", "1 D")
            bar_size: Tamaño de barra (ej: "1 min", "5 mins")
            end_date: Fecha final (default: ahora)
            contract_month: Mes de vencimiento (ej: "202512")
            num_blocks: Número de bloques a extraer
        
        Returns:
            DataFrame con datos históricos
        """
        self.connect_to_ib()
        
        contrato = self.create_contract(
            symbol=symbol,
            contract_month=contract_month
        )
        
        if end_date is None:
            end_date = datetime.utcnow()
        
        all_dataframes = []
        self.datos_historicos.clear()
        
        for i in range(num_blocks):
            end_str = end_date.strftime("%Y%m%d-%H:%M:%S")
            
            self.reqHistoricalData(
                reqId=i+1,
                contract=contrato,
                endDateTime=end_str,
                durationStr=duration,
                barSizeSetting=bar_size,
                whatToShow="TRADES",
                useRTH=0,
                formatDate=1,
                keepUpToDate=False,
                chartOptions=[]
            )
            
            self.evento.wait(timeout=60)
            self.evento.clear()
            
            if (i+1) in self.datos_historicos:
                df_temp = pd.DataFrame(self.datos_historicos[i+1])
                df_temp['Date'] = pd.to_datetime(
                    df_temp['Date'], 
                    format='%Y%m%d %H:%M:%S', 
                    utc=True, 
                    errors='coerce'
                )
                all_dataframes.append(df_temp)
            
            # Retroceder para siguiente bloque
            if duration.endswith("M"):
                months = int(duration.split()[0])
                end_date = end_date - timedelta(days=30 * months)
            elif duration.endswith("D"):
                days = int(duration.split()[0])
                end_date = end_date - timedelta(days=days)
        
        if all_dataframes:
            df = pd.concat(all_dataframes, ignore_index=True)
            df = df.sort_values('Date').drop_duplicates(subset=['Date'])
            
            # Asegurar tipos numéricos
            for col in ['Open', 'High', 'Low', 'Close', 'Volume', 'Count']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            return df
        
        return pd.DataFrame()
    
    def save_to_database(
        self, 
        df: pd.DataFrame, 
        symbol: str, 
        timeframe: str = "1min",
        db: Session = None
    ):
        """Guardar datos en PostgreSQL en lugar de CSV"""
        if df.empty:
            return
        
        # Convertir DataFrame a registros
        records = []
        for _, row in df.iterrows():
            records.append({
                "symbol": symbol,
                "timeframe": timeframe,
                "timestamp": row['Date'],
                "open": row['Open'],
                "high": row['High'],
                "low": row['Low'],
                "close": row['Close'],
                "volume": row['Volume'],
                "count": row.get('Count', 0)
            })
        
        # Bulk insert (implementar según modelo de datos)
        # db.bulk_insert_mappings(MarketData, records)
        # db.commit()
    
    def disconnect(self):
        """Desconectar de IB"""
        if self.connected:
            EClient.disconnect(self)
            self.connected = False
```

## 🗄️ Paso 3: Modelo de Base de Datos

### 3.1 Schema de Datos de Mercado

**Archivo: `backend/app/models/data.py`**

```python
from sqlalchemy import Column, String, DateTime, Float, Integer, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class MarketData(Base):
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False, index=True)
    timeframe = Column(String(10), nullable=False)  # 1min, 5min, 15min, etc.
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    count = Column(Integer, default=0)
    
    # Índices compuestos para queries eficientes
    __table_args__ = (
        Index('idx_symbol_timeframe_timestamp', 'symbol', 'timeframe', 'timestamp'),
    )
```

### 3.2 Script de Migración

**Archivo: `backend/alembic/versions/001_create_market_data.py`**

```python
"""create market_data table

Revision ID: 001
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'market_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(10), nullable=False),
        sa.Column('timeframe', sa.String(10), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('open', sa.Float(), nullable=False),
        sa.Column('high', sa.Float(), nullable=False),
        sa.Column('low', sa.Float(), nullable=False),
        sa.Column('close', sa.Float(), nullable=False),
        sa.Column('volume', sa.Integer(), nullable=False),
        sa.Column('count', sa.Integer(), default=0),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_symbol_timeframe_timestamp', 'market_data', 
                   ['symbol', 'timeframe', 'timestamp'])
    
    # Habilitar TimescaleDB
    op.execute("CREATE EXTENSION IF NOT EXISTS timescaledb;")
    op.execute(
        "SELECT create_hypertable('market_data', 'timestamp', "
        "chunk_time_interval => INTERVAL '1 day');"
    )

def downgrade():
    op.drop_table('market_data')
```

## 🚀 Paso 4: API REST Básica

### 4.1 Endpoint de Datos

**Archivo: `backend/app/api/v1/endpoints/data.py`**

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.core.database import get_db
from app.services.data_extraction.ib_extractor import IBDataExtractor
from app.models.data import MarketData
from pydantic import BaseModel

router = APIRouter()

class ExtractDataRequest(BaseModel):
    symbol: str
    duration: str = "1 M"
    bar_size: str = "1 min"
    contract_month: Optional[str] = None
    num_blocks: int = 1

@router.post("/extract")
async def extract_data(request: ExtractDataRequest):
    """Extraer datos históricos desde IB"""
    extractor = IBDataExtractor()
    try:
        df = extractor.extract_historical_data(
            symbol=request.symbol,
            duration=request.duration,
            bar_size=request.bar_size,
            contract_month=request.contract_month,
            num_blocks=request.num_blocks
        )
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No se obtuvieron datos")
        
        # Guardar en base de datos
        extractor.save_to_database(df, request.symbol, request.bar_size)
        
        return {
            "status": "success",
            "records": len(df),
            "symbol": request.symbol,
            "date_range": {
                "start": df['Date'].min().isoformat(),
                "end": df['Date'].max().isoformat()
            }
        }
    finally:
        extractor.disconnect()

@router.get("/data/{symbol}")
async def get_data(
    symbol: str,
    timeframe: str = "1min",
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Obtener datos históricos desde la base de datos"""
    query = db.query(MarketData).filter(MarketData.symbol == symbol)
    query = query.filter(MarketData.timeframe == timeframe)
    
    if start_date:
        query = query.filter(MarketData.timestamp >= start_date)
    if end_date:
        query = query.filter(MarketData.timestamp <= end_date)
    
    data = query.order_by(MarketData.timestamp).all()
    
    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "records": len(data),
        "data": [
            {
                "timestamp": d.timestamp.isoformat(),
                "open": d.open,
                "high": d.high,
                "low": d.low,
                "close": d.close,
                "volume": d.volume
            }
            for d in data
        ]
    }
```

### 4.2 Main FastAPI App

**Archivo: `backend/app/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import data

app = FastAPI(
    title="G4QC Trading Platform API",
    description="API para plataforma de trading automatizado",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router, prefix="/api/v1/data", tags=["data"])

@app.get("/")
async def root():
    return {"message": "G4QC Trading Platform API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

## 📋 Checklist de Implementación MVP

### Semana 1-2: Setup Base
- [ ] Crear estructura de directorios
- [ ] Configurar Docker Compose
- [ ] Setup PostgreSQL con TimescaleDB
- [ ] Configurar FastAPI básico
- [ ] Crear modelos de base de datos

### Semana 3-4: Refactorizar Extracción
- [ ] Migrar código de Data_Extract.ipynb a servicio
- [ ] Implementar IBDataExtractor
- [ ] Crear función de guardado en DB
- [ ] Testing de extracción

### Semana 5-6: API y Backend
- [ ] Endpoints de extracción de datos
- [ ] Endpoints de consulta de datos
- [ ] Procesamiento de timeframes (1min → 5min, 15min, etc.)
- [ ] Testing de API

### Semana 7-8: Backtesting Básico
- [ ] Integrar Backtrader o motor custom
- [ ] Estrategia de ejemplo (Moving Average Crossover)
- [ ] Endpoint de backtesting
- [ ] Cálculo de métricas básicas (Sharpe, Drawdown)

### Semana 9-10: Frontend Básico
- [ ] Setup React + TypeScript
- [ ] Página de extracción de datos
- [ ] Visualización de datos (gráfico de velas)
- [ ] Página de backtesting con resultados

## 🎯 Métricas de Éxito del MVP

1. ✅ Extraer datos de al menos 3 instrumentos (ES, NQ, EC)
2. ✅ Almacenar datos en PostgreSQL
3. ✅ Consultar datos vía API
4. ✅ Ejecutar backtesting de estrategia simple
5. ✅ Visualizar resultados en web

## 🔄 Siguiente Fase Después del MVP

Una vez completado el MVP, se puede avanzar a:
1. Optimización de parámetros
2. Análisis de portfolio
3. Trading en vivo
4. Walk Forward Analysis
5. Monte Carlo Simulation

---

**¿Quieres que comience implementando alguna parte específica de este plan?**

