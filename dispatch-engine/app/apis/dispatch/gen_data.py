"""This module generates sample data to send via POST request."""

from pprint import pprint
from typing import Dict, List


class GenData:
    """Generates parcel & delivery agent data."""

    def __init__(
        self,
        # common property among parcels and agent
        hub_id: int,
        # parcel properties
        parcel_ids: List[int],
        area_ids: List[int],
        # agent properties
        agent_ids: List[int],
    ) -> None:

        self.hub_id = hub_id  # This should be the same in a collection
        self.parcel_ids = parcel_ids
        self.area_ids = area_ids

        self.agent_ids = agent_ids

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

    def gen_agents(self) -> List[Dict[str, int]]:
        """Generates a list of delivery agent's data."""

        hub_ids = [self.hub_id] * len(self.agent_ids)
        agents = [
            self._gen_agent(hub_id, agent_id)
            for hub_id, agent_id in zip(hub_ids, self.agent_ids)
        ]
        return agents

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
    def _gen_agent(hub_id: int, agent_id: int) -> Dict[str, int]:
        """Generates one delivery agent data."""

        agent = {
            "hub_id": hub_id,
            "agent_id": agent_id,
        }
        return agent


if __name__ == "__main__":
    gendata = GenData(
        hub_id=1,
        parcel_ids=list(range(100, 120)),
        area_ids=list(range(200, 220)),
        agent_ids=list(range(300, 305)),
    )
    parcels = gendata.gen_parcels()
    agents = gendata.gen_agents()

    parcels_agents_input = {"data": {"parcels": parcels, "agents": agents}}

    pprint(parcels_agents_input)
