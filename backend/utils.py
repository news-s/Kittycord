from fastapi import HTTPException
from database.roles import get_role_order, get_user_roles_in_server
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



def get_highest_role(user_id: int, server_id: int) -> int | None:
    user_roles = get_user_roles_in_server(user_id, server_id)
    if user_roles["status"] == "error":
        return None
    
    user_role_ids = set(user_roles["roles"])
    
    order = get_role_order(server_id)
    if order["status"] == "error":
        return None

    for role_id in order["role_order"]:
        if role_id in user_role_ids:
            return role_id

    return None

def can_manage_role(user_id: int, server_id: int, target_role_id: int) -> bool:
    if get_owner_id(server_id)["owner_id"] == user_id:
        return True
    
    highest = get_highest_role(user_id, server_id)
    if highest is None:
        return False

    order = get_role_order(server_id)["role_order"]

    print(order)
    print(highest)
    try:
        user_pos = order.index(highest)
        target_pos = order.index(target_role_id)
    except ValueError:
        return False

    return user_pos < target_pos

def can_manage_user(user_id: int, other_user_id: int, server_id: int) -> bool:
    if get_owner_id(server_id)["owner_id"] == user_id:
        return True
    
    my_highest = get_highest_role(user_id, server_id)
    their_highest = get_highest_role(other_user_id, server_id)

    if my_highest is None or their_highest is None:
        return False
    
    order = get_role_order(server_id)["role_order"]
    return order.index(my_highest) < order.index(their_highest)
