from flask import Blueprint, g
from flask_admin.contrib.sqla import ModelView

from app.answer.models import Answer


answer_module = Blueprint('answer', __name__)

class AnswerView(ModelView):
    # Disable model creation
    can_create = True

    # Override displayed fields
    column_list = ('id', 'content', 'question', 'question.examination')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(AnswerView, self).__init__(Answer, session, **kwargs)

    def is_accessible(self):
        return g.user.is_authenticated() and g.user.is_admin()
