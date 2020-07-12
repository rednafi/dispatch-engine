from redis import Redis
from rq import Queue

redis_connection = Redis()

q_dispatch_hook = Queue(name="dispatch-hook", connection=redis_connection)
q_send_csv = Queue(name="send-csv", connection=redis_connection)
