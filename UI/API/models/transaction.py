from marshmallow import Schema, fields, post_load

class Transaction():
    def __init__(self, sender, receiver, currency, amount, id = -1):
            self.sender = sender
            self.receiver = receiver
            self.currency = currency
            self.amount = amount
            self.id = id
            
class TransactionSchema(Schema):
    id = fields.Number()
    sender = fields.Number()
    receiver = fields.String()
    currency = fields.String()
    amount = fields.Number()
    
    @post_load
    def make_transaction(self, data, **kwargs):
        return Transaction(**data)