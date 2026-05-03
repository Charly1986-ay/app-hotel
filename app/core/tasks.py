from sqlmodel import Session
from .db import engine
from app.services import tasks_services as tasks
from datetime import date


def check_out_job():
    with Session(engine) as db:
        print('[JOB-CHECK OUT] comienza la rutina PROGRAMADA...!!!')
        tasks.check_out(db=db, check_out=date.today())
        print('Ha finalizado la rutina...!!!')

def check_in_job():
    with Session(engine) as db:
        print('[JOB-CHECK IN] comienza la rutina PROGRAMADA...!!!')
        tasks.check_in(db=db, check_in=date.today())
        print('Ha finalizado la rutina...!!!')