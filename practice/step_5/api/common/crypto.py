from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Depends, Path, HTTPException, Request, Header
from sqlalchemy.orm import Session

from database import get_session
from api.auth.service.certificate_service import CertificateService


def get_private_key(db: Session, certificate_id: int):
    certificate_service = CertificateService(db)
    return certificate_service.get_private_key(certificate_id)
