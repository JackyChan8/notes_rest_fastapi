from datetime import datetime
from pydantic import Field, field_validator

from src.schemas import Serializer


class UserBase(Serializer):
    username: str = Field(
        min_length=5,
        max_length=100,
        title='Username',
        description='Username User',
    )


class UserAuth(UserBase):
    password: str


class UserGet(UserBase):
    id: int


class UserPasswords(Serializer):
    password: str = Field(
        min_length=8,
        max_length=100,
        title='Password',
        description='Password User'
    )
    password_confirm: str

    @field_validator('password_confirm')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values.data and v != values.data.get('password'):
            raise ValueError('passwords do not match')
        return v


class UserCreate(UserPasswords, UserBase):
    pass


class UserMe(UserGet):
    created_at: datetime

    @field_validator("created_at")
    def parse_date(cls, value):
        return value.strftime("%d-%m-%Y")
