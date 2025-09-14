from sqlalchemy.orm import Session
from sqlalchemy import func

from api.auth.entity.token import Token as T
from core.database.repository.base import BaseRepository
from exceptions import *


class TokenRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)
