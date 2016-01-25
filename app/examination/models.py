import hashlib
import datetime
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from sqlalchemy.orm import backref

from app import db
from app.examination import constants as EXAMINATION


class Examination(db.Model):

    __tablename__ = 'examinations'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, default='')
    limited_time = db.Column(db.Integer, default=15)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now)

    questions = db.relationship('Question', backref='examination', lazy='dynamic')

    def __init__(self, title, limited_time=15):
        self.title = title
        self.limited_time = limited_time

    def __repr__(self):
        return '<Examination %r>' % self.self.title

    def __str__(self):
        return self.title
