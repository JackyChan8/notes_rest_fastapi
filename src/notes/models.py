from typing import Optional
from datetime import datetime

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.models import Base, int_pk


class Note(Base):
    __tablename__ = 'notes'

    id: Mapped[int_pk]
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean(), default=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(default=func.now())
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id'), primary_key=True
    )
