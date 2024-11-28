import flask
from flask import request
from flask.views import MethodView
from models_new import Session, Adv, User


app = flask.Flask("advs_app")


@app.before_request
def before_request():
    session = Session()
    request.session = session
    

@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response


class AdvView(MethodView):
    
    def get(self, adv_id: int):
        pass
    
    def post(self):
        pass
    
    def patch(self, adv_id: int):
        pass
    
    def delete(self, adv_id: int):
        pass
    