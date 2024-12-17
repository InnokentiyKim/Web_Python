from pydantic import BaseModel


class CreateAdv(BaseModel):
    title: str
    description: str
    owner: int


class UpdateAdv(BaseModel):
    title: str | None = None
    description: str | None = None
    owner: int | None = None
