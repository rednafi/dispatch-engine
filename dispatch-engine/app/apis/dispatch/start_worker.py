from rq import Worker
from app.apis.dispatch.tools_queue import q, redis_connection


def start_worker():
    worker = Worker(queues=[q], connection=redis_connection)
    worker.work()


start_worker()
