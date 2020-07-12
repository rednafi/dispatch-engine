from redis import Redis
from rq import Queue

redis_connection = Redis()

q = Queue(name="dispatch-engine", connection=redis_connection)
