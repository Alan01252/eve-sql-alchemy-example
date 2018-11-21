from models import (
    Event, EventMeta, Contact, ContactTeam,
    Number, ContactNumberBridge,
    Comment,Tag,CommentTagBridge,OpLog
)
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
        'contact_team': ResourceConfig(ContactTeam),
        'number': ResourceConfig(Number),
        'contact_number_bridge': ResourceConfig(ContactNumberBridge),
        'comment': ResourceConfig(Comment),
        'tag': ResourceConfig(Tag),
        'comment_tag_bridge': ResourceConfig(CommentTagBridge),
        'oplog': ResourceConfig(OpLog)
    }).render()
}

SETTINGS['DOMAIN']['oplog'].update({
    'resource_methods': ['GET'],
    'allowed_roles': ['superuser']
})

# Set to allow number key to be returned with events
SETTINGS['DOMAIN']['contact']['schema']['numbers']['schema']['data_relation']['embeddable'] = True
# Set to allow number key to be returned with events
#SETTINGS['DOMAIN']['event']['schema']['event_meta']['data_relation']['embeddable'] = True
#SETTINGS['DOMAIN']['comment']['schema']['tag']['schema']['data_relation']['embeddable'] = True



print(SETTINGS['DOMAIN'])

