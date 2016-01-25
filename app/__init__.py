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
from app.answer.views import answer_module, AnswerView
from app.question.views import question_module, QuestionView
from app.examination.views import examination_module, ExaminationView

app.register_blueprint(user_module, url_prefix='/user')
app.register_blueprint(answer_module, url_prefix='/answer')
app.register_blueprint(question_module, url_prefix='/question')
app.register_blueprint(examination_module, url_prefix='/examination')

admin = Admin(app, url='/admin')
admin.add_view(UserView(db.session, name='Users'))
admin.add_view(AnswerView(db.session, name='Answers'))
admin.add_view(QuestionView(db.session, name='Questions'))
admin.add_view(ExaminationView(db.session, name='Examinations'))
