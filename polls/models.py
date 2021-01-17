from datetime import datetime
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


class Question(db.Model):
    """
    Model for questions
    """
    __tablename__ = "question"
    question_id = db.Column(db.Integer, primary_key=True)
    question_content = db.Column(db.String(200), nullable = False)
    date_of_addition = db.Column(db.DateTime(default = datetime.now()))

    def __repr__(self):
        return f'{self.question_id}, {self.question_content}'


class Options(db.Model):
    """
    Model for options
    """
    __tablename__ = "options"
    question = db.ForeignKey(Question)
    choice = db.Column(db.String(200))
    votes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'{self.choice}'
