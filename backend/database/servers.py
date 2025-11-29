from sqlalchemy import insert, delete

from database.roles import get_highest_role, get_role_color
from database import models

def join_server(user_id: int, server_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    #Validating
    server = db.query(models.Server).filter_by(id=server_id).first()
    if server == None:
        return {'status': "error", 'message': "server doesnt exists"}
    rel_check = db.query(models.User_Server).filter_by(user_id=user_id, server_id=server_id).first()
    if rel_check != None:
        return {'status': "error", 'message': "user already in server"}
    banned = db.query(models.Ban).filter_by(user_id=user_id, server_id=server_id).first()
    if banned != None:
        return {'status': "error", 'message': "user is banned from server"}
    rel = models.User_Server(user_id=user_id, server_id=server_id, roles=[])
    db.add(rel)
    db.commit()
    return {'status': "success"}

def leave_server(user_id: int, server_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    rel = db.query(models.User_Server).filter_by(user_id=user_id, server_id=server_id).first()
    if rel == None:
        return {'status': "error", 'message': "user not in server"}
    db.delete(rel)
    db.commit()
    return {'status': "success"}

def create_server(owner_id: int, name: str, invite_link: str):
    db_gen = models.get_db()
    db = next(db_gen)
    usr = db.query(models.User).filter_by(id=owner_id).first()
    if usr == None:
        return {'status': "error", 'message': "owner doesnt exists"}
    try:    # try because of unique
        server = models.Server(name=name, owner_id=owner_id, invite_link=invite_link)
        db.add(server)
        db.commit()
    except Exception as e:
        return {"status": "error", "message": str(e)}
    # getting server id
    server_id = db.query(models.Server).filter_by(invite_link=invite_link).first().id
    # Join owner to server
    join_server(owner_id, server_id)
    return {"status": "success", "server_id": server_id}

def delete_server(server_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    # Removing users relationship with server
    db.query(models.User_Server).filter_by(server_id=server_id).delete()
    db.query(models.Channel).filter_by(server_id=server_id).delete()
    db.query(models.Server).filter_by(id=server_id).delete()
    db.commit()
    return {'status': "success"}

def get_owner_id(server_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    owner_id = db.query(models.Server).filter_by(id=server_id).first().owner_id
    if owner_id == None:
        return {'status': "error", 'message': "owner id missing"}
    return {'status': "success", 'owner_id': owner_id}

def get_server_by_link(invite_link: str):
    db_gen = models.get_db()
    db = next(db_gen)
    try:
        server_id = db.query(models.Server).filter_by(invite_link=invite_link).first().id
    except AttributeError:
        return {'status': "error", 'message': "Invalid invite link"}
    if server_id == None:
        return {'status': "error", 'message': "Invalid invite link"}
    return {'status': "success", 'id': server_id}

def set_invite_link(server_id: int, new_link: str):
    db_gen = models.get_db()
    db = next(db_gen)
    server = db.query(models.Server).filter_by(id=server_id).first()
    if server == None:
        return {'status': "error", 'message': "server doesnt exists"}
    server.invite_link = new_link
    db.commit()
    return {'status': "success"}

def change_server_name(server_id: int, new_name: str):
    db_gen = models.get_db()
    db = next(db_gen)
    server = db.query(models.Server).filter_by(id=server_id).first()
    if server == None:
        return {'status': "error", 'message': "server doesnt exists"}
    server.name = new_name
    db.commit()
    return {'status': "success"}

def get_users_in_server(server_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    rels = db.query(models.User_Server).filter_by(server_id=server_id).all()
    if rels == None:
        return {'status': "error", 'message': "server doesnt exists"}
    return {'status': "success", 'users':
            [{
                'name': db.query(models.User).filter_by(id=rel.user_id).first().display_name,
                'user_id': rel.user_id,
                'color': get_role_color(get_highest_role(rel.user_id, server_id)).get("color", [])
            } for rel in rels]
        }

def get_servers_of_user(user_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    rels = db.query(models.User_Server).filter_by(user_id=user_id).all()
    if rels == None:
        return {'status': "error", 'message': "user doesnt exists"}
    return {'status': "success", 'servers':
            [{
                'server_id': rel.server_id,
                'roles': rel.roles
            } for rel in rels]
        }

def get_server_name(server_id: int) -> dict:
    db_gen = models.get_db()
    db = next(db_gen)
    srv = db.query(models.Server).filter_by(id=server_id).first()
    if srv == None:
        return {'status': "error", 'message': "server doesnt exists"}
    return {'status': "success", 'name': srv.name, 'link': srv.invite_link}

if __name__ == "__main__":
    id = create_server(1, "test", "testlink")
    #join_server(1, 1)
    print(get_users_in_server(id['server_id']))
