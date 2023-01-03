from marshmallow import Schema, fields, post_load
from EngineAPI import db

class Account_balance(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    currency = db.Column(db.String(3), nullable = False)
    amount = db.Column(db.Float(), nullable = False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    
    def __init__(self,currency="RSD", amount= 0, id = None,user_id=-1):
        self.id = id
        self.currency = currency
        self.amount = amount
        self.user_id = user_id
        
        
class Account_balanceSchema(Schema):
    id = fields.Number()
    currency = fields.String()
    amount = fields.Number()
    user_id = fields.Number()
    
    @post_load
    def make_account_balance(self, data, **kwargs):
        return Account_balance(**data)