from datetime import datetime

from mongoengine import DynamicDocument, StringField, DateTimeField


class Resource(DynamicDocument):
    meta = {'collection': 'resources'}

    name = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow())
