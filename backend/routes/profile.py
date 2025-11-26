from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth_token import verify_token
from database.profile import get_user_data, change_name, change_display_name, change_note

router = APIRouter()

class ProfileResponse(BaseModel):
    name: str
    display_name: str
    note: str
    servers: list[int]


@router.get("/profile/{user_id}", status_code=200)
async def profile(user_id) -> ProfileResponse:
    user_data = get_user_data(user_id)

    if user_data["status"] == "error":
        raise HTTPException(status_code=404, detail="User not found")
    
    return ProfileResponse(name=user_data["name"], display_name=user_data["display_name"], note=user_data["note"], servers=user_data["servers"])


class EditProfile(BaseModel):
    token: str
    new_val: str

@router.put("/edit_profile/display_name", status_code=200)
async def edit_display_name(data: EditProfile) -> str:
    user_id = verify_token(data.token)

    res = change_display_name(user_id, data.new_val)

    return res["status"]


@router.put("/edit_profile/name", status_code=200)
async def edit_name(data: EditProfile) -> str:
    user_id = verify_token(data.token)

    res = change_name(user_id, data.new_val)

    return res["status"]

@router.put("/edit_profile/note", status_code=200)
async def edit_note(data: EditProfile) -> str:
    user_id = verify_token(data.token)

    res = change_note(user_id, data.new_val)
    
    return res["status"]