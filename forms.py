from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators, PasswordField, SubmitField

class SignUp(FlaskForm):
    username = StringField('Username', [validators.Length(max=25)])
    email = StringField('Email Address', [validators.Length(max=35)])
    password = PasswordField("Password", [validators.Length(min=1)])
    submit = SubmitField('Sign Up')  
    
class Login(FlaskForm):
    username = StringField('Username', [validators.Length(max=25)])
    password = PasswordField("Password", [validators.Length(min=1)])
    submit = SubmitField('Login') 
