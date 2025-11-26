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

def create_role(server_id: int, role_name: str, perms_dict: dict):
    db_gen = models.get_db()
    db = next(db_gen)
    server = db.query(models.Server).filter_by(id=server_id).first()
    if server == None:
        return {'status': "error", 'message': "Server does not exist"}
    perms_int = int(permissions.convert_to_string(perms_dict))
    role = models.Role(server_id=server_id, role_name=role_name, permissions=perms_int)
    db.add(role)
    db.commit()
    return {'status': "success", 'role_id': role.id}

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