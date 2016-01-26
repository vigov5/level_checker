import hashlib
import datetime
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from sqlalchemy.orm import backref

from app import db
from app.answer import constants as ANSWER


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
