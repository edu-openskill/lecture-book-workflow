#!/usr/bin/env python3
"""사내AI비서_v2 — Typst 기반 PDF 빌드 스크립트

실행:
    cd projects/사내AI비서_v2
    python3 book/build_pdf_typst.py           # 통합 PDF
    python3 book/build_pdf_typst.py --chapter 01  # CH01만 개별 빌드
    python3 book/build_pdf_typst.py --all     # 챕터별 개별 PDF 전부
"""

import sys
from pathlib import Path

# 스킬 엔진 경로 추가
SKILL_SCRIPTS = Path(__file__).resolve().parents[3] / ".claude" / "skills" / "pub-build" / "references" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

import typst_builder

# ── 프로젝트 경로 ──
BASE = Path(__file__).resolve().parent.parent  # projects/사내AI비서_v2
BOOK = BASE / "book"
CHAPTERS = BASE / "chapters"
FRONT = BOOK / "front"
BACK = BOOK / "back"
ASSETS = BASE / "assets"

CHAPTER_FILES = [
    CHAPTERS / "00-들어가며.md",
    CHAPTERS / "01-환각과-RAG의-첫-만남.md",
    CHAPTERS / "02-일단-사내-시스템부터.md",
    CHAPTERS / "03-어떤-문서를-넣을까.md",
    CHAPTERS / "04-문서를-지식으로-바꾸다.md",
    CHAPTERS / "05-드디어-답해준다.md",
    CHAPTERS / "06-연차도-규정도-한번에.md",
    CHAPTERS / "07-실제로-써보니.md",
    CHAPTERS / "08-엉뚱한-문서를-가져온다.md",
    CHAPTERS / "09-질문을-제대로-이해-못한다.md",
    CHAPTERS / "10-PDF-이미지까지-잡아라.md",
]

CONFIG = {
    "title": "환각에서 시작하는 RAG",
    "subtitle": "사내 AI 비서를 만들며 배우는 검색 증강 생성",
    "base": BASE,
    "assets_dir": ASSETS,
    "template": BOOK / "templates" / "book.typ",
    "font_path": Path.home() / "Library" / "Fonts",
    "pre_toc": [
        FRONT / "preface.md",
        FRONT / "github-source.md",
    ],
    "front": [
        FRONT / "prologue.md",
    ],
    "chapters": CHAPTER_FILES,
    "back": [
        BACK / "epilogue.md",
    ],
    "output_md": BOOK / "ConnectHR_통합본.md",
    "output_typ": BOOK / "ConnectHR_통합본.typ",
    "output_pdf": BOOK / "ConnectHR_통합본.pdf",
    "output_dir": BOOK / "chapter_pdfs",
    "mermaid_out": BOOK / "_mermaid_images",
    "cover_data": {
        "series": "특이점이 온 개발자",
        "series_sub": "개념편",
        "authors": "최주호, 류재성, 김주혁",
        "badges": ["RAG", "LangChain", "ChromaDB", "FastAPI",
                   "LLM", "임베딩", "리랭킹", "HyDE", "Vision LLM"],
        "publisher": "오픈스킬북스",
        "accent_color": (45, 99, 235),
        "top_descs": ["LLM 환각이 두려운 개발자를 위한",
                      "RAG 파이프라인 처음부터 끝까지",
                      "이야기로 시작하는 실습서가 필요할 때"],
        "main_words": [
            ("환각에서", 38, True, "L", -2, "dark"),
            ("시작하는", 14, True, "L", -2, "gray"),
            ("RAG", 55, True, "R", 0, "dark", True),
        ],
    },
}


def build_single_chapter(ch_num: str):
    """특정 챕터 하나만 개별 PDF 빌드"""
    for f in CHAPTER_FILES:
        if f.name.startswith(ch_num):
            print(f"챕터 개별 빌드: {f.name}")
            result = typst_builder.build_chapter(f, CONFIG)
            if result:
                print(f"완료: {result}")
            return
    print(f"[오류] 챕터 '{ch_num}'을 찾을 수 없습니다.")


def build_all_chapters():
    """모든 챕터를 개별 PDF로 빌드"""
    print("전체 챕터 개별 빌드")
    print("=" * 50)
    results = []
    for f in CHAPTER_FILES:
        result = typst_builder.build_chapter(f, CONFIG)
        if result:
            results.append(result)
    print(f"\n{'=' * 50}")
    print(f"완료: {len(results)}/{len(CHAPTER_FILES)} 챕터 빌드")


def _import_cover():
    _cover_scripts = SKILL_SCRIPTS.parents[2] / "pub-studio" / "references" / "scripts"
    if str(_cover_scripts) not in sys.path:
        sys.path.insert(0, str(_cover_scripts))
    import cover_generator
    return cover_generator


if __name__ == "__main__":
    if "--design" in sys.argv:
        idx = sys.argv.index("--design")
        if idx + 1 < len(sys.argv):
            CONFIG["design"] = sys.argv[idx + 1]

    ebook = "--ebook" in sys.argv
    cg = _import_cover()

    if "--cover-preview" in sys.argv:
        cg.wizard_step1_layout(CONFIG, ASSETS, ebook=ebook)
    elif "--cover-shadow" in sys.argv:
        mw = CONFIG["cover_data"]["main_words"]
        cg.wizard_step2_shadow(CONFIG, ASSETS, mw, ebook=ebook)
    elif "--cover-color" in sys.argv:
        mw = CONFIG["cover_data"]["main_words"]
        cg.wizard_step3_color(CONFIG, ASSETS, mw, ebook=ebook)
    elif "--cover-confirm" in sys.argv:
        mw = CONFIG["cover_data"]["main_words"]
        cg.wizard_step4_confirm(CONFIG, ASSETS, mw, ebook=ebook)
    elif "--cover-select" in sys.argv:
        idx = sys.argv.index("--cover-select")
        if idx + 1 < len(sys.argv):
            cg.select_cover_variation(ASSETS, int(sys.argv[idx + 1]))
    elif "--chapter" in sys.argv:
        idx = sys.argv.index("--chapter")
        if idx + 1 < len(sys.argv):
            build_single_chapter(sys.argv[idx + 1])
    elif "--all" in sys.argv:
        build_all_chapters()
    else:
        typst_builder.build(CONFIG)
