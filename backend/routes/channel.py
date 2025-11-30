from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from utils import has_permission, is_member
from database.profile import get_user_data
from database.channels import change_channel_color, change_channel_role_needed, create_channel, get_server_id, delete_channel, change_channel_name

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
    if len(data.channel_name) > 40:
        raise HTTPException(status_code=400, detail="Channel name too long")

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
    new_val: str

@router.put("/edit_channel/name", status_code=200)
async def edit_name(data: EditChannel) -> str:
    if len(data.new_val) > 40:
        raise HTTPException(status_code=400, detail="Channel name too long")
    
    user_id = verify_token(data.token)
    res = get_server_id(data.channel_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Channel not found")
    
    server_id = res["server_id"]
    
    if not is_member(user_id, server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")
    
    if not has_permission(user_id, server_id, CHANNEL_PERM):
        raise HTTPException(status_code=403, detail=f"User does not have the {CHANNEL_PERM} permission")
    
    res = change_channel_name(data.channel_id, data.new_val)

    if res["status"] == "error":
        raise HTTPException(status_code=500, detail="Channel initally found but failed to rename")
    
    await broadcast.broadcast({
        "class": ["server"],
        "type": "edit_channel_name",
        "channel_id": data.channel_id,
        "server_id": server_id,
        "new_content": data.new_val,
    })

    return res["status"]

@router.put("/edit_channel/color", status_code=200)
async def edit_color(data: EditChannel) -> str:
    if data.new_val[0] != '#' or len(data.new_val) > 7:
        raise HTTPException(status_code=400, detail="Channel color invalid")

    user_id = verify_token(data.token)
    res = get_server_id(data.channel_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Channel not found")
    
    server_id = res["server_id"]
    
    if not is_member(user_id, server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")
    
    if not has_permission(user_id, server_id, CHANNEL_PERM):
        raise HTTPException(status_code=403, detail=f"User does not have the {CHANNEL_PERM} permission")
    
    res = change_channel_color(data.channel_id, data.new_val)

    if res["status"] == "error":
        raise HTTPException(status_code=500, detail="Channel initally found but failed to rename")
    
    await broadcast.broadcast({
        "class": ["server"],
        "type": "edit_channel_color",
        "channel_id": data.channel_id,
        "server_id": server_id,
        "new_content": data.new_val,
    })

    return res["status"]


@router.put("/edit_channel/role_needed", status_code=200)
async def edit_color(data: EditChannel) -> str:

    user_id = verify_token(data.token)
    res = get_server_id(data.channel_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Channel not found")
    
    server_id = res["server_id"]
    
    if not is_member(user_id, server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")
    
    if not has_permission(user_id, server_id, CHANNEL_PERM):
        raise HTTPException(status_code=403, detail=f"User does not have the {CHANNEL_PERM} permission")

    if data.new_val == "None":
        res = change_channel_role_needed(data.channel_id, None)
    else:
        res = change_channel_role_needed(data.channel_id, data.new_val)

    if res["status"] == "error":
        raise HTTPException(status_code=400, detail="Role doesn't exist")
    
    await broadcast.broadcast({
        "class": ["server"],
        "type": "edit_channel_role_needed",
        "channel_id": data.channel_id,
        "server_id": server_id,
        "role_needed": data.new_val,
    })

    return res["status"]