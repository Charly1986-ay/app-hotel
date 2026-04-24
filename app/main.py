from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root_get():
    return {'message': 'welcome hotel management room app!!'}