from flask import Blueprint, current_app as app

event_blueprint = Blueprint('prefix_uri', __name__)

from eve.methods.common import (
    pre_event,
)

sql = (
 "select url,group_concat(tag.text)"
 " from"
 " event_meta"
 " join comment on ( event_meta.id = comment.event_meta )"
 " join comment_tag_bridge on (comment_tag_bridge.comment_id = comment.id)"
 " join tag on ( comment_tag_bridge.tag_id = tag.id )"
 )

from flask import request
@event_blueprint.route('/events?{embedded=tags}', methods=['GET'])
def get_tags():
    db =  app.data.driver
    result = db.session.execute(sql)
    app.logger.info(result)
    app.logger.info(sql)
    for row in result:
        app.logger.info(row[0])
        app.logger.info(row[1])
        return row[1]