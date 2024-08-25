from sqlalchemy import ForeignKey, Enum as DBEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from uuid import UUID, uuid4

from datetime import datetime

from models.token import SessionStatus

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    sessions: Mapped["SessionInfo"] = relationship(back_populates="user")

class SessionInfo(Base):
    __tablename__ = 'sessions'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    ip: Mapped[str] = mapped_column()
    location: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=True, onupdate=datetime.now())
    status: Mapped["SessionStatus"] = mapped_column(DBEnum(SessionStatus))
    user_agent: Mapped[str] = mapped_column()
    token: Mapped[str] = mapped_column(nullable=True)
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="sessions")