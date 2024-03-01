from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str
    APP_VERSION: str
    APP_DESCRIPTION: str
    APP_SUMMARY: str

    # Postgresql database settings
    DATABASE_PROTOCOL: str = 'postgresql'
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: SecretStr
    DATABASE_HOST: str
    DATABASE_PORT: int

    def db_dsn(self, protocol=None) -> PostgresDsn:
        protocol = protocol or self.DATABASE_PROTOCOL
        return PostgresDsn.build(
            scheme=protocol,
            username=self.DATABASE_USER,
            password=self.DATABASE_PASSWORD.get_secret_value(),
            host=self.DATABASE_HOST,
            port=self.DATABASE_PORT,
            path=self.DATABASE_NAME,
        )

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
