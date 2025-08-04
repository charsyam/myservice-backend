from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel


USERNAME="insight"
PASSWORD="insight"
HOST="localhost"
PORT=3306
DBNAME="shorturl"

DB_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'

REDIS_HOSTS = [
    ("127.0.0.1", 6379, "Redis1"),
]

WORKER_QUEUE_HOST = ("127.0.0.1", 6379)

SHORTURL_DATABASES = [
    "127.0.0.1",
    "127.0.0.1",
]

MAIN_DATABASES = [
    "127.0.0.1",
]

class engineconn:
    def __init__(self, hosts):
        self.hosts = hosts
        self.engines = [create_engine(f'mysql+pymysql://{USERNAME}:{PASSWORD}@{db_host}:{PORT}/{DBNAME}', pool_recycle = 500) for db_host in hosts]

    def sessionmaker(self, shard_id):
        Session = sessionmaker(bind=self.engines[shard_id], autocommit=False, autoflush=False)
        session = Session()
        return session

    def connection(self, shard_id):
        conn = self.engines[shard_id].connect()
        return conn


main_engine = engineconn(MAIN_DATABASES)
shorturl_engine = engineconn(SHORTURL_DATABASES)
Base = declarative_base()


def get_session():
    session = main_engine.sessionmaker(0)
    try:
        yield session
    finally:
        session.close()


def get_shorturl_shard_session(shard_id):
    session = shorturl_engine.sessionmaker(shard_id)
    try:
        yield session
    finally:
        session.close()
