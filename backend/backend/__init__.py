import json
import os
import flask
from flask import Flask, g

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

RDB_HOST =  os.environ.get('RDB_HOST') or 'localhost'
RDB_PORT = os.environ.get('RDB_PORT') or 28015
RDB_DB = 'courses'

app = Flask(__name__, static_folder='../../public', static_url_path='')
app.config.from_object(__name__)

app.config['facebook'] = {
    'key': '478856265465801',
    'secret': os.environ['FACEBOOK_CLIENT_SECRET']
}

@app.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=RDB_DB)
    except RqlDriverError:
        abort(503, "No database connection could be established.")

@app.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass

import backend.views
