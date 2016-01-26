from flask_wtf import Form
from wtforms import TextField, SubmitField, validators, IntegerField, BooleanField, FormField, SelectField, FieldList, RadioField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms_alchemy import model_form_factory

from app.question.models import Question
from app.examination.models import Examination
from app.answer.forms import AnswerForm

ModelForm = model_form_factory(Form)


def exam_query():
    return Examination.query.all()


class CreateQuestionForm(Form):
    content = TextField('Content',  [
        validators.Required('Please enter question content.'),
    ])
    examination = QuerySelectField(query_factory=exam_query, get_label='title')
    correct_id = SelectField('Correct Answer', choices=[(str(k), v) for k, v in [(1, 1), (2, 2), (3, 3), (4, 4)]])
    answers = FieldList(FormField(AnswerForm), min_entries=4)
    submit = SubmitField('Create question')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class AnswerQuestionForm(Form):
    answers = RadioField('Answer', choices=[])
    question_id = HiddenField('question_id')


class QuestionForm(ModelForm):
    class Meta:
        model = Question

    content = QuerySelectField(query_factory=exam_query, get_label='title')
