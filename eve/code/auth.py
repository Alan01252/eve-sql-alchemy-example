from flask import current_app as app
from eve.auth import TokenAuth, BasicAuth
from passlib.hash import pbkdf2_sha256

# Login for initial username and password
class LoginAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        portal_user = app.data.driver.db['portal_user']
        portal_user = portal_user.find_one({'email': username})
        return portal_user and pbkdf2_sha256.verify(password, portal_user['password'])

# login once token has been set
class VoxTokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        return True

