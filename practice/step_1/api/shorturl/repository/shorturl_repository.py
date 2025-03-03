from sqlalchemy.orm import Session
from sqlalchemy import func

from core.database.repository.base import BaseRepository
from api.shorturl.entity.shorturl import ShortUrl as T
from exceptions import *


class ShortUrlRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)

    def find_by_id(self, entity_id):
        return self.db.query(T).filter(T.id == entity_id).first()

    def find_by_source(self, source, status='REGISTERED'):
        return self.db.query(T).filter(T.source == source, T.status == 'REGISTERED').first()

    def find_by_shorturl(self, shorturl, status='REGISTERED'):
        return self.db.query(T).filter(T.shorturl == shorturl, T.status == 'REGISTERED').first()
