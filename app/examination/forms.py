from flask_wtf import Form
from wtforms import TextField, SubmitField, validators, PasswordField, HiddenField, FormField, FieldList
from wtforms_alchemy import model_form_factory

from app.question.forms import AnswerQuestionForm

ModelForm = model_form_factory(Form)


class DoExaminationForm(Form):
    questions = FieldList(FormField(AnswerQuestionForm))
