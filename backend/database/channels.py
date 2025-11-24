from database import models

def create_channel(server_id, name, role_needed = None):
    db_gen = models.get_db()
    db = next(db_gen)
    if role_needed == None:
        channel = models.Channel(server_id=server_id, name=name)
        db.add(channel)
    else:
        roles = db.query(models.Server).filter_by(server_id=server_id).first().roles
        if role_needed not in roles:
            return {'status': "error", 'message': "role_needed doesnt exists"}
        channel = models.Channel(server_id=server_id, name=name, role_needed=role_needed)
        db.add(channel)
    db.commit()
    return {'status': "success"}

def delete_channel(channel_id):
    db_gen = models.get_db()
    db = next(db_gen)
    # Deleting all messages with channel id
    db.query(models.Messages).filter_by(channel_id=channel_id).all().delete()
    db.query(models.Channel).filter_by(id=channel_id).first().delete()
    db.commit()
    return {'status': "success"}
