import models

def invite_friend(me: int, someone: int):
    db_gen = models.get_db()
    db = next(db_gen)
    friend_request = models.Friend_request(user_id_1=me, user_id_2=someone)
    db.add(friend_request)
    db.commit()
    db.refresh(friend_request)
    return {'status': "success"}

def get_friend_requests(user_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    requests = db.query(models.Friend_request).filter_by(user_id_2=user_id).all()
    return {'status': "success", 'friend_requests':
            [{
                'id': fr.id,
                'from_user_id': fr.user_id_1,
            } for fr in requests]
        }

def accept_friend(me: int, someone: int):
    db_gen = models.get_db()
    db = next(db_gen)
    friend_request = db.query(models.Friend_request).filter_by(user_id_1=me, user_id_2=someone).first()
    if friend_request == None:
        return {'status': "error", 'message': "No friend request found"}
    db.delete(friend_request)
    db.query(models.User).filter_by(id=me).first().friends.append(someone)
    db.query(models.User).filter_by(id=someone).first().friends.append(me)
    db.commit()
    return {'status': "success"}

def reject_friend(me: int, someone: int):
    db_gen = models.get_db()
    db = next(db_gen)
    friend_request = db.query(models.Friend_request).filter_by(user_id_1=me, user_id_2=someone).first()
    if friend_request == None:
        return {'status': "error", 'message': "No friend request found"}
    db.delete(friend_request)
    db.commit()
    return {'status': "success"}