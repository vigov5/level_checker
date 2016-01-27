from flask import render_template, g, send_from_directory, abort
from flask_login import current_user, login_required

from app import app, lm
from app.user.models import User
from app.examination.models import Examination
from app.common.utils import admin_required


@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/admin')
def admin():
    examinations = Examination.query.all()

    return render_template(
        'common/admin.html',
        examinations=examinations
    )

@app.route('/index')
@login_required
def index():
    examinations = Examination.query.all()

    return render_template(
        'common/index.html',
        examinations=examinations
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/uploads/<path:filename>')
def download_file(filename):
    if '..' in filename or filename.startswith('/'):
        abort(404)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
