from datetime import datetime
from app.db import db


class Vote(db.Model):
    __tablename__ = 'vote'
    id = db.Column(db.Integer, primary_key= True)
    vote = db.Column(db.Integer, default=0)
    submitted = db.Column(db.DateTime, default = datetime.now)
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'))

    def __repr__(self):
        return f'{self.id}, {self.vote}, {self.submitted}, {self.option_id}'

