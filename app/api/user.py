
from flask import (Blueprint, request, jsonify, send_file)
from ..tasks import celery
from ..tasks import generate_matches

"""
User API Endpoints
"""

user = Blueprint('user', __name__, url_prefix='/api/v1/user')

@user.route('/records', methods=['POST'])
def records():
    file = request.files['file']
    threshold = request.form.get('threshold')

    if not file.filename.endswith('.csv'):  # Check if .csv file
        return jsonify('Only .csv files are supported'), 400

    f = file.read().decode('latin-1')
    if f.splitlines()[0] != "id,name":  # Check if .csv has the correct format
        return jsonify('Only .csv files with id, name columns are supported'), 400

    if float(threshold) < 0.0 or float(threshold) > 1.0: # Check threshold value is in acceptable range
        return jsonify('Only threshold values in range 0.0 - 1.0 are supported'), 400

    result = generate_matches.delay(f, threshold)
    return jsonify({ 'id': result.id, 'status': result.status }), 200

@user.route('/matches/<task_id>', methods=['GET'])
def matches(task_id):
    result = celery.AsyncResult(task_id)
    if result.ready(): # Task completed
        return send_file('static/matches_' + task_id + '.csv', mimetype='text/csv', attachment_filename='matches_' + task_id + '.csv', as_attachment=True)
    else:
        if result.state == 'MATCHING_IN_PROGRESS' or result.status == 'FILE_IN_CREATION':
            return jsonify({ 'id': result.id, 'status': result.status, 'info': result.info }), 200
        else:
            return jsonify({ 'id': result.id, 'status': result.status }), 200
