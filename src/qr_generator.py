"""
QR Code Generator
Generates styled QR codes with rounded corners, circular dots, and logo support.
Each generate() call is stateless; exclusion_zone is per-instance.
"""

import io
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer, RoundedModuleDrawer
from qrcode.image.styles.moduledrawers.pil import StyledPilQRModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.compat.pil import Image as QRImage, ImageDraw as QRImageDraw
from PIL import Image, ImageDraw, ImageFilter
import os
from typing import Optional, Tuple

# Antialiasing factor for smoother circles
ANTIALIASING_FACTOR = 4


class CustomCircleDrawer(StyledPilQRModuleDrawer):
    """Circle drawer with configurable dot size and logo exclusion zone."""

    def __init__(self, size_ratio: float = 0.9, exclusion_zone: Optional[Tuple[float, float, float]] = None):
        """
        Args:
            size_ratio: Size of dots relative to module (0.1-1.5)
            exclusion_zone: Optional (center_x, center_y, radius) to skip dots inside logo area
        """
        super().__init__()
        self.size_ratio = max(0.1, min(1.5, size_ratio))
        self.circle = None
        self.exclusion_zone = exclusion_zone
    
    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        box_size = self.img.box_size
        
        # Calculate actual circle size based on ratio
        circle_diameter = int(box_size * self.size_ratio)
        if circle_diameter < 1:
            circle_diameter = 1
            
        # Create antialiased circle
        fake_size = circle_diameter * ANTIALIASING_FACTOR
        self.circle = QRImage.new(
            self.img.mode,
            (fake_size, fake_size),
            self.img.color_mask.back_color,
        )
        QRImageDraw.Draw(self.circle).ellipse(
            (0, 0, fake_size - 1, fake_size - 1), fill=self.img.paint_color
        )
        self.circle = self.circle.resize((circle_diameter, circle_diameter), Image.Resampling.LANCZOS)
        
        # Calculate offset to center the circle in the box
        self.offset = (box_size - circle_diameter) // 2
    
    def _is_in_exclusion_zone(self, box):
        """Check if dot center is within the exclusion zone."""
        if self.exclusion_zone is None:
            return False

        center_x, center_y, radius = self.exclusion_zone
        dot_center_x = (box[0][0] + box[1][0]) / 2
        dot_center_y = (box[0][1] + box[1][1]) / 2
        distance = ((dot_center_x - center_x) ** 2 + (dot_center_y - center_y) ** 2) ** 0.5
        return distance < radius
    
    def drawrect(self, box, is_active: bool):
        if is_active and not self._is_in_exclusion_zone(box):
            self.img._img.paste(
                self.circle, 
                (box[0][0] + self.offset, box[0][1] + self.offset)
            )


class CustomRoundedDrawer(StyledPilQRModuleDrawer):
    """Rounded square drawer with configurable size and logo exclusion zone."""

    def __init__(self, size_ratio: float = 0.9, exclusion_zone: Optional[Tuple[float, float, float]] = None):
        """
        Args:
            size_ratio: Size of squares relative to module (0.1-1.5)
            exclusion_zone: Optional (center_x, center_y, radius) to skip dots inside logo area
        """
        super().__init__()
        self.size_ratio = max(0.1, min(1.5, size_ratio))
        self.exclusion_zone = exclusion_zone
    
    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.imgDraw = QRImageDraw.Draw(self.img._img)
        self.delta = (1 - self.size_ratio) * self.img.box_size / 2
    
    def _is_in_exclusion_zone(self, box):
        """Check if dot center is within the exclusion zone."""
        if self.exclusion_zone is None:
            return False

        center_x, center_y, radius = self.exclusion_zone
        dot_center_x = (box[0][0] + box[1][0]) / 2
        dot_center_y = (box[0][1] + box[1][1]) / 2
        distance = ((dot_center_x - center_x) ** 2 + (dot_center_y - center_y) ** 2) ** 0.5
        return distance < radius
    
    def drawrect(self, box, is_active: bool):
        if is_active and not self._is_in_exclusion_zone(box):
            smaller_box = (
                box[0][0] + self.delta,
                box[0][1] + self.delta,
                box[1][0] - self.delta,
                box[1][1] - self.delta,
            )
            # Calculate radius for rounded corners
            size = smaller_box[2] - smaller_box[0]
            radius = size * 0.3  # 30% corner radius
            self.imgDraw.rounded_rectangle(smaller_box, radius=radius, fill=self.img.paint_color)


