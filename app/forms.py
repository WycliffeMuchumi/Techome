from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class SignUpForm(FlaskForm):
    first_name = StringField('FirstName', validators=[DataRequired(), Length(min=2, max=20)])
    second_name = StringField('SecondName', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('UserName', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('ConfirmPassword', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('login')


class UpdateSignUpForm(FlaskForm):
    first_name = StringField('FirstName', validators=[DataRequired(), Length(min=2, max=20)])
    second_name = StringField('SecondName', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('UserName', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    post_content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('ConfirmPassword', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


