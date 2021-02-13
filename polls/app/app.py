import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from .db import db
from my_secrets import User, Password

login_manager = LoginManager()

base_dir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(base_dir, 'uploads')


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = 'blebleble'
    login_manager.init_app(app)
    app.config.update(DATABASE=os.path.join(app.root_path, 'polls.db'))
    app.config['SECRET_KEY'] = 'secret-key-IS_the-lalale'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///polls.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECURITY_PASSWORD_SALT'] = 'VanillaSkinDelight'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = User
    app.config['MAIL_PASSWORD'] = Password
    app.config['MAIL_DEFAULT_SENDER'] = User
    app.static_folder = 'static'
    Bootstrap(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

app = create_app()
from app import routes