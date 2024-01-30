from wtforms import Form, StringField, validators, PasswordField, SubmitField

class SignUp(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField("Password", [validators.Length(min=8)])
    submit = SubmitField('Sign Up')  
    
class Login(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField("Password", [validators.Length(min=8)])
    submit = SubmitField('Login') 
