from marshmallow import Schema, fields, post_load
from EngineAPI import db

class CreditCard(db.Model):
    __tablename__ = 'creditCards'
    cardNum = db.Column(db.Integer, primary_key=True)
    ownerName = db.Column(db.String(32), nullable=False)
    expDate = db.Column(db.String(5), nullable=False)
    securityCode = db.Column(db.Integer, nullable = False, unique = True)
    
    def __init__(self,cardNum,ownerName,expDate,securityCode):
        self.cardNum = cardNum
        self.ownerName = ownerName
        self.expDate = expDate
        self.securityCode = securityCode
        

class CreditCardSchema(Schema):
    cardNum = fields.Number()
    ownerName = fields.String()
    expDate = fields.String()
    securityCode = fields.Number()
    
    @post_load
    def make_creditCard(self, data, **kwargs):
        return CreditCard(**data)