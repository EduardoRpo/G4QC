#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión a IB Gateway
"""
import sys
import time

try:
    from ibapi.client import EClient
    from ibapi.wrapper import EWrapper
    IBAPI_AVAILABLE = True
except ImportError:
    print("❌ Error: ibapi no está instalado")
    print("Instálalo con: pip install ibapi")
    sys.exit(1)

from app.core.config import settings


class TestIBConnection(EClient, EWrapper):
    """Clase simple para probar la conexión"""
    
    def __init__(self):
        EClient.__init__(self, self)
        self.connected = False
        self.next_valid_order_id = None
    
    def nextValidId(self, orderId):
        """Callback cuando se establece la conexión"""
        print(f"✅ ¡Conexión exitosa! Next Valid Order ID: {orderId}")
        self.next_valid_order_id = orderId
        self.connected = True
        self.disconnect()
    
    def error(self, reqId, code, msg):
        """Callback para errores"""
        # Ignorar mensajes informativos
        if code not in [2104, 2106, 2158]:
            print(f"⚠️  Error {code}: {msg}")
            if code == 502:  # Couldn't connect to TWS
                print("❌ No se pudo conectar a IB Gateway")
                self.disconnect()
            elif code == 504:  # Not connected
                print("❌ No conectado a IB Gateway")
                self.disconnect()


def test_connection():
    """Probar la conexión a IB Gateway"""
    print("=" * 60)
    print("🧪 Prueba de Conexión a Interactive Brokers Gateway")
    print("=" * 60)
    print(f"📍 Host: {settings.IB_HOST}")
    print(f"📍 Puerto: {settings.IB_PORT}")
    print(f"📍 Client ID: {settings.IB_CLIENT_ID}")
    print("-" * 60)
    
    client = TestIBConnection()
    
    try:
        print("🔄 Intentando conectar...")
        client.connect(settings.IB_HOST, settings.IB_PORT, settings.IB_CLIENT_ID)
        
        # Ejecutar el loop de mensajes en un thread separado
        import threading
        def run():
            client.run()
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        
        # Esperar hasta 15 segundos para la conexión
        timeout = 15
        start_time = time.time()
        
        while not client.connected and (time.time() - start_time) < timeout:
            time.sleep(0.5)
        
        if client.connected:
            print("=" * 60)
            print("✅ ¡PRUEBA EXITOSA! IB Gateway está funcionando correctamente")
            print("=" * 60)
            return True
        else:
            print("=" * 60)
            print("❌ TIMEOUT: No se recibió confirmación de conexión en 15 segundos")
            print("=" * 60)
            client.disconnect()
            return False
            
    except Exception as e:
        print("=" * 60)
        print(f"❌ ERROR: {str(e)}")
        print("=" * 60)
        return False
    finally:
        if not client.connected:
            try:
                client.disconnect()
            except:
                pass


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

