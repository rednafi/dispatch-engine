"""
This module establishes the redis connection necessary for messaging
and defines the task queues.
"""

from app.core.config import config
from redis import Redis
from rq import Queue

redis_connection = Redis(
    config.REDIS_HOST, config.REDIS_PORT, password=config.REDIS_PASSWORD
)

q_dispatch_hook = Queue(name="dispatch-hook", connection=redis_connection)
q_send_csv = Queue(name="send-csv", connection=redis_connection)
