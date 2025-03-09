from datetime import datetime, timedelta
import random
import uuid
import argon2

from api.user.repository.account_repository import AccountRepository
from api.auth.converter.token_converter import TokenConverter
from api.auth.entity.token import Token
from exceptions import *
from core.utils.token import create_token, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from core.utils.crypto.password import password_verify





class AuthService:
    def __init__(self, db):
        self.account_repository = AccountRepository(db)

    def login(self, email, password, request_ip):
        account = self.account_repository.find_by_email(email)
        if not account:
            raise UserNotExistException(email)

        try:
            password_verify(account.password, password)
        except argon2.exceptions.VerifyMismatchError:
            raise PasswordMismatchException(email) 
        except Exception as e:
            raise InvalidParameterException(str(e))
            
            

        now = datetime.now()
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        uuid4_value = str(uuid.uuid4())
        access_token = create_token(data={"sub": account.email, "uuid": uuid4_value}, expires_delta=access_token_expires)
        refresh_token = create_token(data={"sub": account.email, "uuid": uuid4_value, "type": "refresh"}, expires_delta=refresh_token_expires)

        token = Token(
            user_id = account.id,
            user_uid = account.uid,
            access_token = access_token,
            refresh_token = refresh_token,
            request_ip = request_ip,
            access_token_expired_at = now+access_token_expires,
            refresh_token_expired_at = now+refresh_token_expires,
            status = "REGISTERED",
        )

        return TokenConverter.to_dto(self.account_repository.save(token))
