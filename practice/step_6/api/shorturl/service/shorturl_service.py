from api.shorturl.repository.shorturl_repository import ShortUrlRepository
from api.shorturl.converter.shorturl_converter import ShortUrlConverter
from api.shorturl.repository.visit_history_repository import VisitHistoryRepository
from api.shorturl.entity.shorturl import ShortUrl
from api.shorturl.model.shorturl import ShortUrl as ShortUrlDto
import json
import time
import uuid

from datetime import datetime
from api.shorturl.entity.visit_history import VisitHistory
from exceptions import *
from api.common.cache.cache import CacheService
from core.utils.mapper import json_serializer
from api.common.logger import logger
from api.worker.queue_manager import WORKER_QUEUE_MANAGER
from api.event.event_type import *


class ShortUrlService:
    def __init__(self, shard_manager):
        self.shard_manager = shard_manager
        self.shorturl_repository = ShortUrlRepository(shard_manager)
        self.cache_service = CacheService()

    def insert_shorturl(self, shorturl):
        shorturl = ShortUrl(
            uid=shorturl["uid"],
            user_id=shorturl["user_id"],
            user_uid=shorturl["user_uid"],
            source=shorturl["source"],
            shorturl=shorturl["shorturl"],
            status=shorturl["status"],
            created_at=datetime.fromisoformat(shorturl["created_at"]),
        )

        self.shorturl_repository.save(shorturl)
        return ShortUrlConverter.to_dto(shorturl)


    def create(self, source, account):
        shorturl_value = str(uuid.uuid4())
        shorturl = ShortUrlDto(
            uid=str(uuid.uuid4()),
            user_id = account.id,
            user_uid = account.uid,
            source = source,
            shorturl = shorturl_value,
            status = "REGISTERED",
            created_at = datetime.now()
        )
 
        params = ShortUrlConverter.to_dict(shorturl)
        self.cache_service.set_shorturl(shorturl.shorturl, params)
        WORKER_QUEUE_MANAGER.add_item(SHORTURL_CREATED_EVENT, params=params)
        return ShortUrlConverter.to_dto(shorturl)

    def get_shorturl(self, url, request_ip = None):
        cache_value = self.cache_service.get_shorturl(url)
        if not cache_value:
            shorturl = self.shorturl_repository.find_by_shorturl(url)
            if not shorturl:
                raise ShortUrlNotExistException(url)

            self.cache_service.set_shorturl(url, shorturl)
        else:
            shorturl = ShortUrl.from_dict(cache_value)

        return ShortUrlConverter.to_dto(shorturl)
