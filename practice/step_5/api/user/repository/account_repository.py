from sqlalchemy.orm import Session
from sqlalchemy import func

from core.database.repository.base import BaseRepository
from api.user.entity.account import Account as T
from exceptions import *


class AccountRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)

    def find_by_id(self, user_id):
        return self.db.query(T).filter(T.id == user_id).first()

    def find_by_email(self, email, status='REGISTERED'):
        return self.db.query(T).filter(T.email == email, T.status == status).first()
