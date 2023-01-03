from marshmallow import Schema, fields, post_load
from EngineAPI import db


class Account_balance(db.Model):
    __tablename__ = 'account_balance'
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __init__(self, currency, amount, user_id, id):
        self.currency = currency
        self.user_id = user_id
        self.amount = amount
        self.id = id

class Account_balanceSchema(Schema):
    id = fields.Number()
    currency = fields.String()
    amount = fields.Number()
    user_id = fields.Number()

    @post_load
    def make_state(self, data, **kwargs):
        return Account_balance(**data)