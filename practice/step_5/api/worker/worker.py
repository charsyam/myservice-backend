from sqlalchemy.orm import Session

from api.worker.queue_manager import WORKER_QUEUE_MANAGER, ALLJOB_QUEUE
from api.shorturl.manager.shard_manager import ShortUrlShardManager
from api.shorturl.service.shorturl_service import ShortUrlService
from database import get_session


SHORTURL_CREATED_ITEM_TYPE = "SHORTURL_CREATED"

if __name__ == "__main__":
    db: Session = get_session()
    shorturl_service = ShortUrlService(db)

    while True:
        item = WORKER_QUEUE_MANAGER.get_item()
        print(item)

        if not item:
            continue

        if item["item_type"] == SHORTURL_CREATED_ITEM_TYPE:
            resp = shorturl_service.insert_shorturl(item["params"]) 
            shard_manager.commit()
            print(resp)

