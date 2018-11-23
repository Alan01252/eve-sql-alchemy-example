from eve import Eve
from eve.utils import config
from settings import SETTINGS
from models import (
    Event, EventMeta, Contact, Number, ContactNumberBridge, 
    Comment, Tag, CommentTagBridge, OpLog
)
from models import Base

from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from eve_sqlalchemy.config import ResourceConfig
from event_blueprint import event_blueprint
from eve.auth import TokenAuth, BasicAuth
 
from hooks import oplog_hooks, totp_hooks, user_hooks, generic_hooks

app = Eve(auth=None, settings=SETTINGS, validator=ValidatorSQL, data=SQL)
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

oplog_hooks.add(app)
totp_hooks.add(app)
user_hooks.add(app)
generic_hooks.add(app)


app.run(host='0.0.0.0', use_reloader=True)

