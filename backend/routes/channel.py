import typing
from fastapi import APIRouter, HTTPException
from users import servers

from auth_token import verify_token

router = APIRouter()

@router.post("/create_channel")
async def create_channel(token: str, id_server: int, channel_name: str):
    user_id = verify_token(token)

    # TODO database integration
    server = None
    for s in servers:
        if s.id == id_server:
            server = s
            break

    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")

    if server.id_owner != user_id:
        raise HTTPException(status_code=403, detail="User is not the owner")

    server.add_channel(channel_name)


@router.post("/remove_channel")
async def remove_channel(token: str, id: int):
    user_id = verify_token(token)

    # TODO database integration
    for server in servers:
        for channel in server.channels:
            if channel.id != id: continue
            if server.id_owner != user_id:
                raise HTTPException(status_code=403, detail="User is not the owner")

            server.channels.remove(channel)
            return
            
    raise HTTPException(status_code=404, detail="Channel not found")