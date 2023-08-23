from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min = 5, max = 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired(), Length(min=3, max = 20)])
    person = BooleanField('Actor/Writer/Director')
    mediatype = BooleanField('Movie/Show')
    submit = SubmitField('Search')
    
class DeleteAccountForm(FlaskForm):
    deletebutton = BooleanField('Delete Account?')
    submit = SubmitField('Confirm')