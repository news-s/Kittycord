from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth_token import verify_token
from database.servers import get_server_by_link, join_server, create_server, delete_server, get_owner_id, set_invite_link, change_server_name


router = APIRouter()


@router.put("/join/{link}", status_code=200)
async def join_server(link: str, token: str) -> int:
    user_id = verify_token(token)
    res = get_server_by_link(link)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Server not found")
    
    join_server(user_id, res["id"])

    return res["id"]



class AddServer(BaseModel):
    token: str
    server_name: str
    invite_link: str

class AddServerResponse(BaseModel):
    server_id: int

@router.post("/add_server", status_code=201)
async def add_server(data: AddServer) -> AddServerResponse:
    user_id = verify_token(data.token)

    res = create_server(int(user_id), data.server_name, data.invite_link)

    if res["status"] == "error":
        return HTTPException(status_code=409, detail="Server invite link must be unique")

    return AddServerResponse(server_id=res["server_id"])


class RemoveServer(BaseModel):
    token: str
    server_id: str

@router.delete("/remove_server", status_code=202)
async def remove_server(data: RemoveServer) -> str:
    user_id = verify_token(data.token)

    res = get_owner_id(data.server_id)
    
    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Server doesn't exist")

    if res["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="User is not owner")

    res = delete_server(data.server_id)
    
    return res["status"]


class EditServer(BaseModel):
    token: str
    server_id: int
    new_val: str

@router.put("/edit_server/name")
async def edit_server_name(data: EditServer):
    user_id = verify_token(data.token)

    res = get_owner_id(data.server_id)
    
    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Server doesn't exist")

    if res["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="User is not owner")
    
    res = change_server_name(data.server_id, data.new_val)

    if res["status"] == "error":
        return HTTPException(status_code=500, detail="Server initially found but failed to edit")
    
    return res["status"]

@router.put("/edit_server/link")
async def edit_server_link(data: EditServer):
    user_id = verify_token(data.token)

    res = get_owner_id(data.server_id)
    
    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Server doesn't exist")

    if res["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="User is not owner")

    res = set_invite_link(data.server_id, data.new_val)

    if res["status"] == "error":
        return HTTPException(status_code=500, detail="Server initially found but failed to edit")
    
    return res["status"]

