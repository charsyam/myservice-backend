from sqlalchemy.orm import Session
from sqlalchemy import func

from api.auth.entity.certificate import Certificate as T
from core.database.repository.base import BaseRepository
from exceptions import *


class CertificateRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)

    def find_by_id(self, certificate_id):
        return self.db.query(T).filter(T.id == certificate_id).first()

    def count_all(self):
        return self.db.query(func.count(T.id)).scalar()
