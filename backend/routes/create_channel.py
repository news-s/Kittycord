from fastapi import APIRouter, HTTPException
from ..users import servers

from auth_token import create_access_token

router_ch = APIRouter()

@router_ch.post("/create_channel")
def create_channel(id_owner: int, id_server: int, channel_name: str):
    server = None
    for s in servers:
        if s.id == id_server:
            server = s
            break

    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")

    if server.owner != id_owner:
        raise HTTPException(status_code=403, detail="You are not the owner of this server")

    server.add_channel(channel_name)