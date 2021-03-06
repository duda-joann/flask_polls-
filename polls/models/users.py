from datetime import datetime

from flask_login import UserMixin
from app.db import db


class Users(UserMixin, db.Model):
    """Admin Model
    model for user admin models, user is allowed to add a question to poll
    """

    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    mail = db.Column(db.String(40), unique=True, nullable = False)
    password = db.Column(db.String(), nullable=False)
    confirmed = db.Column(db.Boolean(), nullable = False, default=False)
    confimed_on = db.Column(db.DateTime(), default = datetime.now())

    def __repr__(self):
        return f'{self.id}, {self.username}, {self.mail}, {self.password}'