import flask
from flask import request, jsonify
from flask.views import MethodView
from models import Session, User
from sqlalchemy.exc import IntegrityError
import flask_bcrypt
from pydantic import ValidationError
from schema import CreateUser, UpdateUser


app = flask.Flask("user_app")
bcrypt = flask_bcrypt.Bcrypt(app)


def validate_json(json_data, schema_cls):
    try:
        schema_obj = schema_cls(**json_data)
        json_data_validated = schema_obj.dict(exclude_unset=True)
        return json_data_validated
    except ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop("ctx", None)
        raise HttpError(400, errors)
        
    


def hash_password(password: str) -> str:
    password_bytes = password.encode()
    password_hashed_bytes = bcrypt.generate_password_hash(password_bytes)
    password_hashed_str = password_hashed_bytes.decode()
    return password_hashed_str


class HttpError(Exception):
    
    def __init__(self, status_code: int, error_msg: str | dict):
        self.status_code = status_code
        self.error_msg = error_msg
        

@app.errorhandler(HttpError)
def error_handler(err: HttpError):
    http_response = jsonify({"error": err.error_msg})
    http_response.status_code = err.status_code
    return http_response


@app.before_request
def before_request():
    session = Session()
    request.session = session
    
    
@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response
        
        
def get_user_by_id(user_id: int):
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user


def add_user(user: User):
    request.session.add(user)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "user already exists")

        

class UserView(MethodView):
    
    def get(self, user_id: int):
        user = get_user_by_id(user_id)
        if user is None:
            http_response = jsonify({"error": "user not found"})
            http_response.status_code = 404
            return http_response
        return jsonify(user.dict)
    
    def post(self):
        json_data = validate_json(request.json, CreateUser)
        json_data["password"] = hash_password(json_data["password"])
        user = User(**json_data)
        add_user(user)
        return jsonify(user.id_dict)
        
    
    def patch(self, user_id: int):
        json_data = validate_json(request.json, UpdateUser)
        if "password" in json_data:
            json_data["password"] = hash_password(json_data["password"])
        user = get_user_by_id(user_id)
        for key, value in json_data.items():
            setattr(user, key, value)
        add_user(user)
        return jsonify(user.id_dict)
    
    def delete(self, user_id: int):
        user = get_user_by_id(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({"status": "deleted"})
    
user_view = UserView.as_view("users")

app.add_url_rule(
    "/user/<int:user_id>",
    view_func=user_view,
    methods=["GET", "PATCH", "DELETE"]
     
)

app.add_url_rule("/user", view_func=user_view, methods=["POST"])
app.run()