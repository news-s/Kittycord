from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database.servers import get_owner_id
from database.channels import create_channel

from auth_token import verify_token

router = APIRouter()

class AddChannel(BaseModel):
    token: str
    server_id: int
    channel_name: str

@router.post("/add_channel", status_code=201)
async def add_channel(data: AddChannel) -> str:
    user_id = verify_token(data.token)
    
    owner_id = get_owner_id(data.server_id)["owner_id"]

    if owner_id != user_id:
        raise HTTPException(status_code=403, detail="User is not the owner")

    res = create_channel(data.server_id, data.channel_name)

    return res["status"]



class RemoveChannel(BaseModel):
    token: str
    channel_id: int

@router.post("/remove_channel", status_code=202)
async def remove_channel(data: RemoveChannel) -> str:
    # TODO implement with database
    raise HTTPException(status=501)


    user_id = verify_token(token)

            
    raise HTTPException(status_code=404, detail="Channel not found")
