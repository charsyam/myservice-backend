from api.worker.queue_manager import WORKER_QUEUE_MANAGER
from api.worker.workers import build_worker_map
from api.shorturl.manager.shard_manager import get_shard_manager


if __name__ == "__main__":
    params = {
        "shard_manager": get_shard_manager(),
    }

    worker_map = build_worker_map(params)

    while True:
        item = WORKER_QUEUE_MANAGER.get_item()
        if not item:
            continue

        event_type = item["item_type"]
        if event_type in worker_map:
            worker = worker_map[event_type]
            try:
                worker.process(item)
            except Exception as e:
                print(e, item)
        else:
            print(f"Not Supported: {event_type}")
