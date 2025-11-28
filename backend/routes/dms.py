from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth_token import verify_token
from database.dms import change_dm, delete_dm, get_author
from routes.ws import broadcast

router = APIRouter()


class RemoveDM(BaseModel):
    token: str
    dm_id: int

@router.patch("/remove_dm", status_code=200)
async def remove_dm(data: RemoveDM) -> str:
    user_id = verify_token(data.token)
    res = get_author(data.dm_id)
    reciever = res["reciever_id"]

    if res["status"] == "error":
        raise HTTPException(status_code=403, detail="DM doesn't exist")
    
    if res["author_id"] != user_id:
        raise HTTPException(status_code=403, detail="User is not DM author")
    
    res = delete_dm(data.dm_id)

    await broadcast.broadcast({
        "class": ["author", "reciever"],
        "type": "remove_dm",
        "reciever_id": reciever,
        "author_id": user_id,
        "dm_id": data.dm_id,
    })

    return res["status"]


class EditDM(BaseModel):
    token: str
    dm_id: int
    new_content: str

@router.put("/edit_dm", status_code=200)
async def edit_dm(data: EditDM) -> str:
    user_id = verify_token(data.token)
    res = get_author(data.dm_id)
    reciever = res["reciever_id"]

    if res["status"] == "error":
        raise HTTPException(status_code=403, detail="DM doesn't exist")
    
    if res["author_id"] != user_id:
        raise HTTPException(status_code=403, detail="User is not DM author")
    
    res = change_dm(data.dm_id, data.new_content)

    await broadcast.broadcast({
        "class": ["author", "reciever"],
        "type": "edit_dm",
        "reciever_id": reciever,
        "author_id": user_id,
        "dm_id": data.dm_id,
        "new_content": data.new_content
    })

    return res["status"]