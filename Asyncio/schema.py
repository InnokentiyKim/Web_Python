from pydantic import BaseModel


class SwapiPeopleSchema(BaseModel):
    name: str
    birth_year: str | None = ""
    eye_color: str | None = ""
    films: str | None = ""
    gender: str | None = ""
    hair_color: str | None = ""
    height: str | int | None = ""
    mass: str | int | None = ""
    skin_color: str | None = ""
    homeworld: str | None = ""
    species: str | None = ""
    starships: str | None = ""
    vehicles: str | None = ""


def validate_json(json_data, schema_cls):
    schema_obj = schema_cls(**json_data)
    json_data_validated = schema_obj.dict(exclude_unset=True)
    return json_data_validated
