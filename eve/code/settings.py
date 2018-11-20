from models import Event, EventMeta, Contact, Number, ContactNumberBridge,Comment,Tag,CommentTagBridge,OpLog
from eve_sqlalchemy.config import DomainConfig, ResourceConfig

SETTINGS = {
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:////code/test.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'RESOURCE_METHODS': ['GET', 'POST', 'DELETE'],
    'ITEM_METHODS': ['GET', 'PATCH', 'PUT'],
    'OPLOG': True,
    'OPLOG_AUDIT': True,
    'OPLOG_ENDPOINT': 'audit',
    'OPLOG_METHODS': ['GET', 'DELETE', 'POST', 'PATCH', 'PUT'],
    'DOMAIN': DomainConfig({
        'event': ResourceConfig(Event),
        'event_meta': ResourceConfig(EventMeta),
        'contact': ResourceConfig(Contact),
        'number': ResourceConfig(Number),
        'contact_number_bridge': ResourceConfig(ContactNumberBridge),
        'comment': ResourceConfig(Comment),
        'tag': ResourceConfig(Tag),
        'comment_tag_bridge': ResourceConfig(CommentTagBridge),
        'oplog': ResourceConfig(OpLog)
    }).render()
}


