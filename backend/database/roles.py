import models, permissions
from sqlalchemy import delete

def add_role_to_user(user_id: int, server_id: int, role_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    rel = db.query(models.User_Server).filter_by(user_id=user_id, server_id=server_id).first()
    if rel == None:
        return {'status': "error", 'message': "User is not in server"}
    if role_id in rel.roles:
        return {'status': "error", 'message': "User already has this role"}
    rel.roles.append(role_id)
    db.commit()
    return {'status': "success"}

def remove_role_from_user(user_id: int, server_id: int, role_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    rel = db.query(models.User_Server).filter_by(user_id=user_id, server_id=server_id).first()
    if rel == None:
        return {'status': "error", 'message': "User is not in server"}
    if role_id not in rel.roles:
        return {'status': "error", 'message': "User doesnt have this role"}
    rel.roles.remove(role_id)
    db.commit()
    return {'status': "success"}

def create_role(server_id: int, role_name: str, perms_dict: dict, color: str):
    db_gen = models.get_db()
    db = next(db_gen)
    server = db.query(models.Server).filter_by(id=server_id).first()
    if server == None:
        return {'status': "error", 'message': "Server does not exist"}
    perms_int = int(permissions.convert_to_string(perms_dict))
    role = models.Role(server_id=server_id, role_name=role_name, permissions=perms_int, color=color)
    db.add(role)
    db.commit()
    db.refresh(role)
    return {'status': "success", 'role_id': role.id, 'role_color': role.color}

def delete_role(role_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    role = delete(models.Role).where(models.Role.id == role_id)
    if role == None:
        return {'status': "error", 'message': "Role does not exist"}
    db.execute(role)
    db.commit()
    return {'status': "success"}

def set_role_permissions(role_id: int, perms_dict: dict):
    db_gen = models.get_db()
    db = next(db_gen)
    role = db.query(models.Role).filter_by(id=role_id).first()
    if role == None:
        return {'status': "error", 'message': "Role does not exist"}
    role.permissions = int(permissions.convert_to_string(perms_dict))
    db.commit()
    return {'status': "success"}

def change_role_color(role_id: int, new_color: str):
    db_gen = models.get_db()
    db = next(db_gen)
    role = db.query(models.Role).filter_by(id=role_id).first()
    if role == None:
        return {'status': "error", 'message': "Role does not exist"}
    role.color = new_color
    db.commit()
    return {'status': "success"}

def get_server_id_by_role(role_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    role = db.query(models.Role).filter_by(id=role_id).first()
    if role == None:
        return {'status': "error", 'message': "Role does not exist"}
    return {'status': "success", 'server_id': role.server_id}

def get_role_color(role_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    role = db.query(models.Role).filter_by(id=role_id).first()
    if role == None:
        return {'status': "error", 'message': "Role does not exist"}
    return {'status': "success", 'color': role.color}

def reorder_roles(server_id: int, new_order: list[int]):
    db_gen = models.get_db()
    db = next(db_gen)
    server = db.query(models.Server).filter_by(id=server_id).first()
    if server == None:
        return {'status': "error", 'message': "Server does not exist"}
    roles = db.query(models.Role).filter_by(server_id=server_id).all()
    role_ids = [role.id for role in roles]
    if set(new_order) != set(role_ids):
        return {'status': "error", 'message': "New order does not match existing roles"}
    server.roles = new_order
    db.commit()
    return {'status': "success"}

def get_roles_in_server(server_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    server = db.query(models.Server).filter_by(id=server_id).first()
    if server == None:
        return {'status': "error", 'message': "Server does not exist"}
    roles = db.query(models.Role).filter_by(server_id=server_id).all()
    return {'status': "success", 'roles':
            [{
                'id': r.id,
                'role_name': r.role_name,
                'permissions': permissions.convert_to_permissions(r.permissions),
                'color': r.color
            } for r in roles]
        }

if __name__ == "__main__":
    print(create_role(1, "Moderator", {
        "Mute members": True,
        "Kick members": True,
        "Ban members": False,
        "Manage channels": False,
        "Manage roles": False,
        "Manage server": False,
        "Admin": False
    }, "#00FF00"))
    create_role(1, "Admin", {
        "Mute members": True,
        "Kick members": True,
        "Ban members": True,
        "Manage channels": True,
        "Manage roles": True,
        "Manage server": True,
        "Admin": True
    }, "#FF0000")
    print(get_roles_in_server(1))
    reorder_roles(1, [2, 1])
    print(get_roles_in_server(1))
    add_role_to_user(1, 1, 1)
    print(permissions.get_user_permissions(1, 1))
    change_role_color(1, "#0000FF")
    print(get_role_color(1))
    print(get_server_id_by_role(1))
    remove_role_from_user(1, 1, 1)
    delete_role(1)
    delete_role(2)