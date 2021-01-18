from flask_login import UserMixin
from polls.db import db


class Admin(UserMixin, db.Model):
    """Admin Model
    model for user admin models, user is allowed to add a question to poll
    """

    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    mail = db.Column(db.String(40), unique=True, nullable = False)
    password = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'{self.id}, {self.username}, {self.mail}, {self.password}'