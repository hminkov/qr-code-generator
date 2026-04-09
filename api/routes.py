"""QR generation API routes."""

import os
import sys
import tempfile
import uuid
from io import BytesIO
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from models import QRRequest
from qr_generator import WeddingQRGenerator
from api.dependencies import get_generator, rate_limiter


router = APIRouter()


def _png_response(image_bytes: bytes, disposition: str = "attachment") -> StreamingResponse:
    filename = f"qr-{uuid.uuid4()}.png"
    return StreamingResponse(
        BytesIO(image_bytes),
        media_type="image/png",
        headers={"Content-Disposition": f'{disposition}; filename="{filename}"'},
    )


@router.post("/api/generate")
async def generate(
    generator: WeddingQRGenerator = Depends(get_generator),
    _: None = Depends(rate_limiter),
    data: str = Form(...),
    color: str = Form("navy"),
    background_color: str = Form("#FFFFFF"),
    size: int = Form(1000),
    style: str = Form("circles"),
    error_correction: str = Form("H"),
    dot_size: float = Form(0.9),
    logo_size_ratio: float = Form(0.25),
    logo_padding: float = Form(0.03),
    version: Optional[int] = Form(None),
    logo: Optional[UploadFile] = File(None),
):
    logo_path = None
    try:
        if logo and logo.filename:
            suffix = os.path.splitext(logo.filename)[1] or ".png"
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp.write(await logo.read())
            tmp.close()
            logo_path = tmp.name

        request = QRRequest(
            data=data,
            color=color,
            background_color=background_color,
            size=size,
            style=style,
            error_correction=error_correction,
            dot_size=dot_size,
            logo_path=logo_path,
            logo_size_ratio=logo_size_ratio,
            logo_padding=logo_padding,
            version=version,
        )
        result = generator.generate(request)
        return _png_response(result.image_bytes)
    finally:
        if logo_path and os.path.exists(logo_path):
            os.unlink(logo_path)


@router.get("/api/generate/preview")
def preview(
    generator: WeddingQRGenerator = Depends(get_generator),
    _: None = Depends(rate_limiter),
    data: str = Query(...),
    color: str = Query("navy"),
    background_color: str = Query("#FFFFFF"),
    logo_size_ratio: float = Query(0.25),
    logo_padding: float = Query(0.03),
    style: str = Query("circles"),
    error_correction: str = Query("H"),
    dot_size: float = Query(0.9),
    version: Optional[int] = Query(None),
):
    req = QRRequest(
        data=data,
        color=color,
        background_color=background_color,
        size=500,
        logo_size_ratio=logo_size_ratio,
        logo_padding=logo_padding,
        style=style,
        error_correction=error_correction,
        dot_size=dot_size,
        version=version,
    )
    result = generator.generate(req)
    return _png_response(result.image_bytes, disposition="inline")


@router.get("/api/presets")
def presets():
    return JSONResponse(WeddingQRGenerator.COLOR_PRESETS)


@router.get("/api/health")
def health():
    return {"status": "ok"}
