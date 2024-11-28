import flask
import flask_bcrypt
from flask import jsonify, request
from flask.views import MethodView
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from models_new import Session, Adv, User
from schema_new import CreateAdv, CreateUser, UpdateAdv, UpdateUser


app = flask.Flask("advs_app")
bcrypt = flask_bcrypt.Bcrypt(app)


def hash_password(password: str) -> str:
    password_bytes = password.encode()
    password_hashed_bytes = bcrypt.generate_password_hash(password_bytes)
    password_hashed_string = password_hashed_bytes.decode()
    return password_hashed_string


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
        

class HttpError(Exception):
    def __init__(self, status_code: int, err_message: str | dict):
        self.status_code = status_code
        self.err_message = err_message
        

@app.errorhandler(HttpError)
def error_handler(err: HttpError):
    http_response = jsonify({"error": err.err_message})
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


def get_adv_by_id(adv_id: int):
    adv = request.session.get(Adv, adv_id)
    if not adv:
        raise HttpError(status_code=404, err_message="advertisement not found")
    return adv


def get_user_by_id(user_id: int):
    user = request.session.get(User, user_id)
    if not user:
        raise HttpError(status_code=404, err_message="user not found")
    return user


def add_adv(adv: Adv):
    request.session.add(adv)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(status_code=409, err_message="advertisement already exists")
    
    
def add_user(user: User):
    request.session.add(user)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(status_code=409, err_message="user already exists")


class AdvView(MethodView):
    
    def get(self, adv_id: int):
        adv = get_adv_by_id(adv_id)
        return jsonify(adv.dict)
    
    def post(self):
        json_data = validate_json(request.json, CreateAdv)
        adv = Adv(**json_data)
        add_adv(adv)
        return jsonify(adv.id_dict)
    
    def patch(self, adv_id: int):
        json_data = validate_json(request.json, UpdateAdv)
        adv = get_adv_by_id(adv_id)
        for key, value in json_data.items():
            setattr(adv, key, value)
        add_adv(adv)
        return jsonify(adv.id_dict)
        
    
    def delete(self, adv_id: int):
        adv = get_adv_by_id(adv_id)
        request.session.delete(adv)
        request.session.commit()
        return jsonify({"status": "deleted"})
    
    
class UserView(MethodView):
    
    def get(self, user_id: int):
        user = get_user_by_id(user_id)
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
    
    
adv_view = AdvView.as_view("advs")
user_view = UserView.as_view("users")

app.add_url_rule(rule="/api/adv/<int:adv_id", view_func=adv_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule(rule="/api/adv", view_func=adv_view, methods=['POST'])

app.add_url_rule(rule="/api/user/<int:user_id", view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule(rule="/api/user", view_func=user_view, methods=['POST'])

app.run()
    