from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routers import booking_router
from app.api.routers import auth_router
from app.api.routers import user_router
from app.core.config import settings
from app.core.db import init_db

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(booking_router.router)
app.include_router(auth_router.router, prefix='/auth')
app.include_router(user_router.router, prefix='/account')