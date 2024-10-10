from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import redis
import os

# Replace these values with your Redis server details
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = 0

DATABASE_URL = "sqlite:///./data/test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_redis_connection():
    redis_conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    try:
        yield redis_conn
    finally:
        redis_conn.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def initialize_database():
    Base.metadata.create_all(bind=engine)
