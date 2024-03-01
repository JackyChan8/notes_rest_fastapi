from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.users import services
from src.users.models import User
from src.users.schemas import UserMe
from src.auth.services import verify_password
from tests.auth.test_auth_service import test_create_user, get_user


async def test_get_user_by_id(db_session: AsyncSession):
    await test_create_user(db_session)
    user_created = await get_user(db_session)
    user_get = await services.get_user_by_id(user_created.id, db_session)
    user_me = UserMe(**user_created.__dict__)
    assert user_me == user_get


async def test_change_username(db_session: AsyncSession):
    change_username = 'biba-boba'

    await test_create_user(db_session)
    user_created = await get_user(db_session)
    await services.change_username(user_created.id, change_username, db_session)

    # Check Update Username
    user = await db_session.scalar(select(User).where(User.username == change_username))
    assert user.username == change_username


async def test_change_password(db_session: AsyncSession):
    change_password = 'biba-pass'

    await test_create_user(db_session)
    user_created = await get_user(db_session)
    await services.change_password(user_created.id, change_password, db_session)

    # Check Update Password
    user = await db_session.scalar(select(User).where(User.id == user_created.id))
    assert verify_password(change_password, user.password) is True
