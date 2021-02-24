from app.db import db


class Options(db.Model):
    """
    Model for options
    """
    __tablename__ = "options"
    id = db.Column(db.Integer, primary_key = True)
    choice = db.Column(db.String(200))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    votes = db.relationship('Vote', backref='options', lazy='dynamic')

    def __init__(self, id, choice, question_id, votes):
        self.id = id
        self.choice = choice
        self.question_id = question_id
        self.votes = votes

    def __repr__(self):
        return f'{self.choice}, {self.votes}'