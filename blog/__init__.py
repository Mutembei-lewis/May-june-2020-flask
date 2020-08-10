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

app.config['SECRET_KEY'] = ' Mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
os.environ['DATABASE_URL'] = "postgresql://postgres://tyedljkdgladsv:2e3341bc7bbd7ec1bd97132ef08fc667e2356b40533cde003f1453a77ae13200@ec2-34-224-229-81.compute-1.amazonaws.com:5432/dbrrtjs6iqpn2p"

app.config["DATABASE_URL"] = "postgresql://postgres://tyedljkdgladsv:2e3341bc7bbd7ec1bd97132ef08fc667e2356b40533cde003f1453a77ae13200@ec2-34-224-229-81.compute-1.amazonaws.com:5432/dbrrtjs6iqpn2p"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATION']= False
app.config['POST_UPLOAD_FOLDER']  = os.path.join(basedir,'static/images/post/')
app.config['IMAGE_UPLOAD_FOLDER'] = os.path.join(basedir,'static/images/profiles/')
db =SQLAlchemy(app)      

login_manager.init_app(app)
login_manager.login_view = "login"
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'example@gmail.com'
app.config['MAIL_PASSWORD'] = 'thisisprivate'
mail = Mail(app)
