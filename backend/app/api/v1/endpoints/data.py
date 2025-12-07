"""
Data extraction and query endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.core.database import get_db
from app.core.config import settings
from app.services.data_extraction.ib_extractor import IBDataExtractor
from app.models.data import MarketData
from app.services.data_extraction.data_processor import DataProcessor

router = APIRouter()


class ExtractDataRequest(BaseModel):
    """Request model for data extraction"""
    symbol: str = Field(..., description="Símbolo del instrumento (ES, NQ, EC, etc.)")
    duration: str = Field(default="1 M", description="Duración por bloque (ej: '1 M', '1 D')")
    bar_size: str = Field(default="1 min", description="Tamaño de barra (ej: '1 min', '5 mins')")
    contract_month: Optional[str] = Field(None, description="Mes de vencimiento (ej: '202512')")
    num_blocks: int = Field(default=1, ge=1, le=12, description="Número de bloques a extraer")
    save_to_db: bool = Field(default=True, description="Guardar en base de datos")


class ExtractDataResponse(BaseModel):
    """Response model for data extraction"""
    status: str
    records: int
    symbol: str
    date_range: dict
    message: Optional[str] = None


class MarketDataResponse(BaseModel):
    """Response model for market data query"""
    symbol: str
    timeframe: str
    records: int
    data: List[dict]


@router.post("/extract", response_model=ExtractDataResponse)
async def extract_data(
    request: ExtractDataRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Extraer datos históricos desde Interactive Brokers
    
    - **symbol**: Símbolo del instrumento (ES, NQ, EC, 6B, RB, GC, LE, HE, etc.)
    - **duration**: Duración por bloque (ej: "1 M", "1 D", "3600 S")
    - **bar_size**: Tamaño de barra (ej: "1 min", "5 mins", "1 hour")
    - **contract_month**: Mes de vencimiento opcional (ej: "202512")
    - **num_blocks**: Número de bloques a extraer (máximo 12)
    
    **Nota**: Requiere que ibapi esté instalado y que IB TWS/Gateway esté ejecutándose.
    """
    processor = DataProcessor(db)
    extractor = None
    
    try:
        # Calcular contract_month automáticamente si no se proporciona
        # Para futuros, necesitamos especificar el mes de vencimiento
        contract_month = request.contract_month
        if not contract_month:
            # Calcular el próximo mes de vencimiento (formato YYYYMM)
            # Para futuros, normalmente se usa el "front month" (próximo disponible)
            from datetime import datetime
            now = datetime.utcnow()
            # Usar el mes actual primero, si estamos después del día 15, usar el próximo mes
            if now.day > 15 and now.month < 12:
                # Después del día 15, usar próximo mes
                contract_month = f"{now.year}{now.month + 1:02d}"
            elif now.day > 15 and now.month == 12:
                # Diciembre después del día 15, usar enero del año siguiente
                contract_month = f"{now.year + 1}01"
            else:
                # Antes del día 15, usar el mes actual
                contract_month = f"{now.year}{now.month:02d}"
        
        # Intentar crear el extractor (verificará si ibapi está instalado)
        extractor = IBDataExtractor()
        
        # Extraer datos
        df = extractor.extract_historical_data(
            symbol=request.symbol,
            duration=request.duration,
            bar_size=request.bar_size,
            contract_month=contract_month,
            num_blocks=request.num_blocks
        )
        
        if df.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "No se obtuvieron datos",
                    "message": f"No se obtuvieron datos para {request.symbol} con contract_month={contract_month}",
                    "suggestion": "Verifica que el símbolo y el mes de vencimiento sean correctos"
                }
            )
        
        # Guardar en base de datos si se solicita
        if request.save_to_db:
            timeframe = request.bar_size.replace(" ", "").lower()
            processor.save_market_data(df, request.symbol, timeframe)
            
            # Generar timeframes adicionales en background
            if timeframe == "1min":
                background_tasks.add_task(
                    processor.generate_timeframes,
                    request.symbol,
                    "1min"
                )
        
        return ExtractDataResponse(
            status="success",
            records=len(df),
            symbol=request.symbol,
            date_range={
                "start": df['Date'].min().isoformat(),
                "end": df['Date'].max().isoformat()
            },
            message=f"Datos extraídos y guardados correctamente"
        )
        
    except ImportError as e:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "ibapi no está instalado",
                "message": str(e),
                "solution": "Instala ibapi con: docker-compose exec backend pip install ibapi",
                "note": "También necesitas tener Interactive Brokers TWS o IB Gateway ejecutándose"
            }
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "No se puede conectar a Interactive Brokers",
                "message": str(e),
                "solution": "Asegúrate de que IB TWS o IB Gateway esté ejecutándose en el puerto configurado"
            }
        )
    except ValueError as e:
        # Error de validación del contrato (ej: falta contract_month o error 321)
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Error de validación del contrato",
                "message": str(e),
                "solution": "Especifica un contract_month válido (ej: '202512' para diciembre 2025) o verifica el símbolo"
            }
        )
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Error al extraer datos",
                "message": str(e) if str(e) else "Error desconocido",
                "type": type(e).__name__,
                "traceback": error_trace if settings.DEBUG else None
            }
        )
    finally:
        if 'extractor' in locals():
            extractor.disconnect()


@router.get("/data/{symbol}", response_model=MarketDataResponse)
async def get_data(
    symbol: str,
    timeframe: str = "1min",
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 1000,
    db: Session = Depends(get_db)
):
    """
    Obtener datos históricos desde la base de datos
    
    - **symbol**: Símbolo del instrumento
    - **timeframe**: Timeframe de los datos (1min, 5min, 15min, 30min, 1h, 4h, 1d)
    - **start_date**: Fecha de inicio (opcional)
    - **end_date**: Fecha de fin (opcional)
    - **limit**: Límite de registros a retornar (default: 1000)
    """
    query = db.query(MarketData).filter(MarketData.symbol == symbol.upper())
    query = query.filter(MarketData.timeframe == timeframe.lower())
    
    if start_date:
        query = query.filter(MarketData.timestamp >= start_date)
    if end_date:
        query = query.filter(MarketData.timestamp <= end_date)
    
    data = query.order_by(MarketData.timestamp.desc()).limit(limit).all()
    
    return MarketDataResponse(
        symbol=symbol.upper(),
        timeframe=timeframe.lower(),
        records=len(data),
        data=[
            {
                "timestamp": d.timestamp.isoformat(),
                "open": d.open,
                "high": d.high,
                "low": d.low,
                "close": d.close,
                "volume": d.volume,
                "count": d.count
            }
            for d in reversed(data)  # Revertir para orden cronológico
        ]
    )


@router.get("/symbols")
async def get_available_symbols(db: Session = Depends(get_db)):
    """
    Obtener lista de símbolos disponibles en la base de datos
    """
    symbols = db.query(MarketData.symbol).distinct().all()
    return {
        "symbols": [s[0] for s in symbols],
        "count": len(symbols)
    }


@router.get("/timeframes/{symbol}")
async def get_available_timeframes(symbol: str, db: Session = Depends(get_db)):
    """
    Obtener timeframes disponibles para un símbolo
    """
    timeframes = db.query(MarketData.timeframe).filter(
        MarketData.symbol == symbol.upper()
    ).distinct().all()
    
    return {
        "symbol": symbol.upper(),
        "timeframes": [t[0] for t in timeframes],
        "count": len(timeframes)
    }

