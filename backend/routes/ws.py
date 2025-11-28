from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
import json
import datetime

from auth_token import verify_token
from database.friends import is_friends
from database.dms import get_messsages_from_dm, store_direct_message
from database.servers import get_owner_id
from database.roles import get_user_roles_in_server
from database.admin_tool import is_user_muted
from database.messages import store_channel_message, get_last_messsages_from_channel
from database.channels import get_channels, get_role_needed, get_server_id
from database.profile import get_user_data

class Socket:
    websocket: WebSocket
    user_id: int
    
    current_channel: int
    current_server: int
    is_muted: bool

    current_dm: int

    def __init__(self, websocket: WebSocket, user_id: int):
        self.websocket = websocket
        self.user_id = user_id

        self.current_channel = None
        self.current_server = None
        self.is_muted = False

        self.current_dm = None

    async def send(self, message):
        classes = message["class"].copy()
        message["class"] = None

        
        for classifier in classes:
            should_send = False
            match classifier:
                case "user":
                    should_send = message["user_id"] == self.user_id

                case "channel":
                    should_send = message["channel_id"] == self.current_channel
                    
                case "server":
                    should_send = message["server_id"] == self.current_server

                case "reset_ids":
                    if message["type"] == "remove_channel" and message["channel_id"] == self.current_channel:
                        self.current_channel = None
                        self.current_server = None
                    if message["type"] == "remove_server" and message["server_id"] == self.current_server:
                        self.current_channel = None
                        self.current_server = None

                case "author":
                    should_send = self.user_id == message["author_id"]

                case "reciever":
                    should_send = self.user_id == message["reciever_id"]

                case "mute":
                    if self.user_id == message["user_id"] and self.current_server == message["server_id"]:
                        self.is_muted = True

                case "unmute":
                    if self.user_id == message["user_id"] and self.current_server == message["server_id"]:
                        self.is_muted = False
                

                case _:
                    pass

            if should_send:
                _ = await self.websocket.send_json(message)
            
        return
            

    async def handle_error(self, status_code: int, detail: str):
        await self.websocket.send_json({
                "status": status_code,
                "detail": detail
            })
        return

    async def handle_message(self, msg: dict[str, str]):
        if self.is_muted:
            await self.handle_error(403, "User is muted")
            return

        if self.current_channel == None:
            await self.handle_error(400, "Channel not yet selected")
            return

        if len(msg["content"]) > 1000:
            await self.handle_error(400, "Message content is too long")
            return

        message_id = store_channel_message(self.user_id, self.current_channel, msg["content"], None)["message_id"]

        await broadcast.broadcast({
            "class": ["channel"],
            "type": "new_message",
            "author_id": self.user_id,
            "channel_id": self.current_channel,
            "date": str(datetime.datetime.now()),
            "content": msg["content"],
            "message_id": message_id
        })

        await self.websocket.send_json({
            "status": 201,
            "message": "success"
        })

    async def handle_channel(self, msg: dict[str, str]):
        try:
            channel_id = int(msg["content"])
        except Exception:
            await self.handle_error(400, "Channel ID is not a number")
            return
        
        res = get_server_id(channel_id)

        if res["status"] == "error":
            await self.handle_error(404, "Channel not found")
            return

        server_id = res["server_id"]
        res = get_user_data(self.user_id)

        if res["status"] == "error":
            await self.handle_error(404, "User doesn't exist")
            return
        
        if int(server_id) not in res["servers"]:
            await self.handle_error(403, "User is not member of the requested server")
            return
        
        roles = get_user_roles_in_server(self.user_id, server_id)["roles"]
        is_user_owner = get_owner_id(server_id)["owner_id"] == self.user_id
        role_needed = get_role_needed(channel_id)["role_needed"]

        if is_user_owner and (role_needed not in roles and role_needed != None):
            await self.handle_error(403, "User does not have the required role to view this channel")
            return
    

        try:
            start_from = msg["start_from"]
        except KeyError:
            start_from = 0
        res = get_last_messsages_from_channel(50, channel_id, start_count=start_from)

        if res["status"] == "error":
            await self.handle_error(500, "Channel initially found but failed to load messages")
            return
        
        is_muted = is_user_muted(self.user_id, server_id)["muted"]
        
        self.current_dm = None
        self.current_channel = channel_id
        self.current_server = server_id
        self.is_muted = is_muted

        await self.websocket.send_json({
            "status": 200,
            "type": "load_channel",
            "messages": res["messages"],
            "is_muted": is_muted,
        })

    async def handle_server(self, msg: dict[str, str]):
        res = get_user_data(self.user_id)

        if res["status"] == "error":
            await self.handle_error(500, "Connected user doesn't exist")
            return
        
        if int(msg["content"]) not in res["servers"]:
            await self.handle_error(403, "User is not member of the requested server")
            return

        res = get_channels(msg["content"])

        if res["status"] == "error":
            await self.handle_error(404, "Server not found")
            return
        
        channels = res["channels"]
        roles = get_user_roles_in_server(self.user_id, msg["content"])["roles"]
        is_user_owner = get_owner_id(int(msg["content"]))["owner_id"] == self.user_id

        is_muted = is_user_muted(self.user_id, msg["content"])["muted"]
        self.is_muted = is_muted

        if len(channels) == 0:
            self.current_channel = None
            self.current_server = int(msg["content"])
            await self.websocket.send_json({
                "status": 200,
                "type": "load_server",
                "channels": [],
                "messages": [],
                "is_muted": is_muted,
            })
            return

        res = get_last_messsages_from_channel(50, channels[0]["id"])

        if res["status"] == "error":
            await self.handle_error(500, "Channel found but failed to get messages")
            return
        

        self.current_dm = None
        self.current_channel = channels[0]["id"]
        self.current_server = int(msg["content"])
        
        messages = res["messages"]
        
        await self.websocket.send_json({
            "status": 200,
            "type": "load_server",
            "channels": [{
                "channel_id": channel["id"],
                "channel_name": channel["name"],
                "color": channel["color"],
                "role_needed": channel["role_needed"],
                } for channel in filter(lambda channel: is_user_owner or channel["role_needed"] in roles or channel["role_needed"] == None, channels)],
            "messages": messages,
            "is_muted": is_muted,
        })

    async def handle_status(self, msg: dict[str, str]):
        if msg["content"] == "Online" and self.user_id not in broadcast.connected_ids:
            broadcast.connected_ids[self.user_id] = None
            await self.websocket.send_json({
                "status": 200
            })
            return
        
        if msg["content"] == "Offline" and self.user_id in broadcast.connected_ids:
            broadcast.connected_ids.pop(self.user_id, None)
            await self.websocket.send_json({
                "status": 200
            })
            return
        
        await self.handle_error(400, "User status is already set to requested status or status is invalid")

    
    async def handle_dm(self, msg: dict[str, str]):
        if len(msg["content"]) > 1000:
            await self.handle_error(400, "Message content is too long")
            return
        
        if self.current_dm == None:
            await self.handle_error(400, "DM not yet selected")
            return
        
        dm_id = store_direct_message(self.user_id, self.current_dm, msg["content"], None)
        
        await broadcast.broadcast({
            "class": ["reciever", "author"],
            "type": "new_dm",
            "reciever_id": self.current_dm,
            "author_id": self.user_id,
            "date": str(datetime.datetime.now()),
            "content": msg["content"],
            "message_id": dm_id
        })

        await self.websocket.send_json({
            "status": 201,
            "message": "success"
        })

    
    async def handle_load_dms(self, msg: dict[str, str]):
        if not is_friends(self.user_id, msg["content"]):
            await self.handle_error(403, "User is not friend with target")
            return
        
        try:
            start_from = msg["start_from"]
        except KeyError:
            start_from = 0
        res = get_messsages_from_dm(50, self.user_id, msg["content"], start_from)
        
        self.current_dm = msg["content"]
        self.current_channel = None
        self.current_server = None
        self.is_muted = False

        await self.websocket.send_json({
            "status": 200,
            "type": "load_dms",
            "messages": res["messages"],
        })


class Broadcaster:
    connections: list[Socket]
    connected_ids: dict[int, None]

    def __init__(self):
        self.connections = []
        self.connected_ids = {}

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
    broadcast.connected_ids[int(user_id)] = None
    await websocket.send_json({
        "status": 200,
        "user_id": int(user_id)
    })
    
    try:
        while True:
            raw = await websocket.receive_text()
            msg: dict[str, str] = json.loads(raw)

            if msg["type"] == "":
                await socket.handle_error(400, "Message type missing")

            match msg["type"]:
                case "message":
                    await socket.handle_message(msg)
                
                case "channel":
                    await socket.handle_channel(msg)

                case "server":
                    await socket.handle_server(msg)

                case "status":
                    await socket.handle_status(msg)

                case "dm":
                    await socket.handle_dm(msg)
                
                case "load_dms":
                    await socket.handle_load_dms(msg)

                case _:
                    socket.handle_error(400, "Message type is invalid")
                
    except WebSocketDisconnect:
        broadcast.connections.remove(socket)
        broadcast.connected_ids.pop(int(user_id), None)
