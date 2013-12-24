import urllib2
import facebook
from functools import wraps
from flask import g, request, redirect, url_for, abort, current_app

# Puts uid in the global object if the Facebook cookie
# has been signed correctly.
def login_required(f):
    @wraps(f)

    def decorated_function(*args, **kwargs):
        try:
            app_id = current_app.config['facebook']['key']
            secret = current_app.config['facebook']['secret']
            cookie = request.cookies.get("fbsr_" + app_id, "")
            signed_request = facebook.parse_signed_request(cookie, secret)
        except None, e:
            return abort(400, "User needs to reauthorize")

        if signed_request.get('user_id'):
            g.uid = int(signed_request['user_id'])
        else:
            return abort(400, "User does not have a valid cookie")
        return f(*args, **kwargs)
    return decorated_function

def schedule_id_format(uid, semester):
    return "%s:%s" % (uid, semester)
