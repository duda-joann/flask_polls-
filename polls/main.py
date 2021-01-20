import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from polls.db import db

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'blebleble'
    login_manager.init_app(app)
    app.config.update(DATABASE=os.path.join(app.root_path, 'polls.db'))
    app.config['SECRET_KEY'] = 'secret-key-IS_the-lalale'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///polls.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    Bootstrap(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

