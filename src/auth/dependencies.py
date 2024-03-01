from typing import Annotated

from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.auth.config import JWTSettings
from src.auth.schemas import TokenData
from src.users.models import User
from src.users.schemas import UserMe
from src.users.services import get_user_by_id

jwt_settings = JWTSettings()

auth_scheme = HTTPBearer()


async def get_user_id_from_jwt(token: str):
    """Get User ID from JWT"""
    payload: dict = jwt.decode(
        token,
        jwt_settings.JWT_SECRET_KEY.get_secret_value(),
        algorithms=[jwt_settings.ALGORITHM]
    )
    user_id = payload.get("sub")
    return user_id


async def get_current_user(token: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)],
                           session: Annotated[AsyncSession, Depends(get_session)]) -> UserMe:
    """Get Current User by Bearer Token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id = await get_user_id_from_jwt(token.credentials)
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_id(token_data.id, session=session)
    if user is None:
        raise credentials_exception
    return user


current_user = Annotated[User, Depends(get_current_user)]

