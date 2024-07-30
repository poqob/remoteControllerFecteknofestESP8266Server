import network
import time

class Connection:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.sta_if = network.WLAN(network.STA_IF)
        self.sta_if.active(True)
        
    def connect(self, timeout=15):
        self.sta_if.connect(self.ssid, self.password)
        print('Connecting to network...')
        
        start_time = time.time()
        while not self.sta_if.isconnected():
            if time.time() - start_time > timeout:
                print("Connection timeout.")
                return False
            print('.')
            time.sleep(1)
        
        if self.sta_if.isconnected():
            print('Network config:', self.sta_if.ifconfig())
            return True
        else:
            return False

