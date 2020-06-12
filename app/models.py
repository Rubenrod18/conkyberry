import logging
from datetime import datetime

from .extensions import mongoengine as db

logger = logging.getLogger(__name__)

_TYPE_VAR_CHOICES = ('str', 'int', 'list', 'tuple', 'float', 'dict', )


class ResourceData(db.EmbeddedDocument):
    resource_name = db.StringField(required=True)
    resource_type = db.StringField(required=True, choices=_TYPE_VAR_CHOICES)
    resource_graph = db.DictField(required=True)
    resource_value = db.StringField(required=True)


class Resource(db.Document):
    meta = {
        'collection': 'resources',
        'allow_inheritance': True,
    }

    created_at = db.DateTimeField(default=datetime.utcnow(), unique=True)
    data = db.EmbeddedDocumentListField('ResourceData', required=True)
