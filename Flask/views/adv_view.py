import flask
from flask.views import MethodView
from flask import request, jsonify, g
from database import get_adv_by_id, add_adv
from models import Adv
from utils.http_error import HttpError
from utils.validation import validate_json
from schema import CreateAdv, UpdateAdv
from sqlalchemy import select
from app_base import auth
from utils.verification import is_owner_or_raise_error


class AdvView(MethodView):
    
    def get(self, adv_id: int):
        adv = get_adv_by_id(adv_id)
        return jsonify(adv.dict)
   
    @auth.login_required
    def post(self):
        json_data = validate_json(request.json, CreateAdv)
        adv = Adv(**json_data)
        adv.owner = g.user.id
        add_adv(adv)
        return jsonify(adv.id_dict)
    

    @auth.login_required
    def patch(self, adv_id: int) -> flask.Response:
        json_data = validate_json(request.json, UpdateAdv)
        adv = get_adv_by_id(adv_id)
        is_owner_or_raise_error(user_id=g.user.id, owner_id=adv.owner)
        if "owner" in json_data:
            raise HttpError(status_code=400, err_message="Owner field can't be changed")
        for key, value in json_data.items():
            setattr(adv, key, value)
        add_adv(adv)
        return jsonify(adv.id_dict)

        
    @auth.login_required
    def delete(self, adv_id: int):
        adv = get_adv_by_id(adv_id)
        is_owner_or_raise_error(user_id=g.user.id, owner_id=adv.owner)
        request.session.delete(adv)
        request.session.commit()
        return jsonify({"status": "deleted"})
    

class AdvListView(MethodView):
    
    def get(self):
        advs = request.session.scalars(select(Adv)).all()
        return jsonify([adv.dict for adv in advs])
    