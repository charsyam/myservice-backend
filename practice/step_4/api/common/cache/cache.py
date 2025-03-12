import json

from database import REDIS_HOSTS
from core.utils.mapper import json_serializer
from api.common.cache.ketama import KatemaConsistentHashing


SHORTURL_CACHE_PREFIX = "shorturl"

ch = KatemaConsistentHashing(REDIS_HOSTS)


class CacheService:
    def __init__(self):
        self.ch = ch

    def get_key(self, prefix, sub_key):
        return f"{prefix}:{sub_key}"

    def get_shorturl(self, shorturl):
        conn = self.ch.get_node(shorturl)
        value = conn.get(self.get_key(SHORTURL_CACHE_PREFIX, shorturl))
        if value:
            print(value)
            return json.loads(value.encode('utf-8'))

        return None

    def set_shorturl(self, shorturl, value):
        conn = self.ch.get_node(shorturl)
        conn.set(self.get_key(SHORTURL_CACHE_PREFIX, shorturl),
                 json.dumps(value.to_dict(), default=json_serializer))
