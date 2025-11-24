from database import models

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