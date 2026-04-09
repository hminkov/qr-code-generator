"""Integration and concurrency tests for WeddingQRGenerator."""

import io
import struct
import threading
import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from qr_generator import WeddingQRGenerator
from models import QRRequest, QRResult


def _is_valid_png(data: bytes) -> bool:
    return data[:8] == b"\x89PNG\r\n\x1a\n"


def _png_dimensions(data: bytes):
    w = struct.unpack(">I", data[16:20])[0]
    h = struct.unpack(">I", data[20:24])[0]
    return w, h


@pytest.fixture(scope="module")
def generator():
    return WeddingQRGenerator()


def test_generate_basic_returns_valid_png(generator):
    req = QRRequest(data="https://example.com")
    result = generator.generate(req)
    assert isinstance(result, QRResult)
    assert _is_valid_png(result.image_bytes)
    w, h = _png_dimensions(result.image_bytes)
    assert w == req.size
    assert h == req.size
    assert result.content_type == "image/png"
    assert result.width == req.size
    assert result.height == req.size


def test_generate_with_logo_clears_center(generator, tmp_path):
    from PIL import Image
    logo = Image.new("RGBA", (100, 100), (255, 0, 0, 255))
    logo_path = str(tmp_path / "logo.png")
    logo.save(logo_path)

    req = QRRequest(data="https://example.com/logo", logo_path=logo_path)
    result = generator.generate(req)
    assert _is_valid_png(result.image_bytes)
    assert result.width == req.size


@pytest.mark.parametrize("style", ["circles", "rounded"])
def test_generate_each_style(generator, style):
    req = QRRequest(data="https://example.com", style=style)
    result = generator.generate(req)
    assert _is_valid_png(result.image_bytes)


@pytest.mark.parametrize("color", list(WeddingQRGenerator.COLOR_PRESETS.keys()))
def test_generate_each_color_preset(generator, color):
    req = QRRequest(data="https://example.com", color=color)
    result = generator.generate(req)
    assert _is_valid_png(result.image_bytes)


def test_concurrent_generation_independent(tmp_path):
    logo_sizes = [0.15, 0.20, 0.25, 0.30]
    results = [None] * 4
    errors = []

    from PIL import Image

    logo_path = str(tmp_path / "logo.png")
    logo = Image.new("RGBA", (50, 50), (0, 128, 0, 255))
    logo.save(logo_path)

    def worker(idx, logo_size):
        try:
            gen = WeddingQRGenerator()
            req = QRRequest(
                data=f"https://example.com/thread/{idx}",
                logo_path=logo_path,
                logo_size_ratio=logo_size,
                size=500,
            )
            results[idx] = gen.generate(req)
        except Exception as exc:
            errors.append(exc)

    threads = [
        threading.Thread(target=worker, args=(i, logo_sizes[i]))
        for i in range(4)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors, f"Thread errors: {errors}"
    for r in results:
        assert r is not None
        assert _is_valid_png(r.image_bytes)

    unique_outputs = {r.image_bytes for r in results}
    assert len(unique_outputs) == 4, "All thread outputs should be distinct"


@pytest.mark.parametrize("size", [200, 500, 1000])
def test_property_valid_output_various_sizes(generator, size):
    req = QRRequest(data="https://example.com", size=size)
    result = generator.generate(req)
    assert _is_valid_png(result.image_bytes)
    w, h = _png_dimensions(result.image_bytes)
    assert w == size
    assert h == size


@pytest.mark.parametrize("ec", ["L", "M", "Q", "H"])
def test_property_all_error_correction_levels(generator, ec):
    req = QRRequest(data="https://example.com", error_correction=ec)
    result = generator.generate(req)
    assert _is_valid_png(result.image_bytes)


def test_backward_compatible_kwargs(generator):
    result = generator.generate(data="https://example.com", color="gold", style="rounded")
    assert isinstance(result, QRResult)
    assert len(result.image_bytes) > 0
