from pydantic import BaseModel, field_validator


class CreateAdv(BaseModel):
    title: str
    description: str


class UpdateAdv(BaseModel):
    title: str | None = None
    description: str | None = None


class BaseUser(BaseModel):
    password: str
    
    @field_validator("password")
    @classmethod
    def check_password(cls, value: str):
        if len(value) < 8:
            raise ValueError("Your password is too short")
        return value
    

class CreateUser(BaseUser):
    name: str
    email: str | None = None
    password: str
    
    
class UpdateUser(BaseUser):
    name: str | None = None
    email: str | None = None
    password: str | None = None
        