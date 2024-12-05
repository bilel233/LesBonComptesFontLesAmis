from mongoengine import Document, StringField, ReferenceField, FileField
from .user import User

class PaymentInfo(Document):
    user = ReferenceField(User, unique=True, required=True)
    payment_method = StringField(required=True)
    rib_file = FileField()

    meta = {'collection': 'payment_infos'}
