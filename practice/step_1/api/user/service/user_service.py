from api.user.repository.account_repository import AccountRepository
from api.user.converter.account_converter import AccountConverter
from api.user.entity.account import Account

from exceptions import *


class UserService:
    def __init__(self, db):
        self.repository = AccountRepository(db)

    def register_user(self, email, password):
        account = self.repository.find_by_email(email, "REGISTERED")
        if account:
            raise UserAlreadyExistException(email)

        account = Account(
            email = email,
            password = password,
            status = 'REGISTERED',
        ) 

        account = self.repository.save(account)
        return AccountConverter.to_dto(account)

    def get_user(self, email, status='REGISTERED'):
        account = self.repository.find_by_email(email, status)
        if not account:
            raise UserNotExistException(email)

        return AccountConverter.to_dto(account)
