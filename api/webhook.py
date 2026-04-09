"""Lemon Squeezy webhook handler with HMAC-SHA256 signature validation."""

import hashlib
import hmac
import json
import os

from fastapi import APIRouter, HTTPException, Request

from api.payment import OrderCache


router = APIRouter()
_order_cache = OrderCache()
SIGNING_SECRET = os.environ.get("LEMON_SQUEEZY_SIGNING_SECRET", "")


def _verify_signature(body: bytes, signature: str) -> bool:
    if not SIGNING_SECRET:
        return False
    expected = hmac.new(
        SIGNING_SECRET.encode(),
        body,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


@router.post("/api/webhook/lemon-squeezy")
async def lemon_squeezy_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Signature", "")

    if not _verify_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    event_name = payload.get("meta", {}).get("event_name", "")
    if event_name == "order_created":
        order_id = str(payload.get("data", {}).get("id", ""))
        if order_id:
            _order_cache.add(order_id)

    return {"received": True}
