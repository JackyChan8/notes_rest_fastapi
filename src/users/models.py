from datetime import datetime

from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.models import Base, int_pk


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int_pk]
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(Date, default=func.now())
