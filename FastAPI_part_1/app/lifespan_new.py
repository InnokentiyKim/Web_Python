from models import init_orm, close_orm
from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("START")
    await init_orm()
    yield
    print("END")
    await close_orm()
