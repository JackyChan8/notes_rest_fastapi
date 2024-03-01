from fastapi import APIRouter

from src.auth.schemas import Token
from src.users.schemas import UserAuth, UserGet, UserCreate
from src.auth.services import create_user, login_for_access_token
from src.dependencies import async_session

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=UserGet)
async def register(user: UserCreate, session: async_session):
    """Register a new User"""
    return await create_user(user, session)


@router.post('/login', response_model=Token)
async def login(user: UserAuth, session: async_session):
    """Login a user"""
    return await login_for_access_token(user, session)
