from flask.views import MethodView
from flask import g, request, jsonify
from models import User
from schema import CreateUser, UpdateUser
from utils.http_error import HttpError
from utils.validation import validate_json
from utils.verification import hash_password, is_owner_or_raise_error
from database import get_user_by_id, add_user
from app_base import auth


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
    
    @auth.login_required
    def patch(self, user_id: int):
        is_owner_or_raise_error(user_id=g.user.id, owner_id=user_id)
        json_data = validate_json(request.json, UpdateUser)
        if "password" in json_data:
            json_data["password"] = hash_password(json_data["password"])
        user = get_user_by_id(user_id)
        for key, value in json_data.items():
            setattr(user, key, value)
        add_user(user)
        return jsonify(user.id_dict)
    
    @auth.login_required
    def delete(self, user_id: int):
        user = get_user_by_id(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({"status": "deleted"})
    