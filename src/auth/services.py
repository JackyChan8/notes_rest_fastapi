from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists

from src.users.models import User
from src.auth.schemas import Token
from src.auth.config import JWTSettings, pwd_context
from src.users.schemas import UserCreate, UserAuth, UserGet

jwt_settings = JWTSettings()


# bcrypt Password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the plain_password and hashed"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash the password"""
    return pwd_context.hash(password)


# jwt Settings
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a new access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             jwt_settings.JWT_SECRET_KEY.get_secret_value(),
                             algorithm=jwt_settings.ALGORITHM)
    return encoded_jwt


# Services
async def create_user(user: UserCreate, session: AsyncSession) -> UserGet:
    """Create User Service"""
    query = select(exists(select(User.username).where(User.username == user.username)))
    exists_user = await session.scalar(query)
    if exists_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')
    db_user = User(username=user.username, password=get_password_hash(user.password))
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return UserGet(id=db_user.id, username=db_user.username)


async def login_for_access_token(user: UserAuth, session: AsyncSession) -> Token:
    """Login for access token"""
    query = select(exists(select(User.username).where(User.username == user.username)))
    exists_user = await session.scalar(query)
    if not exists_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User doesn\'t exists')

    db_user = await session.execute(select(User.id, User.password).where(User.username == user.username))
    db_user = db_user.one()
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Incorrect username or password')

    access_token_expires = timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token)

