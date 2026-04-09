"""Integration tests for the FastAPI QR code API."""

import sys
import os

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from api.main import app
from api.dependencies import _generate_limiter


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_health_returns_200(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_presets_returns_all_colors(client):
    resp = client.get("/api/presets")
    assert resp.status_code == 200
    data = resp.json()
    expected = {"navy", "gold", "rose_gold", "burgundy", "sage", "dusty_blue", "black", "charcoal"}
    assert expected.issubset(set(data.keys()))


def test_generate_valid_returns_png(client):
    resp = client.post(
        "/api/generate",
        data={"data": "https://example.com", "size": "200"},
    )
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/png"
    assert resp.content[:8] == b"\x89PNG\r\n\x1a\n"


def test_generate_missing_data_returns_422(client):
    resp = client.post("/api/generate", data={})
    assert resp.status_code == 422


def test_generate_with_logo(client, tmp_path):
    from PIL import Image
    logo = Image.new("RGBA", (50, 50), (255, 0, 0, 255))
    logo_path = tmp_path / "logo.png"
    logo.save(str(logo_path))

    with open(logo_path, "rb") as f:
        resp = client.post(
            "/api/generate",
            data={"data": "https://example.com", "size": "200"},
            files={"logo": ("logo.png", f, "image/png")},
        )
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/png"


def test_preview_returns_png(client):
    resp = client.get("/api/generate/preview", params={"data": "https://example.com"})
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/png"


def test_rate_limiter_returns_429():
    """Rate limiter triggers 429 after exceeding 10 requests/min."""
    with TestClient(app) as c:
        # Clear any existing tokens for our test IP
        with _generate_limiter._lock:
            _generate_limiter._tokens.pop("1.2.3.4", None)

        for _ in range(10):
            r = c.post(
                "/api/generate",
                data={"data": "https://example.com", "size": "200"},
                headers={"X-Forwarded-For": "1.2.3.4"},
            )
            assert r.status_code == 200

        resp = c.post(
            "/api/generate",
            data={"data": "https://example.com", "size": "200"},
            headers={"X-Forwarded-For": "1.2.3.4"},
        )
        assert resp.status_code == 429
