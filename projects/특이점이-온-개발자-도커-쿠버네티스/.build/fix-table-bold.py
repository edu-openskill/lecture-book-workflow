"""각 챕터의 표 안에 있는 **...** 패턴을 `...`로 변환.

표 라인 식별: 라인이 `|`로 시작하고 `|`로 끝나는 마크다운 테이블 행.
구분선(`|---|`)은 건드리지 않는다.
"""
import re
import sys
from pathlib import Path

CHAPTERS_DIR = Path(__file__).resolve().parent.parent / "chapters"

BOLD_RE = re.compile(r"\*\*([^*\n]+?)\*\*")
TABLE_LINE_RE = re.compile(r"^\s*\|.*\|\s*$")
SEPARATOR_RE = re.compile(r"^\s*\|[\s:|-]+\|\s*$")


def process(path: Path, dry: bool = False):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    changed = []

    for i, line in enumerate(lines):
        if not TABLE_LINE_RE.match(line):
            continue
        if SEPARATOR_RE.match(line):
            continue
        new_line, n = BOLD_RE.subn(r"`\1`", line)
        if n > 0:
            changed.append((i + 1, n, line.rstrip(), new_line.rstrip()))
            lines[i] = new_line

    if changed and not dry:
        path.write_text("".join(lines), encoding="utf-8")

    return changed


def main():
    dry = "--dry" in sys.argv
    total_files = 0
    total_replacements = 0
    for chapter_path in sorted(CHAPTERS_DIR.glob("*.md")):
        changed = process(chapter_path, dry=dry)
        if changed:
            total_files += 1
            n = sum(c[1] for c in changed)
            total_replacements += n
            print(f"\n=== {chapter_path.name} ({n}건) ===")
            for ln, count, before, after in changed:
                print(f"  L{ln}: {count}건")
                print(f"    BEFORE: {before}")
                print(f"    AFTER:  {after}")
    print(f"\n--- 총 {total_files}개 챕터, {total_replacements}건 변환 {'(dry-run)' if dry else ''} ---")


if __name__ == "__main__":
    main()
