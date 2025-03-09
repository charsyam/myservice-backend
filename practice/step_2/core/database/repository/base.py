from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, entity):
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity
