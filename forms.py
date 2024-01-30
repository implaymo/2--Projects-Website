from wtforms import Form, StringField, validators, PasswordField

class SignUp(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField("Password", [validators.Length(min=8)])
    
    
    
class Login(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField("Password", [validators.Length(min=8)])