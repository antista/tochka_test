import json

from flask import request

from api.wsgi import app, db
from api.models import Account, Response
from api import strings

import atexit

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(func=Account.subtract_all_holds, trigger="interval", minutes=10)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

db.drop_all()
db.create_all()

Account.create(account_id='26c940a1-7228-4ea2-a3bc-e6460b172040', name='Петров Иван Сергеевич',
               current_balance=1700, holds=300, status=True)
Account.create(account_id='7badc8f8-65bc-449a-8cde-855234ac63e1', name='Kazitsky Jason',
               current_balance=200, holds=200, status=True)
Account.create(account_id='5597cc3d-c948-48a0-b711-393edf20d9c0', name='ПархоменкоАнтонАлександрович',
               current_balance=10, holds=300, status=True)
Account.create(account_id='867f0924-a917-4711-939b-90b179a96392', name='Петечкин Петр Измаилович',
               current_balance=1000000, holds=1, status=False)


@app.route('/api/ping', methods=['GET'])
def handle_ping_request():
    return json.dumps(Response(result=True).to_dict())


@app.route('/api/add', methods=['POST'])
def handle_add_request():
    if 'addition' not in request.json.keys() or 'uuid' not in request.json['addition'] \
            or 'additional_sum' not in request.json['addition']:
        return json.dumps(Response(result=False,
                                   description={'error': strings.WRONG_DATA_ERROR}).to_dict())

    operation_result = Account.add(account_id=request.json['addition']['uuid'],
                                   sum=request.json['addition']['additional_sum'])
    return json.dumps(Response(result=operation_result.result,
                               description=operation_result.description,
                               addition={'uuid': request.json['addition']['uuid']}).to_dict())


@app.route('/api/substruct', methods=['POST'])
def handle_substruct_request():
    if 'addition' not in request.json.keys() or 'uuid' not in request.json['addition'] \
            or 'substruction_sum' not in request.json['addition']:
        return json.dumps(Response(result=False,
                                   description={'error': strings.WRONG_DATA_ERROR}).to_dict())

    operation_result = Account.subtract(account_id=request.json['addition']['uuid'],
                                        substraction=request.json['addition']['substruction_sum'])
    return json.dumps(Response(result=operation_result.result,
                               description=operation_result.description,
                               addition={'uuid': request.json['addition']['uuid']}).to_dict())


@app.route('/api/status', methods=['GET'])
def handle_status_request():
    if 'addition' not in request.json.keys() or 'uuid' not in request.json['addition']:
        return json.dumps(Response(result=False,
                                   description={'error': strings.WRONG_DATA_ERROR}).to_dict())

    operation_result = Account.get_info(account_id=request.json['addition']['uuid'])
    return json.dumps(Response(result=operation_result.result,
                               description=operation_result.description,
                               addition={'uuid': request.json['addition']['uuid']}).to_dict())
