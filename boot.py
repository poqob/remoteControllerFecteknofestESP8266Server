# This file is executed on every boot (including wake-boot from deepsleep)

#import esp

#esp.osdebug(None)

import os
import machine
import time
from home.connection import Connection
from home.service import ESP8266WebServer
import gc

#import webrepl

#webrepl.start()

def main():
    try:
        conn = Connection(ssid='merkur', password='merkur.online')
        
        is_connected = conn.connect()

        # Bağlantı sağlanamazsa programı durdur
        if not is_connected:
            print("Bağlantı sağlanamadı, program sonlandırılıyor.")
            return  # REPL moduna döner

        server = ESP8266WebServer()
        server.run()

        print("Hoşgeldin sahip.")
    except KeyboardInterrupt:
        print("Program kesintiye uğradı. REPL moduna dönülüyor.")
    finally:
        gc.collect()

if __name__ == '__main__':
    main()

