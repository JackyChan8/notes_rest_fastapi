from fastapi import APIRouter, status

from src.users.services import change_username, change_password
from src.users.schemas import UserBase, UserPasswords, UserMe
from src.auth.dependencies import current_user
from src.dependencies import async_session
from src.utils.status import auth_status, update_status


router = APIRouter(prefix='/users', tags=['users'])


@router.get('/me', response_model=UserMe)
async def get_users_me(user: current_user):
    """Get Information About Me"""
    return user


@router.patch('/me',
              status_code=status.HTTP_204_NO_CONTENT,
              responses={**auth_status, **update_status})
async def update_username(body: UserBase, user: current_user, session: async_session):
    """Update Username User"""
    return await change_username(user.id, body.username, session)


@router.patch('/me/password',
              status_code=status.HTTP_204_NO_CONTENT,
              responses={**auth_status, **update_status})
async def update_password(body: UserPasswords, user: current_user, session: async_session):
    """Update Password User"""
    return await change_password(user.id, body.password, session)
