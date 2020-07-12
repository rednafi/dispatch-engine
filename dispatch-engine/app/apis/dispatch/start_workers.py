from rq import Worker
from app.apis.dispatch.queues import q_dispatch_hook, q_send_csv, redis_connection


def start_worker():
    worker_1 = Worker(queues=[q_dispatch_hook, q_send_csv], connection=redis_connection)
    worker_1.work()


start_worker()
