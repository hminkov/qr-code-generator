"""Security-critical tests for payment webhook and order cache."""

import hashlib
import hmac
import json
import os
import sys
import time

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from api.payment import OrderCache


def test_order_cache_persists_to_file(tmp_path):
    path = str(tmp_path / "orders.json")
    cache1 = OrderCache(path)
    cache1.add("order-789")

    cache2 = OrderCache(path)
    assert cache2.is_paid("order-789")


def test_order_cache_loads_on_restart(tmp_path):
    path = str(tmp_path / "orders.json")
    data = {"order-existing": time.time()}
    (tmp_path / "orders.json").write_text(json.dumps(data))

    cache = OrderCache(path)
    assert cache.is_paid("order-existing")


def test_expired_order_not_valid(tmp_path):
    path = str(tmp_path / "orders.json")
    expired_ts = time.time() - (25 * 60 * 60)  # 25 hours ago
    data = {"order-old": expired_ts}
    (tmp_path / "orders.json").write_text(json.dumps(data))

    cache = OrderCache(path)
    assert not cache.is_paid("order-old")


def test_order_cache_empty_file(tmp_path):
    path = str(tmp_path / "orders.json")
    cache = OrderCache(path)
    assert not cache.is_paid("nonexistent")


def test_order_cache_add_and_check(tmp_path):
    path = str(tmp_path / "orders.json")
    cache = OrderCache(path)
    cache.add("order-abc")
    assert cache.is_paid("order-abc")
    assert not cache.is_paid("order-xyz")
