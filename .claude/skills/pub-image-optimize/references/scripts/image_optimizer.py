#!/usr/bin/env python3
"""이미지 최적화 독립 스크립트

이미지 파일의 공백을 분석하고 자동으로 잘라냅니다.

사용법:
    python3 image_optimizer.py <path>              # 처리 (파일 또는 디렉토리)
    python3 image_optimizer.py <path> --dry-run     # 분석만 (수정 안 함)
    python3 image_optimizer.py <path> --padding 10  # 패딩 10px

의존성: pip install Pillow
"""

import sys
from pathlib import Path


def analyze_whitespace(img_path: Path, padding: int = 14) -> dict:
    """이미지의 공백 영역을 분석하여 통계 반환"""
    from PIL import Image, ImageChops

    img = Image.open(img_path).convert("RGB")
    bg = Image.new("RGB", img.size, (255, 255, 255))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()

    if not bbox:
        return {
            "path": str(img_path),
            "size": img.size,
            "trim_top": 0,
            "trim_bottom": 0,
            "trim_left": 0,
            "trim_right": 0,
            "trim_total": 0,
            "should_crop": False,
        }

    trim_top = bbox[1]
    trim_bottom = img.height - bbox[3]
    trim_left = bbox[0]
    trim_right = img.width - bbox[2]
    trim_total = trim_top + trim_bottom + trim_left + trim_right

    return {
        "path": str(img_path),
        "size": img.size,
        "content_bbox": bbox,
        "trim_top": trim_top,
        "trim_bottom": trim_bottom,
        "trim_left": trim_left,
        "trim_right": trim_right,
        "trim_total": trim_total,
        "trim_vertical": trim_top + trim_bottom,
        "should_crop": (trim_top + trim_bottom) > 20,
    }


def autocrop_image(img_path: Path, padding: int = 14, dry_run: bool = False) -> dict:
    """이미지 공백 제거. dry_run=True이면 분석만."""
    from PIL import Image, ImageChops

    stats = analyze_whitespace(img_path, padding)

    if not stats["should_crop"]:
        stats["action"] = "skip"
        return stats

    if dry_run:
        stats["action"] = "would_crop"
        return stats

    # 실제 잘라내기
    img = Image.open(img_path).convert("RGB")
    bg = Image.new("RGB", img.size, (255, 255, 255))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()

    if bbox:
        bbox = (
            max(0, bbox[0] - padding),
            max(0, bbox[1] - padding),
            min(img.width, bbox[2] + padding),
            min(img.height, bbox[3] + padding),
        )
        cropped = img.crop(bbox)
        cropped.save(img_path)
        stats["action"] = "cropped"
        stats["new_size"] = cropped.size
    else:
        stats["action"] = "skip"

    return stats


def process_path(target: Path, padding: int = 14, dry_run: bool = False) -> list[dict]:
    """파일 또는 디렉토리 처리"""
    results = []

    if target.is_file():
        if target.suffix.lower() in ('.png', '.jpg', '.jpeg'):
            results.append(autocrop_image(target, padding, dry_run))
    elif target.is_dir():
        for ext in ('*.png', '*.jpg', '*.jpeg'):
            for img_path in sorted(target.rglob(ext)):
                results.append(autocrop_image(img_path, padding, dry_run))
    else:
        print(f"[오류] 경로 없음: {target}")

    return results


def print_results(results: list[dict], dry_run: bool = False):
    """결과 출력"""
    if not results:
        print("   처리할 이미지 없음")
        return

    mode = "분석" if dry_run else "처리"
    print(f"\n   이미지 {mode} 결과 ({len(results)}개)")
    print("   " + "-" * 55)

    cropped = 0
    skipped = 0

    for r in results:
        name = Path(r["path"]).name
        action = r["action"]
        w, h = r["size"]

        if action in ("cropped", "would_crop"):
            cropped += 1
            trim_v = r["trim_vertical"]
            marker = "[잘라냄]" if action == "cropped" else "[잘라낼 예정]"
            if "new_size" in r:
                nw, nh = r["new_size"]
                print(f"   {marker} {name}: {w}x{h} -> {nw}x{nh} (상하 {trim_v}px 제거)")
            else:
                print(f"   {marker} {name}: {w}x{h} (상하 {trim_v}px 제거 가능)")
        else:
            skipped += 1

    print("   " + "-" * 55)
    print(f"   {mode} 완료: {cropped}개 {mode}, {skipped}개 건너뜀")


def main():
    args = sys.argv[1:]

    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0)

    target = Path(args[0])
    dry_run = '--dry-run' in args
    padding = 6

    if '--padding' in args:
        idx = args.index('--padding')
        if idx + 1 < len(args):
            padding = int(args[idx + 1])

    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print("[오류] Pillow 미설치 (pip install Pillow)")
        sys.exit(1)

    results = process_path(target, padding, dry_run)
    print_results(results, dry_run)


if __name__ == "__main__":
    main()
