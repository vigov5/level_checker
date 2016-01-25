from flask import Blueprint, render_template, request, g, send_from_directory, abort, jsonify, url_for
from flask_login import current_user, login_required
from sqlalchemy import desc, asc

from app import app, db, lm
from app.common.utils import compute_sign_hash, admin_required
from app.user.models import User

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'common/index.html',
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/uploads/<path:filename>')
def download_file(filename):
    if '..' in filename or filename.startswith('/'):
        abort(404)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
