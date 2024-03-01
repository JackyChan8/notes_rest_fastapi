from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import Settings
from src.auth import router as auth_router
from src.users import router as users_router
from src.notes import router as notes_router
from src.database import engine_factory, Session


settings = Settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    summary=settings.APP_SUMMARY,
)
app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(notes_router.router)

engine = engine_factory(settings)
Session.configure(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await engine.connect()
    yield
    await engine.dispose()
