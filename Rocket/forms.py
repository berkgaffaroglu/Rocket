from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed 
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField  
from wtforms.validators import DataRequired, Length, EqualTo, Email,ValidationError  
from Rocket.models import User
from flask_login import current_user

badwords = ['fuck','anus','bitch','dick','pussy','blowjob','piç','ibne']
class RegistrationForm(FlaskForm):  
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])  
    email = StringField('Email', validators=[DataRequired(), Email()])  
    password = PasswordField('Password', validators=[DataRequired()])  
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])  
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')  
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another username.')
        for word in username.data.strip().lower().split(' '):
            if word.strip() in badwords:
                raise ValidationError(f"Word is not allowed: {word.strip()}")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another email.')
            

    



        
  
class LoginForm(FlaskForm):  
    email = StringField('Email', validators=[DataRequired()])  
    password = PasswordField('Password', validators=[DataRequired()])  
    remember = BooleanField('Remember Me')  
    submit = SubmitField('Login')  



class UpdateProfileForm(FlaskForm):

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

        for word in username.data.strip().lower().split(' '):
            if word.strip() in badwords:
                raise ValidationError(f"Word not allowed: {word.strip()}")
    


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class CreatePostForm(FlaskForm):  
    title = StringField('Title', validators=[DataRequired()])  
    content = TextAreaField('Content', validators=[DataRequired()])   
    submit = SubmitField('Submit')  

    def validate_title(self, title):
        for word in title.data.strip().lower().split(' '):
            if word.strip() in badwords:
                raise ValidationError(f"Word is not allowed: {word.strip()}")
    def validate_content(self, content):
        for word in content.data.strip().lower().split(' '):
            if word.strip() in badwords:
                raise ValidationError(f"Word is not allowed: {word.strip()}")




class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')