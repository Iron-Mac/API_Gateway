from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import redis

# Replace these values with your Redis server details
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

redis_conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

DATABASE_URL = "sqlite:///./test.db"  # SQLite database URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def initialize_database():
    Base.metadata.create_all(bind=engine)
