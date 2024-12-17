from pydantic import BaseModel, field_validator


class BaseUser(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def check_password_length(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        return value


class CreateUser(BaseUser):
    name: str
    password: str


class UpdateUser(BaseUser):
    name: str | None = None
    password: str | None = None