class CustomDiamondDrawer(StyledPilQRModuleDrawer):
    """Diamond-shaped dot drawer with logo exclusion zone."""

    def __init__(self, size_ratio: float = 0.9, exclusion_zone: Optional[Tuple[float, float, float]] = None):
        super().__init__()
        self.size_ratio = max(0.1, min(1.5, size_ratio))
        self.exclusion_zone = exclusion_zone

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.imgDraw = QRImageDraw.Draw(self.img._img)
        self.delta = (1 - self.size_ratio) * self.img.box_size / 2

    def _is_in_exclusion_zone(self, box):
        if self.exclusion_zone is None:
            return False
        center_x, center_y, radius = self.exclusion_zone
        dot_center_x = (box[0][0] + box[1][0]) / 2
        dot_center_y = (box[0][1] + box[1][1]) / 2
        distance = ((dot_center_x - center_x) ** 2 + (dot_center_y - center_y) ** 2) ** 0.5
        return distance < radius

    def drawrect(self, box, is_active: bool):
        if is_active and not self._is_in_exclusion_zone(box):
            cx = (box[0][0] + box[1][0]) / 2
            cy = (box[0][1] + box[1][1]) / 2
            half = (box[1][0] - box[0][0]) * self.size_ratio / 2
            points = [(cx, cy - half), (cx + half, cy), (cx, cy + half), (cx - half, cy)]
            self.imgDraw.polygon(points, fill=self.img.paint_color)


class CustomSquareDrawer(StyledPilQRModuleDrawer):
    """Clean square dot drawer with logo exclusion zone."""

    def __init__(self, size_ratio: float = 0.9, exclusion_zone: Optional[Tuple[float, float, float]] = None):
        super().__init__()
        self.size_ratio = max(0.1, min(1.5, size_ratio))
        self.exclusion_zone = exclusion_zone

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.imgDraw = QRImageDraw.Draw(self.img._img)
        self.delta = (1 - self.size_ratio) * self.img.box_size / 2

    def _is_in_exclusion_zone(self, box):
        if self.exclusion_zone is None:
            return False
        center_x, center_y, radius = self.exclusion_zone
        dot_center_x = (box[0][0] + box[1][0]) / 2
        dot_center_y = (box[0][1] + box[1][1]) / 2
        distance = ((dot_center_x - center_x) ** 2 + (dot_center_y - center_y) ** 2) ** 0.5
        return distance < radius

    def drawrect(self, box, is_active: bool):
        if is_active and not self._is_in_exclusion_zone(box):
            self.imgDraw.rectangle(
                [box[0][0] + self.delta, box[0][1] + self.delta,
                 box[1][0] - self.delta, box[1][1] - self.delta],
                fill=self.img.paint_color
            )


