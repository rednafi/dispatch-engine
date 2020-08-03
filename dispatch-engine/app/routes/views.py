from typing import Dict

from app.apis.dispatch.data_model import ParcelsAgents
from app.apis.dispatch.engine import dispatch_hook, Algo
from app.core.auth import get_current_user
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/dispatch-engine/pd/", tags=["main"])
async def view_dispatch(
    parcels_agents: ParcelsAgents, auth=Depends(get_current_user)
) -> Dict[str, int]:
    parcels_agents = parcels_agents.dict()
    agents_parcels = dispatch_hook(
        Algo, parcels_agents.get("parcels"), parcels_agents.get("agents")
    )
    return {"data": agents_parcels}
