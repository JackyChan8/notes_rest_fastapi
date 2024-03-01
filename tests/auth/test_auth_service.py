from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import services
from src.auth.dependencies import get_user_id_from_jwt
from src.users.schemas import UserCreate, UserAuth
from src.users.models import User


class UserTest:
    username = 'testuser'
    password = '12345678'


async def get_user(db_session: AsyncSession) -> User:
    user = await db_session.scalar(select(User).where(User.username == UserTest.username))
    return user


async def check_decode_token(user_id: int, token: str):
    decode_user_id_from_token = await get_user_id_from_jwt(token)
    assert user_id == int(decode_user_id_from_token)


async def test_create_user(db_session: AsyncSession):
    user_in = UserCreate(username=UserTest.username, password=UserTest.password, password_confirm=UserTest.password)
    user = await services.create_user(user_in, db_session)
    assert user.id


async def test_login_for_access_token(db_session: AsyncSession):
    await test_create_user(db_session)
    user_in = UserAuth(username=UserTest.username, password=UserTest.password)
    token = await services.login_for_access_token(user_in, db_session)
    assert token.access_token

    # Check Decode Token
    user = await get_user(db_session)
    await check_decode_token(user.id, token.access_token)


async def test_create_access_token(db_session: AsyncSession):
    await test_create_user(db_session)
    user = await get_user(db_session)
    jwt_token = services.create_access_token(data={'sub': str(user.id)}, expires_delta=timedelta(minutes=30))

    # Check Decode Token
    await check_decode_token(user.id, jwt_token)


# Testing bcrypt Password

async def test_bcrypt_password(db_session: AsyncSession):
    hash_password = services.get_password_hash(UserTest.password)
    assert services.verify_password(UserTest.password, hash_password) is True


async def test_check_password_hash(db_session: AsyncSession):
    await test_create_user(db_session)
    user = await get_user(db_session)
    assert services.verify_password(UserTest.password, user.password) is True
