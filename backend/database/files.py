from sqlalchemy import delete
from database import models

def store_file(name: str, content: str) -> int:
    db_gen = models.get_db()
    db = next(db_gen)
    file = models.File(name=name, content=content)
    db.add(file)
    db.commit()
    db.refresh(file)
    return file.id

def retrive_file(id: int) -> dict:
    db_gen = models.get_db()
    db = next(db_gen)
    file = db.query(models.File).filter_by(id=id).first()
    if file == None:
        return {'status': "error", 'message': "file doesnt exists"}
    return {
        'status': "success",
        'name': file.name,
        'content': file.content.decode('utf-8'),
    }

def delete_file(id: int):
    db_gen = models.get_db()
    db = next(db_gen)
    db.execute(delete(models.File).where(id == id))
    db.commit()