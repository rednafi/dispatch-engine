"""
Data will go into the body of a get request."""

from pydantic import BaseModel
from typing import List


class Parcel(BaseModel):
    hub_id: int
    parcel_id: int
    area_id: int


class Agent(BaseModel):
    hub_id: int
    agent_id: int


class Parcels(BaseModel):
    parcels: List[Parcel]


class Agents(BaseModel):
    agents: List[Agent]
