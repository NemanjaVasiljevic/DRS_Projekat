from marshmallow import Schema, fields, post_load
from EngineAPI import db

class CreditCard(db.Model):
    __tablename__ = 'creditCards'
    id = db.Column(db.Integer(), primary_key=True)
    cardNum = db.Column(db.String(16), unique=True)
    expDate = db.Column(db.String(5), nullable=False)
    securityCode = db.Column(db.String(3), nullable = False)
    amount = db.Column(db.Integer(), nullable=False, default=1000)
    owner = db.Column(db.Integer(), db.ForeignKey('users.id'))
    
    def __init__(self, cardNum, expDate, securityCode, amount = 1000, id = None, owner = -1):
        self.id = id
        self.cardNum = cardNum
        self.expDate = expDate
        self.securityCode = securityCode
        self.amount = amount
        self.owner = owner

class CreditCardSchema(Schema):
    id = fields.Number()
    cardNum = fields.String()
    expDate = fields.String()
    securityCode = fields.String()
    amount = fields.Number()
    owner = fields.Number()
    
    @post_load
    def make_creditCard(self, data, **kwargs):
        return CreditCard(**data)