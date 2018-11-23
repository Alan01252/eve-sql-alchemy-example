import json

def on_insert_totp_callback(entries):
    for entry in entries:
        print(entry)
        entry['another_token'] = pyotp.random_base32()

def on_post_POST_totp(request, payload):
    data = payload.get_data()
    json_data = json.loads(data)
    json_data["test"] = "test"
    payload.set_data(json.dumps(json_data))

def on_pre_POST_totp(request):
    # Request object can't be modified
    pass

def on_fetched_item_totp(response):
    print("fetched")
    print(response)


def add(app):
    app.on_fetched_item_totp += on_fetched_item_totp
    app.on_insert_totp += on_insert_totp_callback
    app.on_post_POST_totp += on_post_POST_totp
    app.on_pre_POST_totp += on_pre_POST_totp