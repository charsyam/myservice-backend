from dataclasses import asdict
from database import WORKER_QUEUE_HOST
from core.utils.mapper import json_serializer

import json
import redis


ALLJOB_QUEUE = "alljob"


class QueueManager:
    def __init__(self):
        self.queue = redis.Redis(host=WORKER_QUEUE_HOST[0], port=WORKER_QUEUE_HOST[1], decode_responses=True)

    def build_key(self, key):
        return f"queue_{key}"

    def add_item(self, item_type, params):
        item = { "item_type": item_type, "params": params }
        self.queue.rpush(self.build_key(ALLJOB_QUEUE), json.dumps(item, default=json_serializer))

    def get_item(self):
        bvalue = self.queue.blpop(self.build_key(ALLJOB_QUEUE))
        if bvalue:
            v = json.loads(bvalue[1])

        return v


WORKER_QUEUE_MANAGER = QueueManager()
