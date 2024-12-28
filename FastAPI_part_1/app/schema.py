from datetime import datetime
from pydantic import BaseModel
from typing import Literal


class IdResponseBase(BaseModel):
    id: int

class StatusResponse(BaseModel):
    status: Literal['deleted']


class GetUserResponse(BaseModel):
    id: int
    name: str
    registered_at: datetime


class CreateUserRequest(BaseModel):
    name: str
    password: str


class CreateUserResponse(IdResponseBase):
    pass


class UpdateUserRequest(BaseModel):
    name: str | None = None
    password: str | None = None


class UpdateUserResponse(IdResponseBase):
    pass


class DeleteUserResponse(StatusResponse):
    pass


class GetAdvSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    author: int | None = None
    created_at: datetime | None = None


class GetAdvResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    author: int
    created_at: str


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


class DeleteAdvResponse(StatusResponse):
    pass