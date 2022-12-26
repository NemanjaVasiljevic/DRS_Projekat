from marshmallow import Schema, fields, post_load

class CreditCard():
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
        return CreditCard(data)