from mongoengine import Document, StringField, IntField, SequenceField, DateTimeField
from datetime import datetime


class ChatMessages(Document):
    id = SequenceField(primary_key=True)
    text = StringField()
    created = DateTimeField(default=datetime.utcnow())
    user_id = IntField()
    chat_id = IntField()