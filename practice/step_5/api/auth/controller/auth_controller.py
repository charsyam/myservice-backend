from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi.responses import JSONResponse
from database import get_session
from sqlalchemy.orm import Session
from typing import Dict, Any

from api.common.response import Response
from api.auth.service.certificate_service import CertificateService
from api.auth.service.auth_service import AuthService
from api.common.utils.client import get_client_ip
from core.utils.crypto.password import password_hasher, decrypt_password


router = APIRouter(prefix="/api/auth/v1")


@router.get("/public-key")
def get_public_key(
    db: Session = Depends(get_session),
    response_model=Response,
):
    certificate_service = CertificateService(db)
    certificate = certificate_service.get_one_certificate()
    resp = Response(body={"public-key": certificate})

    return resp


@router.post("/login")
def login(
    request: Dict[str, Any],
    r: Request,
    db: Session = Depends(get_session),
    response_model=Response,
):
    certificate_service = CertificateService(db)
    auth_service = AuthService(db)

    body = request["body"]
    certificate_id = int(body["certificate_id"])
    email = body["email"]
    encrypted_password = body["password"]

    private_key = certificate_service.get_private_key(certificate_id)
    password = decrypt_password(private_key, encrypted_password)

    client_ip = get_client_ip(r)
    token = auth_service.login(email=email, password=password, request_ip=client_ip)

    db.commit()
    return Response(body={"token": token})
