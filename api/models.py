from uuid import uuid4

from api import strings
from api.wsgi import db


class OperationResult:
    def __init__(self, result, description=None):
        self.result = result
        self.description = description


class Response:
    def __init__(self, result, description=None, addition=None):
        self.result = result
        self.addition = addition if addition else {}
        self.description = description if description else {}

    def to_dict(self):
        return {
            'status': 200 if self.result else 400,
            'result': self.result,
            'addition': self.addition,
            'description': self.description
        }


class Account(db.Model):
    id = db.Column(db.String(40), primary_key=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    current_balance = db.Column(db.Float, nullable=False)
    holds = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    # last_subtract = db.Column(db.DateTime)

    @staticmethod
    def create(name, current_balance, holds, status, account_id=None):
        if current_balance < 0 or holds < 0:
            return OperationResult(result=False, description={'error': strings.WRONG_DATA})

        if not account_id:
            account_id = str(uuid4())
        db.session.add(Account(id=account_id, name=name, current_balance=current_balance, holds=holds, status=status))
        db.session.commit()
        return OperationResult(result=True, description=account_id)

    @staticmethod
    def get(account_id):
        return Account.query.get(account_id)

    @staticmethod
    def subtract(account_id, substraction):
        account = Account.get(account_id)
        if not account:
            return OperationResult(result=False, description={'error': strings.ACCOUNT_DOES_NOT_EXIST})

        if not account.status or account.current_balance - account.holds - substraction < 0:
            return OperationResult(result=False, description={'error': strings.OPERATION_NOT_POSSIBLE})

        account.holds += round(substraction, 2)
        db.session.commit()
        return OperationResult(result=True)

    @staticmethod
    def add(account_id, sum):
        account = Account.get(account_id)
        if not account:
            return OperationResult(result=False, description={'error': strings.ACCOUNT_DOES_NOT_EXIST})

        if not account.status:
            return OperationResult(result=False, description={'error': strings.OPERATION_NOT_POSSIBLE})

        account.current_balance += round(sum, 2)
        db.session.commit()
        return OperationResult(result=True)

    @staticmethod
    def get_info(account_id):
        account = Account.get(account_id)
        if not account:
            return OperationResult(result=False, description={'error': strings.ACCOUNT_DOES_NOT_EXIST})

        return OperationResult(result=True, description={
            'current_balance': round(account.current_balance, 2),
            'holds': round(account.holds, 2),
            'status': account.status
        })

    @staticmethod
    def subtract_holds(account_id):
        account = Account.get(account_id)
        if not account or not account.status or account.current_balance < account.holds:
            return
        account.current_balance -= account.holds
        account.holds = 0
        db.session.commit()
