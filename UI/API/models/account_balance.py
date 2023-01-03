from marshmallow import Schema, fields, post_load


class Account_balance():
    def __init__(self,  amount,currency="RSD", user_id=-1, id=-1):
        self.currency = currency
        self.user_id = user_id
        self.amount = amount
        self.id = id

class AccountBalanceSchema(Schema):
    id = fields.Number()
    currency = fields.String()
    amount = fields.Number()
    user_id = fields.Number()

    @post_load
    def make_state(self, data, **kwargs):
        return Account_balance(**data)