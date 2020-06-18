import os
from flask_sqlalchemy import SQLAlchemy
from  flask import Flask,render_template,session
from flask_mail import Mail
from flask_login import LoginManager
from werkzeug.utils import secure_filename
from flask_admin import Admin

login_manager = LoginManager()

app =Flask(__name__)
admin = Admin(app,template_mode='bootstrap4')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATION']= False
app.config['POST_UPLOAD_FOLDER']  = os.path.join(basedir,'static/images/post/')
app.config['IMAGE_UPLOAD_FOLDER'] = os.path.join(basedir,'static/images/profiles/')
db =SQLAlchemy(app)      

login_manager.init_app(app)
login_manager.login_view = "login"
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'lewismutembei001@gmail.com'
app.config['MAIL_PASSWORD'] = 'Lewis668@'
mail = Mail(app)
