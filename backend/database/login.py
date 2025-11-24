import models, bcrypt
from datetime import datetime

def verify_user(name: str, password: str):
    db_gen = models.get_db()
    db = next(db_gen)
    try:
        usr = db.query(models.User).filter_by(name=name).first()
        if usr is None:
            return None
        return bcrypt.checkpw(password.encode('utf-8'), usr.password)
    finally:
        db_gen.close()

def create_user(name: str, password: str):
    db_gen = models.get_db()
    db = next(db_gen)
    try:
        # Check if username is taken
        usr = db.query(models.User).filter_by(name=name).first()
        if usr is not None:
            return {'status': "error", 'error': "name already taken"}

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = models.User(name=name, display_name=name, password=hashed, account_creation_date=datetime.now())
        db.add(user)
        db.commit()
        return {'status': "ok"}
    finally:
        db_gen.close()

def delete_user(id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    try:
        usr = db.query(models.User).filter_by(id=id).first()
        if usr is None:
            return {'status': "error", 'error': "user not found"}
        db.delete(usr)
        db.commit()
        return {'status': "ok"}
    finally:
        db_gen.close()

if __name__ == "__main__":
    create_user("test", "test")
    verify_user("test", "nah")
    verify_user("test", "test")
    delete_user(1)
