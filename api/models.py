from typing import Optional, Type, Union
from uuid import uuid4

from api import strings
from api.wsgi import db


class OperationResult:
    """
    Class for reporting database operation results.
    """
    result: bool
    description: dict

    def __init__(self, result: bool, description: Optional[dict] = None):
        self.result = result
        self.description = description if description else {}


class Response:
    """
    Class creating http responses.
    """
    result: bool
    addition: dict
    description: dict

    def __init__(self, result: bool, description: Optional[dict] = None, addition: Optional[dict] = None):
        self.result = result
        self.addition = addition if addition else {}
        self.description = description if description else {}

    def to_dict(self) -> dict:
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
    def create(name: str, current_balance: Union[int, float], holds: Union[int, float], status: bool,
               account_id: Optional[str] = None) -> OperationResult(Type[bool], Optional[dict]):
        """
        Create new Account and return it's account_id.
        If account_id is not defined, then account_id = uuid4.
        """
        if current_balance < 0 or holds < 0:
            return OperationResult(result=False, description={'error': strings.WRONG_DATA_ERROR})

        if not account_id:
            account_id = str(uuid4())
        db.session.add(Account(id=account_id, name=name, current_balance=current_balance, holds=holds, status=status))
        db.session.commit()
        return OperationResult(result=True, description={'uuid': account_id})

    @staticmethod
    def get(account_id: str):
        """Get account by account_id."""
        return Account.query.get(account_id)

    @staticmethod
    def subtract(account_id: str, substraction: Union[int, float]) -> OperationResult(Type[bool], Optional[dict]):
        """
        Add substraction to holds if (holds + substracrion) <= current_balance.
        """
        account = Account.get(account_id)
        if not account:
            return OperationResult(result=False, description={'error': strings.ACCOUNT_DOES_NOT_EXIST_ERROR})

        if not account.status or account.current_balance - account.holds - substraction < 0:
            return OperationResult(result=False, description={'error': strings.OPERATION_NOT_POSSIBLE_ERROR})

        account.holds += round(substraction, 2)
        db.session.commit()
        return OperationResult(result=True)

    @staticmethod
    def add(account_id, sum) -> OperationResult(Type[bool], Optional[dict]):
        """
        Add sum to current_balance.
        """
        account = Account.get(account_id)
        if not account:
            return OperationResult(result=False, description={'error': strings.ACCOUNT_DOES_NOT_EXIST_ERROR})

        if not account.status:
            return OperationResult(result=False, description={'error': strings.OPERATION_NOT_POSSIBLE_ERROR})

        account.current_balance += round(sum, 2)
        db.session.commit()
        return OperationResult(result=True)

    @staticmethod
    def get_info(account_id) -> OperationResult(Type[bool], Optional[dict]):
        """
        Returns information (current_balance, holds, status) about Account.
        """
        account = Account.get(account_id)
        if not account:
            return OperationResult(result=False, description={'error': strings.ACCOUNT_DOES_NOT_EXIST_ERROR})

        return OperationResult(result=True, description={
            'current_balance': round(account.current_balance, 2),
            'holds': round(account.holds, 2),
            'status': account.status
        })

    # @staticmethod
    # def subtract_holds(account_id):
    #     account = Account.get(account_id)
    #     if not account or not account.status or account.current_balance < account.holds:
    #         return
    #     account.current_balance -= account.holds
    #     account.holds = 0
    #     db.session.commit()
