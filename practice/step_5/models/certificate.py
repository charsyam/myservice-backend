from sqlalchemy import Column, TEXT, INT, BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select, func, Integer, Table, Column, MetaData


Base = declarative_base()

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    public_key = Column(TEXT, nullable=False)
    private_key = Column(TEXT, nullable=False)
    encrypt_type = Column(TEXT, nullable=False)
    status = Column(TEXT, nullable=False)


class CertificateConverter:
    @staticmethod
    def to_dao(certificate):
        resp = {
            "id": certificate.id,
            "public_key": certificate.public_key,
            "encrypt_type": certificate.encrypt_type,
            "status": certificate.status 
        }

        return resp
