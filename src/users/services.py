from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from src.auth.services import get_password_hash
from src.users.models import User
from src.users.schemas import UserMe


async def get_user_by_id(user_id: int, session: AsyncSession) -> UserMe:
    """Get User By ID"""
    user_db = await session.execute(select(User.id, User.username, User.created_at).where(User.id == user_id))
    user = user_db.one()
    return UserMe(id=user.id, username=user.username, created_at=user.created_at)


async def change_username(user_id: int, username: str, session: AsyncSession):
    """Change User username"""
    query = update(User).where(User.id == user_id).values(username=username).returning(User)
    user = await session.scalar(query, execution_options={'synchronize_session': 'fetch'})
    session.add(user)
    await session.commit()
    await session.refresh(user)


async def change_password(user_id: str, password: str, session: AsyncSession):
    """Change User password"""
    query = update(User).where(User.id == user_id).values(password=get_password_hash(password)).returning(User)
    user = await session.scalar(query, execution_options={'synchronize_session': 'fetch'})
    session.add(user)
    await session.commit()
    await session.refresh(user)
