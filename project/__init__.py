from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baruga.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webRtc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'kajan-drink-beer'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from project import models, routes, camera