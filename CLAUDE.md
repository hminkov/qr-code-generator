# QR Code Generator

Wedding QR code generator with stylized dots, rounded finder patterns, and logo support.

## Files

| File               | What                                        | When to read                                          |
| ------------------ | ------------------------------------------- | ----------------------------------------------------- |
| `generate_qr.py`   | CLI entry point, config loading, arg parsing | Adding CLI options, changing defaults, debugging args |
| `config.json`      | Default generation settings (URL, colors)   | Changing default QR parameters, understanding options |
| `requirements.txt` | Python dependencies (qrcode, Pillow)        | Adding dependencies, debugging import errors          |
| `README.md`        | User-facing docs, usage examples, color presets | Updating user instructions, adding features docs   |

## Subdirectories

| Directory | What                              | When to read                                         |
| --------- | --------------------------------- | ---------------------------------------------------- |
| `src/`    | Core QR generation logic          | Modifying QR rendering, adding styles, fixing output |
| `logos/`  | Logo assets for QR center overlay | Adding logos for QR code generation                  |
| `output/` | Generated QR code PNGs            | Never edit directly                                  |

## Build

```bash
pip install -r requirements.txt
```

## Test

```bash
python generate_qr.py --url "https://example.com"
```
