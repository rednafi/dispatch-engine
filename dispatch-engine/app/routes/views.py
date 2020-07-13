from typing import Dict

from app.apis.dispatch.start_tasks import start_queue
from fastapi import APIRouter, Depends
from app.core.auth import get_current_user


router = APIRouter()


@router.get("/parcel-dispatch/{num}", tags=["main"])
async def view_a(num: int, auth=Depends(get_current_user)) -> Dict[str, int]:
    return main_func_a(num)
