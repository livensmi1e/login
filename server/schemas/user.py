from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from uuid import UUID, uuid4

from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    created_at: Mapped[str] = mapped_column(default=datetime.now())

