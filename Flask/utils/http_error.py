
class HttpError(Exception):
    def __init__(self, status_code: int, err_message: str | dict):
        self.status_code = status_code
        self.err_message = err_message