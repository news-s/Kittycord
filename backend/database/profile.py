from database import models
from database.friends import get_friends
from sqlalchemy import update

def get_user_data(user_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    usr = db.query(models.User).filter_by(id=user_id).first()
    if usr == None:
        return {'status': "error", 'message': "Couldnt find user"}
    servers = db.query(models.User_Server.server_id).filter_by(user_id=user_id).all()
    friends = get_friends(user_id)["friends"]
    if friends is None:
        friends = []
    return {
        "status": "success",
        "name": usr.name,
        "display_name": usr.display_name,
        "note": usr.note,
        "badges": usr.badges,
        "creation_date": usr.account_creation_date,
        "servers": [server[0] for server in servers],
        "friends": friends,
        "avatar_id": usr.avatar_id
    }

def change_display_name(user_id: int, new_name: str):
    db_gen = models.get_db()
    db = next(db_gen)
    db.execute(update(models.User).where(models.User.id==user_id).values(display_name=new_name))
    db.commit()
    return {'status': "success"}

def change_name(user_id: int, new_name: str):
    db_gen = models.get_db()
    db = next(db_gen)
    is_free = db.query(models.User).filter_by(name=new_name).first()
    if is_free != None:
        return {'status': "error", 'message': "name already taken"}
    db.execute(update(models.User).where(models.User.id==user_id).values(name=new_name))
    db.commit()
    return {'status': "success"}

def change_note(user_id: int, new_note: str):
    db_gen = models.get_db()
    db = next(db_gen)
    db.execute(update(models.User).where(models.User.id==user_id).values(note=new_note))
    db.commit()
    return {'status': "success"}

def change_avatar(user_id: int, file_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    db.execute(update(models.User).where(models.User.id==user_id).values(avatar_id=file_id))
    db.commit()
    return {'status': "success"}

if __name__ == "__main__":
    get_user_data(1)
