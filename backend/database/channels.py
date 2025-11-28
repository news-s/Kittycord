from database import models
from sqlalchemy import delete

def create_channel(server_id, name, role_needed = None):
    db_gen = models.get_db()
    db = next(db_gen)
    if role_needed == None:
        channel = models.Channel(server_id=server_id, name=name)
    else:
        roles = db.query(models.Server).filter_by(server_id=server_id).first().roles
        if role_needed not in roles:
            return {'status': "error", 'message': "role_needed doesnt exists"}
        channel = models.Channel(server_id=server_id, name=name, role_needed=role_needed)
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return {'status': "success", 'channel_id': channel.id}

def delete_channel(channel_id):
    db_gen = models.get_db()
    db = next(db_gen)
    # Deleting all messages with channel id
    db.execute(delete(models.Message).where(models.Message.channel_id==channel_id))
    db.execute(delete(models.Channel).where(models.Channel.id==channel_id))
    db.commit()
    return {'status': "success"}

def get_server_id(channel_id):
    db_gen = models.get_db()
    db = next(db_gen)
    server_id = db.query(models.Channel).filter_by(id=channel_id).first().server_id
    if server_id == None:
        return {'status': "error", 'message': "channel doesnt exists"}
    return {'status': "success", 'server_id': server_id}

def get_channels(server_id):
    db_gen = models.get_db()
    db = next(db_gen)
    channels = db.query(models.Channel).filter_by(server_id=server_id).all()
    return {'status': "success", 'channels':
            [{
                'id': c.id,
                'name': c.name,
                'color': c.color,
                'role_needed': c.role_needed
            } for c in channels]
        }

def get_role_needed(channel_id):
    db_gen = models.get_db()
    db = next(db_gen)
    channel = db.query(models.Channel).filter_by(id=channel_id).first()
    if channel == None:
        return {'status': "error", 'message': "channel doesnt exists"}
    return {'status': "success", 'role_needed': channel.role_needed}

def change_channel_name(channel_id, new_name):
    db_gen = models.get_db()
    db = next(db_gen)
    channel = db.query(models.Channel).filter_by(id=channel_id).first()
    if channel == None:
        return {'status': "error", 'message': "channel doesnt exists"}
    channel.name = new_name
    db.commit()
    return {'status': "success"}

def change_channel_role_needed(channel_id, new_role_needed):
    db_gen = models.get_db()
    db = next(db_gen)
    channel = db.query(models.Channel).filter_by(id=channel_id).first()
    if channel == None:
        return {'status': "error", 'message': "channel doesnt exists"}
    server_id = channel.server_id
    if not any(int(role.id) == int(new_role_needed) for role in db.query(models.Role).filter_by(server_id=server_id).all()) and new_role_needed != None:
        return {'status': "error", 'message': "role_needed doesnt exists"}
    channel.role_needed = new_role_needed
    db.commit()
    return {'status': "success"}

def change_channel_color(channel_id: int, new_color: str):
    db_gen = models.get_db()
    db = next(db_gen)
    channel = db.query(models.Channel).filter_by(id=channel_id).first()
    if channel == None:
        return {'status': "error", 'message': "Channel does not exist"}
    channel.color = new_color
    db.commit()
    return {'status': "success"}