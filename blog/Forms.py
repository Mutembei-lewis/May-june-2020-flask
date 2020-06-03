from flask_wtf import FlaskForm
from blog.models import Post
import email_validator
from wtforms import StringField, DateField,IntegerField,SelectField, TextField,SubmitField,FileField,TextAreaField,PasswordField
from wtforms.validators import ValidationError, DataRequired,Email,EqualTo,Length
from flask_wtf.file import FileField,FileAllowed,FileRequired
from blog.models import User


class PostForm(FlaskForm):
    title = StringField(' Post title', validators= [DataRequired(message="Your post content must have a title ")])
    the_image = FileField('Image', validators=[FileRequired(),FileAllowed(['gif', 'jpg', 'jpeg', 'png'],'Images only can be uploaded')])
    content = TextAreaField('Post content ', validators= [ DataRequired(message='you need to add some content to your post ')])
    
    category = StringField('Category', validators=[DataRequired(message='THis field must be filled up')])
    submit = SubmitField("post article")

# class UpdatePostForm(FlaskForm):
#     prev_title = StringField('title of the post to edit',validators=[DataRequired(message='This post doesn\'t exit fill out the correct title ')])
#     title   = StringField('New title')
#     content = TextAreaField('Edit content')
#     the_image = FileField('Image', validators=[FileRequired(),FileAllowed(['gif', 'jpg', 'jpeg', 'png'],'Images only can be uploaded')])
#     category = StringField('Category', validators=[DataRequired(message='THis field must be filled up')])

#     submit = SubmitField('submit Changes')


class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired(),Length(min=6, max=12)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password',message='The passwords must match')])
    submit = SubmitField('Register')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    email = StringField('Email:',validators=[DataRequired(message='This must be filled'),Email(message= "This field must be an email")])
    password = PasswordField('password:',validators = [DataRequired(message="This field is required")])
    submit= SubmitField('Log in')

class UpdateBioForm(FlaskForm):
    avatar = FileField('image',validators=[FileAllowed(['gif', 'jpg', 'jpeg', 'png'],'Images only can be uploaded')] )
    bio = TextAreaField('Bio', validators=[Length(min=0,max=300)])
    phone_number = IntegerField('Phone Number')
    firstname = StringField('First Name')
    lastname = StringField( 'Last Name')
    username = StringField( 'Username')
    email = StringField('Email',validators=[Email()])
    address = StringField('Address')
    country = StringField('country')
    submit = SubmitField('update profile')
class UpdatePasswordForm(FlaskForm):
    password = PasswordField('Password:', validators=[DataRequired(),Length(min=6, max=12)])
    password2 = PasswordField(
        'Confirm Password:', validators=[DataRequired(), EqualTo('password',message='The passwords must match')])
    submit = SubmitField('Update password')


class RequestResetForm(FlaskForm):
        email = StringField("Email",
                            validators=[DataRequired(),Email()])
        submit = SubmitField('Request password reset ')
        def validate_email(self, email):
            user = User.query.filter_by(email = email.data).first()
            if user is None:
                raise ValidationError('There is no account with that email . You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators =[DataRequired(),])
    confirm_password = PasswordField("confirm password", validators =[DataRequired(),EqualTo('password')])
    submit = SubmitField("Reset Password")