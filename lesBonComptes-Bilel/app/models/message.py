from mongoengine import Document, StringField, ReferenceField, DateTimeField
import datetime
from .user import User
from .group import Group

class Message(Document):
    content = StringField(required=True)
    sender = ReferenceField(User, required=True)
    group = ReferenceField(Group, null=True)
    recipient = ReferenceField(User, null=True)
    timestamp = DateTimeField(default=datetime.datetime.now)

    meta = {'collection': 'messages'}
