from eve import Eve
from eve.utils import config
from settings import SETTINGS
from models import Base, Event, EventMeta, Tag, TagBridge, Conversation, OpLog

from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from eve_sqlalchemy.config import ResourceConfig

from eve.methods.common import (
    oplog_push
)

app = Eve(auth=None, settings=SETTINGS, validator=ValidatorSQL, data=SQL)

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

# Insert some example dimensions into the db
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


# Insert some example facts into the db
if not db.session.query(Event).count():
    event_meta = db.session.query(EventMeta).one()
    tag = db.session.query(Tag).all()

    db.session.add_all([
        Event(event_meta_key=event_meta.id),
        TagBridge(tag_bridge_key=1, tag_key=tag[0].id),
        TagBridge(tag_bridge_key=1, tag_key=tag[1].id),
        TagBridge(tag_bridge_key=1, tag_key=tag[2].id),
    ])

    db.session.add_all([
	Conversation(tag_bridge_key=1, event_meta_key=1)
    ])

    db.session.commit()


sql = (
"select url,group_concat(TagDimension.text)"
" from"
" EventMetaDimension"
" join ConversationFact on ( EventMetaDimension.id = ConversationFact.event_meta_key )"
" join TagBridge on (TagBridge.tag_bridge_key = ConversationFact.tag_bridge_key)"
" join TagDimension on ( TagBridge.tag_key = TagDimension.id )"
)

result = db.session.execute(sql)

# HOOKS
def pre_get_callback(resource, request, lookup):
    oplog_push(resource, None, "GET")

app.on_pre_GET += pre_get_callback

@app.route('/events/tags')
def event_tags():
    app.logger.info(result)
    app.logger.info(sql)
    for row in result:
    	app.logger.info(row[0])
    return "here"


app.run(host='0.0.0.0', use_reloader=False)

