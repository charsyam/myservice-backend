from api.worker.queue_manager import WORKER_QUEUE_MANAGER, ALLJOB_QUEUE
from api.shorturl.manager.shard_manager import ShortUrlShardManager, get_shard_manager
from api.shorturl.service.shorturl_service import ShortUrlService


SHORTURL_CREATED_ITEM_TYPE = "SHORTURL_CREATED"

if __name__ == "__main__":
    shard_manager: ShortUrlShardManager = get_shard_manager()
    shorturl_service = ShortUrlService(shard_manager)

    while True:
        item = WORKER_QUEUE_MANAGER.get_item()
        print(item)

        if not item:
            continue

        if item["item_type"] == SHORTURL_CREATED_ITEM_TYPE:
            resp = shorturl_service.insert_shorturl(item["params"]) 
            shard_manager.commit()
            print(resp)

