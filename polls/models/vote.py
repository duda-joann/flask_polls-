from datetime import datetime
from app.db import db


class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key= True)
    vote = db.Column(db.String)
    submitted = db.Column(db.DateTime, default = datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __repr__(self):
        return f' {self.vote}, {self.submitted}'

