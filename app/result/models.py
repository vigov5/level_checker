import datetime

from app import db
from app.result import constants as RESULT

class Result(db.Model):

    __tablename__ = ''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    examination_id = db.Column(db.Integer, db.ForeignKey('examinations.id'))
    score = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now)

    def __init__(self, user, examination, score):
        self.user = user
        self.examination = examination
        self.score = score
        self.status = RESULT.STATUS_DOING

    def is_doing(self):
        return self.status == RESULT.STATUS_DOING

    def is_finished(self):
        return self.status == RESULT.STATUS_FINISHED

    def __repr__(self):
        return '<Result %r %r %r>' % (self.user, self.examination, self.score)

    def __str__(self):
        return self.content
