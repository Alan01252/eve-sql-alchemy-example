import json

def pre_oplog(resource, entries):
    for entry in entries:
        if 'c' in entry:
            entry['c'] = json.dumps(entry['c'])

def add(app):
    app.on_oplog_push += pre_oplog