"""
Data will go into the body of a get request."""

from typing import List

from pydantic import BaseModel


class Parcel(BaseModel):
    hub_id: int
    parcel_id: int
    area_id: int


class Agent(BaseModel):
    hub_id: int
    agent_id: int


class ParcelsAgents(BaseModel):
    parcels: List[Parcel]
    agents: List[Parcel]
