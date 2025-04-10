from api.worker.workers.shorturl_created_worker import ShortUrlCreatedWorker

ALL_WORKERS = [ShortUrlCreatedWorker]

def build_worker_map(params):
    worker_map = {}

    for WORKER_CLASS in ALL_WORKERS:
        worker = WORKER_CLASS(params)
        worker_map[worker.event_type()] = worker

    return worker_map
