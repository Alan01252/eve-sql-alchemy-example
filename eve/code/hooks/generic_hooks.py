from eve.methods.common import (
    oplog_push
)
from flask import current_app as app

# HOOKS
def pre_get_callback(resource, request, lookup):
     app.logger.info("pre get fired")
     if resource:
        oplog_push(resource, None, "GET")

def post_get_callback(resource, request, lookup):
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

def add(app):
    app.on_pre_GET += pre_get_callback
    app.on_pre_GET += pre_get_callback
    app.on_post_GET += post_get_callback
    app.on_pre_POST += pre_post_callback
    app.on_pre_PUT += pre_put_callback