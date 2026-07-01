from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Cambiamos BackgroundScheduler por AsyncIOScheduler para soportar tareas async
from apscheduler.schedulers.asyncio import AsyncIOScheduler

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
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Agregamos el 'await' obligatorio para la base de datos asíncrona
    await init_db()

    # 2. Usamos AsyncIOScheduler para que se lleve bien con el entorno async
    scheduler = AsyncIOScheduler(timezone="America/Argentina/Buenos_Aires")
    
    # tarea 1 => check-out JOB (11.21hs)
    scheduler.add_job(
        check_out_job,
        trigger='cron',
        hour=11,
        minute=33,
        id="checkout_daily",
        replace_existing=True
    )
    # tarea 2 => check-IN JOB (11.24hs)
    scheduler.add_job(
        check_in_job,
        trigger='cron',
        hour=11,
        minute=36,
        id="checkin_daily",
        replace_existing=True
    )
    scheduler.start()
    print("Scheduler (Async) iniciado....")
    
    yield
    
    # 4. Apagamos al cerrar la app
    scheduler.shutdown()    

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)

# 2. AGREGA EL MIDDLEWARE DE CORS (¡Obligatorio para WebSockets entre orígenes!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En desarrollo puedes usar ["*"], en producción pones tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(auth_middleware)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(booking_router.router)
app.include_router(auth_router.router, prefix='/auth')
app.include_router(user_router.router, prefix='/api')
app.include_router(supervisor_router.router, prefix='/admin/supervisor')
app.include_router(receptionist_router.router, prefix='/admin/receptionist')
app.include_router(manager_router.router, prefix='/admin/manager')