import ujson
class Packet:
    unit:str
    value=None
    def __init__(self,unit:str,value):
        self.unit=unit
        self.value=value
    
    def toJson(self):
      return ujson.dumps({'u': self.unit,'v': self.value})
    
    def parse(self, content: str):
        # JSON içeriğini ayrıştır
        data = ujson.loads(content)
        
        # 'u' ve 'v' anahtarlarına sahip olup olmadığını kontrol et
        if 'u' in data and 'v' in data:
            self.unit = data['u']
            self.value = data['v']
        else:
            raise ValueError("Invalid content format: 'u' or 'v' key missing")
        

