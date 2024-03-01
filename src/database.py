import uuid

from asyncpg import Connection
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import Settings


class SQLAlchemyConnection(Connection):
    def _get_unique_id(self, prefix: str) -> str:
        return f'__asyncpg_{prefix}_{uuid.uuid4()}__'


def engine_factory(settings: Settings):
    return create_async_engine(
        url=settings.db_dsn().__str__().replace('postgresql', 'postgresql+asyncpg', 1),
        echo=True,
        connect_args={
            'statement_cache_size': 0,  # required by asyncpg
            'prepared_statement_cache_size': 0,  # required by asyncpg
            'connection_class': SQLAlchemyConnection,
        },
        pool_pre_ping=True,
    )


Session = async_sessionmaker()


async def get_session():
    async with Session() as session:
        yield session
