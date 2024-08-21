from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import redis

from fastapi import HTTPException

from config import settings

engine = create_engine(str(settings.POSTGRES_URI))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

redis_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    max_connections=settings.REDIS_MAX_CONNECTIONS,
    decode_responses=True
)

class Database:
    @staticmethod
    def get_db():
        try:
            db = SessionLocal()
            yield db
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()

    @staticmethod
    def get_session_db():
        try:
            r = redis.Redis(connection_pool=redis_pool)
            yield r
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            pass