from api.worker.worker import Worker
from api.event.event_type import *
from api.shorturl.service.shorturl_service import ShortUrlService


class ShortUrlCreatedWorker(Worker):
    def __init__(self, params):
        self._event_type = SHORTURL_CREATED_EVENT
        self.shard_manager = params["shard_manager"]
        self.shorturl_service = ShortUrlService(self.shard_manager)

    def match(self, item_type):
        return item_type == self._event_type        

    def event_type(self):
        return self._event_type

    def process(self, item):
        if not self.match(item["item_type"]):
            raise Exception(f"Not supported: {item['item_type']}") 
        
        print(f"Handle: {item}")
        self.shorturl_service.insert_shorturl(item["params"])
        self.shard_manager.commit()
