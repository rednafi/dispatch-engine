"""
When a new request is placed, this module starts the tasks and
sends them to three different queues.

The first one applies the dispatch algorithm via the dispatch_hook method
The second one sends csv file to the destination
"""


import time
from pprint import pprint

from app.apis.dispatch.engine import Algo, GenData, dispatch_hook, send_csv
from app.apis.dispatch.queues import q_dispatch_hook, q_send_csv

# get the data
gen = GenData(
    hub_id=0,
    parcel_ids=list(range(100, 120)),
    area_ids=list(range(1000, 1020)),
    person_ids=list(range(20, 26)),
)

parcels = gen.gen_parcels()
persons = gen.gen_person()
algo = Algo()


class StartQueues:
    """Initiates the task queues when a request is incurred."""

    def __init__(self, parcels, persons, algo, filename) -> None:
        self.parcels = parcels
        self.persons = persons
        self.algo = algo
        self.filename = filename

    def start(self):
        time.sleep(5)

        # start the first queue
        job_dispatch_hook = q_dispatch_hook.enqueue(
            dispatch_hook,
            kwargs={"algo": self.algo, "parcels": self.parcels, "persons": persons},
            job_id="dh-1",
        )
        # get the result from the first task
        job_dispatch_hook_result = q_dispatch_hook.fetch_job("dh-1").result

        # start the second that depends on the first queue
        job_send_csv = q_send_csv.enqueue(
            send_csv,
            kwargs={
                "person_parcels": job_dispatch_hook_result,
                "filename": self.filename,
            },
            depends_on=job_dispatch_hook,
        )
        time.sleep(2)
        pprint(job_dispatch_hook.result)


i = 0
while i < 1:
    sq = StartQueues(parcels, persons, algo, f"{i}.csv")
    sq.start()
    i += 1
