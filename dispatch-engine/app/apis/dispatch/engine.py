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


class GenData:
    """Generates parcel & delivery person data."""

    def __init__(
        self,
        # common property among parcels and person
        hub_id: int,
        # parcel properties
        parcel_ids: List[int],
        area_ids: List[int],
        # person properties
        person_ids: List[int],
    ) -> None:

        self.hub_id = hub_id  # This should be the same in a collection

        self.parcel_ids = parcel_ids
        self.area_ids = area_ids

        self.person_ids = person_ids

    def gen_parcels(self) -> List[Dict[str, int]]:
        """Generates a list of parcels' data."""

        hub_ids = [self.hub_id] * len(self.parcel_ids)
        parcels = [
            self._gen_parcel(hub_id, parcel_id, area_id)
            for hub_id, parcel_id, area_id in zip(
                hub_ids, self.parcel_ids, self.area_ids
            )
        ]
        return parcels

    def gen_persons(self) -> List[Dict[str, int]]:
        """Generates a list of delivery person's data."""

        hub_ids = [self.hub_id] * len(self.person_ids)
        persons = [
            self._gen_person(hub_id, person_id)
            for hub_id, person_id in zip(hub_ids, self.person_ids)
        ]
        return persons

    @staticmethod
    def _gen_parcel(hub_id: int, parcel_id: int, area_id: int) -> Dict[str, int]:
        """Generates one parcel data."""

        parcel = {
            "hub_id": hub_id,
            "parcel_id": parcel_id,
            "area_id": area_id,
        }
        return parcel

    @staticmethod
    def _gen_person(hub_id: int, person_id: int) -> Dict[str, int]:
        """Generates one delivery person data."""

        person = {
            "hub_id": hub_id,
            "person_id": person_id,
        }
        return person


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
        self, algo: Algo, parcels: List[Dict[str, int]], persons: List[Dict[str, int]],
    ) -> None:

        self.algo = algo
        self.parcels = parcels
        self.persons = persons

    def dispatch(self) -> Generator[List, None, None]:
        return self.algo.ordered_chunk(self.parcels, len(self.persons))

    @classmethod
    def dispatch_hook(cls, algo, parcels, persons) -> Dict[int, Any]:
        """Making this a classmethod is necessary for this task to be
        consumed by rq worker."""

        instance = cls(algo, parcels, persons)
        dispatched = instance.dispatch()
        person_ids = [d["person_id"] for d in instance.persons]
        person_parcels = {k: v for k, v in zip(person_ids, list(dispatched))}
        return person_parcels

    @classmethod
    def send_csv(cls, person_parcels: Dict[int, Any], filename=None):
        """Converting the output of dispatch_hook into csv."""

        fields = ["person_id", "area_id", "hub_id", "parcel_id"]

        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for person_id, parcels in person_parcels.items():
                for row in parcels:
                    row["person_id"] = person_id
                    writer.writerow(row)


# binding the classmethods to make them work like functions
dispatch_hook = DispatchEngine.dispatch_hook
send_csv = DispatchEngine.send_csv


