#!/usr/bin/env python3
"""
build_latest_chapters_msa.py — MSA 책의 챕터 1~5 최신본 HTML만 PDF로 변환 후 하나로 병합.
build_pdf.render_pdf 재사용. 사용법: python .claude/skills/pub-html-to-pdf/build_latest_chapters_msa.py
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_pdf import render_pdf  # noqa: E402

REPO_ROOT = HERE.parent.parent.parent
PROJECT = REPO_ROOT / "projects" / "특이점이-온-개발자-MSA"
BUILD_DIR = PROJECT / ".build"
PDF_DIR = BUILD_DIR / "pdf"

CHAPTERS = [
    "01-MSA란-무엇인가-v4",
    "02-동기식-MSA-구현-v4",
    "03-클린-아키텍처와-Kubernetes-v4",
    "04-비동기-MSA-Kafka-v5",
    "05-실시간-알림-WebSocket-v5",
]


def main() -> int:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    chapter_pdfs: list[Path] = []
    for name in CHAPTERS:
        html = BUILD_DIR / f"{name}.html"
        pdf = PDF_DIR / f"{name}.pdf"
        if not html.exists():
            print(f"[!] HTML 없음: {html}")
            continue
        print(f"[>] {name} → PDF 변환 중")
        render_pdf(html, pdf, pagedjs=False)
        chapter_pdfs.append(pdf)
        print(f"[OK] {pdf}")

    if not chapter_pdfs:
        print("[!] 변환된 PDF 없음")
        return 1

    merged = PDF_DIR / "특이점이-온-개발자-MSA.pdf"
    print(f"[>] {len(chapter_pdfs)}개 PDF 병합 → {merged.name}")
    from pypdf import PdfWriter

    writer = PdfWriter()
    for pdf in chapter_pdfs:
        writer.append(str(pdf))
    with open(merged, "wb") as f:
        writer.write(f)
    writer.close()
    print(f"[OK] 병합 완료: {merged}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
