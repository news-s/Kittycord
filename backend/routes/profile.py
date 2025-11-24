from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database.profile import get_user_data

router = APIRouter()

class Profile(BaseModel):
    user_id: int

class ProfileResponse(BaseModel):
    name: str
    display_name: str
    note: str
    servers: list[int]


@router.get("/profile", status_code=200)
async def profile(data: Profile) -> ProfileResponse:
    user_data = get_user_data(data.user_id)

    if user_data["status"] == "error":
        raise HTTPException(status_code=404, detail="User not found")
    
    return ProfileResponse(name=user_data["name"], display_name=user_data["display_name"], note=data["note"], servers=data["servers"])
