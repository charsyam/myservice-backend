from sqlalchemy import Column, TEXT, INT, BIGINT, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select, func, Integer, Table, Column, MetaData

import uuid
from datetime import datetime

from database import Base


class VisitHistory(Base):
    __tablename__ = "visit_history"

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    uid = Column(TEXT, nullable=False, default=uuid.uuid4)
    shorturl_id = Column(BIGINT, nullable=False)
    shorturl_uid = Column(TEXT, nullable=False)
    agent = Column(TEXT, nullable=False)
    request_ip = Column(TEXT, nullable=False)
    status = Column(TEXT, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
