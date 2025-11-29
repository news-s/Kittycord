from database import models, permissions
from sqlalchemy import delete, update

def add_role_to_user(user_id: int, server_id: int, role_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    rel = db.query(models.User_Server).filter_by(user_id=user_id, server_id=server_id).first()
    if rel == None:
        return {'status': "error", 'message': "User is not in server"}
    if role_id in rel.roles:
        return {'status': "error", 'message': "User already has this role"}
    rel.roles.append(role_id)
    db.execute(update(models.User_Server).where(models.User_Server.user_id==user_id, models.User_Server.server_id==server_id).values(roles=rel.roles))
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
    db.execute(update(models.User_Server).where(models.User_Server.user_id==user_id, models.User_Server.server_id==server_id).values(roles=rel.roles))
    db.commit()
    return {'status': "success"}

def create_role(server_id: int, role_name: str, perms_dict: dict, color: str):
    db_gen = models.get_db()
    db = next(db_gen)
    server = db.query(models.Server).filter_by(id=server_id).first()
    if server == None:
        return {'status': "error", 'message': "Server does not exist"}
    perms_str = permissions.convert_to_string(perms_dict)
    role = models.Role(server_id=server_id, role_name=role_name, permissions=perms_str, color=color)
    db.add(role)
    db.commit()
    db.refresh(role)
    if server.role_order is None:
        server.role_order = []
    server.role_order.append(role.id)
    db.execute(update(models.Server).where(models.Server.id==server_id).values(role_order=server.role_order))
    db.commit()
    return {'status': "success", 'role_id': role.id, 'role_color': role.color}

def delete_role(role_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    role = db.query(models.Role).filter_by(id=role_id).first()
    if role is None:
        return {'status': "error", 'message': "Role does not exist"}
    server = db.query(models.Server).filter_by(id=role.server_id).first()
    if server and server.role_order:
        server.role_order = [r for r in server.role_order if r != role_id]
    db.delete(role)
    db.commit()
    return {'status': "success"}

def set_role_permissions(role_id: int, perms_dict: dict):
    db_gen = models.get_db()
    db = next(db_gen)
    role = db.query(models.Role).filter_by(id=role_id).first()
    if role == None:
        return {'status': "error", 'message': "Role does not exist"}
    role.permissions = permissions.convert_to_string(perms_dict)
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
    server.role_order = new_order
    db.commit()
    return {'status': "success"}

def get_role_order(server_id):
    db_gen = models.get_db()
    db = next(db_gen)
    role_order = db.query(models.Server).filter_by(id=server_id).first().role_order
    if role_order == None:
        return {'status': "error", 'message': "Server does not exist"}
    return {'status': "success", 'role_order': role_order}

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

def get_user_roles_in_server(user_id: int, server_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    rel = db.query(models.User_Server).filter_by(user_id=user_id, server_id=server_id).first()
    if rel == None:
        return {'status': "error", 'message': "User is not in server"}
    return {'status': "success", 'roles': rel.roles}

def change_role_name(role_id: int, new_name: str):
    db_gen = models.get_db()
    db = next(db_gen)
    role = db.query(models.Role).filter_by(id=role_id).first()
    if role == None:
        return {'status': "error", 'message': "Role does not exist"}
    role.role_name = new_name
    db.commit()
    return {'status': "success"}

def get_role_by_id(role_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    role = db.query(models.Role).filter_by(id=role_id).first()
    if role == None:
        return {'status': "error", 'message': "Role does not exist"}
    return {'status': "success", 'role': {
        'id': role.id,
        'role_name': role.role_name,
        'permissions': permissions.convert_to_permissions(role.permissions),
        'color': role.color
    }}


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

if __name__ == "__main__":
    server_id = 1
    print(create_role(server_id, "Moderator", {
        "Mute members": True,
        "Kick members": True,
        "Ban members": False,
        "Manage channels": False,
        "Manage roles": False,
        "Manage server": False,
        "Admin": False
    }, "#00FF00"))
    create_role(server_id, "Admin", {
        "Mute members": True,
        "Kick members": True,
        "Ban members": True,
        "Manage channels": True,
        "Manage roles": True,
        "Manage server": True,
        "Admin": True
    }, "#FF0000")
    print(get_roles_in_server(server_id))
    reorder_roles(server_id, [2, 1])
    print(get_roles_in_server(server_id))
    add_role_to_user(1, server_id, 1)
    get_user_roles_in_server(1, server_id)
    print(get_user_roles_in_server(1, server_id))
    print(permissions.get_user_permissions(1, server_id))
    change_role_color(1, "#0000FF")
    change_role_name(1, "Super Moderator")
    print(get_role_color(1))
    print(get_server_id_by_role(1))
    remove_role_from_user(1, server_id, 1)
    delete_role(1)
    delete_role(2)
