import typing
from fastapi import APIRouter, HTTPException
from ..users import servers, Server

from auth_token import verify_token

router = APIRouter()

@router.post("/create_server")
async def create_channel(token: str, server_name: str):
    user_id = verify_token(token)

    # TODO database integration

    servers.append(
        Server(servers[len(servers) - 1].id+1, server_name, [], [user_id], user_id)
    )


@router.post("/remove_server")
async def remove_channel(token: dict[str, typing.Any], id: int):
    # TODO database intergration

    user_id = verify_token(token)

    for server in servers:
        if server.id == id:
            if server.id_owner != user_id:
                raise HTTPException(status_code=403, detail="User is not the owner")
            
            servers.remove(server)
            return
            
    raise HTTPException(status_code=404, detail="Server not found")