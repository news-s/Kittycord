import datetime
from sqlalchemy import asc

from database import models

def store_channel_message(author_id, channel_id, content, attachment_id):
    db_gen = models.get_db()
    db = next(db_gen)
    message = models.Message(user_id=author_id, channel_id=channel_id, date=datetime.datetime.now(), text=content, attachment_id=attachment_id)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message.id

def get_last_messsages_from_channel(count, channel_id):
    db_gen = models.get_db()
    db = next(db_gen)
    messages = db.query(models.Message).filter_by(channel_id=channel_id).order_by(asc(models.Message.date)).limit(count).all()
    return {'status': "success", "messages":
            [{
                'author_id': m.user_id,
                'date': m.date,
                'content': m.text,
                'attachment_id': m.attachment_id
            } for m in messages]
        }

def delete_message(id):
    db_gen = models.get_db()
    db = next(db_gen)
    message = db.query(models.Message).filter_by(id=id).first()
    if message == None:
        return {'status': "error",  'message': "message doesnt exist"}
    message.delete()
    db.commit()
    return {'status': "success"}
    
