from contextlib import suppress
from pprint import pprint
from typing import Any, Dict, Generator, List, Tuple


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
        """Generate a list of parcels' data."""

        hub_ids = [self.hub_id] * len(self.parcel_ids)
        parcels = [
            self._gen_parcel(hub_id, parcel_id, area_id)
            for hub_id, parcel_id, area_id in zip(
                hub_ids, self.parcel_ids, self.area_ids
            )
        ]
        return parcels

    def gen_person(self) -> List[Dict[str, int]]:
        """Generate a list of delivery person's data."""

        hub_ids = [self.hub_id] * len(self.person_ids)
        persons = [
            self._gen_person(hub_id, person_id)
            for hub_id, person_id in zip(hub_ids, self.person_ids)
        ]
        return persons

    @staticmethod
    def _gen_parcel(hub_id: int, parcel_id: int, area_id: int) -> Dict[str, int]:
        """Generate one parcel data."""

        parcel = {
            "hub_id": hub_id,
            "parcel_id": parcel_id,
            "area_id": area_id,
        }
        return parcel

    @staticmethod
    def _gen_person(hub_id: int, person_id: int) -> Dict[str, int]:
        """Generate one delivery person data."""

        person = {
            "hub_id": hub_id,
            "person_id": person_id,
        }
        return person


class Algo:
    """Primary parcel dispatch algorithm."""

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


dispatch_hook = DispatchEngine.dispatch_hook
