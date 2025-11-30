from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from auth_token import verify_token
from utils import has_permission, is_member
from database.servers import get_server_by_link, get_server_name, get_users_in_server, join_server, leave_server, create_server, delete_server, get_owner_id, set_invite_link, change_server_name
from database.admin_tool import is_user_banned
from routes.ws import broadcast

SERVER_PERM = "Manage server"

router = APIRouter()

class JoinServer(BaseModel):
    token: str
    link: str

@router.put("/join", status_code=200)
async def join(data: JoinServer) -> str:
    user_id = verify_token(data.token)
    res = get_server_by_link(data.link)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Server not found")
    
    server_id = res["id"]
    
    res = is_user_banned(user_id, server_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="User doesn't exist")
    

    if res["banned"]:
        raise HTTPException(status_code=403, detail="User is banned")
    
    
    res = join_server(user_id, server_id)

    if res["status"] == "error":
        raise HTTPException(status_code=500, detail="Server initally found but failed to join")
    

    await broadcast.broadcast({
        "class": ["server"],
        "type": "leave_server",
        "user_id": user_id,
        "server_id": server_id,
    })

    return res["status"]

class LeaveServer(BaseModel):
    token: str
    server_id: int

@router.put("/leave", status_code=200)
async def leave(data: LeaveServer) -> str:
    user_id = verify_token(data.token)

    res = leave_server(user_id, data.server_id)

    if res["status"] == "error":
        raise HTTPException(status_code=400, detail="User is not member of server")
    
    await broadcast.broadcast({
        "class": ["server"],
        "type": "leave_server",
        "user_id": user_id,
        "server_id": data.server_id,
    })
    
    return res["status"]


class AddServer(BaseModel):
    token: str
    server_name: str
    invite_link: str

class AddServerResponse(BaseModel):
    server_id: int

@router.post("/add_server", status_code=201)
async def add_server(data: AddServer) -> AddServerResponse:
    if len(data.server_name) > 40:
        raise HTTPException(status_code=400, detail="Server name too long")
    
    if len(data.invite_link) > 20:
        raise HTTPException(status_code=400, detail="Server invite link too long")
    
    user_id = verify_token(data.token)

    res = create_server(int(user_id), data.server_name, data.invite_link)

    if res["status"] == "error":
        raise HTTPException(status_code=409, detail="Server invite link must be unique")

    return AddServerResponse(server_id=res["server_id"])


class RemoveServer(BaseModel):
    token: str
    server_id: int

@router.patch("/remove_server", status_code=200)
async def remove_server(data: RemoveServer) -> str:
    user_id = verify_token(data.token)

    res = get_owner_id(data.server_id)
    
    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Server doesn't exist")

    if res["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="User is not owner")

    res = delete_server(data.server_id)

    await broadcast.broadcast({
        "class": ["server", "reset_ids"],
        "type": "remove_server",
        "server_id": data.server_id
    })
    
    return res["status"]

@router.get("/get_members/{server_id}")
async def get_members(server_id: int):
    res = get_users_in_server(server_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Server not found")

    return res["users"]


@router.get("/server_name/{server_id}")
async def server_name(server_id):
    res = get_server_name(server_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Server not found")
    
    return {
        "server_name": res["name"],
        "server_link": res["link"],
    }


class EditServer(BaseModel):
    token: str
    server_id: int
    new_val: str

@router.put("/edit_server/name", status_code=200)
async def edit_server_name(data: EditServer) -> str:
    if len(data.new_val) > 40:
        raise HTTPException(status_code=400, detail="Server name too long")
    
    user_id = verify_token(data.token)

    if not is_member(user_id, data.server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")

    if not has_permission(user_id, data.server_id, SERVER_PERM):
        raise HTTPException(status_code=403, detail=f"User is missing {SERVER_PERM} permission")
    
    res = change_server_name(data.server_id, data.new_val)

    if res["status"] == "error":
        raise HTTPException(status_code=500, detail="Server initially found but failed to edit")

    if res["status"] == "error":
        return HTTPException(status_code=500, detail="Message changed but failed to broadcast")
    
    await broadcast.broadcast({
        "class": ["server"],
        "type": "edit_server_name",
        "server_id": data.server_id,
        "new_name": data.new_val,
    })
    
    return res["status"]

@router.put("/edit_server/link", status_code=200)
async def edit_server_link(data: EditServer) -> str:
    if len(data.new_val) > 20:
        raise HTTPException(status_code=400, detail="Server invite link too long")
    
    user_id = verify_token(data.token)

    if not is_member(user_id, data.server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")

    if not has_permission(user_id, data.server_id, SERVER_PERM):
        raise HTTPException(status_code=403, detail=f"User is missing {SERVER_PERM} permission")

    res = set_invite_link(data.server_id, data.new_val)

    if res["status"] == "error":
        raise HTTPException(status_code=409, detail="Server invite link is not unique")
    
    return res["status"]

