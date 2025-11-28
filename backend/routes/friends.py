from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth_token import verify_token
from database.friends import accept_friend, get_friend_requests, invite_friend, reject_friend


router = APIRouter()


class FriendRequest(BaseModel):
    token: str
    user_id: int

@router.post("/send_friend_req", status_code=201)
async def send_friend_req(data: FriendRequest) -> int:
    user_id = verify_token(data.token)

    res = invite_friend(user_id, data.user_id)
    
    if res["status"] == "error":
        raise HTTPException(status_code=400, detail="Already friends or already sent request")

    return res["friend_request_id"]


@router.put("/accept_friend_req", status_code=200)
async def accept_friend_req(data: FriendRequest) -> str:
    user_id = verify_token(data.token)
    
    res = accept_friend(user_id, data.user_id)

    if res["status"] == "error":
        raise HTTPException(status_code=400, detail="No friend request found")

    return res["status"]

@router.patch("/reject_friend_req", status_code=200)
async def reject_friend_req(data: FriendRequest) -> str:
    user_id = verify_token(data.token)
    
    res = reject_friend(user_id, data.user_id)

    if res["status"] == "error":
        raise HTTPException(status_code=400, detail="No friend request found")

    return res["status"]


class GetFriendRequests(BaseModel):
    token: str

class GetFriendRequestsResponse(BaseModel):
    friend_requests: list[dict[str, int]]

@router.post("/get_friend_reqs", status_code=200)
async def get_friend_reqs(data: GetFriendRequests) -> GetFriendRequestsResponse:
    user_id = verify_token(data.token)

    return GetFriendRequestsResponse(friend_requests=get_friend_requests(user_id)["friend_requests"])
