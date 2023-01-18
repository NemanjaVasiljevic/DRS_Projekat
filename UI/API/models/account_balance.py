from marshmallow import Schema, fields, post_load


class Account_balance():
    def __init__(self, amount = 0, user_id = -1,currency="RSD", id = -1, reserved = 0):
        self.id = id
        self.currency = currency
        self.amount = amount
        self.reserved = reserved
        self.user_id = user_id
        

class Account_balanceSchema(Schema):
    id = fields.Number()
    currency = fields.String()
    amount = fields.Number()
    reserved = fields.Number()
    user_id = fields.Number()
    
    @post_load
    def make_account_balance(self,data,**kwargs):
        return Account_balance(**data)