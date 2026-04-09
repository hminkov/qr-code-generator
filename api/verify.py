"""Payment verification endpoint polled by the frontend after checkout."""

from fastapi import APIRouter
from .payment import verify_order
from .webhook import _order_cache

router = APIRouter()


@router.get("/api/verify/{order_id}")
async def verify(order_id: str):
    if _order_cache.is_paid(order_id):
        return {"paid": True}
    paid = await verify_order(order_id)
    return {"paid": paid}
