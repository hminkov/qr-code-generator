#!/usr/bin/env python3
"""
Wedding QR Code Generator - Main Entry Point

Quick start (using config file):
    python generate_qr.py
    
Or with command line args:
    python generate_qr.py --url "https://yourwedding.com/rsvp"
"""

import argparse
import json
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from qr_generator import WeddingQRGenerator
from models import QRRequest

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')


def load_config():
    """Load configuration from config.json"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}


def get_next_filename():
    """Get the next available numbered filename (1.png, 2.png, etc.)"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        return os.path.join(OUTPUT_DIR, "1.png")
    
    # Find existing numbered files
    existing_numbers = []
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith('.png'):
            name = filename[:-4]  # Remove .png
            if name.isdigit():
                existing_numbers.append(int(name))
    
    # Get next number
    next_num = max(existing_numbers, default=0) + 1
    return os.path.join(OUTPUT_DIR, f"{next_num}.png")


def main():
    config = load_config()
    
    parser = argparse.ArgumentParser(
        description='🎊 Generate beautiful QR codes for your wedding invitation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                              # Uses config.json
  %(prog)s --url "https://yourwedding.com/rsvp"         # Override URL
  %(prog)s --url "https://yourwedding.com" --logo "logos/heart.png" --color rose_gold

Color Presets: navy, gold, rose_gold, burgundy, sage, dusty_blue, black, charcoal

Edit config.json to set your defaults!
        """
    )
    
    parser.add_argument(
        '--url', '-u',
        default=config.get('url'),
        help='URL or text to encode (default: from config.json)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default=None,  # Will auto-generate numbered filename
        help='Output file path (default: auto-numbered 1.png, 2.png, etc.)'
    )
    
    parser.add_argument(
        '--logo', '-l',
        default=config.get('logo'),
        help='Path to logo image to place in center'
    )
    
    parser.add_argument(
        '--color', '-c',
        default=config.get('color', 'navy'),
        help='QR code color - preset name or hex (default: from config.json)'
    )
    
    parser.add_argument(
        '--background', '-bg',
        default=config.get('background', '#FFFFFF'),
        help='Background color in hex (default: from config.json)'
    )
    
    parser.add_argument(
        '--size', '-s',
        type=int,
        default=config.get('size', 1000),
        help='Output size in pixels (default: from config.json)'
    )
    
    parser.add_argument(
        '--logo-size', '-ls',
        type=float,
        default=config.get('logo_size_ratio', 0.25),
        help='Logo size as ratio of QR code, 0.2-0.3 recommended (default: from config.json)'
    )
    
    parser.add_argument(
        '--logo-padding', '-lp',
        type=float,
        default=config.get('logo_padding', 0.03),
        help='Padding around logo as ratio of QR size (default: 0.03, try 0.05 for more space)'
    )
    
    parser.add_argument(
        '--style',
        choices=['circles', 'rounded'],
        default=config.get('style', 'circles'),
        help='Module style: circles or rounded (default: from config.json)'
    )
    
    parser.add_argument(
        '--error-correction', '-ec',
        choices=['L', 'M', 'Q', 'H'],
        default=config.get('error_correction', 'H'),
        help='Error correction level L/M/Q/H (default: from config.json)'
    )
    
    parser.add_argument(
        '--dot-size', '-ds',
        type=float,
        default=config.get('dot_size', 0.9),
        help='Dot size ratio 0.1-1.0 (1.0=dots touch, 0.5=half size with gaps, default: 0.9)'
    )
    
    parser.add_argument(
        '--version', '-v',
        type=int,
        default=config.get('version'),
        help='QR version 1-40 controls density (1=sparse 21x21, 10=medium 57x57, 40=dense 177x177). Default: auto'
    )
    
    args = parser.parse_args()
    
    # Check if URL is provided
    if not args.url:
        print("❌ Error: No URL provided!")
        print("   Either set 'url' in config.json or use --url argument")
        print(f"\n   Config file location: {CONFIG_FILE}")
        sys.exit(1)
    
    # Auto-generate numbered filename if not specified
    if args.output is None:
        args.output = get_next_filename()
    else:
        # Ensure output directory exists for custom path
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    # Generate QR code
    generator = WeddingQRGenerator()
    
    print("\n" + "=" * 50)
    print("🎊 Wedding QR Code Generator")
    print("=" * 50)
    print(f"\n📝 Encoding: {args.url}")
    print(f"🎨 Color: {args.color}")
    print(f"⭕ Style: {args.style}")
    print(f"🔘 Dot size: {args.dot_size}")
    print(f"📁 Output: {args.output}")
    if args.logo:
        print(f"🖼️  Logo: {args.logo}")
    print()
    
    try:
        request = QRRequest(
            data=args.url,
            logo_path=args.logo,
            color=args.color,
            background_color=args.background,
            size=args.size,
            logo_size_ratio=args.logo_size,
            logo_padding=args.logo_padding,
            style=args.style,
            error_correction=args.error_correction,
            dot_size=args.dot_size,
            version=args.version,
        )
        result = generator.generate(request)
        with open(args.output, 'wb') as f:
            f.write(result.image_bytes)
        print(f"✨ QR code saved to: {args.output}")

        print("\n✅ Success! Your QR code is ready.")
        print("📱 Test it with your phone camera before printing!\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
