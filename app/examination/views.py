from flask import Blueprint, render_template, flash, redirect, url_for, request, g, make_response, abort
from flask_login import login_user, logout_user, login_required
from flask_admin.contrib.sqla import ModelView

from app import app, db
from app.question.models import Question
from app.examination.models import Examination
from app.examination.forms import DoExaminationForm
from app.common.utils import send_email, generate_token

examination_module = Blueprint('examination', __name__)

@examination_module.route('/<int:examination_id>/do', methods=['GET', 'POST'])
@login_required
def do_examination(examination_id=0):
    examination = Examination.query.get_or_404(examination_id)
    form = DoExaminationForm(obj=examination)
    counter = 0
    for sub_form in form.questions:
        sub_form.answers.choices = [(str(answer.id), answer.content) for answer in examination.questions[counter].answers]
        sub_form.question_id.data = examination.questions[counter].id
        sub_form.answers.label.text = examination.questions[counter].content
        counter += 1

    correct = 0
    if form.validate_on_submit():
        for entry in form.questions.data:
            if Question.query.get_or_404(int(entry['question_id'])).correct_id == int(entry['answers']):
                correct += 1
        flash('Correct %d' % correct)

        return redirect(url_for('examination.do_examination', examination_id=examination.id))

    return render_template('examination/do_examination.html', form=form, examination=examination)

class ExaminationView(ModelView):
    # Disable model creation
    can_create = True

    form_excluded_columns = ('questions')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(ExaminationView, self).__init__(Examination, session, **kwargs)

    def is_accessible(self):
        return g.user.is_authenticated() and g.user.is_admin()
