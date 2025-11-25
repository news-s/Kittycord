from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
import json

from auth_token import verify_token
from database.messages import store_channel_message, get_last_messsages_from_channel
from database.channels import get_channels
from database.profile import get_user_data

class Socket:
    websocket: WebSocket
    user_id: int
    current_channel: int

    def __init__(self, websocket: WebSocket, user_id: int, current_channel: int):
        self.websocket = websocket
        self.user_id = user_id
        self.current_channel = current_channel

    async def send(self, message: str):
        if message["channel_id"] == self.current_channel:
            _ = await self.websocket.send_json(message)

    async def handle_message(self, msg: dict[str, str]):
        if len(msg["content"]) > 1000:
            response = {
                "status": 400,
                "message": "Message content is too long"
            }
            await self.websocket.send_json(json.dumps(response))
            return
        

        id = store_channel_message(self.user_id, self.current_channel, msg["content"], None)

        message = {
            "author_id": self.user_id,
            "channel_id": self.current_channel,
            "content": msg["content"],
            "id": id
        }
        await broadcast.broadcast(json.dumps(message))


        response = {
            "status": 201,
            "id": id
        }
        await self.websocket.send_json(json.dumps(response))

    async def handle_channel(self, msg: dict[str, str]):
        res = get_last_messsages_from_channel(50, msg["content"])

        if res["status"] == "error":
            response = {
                "status": 404,
                "message": "Channel not found"
            }
            await self.websocket.send_json(json.dumps(response))
            return
        
        response = {
            "status": 200,
            "messages": res["messages"]
        }
        await self.websocket.send_json(json.dumps(response, default=lambda o: o.__dict__))

    async def handle_server(self, msg: dict[str, str]):
        res = get_user_data(self.user_id)

        if res["status"] == "error":
            response = {
                "status": 500,
                "message": "Connected user doesn't exist"
            }
            await self.websocket.send_json(json.dumps(response))
            return
        
        if msg["content"] not in res["servers"]:
            response = {
                "status": 403,
                "message": "User is not member of the requested server"
            }
            await self.websocket.send_json(json.dumps(response))
            return

        res = get_channels(msg["content"])

        if res["status"] == "error":
            response = {
                "status": 404,
                "message": "Server not found"
            }
            await self.websocket.send_json(json.dumps(response))
            return
        
        channels = res["channels"]

        if len(channels) == 0:
            response = {
                "status": 200,
                "channels": [],
                "messages": []
            }
            await self.websocket.send_json(json.dumps(response))
            return

        res = get_last_messsages_from_channel(50, channels[0]["id"])

        if res["status"] == "error":
            response = {
                "status": 500,
                "message": "Channel found but failed to get messages"
            }
            await self.websocket.send_json(json.dumps(response))
            return
        
        messages = res["messages"]
        
        response = {
            "status": 200,
            "channels": [(channel["id"], channel["name"]) for channel in channels],
            "messages": [(message["author_id"], message["date"], message["content"]) for message in messages]
        }
        await self.websocket.send_json(json.dumps(response))

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
        "status": 200,
        "user_id": int(user_id)
    }
    await websocket.send_json(json.dumps(res))
    
    try:
        while True:
            raw = await websocket.receive_text()
            msg: dict[str, str] = json.loads(raw)

            if msg["type"] == "":
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
