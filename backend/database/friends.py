from database import models
from sqlalchemy import update

def invite_friend(me: int, someone: str):
    db_gen = models.get_db()
    db = next(db_gen)
    user = db.query(models.User).filter_by(name=someone).first()
    if user == None:
        return {'status': "error", 'message': "Requested user doesn't exist"}
    existing_request = db.query(models.Friend_request).filter_by(user_id_1=me, user_id_2=user.id).first()
    if existing_request != None:
        return {'status': "error", 'message': "Friend request already sent"}
    existing_friendship = db.query(models.User).filter_by(id=me).all()
    for friend in existing_friendship:
        if friend.id == someone:
            return {'status': "error", 'message': "Already friends"}

    friend_request = models.Friend_request(user_id_1=me, user_id_2=user.id)
    db.add(friend_request)
    db.commit()
    db.refresh(friend_request)
    return {'status': "success", 'friend_request_id': friend_request.id}

def get_friend_requests(user_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    requests = db.query(models.User).join(models.Friend_request, models.Friend_request.user_id_1==models.User.id).filter(models.Friend_request.user_id_2 == user_id).all()
    return {'status': "success", 'friend_requests':
            [{
                # 'id': fr.id,
                'from_user_id': fr.id,
                'name': fr.name
            } for fr in requests]
        }

def add_friend(db, me: int, someone: int):
    result = db.query(models.User).filter_by(id=me).first()
    if result == None:
        return {'status': "error", 'message': "user doesnt exists"}
    elif result.friends == None:
        print("Friends is noen")
        db.execute(update(models.User).where(models.User.id==me).values(friends = [someone]))
    else:
        print("friends is not noen")
        friends = result.friends.append(someone)
        db.execute(update(models.User).where(models.User.id==me).values(friends=friends))
    db.commit()

def accept_friend(me: int, someone: str):
    db_gen = models.get_db()
    db = next(db_gen)
    user = db.query(models.User).filter_by(name=someone).first()
    if user == None:
        return {'status': "error", 'message': "User doesnt exist"}
    friend_request = db.query(models.Friend_request).filter_by(user_id_1=user.id, user_id_2=me).first()
    if friend_request == None:
        return {'status': "error", 'message': "No friend request found"}
    result = add_friend(db, me, user.id)
    if result != None:
        return {'status': "error", 'message': result['message']}
    result = add_friend(db, user.id, me)
    if result != None:
        return {'status': "error", 'message': result['message']}
    db.delete(friend_request)
    db.commit()
    return {'status': "success"}

def reject_friend(me: int, someone: str):
    db_gen = models.get_db()
    db = next(db_gen)
    user = db.query(models.User).filter_by(name=someone).first()
    if user == None:
        return {'status': "error", 'message': "User doesnt exist"}
    friend_request = db.query(models.Friend_request).filter_by(user_id_1=user.id, user_id_2=me).first()
    if friend_request == None:
        return {'status': "error", 'message': "No friend request found"}
    db.delete(friend_request)
    db.commit()
    return {'status': "success"}

def get_friends(user_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    user = db.query(models.User).filter_by(id=user_id).first()
    if user.friends == None:
        return {'status': "success", 'friends': []}
    friends = db.query(models.User).filter(models.User.id.in_(user.friends)).all()
    if user == None:
        return {'status': "error", 'message': "user doesnt exists"}
    return {'status': "success", 'friends': [friend.display_name for friend in friends]}

def is_friends(user_id1: int, user_id2: int):
    db_gen = models.get_db()
    db = next(db_gen)
    user = db.query(models.User).filter_by(id=user_id1).first()
    if user.friends == None:
        return False
    return user_id2 in user.friends

if __name__ == "__main__":
    invite_friend(1, 2)
    print(get_friend_requests(2))
    r = reject_friend(2, 1)
    print(r)
    print(get_friends(1))
    print(get_friends(2))
