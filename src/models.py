"""Data models for QR code generation requests and results."""

from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class QRRequest:
    data: str
    color: str = "navy"
    background_color: str = "#FFFFFF"
    size: int = 1000
    logo_path: Optional[str] = None
    logo_size_ratio: float = 0.25
    logo_padding: float = 0.03
    style: Literal["circles", "rounded", "diamond", "square"] = "circles"
    error_correction: Literal["L", "M", "Q", "H"] = "H"
    dot_size: float = 0.9
    version: Optional[int] = None

    def __post_init__(self):
        if self.version is not None:
            self.version = max(1, min(40, int(self.version)))
        self.dot_size = max(0.1, min(1.5, float(self.dot_size)))
        self.logo_size_ratio = max(0.05, min(0.5, float(self.logo_size_ratio)))
        self.logo_padding = max(0.0, min(0.2, float(self.logo_padding)))
        self.size = max(100, min(4000, int(self.size)))


@dataclass
class QRResult:
    image_bytes: bytes
    content_type: str = "image/png"
    width: int = 0
    height: int = 0
