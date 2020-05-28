from blog import db,app,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin 
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Post(db.Model):
    __tablename__ = 'post'


    def __init__(self,title,content,category,user_id, date_created, author,post_image_location):
        self.title = title
        self.content = content
        self.date_created = date_created
        self.author = author
        
        self.post_image_location = post_image_location
        self.category = category
        self.user_id = user_id

        
    id = db.Column(db.Integer(), primary_key =True)
    title = db.Column(db.String(50),nullable=False)
    content = db.Column(db.String(800), nullable= False )
    date_created = db.Column(db.DateTime())
    category = db.Column(db.String(20),nullable=False)
    author= db.Column(db.String(40),index =True)
    post_image_location = db.Column(db.String(30),index= True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable =False)
    post = db.relationship('Comment', backref='comments', lazy=True)

    
class User (UserMixin,db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(64), unique= True)
    email = db.Column(db.String(64), unique = True,index =True)
    password_hash = db.Column(db.String(128))
    profile_picture = db.Column(db.String(40))
    bio = db.Column(db.String(100))
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    address =db.Column(db.String(30))
    country = db.Column(db.String(12))
    phone_number = db.Column(db.Integer())
    posts = db.relationship('Post', backref='user', lazy=True)
    

    def check_password(self,password):
            return check_password_hash(self.password_hash,password )
    ### REPRESENTATION METHOD CODE GOES HERE ###
    # def __repr__(self):
    #     return '<User %r>' % (self.username)

class Comment(db.Model):
    __tablename__ = 'comments'
    def __init__(self,name,email,message,post_id):
        self.name = name
        self.email = email
        self.message = message
        self.post_id = post_id

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64), unique= False)
    email = db.Column(db.String(64),unique=False)
    message =db.Column(db.String(250), index=False, nullable= False)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'),nullable=False)
    
