from typing import Dict

from app.apis.dispatch.data_model import ParcelsAgents
from app.apis.dispatch.engine import dispatch_hook
from app.core.auth import get_current_user
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/dispatch-engine/pd/", tags=["main"])
async def view_a(
    parcels_agents: ParcelsAgents, auth=Depends(get_current_user)
) -> Dict[str, int]:

    agents_parcels = dispatch_hook(parcels_agents.parcels, parcels_agents.agents)
    return {"data": agents_parcels}
