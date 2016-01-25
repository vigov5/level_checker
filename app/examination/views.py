from flask import Blueprint, render_template, flash, redirect, url_for, request, g, make_response, abort
from flask_login import login_user, logout_user, login_required
from flask_admin.contrib.sqla import ModelView

from app import app, db
from app.examination.models import Examination
from app.common.utils import send_email, generate_token

examination_module = Blueprint('examination', __name__)

class ExaminationView(ModelView):
    # Disable model creation
    can_create = True

    form_excluded_columns = ('questions')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(ExaminationView, self).__init__(Examination, session, **kwargs)

    def is_accessible(self):
        return g.user.is_authenticated() and g.user.is_admin()
