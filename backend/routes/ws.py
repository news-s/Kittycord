from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from users import servers, users, Message
import typing
import json

from auth_token import verify_token

class Socket:
    websocket: WebSocket
    user_id: int
    current_channel: int

    def __init__(self, websocket: WebSocket, user_id: int, current_channel: int):
        self.websocket = websocket
        self.user_id = user_id
        self.current_channel = current_channel

    async def send(self, message: str):
        _ = await self.websocket.send_json(message)

    async def handle_message(self, msg):
        if len(msg["content"]) > 1000:
            res = {
                "status": 400,
                "message": "Message content is too long"
            }
            await self.websocket.send_json(json.dumps(res))
            return



        # TODO database integration
        for server in servers:
            for channel in server.channels:
                if channel.id == self.current_channel:
                    channel.messages.append(Message(1, self.user_id, msg["content"]))

                    message = {
                        "author_id": self.user_id,
                        "channel_id": self.current_channel,
                        "content": msg["content"],
                        "id": 0 # TODO return actual message id
                    }
                    await broadcast.broadcast(message)

                    res = {
                        "status": 200,
                        "id": 0 # TODO return actual message id
                    }
                    await self.websocket.send_json(json.dumps(res))

    async def handle_channel(self, msg):
        # TODO database integration

        found = False

        for server in servers:
            for channel in server.channels:
                if channel.id == int(msg["content"]):
                    res = {
                        "status": 200,
                        "messages": channel.messages
                    }
                    await self.websocket.send_json(json.dumps(res, default=lambda o: o.__dict__))

                    self.current_channel = int(msg["content"])
                    found = True
                    break

        if not found:
            res = {
                "status": 404,
                "message": "Channel not found"
            }
            await self.websocket.send_json(json.dumps(res))

    async def handle_server(self, msg):
        # TODO database intergration

        found = True

        for server in servers:
            if server.id == msg["content"]:
                self.current_channel = server.channels[0].id

                res = {
                    "status": 200,
                    "channels": [channel.name for channel in server.channels],
                    "messages": server.channels[0].messages,
                }
                await self.websocket.send_json(json.dumps(res, default=lambda o: o.__dict__))

        if not found:
            res = {
                "status": 404,
                "message": "Server not found"
            }
            await self.websocket.send_json(json.dumps(res))

class Broadcaster:
    connections: list[Socket]

    def __init__(self):
        self.connections = []

    async def broadcast(self, message: str):
        for socket in self.connections:
            await socket.send(message)


router = APIRouter()
broadcast = Broadcaster()

@router.websocket("/ws")
async def ws(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return

    try:
        user_id = verify_token(token)
    except HTTPException:
        await websocket.close(code=1008)
        return

    await websocket.accept()

    socket = Socket(websocket, int(user_id), 1)
    broadcast.connections.append(socket)
    res = {
        "status": 200
    }
    await websocket.send_json(json.dumps(res))
    
    try:
        while True:
            raw = await websocket.receive_text()
            msg: dict[str, typing.Any] = json.loads(raw)

            if msg["type"] == None:
                res = {
                    "status": 400,
                    "message": "Message type missing"
                }
                await websocket.send_json(json.dumps(res))
                continue

            match msg["type"]:
                case "message":
                    await socket.handle_message(msg)
                
                case "channel":
                    await socket.handle_channel(msg)

                case "server":
                    await socket.handle_server(msg)

                case _:
                    res = {
                        "status": 400,
                        "message": "Message type invalid"
                    }
                    await websocket.send_json(json.dumps(res))
                
    except WebSocketDisconnect:
        print(f"User {user_id} disconnected.")