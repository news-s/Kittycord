import models

# List below is inverted
permissions = ["Mute members", "Kick members", "Ban members", "Manage channels", "Manage roles", "Manage server", "Admin"]

def convert_to_permissions(n: int):
    result = {}
    for i, permission in enumerate(permissions):
        result[permission] = bool(n & (1 << i))
    return result

def convert_to_string(perms: dict):
    if perms.keys() != set(permissions):
        return {'status': "error", 'message': "Invalid permissions dictionary"}
    result = []
    for _, has_permission in perms.items():
        if has_permission:
            result.insert(0, "1")
        else:
            result.insert(0, "0")
    return "".join(result).encode("utf-8")

def get_user_permissions(user_id: int, server_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    user_server = db.query(models.User_Server).filter_by(user_id=user_id, server_id=server_id).first()
    if user_server == None:
        return {'status': "error", 'message': "Invalid data"}
    roles = user_server.roles
    combined_permissions = 0
    for role_id in roles:
        role = db.query(models.Roles).filter_by(id=role_id).first()
        if role:
            combined_permissions |= role.permissions
    return {'status': "success", 'permissions': convert_to_permissions(combined_permissions)}