from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth_token import verify_token
from database.messages import delete_message, get_author, change_message

router = APIRouter()

class RemoveMessage(BaseModel):
    token: str
    message_id: int


@router.patch("/remove_message", status_code=200)
async def remove_message(data: RemoveMessage) -> str:
    user_id = verify_token(data.token)
    res = get_author(data.message_id)

    if res["status"] == "error":
        return HTTPException(status_code=404, detail="Message not found")
    
    if res["author_id"] != user_id:
        return HTTPException(status_code=403, detail="User is not author")

    res = delete_message(data.message_id)
    
    if res["status"] == "error":
        return HTTPException(status_code=500, detail="Message initially found but failed to delete")
    
    return res["status"]


class EditMessage(BaseModel):
    token: str
    message_id: int
    new_content: str

@router.put("/edit_message", status_code=200)
async def edit_message(data: EditMessage) -> str:
    user_id = verify_token(data.token)
    
    res = get_author(data.message_id)

    if res["status"] == "error":
        return HTTPException(status_code=404, detail="Message not found")
    
    if res["author_id"] != user_id:
        return HTTPException(status_code=403, detail="User is not author")

    res = change_message(data.message_id, data.new_content)

    if res["status"] == "error":
        return HTTPException(status_code=500, detail="Message initially found but failed to edit")
    
    return res["status"]
