from flask_wtf import Form
from wtforms import TextField, SubmitField, validators, IntegerField, BooleanField, FormField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms_alchemy import model_form_factory

from app.answer.models import Answer

ModelForm = model_form_factory(Form)

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
