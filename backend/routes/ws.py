from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
import json

from auth_token import verify_token
from database.messages import store_channel_message, get_last_messsages_from_channel
from database.channels import get_channels, get_server_id
from database.profile import get_user_data

class Socket:
    websocket: WebSocket
    user_id: int
    current_channel: int
    current_server: int

    def __init__(self, websocket: WebSocket, user_id: int):
        self.websocket = websocket
        self.user_id = user_id
        self.current_channel = None
        self.current_server = None

    async def send(self, message):
        match message["type"]:
            case "new_message":
                if message["channel_id"] != self.current_channel:
                    return
                _ = await self.websocket.send_json(json.dumps(message))
            
            case "edit_message":
                if message["channel_id"] != self.current_channel:
                    return
                _ = await self.websocket.send_json(json.dumps(message))

            case  "edit_channel_name":
                if message["server_id"] != self.current_server:
                    return
                _ = await self.websocket.send_json(json.dumps(message))

            case "edit_server_name":
                if message["server_id"] != self.current_server:
                    return
                _ = await self.websocket.send_json(json.dumps(message))

            

    async def handle_error(self, status_code: int, detail: str):
        response = {
                "status": status_code,
                "detail": detail
            }
        await self.websocket.send_json(json.dumps(response))
        return

    async def handle_message(self, msg: dict[str, str]):
        if self.current_channel == None:
            self.handle_error(400, "Channel not yet selected")
            return

        if len(msg["content"]) > 1000:
            self.handle_error(400, "Message content is too long")
            return
        

        id = store_channel_message(self.user_id, self.current_channel, msg["content"], None)["message_id"]

        message = {
            "type": "new_message",
            "author_id": self.user_id,
            "channel_id": self.current_channel,
            "content": msg["content"],
            "id": id
        }
        await broadcast.broadcast(message)


        response = {
            "status": 201,
            "id": id
        }
        await self.websocket.send_json(json.dumps(response))

    async def handle_channel(self, msg: dict[str, str]):
        try:
            channel_id = int(msg["content"])
        except ValueError:
            self.handle_error(400, "Channel ID is not a number")
            return
        
        res = get_server_id(channel_id)

        if res["status"] == "error":
            self.handle_error(404, "Channel not found")
            return

        server_id = res["server_id"]
        res = get_user_data(self.user_id)

        if res["status"] == "error":
            self.handle_error(404, "User doesn't exist")
            return
        
        if int(server_id) not in res["servers"]:
            self.handle_error(403, "User is not member of the requested server")
            return
    
        res = get_last_messsages_from_channel(50, channel_id)

        if res["status"] == "error":
            self.handle_error(500, "Channel initially found but failed to load messages")
            return
        
        self.current_channel = channel_id
        self.current_server = server_id

        response = {
            "status": 200,
            "messages": res["messages"]
        }
        await self.websocket.send_json(json.dumps(response, default=lambda o: o.__dict__))

    async def handle_server(self, msg: dict[str, str]):
        res = get_user_data(self.user_id)

        if res["status"] == "error":
            self.handle_error(500, "Connected user doesn't exist")
            return
        
        if int(msg["content"]) not in res["servers"]:
            self.handle_error(403, "User is not member of the requested server")
            return

        res = get_channels(msg["content"])

        if res["status"] == "error":
            self.handle_error(404, "Server not found")
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
            self.handle_error(500, "Channel found but failed to get messages")
            return
        

        self.current_channel = channels[0]["id"]
        self.current_server = int(msg["content"])
        
        messages = res["messages"]
        
        response = {
            "status": 200,
            "channels": [{"id": channel["id"], "name": channel["name"]} for channel in channels],
            "messages": [{"author_id": message["author_id"], "date": message["date"], "content": message["content"]} for message in messages]
        }
        await self.websocket.send_json(json.dumps(response))

class Broadcaster:
    connections: list[Socket]

    def __init__(self):
        self.connections = []

    async def broadcast(self, message):
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

    socket = Socket(websocket, int(user_id))
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
                socket.handle_error(400, "Message type missing")

            match msg["type"]:
                case "message":
                    await socket.handle_message(msg)
                
                case "channel":
                    await socket.handle_channel(msg)

                case "server":
                    await socket.handle_server(msg)

                case _:
                    socket.handle_error(400, "Message type is invalid")
                
    except WebSocketDisconnect:
        print(f"User {user_id} disconnected.")
