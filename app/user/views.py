from flask import Blueprint, render_template, flash, redirect, url_for, request, g, make_response, abort
from flask_login import login_user, logout_user, login_required
from flask_admin.contrib.sqla import ModelView

from app import app, db
from app.user.forms import LoginForm, SignupForm, UserForm, ChangePasswordForm, SendForgotPasswordForm, ResetPasswordForm, ResendMailForm
from app.user.models import User, UserForgotPassword, UserMailActivation
from app.common.utils import send_email, generate_token

user_module = Blueprint('user', __name__)


@user_module.route('/signup', methods=['GET', 'POST'])
def signup():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))

    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(form.username.data, form.email.data, form.password.data)
        mail_activation = UserMailActivation(new_user)

        db.session.add(new_user)
        db.session.add(mail_activation)
        db.session.commit()

        result, message = send_email(
            'Framgia Level Checker - Account Confirmation',
            app.config['MAIL_SENDERS']['admin'],
            [new_user.email],
            'confirm_activation',
            dict(token=mail_activation.token)
        )
        if not result:
            form.email.errors.append('Error: ' + message)
        else:
            return render_template('user/confirm_mail_sent.html', user=new_user)

    return render_template('user/signup.html', form=form)


@user_module.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash('Logged in successfully.', category='success')
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('user/login.html', form=form)


@user_module.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', category='success')
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('ss_sign')
    return redirect(url_for('index'))


@user_module.route('/profile', methods=['GET', 'POST'])
@user_module.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id=None):
    if user_id is None or user_id == g.user.id:
        return render_template('user/profile.html', user=g.user)
    else:
        user = User.query.get_or_404(user_id)
        return render_template('user/profile.html', user=user)


@user_module.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    model = User.query.get(g.user.id)
    form = UserForm(obj=model)

    if form.validate_on_submit():
        form.populate_obj(model)
        db.session.add(model)
        db.session.commit()
        flash('Profile updated', category='success')
        return redirect(url_for('user.profile'))
    return render_template('user/edit_profile.html', user=g.user, form=form)


@user_module.route('/change_password/<int:user_id>', methods=['GET', 'POST'])
@login_required
def change_password(user_id=None):
    if g.user.is_admin():
        user = User.query.get_or_404(user_id)
    else:
        user = User.query.get(g.user.id)
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.add(user)
        db.session.commit()
        flash('Password changed successfully.', category='success')
        return redirect(url_for('user.profile', user_id=user.id))
    return render_template('user/change_password.html', user=user, form=form)


@user_module.route('/password/forgot', methods=['GET', 'POST'])
def forgot_password():
    form = SendForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        user_forgot_password = UserForgotPassword.query.filter_by(user_id=user.id).first()
        if not user_forgot_password:
            user_forgot_password = UserForgotPassword(user)
        else:
            user_forgot_password.refresh()
        db.session.add(user_forgot_password)
        db.session.commit()

        token = user_forgot_password.token.encode('base64').strip().replace('=', '_')
        result, message = send_email(
            'Framgia Level Checker - Reset Password',
            app.config['MAIL_SENDERS']['admin'],
            [user.email],
            'reset_password',
            dict(token=token)
        )
        if not result:
            form.email.errors.append('Error: ' + message)
        else:
            flash('Reset password mail sent.', category='success')
            return render_template('user/reset_password_sent.html', user=user)

    return render_template('user/forgot_password.html', form=form)


@user_module.route('/password/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        token = token.replace('_', '=').decode('base64')
    except Exception, e:
        abort(404)
    user_forgot_password = UserForgotPassword.query.filter_by(token=token).first_or_404()

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user_forgot_password.user.set_password(form.new_password.data)
        user_forgot_password.refresh()
        db.session.add(user_forgot_password)
        db.session.commit()
        flash('Password changed successfully.', category='success')
        return redirect(url_for('user.login'))

    return render_template('user/reset_password.html', form=form, username=user_forgot_password.user.username)


@user_module.route('/mail/confirm/<token>')
def confirm_activation(token):
    mail_activation = UserMailActivation.query.filter_by(token=token).first_or_404()

    if mail_activation.user.is_active():
        result = 'activated'
    elif mail_activation.is_expired():
        result = 'expired'
    else:
        mail_activation.user.activate()
        mail_activation.token = generate_token()
        db.session.add(mail_activation)
        db.session.commit()
        result = 'success'

    return render_template('user/confirm_mail_result.html', result=result, user=mail_activation.user)


@user_module.route('/mail/resend', methods=['GET', 'POST'])
def resend_confirm():
    form = ResendMailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        mail_activation = UserMailActivation.query.filter_by(user_id=user.id).first()
        if not mail_activation:
            mail_activation = UserMailActivation(user)
        else:
            mail_activation.refresh()
        db.session.add(mail_activation)
        db.session.commit()

        result, message = send_email(
            'Framgia Level Checker - Resend Confirmation',
            app.config['MAIL_SENDERS']['admin'],
            [user.email],
            'confirm_activation',
            dict(token=mail_activation.token)
        )
        if not result:
            form.email.errors.append('Error: ' + message)
        else:
            flash('Confirmation mail resent.', category='success')

            return render_template('user/confirm_mail_sent.html', user=user)

    return render_template('user/confirm_mail_resend.html', form=form)


class UserView(ModelView):
    # Disable model creation
    can_create = False

    # Override displayed fields
    column_list = ('username', 'name', 'email', 'role', 'is_actived')
    column_filters = ('username', 'name', 'email')

    form_excluded_columns = ('password', 'forgot_password', 'mail_activation', 'results')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(UserView, self).__init__(User, session, **kwargs)

    def is_accessible(self):
        return g.user.is_authenticated() and g.user.is_admin()
