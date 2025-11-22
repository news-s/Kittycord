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

if __name__ == "__main__":
    get_user_data(1)
