from api.worker.queue_client import QueueClient
from database import WORKER_QUEUE_HOST


import redis


class RedisQueueClient(QueueClient):
    def __init__(self):
        self.conn = redis.Redis(host=WORKER_QUEUE_HOST[0], port=WORKER_QUEUE_HOST[1], decode_responses=True)

    def build_key(self, key):
        return f"queue_{key}"

    def push(self, key, value):
        return self.conn.rpush(self.build_key(key), value)
        
    def pop(self, key):
        bvalue = self.conn.blpop(self.build_key(key))
        return bvalue[1]
