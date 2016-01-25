import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://admin:admin@localhost/checker'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'place_your_csrf_session_key_here'

CSRF_SESSION_KEY = 'place_your_csrf_key_here'

MAX_MEMBER = 5
LOCK_TEAM = False
LOCK_PROFILE = False
GAME_STARTED = False

UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'files')

# mail config
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
# MAIL_DEBUG = app.debug
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_DEFAULT_SENDER = None
MAIL_MAX_EMAILS = None
# MAIL_SUPPRESS_SEND = app.testing
MAIL_ASCII_ATTACHMENTS = False

MAIL_TEMPLATE_FOLDER = 'mails'

MAIL_SENDERS = {
    'admin': ('Admin Team', 'admin@ctf.framgia.vn'),
    'support': ('Support Team', 'support@ctf.framgia.vn')
}

ADMINS = ['nguyen.anh.tien@framgia.com']

RECAPTCHA_PUBLIC_KEY = 'public_key_here'
RECAPTCHA_PRIVATE_KEY = 'private_key_here'
