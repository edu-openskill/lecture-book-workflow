#!/usr/bin/env python3
"""
build_pdf.py — pub-html-build이 생성한 HTML 프리뷰를 Playwright Chromium으로 A4 PDF로 변환.

정식 전자책 PDF는 `pub-build`(Typst) 파이프라인으로 생성한다. 이 스킬은 프리뷰 한 장을
파일로 공유하고 싶을 때만 사용하는 유틸.

의존성:
  pip install playwright
  python -m playwright install chromium
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.parse import quote


PAGEDJS_CDN = "https://unpkg.com/pagedjs@0.4.3/dist/paged.polyfill.js"


def find_html_files(build_dir: Path, which: int | None) -> list[Path]:
    files = sorted(build_dir.glob("[0-9][0-9]-*.html"))
    if which is not None:
        files = [f for f in files if f.name.startswith(f"{which:02d}-")]
    return files


def render_pdf(html_path: Path, pdf_path: Path, pagedjs: bool) -> None:
    """Playwright로 HTML을 PDF로 렌더한다."""
    from playwright.sync_api import sync_playwright

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    url = "file://" + quote(str(html_path.resolve()))

    with sync_playwright() as p:
        browser = p.chromium.launch()
        # HiDPI 뷰포트로 이미지 리샘플링 화질 확보
        context = browser.new_context(
            viewport={"width": 1240, "height": 1754},
            device_scale_factor=2,
        )
        page = context.new_page()
        page.goto(url, wait_until="networkidle")
        if pagedjs:
            # PDF 렌더링 시에만 Paged.js 주입 — HTML 파일은 건드리지 않음
            page.add_script_tag(url=PAGEDJS_CDN)
            page.wait_for_function(
                "() => window.PagedPolyfill && document.querySelector('.pagedjs_pages')",
                timeout=60000,
            )
            page.wait_for_timeout(500)
            page.pdf(
                path=str(pdf_path),
                prefer_css_page_size=True,
                print_background=True,
            )
        else:
            page.emulate_media(media="print")
            page.pdf(
                path=str(pdf_path),
                format="A4",
                margin={
                    "top": "22mm",
                    "bottom": "22mm",
                    "left": "18mm",
                    "right": "18mm",
                },
                print_background=True,
            )
        browser.close()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="pub-html-build 산출 HTML을 Playwright로 A4 PDF로 변환"
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        required=True,
        help="책 프로젝트 루트 경로 (예: projects/사내AI비서_v2)",
    )
    parser.add_argument(
        "--chapter",
        type=int,
        default=None,
        help="특정 챕터 번호만 변환 (예: --chapter 11)",
    )
    parser.add_argument(
        "--no-pagedjs",
        action="store_true",
        help="Paged.js 주입 없이 Chromium 기본 인쇄로 렌더 (빠름, 조판 품질 낮음)",
    )
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    build_dir = project_root / ".build"
    if not build_dir.is_dir():
        print(
            f"❌ {build_dir} 를 찾지 못했습니다. 먼저 pub-html-build로 HTML을 빌드하세요.\n"
            f"   python .claude/skills/pub-html-build/build_html.py "
            f"--project-root {args.project_root} --chapter {args.chapter or 'N'}",
            file=sys.stderr,
        )
        return 1

    files = find_html_files(build_dir, args.chapter)
    if not files:
        print(
            f"❌ {build_dir} 안에 변환할 HTML이 없습니다. pub-html-build로 먼저 빌드하세요.",
            file=sys.stderr,
        )
        return 1

    pdf_dir = build_dir / "pdf"
    use_pagedjs = not args.no_pagedjs

    for html_path in files:
        print(f"📄 {html_path.name}")
        pdf_path = pdf_dir / f"{html_path.stem}.pdf"
        render_pdf(html_path, pdf_path, use_pagedjs)
        print(f"  ✅ PDF: {pdf_path.relative_to(project_root)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
