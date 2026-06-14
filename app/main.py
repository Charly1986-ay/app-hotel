from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from apscheduler.schedulers.background import BackgroundScheduler

from app.api.routers import booking_router
from app.api.routers import auth_router
from app.api.routers import user_router
from app.api.routers import supervisor_router
from app.api.routers import receptionist_router
from app.api.routers import manager_router
from app.core.config import settings
from app.core.db import init_db
from app.core.tasks import check_in_job, check_out_job
from app.middleware.aut_middleware import auth_middleware

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()

    scheduler = BackgroundScheduler(timezone="America/Argentina/Buenos_Aires")
    
    # tarea 1 => check-out JOB (13.00hs)
    scheduler.add_job(
        check_out_job,
        trigger='cron',
        hour=13,
        minute=00,
        id="checkout_daily",
        replace_existing=True
    )
    # tarea 2 => check-IN JOB (15.00hs)
    scheduler.add_job(
        check_in_job,
        trigger='cron',
        hour=15,
        minute=00,
        id="checkin_daily",
        replace_existing=True
    )
    scheduler.start()
    print("Scheduler iniciado....")
    
    yield
    
    # 4. Apagamos al cerrar la app
    scheduler.shutdown()    

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)

app.middleware("http")(auth_middleware)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(booking_router.router)
app.include_router(auth_router.router, prefix='/auth')
app.include_router(user_router.router, prefix='/api')
app.include_router(supervisor_router.router, prefix='/admin/supervisor')
app.include_router(receptionist_router.router, prefix='/admin/receptionist')
app.include_router(manager_router.router, prefix='/admin/manager')