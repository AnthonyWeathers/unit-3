from flask_wtf import FlaskForm # apparently these need python 3.11
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])

class NumOfMelonsForm(FlaskForm):
    number = StringField('Add', [validators.InputRequired()])