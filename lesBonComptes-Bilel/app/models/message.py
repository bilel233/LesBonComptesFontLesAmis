from mongoengine import Document,StringField, ReferenceField,DateTimeField,IntField
from .user import User
from .group import Group
import datetime

class Message(Document):
    content = StringField(required=True)
    sender = ReferenceField(User,required=True)
    group = ReferenceField(Group,null=True) # Null dans le cas ou le message est privé
    recipient = ReferenceField(User,null=True) # utilisé pour les messages
    timestamp = DateTimeField(default=datetime.datetime.now)

    meta = {'collection': 'messages'}



    