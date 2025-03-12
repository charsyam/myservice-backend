from sqlalchemy.orm import Session
from sqlalchemy import func

from core.database.repository.base import BaseRepository
from api.shorturl.entity.shorturl import ShortUrl as T
from api.shorturl.manager.shard_manager import ShortUrlShardManager
from exceptions import *


class ShortUrlRepository:
    def __init__(self, shard_manager: Session):
        self.shard_manager = shard_manager

    def find_by_shorturl(self, shorturl, status='REGISTERED'):
        db = self.shard_manager.get_shard(shorturl)
        return db.query(T).filter(T.shorturl == shorturl, T.status == 'REGISTERED').first()

    def save(self, entity):
        db = self.shard_manager.get_shard(entity.shorturl)
        db.add(entity)
        db.flush()
        db.refresh(entity)
        return entity
