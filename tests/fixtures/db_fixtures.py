import pytest
import yoyo
from sqlalchemy.ext.asyncio import create_async_engine

import database

TTL_YOYO_MIGRATION = 300

postgres_url = 'postgresql://postgres:postgres@test-db:5432/postgres'


@pytest.fixture(scope='session', autouse=True)
def apply_migrations(settings, root_dir):
    backend = yoyo.get_backend(
        postgres_url, 'migrations'
    )

    migrations = yoyo.read_migrations((root_dir / 'migrations').as_posix())

    with backend.lock(timeout=TTL_YOYO_MIGRATION):
        backend.apply_migrations(backend.to_apply(migrations))

    yield
    with backend.lock(timeout=TTL_YOYO_MIGRATION):
        backend.rollback_migrations(backend.to_rollback(migrations))


@pytest.fixture(scope='session')
async def db_engine(settings):
    engine = create_async_engine(url=postgres_url.replace('postgresql', 'postgresql+asyncpg'))
    yield engine
    await engine.dispose()


@pytest.fixture(scope='session')
async def db_connection(db_engine):
    async with db_engine.connect() as connection:
        database.Session.configure(bind=connection)
        yield connection


@pytest.fixture
async def db_session(db_connection):
    transaction = await db_connection.begin()
    async with database.Session() as session:
        yield session
    await transaction.rollback()
