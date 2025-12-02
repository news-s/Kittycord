from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth_token import verify_token
# from utils import has_permission
from database.messages import delete_message, get_author, change_message, channel_id_by_message_id, get_channel_from_mesage
from routes.ws import broadcast

# MESSAGE_PERM = "Manage channels"

router = APIRouter()

class RemoveMessage(BaseModel):
    token: str
    message_id: int


@router.patch("/remove_message", status_code=200)
async def remove_message(data: RemoveMessage) -> str:
    user_id = verify_token(data.token)
    res = get_author(data.message_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Message not found")
    
    if res["author_id"] != user_id:
        # if not has_permission(user_id, data.server_id, MESSAGE_PERM):
        raise HTTPException(status_code=403, detail=f"User is not author")
        
    channel_id = get_channel_from_mesage(data.message_id)["message_id"]

    res = delete_message(data.message_id)
    
    if res["status"] == "error":
        raise HTTPException(status_code=500, detail="Message initially found but failed to delete")
    
    await broadcast.broadcast({
        "class": ["channel"],
        "type": "remove_message",
        "channel_id": channel_id,
        "message_id": data.message_id,
    })
    
    return res["status"]


class EditMessage(BaseModel):
    token: str
    message_id: int
    new_content: str

@router.put("/edit_message", status_code=200)
async def edit_message(data: EditMessage) -> str:
    if len(data.new_content) > 100:
        raise HTTPException(status_code=400, detail="New message too long")

    user_id = verify_token(data.token)
    
    res = get_author(data.message_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Message not found")
    
    if res["author_id"] != user_id:
        raise HTTPException(status_code=403, detail="User is not author")

    res = change_message(data.message_id, data.new_content)

    if res["status"] == "error":
        raise HTTPException(status_code=500, detail="Message initially found but failed to edit")
    
    res = channel_id_by_message_id(data.message_id)

    if res["status"] == "error":
        return HTTPException(status_code=500, detail="Message changed but failed to broadcast")
    
    await broadcast.broadcast({
        "class": ["channel"],
        "type": "edit_message",
        "channel_id": res["channel_id"],
        "message_id": data.message_id,
        "new_content": data.new_content,
    })
    
    return res["status"]
