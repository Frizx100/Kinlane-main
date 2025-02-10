from fastapi import APIRouter, Response, status, Body
from fastapi.responses import JSONResponse
from starlette.requests import Request

from db_handler import DataBase

user_router = APIRouter(prefix='/user', tags=["user"])

@user_router.post('/login')
async def login(request: Request, data=Body()):
    bd: DataBase = request.app.state.database
    answer = bd.login(data['username'], data['password'])
    return JSONResponse({'status_message': answer['status_message']}, status_code=answer['status'])

@user_router.post('/registration')
async def registration(request: Request, data=Body()):
    bd: DataBase = request.app.state.database
    answer = bd.registration(data['username'], data['password'])
    return JSONResponse({'status_message': answer['status_message']}, status_code=answer['status'])