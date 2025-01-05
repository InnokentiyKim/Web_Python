from http.client import HTTPException
from fastapi import FastAPI, Query
from typing import Optional
from datetime import datetime

from sqlalchemy import select
import auth
import crud
from constants import STATUS_DELETED
from crud import add_item, get_item_by_id
from lifespan import lifespan
from dependency import SessionDependency
from models import User, Adv, Token
from schema import (GetAdvResponse, CreateAdvRequest, CreateAdvResponse, UpdateAdvRequest,
                    UpdateAdvResponse, DeleteAdvResponse, GetUserResponse, CreateUserRequest,
                    CreateUserResponse, UpdateUserRequest, UpdateUserResponse, DeleteUserResponse,
                    GetAdvSchema, LoginResponse, LoginRequest)


app = FastAPI(
    title="Advertisements",
    description="Advertisements app",
    lifespan=lifespan,
)


@app.get("/api/v1/user/{user_id}", response_model=GetUserResponse, tags=["user"])
async def get_user(session: SessionDependency, user_id: int):
    user = await crud.get_item_by_id(session, User, user_id)
    return user.dict


@app.post("/api/v1/user", response_model=CreateUserResponse, tags=["user"])
async def create_user(session: SessionDependency, user_request: CreateUserRequest):
    user = User(name=user_request.name, password=user_request.password)
    await add_item(session, user)
    return user.id_dict


@app.patch("/api/v1/user/{user_id}", response_model=UpdateUserResponse, tags=["user"])
async def update_user(session: SessionDependency, user_request: UpdateUserRequest, user_id: int):
    user_json = user_request.model_dump(exclude_unset=True)
    user = await get_item_by_id(session, User, user_id)
    for field, value in user_json.items():
        setattr(user, field, value)
    await add_item(session, user)
    return user.id_dict


@app.delete("/api/v1/user/{user_id}", response_model=DeleteUserResponse, tags=["user"])
async def delete_user(session: SessionDependency, user_id: int):
    user = await get_item_by_id(session, User, user_id)
    await crud.delete_item(session, user)
    return STATUS_DELETED


@app.post("/api/v1/login", response_model=LoginResponse, tags=["user"])
async def login(session: SessionDependency, login_request: LoginRequest):
    user_query = select(User).where(User.name == login_request.name)
    user = await session.scalar(user_query)
    if user is None:
        raise HTTPException(401, "Username or password is incorrect")
    if not auth.check_password(login_request.password, user.password):
        raise HTTPException(401, "Username or password is incorrect")
    token = Token(user_id=user.id)
    await crud.add_item(session, token)
    return token.dict


@app.get("/api/v1/advertisement/{advertisement_id}", response_model=GetAdvResponse, tags=["advertisement"])
async def get_adv(session: SessionDependency, advertisement_id: int):
    adv = await crud.get_item_by_id(session, Adv, advertisement_id)
    return adv.dict


@app.get("/api/v1/advertisement", response_model=list[GetAdvResponse], tags=["advertisement"])
async def get_adv_by_params(
        session: SessionDependency, title: Optional[str] = None, description: Optional[str] = None,
        price: Optional[float] = Query(default=None, ge=0), author: Optional[int] = None,
        created_at: Optional[datetime] = None
):
    params = GetAdvSchema(title=title, description=description, price=price,
                          author=author, created_at=created_at).model_dump(exclude_unset=True, exclude_none=True)
    advs = await crud.get_adv_by_params(session, params)
    return [adv.dict for adv in advs]


@app.post("/api/v1/advertisement", response_model=CreateAdvResponse, tags=["advertisement"])
async def create_adv(session: SessionDependency, adv_request: CreateAdvRequest):
    adv = Adv(title=adv_request.title, description=adv_request.description,
              price=adv_request.price, author=adv_request.author)
    await add_item(session, adv)
    return adv.id_dict


@app.patch("/api/v1/advertisement/{advertisement_id}", response_model=UpdateAdvResponse, tags=["advertisement"])
async def update_adv(session: SessionDependency, advertisement_id: int, adv_request: UpdateAdvRequest):
    adv_json = adv_request.model_dump(exclude_unset=True)
    adv = await get_item_by_id(session, Adv, advertisement_id)
    for field, value in adv_json.items():
        setattr(adv, field, value)
    await crud.add_item(session, adv)
    return adv.id_dict


@app.delete("/api/v1/advertisement/{advertisement_id}", response_model=DeleteAdvResponse, tags=["advertisement"])
async def delete_adv(session: SessionDependency, advertisement_id: int):
    adv = await get_item_by_id(session, Adv, advertisement_id)
    await crud.delete_item(session, adv)
    return STATUS_DELETED
