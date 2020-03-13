from uuid import uuid4

from api import strings
from api.wsgi import db


class Account(db.Model):
    id = db.Column(db.String(40), primary_key=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    current_balance = db.Column(db.Integer, nullable=False)
    holds = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    # last_subtract = db.Column(db.DateTime)

    @staticmethod
    def create(name, current_balance, holds, status):
        if current_balance < 0 or holds < 0:
            return False, strings.WRONG_DATA
        account_id = str(uuid4())
        db.session.add(Account(id=account_id, name=name, current_balance=current_balance, holds=holds, status=status))
        db.session.commit()
        return True, account_id

    @staticmethod
    def get(account_id):
        return Account.query.get(account_id)

    @staticmethod
    def subtract(account_id, substraction):
        account = Account.query.get(account_id)
        if not account or not account.status:
            return False, strings.ACCOUNT_DOES_NOT_EXIST
        if account.current_balance - account.holds - substraction < 0:
            return False, strings.OPERATION_NOT_POSSIBLE
        account.holds += substraction
        db.session.commit()
        return True, ''

    @staticmethod
    def add(account_id, amount):
        account = Account.query.get(account_id)
        if not account or not account.status:
            return False, strings.ACCOUNT_DOES_NOT_EXIST
        account.current_balance += amount
        db.session.commit()
        return True, ''

    @staticmethod
    def subtract_holds(account_id):
        account = Account.query.get(account_id)
        if not account or not account.status or account.current_balance < account.holds:
            return
        account.current_balance -= account.holds
        account.holds = 0
        db.session.commit()
