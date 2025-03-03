from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel

USERNAME="insight"
PASSWORD="insight"
HOST="localhost"
PORT=3306
DBNAME="shorturl"

DB_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'

class engineconn:

    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle = 500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn


engine = engineconn()
Base = declarative_base()


def get_session():
    session = engine.sessionmaker()
    try:
        yield session
    finally:
        session.close()
