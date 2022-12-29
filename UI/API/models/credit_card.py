from marshmallow import Schema, fields, post_load

class CreditCard():
    def __init__(self, cardNum, expDate, securityCode, amount = 1000, id = -1, owner = -1):
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