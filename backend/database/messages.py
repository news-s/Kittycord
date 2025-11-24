import models, datetime, login
from sqlalchemy import asc

async def store_channel_message(author_id, channel_id, content, attachment_id):
    db_gen = models.get_db()
    db = next(db_gen)
    message = models.Message(user_id=author_id, channel_id=channel_id, date=datetime.now(), text=content, attachment_id=attachment_id)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message.id

def get_last_messsages_from_channel(count, channel_id):
    db_gen = models.get_db()
    db = next(db_gen)
    #Check if channel exists
    channel = db.query(models.Channel).filter_by(id=channel_id).first()
    if channel == None:
        return {'status': "error", 'message': "channel doesnt exists"}
    # TODO: start_count stop_count
    messages = db.query(models.Message).filter_by(channel_id=channel_id).order_by(asc(models.Message.date)).limit(count).all()
    return {'status': "success", "messages":
            [{
                'author_id': m.user_id,
                'date': m.date,
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

def delete_message(id):
    db_gen = models.get_db()
    db = next(db_gen)
    message = db.query(models.Message).filter_by(id=id).first()
    if message == None:
        return {'status': "error",  'message': "message doesnt exist"}
    message.delete()
    db.commit()
    return {'status': "success"}

def edit_message(id, new_content):
    db_gen = models.get_db()
    db = next(db_gen)
    message = db.query(models.Message).filter_by(id=id).first()
    if message == None:
        return {'status': "error",  'message': "message doesnt exist"}
    message.text = new_content
    db.commit()
    return {'status': "success"}

if __name__ == "__main__":
    login.create_user("test", "test")