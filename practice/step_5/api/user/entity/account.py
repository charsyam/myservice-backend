from sqlalchemy import Column, TEXT, INT, BIGINT, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select, func, Integer, Table, Column, MetaData
from database import Base

from datetime import datetime
import uuid


class Account(Base):
    __tablename__ = "accounts"

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    uid = Column(TEXT, nullable=False, default=uuid.uuid4)
    email = Column(TEXT, nullable=False)
    password = Column(TEXT, nullable=False)
    status = Column(TEXT, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
