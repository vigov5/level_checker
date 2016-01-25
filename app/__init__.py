from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'user.login'

mail = Mail(app)

from app.common import views
from app.user.views import user_module, UserView

app.register_blueprint(user_module, url_prefix='/user')

admin = Admin(app, url='/admin')
admin.add_view(UserView(db.session, name='Users'))
