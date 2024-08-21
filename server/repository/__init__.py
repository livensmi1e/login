from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_engine(str(settings.POSTGRES_URI))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Database:
    @staticmethod
    def get_db():
        try:
            db = SessionLocal()
            yield db
        except Exception as e:
            raise e
        finally:
            db.close()