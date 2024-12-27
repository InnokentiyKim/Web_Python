from fastapi import FastAPI

from crud_new import add_item, get_item_by_id
from lifespan_new import lifespan
from dependency_new import SessionDependency
from models_new import User, Adv
from schema import (GetAdvResponse, CreateAdvRequest, CreateAdvResponse,
                    UpdateAdvRequest, UpdateAdvResponse, DeleteAdvResponse)
import crud_new


app = FastAPI(
    title="Advertisements",
    description="Advertisements app",
    lifespan=lifespan,
)


@app.get("/api/v1/adv/{adv_id}", response_model=GetAdvResponse, tags=['advertisements'])
async def get_adv(session: SessionDependency, adv_id: int):
    adv = crud_new.get_item_by_id(session, Adv, adv_id)
    return adv.dict


@app.post("/api/v1/adv", response_model=CreateAdvResponse, tags=['advertisements'])
async def create_adv(session: SessionDependency, adv_request: CreateAdvRequest):
    adv = Adv(title=adv_request.title, description=adv_request.description,
              price=adv_request.price, author=adv_request.author)
    await add_item(session, adv)
    return adv.id_dict


@app.patch("/api/v1/adv/{adv_id}", response_model=UpdateAdvResponse, tags=['advertisements'])
async def update_adv(session: SessionDependency, adv_id: int, adv_request: UpdateAdvRequest):
    adv_json = adv_request.model_dump(exclude_unset=True)
    adv = await get_item_by_id(session, Adv, adv_id)
    for field, value in adv_json.items():
        setattr(adv, field, value)
    await crud_new.add_item(session, adv)
    return adv.id_dict



