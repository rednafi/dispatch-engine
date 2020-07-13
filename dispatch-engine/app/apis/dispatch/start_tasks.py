# This a dummy module
# This gets called in the module_main.py file

from rq import get_current_job
from rq.utils import first
from app.apis.dispatch.queues import q_dispatch_hook, q_send_csv, redis_connection
from app.apis.dispatch.engine import GenData, Algo, dispatch_hook, send_csv

from pprint import pprint
from datetime import timedelta
import time

gen = GenData(
    hub_id=0,
    parcel_ids=list(range(100, 120)),
    area_ids=list(range(1000, 1020)),
    person_ids=list(range(20, 26)),
)

parcels = gen.gen_parcels()
persons = gen.gen_person()
algo = Algo()


def start_queue(i):
    time.sleep(5)
    job_dispatch_hook = q_dispatch_hook.enqueue(
        dispatch_hook,
        kwargs={"algo": algo, "parcels": parcels, "persons": persons},
        job_id="dh-1",
    )

    job_dispatch_hook_result = q_dispatch_hook.fetch_job("dh-1").result
    job_send_csv = q_send_csv.enqueue(
        send_csv,
        kwargs={"person_parcels": job_dispatch_hook_result, "filename": f"{i}.csv"},
        depends_on=job_dispatch_hook,
    )
    time.sleep(2)
    pprint(job_dispatch_hook.result)


i = 0
while i < 1:
    start_queue(i)
    i += 1
