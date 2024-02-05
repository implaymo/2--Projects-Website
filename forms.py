from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField, TextAreaField

class SignUp(FlaskForm):
    username = StringField('Username', [validators.Length(max=25)])
    email = StringField('Email Address', [validators.Length(max=35)])
    password = PasswordField("Password", [validators.Length(min=1)])
    submit = SubmitField('Sign Up')  
    
class Login(FlaskForm):
    username = StringField('Username', [validators.Length(max=25)])
    password = PasswordField("Password", [validators.Length(min=1)])
    submit = SubmitField('Login') 
    
class Edit(FlaskForm):
    title = StringField('Title')
    content = TextAreaField('Content')
    image = StringField("Image")
    submit = SubmitField('Submit') 
    
class Add(FlaskForm):
    title = StringField('Title')
    content = TextAreaField('Content')
    image = StringField("Image")
    submit = SubmitField('Submit') 