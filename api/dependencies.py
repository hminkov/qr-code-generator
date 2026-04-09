"""Shared FastAPI dependencies: WeddingQRGenerator singleton, rate limiter."""

import time
import threading
from collections import defaultdict

from fastapi import Request, HTTPException

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from qr_generator import WeddingQRGenerator


_generator_instance = WeddingQRGenerator()


def get_generator() -> WeddingQRGenerator:
    return _generator_instance


class _TokenBucket:
    """Sliding-window token bucket for per-IP rate limiting."""

    def __init__(self, rate: int, period: float = 60.0):
        self._rate = rate
        self._period = period
        self._tokens: dict[str, list[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def is_allowed(self, key: str) -> bool:
        now = time.monotonic()
        window_start = now - self._period
        with self._lock:
            timestamps = self._tokens[key]
            self._tokens[key] = [t for t in timestamps if t > window_start]
            if len(self._tokens[key]) >= self._rate:
                return False
            self._tokens[key].append(now)
            return True


_generate_limiter = _TokenBucket(rate=10)
_preview_limiter = _TokenBucket(rate=60)


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def rate_limiter(request: Request) -> None:
    ip = _client_ip(request)
    path = request.url.path
    bucket = _preview_limiter if "preview" in path else _generate_limiter
    if not bucket.is_allowed(ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
