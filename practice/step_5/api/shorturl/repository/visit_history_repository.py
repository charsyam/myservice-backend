from sqlalchemy.orm import Session
from sqlalchemy import func

from core.database.repository.base import BaseRepository
from api.shorturl.entity.visit_history import VisitHistory as T
from exceptions import *


class VisitHistoryRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)
