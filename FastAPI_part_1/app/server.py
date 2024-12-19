from fastapi import FastAPI
import pydantic
from lifespan import lifespan
from models import Todo
from dependency import SessionDependency
import crud


app = FastAPI(
    title="Hello world",
    terms_of_service="",
    description="awesome project",
    lifespan=lifespan,
)


@app.get("/api/v1/todo/{todo_id}")
async def get_todo(session: SessionDependency, todo_id: int):
    todo_item = await crud.get_item_by_id(session, Todo, todo_id)
    return todo_item.dict

async def create_todo():
    pass

async def update_todo():
    pass

async def delete_todo():
    pass
