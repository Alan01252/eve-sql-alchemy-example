from eve import Eve
from eve.utils import config
from settings import SETTINGS
from models import Event, EventMeta, Contact, Number, ContactNumberBridge, Comment, Tag, CommentTagBridge, OpLog
from models import Base

from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from eve_sqlalchemy.config import ResourceConfig
from event_blueprint import event_blueprint
from eve.auth import TokenAuth

import json

from eve.methods.common import (
    oplog_push
)

from eve.methods.common import (
    pre_event,
)

class TokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        print(token)
        print(resource)
        print(allowed_roles)

app = Eve(auth=TokenAuth, settings=SETTINGS, validator=ValidatorSQL, data=SQL)
app.register_blueprint(event_blueprint)

# Eve hardcodes the oplog schema, overwriting the settings needed for sqlalchemy
# Make them back to what they need to be for SQLAlchemy here
oplog = ResourceConfig(OpLog)
oplogSchema = oplog.render(config.DATE_CREATED,
               last_updated=config.LAST_UPDATED, etag=config.ETAG)
app.config['DOMAIN']['oplog']['schema'] = oplogSchema

db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base
db.create_all();

# # Insert some example dimensions into the db
if not db.session.query(EventMeta).count():
     db.session.add_all([
         EventMeta(url="http://path_to_s3"),
         Tag(text="#a_tag"),
         Tag(text="#a_tag1"),
         Tag(text="#a_tag2"),
         Tag(text="#a_tag3"),
         Tag(text="#a_tag4"),
     ])
     db.session.commit()


# # Insert some example facts into the db
if not db.session.query(Event).count():
     event_meta = db.session.query(EventMeta).one()
     tags = db.session.query(Tag).all()

     db.session.add_all([
         Event(event_meta_key=event_meta.id),
     ])

     db.session.add_all([
 	    Comment(tags=tags, event_meta_key=1)
     ])

     db.session.commit()





# HOOKS
def pre_get_callback(resource, request, lookup):
     app.logger.info("pre get fired")
     if resource:
        oplog_push(resource, None, "GET")


def post_get_callback(resource, request, lookup):
     # work out what we get here, if we're getting a list of comments / events then we should log
     # each individual event id here too
     events = [] 
     if resource:
        oplog_push(resource, events, "GET")

def pre_post_callback(resource, request):
     print(resource)
     print(request)

def pre_put_callback(resource, request, lookup):
     print(resource)
     print(request)
     print(lookup)

def pre_oplog(resource, entries):
    for entry in entries:
        if 'c' in entry:
            entry['c'] = json.dumps(entry['c'])

app.on_pre_GET += pre_get_callback
app.on_pre_GET += pre_get_callback
app.on_post_GET += post_get_callback
app.on_pre_POST += pre_post_callback
app.on_pre_PUT += pre_put_callback
app.on_oplog_push += pre_oplog

app.run(host='0.0.0.0', use_reloader=True)

