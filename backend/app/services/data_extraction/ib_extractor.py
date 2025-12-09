"""
Interactive Brokers Data Extractor
Refactorizado desde Data_Extract.ipynb
"""
import threading
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import pandas as pd

try:
    from ibapi.client import EClient
    from ibapi.wrapper import EWrapper
    from ibapi.contract import Contract
    IBAPI_AVAILABLE = True
except ImportError:
    IBAPI_AVAILABLE = False
    # Crear clases dummy para que el código no falle
    class EClient:
        pass
    class EWrapper:
        pass
    class Contract:
        pass

from app.core.config import settings


class IBDataExtractor(EClient, EWrapper):
    """
    Servicio para extraer datos históricos de Interactive Brokers
    Basado en el código de Data_Extract.ipynb
    """
    
    def __init__(self, host: Optional[str] = None, port: Optional[int] = None, client_id: Optional[int] = None):
        if not IBAPI_AVAILABLE:
            raise ImportError(
                "ibapi no está instalado. "
                "Instálalo con: pip install ibapi "
                "o desde: https://interactivebrokers.github.io/tws-api/"
            )
        EClient.__init__(self, self)
        self.host = host or settings.IB_HOST
        self.port = port or settings.IB_PORT
        self.client_id = client_id or settings.IB_CLIENT_ID
        self.datos_historicos: Dict[int, List] = {}
        self.objetos_datos: Dict[int, List] = {}
        self.error_en_req: Dict[int, bool] = {}  # Registrar errores por reqId
        self.evento = threading.Event()
        self.connected = False
        self.api_thread: Optional[threading.Thread] = None
    
    def connect_to_ib(self):
        """Conectar a Interactive Brokers"""
        if not self.connected:
            try:
                self.connect(self.host, self.port, self.client_id)
                self.api_thread = threading.Thread(target=self.run, daemon=True)
                self.api_thread.start()
                # Esperar conexión (timeout de 10 segundos)
                if not self.evento.wait(timeout=10):
                    raise ConnectionError("Timeout al conectar con Interactive Brokers")
                self.evento.clear()
                self.connected = True
            except Exception as e:
                raise ConnectionError(f"Error al conectar con IB: {str(e)}")
    
    def nextValidId(self, orderId):
        """Callback cuando se recibe el ID válido (conexión establecida)"""
        self.evento.set()
    
    def historicalData(self, reqId, bar):
        """Callback cuando se recibe un bar de datos históricos"""
        if reqId not in self.datos_historicos:
            self.datos_historicos[reqId] = []
            self.objetos_datos[reqId] = []
        
        self.datos_historicos[reqId].append({
            "Date": bar.date,
            "Open": bar.open,
            "High": bar.high,
            "Low": bar.low,
            "Close": bar.close,
            "Volume": bar.volume,
            "Count": bar.barCount
        })
        self.objetos_datos[reqId].append(bar)
    
    def historicalDataEnd(self, reqId, start, end):
        """Callback cuando termina la solicitud de datos históricos"""
        print(f"✅ Fin de datos históricos para ID: {reqId} | Rango: {start} -> {end}")
        self.evento.set()
    
    def error(self, reqId, code, msg):
        """Callback para errores"""
        # Ignorar mensajes informativos de conexión
        if code not in [2104, 2106, 2107, 2158]:
            print(f"❗ Error reqId={reqId}, code={code}, msg={msg}")
            # Error 321: necesita contract_month o local symbol
            if code == 321:
                self.error_en_req = getattr(self, 'error_en_req', {})
                self.error_en_req[reqId] = True
                self.evento.set()  # Desbloquear para que no se quede esperando
    
    def detect_instrument_type(self, symbol: str) -> dict:
        """
        Detectar automáticamente el tipo de instrumento basado en el símbolo
        
        Returns:
            dict con sec_type, exchange, currency, y si necesita contract_month
        """
        symbol_upper = symbol.upper()
        
        # Futuros conocidos
        futures_cme = ['ES', 'NQ', 'YM', 'RTY', 'EC', '6E', '6B', '6J', '6A', '6C', '6S', '6N', '6M']
        futures_nymex = ['CL', 'NG', 'RB', 'HO', 'GC', 'SI', 'HG', 'PA', 'PL', 'ZC', 'ZS', 'ZW', 'ZL', 'ZM', 'LE', 'HE', 'KE']
        futures_cbot = ['ZB', 'ZN', 'ZF', 'ZT', 'ZS', 'ZW', 'ZC', 'KE']
        
        # ETFs conocidos
        etfs = ['SPY', 'QQQ', 'TLT', 'IWM', 'DIA', 'GLD', 'SLV', 'USO', 'XLF', 'XLE']
        
        # Forex conocido (formato CURRENCY1CURRENCY2)
        if len(symbol_upper) == 6 and symbol_upper.isalpha():
            # Verificar si es un par de divisas común
            forex_pairs = ['EURUSD', 'GBPUSD', 'AUDUSD', 'USDJPY', 'USDCAD', 'USDCHF', 'NZDUSD', 
                          'EURGBP', 'EURJPY', 'GBPJPY', 'AUDJPY', 'EURAUD', 'EURCAD']
            if symbol_upper in forex_pairs:
                return {
                    'sec_type': 'CASH',
                    'exchange': 'IDEALPRO',
                    'currency': symbol_upper[3:6],  # Segunda divisa
                    'needs_contract_month': False
                }
        
        # Detectar futuros
        if symbol_upper in futures_cme:
            return {
                'sec_type': 'FUT',
                'exchange': 'CME',
                'currency': 'USD',
                'needs_contract_month': True,
                'trading_class': symbol_upper if symbol_upper in ['RB'] else None
            }
        elif symbol_upper in futures_nymex:
            return {
                'sec_type': 'FUT',
                'exchange': 'NYMEX' if symbol_upper in ['CL', 'NG', 'RB', 'HO'] else 'COMEX' if symbol_upper in ['GC', 'SI', 'HG', 'PA', 'PL'] else 'CME',
                'currency': 'USD',
                'needs_contract_month': True,
                'trading_class': symbol_upper if symbol_upper in ['RB', 'HE', 'LE'] else None
            }
        elif symbol_upper in futures_cbot:
            return {
                'sec_type': 'FUT',
                'exchange': 'CBOT',
                'currency': 'USD',
                'needs_contract_month': True,
                'trading_class': symbol_upper
            }
        
        # Detectar ETFs/Stocks
        if symbol_upper in etfs or (len(symbol_upper) <= 5 and symbol_upper.isalpha()):
            return {
                'sec_type': 'STK',
                'exchange': 'SMART',  # IB usa SMART para encontrar el mejor exchange
                'currency': 'USD',
                'needs_contract_month': False
            }
        
        # Por defecto, asumir futuro en CME
        return {
            'sec_type': 'FUT',
            'exchange': 'CME',
            'currency': 'USD',
            'needs_contract_month': True
        }
    
    def create_contract(
        self, 
        symbol: str, 
        sec_type: Optional[str] = None,
        exchange: Optional[str] = None,
        currency: Optional[str] = None,
        contract_month: Optional[str] = None,
        trading_class: Optional[str] = None
    ) -> Contract:
        """
        Crear contrato IB con detección automática del tipo de instrumento
        
        Args:
            symbol: Símbolo del instrumento (ES, NQ, SPY, EURUSD, etc.)
            sec_type: Tipo de contrato (FUT, STK, CASH). Si es None, se detecta automáticamente
            exchange: Exchange (CME, SMART, IDEALPRO, etc.). Si es None, se detecta automáticamente
            currency: Moneda. Si es None, se detecta automáticamente
            contract_month: Mes de vencimiento (ej: "202512"). Solo para futuros
            trading_class: Clase de trading (opcional). Solo para algunos futuros
        """
        # Detectar tipo de instrumento si no se especifica
        if sec_type is None:
            instrument_info = self.detect_instrument_type(symbol)
            sec_type = instrument_info['sec_type']
            exchange = exchange or instrument_info['exchange']
            currency = currency or instrument_info['currency']
            trading_class = trading_class or instrument_info.get('trading_class')
            
            # Solo agregar contract_month si es necesario y no se proporcionó
            if instrument_info['needs_contract_month'] and contract_month is None:
                # Calcular contract_month automáticamente para futuros
                from datetime import datetime
                now = datetime.utcnow()
                if now.day > 15 and now.month < 12:
                    contract_month = f"{now.year}{now.month + 1:02d}"
                elif now.day > 15 and now.month == 12:
                    contract_month = f"{now.year + 1}01"
                else:
                    contract_month = f"{now.year}{now.month:02d}"
        
        contrato = Contract()
        contrato.symbol = symbol
        
        # Para forex (CASH), el símbolo debe ser la primera divisa
        if sec_type == 'CASH':
            # EURUSD -> symbol=EUR, currency=USD
            if len(symbol) == 6 and symbol.isalpha():
                contrato.symbol = symbol[:3]
                contrato.currency = symbol[3:6]
            else:
                contrato.symbol = symbol
                contrato.currency = currency or 'USD'
        else:
            contrato.symbol = symbol
            contrato.currency = currency or 'USD'
        
        contrato.secType = sec_type
        contrato.exchange = exchange or 'CME'
        
        if contract_month and sec_type == 'FUT':
            contrato.lastTradeDateOrContractMonth = contract_month
        
        if trading_class:
            contrato.tradingClass = trading_class
        
        return contrato
    
    def extract_historical_data(
        self,
        symbol: str,
        duration: str = "1 M",
        bar_size: str = "1 min",
        end_date: Optional[datetime] = None,
        contract_month: Optional[str] = None,
        num_blocks: int = 1,
        exchange: str = "CME",
        trading_class: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Extraer datos históricos desde Interactive Brokers
        
        Args:
            symbol: Símbolo del instrumento (ES, NQ, EC, 6B, RB, GC, LE, HE, etc.)
            duration: Duración por bloque (ej: "1 M", "1 D", "3600 S")
            bar_size: Tamaño de barra (ej: "1 min", "5 mins", "1 hour")
            end_date: Fecha final (default: ahora UTC)
            contract_month: Mes de vencimiento (ej: "202512")
            num_blocks: Número de bloques a extraer
            exchange: Exchange del contrato
            trading_class: Clase de trading (para algunos contratos como RB)
        
        Returns:
            DataFrame con datos históricos (Date, Open, High, Low, Close, Volume, Count)
        """
        # Conectar si no está conectado
        if not self.connected:
            self.connect_to_ib()
        
        # Detectar tipo de instrumento y crear contrato
        instrument_info = self.detect_instrument_type(symbol)
        
        # Solo usar contract_month si el instrumento lo necesita
        if not instrument_info['needs_contract_month']:
            contract_month = None
        
        contrato = self.create_contract(
            symbol=symbol,
            contract_month=contract_month,
            exchange=exchange or instrument_info['exchange'],
            trading_class=trading_class or instrument_info.get('trading_class')
        )
        
        # Fecha final por defecto
        if end_date is None:
            end_date = datetime.utcnow()
        
        # Limpiar datos anteriores
        self.datos_historicos.clear()
        self.objetos_datos.clear()
        self.error_en_req.clear()
        all_dataframes = []
        
        # Extraer en bloques
        for i in range(num_blocks):
            end_str = end_date.strftime("%Y%m%d-%H:%M:%S")
            
            print(f"📥 Extrayendo bloque {i+1}/{num_blocks} para {symbol}...")
            
            self.reqHistoricalData(
                reqId=i+1,
                contract=contrato,
                endDateTime=end_str,
                durationStr=duration,
                barSizeSetting=bar_size,
                whatToShow="TRADES",
                useRTH=0,  # Incluir datos fuera de horas regulares
                formatDate=1,  # Formato YYYYMMDD HH:MM:SS
                keepUpToDate=False,
                chartOptions=[]
            )
            
            # Esperar a que termine la solicitud (timeout de 60 segundos)
            if not self.evento.wait(timeout=60):
                print(f"⚠️ Timeout esperando datos para bloque {i+1}")
            self.evento.clear()
            
            # Verificar si hubo error en este reqId
            if (i+1) in self.error_en_req and self.error_en_req[i+1]:
                error_msg = f"Error al solicitar datos para bloque {i+1}. Verifica el contract_month."
                print(f"❌ {error_msg}")
                raise ValueError(error_msg)
            
            # Procesar datos recibidos
            if (i+1) in self.datos_historicos and len(self.datos_historicos[i+1]) > 0:
                df_temp = pd.DataFrame(self.datos_historicos[i+1])
                df_temp['Date'] = pd.to_datetime(
                    df_temp['Date'], 
                    format='%Y%m%d %H:%M:%S', 
                    utc=True, 
                    errors='coerce'
                )
                all_dataframes.append(df_temp)
                print(f"✅ Bloque {i+1}: {len(df_temp)} registros recibidos")
            else:
                print(f"⚠️ Bloque {i+1}: No se recibieron datos")
            
            # Retroceder fecha para siguiente bloque
            if duration.endswith("M"):
                months = int(duration.split()[0])
                end_date = end_date - timedelta(days=30 * months)
            elif duration.endswith("D"):
                days = int(duration.split()[0])
                end_date = end_date - timedelta(days=days)
            elif duration.endswith("S"):
                seconds = int(duration.split()[0])
                end_date = end_date - timedelta(seconds=seconds)
        
        # Concatenar y limpiar datos
        if all_dataframes:
            df = pd.concat(all_dataframes, ignore_index=True)
            df = df.sort_values('Date').drop_duplicates(subset=['Date'])
            
            # Asegurar tipos numéricos
            for col in ['Open', 'High', 'Low', 'Close', 'Volume', 'Count']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            print(f"✅ Total de registros: {len(df)}")
            return df
        
        return pd.DataFrame()
    
    def disconnect(self):
        """Desconectar de Interactive Brokers"""
        if self.connected:
            try:
                EClient.disconnect(self)
                self.connected = False
                print("✅ Desconectado de Interactive Brokers")
            except Exception as e:
                print(f"⚠️ Error al desconectar: {str(e)}")

