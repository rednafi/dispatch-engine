"""
Data will go into the body of a get request."""

from typing import List, Dict

from pydantic import BaseModel, Field


class Parcel(BaseModel):
    hub_id: int = Field(..., alias="hubId")
    parcel_id: int = Field(..., alias="parcelId")
    area_id: int = Field(..., alias="areaId")


class Agent(BaseModel):
    hub_id: int = Field(..., alias="hubId")
    agent_id: int = Field(..., alias="agentId")


class DataIn(BaseModel):
    """Defines the structure of the payload."""

    parcels: List[Parcel]
    agents: List[Agent]


class DataOut(BaseModel):
    data: Dict[str, List[Parcel]]
