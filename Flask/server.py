import flask
from flask import request, jsonify
from flask.views import MethodView
from models import Session, User


app = flask.Flask("user_app")

class UserView(MethodView):
    
    def get(self, user_id: int):
        with Session() as session:
            user = session.get(User, user_id)
            return jsonify(user.dict)
    
    def post(self):
        json_data = request.json
        with Session as session:
            user = User(**json_data)
            session.add(user)
            session.commit()
            return jsonify(user.id_dict)
        
        
    
    def patch(self, user_id: int):
        json_data = request.json
        with Session() as session:
            user = session.get(User, user_id)
            for key, value in json_data.items():
                setattr(user, key, value)
            session.add(user)
            session.commit()
            return jsonify(user.id_dict)
    
    def delete(self, user_id: int):
        with Session() as session:
            user = session.get(User, user_id)
            session.delete(user)
            session.commit()
        return jsonify({"status": "deleted"})
    
user_view = UserView.as_view("users")

app.add_url_rule(
    "user/<int:user_id>",
    view_func=user_view,
    methods=["GET", "PATCH", "DELETE"]
     
)

app.add_url_rule("user", view_func=user_view, methods=["POST"])
app.run()