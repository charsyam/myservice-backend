from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi.responses import JSONResponse
from database import get_session
from sqlalchemy.orm import Session
from typing import Any, Dict

from api.user.model.account import Account
from api.shorturl.service.shorturl_service import ShortUrlService
from api.common.response import Response
from api.common.token import verify_token
from api.common.utils.client import get_client_ip
from api.shorturl.manager.shard_manager import ShortUrlShardManager, get_shard_manager



router = APIRouter(prefix="/api/shorturl/v1")


@router.post("/shorturl")
def create(
    request: Dict[str, Any],
    account: Account = Depends(verify_token),
    response_model=Response,
    shard_manager: ShortUrlShardManager = Depends(get_shard_manager)
):
    shorturl_service = ShortUrlService(shard_manager)

    body = request["body"]
    source = body["source"]

    shorturl = shorturl_service.create(source, account)
    shard_manager.commit() 
    return Response(body={"shorturl": shorturl})

@router.post("/shorturl/noauth")
def create(
    response_model=Response,
    shard_manager: ShortUrlShardManager = Depends(get_shard_manager)
):
    shorturl_service = ShortUrlService(shard_manager)

    source = "https://www.naver.com"

    account = Account(
        id = 1,
        uid = "66eb7036-0d24-4c2a-9451-fe966699515d",        
        email = "",
        status = "REGISTERED"
    )

    shorturl = shorturl_service.create(source, account)
    shard_manager.commit()
    return Response(body={"shorturl": shorturl})


@router.get("/shorturl/{url}")
def visit_shorturl(
    url: str,
    request: Request,
    shard_manager: ShortUrlShardManager = Depends(get_shard_manager)
):
    shorturl_service = ShortUrlService(shard_manager)
    request_ip = get_client_ip(request)
    shorturl = shorturl_service.get_shorturl(url, request_ip)
    if not shorturl:
        raise ShortUrlNotExistException(url)

    return Response(body={"shorturl": shorturl})
