from datetime import datetime
from app.db import db


class Question(db.Model):
    """
    Model for questions
    """
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable = False)
    cover = db.Column(db.String(250), nullable = False)
    date_of_addition = db.Column(db.DateTime, default = datetime.now)
    options = db.relationship('Options', backref ='question', lazy='dynamic')

    def __init__(self, id, question, cover, date_of_addition, options):
        self.id = id
        self.question = question
        self.cover = cover
        self.date_of_addition= date_of_addition
        self.options = options

    def __repr__(self):
        return f'{self.question_id}, {self.question_content}', {self.options}