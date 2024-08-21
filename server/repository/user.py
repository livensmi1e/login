from fastapi import Depends

from sqlalchemy.orm import Session

from pydantic import EmailStr

from repository import Database

from schemas import *

from models.user import *

class UserRepo:
    def __init__(self, db: Session = Depends(Database.get_db)):
        self._db = db
    
    def get_by_id(self, id: int):
        try:
            return self._db.query(User).filter(User.id == id).first()
        except Exception as e:
            raise e
    
    def get_by_email(self, email: EmailStr):
        try:
            return self._db.query(User).filter(User.email == email).first()
        except Exception as e:
            raise e
        
    def create(self, user: CreateUser) -> UserModel:
        try:
            user = User(**user.model_dump())
            self._db.add(user)
            self._db.commit()
            self._db.refresh(user)
            return UserModel.model_validate(user, strict=False, from_attributes=True)
        except Exception as e:
            raise e
