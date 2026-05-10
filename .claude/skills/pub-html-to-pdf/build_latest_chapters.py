#!/usr/bin/env python3
"""
build_latest_chapters.py — 도커·쿠버네티스 책의 챕터별 최신본 HTML만 PDF로 변환.

build_pdf.py의 render_pdf 함수를 재사용하되,
.build/ 안에 누적된 v1~vN 모든 버전을 변환하지 않고 챕터별 최신본 6개만 처리한다.

사용법:
  python .claude/skills/pub-html-to-pdf/build_latest_chapters.py
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_pdf import render_pdf  # noqa: E402

REPO_ROOT = HERE.parent.parent.parent
PROJECT = REPO_ROOT / "projects" / "특이점이-온-개발자-도커-쿠버네티스"
BUILD_DIR = PROJECT / ".build"
PDF_DIR = BUILD_DIR / "pdf"

CHAPTERS = [
    "01-왜-컨테이너인가-v5",
    "02-Docker-이해하기-v5",
    "03-Docker-다루기-v7",
    "04-Kubernetes-시작하기-v6",
    "05-Kubernetes-네트워킹-v8",
    "06-Kubernetes-운영하기-v5",
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

    merged = PDF_DIR / "특이점이-온-개발자-도커-쿠버네티스.pdf"
    print(f"[>] 6개 PDF 병합 → {merged.name}")
    from pypdf import PdfWriter

    writer = PdfWriter()
    for pdf in chapter_pdfs:
        writer.append(str(pdf))
    with open(merged, "wb") as f:
        writer.write(f)
    writer.close()
    print(f"[OK] 병합 완료: {merged}")
    print("[DONE] 챕터별 PDF + 통합 PDF 생성 완료")
    return 0


if __name__ == "__main__":
    sys.exit(main())
