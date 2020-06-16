import logging
from datetime import datetime

from .extensions import mongoengine as db

logger = logging.getLogger(__name__)

_TYPE_VAR_CHOICES = ('str', 'int', 'list', 'tuple', 'float', 'dict',)


RESOURCE_FIELDS = [
    # CPU
    ('5ee3b8af24587fb41c74ad33', 'CPU average usage'),
    ('5ee3b99e9e62e3722c6652e5', 'CPU average temperature'),
    ('5ee718d260323a7836891238', 'per-CPU average usage'),
    #('5ee7192fe9d0ec9d96ee298a', 'Top 5 CPU consuming processes'),
    # GPU
    ('5ee71b8fde616ffedec72dfb', 'GPU average temperature'),
    # RAM
    ('5ee71b9ecba5d61d159b8fc8', 'RAM average usage'),
    ('5ee71bab85cc9f1664bb006f', 'Top 5 RAM consuming processes'),
    ('5ee71bb5aa4faf99ed69296c', 'SWAP average usage'),
    # System
    ('5ee71bcb43fc0a4a44b07d4e', 'Linux kernel version'),
    ('5ee71bd389a104a4514ce702', 'CPU model'),
    ('5ee71bdd93e87cbb3b767e26', 'MAC'),
    ('5ee71be5f7bb1f60cefc2cb4', 'Uptime server'),
    # Hard disk
    ('5ee71bfcaaaf59d2e8c3d6b5', 'Hard disk storage: /'),
    # Network
    ('5ee71c0576ee8395333c3a7b', 'Public IP'),
    ('5ee71c0f7b47445a0f43f74a', 'Private IP'),
    ('5ee71c17099c6c6a726c4c9d', 'Download average traffic rate for today'),
    ('5ee71c218255394a266fb4b2', 'Download packages total for day'),
    ('5ee71c2bc052ea5cda76da8e', 'Download packages total for month'),
    ('5ee71c3324de9b7519b23894', 'Upload average traffic rate for today'),
    ('5ee71c3c9b8e880c0a105c17', 'Upload packages total for day'),
    ('5ee71c4707ed517d1e8c8ee3', 'Upload packages total for month'),
]
RESOURCE_FIELDS_BY_NAME = {item[1]: item[0] for item in RESOURCE_FIELDS}
RESOURCE_FIELD_IDS = [item[0] for item in RESOURCE_FIELDS]


class ResourceGraph(db.Document):
    meta = {
        'collection': 'resource_graphs',
    }

    name = db.StringField(required=True, unique=True)
    graph = db.DictField(required=True)


class ResourceData(db.EmbeddedDocument):
    resource_name = db.StringField(required=True, choices=RESOURCE_FIELD_IDS)
    resource_type = db.StringField(required=True, choices=_TYPE_VAR_CHOICES)
    resource_graph = db.ReferenceField('ResourceGraph')
    resource_value = db.StringField(required=True)


class Resource(db.Document):
    meta = {
        'collection': 'resources',
    }

    created_at = db.DateTimeField(default=datetime.utcnow(), unique=True)
    data = db.EmbeddedDocumentListField('ResourceData', required=True)
