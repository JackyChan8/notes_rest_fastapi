from datetime import datetime
from pydantic import Field, field_validator

from src.schemas import Serializer


class NoteBase(Serializer):
    pass


class NoteCreate(NoteBase):
    text: str = Field(
        min_length=10,
        max_length=200,
        title='Text',
        description='Text of the note',
    )


class NoteGet(NoteCreate):
    id: int
    is_published: bool
    author_id: int
    created_at: datetime

    @field_validator("created_at")
    def parse_date(cls, value):
        return value.strftime("%d-%m-%Y")


class NoteUpdate(NoteCreate):
    is_published: bool | None = None
    text: str | None = Field(
        default=None,
        min_length=10,
        max_length=200,
        title='Text',
        description='Text of the note',
    )
