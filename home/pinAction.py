import machine
import ujson
from home.packet import Packet

class PinAction:
    def __init__(self, uart_num: int, baudrate: int = 115200):
        # UART'ı başlat
        self.uart = machine.UART(uart_num, baudrate=baudrate)
        self.uart.init(bits=8, parity=None, stop=2)  # 8 bit veri, parity yok, 2 stop biti

    def send_package(self, packet: Packet):
        # JSON verisini UART üzerinden gönder
        print(packet.toJson())
        self.uart.write(packet.toJson() + '\n')

# Örnek kullanım
if __name__ == '__main__':
    # UART1 örneği, 9600 baud hızında
    pin_action = PinAction(uart_num=1, baudrate=115200)
    
    # Paket oluşturma ve gönderme
    packet = Packet(unit="temperature", value=23.5)
    pin_action.send_package(packet)


