from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from jwt import PyJWTError
import jwt

from exceptions import *

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
SECRET_KEY = "insight1234"


def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)

    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
        exp = int(payload["exp"])
        now = int(datetime.now().timestamp())

        if exp < now:
            raise ExpiredTokenException("Expired Token")

        return payload
    except ExpiredTokenException as e:
        raise e
    except Exception as e:
        raise InvalidParameterException("Invalid token")
