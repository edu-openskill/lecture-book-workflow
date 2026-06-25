#!/usr/bin/env python3
"""수학·LLM 별책 — PDF 빌드 설정.
범용 엔진(pub-build 스킬의 typst_builder.py)을 import하여 build(CONFIG) 호출.
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

CONFIG = {
    "title": "수학·LLM 별책",
    "base": PROJECT,
    "assets_dir": PROJECT / "assets",
    "mermaid_out": BUILD / "_mermaid_images",
    "template": PROJECT / "book" / "book.typ",
    "font_path": None,                                 # 시스템 폰트(Noto Sans KR/Malgun Gothic) 자동 탐색
    "front": [],
    "chapters": [
        PROJECT / "chapters" / "01-가장낮은점하나.md",
    ],
    "back": [],
    "output_md": BUILD / "통합.md",
    "output_typ": BUILD / "수학-LLM-별책.typ",
    "output_pdf": PROJECT / "book" / "수학-LLM-별책-sample.pdf",
    "layout_checker": str(LAYOUT_CHECKER),             # pub-layout-check 스킬 (PyMuPDF 필요)
}

if __name__ == "__main__":
    BUILD.mkdir(parents=True, exist_ok=True)
    (BUILD / "_mermaid_images").mkdir(parents=True, exist_ok=True)
    typst_builder.build(CONFIG)
