from curses import use_env
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from auth_token import verify_token
from utils import has_permission, is_member
from database.permissions import convert_to_permissions
from database.roles import add_role_to_user, change_role_name, create_role, delete_role, get_server_id_by_role, reorder_roles, set_role_permissions, change_role_color, remove_role_from_user
from database.servers import get_owner_id
from database.permissions import permissions

ROLES_PERM = "Manage roles"

router = APIRouter()


class AddRole(BaseModel):
    token: str
    server_id: int
    role_name: str
    role_color: str


@router.post("/add_role", status_code=201)
def add_role(data: AddRole) -> int:
    if data.role_color[0] != "#" or len(data.role_color) > 7:
        raise HTTPException(status_code=400, detail="Role color invalid")

    user_id = verify_token(data.token)

    if not is_member(user_id, data.server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")

    if not has_permission(user_id, data.server_id, ROLES_PERM):
        print("test")
        raise HTTPException(status_code=403, detail=f"User is missing {ROLES_PERM} permission")

    res = create_role(data.server_id, data.role_name, convert_to_permissions("0000000"), data.role_color)

    if res["status"] == "error":
        raise HTTPException(status_code=500, detail="Server found but role failed to add")

    return res["role_id"]

class AddRoleToUser(BaseModel):
    token: str
    role_id: int
    user_id: int

@router.put("/add_role", status_code=200)
def add_role_to(data: AddRoleToUser) -> str:
    user_id = verify_token(data.token)

    res = get_server_id_by_role(data.role_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Role doesn't exist")
    
    server_id = res["server_id"]
    
    if not is_member(user_id, server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")

    if not has_permission(user_id, server_id, ROLES_PERM):
        raise HTTPException(status_code=403, detail=f"User is missing {ROLES_PERM} permission")

    res = add_role_to_user(data.user_id, server_id, data.role_id)

    if res["status"] == "error":
        raise HTTPException(status_code=400, detail=res["message"])

    return res["status"]


class RemoveRole(BaseModel):
    token: str
    role_id: int

@router.patch("/remove_role", status_code=200)
def remove_role(data: RemoveRole) -> str:
    user_id = verify_token(data.token)
    res = get_server_id_by_role(data.role_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Role doesn't exist")
    
    server_id = res["server_id"]
    
    if not is_member(user_id, server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")
    
    if not has_permission(user_id, res["server_id"], ROLES_PERM):
        raise HTTPException(status_code=403, detail=f"User is missing {ROLES_PERM} permission")

    res = delete_role(data.role_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Role not found")

    return res["status"]


class RemoveRoleFromUser(BaseModel):
    token: str
    role_id: int
    user_id: int

@router.put("/remove_role", status_code=200)
def remove_role_from(data: RemoveRoleFromUser) -> str:
    user_id = verify_token(data.token)

    res = get_server_id_by_role(data.role_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Role doesn't exist")
    
    server_id = res["server_id"]
    
    if not is_member(user_id, server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")
    
    if not has_permission(user_id, server_id, ROLES_PERM):
        raise HTTPException(status_code=403, detail=f"User is missing {ROLES_PERM} permission")

    res = remove_role_from_user(user_id, server_id, data.role_id)

    if res["status"] == "error":
        raise HTTPException(status_code=400, detail=res["message"])

    return res["status"]
    

class EditRole(BaseModel):
    token: str
    role_id: int
    new_val: str

@router.put("/edit_role/name", status_code=200)
def edit_name(data: EditRole) -> str:
    user_id = verify_token(data.token)
    
    res = get_server_id_by_role(data.role_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Role doesn't exist")
    
    if not is_member(user_id, res["server_id"]):
        raise HTTPException(status_code=400, detail=f"User is not member of server")

    if not has_permission(user_id, res["server_id"], ROLES_PERM):
        raise HTTPException(status_code=403, detail=f"User is missing {ROLES_PERM} permission")

    res = change_role_name(data.role_id, data.new_val)

    if res["status"] == "error":
        raise HTTPException(status_code=500, detail="Role initially found but failed to change name")

    return res["status"]


@router.put("/edit_role/color", status_code=200)
def edit_color(data: EditRole) -> str:
    if data.new_val[0] != "#" or len(data.new_val) > 7:
        raise HTTPException(status_code=400, detail="Role color invalid")
    
    user_id = verify_token(data.token)
    
    res = get_server_id_by_role(data.role_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Role doesn't exist")
    
    if not is_member(user_id, res["server_id"]):
        raise HTTPException(status_code=400, detail=f"User is not member of server")

    if not has_permission(user_id, res["server_id"], ROLES_PERM):
        raise HTTPException(status_code=403, detail=f"User is missing {ROLES_PERM} permission")

    res = change_role_color(data.role_id, data.new_val)

    if res["status"] == "error":
        raise HTTPException(status_code=500, detail="Role initially found but failed to change color")

    return res["status"]

class EditRolePermissions(BaseModel):
    token: str
    role_id: int
    new_permissions: dict[str, bool]

@router.put("/edit_role/permissions", status_code=200)
def edit_permissions(data: EditRolePermissions) -> str:
    if list(data.new_permissions.keys()) != permissions:
        raise HTTPException(status_code=400, detail="Permission dict invalid")

    user_id = verify_token(data.token)
    
    res = get_server_id_by_role(data.role_id)

    if res["status"] == "error":
        raise HTTPException(status_code=404, detail="Role doesn't exist")

    if not has_permission(user_id, res["server_id"], ROLES_PERM):
        raise HTTPException(status_code=403, detail=f"User is missing {ROLES_PERM} permission")
    
    if data.new_permissions["Admin"] and not has_permission(user_id, res["server_id"], "Admin"):
        raise HTTPException(status_code=403, detail=f"User is missing Admin permission")

    res = set_role_permissions(data.role_id, data.new_permissions)

    if res["status"] == "error":
        raise HTTPException(status_code=500, detail="Role initially found but failed to set permissions")

    return res["status"]


class EditRoleOrder(BaseModel):
    token: str
    server_id: int
    new_order: list[int]

@router.put("/edit_server/role_order", status_code=200)
async def edit_role_oder(data: EditRoleOrder) -> str:
    user_id = verify_token(data.token)
    
    if not is_member(user_id, data.server_id):
        raise HTTPException(status_code=400, detail=f"User is not member of server")

    if not has_permission(user_id, data.server_id, ROLES_PERM):
        raise HTTPException(status_code=403, detail=f"User is missing {ROLES_PERM} permission")

    res = reorder_roles(data.server_id, data.new_order)

    if res["error"] == "error":
        raise HTTPException(status_code=400, detail="New order does not match existing roles")
    
    return res["status"]
    