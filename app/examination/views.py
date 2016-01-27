import datetime

from flask import Blueprint, render_template, flash, redirect, url_for, g, session, request
from flask_login import login_required
from flask_admin.contrib.sqla import ModelView

from app import app, db
from app.result.models import Result
from app.result import constants as RESULT
from app.question.models import Question
from app.examination.models import Examination
from app.examination.forms import DoExaminationForm

examination_module = Blueprint('examination', __name__)

@examination_module.route('/<int:examination_id>/do', methods=['GET', 'POST'])
@login_required
def do_examination(examination_id=0):
    examination = Examination.query.get_or_404(examination_id)
    result = g.user.results.filter_by(examination_id=examination.id).first()
    uid = 'u-%d-e-%d' % (g.user.id, examination.id)

    if result and result.is_finished():
        session.pop(uid, None)
        return redirect(url_for('result.show', result_id=result.id))

    start_time = None
    if uid in session:
        start_time = session[uid]
        if datetime.datetime.now() > session[uid] + datetime.timedelta(minutes=examination.limited_time, seconds=30):
            session.pop(uid, None)
            result = g.user.results.filter_by(examination_id=examination.id).first()
            if result:
                if result.is_doing():
                    result.status =  RESULT.STATUS_FINISHED
                    db.session.add(result)
                    db.session.commit()
                return redirect(url_for('result.show', result_id=result.id))
            else:
                flash('Error !', category='danger')
                return redirect(url_for('index'))
    else:
        result = Result(g.user, examination, 0)
        db.session.add(result)
        db.session.commit()
        session[uid] = datetime.datetime.now()

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
            if examination.questions.filter_by(id=int(entry['question_id'])).first().correct_id == int(entry['answers']):
                correct += 1
    else:
        for entry in form.questions.data:
            if entry['answers'].isdigit() and examination.questions.filter_by(id=int(entry['question_id'])).first().correct_id == int(entry['answers']):
                correct += 1

    result = Result.query.filter_by(user_id=g.user.id, examination_id=examination.id).first()
    if result and request.method == 'POST':
        result.score = correct
        result.status = RESULT.STATUS_FINISHED
        db.session.add(result)
        db.session.commit()

        return redirect(url_for('result.show', result_id=result.id))

    remain = examination.limited_time * 60
    if start_time:
        remain = examination.limited_time - (datetime.datetime.now() - start_time).seconds

    return render_template('examination/do_examination.html', form=form, examination=examination, remain=remain)

class ExaminationView(ModelView):
    # Disable model creation
    can_create = True

    form_excluded_columns = ('questions', 'results')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(ExaminationView, self).__init__(Examination, session, **kwargs)

    def is_accessible(self):
        return g.user.is_authenticated() and g.user.is_admin()
