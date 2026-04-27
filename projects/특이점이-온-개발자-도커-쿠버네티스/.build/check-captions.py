"""각 챕터에서 이미지와 캡션을 매칭하여 누락 식별"""
import re
import sys
from pathlib import Path

CHAPTERS_DIR = Path(__file__).resolve().parent.parent / "chapters"

IMAGE_RE = re.compile(r"^!\[\]\((.*?)\)\s*$")
# 캡션은 *그림 N-N. ...* 형태 또는 *...* 형태 (단, 따옴표로 시작하는 내면독백 제외)
CAPTION_RE = re.compile(r"^\*([^'\"].*?)\*\s*$")


def check_chapter(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    images = []  # [(line_num, image_path, caption_line_num, caption_text)]
    missing = []
    for i, line in enumerate(lines):
        m = IMAGE_RE.match(line)
        if not m:
            continue
        image_path = m.group(1)
        # 다음 비어있지 않은 라인 찾기
        j = i + 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1
        caption = None
        caption_line = None
        if j < len(lines):
            cm = CAPTION_RE.match(lines[j])
            if cm:
                caption = cm.group(1)
                caption_line = j + 1  # 1-based
        if caption is None:
            missing.append((i + 1, image_path))
        images.append((i + 1, image_path, caption_line, caption))
    return images, missing


def main():
    for chapter_path in sorted(CHAPTERS_DIR.glob("*.md")):
        images, missing = check_chapter(chapter_path)
        print(f"\n=== {chapter_path.name} ===")
        print(f"이미지 {len(images)}개, 누락 캡션 {len(missing)}개")
        if missing:
            for ln, img in missing:
                print(f"  L{ln}: {img}")


if __name__ == "__main__":
    main()
