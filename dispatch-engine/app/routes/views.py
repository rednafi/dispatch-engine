from typing import Dict


from fastapi import APIRouter, Depends
from app.core.auth import get_current_user
from app.apis.dispatch.data_model import Parcels, Agents
from app.apis.dispatch.engine import dispatch_hook

router = APIRouter()


@router.post("/dispatch-engine/pd/", tags=["main"])
async def view_a(
    parcels: Parcels, agents: Agents, auth=Depends(get_current_user)
) -> Dict[str, int]:
    agents_parcels = dispatch_hook(parcels, agents)
    return agents_parcels
