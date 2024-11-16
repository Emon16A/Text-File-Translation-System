# This file manages the WebSocket connections

# A dictionary to hold active WebSocket connections by session_id
connections = {}

# If you intended to use a "manager" object, define it here.
class WebSocketManager:
    def __init__(self):
        self.connections = {}

    async def connect(self, session_id, websocket):
        self.connections[session_id] = websocket

    async def disconnect(self, session_id):
        if session_id in self.connections:
            del self.connections[session_id]

    async def send_message(self, session_id, message):
        if session_id in self.connections:
            await self.connections[session_id].send_text(message)

# If your code expects a "manager" instance:
manager = WebSocketManager()
