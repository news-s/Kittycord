from fastapi import WebSocket

class BroadCastMessage:
    author_id: int
    channel_id: int
    content: str

    def __init__(self, author_id: int, channel_id: int, content: str):
        self.author_id = author_id
        self.channel_id = channel_id
        self.content = content

    def json(self):
        return {
            "author_id": self.author_id,
            "channel_id": self.channel_id,
            "content": self.content
        }

class Socket:
    websocket: WebSocket
    user_id: int
    current_channel: int

    def __init__(self, websocket: WebSocket, user_id: int, current_channel: int):
        self.websocket = websocket
        self.user_id = user_id
        self.current_channel = current_channel

    async def send(self, message: BroadCastMessage):
        if message.channel_id == self.current_channel and message.author_id != self.user_id:
            _ = await self.websocket.send_json(message.json())

class Broadcaster:
    connections: list[Socket]

    def __init__(self):
        self.connections = []

    async def broadcast(self, message: BroadCastMessage):
        for socket in self.connections:
            await socket.send(message)
