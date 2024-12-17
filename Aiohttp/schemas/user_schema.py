from pydantic import BaseModel


class CreareUser(BaseModel):
    name: str
    password: str


class UpdateUser(BaseModel):
    name: str | None = None
    password: str | None = None
