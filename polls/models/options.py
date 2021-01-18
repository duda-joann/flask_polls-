from polls.db import db
from flask import (
                flash,
                redirect,
                url_for,
                request
                )
from .question import Question

class Options(db.Model):
    """
    Model for options
    """
    __tablename__ = "options"
    id = db.Column(db.Integer, primary_key = True)
    choice = db.Column(db.String(200))
    votes = db.Column(db.Integer, default=0)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __repr__(self):
        return f'{self.choice}, {self.votes}'


