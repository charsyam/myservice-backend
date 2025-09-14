from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel


USERNAME="insight"
PASSWORD="insight"
HOST="127.0.0.1"
PORT=3306
DBNAME="shorturl"

DB_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'

REDIS_HOSTS = [
    ("127.0.0.1", 6379, "Redis1"),
    ("127.0.0.1", 6379, "Redis2"),
    ("127.0.0.1", 6379, "Redis3"),
]

WORKER_QUEUE_HOST = ("127.0.0.1", 6379)
DATABASE = "127.0.0.1"

class engineconn:
    def __init__(self, host):
        self.host = host
        self.engine = create_engine(f'mysql+pymysql://{USERNAME}:{PASSWORD}@{host}:{PORT}/{DBNAME}', pool_recycle = 500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn


engine = engineconn(DATABASE)
Base = declarative_base()


def set_engine(_engine):
    global engine
    engine = _engine


def get_session():
    session = engine.sessionmaker()
    try:
        yield session
    finally:
        session.close()
