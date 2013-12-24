from backend import app
from flask import Flask, g, jsonify, render_template, request, abort, url_for
from helpers import login_required, schedule_id_format
import rethinkdb as r
import hashlib
import base64

@app.route("/api/schedule/<semester>", methods=['GET'])
@login_required
def get_schedule(semester):
    id = schedule_id_format(g.uid, semester)
    doc = r.table('schedule').get(id).run(g.rdb_conn)
    return jsonify(doc)

@app.route("/api/schedule", methods=['POST'])
@login_required
def update_schedule():
    doc = {}
    doc['author'] = g.uid
    doc['sections'] = request.json.get('sections', '')
    doc['semester'] = int(request.json['semester'])
    doc['id'] = schedule_id_format(doc['author'], doc['semester'])
    if len(doc['sections']) == 0:
        return abort(400, "No sections to save.")
    inserted = r.table('schedule').insert(doc, upsert=True).run(g.rdb_conn)
    return jsonify(inserted)

@app.route('/')
def home():
    return app.send_static_file('index.html')
