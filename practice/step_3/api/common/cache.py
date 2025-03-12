import json

from core.utils.mapper import json_serializer
from api.common.redis_conn import get_redis_conn


g_conn = get_redis_conn()
SHORTURL_CACHE_PREFIX = "shorturl"


class CacheService:
    def __init__(self):
        self.conn = g_conn 

    def get_key(self, prefix, sub_key):
        return f"{prefix}:{sub_key}"

    def get_shorturl(self, shorturl):
        value = self.conn.get(self.get_key(SHORTURL_CACHE_PREFIX, shorturl))
        if value:
            return json.loads(value.decode('utf-8'))

        return None

    def set_shorturl(self, shorturl, value):
        self.conn.set(self.get_key(SHORTURL_CACHE_PREFIX, shorturl),
                      json.dumps(value.to_dict(), default=json_serializer))

        
