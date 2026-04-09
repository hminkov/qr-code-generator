"""Lemon Squeezy payment integration and file-backed order cache."""

import json
import os
import tempfile
import time
import threading
from pathlib import Path
from typing import Optional

import httpx


LEMON_SQUEEZY_API_KEY = os.environ.get("LEMON_SQUEEZY_API_KEY", "")
LEMON_SQUEEZY_STORE_ID = os.environ.get("LEMON_SQUEEZY_STORE_ID", "")
ORDER_CACHE_PATH = os.environ.get("ORDER_CACHE_PATH", "./data/orders.json")
ORDER_TTL_SECONDS = 24 * 3600


class OrderCache:
    """File-backed TTL cache of paid order IDs.

    Persists to JSON using atomic rename. Entries expire after ORDER_TTL_SECONDS.
    Thread-safe via Lock.
    """

    def __init__(self, path: str = ORDER_CACHE_PATH):
        self._path = Path(path)
        self._lock = threading.Lock()
        self._cache: dict[str, float] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            return
        try:
            with open(self._path) as f:
                raw: dict[str, float] = json.load(f)
            now = time.time()
            self._cache = {
                order_id: ts
                for order_id, ts in raw.items()
                if now - ts < ORDER_TTL_SECONDS
            }
        except (json.JSONDecodeError, OSError):
            self._cache = {}

    def _persist(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp_fd, tmp_path = tempfile.mkstemp(
            dir=self._path.parent, prefix=".orders_tmp_"
        )
        try:
            with os.fdopen(tmp_fd, "w") as f:
                json.dump(self._cache, f)
            os.replace(tmp_path, self._path)
        except OSError:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    def add(self, order_id: str) -> None:
        with self._lock:
            self._cache[order_id] = time.time()
            self._persist()

    def is_paid(self, order_id: str) -> bool:
        with self._lock:
            ts = self._cache.get(order_id)
            if ts is None:
                return False
            if time.time() - ts >= ORDER_TTL_SECONDS:
                del self._cache[order_id]
                self._persist()
                return False
            return True


async def create_checkout(product_id: str, order_metadata: dict) -> str:
    """Create a Lemon Squeezy checkout session and return the checkout URL."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.lemonsqueezy.com/v1/checkouts",
            headers={
                "Authorization": f"Bearer {LEMON_SQUEEZY_API_KEY}",
                "Accept": "application/vnd.api+json",
                "Content-Type": "application/vnd.api+json",
            },
            json={
                "data": {
                    "type": "checkouts",
                    "attributes": {"checkout_data": {"custom": order_metadata}},
                    "relationships": {
                        "store": {"data": {"type": "stores", "id": LEMON_SQUEEZY_STORE_ID}},
                        "variant": {"data": {"type": "variants", "id": product_id}},
                    },
                }
            },
        )
        resp.raise_for_status()
        return resp.json()["data"]["attributes"]["url"]


async def verify_order(order_id: str) -> bool:
    """Check order status via Lemon Squeezy API."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://api.lemonsqueezy.com/v1/orders/{order_id}",
            headers={"Authorization": f"Bearer {LEMON_SQUEEZY_API_KEY}"},
        )
        if resp.status_code != 200:
            return False
        return resp.json()["data"]["attributes"]["status"] == "paid"
