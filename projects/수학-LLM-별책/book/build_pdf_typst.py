#!/usr/bin/env python3
"""수학·LLM 별책 — PDF 빌드 설정.
범용 엔진(pub-build 스킬의 typst_builder.py)을 import하여 build(CONFIG) 호출.

사용법:
  python book/build_pdf_typst.py          # 전체 책(집필 완료 챕터 누적) → book/수학-LLM-별책-sample.pdf
  python book/build_pdf_typst.py 02       # 02 챕터만 → book/chapters-pdf/02-접으면두배.pdf
  python book/build_pdf_typst.py 접으면    # 파일명 일부로도 지정 가능
"""
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]          # projects/수학-LLM-별책
REPO = PROJECT.parents[1]                               # 저장소 루트
SKILL_SCRIPTS = REPO / ".claude" / "skills" / "pub-build" / "references" / "scripts"
LAYOUT_CHECKER = REPO / ".claude" / "skills" / "pub-layout-check" / "references" / "scripts" / "pdf_layout_checker.py"
sys.path.insert(0, str(SKILL_SCRIPTS))

import typst_builder  # noqa: E402

BUILD = PROJECT / "book" / "_build"
CHAPTERS_DIR = PROJECT / "chapters"
PER_CHAPTER_DIR = PROJECT / "book" / "chapters-pdf"

# 집필 완료된 챕터 (집필 순서대로 추가) — 전체 책 빌드에 사용
CHAPTERS = [
    CHAPTERS_DIR / "01-가장낮은점하나.md",
    CHAPTERS_DIR / "02-접으면두배.md",
    CHAPTERS_DIR / "03-지수의거울.md",
    CHAPTERS_DIR / "04-언덕의경사.md",
    CHAPTERS_DIR / "05-골짜기바닥찾기.md",
    CHAPTERS_DIR / "06-자기자신을미분하는수.md",
    CHAPTERS_DIR / "07-톱니바퀴연쇄.md",
    CHAPTERS_DIR / "08-안개산에서내려가기.md",
]


def base_config() -> dict:
    return {
        "title": "수학·LLM 별책",
        "base": PROJECT,
        "assets_dir": PROJECT / "assets",
        "mermaid_out": BUILD / "_mermaid_images",
        "template": PROJECT / "book" / "book.typ",
        "font_path": None,                             # 시스템 폰트(Noto Sans KR/Malgun Gothic) 자동 탐색
        "front": [],
        "back": [],
        "layout_checker": str(LAYOUT_CHECKER),         # pub-layout-check 스킬 (PyMuPDF 필요)
    }


def build_full() -> None:
    cfg = base_config()
    cfg["chapters"] = CHAPTERS
    cfg["output_md"] = BUILD / "통합.md"
    cfg["output_typ"] = BUILD / "수학-LLM-별책.typ"
    cfg["output_pdf"] = PROJECT / "book" / "수학-LLM-별책-sample.pdf"
    typst_builder.build(cfg)


def resolve_chapter(query: str) -> Path:
    """번호('02') 또는 파일명 일부('접으면')로 챕터 .md를 찾는다."""
    candidates = sorted(CHAPTERS_DIR.glob("*.md"))
    # 1) 번호 접두사 우선
    for c in candidates:
        if c.stem.startswith(query):
            return c
    # 2) 파일명 부분 일치
    for c in candidates:
        if query in c.stem:
            return c
    print(f"[error] '{query}'에 해당하는 챕터를 {CHAPTERS_DIR}에서 찾지 못했습니다.")
    print("        후보:", ", ".join(c.name for c in candidates) or "(없음)")
    sys.exit(1)


def build_chapter(query: str) -> None:
    ch = resolve_chapter(query)
    PER_CHAPTER_DIR.mkdir(parents=True, exist_ok=True)
    cfg = base_config()
    cfg["chapters"] = [ch]
    cfg["output_md"] = BUILD / f"_ch_{ch.stem}.md"
    cfg["output_typ"] = BUILD / f"_ch_{ch.stem}.typ"
    cfg["output_pdf"] = PER_CHAPTER_DIR / f"{ch.stem}.pdf"
    print(f"[챕터 빌드] {ch.name} → {cfg['output_pdf'].relative_to(PROJECT)}")
    typst_builder.build(cfg)


if __name__ == "__main__":
    BUILD.mkdir(parents=True, exist_ok=True)
    (BUILD / "_mermaid_images").mkdir(parents=True, exist_ok=True)
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg:
        build_chapter(arg)
    else:
        build_full()
