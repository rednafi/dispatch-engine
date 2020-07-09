from itertools import chain
from pprint import pprint
from typing import Dict, List, Any, Generator, Tuple, Union, Sequence
from contextlib import suppress


class GenData:
    """Generates parcel & delivery man data."""

    def __init__(
        self,
        # common property among parcels and men
        hub_id: int,
        # parcel properties
        parcel_ids: List[int],
        area_ids: List[int],
        # men properties
        men_ids: List[int],
    ) -> None:

        self.hub_id = hub_id  # This should be the same in a collection

        self.parcel_ids = parcel_ids
        self.area_ids = area_ids

        self.men_ids = men_ids

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

    def gen_men(self) -> List[Dict[str, int]]:
        """Generate a list of delivery men's data."""

        hub_ids = [self.hub_id] * len(self.men_ids)
        men = [
            self._gen_man(hub_id, man_id)
            for hub_id, man_id in zip(hub_ids, self.men_ids)
        ]
        return men

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
    def _gen_man(hub_id: int, man_id: int) -> Dict[str, int]:
        """Generate one delivery man data."""

        man = {
            "hub_id": hub_id,
            "man_id": man_id,
        }
        return man


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
        self, algo: Algo, parcels: List[Dict[str, int]], men: List[Dict[str, int]],
    ) -> None:

        self.algo = algo
        self.parcels = parcels
        self.men = men

    def dispatch(self) -> Generator[List, None, None]:
        return self.algo.ordered_chunk(self.parcels, len(self.men))

    def dispatch_hook(self) -> Dict[int, Any]:
        dispatched = self.dispatch()
        man_ids = [d["man_id"] for d in self.men]
        men_parcels = {k: v for k, v in zip(man_ids, list(dispatched))}
        return men_parcels


if __name__ == "__main__":

    gen = GenData(
        hub_id=0,
        parcel_ids=list(range(100, 120)),
        area_ids=list(range(1000, 1020)),
        men_ids=list(range(20, 26)),
    )

    parcels = gen.gen_parcels()
    men = gen.gen_men()

    algos = Algo()

    de = DispatchEngine(algos, parcels, men)
    pprint(de.dispatch_hook())
