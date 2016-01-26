import datetime
import hashlib
import string
import random
import os
import smtplib
import requests
from functools import wraps

from flask import render_template, redirect, url_for, g
from flask_mail import Message

from app import app, mail


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user or not g.user.is_admin():
            return redirect(url_for('index'))
        return f(*args, **kwargs)

    return decorated_function


def generate_random_string(n=7):
    return ''.join([c for i in range(n) for c in random.choice(string.letters)])


def generate_token():
    random_string = generate_random_string()
    return hashlib.sha1(random_string + str(datetime.datetime.now())).hexdigest()


def send_email(subject, sender, recipients, template_name, args):
    try:
        msg = Message(subject, sender=sender, recipients=recipients)
        txt_template = os.path.join(app.config['MAIL_TEMPLATE_FOLDER'], '%s.txt' % template_name)
        html_template = os.path.join(app.config['MAIL_TEMPLATE_FOLDER'], '%s.html' % template_name)
        msg.body = render_template(txt_template, **args)
        msg.html = render_template(html_template, **args)
        mail.send(msg)

        return (True, 'OK')
    except smtplib.SMTPRecipientsRefused:
        return (False, 'Email address does not exist')
    except Exception, e:
        return (False, 'Unknown error. Please try again later')


def check_recaptcha_response(response, remote_ip):
    payload = {
        'secret': app.config['RECAPTCHA_PRIVATE_KEY'],
        'response': response,
        'remoteip': remote_ip
    }
    verify_request = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data=payload
    )
    if verify_request.status_code == 200 and verify_request.json()['success']:
        return (True, 'OK')

    return (False, 'Verify reCAPTCHA response failed')