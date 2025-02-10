from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from db_handler import DataBase

from user.app import user_router
from media.app import media_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    # database_ = app.state.database
    # if not database_.is_connected:
    #     await database_.connect()
    yield
    if app.state.database:
        app.state.database.close()
        

app = FastAPI(lifespan=lifespan)
app.state.database = DataBase()

app.include_router(user_router)
app.include_router(media_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=3222, reload=True)