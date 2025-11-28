from database import models

permissions = ["Mute members", "Kick members", "Ban members", "Manage channels", "Manage roles", "Manage server", "Admin"]

def convert_to_permissions(n: str):
    result = {}
    for i, permission in enumerate(permissions[::-1]):
        result[permission] = bool(int(n[i]))
    return result

def convert_to_string(perms: dict):
    if perms.keys() != set(permissions):
        return {'status': "error", 'message': "Invalid permissions dictionary"}
    result = []
    for _, has_permission in perms.items():
        if has_permission:
            result.append("1")
        else:
            result.append("0")
        
    return "".join(result)

def get_user_permissions(user_id: int, server_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    user_server = db.query(models.User_Server).filter_by(user_id=user_id, server_id=server_id).first()
    if user_server == None:
        return {'status': "error", 'message': "Invalid data"}
    roles = user_server.roles
    combined_permissions = ['0' for _ in permissions]
    for role_id in roles:
        role = db.query(models.Role).filter_by(id=role_id).first()
        if role:
            for i, char in enumerate(role.permissions):
                combined_permissions[i] = '1' if char == '1' else '0'
    return {'status': "success", 'permissions': convert_to_permissions("".join(combined_permissions))}