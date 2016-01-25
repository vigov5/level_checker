from flask import Blueprint, render_template, flash, redirect, url_for, request, g, make_response, abort
from flask_login import login_user, logout_user, login_required
from flask_admin.contrib.sqla import ModelView

from app import app, db
from app.question.models import Question
from app.common.utils import send_email, generate_token

question_module = Blueprint('question', __name__)

class QuestionView(ModelView):
    # Disable model creation
    can_create = True

    column_filters = ['id', 'content', 'examination']

    # Override displayed fields
    column_list = ('content', 'examination', 'correct_id')

    form_excluded_columns = ('answers')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(QuestionView, self).__init__(Question, session, **kwargs)

    def is_accessible(self):
        return g.user.is_authenticated() and g.user.is_admin()
