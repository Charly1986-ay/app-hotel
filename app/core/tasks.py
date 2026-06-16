from datetime import date
from .db import AsyncSessionLocal  
from app.services import tasks_services as tasks

async def check_out_job():    
    async with AsyncSessionLocal() as db:
        print('[JOB-CHECK OUT] comienza la rutina PROGRAMADA...!!!')        
        
        await tasks.check_out(db=db, check_out=date.today())
        
        print('Ha finalizado la rutina...!!!')

async def check_in_job():
    async with AsyncSessionLocal() as db:
        print('[JOB-CHECK IN] comienza la rutina PROGRAMADA...!!!')        
        
        await tasks.check_out(db=db, check_out=date.today())
        
        print('Ha finalizado la rutina...!!!')