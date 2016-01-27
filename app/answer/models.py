import datetime

from app import db


class Answer(db.Model):

    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now)

    def __init__(self, content):
         self.content = content

    def __repr__(self):
        return '<Answer %r>' % self.self.content

    def __str__(self):
        return self.content
