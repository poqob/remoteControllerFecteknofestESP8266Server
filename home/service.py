import network
import socket
import time
from home.pinAction import PinAction
from home.packet import Packet

class ESP8266WebServer:
    def __init__(self):
        self.server = None
        self.embed = PinAction(uart_num=0, baudrate=115200)

    def init_server(self):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self.server = socket.socket()
        self.server.bind(addr)
        self.server.listen(1)
        print('Listening on', addr)
        
    def handle_request(self, client):
        try:
            # İstemciden veriyi okumak için bir döngü kullan
            request_data = b""
            while True:
                chunk = client.recv(1024)
                request_data += chunk
                if len(chunk) < 1024:
                    break
            
            request_str = request_data.decode('utf-8')  # Baytları UTF-8 ile dizeye dönüştür
            

            # İstek başlıklarını ve gövdeyi ayırma
            headers, body = self.split_headers_and_body(request_str)

            # Content-Length başlığı varsa gövdeyi doğrulama
            content_length = self.get_header_value(headers, 'Content-Length')
            if content_length:
                content_length = int(content_length)
                if len(body) > content_length:
                    body = body[:content_length]
                elif len(body) < content_length:
                    # Eğer body eksikse, veriyi tamamlayın
                    while len(body) < content_length:
                        chunk = client.recv(content_length - len(body))
                        body += chunk.decode('utf-8')

           
            
            # JSON veri ayrıştırması ve paket gönderimi
            try:
                packet = Packet(unit="", value=None)
                packet.parse(body)
                
                self.embed.send_package(packet)
            except Exception as e:
                print("Error parsing packet:", e)

            # Yanıtı oluşturma ve gönderme
            response = 'HTTP/1.1 200 OK\nContent-Type: text/plain\n' \
                       'Access-Control-Allow-Origin: *\n' \
                       'Connection: close\n\n' \
                       f'{body}'
            client.send(response.encode('utf-8'))
        except Exception as e:
            print("Error handling request:", e)
        finally:
            client.close()


    def split_headers_and_body(self, request_str):
        try:
            headers, body = request_str.split('\r\n\r\n', 1)
        except ValueError:
            headers = request_str
            body = ""
        return headers, body

    def get_header_value(self, headers, header_name):
        for line in headers.split('\r\n'):
            if line.startswith(header_name + ':'):
                return line.split(':', 1)[1].strip()
        return None

    def run(self):
        self.init_server()
        
        while True:
            client, addr = self.server.accept()
            #print('Client connected from', addr)
            self.handle_request(client)
            time.sleep(1)  # Kısa bir süre bekleyip devam ediyoruz

if __name__ == '__main__':
    server = ESP8266WebServer()
    server.run()




