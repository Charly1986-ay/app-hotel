from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from apscheduler.schedulers.background import BackgroundScheduler

from app.api.routers import booking_router
from app.api.routers import auth_router
from app.api.routers import user_router
from app.core.config import settings
from app.core.db import init_db
from app.core.tasks import check_in_job, check_out_job

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()

    scheduler = BackgroundScheduler(timezone="America/Argentina/Buenos_Aires")
    
    # tarea 1 => check-out JOB (15.00hs)
    scheduler.add_job(
        check_out_job,
        trigger='cron',
        hour=15,
        minute=0,
        id="checkout_daily"
    )
    # tarea 2 => check-IN JOB (17.00hs)
    scheduler.add_job(
        check_in_job,
        trigger='cron',
        hour=17,
        minute=0,
        id="checkin_daily"
    )
    scheduler.start()
    print("Scheduler iniciado: Tareas programadas con éxito.")
    
    yield
    
    # 4. Apagamos al cerrar la app
    scheduler.shutdown()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(booking_router.router)
app.include_router(auth_router.router, prefix='/auth')
app.include_router(user_router.router, prefix='/account')