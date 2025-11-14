from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth_token import create_access_token

from users import users


router = APIRouter()

class LoginData(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(data: LoginData):
    # TODO: Database integration

    found = False
    userdata = users[0]
    for user in users:
        if user.name == data.username and user.password == data.password:
            userdata = user
            found = True
            break

    if not found:
        raise HTTPException(status_code=401, detail="Bad credentials")

    token = create_access_token({"id": userdata.id})
    return {"access_token": token}
