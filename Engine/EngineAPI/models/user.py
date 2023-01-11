from marshmallow import Schema, fields, post_load
from EngineAPI import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(32), nullable=False)
    country = db.Column(db.String(32), nullable=False)
    tel_number = db.Column(db.String(20), nullable=False)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    verified = db.Column(db.Boolean(), nullable=False)
    credit_card = db.relationship('CreditCard', backref='owned_user', lazy=True)

    def __init__(self, name, last_name, address, city, country, tel_number, email_address, password, verified = False, id = None):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.country = country
        self.tel_number = tel_number
        self.email_address = email_address
        self.password = password
        self.verified = verified

class UserSchema(Schema):
    id = fields.Number()
    name = fields.String()
    last_name = fields.String()
    address = fields.String()
    city = fields.String()
    country = fields.String()
    tel_number = fields.String()
    email_address = fields.Email()
    password = fields.String()
    verified = fields.Boolean()

    @post_load
    def make_user(self,data,**kwargs):
        return User(**data)
    
class LoginSchema(Schema):
    email_address = fields.Email()
    password = fields.String()
    
class ExchangeSchema(Schema):
    user_id = fields.Number()
    from_currency = fields.String()
    to_currency = fields.String()
    amount = fields.Number()
    rate = fields.Number()