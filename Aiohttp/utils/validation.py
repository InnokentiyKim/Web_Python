from pydantic import ValidationError
from errors import generate_error
from aiohttp.web import HTTPBadRequest


def validate(json_data, schema_cls):
    try:
        schema_obj = schema_cls(**json_data)
        json_data_validated = schema_obj.dict(exclude_unset=True)
        return json_data_validated
    except ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop("ctx", None)
        raise generate_error(HTTPBadRequest, errors)
