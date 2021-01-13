import os

from flask import Flask
from flask_login import LoginManager

from polls.db import db

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'blebleble'
    login_manager.init_app(app)
    app.config.update(DATABASE=os.path.join(app.root_path, 'artists.db'))
    app.config['SECRET_KEY'] = 'secret-key-IS_the-lalale'
    app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///artists.db"
    with app.app_context():
        db.init_app(app)
    return app

