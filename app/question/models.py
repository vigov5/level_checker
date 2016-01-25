import hashlib
import datetime
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from sqlalchemy.orm import backref

from app import db
from app.question import constants as QUESTION


class Question(db.Model):

    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False, default='')
    correct_id = db.Column(db.Integer)
    examination_id = db.Column(db.Integer, db.ForeignKey('examinations.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now)

    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    # def __init__(self, content, correct_id):
    #     self.content = content
    #     self.correct_id = correct_id

    def __repr__(self):
        return '<Question %r>' % self.self.content[:20]

    def __str__(self):
        return self.content[:20]
