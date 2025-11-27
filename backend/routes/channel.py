from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from utils import has_permission, is_member
from database.profile import get_user_data
from database.channels import create_channel, get_server_id, delete_channel, change_channel_name

from auth_token import verify_token
from routes.ws import broadcast

CHANNEL_PERM = "Manage channels"

router = APIRouter()

class AddChannel(BaseModel):
    token: str
    server_id: int
    channel_name: str

@router.post("/add_channel", status_code=201)
async def add_channel(data: AddChannel) -> int:
    user_id = verify_token(data.token)
    
    if not is_member(user_id, data.server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")
    
    if not has_permission(user_id, data.server_id, CHANNEL_PERM):
        raise HTTPException(status_code=403, detail=f"User is missing {CHANNEL_PERM} permission")

    res = create_channel(data.server_id, data.channel_name)

    if res["status"] == "error":
        raise HTTPException(status_code=500, detail="Failed to create channel")

    await broadcast.broadcast({
        "class": ["server"],
        "type": "add_channel",
        "server_id": data.server_id,
        "channel_id": res["channel_id"],
        "channel_name": data.channel_name,
    })

    return res["channel_id"]



class RemoveChannel(BaseModel):
    token: str
    channel_id: int

@router.patch("/remove_channel", status_code=200)
async def remove_channel(data: RemoveChannel) -> str:
    user_id = verify_token(data.token)
    res = get_server_id(data.channel_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Channel not found")
    
    server_id = res["server_id"]
    
    if not is_member(user_id, server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")
    
    if not has_permission(user_id, res["server_id"], CHANNEL_PERM):
        raise HTTPException(status_code=403, detail=f"User is missing {CHANNEL_PERM} permission")
    
    res = delete_channel(data.channel_id)

    await broadcast.broadcast({
        "class": ["server", "reset_ids"],
        "type": "remove_channel",
        "channel_id": data.channel_id,
        "server_id": server_id,
    })

    return res["status"]


class EditChannel(BaseModel):
    token: str
    channel_id: int
    new_name: str

@router.put("/edit_channel/name", status_code=200)
async def edit_channel(data: EditChannel) -> str:
    user_id = verify_token(data.token)
    res = get_server_id(data.channel_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Channel not found")
    
    server_id = res["server_id"]
    
    if not is_member(user_id, server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")
    
    if not has_permission(user_id, server_id, CHANNEL_PERM):
        raise HTTPException(status_code=403, detail=f"User does not have the {CHANNEL_PERM} permission")
    
    res = change_channel_name(data.channel_id, data.new_name)

    if res["status"] == "error":
        raise HTTPException(status_code=500, detail="Channel initally found but failed to rename")
    
    await broadcast.broadcast({
        "class": ["channel"],
        "type": "edit_channel_name",
        "channel_id": data.channel_id,
        "server_id": server_id,
        "new_content": data.new_name,
    })

    return res["status"]
