from models import Event, EventMeta, Conversation, TagBridge, Tag, OpLog
from eve_sqlalchemy.config import DomainConfig, ResourceConfig

SETTINGS = {
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:////code/test.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'RESOURCE_METHODS': ['GET', 'POST'],
    'OPLOG': True,
    'OPLOG_AUDIT': True,
    'OPLOG_ENDPOINT': 'audit',
    'OPLOG_METHODS': ['GET', 'DELETE', 'POST', 'PATCH', 'PUT'],
    'DOMAIN': DomainConfig({
        'event': ResourceConfig(Event),
        'event_meta': ResourceConfig(EventMeta),
        'conversation': ResourceConfig(Conversation),
        'tag_bridge': ResourceConfig(TagBridge),
        'tag': ResourceConfig(Tag),
        'oplog': ResourceConfig(OpLog)
    }).render()
}


