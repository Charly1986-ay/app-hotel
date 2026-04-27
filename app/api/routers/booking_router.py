from sys import prefix

from fastapi import Request
from fastapi.routing import APIRouter


router = APIRouter()

@router.get('/')
def get_index(request: Request):
    return {'mensagge': 'index'}