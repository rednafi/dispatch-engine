# This a dummy module
# This gets called in the module_main.py file

from app.apis.dispatch.tools_queue import q
from app.apis.dispatch.engine import GenData, Algo, dispatch_hook

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


def start_queue():
    while True:
        time.sleep(5)
        job = q.enqueue(
            dispatch_hook,
            kwargs={"algo": algo, "parcels": parcels, "persons": persons},
        )
        time.sleep(2)
        print(job.result)


start_queue()
