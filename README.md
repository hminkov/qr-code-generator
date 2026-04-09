# QR Code Designer

Design print-ready QR codes with custom dot styles, colors, and logo overlay. Built for wedding invitations, event stationery, and business cards.

## Features

- **4 dot styles**: Circles, rounded squares, diamonds, and clean squares
- **8 color presets**: Navy, Gold, Rose Gold, Burgundy, Sage, Dusty Blue, Black, Charcoal
- **Custom colors**: Any hex color via CLI or web UI
- **Logo overlay**: Upload a monogram or crest — dots clear automatically around it
- **Print quality**: Up to 2000px with 4x antialiased rendering (300 DPI at ~7 inches)
- **No watermarks**: Free tier produces clean 500px PNG, no branding
- **Live preview**: Web UI renders server-side preview on every parameter change
- **Concurrent-safe**: Each generate() call is stateless — safe for web server use

## Quick Start

### CLI

```bash
pip install -r requirements.txt

# Basic
python generate_qr.py --url "https://yourwedding.com/rsvp"

# With options
python generate_qr.py \
  --url "https://yourwedding.com/rsvp" \
  --color rose_gold \
  --style circles \
  --logo logos/monogram.png \
  --size 1000
```

### Web App (local)

```bash
# Terminal 1 — API
pip install -r requirements-api.txt
uvicorn api.main:app --reload

# Terminal 2 — Frontend
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

### Python API

```python
import sys; sys.path.insert(0, "src")
from qr_generator import WeddingQRGenerator
from models import QRRequest

generator = WeddingQRGenerator()

result = generator.generate(QRRequest(
    data="https://yourwedding.com/rsvp",
    color="navy",
    style="circles",
    size=1000,
))

with open("qr.png", "wb") as f:
    f.write(result.image_bytes)
```

## Color Presets

| Name         | Hex     |
| ------------ | ------- |
| `navy`       | #445E7C |
| `gold`       | #D4AF37 |
| `rose_gold`  | #B76E79 |
| `burgundy`   | #800020 |
| `sage`       | #9CAF88 |
| `dusty_blue` | #8BA9C2 |
| `black`      | #000000 |
| `charcoal`   | #36454F |

## Dot Styles

| Style     | Description                        |
| --------- | ---------------------------------- |
| `circles` | Smooth antialiased circles         |
| `rounded` | Rounded squares (30% corner radius)|
| `diamond` | 45-degree rotated squares          |
| `square`  | Clean sharp-edged squares          |

## CLI Options

```
python generate_qr.py --help

Options:
  --url, -u              URL or text to encode (required)
  --output, -o           Output file path (default: auto-numbered)
  --logo, -l             Path to logo image
  --color, -c            Color preset or hex code (default: navy)
  --background, -bg      Background color hex (default: #FFFFFF)
  --size, -s             Output size in pixels (default: 1000)
  --logo-size, -ls       Logo size ratio (default: 0.25)
  --logo-padding, -lp    Padding around logo (default: 0.03)
  --style                circles, rounded, diamond, square (default: circles)
  --error-correction, -ec  L/M/Q/H (default: H)
  --dot-size, -ds        Dot size ratio 0.5-1.2 (default: 0.9)
  --version, -v          QR version 1-40 (default: auto)
```

## API Endpoints

| Method | Path                     | Description              |
| ------ | ------------------------ | ------------------------ |
| POST   | `/api/generate`          | Generate QR (multipart form, supports logo file upload) |
| GET    | `/api/generate/preview`  | 500px preview via query params |
| GET    | `/api/presets`           | Color preset map         |
| GET    | `/api/health`            | Health check             |
| POST   | `/api/webhook/lemon-squeezy` | Payment webhook     |
| GET    | `/api/verify/{order_id}` | Payment verification     |

## Project Structure

```
QR Code generator/
├── generate_qr.py          # CLI entry point
├── config.json              # Default CLI settings
├── requirements.txt         # Core dependencies (qrcode, Pillow)
├── requirements-api.txt     # API dependencies (FastAPI, uvicorn, httpx)
├── .env.example             # Environment variable template
├── src/
│   ├── qr_generator.py      # Core QR engine (drawers, generator)
│   └── models.py            # QRRequest / QRResult dataclasses
├── api/
│   ├── main.py              # FastAPI app, CORS, router wiring
│   ├── routes.py            # QR generation endpoints
│   ├── dependencies.py      # Generator singleton, rate limiter
│   ├── payment.py           # Lemon Squeezy integration, OrderCache
│   ├── webhook.py           # HMAC-verified webhook handler
│   └── verify.py            # Payment verification polling endpoint
├── frontend/
│   ├── src/app/             # Next.js pages (home, examples, pricing)
│   ├── src/components/      # React components (configurator, preview, etc.)
│   └── src/lib/             # API client, payment client
├── deploy/
│   ├── Dockerfile.api       # Python API container
│   ├── Dockerfile.frontend  # Next.js build → nginx
│   ├── docker-compose.yml   # Two-service stack
│   └── nginx.conf           # Reverse proxy config
├── tests/
│   ├── test_qr_generator.py # Core engine + concurrency tests
│   ├── test_api.py          # API endpoint tests
│   └── test_payment.py      # Payment/cache tests
├── docs/
│   └── etsy-listing.md      # Demand validation artifact
├── logos/                    # Logo assets
└── output/                   # Generated QR codes
```

## Tests

```bash
python -m pytest tests/ -v    # All tests (33 passing)
python -m pytest tests/test_qr_generator.py  # Core engine
python -m pytest tests/test_api.py           # API endpoints
python -m pytest tests/test_payment.py       # Payment/cache
```

## Deployment

```bash
cp .env.example .env   # Fill in Lemon Squeezy keys
cd deploy
docker-compose up --build
```

Serves frontend on port 80/443 via nginx, API on port 8000 via uvicorn.

## Tips

- Use error correction **H** (default) when adding a logo — allows up to 30% obstruction
- Keep logo size ratio between 0.20–0.25 for reliable scanning
- Test with your phone camera before printing
- 500px is sufficient for screens; use 1000px+ for print

## License

MIT
