from passlib.context import CryptContext

from pydantic import SecretStr
from pydantic_settings import BaseSettings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class JWTSettings(BaseSettings):
    # Auth settings
    JWT_SECRET_KEY: SecretStr
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = '.env.jwt'
        env_file_encoding = 'utf-8'
