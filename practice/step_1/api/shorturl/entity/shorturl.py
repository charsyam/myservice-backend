from sqlalchemy import Column, TEXT, INT, BIGINT, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select, func, Integer, Table, Column, MetaData

import uuid
from datetime import datetime

from database import Base


class ShortUrl(Base):
    __tablename__ = "shorturls"

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    uid = Column(TEXT, nullable=False, default=uuid.uuid4)
    user_id = Column(BIGINT, nullable=False)
    user_uid = Column(TEXT, nullable=False)
    source = Column(TEXT, nullable=False)
    shorturl = Column(TEXT, nullable=False, default=uuid.uuid4)
    status = Column(TEXT, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
