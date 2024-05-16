from mongoengine import Document, StringField, FloatField, DateTimeField, ReferenceField, ListField, FileField
import datetime

class Expense(Document):
    title = StringField(required=True)
    amount = FloatField(required=True)
    date = DateTimeField(default=datetime.datetime.now)
    payer = ReferenceField('User', required=True)
    group = ReferenceField('Group')
    receipt = FileField()
    category = StringField(required=True)
    involved_members = ListField(ReferenceField('User'))
    weights = ListField(FloatField())

    meta = {'collection': 'expenses'}
