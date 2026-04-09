"""FastAPI application entry point."""

import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router as qr_router
from api.webhook import router as webhook_router
from api.verify import router as verify_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("API starting up")
    yield
    logger.info("API shutting down")


def _parse_origins(raw: str) -> list[str]:
    return [o.strip() for o in raw.split(",") if o.strip()]


cors_origins = _parse_origins(os.environ.get("CORS_ORIGINS", "http://localhost:3000"))

app = FastAPI(title="QR Code Designer API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(qr_router)
app.include_router(webhook_router)
app.include_router(verify_router)
