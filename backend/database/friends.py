import models

def invite_friend(me: int, someone: int):
    db_gen = models.get_db()
    db = next(db_gen)
    existing_request = db.query(models.Friend_request).filter_by(user_id_1=me, user_id_2=someone).first()
    if existing_request != None:
        return {'status': "error", 'message': "Friend request already sent"}
    existing_friendship = db.query(models.User).filter_by(id=me).all()
    for friend in existing_friendship:
        if friend.id == someone:
            return {'status': "error", 'message': "Already friends"}

    friend_request = models.Friend_request(user_id_1=me, user_id_2=someone)
    db.add(friend_request)
    db.commit()
    db.refresh(friend_request)
    return {'status': "success", 'friend_request_id': friend_request.id}

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

def add_friend(db, me: int, someone: int):
    rslt = db.query(models.User).filter_by(id=me).first()
    if rslt == None:
        return {'status': "error", 'message': "user doesnt exists"}
    elif rslt.friends == None:
        rslt.friends = [someone]
    else:
        rslt.friends.append(someone)

def accept_friend(me: int, someone: int):
    db_gen = models.get_db()
    db = next(db_gen)
    friend_request = db.query(models.Friend_request).filter_by(user_id_1=someone, user_id_2=me).first()
    if friend_request == None:
        return {'status': "error", 'message': "No friend request found"}
    add_friend(db, me, someone)
    add_friend(db, someone, me)
    db.delete(friend_request)
    db.commit()
    return {'status': "success"}

def reject_friend(me: int, someone: int):
    db_gen = models.get_db()
    db = next(db_gen)
    friend_request = db.query(models.Friend_request).filter_by(user_id_1=someone, user_id_2=me).first()
    if friend_request == None:
        return {'status': "error", 'message': "No friend request found"}
    db.delete(friend_request)
    db.commit()
    return {'status': "success"}

def get_friends(user_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    user = db.query(models.User).filter_by(id=user_id).first()
    if user == None:
        return {'status': "error", 'message': "user doesnt exists"}
    return {'status': "success", 'friends': user.friends}

if __name__ == "__main__":
    invite_friend(1, 2)
    print(get_friend_requests(2))
    r = reject_friend(2, 1)
    print(r)
    print(get_friends(1))
    print(get_friends(2))