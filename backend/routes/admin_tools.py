
import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth_token import verify_token
from database.servers import leave_server
from utils import has_permission, is_member
from routes.ws import broadcast
from database.admin_tool import ban_user, is_user_banned, is_user_muted, mute_user, unban_user, unmute_user

MUTE_PERM = "Mute members"
BAN_PERM = "Ban members"
KICK_PERM = "Kick members"

router = APIRouter()

# TODO Tests for all of these, websocket messages
class Mute(BaseModel):
    token: str
    user_id: int
    server_id: int
    muted_till: int


@router.post("/mute", status_code=200)
async def mute(data: Mute) -> str:
    user_id = verify_token(data.token)
    
    if not is_member(user_id, data.server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")

    if not is_member(data.user_id, data.server_id):
        raise HTTPException(status_code=400, detail=f"Target is not member of server")

    if not has_permission(user_id, data.server_id, MUTE_PERM):
        raise HTTPException(status_code=403, detail=f"User is missing {MUTE_PERM} permission")
    
    muted_till = datetime.datetime.fromtimestamp(data.muted_till)
    res = mute_user(data.user_id, data.server_id, muted_till)

    if res["status"] == "error":
        raise HTTPException(status_code=500, detail="Target initally loaded but failed to mute")
    
    await broadcast.broadcast({
        "class": ["user", "mute"],
        "type": "mute",
        "user_id": data.user_id,
        "server_id": data.server_id,
        "muted_till": data.muted_till,
    })
    
    return res["status"]

class Unmute(BaseModel):
    token: str
    user_id: int
    server_id: int

@router.post("/unmute", status_code=200)
async def unmute(data: Unmute) -> str:
    user_id = verify_token(data.token)

    if not is_member(user_id, data.server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")

    if not is_member(data.user_id, data.server_id):
        raise HTTPException(status_code=400, detail=f"Target is not member of server")

    if not has_permission(user_id, data.server_id, MUTE_PERM):
        raise HTTPException(status_code=403, detail=f"User is missing {MUTE_PERM} permission")
    
    res = unmute_user(data.user_id, data.server_id)

    if res["status"] == "error":
        raise HTTPException(status_code=500, detail="Target initally loaded but failed to unmute")
    
    await broadcast.broadcast({
        "class": ["user", "unmute"],
        "type": "unmute",
        "user_id": data.user_id,
        "server_id": data.server_id,
    })

    return res["status"]


class IsMutedResponse(BaseModel):
    is_muted: bool
    message: str

@router.get("/is_muted/{user_id}/{server_id}]", status_code=200)
async def is_muted(user_id: int, server_id: int) -> IsMutedResponse:
    res = is_user_muted(user_id, server_id)

    if res["status"] == "error":
        raise HTTPException(status_code=400, detail="User is not member of server")

    if res["muted"]:
        return IsMutedResponse(is_muted=res["muted"], message=res["message"] | "")
    
    return IsMutedResponse(is_muted=res["muted"], message="")


class Ban(BaseModel):
    token: str
    user_id: int
    server_id: int
    reason: str

@router.post("/ban", status_code=200)
async def ban(data: Ban) -> str:
    user_id = verify_token(data.token)

    if not is_member(user_id, data.server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")

    if not is_member(data.user_id, data.server_id):
        raise HTTPException(status_code=400, detail=f"Target is not member of server")

    if not has_permission(user_id, data.server_id, BAN_PERM):
        raise HTTPException(status_code=403, detail=f"User is missing {BAN_PERM} permission")

    res = ban_user(data.user_id, data.server_id, data.reason)

    if res["status"] == "error":
        raise HTTPException(status_code=500, detail="User and Server found but failed to ban")
    
    await broadcast.broadcast({
        "class": ["user", "reset_ids"],
        "type": "ban",
        "user_id": data.user_id,
        "reason": data.reason,
    })

    return res["status"]


class Unban(BaseModel):
    token: str
    user_id: int
    server_id: int

@router.post("/unban", status_code=200)
async def unban(data: Unban) -> str:
    user_id = verify_token(data.token)

    if not is_member(user_id, data.server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")

    if not is_member(data.user_id, data.server_id):
        raise HTTPException(status_code=400, detail=f"Target is not member of server")

    if not has_permission(user_id, data.server_id, BAN_PERM):
        raise HTTPException(status_code=403, detail=f"User is missing {BAN_PERM} permission")

    res = unban_user(data.user_id, data.server_id)

    if res["status"] == "error":
        raise HTTPException(status_code=500, detail="User and Server found but failed to unban")

    return res["status"]


@router.get("/is_banned/{user_id}/{server_id}", status_code=200)
async def is_banned(user_id: int, server_id: int) -> str:
    res = is_user_banned(user_id, server_id)

    if res["status"] == "error":
        raise HTTPException(status_code=400, detail="User is not member of server")

    if res["banned"]:
        return IsMutedResponse(is_muted=res["muted"], message=res["message"] | "")


class Kick(BaseModel):
    token: str
    user_id: int
    server_id: int

@router.post("/kick", status_code=200)
async def kick(data: Kick):
    user_id = verify_token(data.token)

    if not is_member(user_id, data.server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")

    if not is_member(data.user_id, data.server_id):
        raise HTTPException(status_code=400, detail=f"Target is not member of server")

    if not has_permission(user_id, data.server_id, KICK_PERM):
        raise HTTPException(status_code=403, detail=f"User is missing {KICK_PERM} permission")

    res = leave_server(data.user_id, data.server_id)

    if res["status"] == "error":
        raise HTTPException(status_code=500, detail="User and Server found but failed to kick")
    
    await broadcast.broadcast({
        "class": ["user", "reset_ids"],
        "type": "kick",
        "user_id": data.user_id,
    })
    
    return res["status"]