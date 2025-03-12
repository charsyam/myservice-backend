from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from database import get_session
from sqlalchemy.orm import Session
from typing import Any, Dict

from api.user.service.user_service import UserService
from api.auth.service.certificate_service import CertificateService
from api.common.response import Response
from core.utils.crypto.password import password_hasher, decrypt_password


router = APIRouter(prefix="/api/user/v1")


@router.post("/register")
def register_user(
    request: Dict[str, Any],
    db: Session = Depends(get_session),
    response_model=Response,
):
    user_service = UserService(db)
    certificate_service = CertificateService(db)

    body = request["body"]
    certificate_id = int(body["certificate_id"])
    email = body["email"]
    encrypted_password = body["password"]

    private_key = certificate_service.get_private_key(certificate_id)
    password = decrypt_password(private_key, encrypted_password)

    hashed_password = password_hasher(password)

    account = user_service.register_user(email=email, password=hashed_password)
    db.commit() 

    return Response(body={"account": account})
