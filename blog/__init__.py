import os
from flask_sqlalchemy import SQLAlchemy
from  flask import Flask,render_template,session

from flask_login import LoginManager
from werkzeug.utils import secure_filename
from flask_admin import Admin

login_manager = LoginManager()

app =Flask(__name__)
admin = Admin(app,template_mode='bootstrap4')

app.config['SECRET_KEY'] = "mysecretkey"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////home/walker/Bloggy/blogy.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']= False
app.config['POST_UPLOAD_FOLDER']  = os.path.join(basedir,'static/images/post/')
app.config['IMAGE_UPLOAD_FOLDER'] = os.path.join(basedir,'static/images/profiles/')
db =SQLAlchemy(app)      

login_manager.init_app(app)
login_manager.login_view = "login"
