from sqlalchemy.orm import Session
from sqlalchemy import func

from core.database.repository.base import BaseRepository
from api.shorturl.entity.shorturl import ShortUrl as T
from exceptions import *


class ShortUrlRepository:
    def __init__(self, db: Session):
        self.db = db 

    def find_by_shorturl(self, shorturl, status='REGISTERED'):
        return self.db.query(T).filter(T.shorturl == shorturl, T.status == 'REGISTERED').first()

    def save(self, entity):
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity
