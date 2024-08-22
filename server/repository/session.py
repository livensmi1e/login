import redis

from sqlalchemy.orm import Session

from fastapi import Depends

from repository import Database

from models.token import SessionModel, CreateSession, UpdateSession

from schemas import SessionInfo

class SessionRepo:
    def __init__(
        self,
        db: Session = Depends(Database.get_db),
        session_db: redis.Redis = Depends(Database.get_session_db)
    ) -> None:
        self._db = db
        self._session_db = session_db
    
    def get_value(self, key: str) -> str:
        try:
            return self._session_db.get(key)
        except Exception as e:
            raise e

    def set_value(self, key: str, value: str, exp: int) -> None:
        try:
            self._session_db.set(key, value, ex=exp)
        except Exception as e:
            raise e

    def delete_value(self, key: str) -> None:
        try:
            self._session_db.delete(key)
        except Exception as e:
            raise e

    def query_session(self, id: str) -> SessionModel | None:
        try:
            session = self._db.query(SessionInfo).filter(SessionInfo.id == id).first()
            return SessionModel.model_validate(session, strict=False, from_attributes=True) if session else None
        except Exception as e:
            raise e
    
    def create_session(self, session: CreateSession) -> SessionModel:
        try:
            session = SessionInfo(**session.model_dump())
            self._db.add(session)
            self._db.commit()
            self._db.refresh(session)
            session = SessionModel.model_validate(session, strict=False, from_attributes=True)
            return session
        except Exception as e:
            self._db.rollback()
            raise e
        
    def update_session(self, id: str, new_info: UpdateSession) -> SessionModel:
        try:
            session = self._db.query(SessionInfo).filter(SessionInfo.id == id).first()
            if not session:
                raise Exception("Update session failed")
            for key, value in new_info.model_dump(exclude_none=True).items():
                setattr(session, key, value)
            self._db.commit()
            self._db.refresh(session)
            session = SessionModel.model_validate(session, strict=False, from_attributes=True)
            print("done")
            return session
        except Exception as e:
            print(e)
            self._db.rollback()
            raise e