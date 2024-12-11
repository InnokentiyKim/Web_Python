from pydantic import BaseModel, Field
from typing import Optional


class SwapiPeopleSchema(BaseModel):
    name: str
    birth_year: str | None = Field(default="")
    eye_color: str | None = Field(default="")
    gender: str | None = Field(default="")
    hair_color: str | None = Field(default="")
    height: str | int | None = Field(default="")
    mass: str | int | None = Field(default="")
    skin_color: str | None = Field(default="")
    films: Optional[str] | list | list[str] | list | None = Field(default="")
    homeworld: Optional[str] | None = Field(default="")
    species: Optional[str] | list | list[str] | None = Field(default="")
    starships: Optional[str] | list | list[str] | None = Field(default="")
    vehicles: Optional[str] | list | list[str] | None = Field(default="")


def validate_json(json_data, schema_cls):
    schema_obj = schema_cls(**json_data)
    json_data_validated = schema_obj.dict(exclude_unset=True)
    return json_data_validated
