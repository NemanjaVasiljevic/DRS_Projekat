from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from enum import Enum
from EngineAPI import db

class TransactionState(Enum):
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    REFUSED = "REFUSED"

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer(), primary_key=True)
    sender = db.Column(db.Integer(), db.ForeignKey('users.id'))
    receiver = db.Column(db.Integer(), db.ForeignKey('users.id'))
    currency = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float(), nullable=False)
    state = db.Column(db.Enum(TransactionState), nullable=False)
    
    def __init__(self, sender, receiver, currency, amount, state, id = -1):
        self.sender = sender
        self.receiver = receiver
        self.currency = currency
        self.amount = amount
        self.state = state
        self.id = id

class TransactionSchema(Schema):
    id = fields.Number()
    sender = fields.Number()
    receiver_email = fields.String()
    receiver_card = fields.String()
    currency = fields.String()
    amount = fields.Number()
    state = EnumField(TransactionState)
    
    @post_load
    def make_transaction(self, data, **kwargs):
        return Transaction(**data)