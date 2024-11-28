import flask
from flask import jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from models_new import Session, Adv, User


app = flask.Flask("advs_app")


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
        adv = Adv(**request.json)
        add_adv(adv)
        return jsonify(adv.id_dict)
    
    def patch(self, adv_id: int):
        json_data = request.json
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
    
    
adv_view = AdvView.as_view("advs")

app.add_url_rule(rule="/adv/<int:adv_id", view_func=adv_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule(rule="/adv", view_func=adv_view, methods=['POST'])

app.run()
    