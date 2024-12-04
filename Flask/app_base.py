import flask
import flask_bcrypt
from flask_httpauth import HTTPBasicAuth


app = flask.Flask("advs_app")
bcrypt = flask_bcrypt.Bcrypt(app)
auth = HTTPBasicAuth()