class WeddingQRGenerator:
    """Generate stylized QR codes perfect for wedding invitations."""
    
    # Beautiful color presets for weddings
    COLOR_PRESETS = {
        'navy': '#445E7C',      # Navy blue (like your reference image)
        'gold': '#D4AF37',       # Elegant gold
        'rose_gold': '#B76E79', # Rose gold
        'burgundy': '#800020',   # Deep burgundy
        'sage': '#9CAF88',       # Sage green
        'dusty_blue': '#8BA9C2', # Dusty blue
        'black': '#000000',      # Classic black
        'charcoal': '#36454F',   # Soft charcoal
    }
    
    def __init__(self):
        self.qr = None
        
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _resolve_color(self, color: str) -> Tuple[int, int, int]:
        """Resolve color name or hex string to RGB tuple."""
        if color in self.COLOR_PRESETS:
            return self._hex_to_rgb(self.COLOR_PRESETS[color])
        return self._hex_to_rgb(color)

    def _build_qr_code(self, data: str, error_correction: str, version: Optional[int], size: int):
        """Build QRCode object with optimal box_size for target output size."""
        ec_levels = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H,
        }
        ec = ec_levels.get(error_correction.upper(), qrcode.constants.ERROR_CORRECT_H)
        qr_version = max(1, min(40, int(version))) if version is not None else None

        # First pass to determine module count
        qr = qrcode.QRCode(version=qr_version, error_correction=ec, box_size=10, border=2)
        qr.add_data(data)
        qr.make(fit=True)

        # Calculate optimal box_size for high quality output
        modules = qr.modules_count
        optimal_box_size = max(30, size // (modules + 4))

        # Recreate with optimal box size
        qr = qrcode.QRCode(version=qr_version, error_correction=ec, box_size=optimal_box_size, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        return qr
    
    def _create_rounded_finder_pattern(self, size: int, color: tuple, bg_color: tuple = (255, 255, 255)) -> Image.Image:
        """Create a single rounded finder pattern (the big corner squares)."""
        img = Image.new('RGBA', (size, size), bg_color + (255,))
        draw = ImageDraw.Draw(img)
        
        # Outer rounded square
        outer_radius = size // 7
        draw.rounded_rectangle(
            [0, 0, size - 1, size - 1],
            radius=outer_radius,
            fill=color + (255,)
        )
        
        # White middle rounded square
        margin = size // 7
        inner_radius = outer_radius - 2
        draw.rounded_rectangle(
            [margin, margin, size - margin - 1, size - margin - 1],
            radius=inner_radius,
            fill=bg_color + (255,)
        )
        
        # Inner filled rounded square
        inner_margin = size // 7 * 2
        center_radius = outer_radius - 4
        draw.rounded_rectangle(
            [inner_margin, inner_margin, size - inner_margin - 1, size - inner_margin - 1],
            radius=center_radius,
            fill=color + (255,)
        )
        
        return img
    
    def generate(self, request=None, **kwargs):
        """
        Generate a styled QR code and return PNG bytes.

        Accepts a QRRequest instance, or falls back to keyword arguments for
        backward-compatible callers.

        Returns:
            QRResult with PNG image bytes and image dimensions.
        """
        try:
            from models import QRRequest, QRResult
        except ImportError:
            from .models import QRRequest, QRResult

        if request is None:
            request = QRRequest(**kwargs)

        qr_color = self._resolve_color(request.color)
        bg_color = self._hex_to_rgb(request.background_color)

        qr = self._build_qr_code(
            request.data, request.error_correction, request.version, request.size
        )

        print(f"Density: Version {qr.version} ({qr.modules_count}x{qr.modules_count} modules)")

        # Calculate exclusion zone for logo (passed per-instance, not class-level)
        exclusion_zone = None
        if request.logo_path and os.path.exists(request.logo_path):
            generated_size = (qr.modules_count + 4) * qr.box_size
            center = generated_size / 2
            exclusion_radius = (
                (generated_size * request.logo_size_ratio / 2)
                + (generated_size * request.logo_padding)
            )
            exclusion_zone = (center, center, exclusion_radius)

        style_map = {
            "circles": CustomCircleDrawer,
            "rounded": CustomRoundedDrawer,
            "diamond": CustomDiamondDrawer,
            "square": CustomSquareDrawer,
        }
        drawer_cls = style_map.get(request.style, CustomCircleDrawer)
        module_drawer = drawer_cls(size_ratio=request.dot_size, exclusion_zone=exclusion_zone)

        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=SolidFillColorMask(
                back_color=bg_color,
                front_color=qr_color,
            )
        )

        img = img.convert('RGBA')

        current_size = img.size[0]
        if current_size != request.size:
            img = img.resize((request.size, request.size), Image.Resampling.LANCZOS)

        # Calculate finder pattern positions and size
        module_size = request.size / (qr.modules_count + 4)
        finder_size = int(7 * module_size)
        border_offset = int(2 * module_size)

        padding = int(module_size * 0.5)
        draw = ImageDraw.Draw(img)

        # Clear top-left
        draw.rectangle(
            [border_offset - padding, border_offset - padding,
             border_offset + finder_size + padding, border_offset + finder_size + padding],
            fill=bg_color + (255,)
        )

        # Clear top-right
        top_right_x = request.size - border_offset - finder_size
        draw.rectangle(
            [top_right_x - padding, border_offset - padding,
             top_right_x + finder_size + padding, border_offset + finder_size + padding],
            fill=bg_color + (255,)
        )

        # Clear bottom-left
        bottom_left_y = request.size - border_offset - finder_size
        draw.rectangle(
            [border_offset - padding, bottom_left_y - padding,
             border_offset + finder_size + padding, bottom_left_y + finder_size + padding],
            fill=bg_color + (255,)
        )

        # Create and paste custom rounded finder patterns
        finder = self._create_rounded_finder_pattern(finder_size, qr_color, bg_color)

        img.paste(finder, (border_offset, border_offset), finder)
        img.paste(finder, (top_right_x, border_offset), finder)
        img.paste(finder, (border_offset, bottom_left_y), finder)

        if request.logo_path and os.path.exists(request.logo_path):
            img = self._add_logo(img, request.logo_path, request.logo_size_ratio, bg_color, request.logo_padding)

        # Composite RGBA onto RGB before PNG encode
        final_img = Image.new('RGB', img.size, bg_color)
        final_img.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)

        buf = io.BytesIO()
        final_img.save(buf, 'PNG', quality=95)
        image_bytes = buf.getvalue()

        return QRResult(
            image_bytes=image_bytes,
            content_type="image/png",
            width=final_img.width,
            height=final_img.height,
        )
    
    def _add_logo(
        self, 
        qr_img: Image.Image, 
        logo_path: str, 
        size_ratio: float,
        bg_color: tuple,
        padding_ratio: float = 0.03
    ) -> Image.Image:
        """Add a logo to the center of the QR code. Dots already avoid this area."""
        logo = Image.open(logo_path).convert('RGBA')
        
        # Calculate logo size
        qr_size = qr_img.size[0]
        logo_max_size = int(qr_size * size_ratio)
        
        # Resize logo maintaining aspect ratio
        logo.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
        
        # Calculate center position
        pos_x = (qr_size - logo.size[0]) // 2
        pos_y = (qr_size - logo.size[1]) // 2
        
        # Just paste the logo - dots already avoid this area!
        qr_img.paste(logo, (pos_x, pos_y), logo)
        
        return qr_img
    
    def _round_corners(self, img: Image.Image, radius: int) -> Image.Image:
        """Apply rounded corners to an image."""
        # Create mask
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle(
            [0, 0, img.size[0] - 1, img.size[1] - 1],
            radius=radius,
            fill=255
        )
        
        # Apply mask
        output = Image.new('RGBA', img.size, (0, 0, 0, 0))
        output.paste(img, mask=mask)
        
        return output


