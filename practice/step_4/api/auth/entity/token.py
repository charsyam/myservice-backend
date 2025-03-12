from sqlalchemy import Column, TEXT, INT, BIGINT, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select, func, Integer, Table, Column, MetaData

import uuid
from datetime import datetime


Base = declarative_base()

class Token(Base):
    __tablename__ = "tokens"

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    uid = Column(TEXT, nullable=False, default=uuid.uuid4)
    user_id = Column(BIGINT, nullable=False)
    user_uid = Column(TEXT, nullable=False)
    access_token = Column(TEXT, nullable=False)
    refresh_token = Column(TEXT, nullable=False)
    status = Column(TEXT, nullable=False)
    request_ip = Column(TEXT, nullable=False)
    access_token_expired_at = Column(DateTime, nullable=False)
    refresh_token_expired_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
