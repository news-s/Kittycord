import datetime
from sqlalchemy import asc, delete

from database import models

def store_channel_message(author_id, channel_id, content, attachment_id):
    db_gen = models.get_db()
    db = next(db_gen)
    message = models.Message(user_id=author_id, channel_id=channel_id, date=datetime.datetime.now(), text=content, attachment_id=attachment_id)
    db.add(message)
    db.commit()
    db.refresh(message)
    return {'status': "success", 'message_id': message.id }

def get_last_messsages_from_channel(count: int, channel_id: int, start_count: int = 0):
    db_gen = models.get_db()
    db = next(db_gen)
    #Check if channel exists
    channel = db.query(models.Channel).filter_by(id=channel_id).first()
    if channel == None:
        return {'status': "error", 'message': "channel doesnt exists"}
    messages = db.query(models.Message).filter_by(channel_id=channel_id).order_by(asc(models.Message.date)).offset(start_count).limit(count).all()
    return {'status': "success", "messages":
            [{
                'message_id': m.id,
                'author_id': m.user_id,
                'date': str(m.date),
                'content': m.text,
                'attachment_id': m.attachment_id
            } for m in messages]
        }

def get_author(id_message):
    db_gen = models.get_db()
    db = next(db_gen)
    message = db.query(models.Message).filter_by(id=id_message).first()
    if message == None:
        return {'status': "error",  'message': "message doesnt exist"}
    return {'status': "success", 'author_id': message.user_id}


def get_channel_from_mesage(id_message):
    db_gen = models.get_db()
    db = next(db_gen)
    message = db.query(models.Message).filter_by(id=id_message).first()
    if message == None:
        return {'status': "error",  'message': "message doesnt exist"}
    return {'status': "success", 'message_id': message.channel_id}

def delete_message(id):
    db_gen = models.get_db()
    db = next(db_gen)
    db.execute(delete(models.Message).where(models.Message.id==id))
    db.commit()
    return {'status': "success"}
    
def change_message(id, new_content):
    db_gen = models.get_db()
    db = next(db_gen)
    message = db.query(models.Message).filter_by(id=id).first()
    if message == None:
        return {'status': "error",  'message': "message doesnt exist"}
    message.text = new_content
    db.commit()
    return {'status': "success"}

def channel_id_by_message_id(message_id):
    db_gen = models.get_db()
    db = next(db_gen)
    channel_id = db.query(models.Message).filter_by(id=message_id).first().channel_id
    if channel_id == None:
        return {'status': "error", 'message': "message doesnt exists"}
    return {'status': "success", 'channel_id': channel_id}