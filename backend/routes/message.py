from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth_token import verify_token
from database.messages import delete_message

router = APIRouter()

class RemoveMessage(BaseModel):
    token: str
    message_id: int


@router.delete("/remove_message", status_code=202)
async def remove_message(data: RemoveMessage) -> str:
    # TODO implement with database
    raise HTTPException(status=501)