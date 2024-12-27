from datetime import datetime
from pydantic import BaseModel
from typing import Literal


class IdResponseBase(BaseModel):
    id: int


class GetAdvResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    author: int
    created_at: datetime


class CreateAdvRequest(BaseModel):
    title: str
    description: str
    price: float
    author: int


class CreateAdvResponse(IdResponseBase):
    pass


class UpdateAdvRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None


class UpdateAdvResponse(IdResponseBase):
    pass


class StatusResponse(BaseModel):
    status: Literal['deleted']

class DeleteAdvResponse(StatusResponse):
    pass