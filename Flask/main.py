import flask
from flask import jsonify, request
from app_base import app
from database import Session
from utils.http_error import HttpError
from views.adv_view import AdvListView, AdvView
from views.user_view import UserView

        
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

adv_view = AdvView.as_view("advs")
user_view = UserView.as_view("users")
advs_list_view = AdvListView.as_view("advs_list")

app.add_url_rule(rule="/api/adv", view_func=advs_list_view, methods=['GET'])

app.add_url_rule(rule="/api/adv/<int:adv_id>", view_func=adv_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule(rule="/api/adv", view_func=adv_view, methods=['POST'])

app.add_url_rule(rule="/api/user/<int:user_id>", view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule(rule="/api/user", view_func=user_view, methods=['POST'])

app.run(host="127.0.0.1", port=5000)
    