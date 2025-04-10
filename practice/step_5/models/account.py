from sqlalchemy import Column, TEXT, INT, BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select, func, Integer, Table, Column, MetaData


Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    uid = Column(TEXT, nullable=False)
    email = Column(TEXT, nullable=False)
    password = Column(TEXT, nullable=False)
    status = Column(TEXT, nullable=False)


class AccountConverter:
    @staticmethod
    def to_dao(account):
        resp = {
            "id": account.id,
            "uid": account.uid,
            "email": account.email,
            "status": account.status 
        }

        return resp
