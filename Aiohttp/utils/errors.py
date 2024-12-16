import json


def generate_error(error_cls, message):
    error = error_cls(
        text=json.dumps({"error": message}), content_type="application/json"
    )
    return error
