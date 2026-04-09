# Etsy Listing: Custom Wedding QR Code

## Product Title
Custom Wedding QR Code - Elegant Styled Design for Wedding Invitations

## Description
Turn your wedding website link into a beautiful, print-ready QR code that matches your invitation aesthetic. Choose from 8 elegant color presets: navy, gold, rose gold, burgundy, sage, dusty blue, black, or charcoal.

**What you get:**
- High-resolution PNG (1000x1000px), ready to print
- Your choice of circle or rounded-square dot style
- Optional logo overlay in the center
- Fast turnaround (within 24 hours of order)

**How it works:**
1. At checkout, leave a note with: your URL, color preference, style (circles/rounded), and logo file (if any)
2. We generate your custom QR code and email you the PNG file
3. Test it, then drop it into your invitation design

**Pricing:** 4 EUR per QR code

## Sample Images
Include 4-6 sample QR code images in the listing photos:
- Navy circles style (no logo)
- Gold rounded style (no logo)
- Rose gold circles style (with logo placeholder)
- Dusty blue circles style
- Charcoal rounded style

Generate samples with:
```
python generate_qr.py --url "https://example.com/rsvp" --color navy --style circles
python generate_qr.py --url "https://example.com/rsvp" --color gold --style rounded
python generate_qr.py --url "https://example.com/rsvp" --color rose_gold --style circles
python generate_qr.py --url "https://example.com/rsvp" --color dusty_blue --style circles
python generate_qr.py --url "https://example.com/rsvp" --color charcoal --style rounded
```

## Fulfillment Process
1. Receive order notification from Etsy
2. Read customer note for: URL, color, style, logo (if provided)
3. Download logo from Etsy message if supplied
4. Run: `python generate_qr.py --url "<url>" --color <color> --style <style> [--logo <logo_path>]`
5. Verify QR scans correctly with phone camera
6. Email PNG to customer via Etsy messaging system
7. Mark order as complete

## Decision Gate
After 30 days on Etsy, evaluate:

| Result | Action |
|--------|--------|
| >= 1 paid order | Proceed to web MVP (M-001 onward) |
| 0 orders, high views | Adjust pricing or listing copy, extend 30 days |
| 0 orders, low views | Review SEO/tags, consider other platforms |
| 0 orders after 60 days | Pivot concept or abandon project |

**Minimum viable signal:** 1 paid order within 30 days confirms willingness-to-pay and justifies web app investment.
