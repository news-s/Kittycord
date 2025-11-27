from fastapi import HTTPException
from database.profile import get_user_data
from database.permissions import get_user_permissions
from database.servers import get_owner_id


def has_permission(user_id: int, server_id: int, permission: str) -> bool:
    res = get_owner_id(server_id)
    
    if res["status"] == "error" or res["owner_id"] != user_id:
        res = get_user_permissions(user_id, server_id)
        
        if res["status"] == "error":
            raise HTTPException(status_code=500, detail="User doesn't exist")
        
        return res["permissions"]["Admin"] or res["permissions"][permission]
        
    return res["owner_id"] == user_id


def is_member(user_id: int, server_id: int):
    res = get_user_data(user_id)
    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="User not found")

    return server_id in res["servers"]