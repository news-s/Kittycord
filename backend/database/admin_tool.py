from database import models, servers
from datetime import datetime

### Mute
def mute_user(user_id: int, server_id: int, mute_until: datetime):
    db_gen = models.get_db()
    db = next(db_gen)
    rel = db.query(models.User_Server).filter_by(user_id=user_id, server_id=server_id).first()
    if rel == None:
        return {'status': "error", 'message': "user not in server"}
    rel.muted = mute_until
    db.commit()
    return {'status': "success"}

def unmute_user(user_id: int, server_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    rel = db.query(models.User_Server).filter_by(user_id=user_id, server_id=server_id).first()
    if rel == None:
        return {'status': "error", 'message': "user not in server"}
    rel.muted = None
    db.commit()
    return {'status': "success"}

def is_user_muted(user_id: int, server_id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    rel = db.query(models.User_Server).filter_by(user_id=user_id, server_id=server_id).first()
    if rel == None:
        return {'status': "error", 'message': "user not in server"}
    elif rel.muted == None:
        return {'status': "success", 'muted': False}
    elif rel.muted > datetime.now():
        return {'status': "success", 'muted': True, 'message': rel.muted}
    elif rel.muted <= datetime.now():
        rel.muted = None
        db.commit()
        return {'status': "success", 'muted': False, 'message': "mute expired"}
    return {'status': "error", 'message': "how?"}

### Ban

def ban_user(user_id: int, server_id: int, reason: str | None):
    db_gen = models.get_db()
    db = next(db_gen)

    usr = db.query(models.User).filter_by(id=user_id).first()
    if usr == None:
        return {'status': "error", 'message': "user does not exist"}
    srv = db.query(models.Server).filter_by(id=server_id).first()
    if srv == None:
        return {'status': "error", 'message': "server does not exist"}
    
    ban = models.Ban(user_id=user_id, server_id=server_id, ban_date=datetime.now(), reason=reason)
    db.add(ban)
    servers.leave_server(user_id, server_id)
    db.commit()
    return {'status': "success"}

def unban_user(user_id: int, server_id: int):
    db_gen = models.get_db()
    db = next(db_gen)

    ban = db.query(models.Ban).filter_by(user_id=user_id, server_id=server_id).first()
    if ban == None:
        return {'status': "error", 'message': "ban not found"}
    db.delete(ban)
    db.commit()
    return {'status': "success"}

def is_user_banned(user_id: int, server_id: int):
    db_gen = models.get_db()
    db = next(db_gen)

    ban = db.query(models.Ban).filter_by(user_id=user_id, server_id=server_id).first()
    if ban == None:
        return {'status': "success", 'banned': False}
    return {'status': "success", 'banned': True, 'reason': ban.reason, 'ban_date': ban.ban_date}

def get_banned_users_in_server(server_id: int):
    db_gen = models.get_db()
    db = next(db_gen)

    bans = db.query(models.Ban).filter_by(server_id=server_id).all()
    return {'status': "success", 'banned_users':
            [{
                'user_id': ban.user_id,
                'ban_date': ban.ban_date,
                'reason': ban.reason,
            } for ban in bans]
        }

if __name__ == "__main__":
    mute_user(1, 1, datetime(2026, 12, 31, 23, 59, 59))
    print(is_user_muted(1, 1))
    unmute_user(1, 1)
    print(is_user_muted(1, 1))
    ban_user(1, 1, "Spamming")
    print(is_user_banned(1, 1))
    print(get_banned_users_in_server(1))
    unban_user(1, 1)
    print(is_user_banned(1, 1))