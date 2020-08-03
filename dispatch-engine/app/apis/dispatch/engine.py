"""
This is the heart of the source code that makes everything else tick.

Class Description:
------------------

    Class Algo implements the parcel dispatch algorithm
    Class DispatchEngine applies the algorithm on real data
"""

import csv
from contextlib import suppress
from typing import Any, Dict, Generator, List


class Algo:
    """Parcel dispatch algorithm."""

    @staticmethod
    def ordered_chunk(seq: list, n: int) -> Generator[List, None, None]:
        """Yield n number of ordered chunks from seq."""

        if n == 0:
            print("Binsize cannot be zero.")

        elif isinstance(n, float):
            print("Binsize cannot be a float.")

        with suppress(ZeroDivisionError, TypeError):
            k, m = divmod(len(seq), n)

            return (
                seq[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n)
            )


class DispatchEngine:
    """Applies the parcel dispatch algorithm implemented in the class
    Algo on real data."""

    def __init__(
        self, algo: Algo, parcels: List[Dict[str, int]], agents: List[Dict[str, int]],
    ) -> None:

        self.algo = algo
        self.parcels = parcels
        self.agents = agents

    def dispatch(self) -> Generator[List, None, None]:
        return self.algo.ordered_chunk(self.parcels, len(self.agents))

    @classmethod
    def dispatch_hook(cls, algo, parcels, agents) -> Dict[int, Any]:
        """Making this a classmethod is necessary for this task to be
        consumed by rq worker."""

        instance = cls(algo, parcels, agents)
        dispatched = instance.dispatch()
        agent_ids = [d["agent_id"] for d in instance.agents]
        agent_parcels = {k: v for k, v in zip(agent_ids, list(dispatched))}
        return agent_parcels

    @classmethod
    def send_csv(cls, agent_parcels: Dict[int, Any], filename=None):
        """Converting the output of dispatch_hook into csv."""

        fields = ["agent_id", "area_id", "hub_id", "parcel_id"]

        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for agent_id, parcels in agent_parcels.items():
                for row in parcels:
                    row["agent_id"] = agent_id
                    writer.writerow(row)


from functools import partial

# binding the classmethods to make them work like functions
dispatch_hook = partial(DispatchEngine.dispatch_hook, algo=Algo)
send_csv = partial(DispatchEngine.send_csv, algo=Algo)
