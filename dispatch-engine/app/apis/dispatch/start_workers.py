"""
This module starts a single worker that listens to two queues.
"""

from app.apis.dispatch.queues import q_dispatch_hook, q_send_csv, redis_connection
from rq import Worker


def start_worker():
    worker_1 = Worker(queues=[q_dispatch_hook, q_send_csv], connection=redis_connection)
    worker_1.work()


start_worker()
