from flask import Blueprint, render_template, flash, redirect, url_for, g
from flask_login import login_required
from flask_admin.contrib.sqla import ModelView

from app import db
from app.question.models import Question
from app.answer.models import Answer
from app.question.forms import CreateQuestionForm
from app.common.utils import admin_required


question_module = Blueprint('question', __name__)


@question_module.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    form = CreateQuestionForm()
    if form.validate_on_submit():
        flash('Question created successfully.', category='success')
        correct_id =  int(form.correct_id.data)
        question = Question(form.content.data, correct_id)
        db.session.add(question)
        question.examination = form.examination.data
        choices = []
        for answer in form.answers:
            ans = Answer(answer.content.data)
            ans.question = question
            choices.append(ans)
            db.session.add(ans)
        db.session.commit()
        for index, answer in enumerate(choices):
            if index+1 == correct_id:
                question.correct_id = answer.id
                break
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('question/create_question.html', form=form)


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
