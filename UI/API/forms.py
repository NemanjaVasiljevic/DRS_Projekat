from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

class RegisterForm(FlaskForm):
    name = StringField(label='Name:', validators=[Length(min=2, max=30),DataRequired()])
    last_name = StringField(label='Last name: ', validators=[Length(min=2, max=30),DataRequired()])
    address = StringField(label='Address: ', validators=[Length(min=2, max=30),DataRequired()])
    city = StringField(label='City: ', validators=[Length(min=2, max=30),DataRequired()])
    country = StringField(label='Country: ', validators=[Length(min=2, max=30),DataRequired()])
    tel_number = StringField(label='Phone number: ', validators=[Length(min=2, max=30),DataRequired()])
    email_address = StringField(label='Email address:', validators=[Email('Incorrect format for email address.'),DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label='Confirm password:', validators=[EqualTo('password1', 'Passwords do not match.'), DataRequired()])
    submit = SubmitField(label='Register')
    
class LoginForm(FlaskForm):
    email_address = StringField(label='Email address: ', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label='Login')
    
class EditProfileForm(FlaskForm):
    name = StringField(label='Name:', validators=[Length(min=2, max=30),DataRequired()])
    last_name = StringField(label='Last name: ', validators=[Length(min=2, max=30),DataRequired()])
    address = StringField(label='Address: ', validators=[Length(min=2, max=30),DataRequired()])
    city = StringField(label='City: ', validators=[Length(min=2, max=30),DataRequired()])
    country = StringField(label='Country: ', validators=[Length(min=2, max=30),DataRequired()])
    tel_number = StringField(label='Phone number: ', validators=[Length(min=2, max=30),DataRequired()])
    email_address = StringField(label='Email address:', render_kw={'readonly': True})
    password1 = PasswordField(label='Password:', validators=[Length(min=6)])
    password2 = PasswordField(label='Confirm password:', validators=[EqualTo('password1', 'Passwords do not match.')])
    submit = SubmitField(label='Save changes')
    
class CreditCardFrom(FlaskForm):
    cardNum = StringField(label='Card number: ', validators=[Length(min = 16, max = 16),DataRequired()])
    expDate = StringField(label='Expiration date: ', validators=[Length(min = 5, max = 5),DataRequired()])
    securityCode = StringField(label='Security code: ', validators=[Length(min = 3, max = 3),DataRequired()])
    submit = SubmitField(label='Add card')
    
    
class AccountBalanceForm(FlaskForm):
    amount = StringField(label='Amount: ', validators=[Length(min = 1, max = 256),DataRequired()])
    submit = SubmitField(label='Add funds')
    
class ExchangeForm(FlaskForm):
    from_currency = SelectField(validators=[])
    to_currency = SelectField(validators=[])
    amount = StringField(validators=[])
    refresh = SubmitField(label="Refresh table")
    submit = SubmitField(label="Exchange")