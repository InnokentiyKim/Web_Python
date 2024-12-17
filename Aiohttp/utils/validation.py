from aiohttp.web import HTTPBadRequest
from pydantic import ValidationError

from utils.errors import generate_error


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
