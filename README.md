# 🎊 Wedding QR Code Generator

Generate beautiful, customizable QR codes with rounded corners, circular dots, and logo support - perfect for wedding invitations!

![Example QR Code](output/example.png)

## ✨ Features

- **Stylish Design**: Circular dots and rounded finder patterns (like modern QR codes)
- **Logo Support**: Add your monogram, wedding logo, or any image to the center
- **Color Presets**: Beautiful wedding-appropriate colors (navy, rose gold, sage, etc.)
- **Custom Colors**: Use any hex color you want
- **High Quality**: Generates high-resolution PNG images
- **100% Free**: Uses open-source libraries only

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Your QR Code

**Basic (no logo):**

```bash
python generate_qr.py --url "https://yourwedding.com/rsvp"
```

**With logo:**

```bash
python generate_qr.py --url "https://yourwedding.com/rsvp" --logo "logos/your_logo.png"
```

**Custom color:**

```bash
python generate_qr.py --url "https://yourwedding.com/rsvp" --color rose_gold
```

## 🎨 Color Presets

| Name         | Hex     | Description        |
| ------------ | ------- | ------------------ |
| `navy`       | #445E7C | Classic navy blue  |
| `gold`       | #D4AF37 | Elegant gold       |
| `rose_gold`  | #B76E79 | Romantic rose gold |
| `burgundy`   | #800020 | Deep burgundy      |
| `sage`       | #9CAF88 | Soft sage green    |
| `dusty_blue` | #8BA9C2 | Dusty blue         |
| `black`      | #000000 | Classic black      |
| `charcoal`   | #36454F | Soft charcoal      |

You can also use any hex color: `--color "#FF5733"`

## 📖 All Options

```
python generate_qr.py --help

Options:
  --url, -u         URL or text to encode (required)
  --output, -o      Output file path (default: output/wedding_qr.png)
  --logo, -l        Path to logo image
  --color, -c       Color preset or hex code (default: navy)
  --background, -bg Background color hex (default: #FFFFFF)
  --size, -s        Output size in pixels (default: 1000)
  --logo-size, -ls  Logo size ratio 0.2-0.3 (default: 0.25)
  --style           circles or rounded (default: circles)
  --error-correction L/M/Q/H (default: H)
```

## 🔧 Python API Usage

```python
from src.qr_generator import WeddingQRGenerator

generator = WeddingQRGenerator()

# Basic QR code
generator.generate(
    data="https://yourwedding.com/rsvp",
    output_path="output/my_qr.png",
    color="navy",
    style="circles"
)

# With logo
generator.generate(
    data="https://yourwedding.com/rsvp",
    output_path="output/my_qr_logo.png",
    logo_path="logos/monogram.png",
    color="rose_gold",
    logo_size_ratio=0.25
)
```

## 💡 Tips for Best Results

1. **Error Correction**: Use `H` (default) when adding a logo - this allows up to 30% of the QR code to be covered
2. **Logo Size**: Keep between 20-25% of QR size for reliable scanning
3. **Contrast**: Ensure good contrast between QR code color and background
4. **Test First**: Always test with your phone camera before printing!
5. **Resolution**: Use at least 1000px for print quality

## 📂 Folder Structure

```
QR Code generator/
├── generate_qr.py      # Main entry point (CLI)
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── src/
│   ├── __init__.py
│   └── qr_generator.py # Core QR generation logic
├── logos/             # Place your logo images here
└── output/            # Generated QR codes saved here
```

## 🔬 How QR Codes Work

QR (Quick Response) codes store data in a 2D matrix of dark and light modules:

1. **Finder Patterns**: The three large squares in corners help scanners locate and orient the code
2. **Data Encoding**: Your URL/text is converted to binary and encoded in the pattern
3. **Error Correction**: Redundant data allows reading even if partially damaged/obscured
   - Level L: ~7% recovery
   - Level M: ~15% recovery
   - Level Q: ~25% recovery
   - Level H: ~30% recovery (best for logos!)

The error correction is what allows us to place a logo in the center - the scanner can reconstruct the hidden data from the redundant information!

## 📝 License

MIT License - Free to use for your wedding! 💒
