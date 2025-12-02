import datetime
from sqlalchemy import asc, delete

from database import models

def store_direct_message(user_id1, user_id2, content, attachment_id):
    db_gen = models.get_db()
    db = next(db_gen)
    dm = models.DM(user_id_1=user_id1, user_id_2=user_id2, date=datetime.datetime.now(), text=content, attachment_id=attachment_id)
    db.add(dm)
    db.commit()
    db.refresh(dm)
    return {'status': "success", 'dm_id': dm.id }


def get_messsages_from_dm(count: int, user_id1: int, user_id2: int, start_count: int = 0):
    db_gen = models.get_db()
    db = next(db_gen)
    messages = db.query(models.DM).filter_by(user_id_1=user_id1, user_id_2=user_id2).order_by(asc(models.DM.date)).offset(start_count).limit(count).all()
    return {'status': "success", "messages":
            [{
                'message_id': m.id,
                'author_id': m.user_id_1,
                'reciever_id': m.user_id_2,
                'date': str(m.date),
                'content': m.text,
                'attachment_id': m.attachment_id
            } for m in messages]
        }

def get_author(id_dm):
    db_gen = models.get_db()
    db = next(db_gen)
    message = db.query(models.DM).filter_by(id=id_dm).first()
    if message == None:
        return {'status': "error",  'message': "DM doesnt exist"}
    return {'status': "success", 'author_id': message.user_id_1, 'reciever_id': message.user_id_2}


def delete_dm(id):
    db_gen = models.get_db()
    db = next(db_gen)
    db.execute(delete(models.DM).where(models.DM.id==id))
    db.commit()
    return {'status': "success"}


def change_dm(id, new_content):
    db_gen = models.get_db()
    db = next(db_gen)
    message = db.query(models.DM).filter_by(id=id).first()
    if message == None:
        return {'status': "error",  'message': "DM doesnt exist"}
    message.text = new_content
    db.commit()
    return {'status': "success"}