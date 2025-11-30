from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import typing
import json
import uvicorn

from auth_token import verify_token
from socket_manager import BroadCastMessage, Broadcaster, Socket
from routes.login import router as login_router
from users import servers, users, Message

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router)

broadcast = Broadcaster()
            
        

@app.websocket("/ws")
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
    await websocket.send_text(f"Hello {user_id}! You're connected.")
    try:
        while True:
            raw = await websocket.receive_text()
            msg: dict[str, typing.Any] = json.loads(raw)

            match msg["type"]:
                case "message":
                    message = BroadCastMessage(int(user_id), socket.current_channel, msg["content"])
                    await broadcast.broadcast(message)

                    # TODO database integration
                    for server in servers:
                        for channel in server.channels:
                            if channel.id == socket.current_channel:
                                channel.messages.append(Message(1, int(user_id), msg["content"]))
                
                case "channel":
                    socket.current_channel = int(msg["content"])



                    # TODO database integration

                    for server in servers:
                        for channel in server.channels:
                            if channel.id == socket.current_channel:
                                res = {
                                    "messages": channel.messages
                                }
                                await websocket.send_json(json.dumps(res, default=lambda o: o.__dict__))

                case "server":
                    # TODO database intergration


                    for server in servers:
                        if server.id == msg["content"]:
                            socket.current_channel = server.channels[0].id

                            res = {
                                "channels": [channel.name for channel in server.channels],
                                "messages": server.channels[0].messages,
                            }
                            await websocket.send_json(json.dumps(res, default=lambda o: o.__dict__))

                case _:
                    await websocket.send_text("skull")


            await websocket.send_text(f"{user_id} said: {msg}")
    except WebSocketDisconnect:
        print(f"User {user_id} disconnected.")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
