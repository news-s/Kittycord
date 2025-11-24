from sqlalchemy import insert, delete

from database import models

def join_server(user_id: int, server_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    rel = models.User_Server(user_id=user_id, server_id=server_id, permission=[], role=[])
    db.add(rel)
    db.commit()
    return {'status': "success"}

def create_server(owner_id: int, name: str, invite_link: str):
    db_gen = models.get_db()
    db = next(db_gen)
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
    db.query(models.Server).filter_by(id=server_id).delete()
    db.commit()
    return {'status': "success"}

def get_owner_id(server_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    owner_id = db.query(models.Server).filter_by(id=server_id).first().owner_id
    return {'status': "success", 'owner_id': owner_id}

def get_server_by_link(invite_link: str):
    db_gen = models.get_db()
    db = next(db_gen)
    server_id = db.query(models.Server).filter_by(invite_link=invite_link).first().id
    if server_id == None:
        return {'status': "error", 'message': "Invalid invite link"}
    return {'status': "success", 'id': server_id}

if __name__ == "__main__":
    id = create_server(1, "test", "test1")
    print(id)
    get_owner_id(id["server_id"])
    get_server_by_link("test1")
    delete_server(id["server_id"])
