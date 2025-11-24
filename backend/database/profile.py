import models

def get_user_data(user_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    usr = db.query(models.User).filter_by(id=user_id).first()
    if usr == None:
        return {'status': "error", 'message': "Couldnt find user"}
    servers = db.query(models.User_Server.server_id).filter_by(user_id=user_id).all()
    #TODO ma zwracać też zanjomych
    return {
        "name": usr.name,
        "display_name": usr.display_name,
        "note": usr.note,
        "badges": usr.badges,
        "creation_date": usr.account_creation_date,
        "servers": [server for server in servers],
    }

def change_display_name(user_id: int, new_name: str):
    db_gen = models.get_db()
    db = next(db_gen)
    db.query(models.User).filter_by(id=user_id).first().update(display_name=new_name)
    db.commit()
    return {'status': "success"}

def change_name(user_id: int, new_name: str):
    db_gen = models.get_db()
    db = next(db_gen)
    is_free = db.query(models.User).filter_by(name=new_name).first()
    if is_free != None:
        return {'status': "error", 'message': "name already taken"}
    db.query(models.User).filter_by(id=user_id).first().update(name=new_name)
    db.commit()
    return {'status': "success"}

def change_note(user_id: int, new_note: str):
    db_gen = models.get_db()
    db = next(db_gen)
    db.query(models.User).filter_by(id=user_id).first().update(note=new_note)
    db.commit()
    return {'status': "success"}

if __name__ == "__main__":
    get_user_data(1)
