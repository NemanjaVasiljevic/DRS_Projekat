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
    sender = db.Column(db.String(50), db.ForeignKey('users.email_address'))
    receiver = db.Column(db.String(50), db.ForeignKey('users.email_address'))
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
    sender = fields.String()
    receiver_email = fields.String()
    receiver_card = fields.String()
    currency = fields.String()
    amount = fields.Number()
    
    @post_load
    def make_transaction(self, data, **kwargs):
        return Transaction(**data)
    
class TransactionSchema2(Schema):
    id = fields.Number()
    sender = fields.String()
    receiver = fields.String()
    currency = fields.String()
    amount = fields.Number()
    state = EnumField(TransactionState)
    
    @post_load
    def make_transaction(self, data, **kwargs):
        return Transaction(**data)