from fastapi import FastAPI
import crud
from constants import STATUS_DELETED
from crud import add_item, get_item_by_id
from lifespan import lifespan
from dependency import SessionDependency
from models import User, Adv
from schema import (GetAdvResponse, CreateAdvRequest, CreateAdvResponse, UpdateAdvRequest,
                    UpdateAdvResponse, DeleteAdvResponse, GetUserResponse, CreateUserRequest,
                    CreateUserResponse, UpdateUserRequest, UpdateUserResponse, DeleteUserResponse)


app = FastAPI(
    title="Advertisements",
    description="Advertisements app",
    lifespan=lifespan,
)


@app.get("/api/v1/user/{user_id}", response_model=GetUserResponse, tags=['users'])
async def get_user(session: SessionDependency, user_id: int):
    user = crud.get_item_by_id(session, User, user_id)
    return user.dict


@app.post("/api/v1/user", response_model=CreateUserResponse, tags=['users'])
async def create_user(session: SessionDependency, user_request: CreateUserRequest):
    user = User(name=user_request.name, password=user_request.password)
    await add_item(session, user)
    return user.id_dict


@app.patch("/api/v1/user/{user_id}", response_model=UpdateUserResponse, tags=['users'])
async def update_user(session: SessionDependency, user_request: UpdateUserRequest, user_id: int):
    user_json = user_request.model_dump(exclude_unset=True)
    user = await get_item_by_id(session, User, user_id)
    for field, value in user_json.items():
        setattr(user, field, value)
    await add_item(session, user)
    return user.id_dict


@app.delete("/api/v1/user/{user_id}", response_model=DeleteUserResponse, tags=['users'])
async def delete_user(session: SessionDependency, user_id: int):
    user = await get_item_by_id(session, User, user_id)
    await crud.delete_item(session, user)
    return STATUS_DELETED


@app.get("/api/v1/advertisement/{advertisement_id}", response_model=GetAdvResponse, tags=['advertisements'])
async def get_adv(session: SessionDependency, adv_id: int):
    adv = crud.get_item_by_id(session, Adv, adv_id)
    return adv.dict


@app.post("/api/v1/advertisement", response_model=CreateAdvResponse, tags=['advertisements'])
async def create_adv(session: SessionDependency, adv_request: CreateAdvRequest):
    adv = Adv(title=adv_request.title, description=adv_request.description,
              price=adv_request.price, author=adv_request.author)
    await add_item(session, adv)
    return adv.id_dict


@app.patch("/api/v1/advertisement/{advertisement_id}", response_model=UpdateAdvResponse, tags=['advertisements'])
async def update_adv(session: SessionDependency, adv_id: int, adv_request: UpdateAdvRequest):
    adv_json = adv_request.model_dump(exclude_unset=True)
    adv = await get_item_by_id(session, Adv, adv_id)
    for field, value in adv_json.items():
        setattr(adv, field, value)
    await crud.add_item(session, adv)
    return adv.id_dict


@app.delete("/api/v1/advertisement/{advertisement_id}", response_model=DeleteAdvResponse, tags=['advertisements'])
async def delete_adv(session: SessionDependency, adv_id: int):
    adv = await get_item_by_id(session, Adv, adv_id)
    await crud.delete_item(session, adv)
    return STATUS_DELETED
