from dataclasses import asdict
from database import WORKER_QUEUE_HOST
from core.utils.mapper import json_serializer

import json
import redis

from api.worker.redis_queue_client import RedisQueueClient


ALLJOB_QUEUE = "alljob"


class QueueManager:
    def __init__(self, queue_name, queue_client):
        self.queue_name = queue_name
        self.queue_client = queue_client

    def add_item(self, item_type, params):
        item = { "item_type": item_type, "params": params }
        self.queue_client.push(self.queue_name, json.dumps(item, default=json_serializer))

    def get_item(self):
        value = self.queue_client.pop(self.queue_name)
        if not value:
            return value

        return json.loads(value)


WORKER_QUEUE_MANAGER = QueueManager(ALLJOB_QUEUE, RedisQueueClient())
