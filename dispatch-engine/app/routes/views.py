from typing import Dict

from app.apis.dispatch.data_model import DataIn, DataOut
from app.apis.dispatch.engine import dispatch_hook, Algo
from app.core.auth import get_current_user
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/dispatch-engine/pd/", tags=["main"])
async def view_dispatch(
    parcels_agents: DataIn,
    auth=Depends(get_current_user),

):
    parcels_agents = parcels_agents.dict()
    agents_parcels = dispatch_hook(
        Algo, parcels_agents.get("parcels"), parcels_agents.get("agents")
    )
    return agents_parcels