def main():
    """Example usage of the QR generator."""
    generator = WeddingQRGenerator()
    
    # Example: Generate a wedding invitation QR code
    # Replace with your actual wedding website URL
    wedding_url = "https://yourwedding.com/rsvp"
    
    print("=" * 50)
    print("🎊 Wedding QR Code Generator")
    print("=" * 50)
    
    # Generate basic QR code (no logo)
    generator.generate(
        data=wedding_url,
        output_path="output/wedding_qr_basic.png",
        color="navy",
        style="circles",
        size=1000
    )
    
    # If you have a logo, uncomment this:
    # generator.generate(
    #     data=wedding_url,
    #     output_path="output/wedding_qr_with_logo.png",
    #     logo_path="logos/your_logo.png",
    #     color="navy",
    #     style="circles",
    #     size=1000,
    #     logo_size_ratio=0.25
    # )
    
    print("\n📋 Available color presets:")
    for name, hex_val in generator.COLOR_PRESETS.items():
        print(f"   • {name}: {hex_val}")
    
    print("\n💡 Tips:")
    print("   • Use error_correction='H' when adding a logo (default)")
    print("   • Keep logo_size_ratio between 0.2-0.3 for best scannability")
    print("   • Test the QR code with your phone before printing!")


if __name__ == "__main__":
    main()

