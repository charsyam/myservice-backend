from api.shorturl.repository.shorturl_repository import ShortUrlRepository
from api.shorturl.converter.shorturl_converter import ShortUrlConverter
from api.shorturl.repository.visit_history_repository import VisitHistoryRepository
from api.shorturl.entity.shorturl import ShortUrl
import json
import time

from api.shorturl.entity.visit_history import VisitHistory
from exceptions import *
from api.common.cache import CacheService
from core.utils.mapper import json_serializer
from api.common.logger import logger


class ShortUrlService:
    def __init__(self, db):
        self.shorturl_repository = ShortUrlRepository(db)
        self.visit_history_repository = VisitHistoryRepository(db)
        self.cache_service = CacheService()

    def create(self, source, account):
        shorturl = ShortUrl(user_id=account.id, user_uid=account.uid, source=source, status='REGISTERED')
        self.shorturl_repository.save(shorturl)
        return ShortUrlConverter.to_dto(shorturl)

    def get_shorturl(self, url, request_ip = None):
        t1 = time.perf_counter_ns()
        cache_value = self.cache_service.get_shorturl(url)
        t2 = time.perf_counter_ns()
        result = None
        flag = "cache"
        if not cache_value:
            flag = "db"
            shorturl = self.shorturl_repository.find_by_shorturl(url)
            t3 = time.perf_counter_ns()
            if not shorturl:
#                self.cache_service.set_shorturl(url, {})
                raise ShortUrlNotExistException(url)
            
            self.cache_service.set_shorturl(url, shorturl)
            t4 = time.perf_counter_ns()
        else:
            t3 = time.perf_counter_ns()
#            if len(cache_value.keys()) == 0:
#                raise ShortUrlNotExistException(url)
            shorturl = ShortUrl.from_dict(cache_value)
            t4 = time.perf_counter_ns()
        
        logger.info(f"{flag}, cache: {t2-t1} db or null: {t3-t2} {t4-t3}")
        return ShortUrlConverter.to_dto(shorturl)
