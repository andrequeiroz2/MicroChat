class SocketManager:
    def __init__(self):
        
        self.socket_active_connections = []
    
    async def connect(self, ws):
        self.socket_active_connections.append(ws)
        
    
    async def disconnect(self, ws):
        self.socket_active_connections.remove(ws)

    
    async def send_personal_message(self, msg, ws):
        await ws.send(msg)
        
        
    async def broadcast(self, msg):
        for conn in self.socket_active_connections:
            name = msg['name']
            _msg = msg['msg']
            payload = str(name + ": " + _msg)
            await conn.send(payload)