from fastapi import FastAPI

from contextlib import asynccontextmanager

from database.database import init_db
from postback.endpoints import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)

