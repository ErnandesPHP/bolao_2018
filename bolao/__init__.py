from os import environ
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from . import views

app = Flask(__name__, static_url_path = "", static_folder = "static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/bolao2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(
    SECRET_KEY="x34sdfm34",
    )

for config in (
    "GOOGLE_LOGIN_CLIENT_ID",
    "GOOGLE_LOGIN_CLIENT_SECRET",
    "LINKEDIN_LOGIN_CLIENT_ID",
    "LINKEDIN_LOGIN_CLIENT_SECRET",
    "FACEBOOK_LOGIN_CLIENT_ID",
    "FACEBOOK_LOGIN_CLIENT_SECRET"

):
  app.config[config] = environ[config]

db = SQLAlchemy(app)
@app.before_request
def before_request():
    db.drop_all()
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"

from bolao.views import bolao
from . import views

app.register_blueprint(bolao)
