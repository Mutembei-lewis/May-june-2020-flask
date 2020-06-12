from flask import render_template,url_for,request,flash,redirect,abort
from blog import app,admin,mail
from blog.Forms import PostForm,UpdatePasswordForm, UpdateBioForm,RegistrationForm,LoginForm,ResetPasswordForm,RequestResetForm
from blog.models import db,Post,User,Comment
import datetime
from flask_login import login_user,login_required,logout_user,UserMixin,current_user
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash
import string
from flask_admin.contrib.sqla import ModelView
from flask_mail import Message

### FLASK-ADMIN  VIEW SHOULD BE ADDED DOWN HERE###
# admin.add_view(ModelView(User,db.session))
# admin.add_view(ModelView(Post,db.session))


@app.route('/',methods =['GET', 'POST'])
def index():
    posts =Post.query.order_by(Post.date_created.desc()).all()
    categorylist =[]
    for post in posts:
        categorylist.append(post.category)
    unique_category =set(categorylist)
    newlist = list(unique_category)



    
    
    return render_template("home.html",posts = posts,newlist =newlist)
@app.route('/post/<int:post_id>')
def post(post_id):
    post =Post.query.get_or_404(post_id)
    userposts = Post.query.filter_by(author = post.author).all()
    user = User.query.filter_by(username =post.author).first()
    comments = Comment.query.filter_by(post_id =post_id).all()
    return render_template('post.html',title=post.title,post=post, user = user,userposts=userposts, comments =comments)
    
#  2020shavine!

@app.route('/add_post',methods=['GET','POST'])
def add_post():
    form = PostForm()
    if request.method =='POST'and request.files:

            file = request.files['the_image']
            filename = secure_filename(file.filename)
            title = form.title.data
            post = Post(title =title.strip(),
                        content =form.content.data,
                        category = form.category.data,
                        
                        date_created = datetime.datetime.now(),
                        author = current_user.username,
                        user_id=  current_user.id,
                        post_image_location= filename
                        )
            db.session.add(post)
            # upload image to images folder
            file.save(os.path.join(app.config['POST_UPLOAD_FOLDER'],filename))
            db.session.commit()
            return redirect(url_for('account'))
   
      

    return render_template("addpost.html",form =form)


@app.route('/update_post/<int:post_id>', methods=['GET','POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user.username:
        abort(403)
    form= PostForm() 
    
    
    if  request.method=='POST':
        if form.validate_on_submit and request.files:
            
            file = request.files['the_image']
            filename = secure_filename(file.filename)
            post.title =form.title.data
            post.content =form.content.data
            post.category =form.category.data
            post.post_image_location = filename
            # db.session.add(post)
            db.session.commit()
            file.save(os.path.join(app.config['POST_UPLOAD_FOLDER'],filename))
            flash('Your post has been updated!','success')
            return redirect(url_for('blog ',page_num = 1))

    if request.method =='GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category
    return render_template('update_post.html',form =form,post =post)
  

@app.route('/delete_post/<int:post_id>',methods=['GET','POST'])
def delete_post(post_id):
    post =Post.query.get(post_id)
    if request.method =='POST':
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('blog'))

# user registration route i.e signup 
@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegistrationForm()
    if  form.validate_on_submit():
        password = generate_password_hash(form.password.data)

        user = User(username=form.username.data,
                    email=form.email.data,
                    password_hash=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration was successfully completed','success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form = form)
# login code section
@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
        next = request.args.get('next')

        if next == None or not next[0]== '/':
            next = url_for('blog')
    return render_template('login.html', form=form)

# logout code

@app.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("You are logged out successfully",'info')
    return redirect(url_for('index'))

# user account management
@app.route('/account',methods=['GET', 'POST'])
@login_required
def account():
    user = User.query.filter_by(username =current_user.username).first()
    form = UpdateBioForm()
    if request.method =='POST' and request.files:
        if form.validate_on_submit():
            file = request.files['avatar']
            filename =secure_filename(file.filename)
            user.bio =form.bio.data
            user.firstname= form.firstname.data 
            user.lastname= form.lastname.data 
            user.country  = form.country.data
            user.address = form.address.data
            user.phone_number =form.phone_number.data 
            user.profile_picture = filename
            file.save(os.path.join(app.config['IMAGE_UPLOAD_FOLDER'],filename))

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('account'))
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email 
        form.firstname.data = user.firstname
        form.lastname.data =user.lastname
        form.country.data = user.country
        form.address.data =user.address
        form.phone_number.data = user.phone_number
        form.bio.data =user.bio
    posts = Post.query.all()
    user = User.query.filter_by(username =current_user.username).first()
    passform = UpdatePasswordForm()
    if passform.validate_on_submit():
        password = generate_password_hash(passform.password.data)
        user.password_hash = password 
        db.session.add(user)
        db.session.commit()

    return render_template('userpage.html',passform =passform, user= user,form=form,posts =posts)


@app.route('/profile',methods=['GET','POST'])
@login_required
def update_profile():

    form = UpdateBioForm()
    return render_template('update_profile.html',form =form)

@app.route('/updatepassword', methods=['GET','POST'])
@login_required
def updatepassword():
    user = User.query.filter_by(username =current_user.username).first()
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data)
        user.password_hash = password

    return render_template('userpage.html',form=form)

# blog route section
@app.route('/blog/<int:page_num>', methods=['GET','POST'])
def blog(page_num):
    posts = Post.query.all()
    blogs = Post.query.order_by(Post.date_created.desc()).paginate(per_page =4,page = page_num,error_out =True)
    return render_template('blog.html', blogs = blogs, posts=posts)

@app.route('/delete_account/<int:user_id>',methods=['GET','POST'])
def delete_account(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    posts = Post.query.filter_by(user_id = user.id).all()
    if request.method == 'POST':
        db.session.delete(posts)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('index'))
    return redirect(url_for('account'))

@app.route('/add_comment/<int:post_id>',methods =['GET','POST'])
def add_comment(post_id):

    if request.method =='POST':
            comm = Comment(name = request.form.get('name'),
                            email = request.form.get('email'),
                            message = request.form.get('message'),
                            post_id = post_id,
                            date_posted = datetime.datetime.now() )
            db.session.add(comm)
            db.session.commit()
            flash('Your comment has been added successfully','success')
    return redirect(url_for('post',post_id =post_id))

@app.route('/contact',methods=['GET','POST'])
def contact():
    return render_template('contact.html')

@app.route('/about',methods=['GET','POST'])
def about():
    return render_template('about.html')

@app.route('/gallery',methods=['GET','POST'])
def gallery():
    return render_template('gallery.html')

#  RESET PASSWORD SECTION CODE

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender='lewismutembei001@gmail.com',recipients=[user.email])
    msg.body =f''' To reset your password,visit the following link:
{url_for('reset_token', token =token,_external =True)}

If you did not make this request then simply ignore this email and no changes will be made 
'''
    mail.send(msg)


@app.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if  form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset  your password ','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title ="Reset Password", form = form)

@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That token is invalid or expires','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        user.password_hash= password_hash
        db.session.commit()
        flash("Your password has been updated! You can now login")
        return redirect(url_for('login'))



    return render_template('reset_token.html', title = "Reset Password",form=form)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html')

if __name__ == "__main__":
    app.run(debug=True)

