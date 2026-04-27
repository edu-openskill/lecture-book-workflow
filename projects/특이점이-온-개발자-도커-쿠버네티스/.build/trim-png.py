"""흰 여백을 트림하고 균등한 여백을 추가한다.

사용: trim-png.py <png_path> [margin]
- margin 기본값: 12 (px)
- 결과는 같은 경로에 덮어씀
"""
import sys
from PIL import Image, ImageChops


def trim(image_path: str, margin: int = 12) -> None:
    img = Image.open(image_path).convert("RGB")
    bg = Image.new("RGB", img.size, (255, 255, 255))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    if bbox is None:
        return
    cropped = img.crop(bbox)
    final = Image.new("RGB", (cropped.width + 2 * margin, cropped.height + 2 * margin), (255, 255, 255))
    final.paste(cropped, (margin, margin))
    final.save(image_path, "PNG")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: trim-png.py <png_path> [margin]", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    m = int(sys.argv[2]) if len(sys.argv) >= 3 else 12
    trim(path, m)
