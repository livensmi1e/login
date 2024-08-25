from fastapi import Depends

from sqlalchemy.orm import Session

from repository import Database

from mapping import *

from models.user import (
    PublicUser,
    InternalUser,
    CreateUser,
    QueryUser,
    UpdateUser
)

class UserRepo:
    def __init__(self, db: Session = Depends(Database.get_db)):
        self._db = db
    
    def get(self, query: QueryUser) -> PublicUser | None:
        try:
            user = self._db.query(User).filter_by(**query.model_dump(exclude_none=True)).first()
            if user:
                return PublicUser.model_validate(user, strict=False, from_attributes=True)
            return None
        except Exception as e:
            raise e
    
    def get_internal(self, query: QueryUser) -> InternalUser | None:
        try:
            user = self._db.query(User).filter_by(**query.model_dump(exclude_none=True)).first()
            if user:
                return InternalUser.model_validate(user, strict=False, from_attributes=True)
            return None
        except Exception as e:
            raise e
        
    def create(self, user: CreateUser) -> PublicUser:
        try:
            user = User(**user.model_dump())
            self._db.add(user)
            self._db.commit()
            self._db.refresh(user)
            return PublicUser.model_validate(user, strict=False, from_attributes=True)
        except Exception as e:
            self._db.rollback()
            raise e
        
    def update(self, id: str, update_info: UpdateUser) -> PublicUser:
        try:
            user = self._db.query(User).filter_by(id=id).first()
            if not user:
                raise Exception("Invalid email")
            user.password = update_info.password
            self._db.commit()
            self._db.refresh(user)
            return PublicUser.model_validate(user, strict=False, from_attributes=True)
        except Exception as e:
            self._db.rollback()
            raise e