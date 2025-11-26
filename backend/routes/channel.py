from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database.servers import get_owner_id
from database.channels import create_channel, get_server_id, delete_channel, change_channel_name

from auth_token import verify_token

router = APIRouter()

class AddChannel(BaseModel):
    token: str
    server_id: int
    channel_name: str

@router.post("/add_channel", status_code=201)
async def add_channel(data: AddChannel) -> int:
    user_id = verify_token(data.token)
    
    owner_id = get_owner_id(data.server_id)["owner_id"]

    if owner_id != user_id:
        raise HTTPException(status_code=403, detail="User is not the owner")

    res = create_channel(data.server_id, data.channel_name)

    return res["channel_id"]



class RemoveChannel(BaseModel):
    token: str
    channel_id: int

@router.patch("/remove_channel", status_code=200)
async def remove_channel(data: RemoveChannel) -> str:
    user_id = verify_token(data.token)
    res = get_server_id(data.channel_id)

    if res["status"] == "error":
        return HTTPException(status_code=404, detail="Channel not found")
    
    res = get_owner_id(res["server_id"])

    if res["status"] == "error":
        return HTTPException(status_code=500, detail="Owner ID is None")
    
    if res["owner_id"] != user_id:
        return HTTPException(status_code=403, detail="User is not owner")
    
    res = delete_channel(data.channel_id)

    return res["status"]


class EditChannel(BaseModel):
    token: str
    channel_id: int
    channel_name: str

@router.put("/edit_channel/name", status_code=200)
async def edit_channel(data: EditChannel) -> str:
    user_id = verify_token(data.token)
    res = get_server_id(data.channel_id)

    if res["status"] == "error":
        return HTTPException(status_code=404, detail="Channel not found")
    
    res = get_owner_id(res["server_id"])

    if res["status"] == "error":
        return HTTPException(status_code=500, detail="Owner ID is None")
    
    if res["owner_id"] != user_id:
        return HTTPException(status_code=403, detail="User is not owner")
    
    res = change_channel_name(data.channel_id, data.channel_name)

    return res["status"]
