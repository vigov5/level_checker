from flask import Blueprint, g, render_template
from flask_login import login_required
from flask_admin.contrib.sqla import ModelView

from app.result.models import Result
from app.result import constants as RESULT


result_module = Blueprint('result', __name__)


@result_module.route('/<int:result_id>', methods=['GET'])
@login_required
def show(result_id=0):
    result = Result.query.get_or_404(result_id)

    return render_template('result/show.html', result=result)

class ResultView(ModelView):
    # Disable model creation
    can_create = True

    # Override displayed fields
    column_list = ('id', 'user', 'examination', 'status', 'score')
    column_filters = ('id', 'user', 'examination', 'status', 'score')

    column_choices = {
        'status': RESULT.STATUS.items()
    }

    form_choices = {
        'status': [(str(k), v) for k,v in RESULT.STATUS.items()]
    }

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(ResultView, self).__init__(Result, session, **kwargs)

    def is_accessible(self):
        return g.user.is_authenticated() and g.user.is_admin()
