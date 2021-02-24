from datetime import datetime
from app.db import db


class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key= True)
    vote = db.Column(db.String)
    submitted = db.Column(db.DateTime, default = datetime.now)
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'))

    def __init__(self, id, vote, submitted, option_id):
        self.id = id
        self.vote = vote
        self.submitted = submitted
        self.option_id = option_id

    def __repr__(self):
        return f' {self.vote}, {self.submitted}'

