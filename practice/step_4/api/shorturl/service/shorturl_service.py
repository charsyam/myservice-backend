from api.shorturl.repository.shorturl_repository import ShortUrlRepository
from api.shorturl.converter.shorturl_converter import ShortUrlConverter
from api.shorturl.repository.visit_history_repository import VisitHistoryRepository
from api.shorturl.entity.shorturl import ShortUrl
import json
import time
import uuid

from api.shorturl.entity.visit_history import VisitHistory
from exceptions import *
from api.common.cache.cache import CacheService
from core.utils.mapper import json_serializer
from api.common.logger import logger


class ShortUrlService:
    def __init__(self, db):
        self.db = db
        self.shorturl_repository = ShortUrlRepository(db)
        self.cache_service = CacheService()

    def create(self, source, account):
        shorturl_value = str(uuid.uuid4())
        shorturl = ShortUrl(user_id=account.id, shorturl=shorturl_value, user_uid=account.uid, source=source, status='REGISTERED')
        self.shorturl_repository.save(shorturl)
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
