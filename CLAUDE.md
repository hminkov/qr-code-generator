# QR Code Generator

QR code generator with stylized dots, rounded finder patterns, and logo support.
Structured as a Python CLI (existing) + FastAPI API + Next.js frontend.

## Files

| File               | What                                        | When to read                                          |
| ------------------ | ------------------------------------------- | ----------------------------------------------------- |
| `generate_qr.py`   | CLI entry point, config loading, arg parsing | Adding CLI options, changing defaults, debugging args |
| `config.json`      | Default generation settings (URL, colors)   | Changing default QR parameters, understanding options |
| `requirements.txt` | Python dependencies (qrcode, Pillow)        | Adding dependencies, debugging import errors          |
| `requirements-api.txt` | Additional API deps (FastAPI, uvicorn, httpx) | Adding API dependencies                        |
| `.env.example`     | Required environment variables with descriptions | First-time setup, deployment                    |
| `README.md`        | User-facing docs, usage examples, color presets | Updating user instructions, adding features docs   |

## Subdirectories

| Directory | What                              | When to read                                         |
| --------- | --------------------------------- | ---------------------------------------------------- |
| `src/`    | Core QR generation logic          | Modifying QR rendering, adding styles, fixing output |
| `api/`    | FastAPI application (routes, deps, payment, webhook) | Modifying API behavior, payment flow     |
| `frontend/` | Next.js static export frontend  | Modifying UI, preview behavior, payment gate         |
| `deploy/` | Docker, nginx, docker-compose configs | Deployment, infrastructure changes               |
| `docs/`   | Etsy listing and demand validation artifacts | Demand validation phase                    |
| `tests/`  | Pytest suites for core engine, API, payment | Running tests, adding test coverage            |
| `logos/`  | Logo assets for QR center overlay | Adding logos for QR code generation                  |
| `output/` | Generated QR code PNGs            | Never edit directly                                  |

## Architecture Invariants

- `src/qr_generator.py` has no shared mutable state between generate() calls.
  CustomCircleDrawer and CustomRoundedDrawer receive exclusion_zone as a
  constructor argument, not a class attribute. Violating this causes concurrent
  request corruption.

- generate() returns QRResult(image_bytes, ...) not a file path. The CLI writes
  bytes to disk; the API streams them. Do not add output_path back.

- Free tier: 500px. Paid tier: 2000px. No watermarks (breaks scanning).

- Payment processor is Lemon Squeezy (merchant of record for EU VAT compliance).

- Frontend is Next.js static export (`output: "export"`). No Node.js server in
  production. nginx serves frontend/out/ directly.

## Build

```bash
pip install -r requirements.txt
# For API:
pip install -r requirements-api.txt
# For frontend:
cd frontend && npm ci
```

## Test

```bash
# Core engine + CLI
python generate_qr.py --url "https://example.com"
pytest tests/test_qr_generator.py
# API
pytest tests/test_api.py
# Payment
pytest tests/test_payment.py
```

## Run API locally

```bash
uvicorn api.main:app --reload
```
