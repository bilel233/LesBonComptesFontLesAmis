from mongoengine import Document, ReferenceField, FloatField
from .user import User

class Reimbursement(Document):
    sender = ReferenceField(User, required=True)
    recipient = ReferenceField(User, required=True)
    amount = FloatField(required=True)

    meta = {'collection': 'reimbursements'}


