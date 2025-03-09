from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Depends, Path, HTTPException, Request, Header
from sqlalchemy.orm import Session

from core.utils.token import verify_jwt_token
from database import get_session
from api.user.service.user_service import UserService


def verify_token(authorization: Optional[str] = Header(None), db: Session = Depends(get_session)):
    user_service = UserService(db)

    if not authorization or authorization.split(" ")[0] != "Bearer":
        raise InvalidParameterException("Invalid Authorization header format")

    token = authorization.split(" ")[1]
    account = None
    email = None

    try:
        payload = verify_jwt_token(token)
        email = payload["sub"]
        return user_service.get_user(email)
    except Exception as e:
        raise e
