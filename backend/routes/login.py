from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth_token import create_access_token, verify_token
from database.login import verify_user, create_user, delete_user


router = APIRouter()

class Login(BaseModel):
    username: str
    hashed_password: str

class LoginResponse(BaseModel):
    token: str


@router.post("/login", status_code=200)
async def login(data: Login) -> LoginResponse:
    user = verify_user(data.username, data.hashed_password)
    if user is None or user == 0:
        raise HTTPException(status_code=401, detail="Bad credentials")

    token = create_access_token({"id": user})
    return LoginResponse(token=token)


class AddUser(BaseModel):
    name: str
    hashed_password: str


@router.post("/add_user", status_code=201)
async def add_user(data: AddUser) -> str:
    res = create_user(data.name, data.hashed_password)

    if res["status"] == "error":
        raise HTTPException(status_code=409, detail="Username already taken")
    
    return res["status"]


class RemoveUser(BaseModel):
    token: str
    username: str
    hashed_password: str

@router.post("/remove_user", status_code=202)
async def remove_user(data: RemoveUser) -> str:
    user_id = verify_token(data.token)

    if verify_user(data.username, data.hashed_password) != user_id:
        raise HTTPException(status_code=403, detail="Bad Credentials")
    
    res = delete_user(user_id)

    if res["status"] == "error":
        raise HTTPException(status_code=501, detail="User found but not deleted")
    
    return res["status"]
