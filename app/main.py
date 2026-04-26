from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
def root_get():
    return {'message': 'welcome hotel management room app!!'}