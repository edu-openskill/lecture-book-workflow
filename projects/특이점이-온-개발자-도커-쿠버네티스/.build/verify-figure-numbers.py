"""각 챕터의 그림 번호가 등장 순서대로 1, 2, 3, ... 으로 매겨졌는지 검증"""
import re
from pathlib import Path

CHAPTERS_DIR = Path(__file__).resolve().parent.parent / "chapters"

CAPTION_RE = re.compile(r"^\*그림 (\d+)-(\d+)\.\s")


def verify(path: Path):
    chapter_num = int(path.stem.split("-")[0])
    lines = path.read_text(encoding="utf-8").splitlines()
    nums = []
    for i, line in enumerate(lines):
        m = CAPTION_RE.match(line)
        if not m:
            continue
        n, k = int(m.group(1)), int(m.group(2))
        nums.append((i + 1, n, k))

    print(f"\n=== {path.name} (챕터 {chapter_num}) ===")
    print(f"캡션 {len(nums)}개")

    expected = 1
    bad = []
    for ln, n, k in nums:
        if n != chapter_num:
            bad.append(f"L{ln}: 챕터 번호 불일치 ({n}, 기대 {chapter_num})")
        if k != expected:
            bad.append(f"L{ln}: 그림 {n}-{k} (기대 {chapter_num}-{expected})")
        expected += 1

    if bad:
        for b in bad:
            print(f"  [X] {b}")
    else:
        print(f"  [OK] {chapter_num}-1 ~ {chapter_num}-{len(nums)} 순차 정렬")


for chapter_path in sorted(CHAPTERS_DIR.glob("*.md")):
    verify(chapter_path)
