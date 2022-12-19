from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class RegisterForm(FlaskForm):
    name = StringField(label='Name:')
    last_name = StringField(label='Last name: ')
    address = StringField(label='Address: ')
    city = StringField(label='City: ')
    country = StringField(label='Country: ')
    tel_number = StringField(label='Phone number: ')
    email_address = StringField(label='Email address:')
    password1 = PasswordField(label='Password:')
    password2 = PasswordField(label='Confirm password:')
    submit = SubmitField(label='Register')