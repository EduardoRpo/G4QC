"""
Data Processor - Procesamiento y almacenamiento de datos de mercado
Incluye normalización robusta de timezones (UTC)
"""
import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
import pytz
from app.models.data import MarketData


class DataProcessor:
    """
    Procesador de datos de mercado:
    - Normaliza timezones a UTC (crítico para datos de diferentes exchanges)
    - Guarda datos en base de datos
    - Genera timeframes adicionales (5min, 15min, etc.) desde 1min
    - Valida y limpia datos
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def normalize_timezone(self, df: pd.DataFrame, source_timezone: Optional[str] = None) -> pd.DataFrame:
        """
        Normalizar timezone de datos a UTC
        
        Args:
            df: DataFrame con columna Date (datetime)
            source_timezone: Timezone origen (ej: 'America/New_York', 'America/Chicago')
                          Si es None, asume que ya está en UTC o detecta automáticamente
        
        Returns:
            DataFrame con timestamps normalizados a UTC
        """
        if df.empty or 'Date' not in df.columns:
            return df
        
        df = df.copy()
        
        # Si la columna Date no tiene timezone info, asumimos UTC
        if df['Date'].dtype.tz is None:
            if source_timezone:
                # Convertir desde timezone origen a UTC
                tz = pytz.timezone(source_timezone)
                df['Date'] = df['Date'].dt.tz_localize(tz, ambiguous='infer', nonexistent='shift_forward')
                df['Date'] = df['Date'].dt.tz_convert(pytz.UTC)
            else:
                # Asumir UTC y localizar
                df['Date'] = df['Date'].dt.tz_localize(pytz.UTC, ambiguous='infer', nonexistent='shift_forward')
        else:
            # Ya tiene timezone, convertir a UTC
            df['Date'] = df['Date'].dt.tz_convert(pytz.UTC)
        
        return df
    
    def save_market_data(
        self, 
        df: pd.DataFrame, 
        symbol: str, 
        timeframe: str,
        source_timezone: Optional[str] = None
    ) -> int:
        """
        Guardar datos de mercado en PostgreSQL con normalización de timezone
        
        Args:
            df: DataFrame con columnas Date, Open, High, Low, Close, Volume, Count
            symbol: Símbolo del instrumento
            timeframe: Timeframe (1min, 5min, etc.)
            source_timezone: Timezone origen del exchange (ej: 'America/Chicago' para CME)
                           Si es None, asume UTC
        
        Returns:
            Número de registros guardados
        """
        if df.empty or 'Date' not in df.columns:
            return 0
        
        # Normalizar timezone a UTC antes de guardar
        df = self.normalize_timezone(df, source_timezone)
        
        # Mapeo de símbolos comunes a sus timezones de exchange
        # (puedes expandir esto según necesites)
        exchange_timezones = {
            'ES': 'America/Chicago',  # CME
            'NQ': 'America/Chicago',  # CME
            'YM': 'America/Chicago',  # CME
            'EC': 'America/New_York', # CME
            '6B': 'America/New_York', # CME
            'GC': 'America/New_York', # COMEX
            'CL': 'America/New_York', # NYMEX
            'RB': 'America/New_York', # NYMEX
        }
        
        # Si no se especificó timezone y conocemos el símbolo, usar su timezone
        if source_timezone is None and symbol.upper() in exchange_timezones:
            df = self.normalize_timezone(df, exchange_timezones[symbol.upper()])
        
        # Preparar registros para UPSERT
        records = []
        for _, row in df.iterrows():
            # Asegurar que el timestamp es timezone-aware en UTC
            timestamp = row['Date']
            if timestamp.tzinfo is None:
                timestamp = pytz.UTC.localize(timestamp)
            elif timestamp.tzinfo != pytz.UTC:
                timestamp = timestamp.astimezone(pytz.UTC)
            
            records.append({
                'symbol': symbol.upper(),
                'timeframe': timeframe.lower(),
                'timestamp': timestamp,
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
                'volume': int(row['Volume']),
                'count': int(row.get('Count', 0))
            })
        
        if not records:
            return 0
        
        # Usar UPSERT (INSERT ... ON CONFLICT DO NOTHING) para prevenir duplicados
        # Esto es thread-safe y eficiente
        from sqlalchemy.dialects.postgresql import insert
        
        stmt = insert(MarketData).values(records)
        stmt = stmt.on_conflict_do_nothing(
            index_elements=['symbol', 'timeframe', 'timestamp']
        )
        
        result = self.db.execute(stmt)
        self.db.commit()
        
        # Contar cuántos registros se insertaron realmente
        inserted_count = result.rowcount if hasattr(result, 'rowcount') else len(records)
        
        print(f"✅ Guardados {inserted_count} registros nuevos para {symbol} ({timeframe}) - Timezone normalizado a UTC")
        if inserted_count < len(records):
            skipped = len(records) - inserted_count
            print(f"   ⏭️  {skipped} registros ya existían (duplicados ignorados)")
        
        return inserted_count
    
    def generate_timeframes(self, symbol: str, source_timeframe: str = "1min"):
        """
        Generar timeframes adicionales desde el timeframe fuente
        
        Args:
            symbol: Símbolo del instrumento
            source_timeframe: Timeframe fuente (debe ser el más pequeño, ej: "1min")
        """
        if source_timeframe != "1min":
            print(f"⚠️ Solo se pueden generar timeframes desde 1min")
            return
        
        # Obtener datos de 1min
        data = self.db.query(MarketData).filter(
            MarketData.symbol == symbol.upper(),
            MarketData.timeframe == "1min"
        ).order_by(MarketData.timestamp).all()
        
        if not data:
            print(f"⚠️ No hay datos de 1min para {symbol}")
            return
        
        # Convertir a DataFrame
        df = pd.DataFrame([{
            'Date': d.timestamp,
            'Open': d.open,
            'High': d.high,
            'Low': d.low,
            'Close': d.close,
            'Volume': d.volume,
            'Count': d.count
        } for d in data])
        
        df.set_index('Date', inplace=True)
        
        # Timeframes a generar
        timeframes = {
            '5min': '5T',
            '15min': '15T',
            '30min': '30T',
            '1h': '1H',
            '4h': '4H',
            '1d': '1D'
        }
        
        for tf_name, tf_resample in timeframes.items():
            # Verificar si ya existen datos para este timeframe
            existing = self.db.query(MarketData).filter(
                MarketData.symbol == symbol.upper(),
                MarketData.timeframe == tf_name
            ).first()
            
            if existing:
                print(f"⏭️ Timeframe {tf_name} ya existe para {symbol}, omitiendo...")
                continue
            
            # Resamplear datos
            df_resampled = df.resample(tf_resample).agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum',
                'Count': 'sum'
            }).dropna()
            
            if not df_resampled.empty:
                # Guardar datos resampleados
                records = []
                for timestamp, row in df_resampled.iterrows():
                    records.append(MarketData(
                        symbol=symbol.upper(),
                        timeframe=tf_name,
                        timestamp=timestamp,
                        open=float(row['Open']),
                        high=float(row['High']),
                        low=float(row['Low']),
                        close=float(row['Close']),
                        volume=int(row['Volume']),
                        count=int(row['Count'])
                    ))
                
                self.db.bulk_save_objects(records)
                self.db.commit()
                print(f"✅ Generado timeframe {tf_name}: {len(records)} registros para {symbol}")
    
    def update_timeframes_incremental(self, symbol: str, source_timeframe: str = "1min"):
        """
        Actualizar timeframes solo con datos nuevos (incremental)
        Más eficiente que regenerar todo desde cero
        
        Args:
            symbol: Símbolo del instrumento
            source_timeframe: Timeframe fuente (debe ser "1min")
        """
        if source_timeframe != "1min":
            print(f"⚠️ Solo se pueden actualizar timeframes desde 1min")
            return
        
        from sqlalchemy import func
        
        # Timeframes a generar
        timeframes = {
            '5min': '5T',
            '15min': '15T',
            '30min': '30T',
            '1h': '1H',
            '4h': '4H',
            '1d': '1D'
        }
        
        # Obtener el último timestamp procesado para cada timeframe
        last_timestamps = {}
        for tf_name in timeframes.keys():
            last = self.db.query(func.max(MarketData.timestamp)).filter(
                MarketData.symbol == symbol.upper(),
                MarketData.timeframe == tf_name
            ).scalar()
            last_timestamps[tf_name] = last or datetime(1970, 1, 1, tzinfo=pytz.UTC)
        
        # Obtener el mínimo de los últimos timestamps para saber desde dónde procesar
        min_last_timestamp = min(last_timestamps.values()) if last_timestamps.values() else datetime(1970, 1, 1, tzinfo=pytz.UTC)
        
        # Obtener solo datos de 1min NUEVOS (después del último procesado)
        new_data = self.db.query(MarketData).filter(
            MarketData.symbol == symbol.upper(),
            MarketData.timeframe == "1min",
            MarketData.timestamp > min_last_timestamp
        ).order_by(MarketData.timestamp).all()
        
        if not new_data:
            print(f"⏭️ No hay datos nuevos de 1min para {symbol}, omitiendo actualización de timeframes")
            return
        
        # Convertir a DataFrame
        df = pd.DataFrame([{
            'Date': d.timestamp,
            'Open': d.open,
            'High': d.high,
            'Low': d.low,
            'Close': d.close,
            'Volume': d.volume,
            'Count': d.count
        } for d in new_data])
        
        if df.empty:
            return
        
        df.set_index('Date', inplace=True)
        
        # Actualizar cada timeframe solo con datos nuevos
        for tf_name, tf_resample in timeframes.items():
            # Resamplear solo los datos nuevos
            df_resampled = df.resample(tf_resample).agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum',
                'Count': 'sum'
            }).dropna()
            
            if df_resampled.empty:
                continue
            
            # Filtrar solo los timestamps que son nuevos para este timeframe
            existing_timestamps = set(
                row[0] for row in self.db.query(MarketData.timestamp).filter(
                    MarketData.symbol == symbol.upper(),
                    MarketData.timeframe == tf_name
                ).all()
            )
            
            # Preparar registros nuevos usando UPSERT
            records = []
            for timestamp, row in df_resampled.iterrows():
                if timestamp not in existing_timestamps:
                    records.append({
                        'symbol': symbol.upper(),
                        'timeframe': tf_name,
                        'timestamp': timestamp,
                        'open': float(row['Open']),
                        'high': float(row['High']),
                        'low': float(row['Low']),
                        'close': float(row['Close']),
                        'volume': int(row['Volume']),
                        'count': int(row['Count'])
                    })
            
            if records:
                # Usar UPSERT para prevenir duplicados
                from sqlalchemy.dialects.postgresql import insert
                
                stmt = insert(MarketData).values(records)
                stmt = stmt.on_conflict_do_nothing(
                    index_elements=['symbol', 'timeframe', 'timestamp']
                )
                self.db.execute(stmt)
                self.db.commit()
                
                print(f"✅ Actualizado timeframe {tf_name}: {len(records)} registros nuevos para {symbol}")

