import json

from flask import request

from api.wsgi import app, db
from api.models import User

db.drop_all()
db.create_all()

ERROR_RESPONSE = json.dumps({
    'status': 406,
    'result': False,
    'addition': {},
    'description': {'error': 'Wrong data format.'}
})


@app.route('/')
def hello_world():
    User.create()
    if User.query.filter_by(login='ffff').first() is None:
        return 'None'
    return User.query.filter_by(login='ffff').first().id


@app.route('/api/ping', methods=['GET'])
def ping():
    return json.dumps({
        'status': 200,
        'result': True,
        'addition': {},
        'description': {}
    })


@app.route('/api/add', methods=['POST'])
def add():
    if 'addition' not in request.json or 'uuid' not in request.json['addition']:
        return ERROR_RESPONSE
