from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth_token import verify_token
from database.profile import get_user_data, change_name, change_display_name, change_note
from database.permissions import get_user_permissions
from routes.ws import broadcast

router = APIRouter()

class ProfileResponse(BaseModel):
    user_id: int
    name: str
    display_name: str
    note: str
    servers: list[int]
    friends: list[str]
    status: str


@router.get("/profile/{user_id}", status_code=200)
async def profile(user_id: int) -> ProfileResponse:
    user_data = get_user_data(user_id)

    if user_data["status"] == "error":
        raise HTTPException(status_code=404, detail="User not found")

    print(broadcast.connected_ids)
    
    return ProfileResponse(
        user_id=user_id, name=user_data["name"], display_name=user_data["display_name"],
        note=user_data["note"], servers=user_data["servers"], friends=user_data["friends"],
        status="Online" if user_id in broadcast.connected_ids else "Offline"
    )


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


@router.get("/permissions/{user_id}/{server_id}", status_code=200)
async def get_permissions(user_id: int, server_id: int):
    res = get_user_permissions(user_id, server_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="User or server not found")
    
    return res["permissions"]
