#!/usr/bin/env python3
"""
build_pdf_html.py — 마크다운 챕터를 HTML → PDF로 빌드.

흐름:
  chapters/NN-*.md
    → (커스텀 블록 + 코드블록 타이틀 전처리)
    → markdown-it-py
    → Jinja2 템플릿 병합
    → Playwright + Chromium 헤드리스 → PDF

의존성:
  pip install markdown-it-py mdit-py-plugins jinja2 playwright
  python -m playwright install chromium
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

# ----- 경로 기준 ----------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = PROJECT_ROOT / "book"
CHAPTERS_DIR = PROJECT_ROOT / "chapters"
ASSETS_DIR = PROJECT_ROOT / "assets"
STYLES_DIR = BOOK_DIR / "styles"
TEMPLATES_DIR = BOOK_DIR / "templates"
BUILD_DIR = BOOK_DIR / "build"
OUTPUT_DIR = BOOK_DIR / "output"


# ========== 코드블록 타이틀 전처리 =========================================
# 마크다운:
#   ```python [실습 N] ex01/file.py — 설명
#   code...
#   ```
#   ```bash [터미널] 타이틀
#   cmd
#   ```
# 위 형식을 표준 마크다운 코드블록으로 정제하고, 동시에 별도 html 렌더를 위해
# 플레이스홀더를 심는다. 단순화를 위해 직접 HTML로 치환한다.

CODE_TITLE_RE = re.compile(
    r"^```(?P<lang>[a-zA-Z0-9_+\-]+)(?:\s+\[(?P<badge>[^\]]+)\])?(?P<title>[^\n]*)\n"
    r"(?P<body>.*?)\n```",
    re.DOTALL | re.MULTILINE,
)


def _escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


_TODO_LINE_RE = re.compile(r'(\s*#\s*TODO:[^\n]*)', re.MULTILINE)
_PYGMENTS_TODO_RE = re.compile(r'<span class="(c1?)">(\s*#\s*TODO:[^<]*)</span>')


def _highlight_body(lang: str, body: str) -> str:
    """
    Pygments로 구문 강조된 HTML을 반환한다.
    - 지원 언어: Pygments 강조 + TODO 주석 span을 .cb-todo로 교체
    - 미지원 언어: HTML 이스케이프 후 TODO 라인만 .cb-todo로 래핑
    두 경로 모두 TODO는 한 번만 래핑된다 (이중 래핑 방지).
    """
    try:
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import HtmlFormatter
        from pygments.util import ClassNotFound
    except ImportError:
        return _wrap_todo_plain(_escape(body))

    lang_map = {
        "py": "python", "python": "python",
        "bash": "bash", "sh": "bash", "shell": "bash",
        "text": None, "plain": None,
        "markdown": "markdown", "md": "markdown",
        "js": "javascript", "ts": "typescript",
        "json": "json", "yaml": "yaml", "yml": "yaml",
        "sql": "sql", "html": "html", "css": "css",
    }
    pyg_name = lang_map.get(lang.lower(), lang.lower())
    if pyg_name is None:
        return _wrap_todo_plain(_escape(body))
    try:
        lexer = get_lexer_by_name(pyg_name, stripnl=False)
    except ClassNotFound:
        return _wrap_todo_plain(_escape(body))

    formatter = HtmlFormatter(nowrap=True)
    highlighted = highlight(body, lexer, formatter)
    if highlighted.endswith("\n"):
        highlighted = highlighted[:-1]

    # Pygments가 만든 TODO 주석 span 자체를 .cb-todo로 치환 (래핑 아닌 교체)
    highlighted = _PYGMENTS_TODO_RE.sub(
        lambda m: f'<span class="cb-todo">{m.group(2)}</span>',
        highlighted,
    )
    return highlighted


def _wrap_todo_plain(escaped_body: str) -> str:
    """이스케이프만 된 본문에서 TODO 라인을 .cb-todo로 감싼다."""
    return _TODO_LINE_RE.sub(
        lambda m: f'<span class="cb-todo">{m.group(1)}</span>',
        escaped_body,
    )


def _render_code_block(lang: str, badge: str | None, title: str, body: str) -> str:
    title = (title or "").strip().lstrip("—").strip()
    if title.startswith("- "):
        title = title[2:]

    cb_parts: list[str] = []
    if badge:
        badge_text = badge.strip()
        badge_cls = "badge"
        if re.search(r"터미널|bash|shell|cmd|터미", badge_text, re.I):
            badge_cls += " bash"
        elif re.search(r"설명", badge_text):
            badge_cls += " explain"
        elif re.search(r"참고", badge_text):
            badge_cls += " reference"
        cb_parts.append(f'<span class="{badge_cls}">{_escape(badge_text)}</span>')
    if title:
        cb_parts.append(_escape(title))

    cb_title_inner = " ".join(cb_parts)
    cb_title_html = f'<div class="cb-title">{cb_title_inner}</div>' if cb_title_inner else ''
    body_html = _highlight_body(lang, body)
    return (
        f'<div class="code-block highlight" data-lang="{lang}">'
        f'{cb_title_html}'
        f'{body_html}'
        f'</div>'
    )


def preprocess_code_blocks(md: str) -> tuple[str, dict[str, str]]:
    """
    '```lang [뱃지] 타이틀' 형식의 코드블록을 placeholder로 stash.
    마크다운 파서를 거친 후 placeholder를 HTML로 치환한다.
    코드블록 본문의 빈 줄이 CommonMark HTML block 경계를 깨면 안 되므로
    직접 HTML을 삽입하지 않고 토큰화한다.
    """
    stash: dict[str, str] = {}

    def sub(m: re.Match) -> str:
        key = f"CODEBLOCKTOKEN{len(stash):04d}"
        stash[key] = _render_code_block(
            m.group("lang"),
            m.group("badge"),
            m.group("title"),
            m.group("body"),
        )
        # 앞뒤 빈 줄로 문단 격리
        return f"\n\n{key}\n\n"

    return CODE_TITLE_RE.sub(sub, md), stash


def restore_code_blocks(html: str, stash: dict[str, str]) -> str:
    for key, block in stash.items():
        # 문단으로 감싸지면 벗겨내고 교체
        html = html.replace(f"<p>{key}</p>", block)
        html = html.replace(key, block)
    return html


# ========== 커스텀 컨테이너 ================================================
# :::name\n ... :::
# 중첩은 지원하지 않는다. 첫 줄이 제목(선택)이라고 간주하지 않고 그대로 렌더.

CONTAINER_RE = re.compile(
    r"^:::(?P<name>[a-zA-Z][a-zA-Z0-9_-]*)\s*\n(?P<inner>.*?)^:::\s*$",
    re.DOTALL | re.MULTILINE,
)

# 각 컨테이너 이름을 CSS 클래스로 매핑
CONTAINER_CLASSES = {
    "goal": "goal-box",
    "preview": "preview-notice",
    "prep": "prep-section-md",  # prep은 md 내부라 구조는 자유
    "tip": "tip",
    "note": "prep-note",
    "compare": "annotated-compare",
    "rag-pipeline": "rag-pipeline-box",
    "term-box": "term-box",
    "remember": "remember",
    "journey": "journey-forward",
    "result-fail": "result fail",
    "result-ok": "result ok",
}


# ========== Markdown 렌더러 ================================================
def make_md():
    from markdown_it import MarkdownIt
    from mdit_py_plugins.container import container_plugin

    md = MarkdownIt("commonmark", {"html": True, "linkify": True, "breaks": False})
    md.enable("table")
    md.enable("strikethrough")

    for name, cls in CONTAINER_CLASSES.items():
        def make_render(css_class):
            def render(self, tokens, idx, options, env):  # noqa: D401
                token = tokens[idx]
                if token.nesting == 1:
                    return f'<div class="{css_class}">\n'
                return '</div>\n'
            return render

        md.use(container_plugin, name, render=make_render(cls))

    return md


# ========== 대화 / 내면독백 전처리 ==========================================
# 마크다운의 `**캐릭터**: "대사"` 단독 문단 → <div class="dialogue">
# 내면독백 `*생각 내용*`이 문단 전체 → <p class="thought">
DIALOGUE_RE = re.compile(
    r"^\*\*(?P<speaker>팀장|동료|오픈이|선배|[가-힣]{1,6})\*\*:\s*(?P<line>.+?)$",
    re.MULTILINE,
)

INLINE_BOLD_RE = re.compile(r"\*\*([^*\n]+?)\*\*")
INLINE_CODE_RE = re.compile(r"`([^`\n]+?)`")


def _inline_markdown(text: str) -> str:
    """대화 라인 내부의 간단한 인라인 마크다운(**bold**, `code`)을 HTML로 치환."""
    text = INLINE_CODE_RE.sub(lambda m: f"<code>{m.group(1)}</code>", text)
    text = INLINE_BOLD_RE.sub(lambda m: f"<strong>{m.group(1)}</strong>", text)
    return text


def preprocess_dialogue(md: str) -> str:
    def dialogue_sub(m: re.Match) -> str:
        line = _inline_markdown(m.group("line").strip())
        return (
            f'<div class="dialogue">'
            f'<span class="speaker">{m.group("speaker")}</span>: '
            f'{line}'
            f'</div>'
        )

    md = DIALOGUE_RE.sub(dialogue_sub, md)

    # 내면독백: `*text*` 단독 문단 (단, 바로 앞 라인이 이미지 `![](..)`면 캡션이므로 스킵)
    lines = md.split("\n")
    out: list[str] = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        is_thought = (
            stripped.startswith("*")
            and stripped.endswith("*")
            and not stripped.startswith("**")
            and not stripped.endswith("**")
            and len(stripped) >= 4
            and stripped.count("*") == 2
        )
        if is_thought:
            prev = lines[i - 1].strip() if i > 0 else ""
            if prev.startswith("!["):
                out.append(line)
                continue
            inner = stripped[1:-1].strip()
            out.append(f'<p class="thought">{inner}</p>')
        else:
            out.append(line)
    return "\n".join(out)


# ========== 이미지 경로 보정 ================================================
IMG_RE = re.compile(r'<img\s+([^>]*?)src="([^"]+)"([^>]*)>', re.IGNORECASE)


def resolve_image_paths(html: str, md_file: Path) -> str:
    """
    마크다운의 이미지 경로(예: ../assets/CH01/...)를 build 폴더에서 접근 가능한
    상대 경로(./assets/CH01/...)로 변환. build/에 심링크가 이미 있어야 한다.
    """
    def sub(m: re.Match) -> str:
        before, src, after = m.group(1), m.group(2), m.group(3)
        if src.startswith(("http://", "https://", "data:", "file://", "/")):
            return m.group(0)
        # 마크다운 기준 상대경로를 프로젝트 루트 기준으로 해석
        resolved = (md_file.parent / src).resolve()
        try:
            rel = resolved.relative_to(PROJECT_ROOT)
        except ValueError:
            # 프로젝트 바깥이면 file:// 로 폴백
            return f'<img {before}src="file://{quote(str(resolved))}"{after}>'
        if not resolved.exists():
            print(f"  ⚠️  이미지 없음: {src} → {resolved}", file=sys.stderr)
        # build/에서 프로젝트 루트의 자원으로 접근
        return f'<img {before}src="./{rel.as_posix()}"{after}>'

    return IMG_RE.sub(sub, html)


def wrap_chapter_images(html: str) -> str:
    """
    이미지 단독 문단을 `<div class="chapter-image">...</div>`로 감싼다.
    케이스 1: `<p><img .../></p><p><em>caption</em></p>`
    케이스 2: `<p><img .../>\n<em>caption</em></p>` (같은 p 내부)
    케이스 3: `<p><img .../></p>` (캡션 없음)
    """
    # 케이스 2 먼저 — 같은 <p> 안에 <img> + <em> 캡션
    pattern_inline = re.compile(
        r'<p>\s*(<img\s+[^>]+/?>)\s*(?:<br\s*/?>)?\s*<em>(.*?)</em>\s*</p>',
        re.DOTALL,
    )

    # 케이스 1+3 — <p><img/></p> 뒤 선택적 <p><em>캡션</em></p>
    pattern_split = re.compile(
        r'<p>\s*(<img\s+[^>]+/?>)\s*</p>\s*'
        r'(?:<p><em>(.*?)</em></p>)?',
        re.DOTALL,
    )

    def make_wrap(img: str, caption: str | None) -> str:
        img_cls = "chapter-image"
        if 'terminal/' in img:
            img_cls += " terminal"
        elif 'diagram/' in img:
            img_cls += " diagram"
        elif 'gemini/' in img:
            img_cls += " gemini"
        caption_html = f'<div class="caption">{caption}</div>' if caption else ''
        return f'<div class="{img_cls}">{img}{caption_html}</div>'

    html = pattern_inline.sub(lambda m: make_wrap(m.group(1), m.group(2)), html)
    html = pattern_split.sub(lambda m: make_wrap(m.group(1), m.group(2)), html)
    return html


# ========== 챕터 빌드 ======================================================
@dataclass
class Chapter:
    number: int
    title: str
    md_path: Path
    html: str


def find_chapter_files(which: int | None = None) -> list[Path]:
    files = sorted(CHAPTERS_DIR.glob("[0-9][0-9]-*.md"))
    if which is not None:
        files = [f for f in files if f.name.startswith(f"{which:02d}-")]
    return files


def render_chapter(md_path: Path, md_renderer) -> Chapter:
    raw = md_path.read_text(encoding="utf-8")

    # 1. 코드블록을 placeholder로 stash (본문의 `#` 주석이 h1으로 해석되는 것 방지)
    pre, stash = preprocess_code_blocks(raw)

    # 1b. 대화·내면독백을 HTML로 치환
    pre = preprocess_dialogue(pre)

    # 2. 마크다운 → HTML
    html = md_renderer.render(pre)

    # 3. 코드블록 복원
    html = restore_code_blocks(html, stash)

    # 4. 이미지 래핑 + 경로 보정
    html = wrap_chapter_images(html)
    html = resolve_image_paths(html, md_path)

    # 4. 제목 추출
    m = re.search(r"^#\s+(.*)", raw, re.MULTILINE)
    title = (m.group(1) if m else md_path.stem).strip()

    # 5. 챕터 번호
    n = int(md_path.name[:2])

    return Chapter(number=n, title=title, md_path=md_path, html=html)


# ========== Jinja2 템플릿 병합 =============================================
def ensure_build_symlinks() -> None:
    """build 폴더에서 프로젝트 자원(styles, assets)을 상대 경로로 접근할 수 있게
    심링크를 만든다. 이미 있으면 스킵."""
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    targets = {
        "styles": BOOK_DIR / "styles",
        "assets": ASSETS_DIR,
    }
    for name, src in targets.items():
        link = BUILD_DIR / name
        if link.is_symlink() or link.exists():
            continue
        try:
            link.symlink_to(src)
        except OSError as exc:
            print(f"  ⚠️  심링크 생성 실패 {name}: {exc}", file=sys.stderr)


def render_html_file(chapter: Chapter) -> Path:
    """
    HTML 프리뷰 파일 생성. 브라우저에서 한 장으로 흐르게 읽을 수 있도록
    Paged.js는 항상 **로드하지 않는다**. PDF 생성 시에는 Playwright가
    런타임에 Paged.js 스크립트를 주입한다 (render_pdf 참고).
    """
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html"]),
    )
    tpl = env.get_template("chapter-template.html")

    ensure_build_symlinks()
    out_html = BUILD_DIR / f"{chapter.md_path.stem}.html"

    html = tpl.render(
        chapter={"title": chapter.title, "html": chapter.html},
        fonts_css="./styles/fonts.css",
        tokens_css="./styles/tokens.css",
        base_css="./styles/base.css",
        components_css="./styles/components.css",
        diagrams_css="./styles/diagrams.css",
        print_css="./styles/print.css",
        pagedjs=False,  # HTML 프리뷰는 항상 단일 페이지 흐름
    )
    out_html.write_text(html, encoding="utf-8")
    return out_html


# ========== PDF 렌더링 =====================================================
PAGEDJS_CDN = "https://unpkg.com/pagedjs@0.4.3/dist/paged.polyfill.js"


def render_pdf(html_path: Path, pdf_path: Path, pagedjs: bool) -> None:
    """
    Playwright로 HTML을 PDF로 렌더.
    pagedjs=True면 page.goto 후 Paged.js 스크립트를 주입해 페이지 조판을 시킨다.
    HTML 파일 자체엔 Paged.js가 들어 있지 않기 때문에 브라우저 프리뷰는
    영향을 받지 않는다.
    """
    from playwright.sync_api import sync_playwright

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
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


# ========== 메인 ============================================================
def main() -> int:
    parser = argparse.ArgumentParser(description="HTML→PDF 챕터 빌더")
    parser.add_argument(
        "--chapter",
        type=int,
        default=None,
        help="특정 챕터 번호만 빌드 (예: --chapter 1)",
    )
    parser.add_argument(
        "--html-only",
        action="store_true",
        help="HTML 중간 산출물만 만들고 PDF는 생략",
    )
    parser.add_argument(
        "--no-pagedjs",
        action="store_true",
        help="Paged.js 없이 Chromium 기본 인쇄로 PDF 생성 (빠름)",
    )
    args = parser.parse_args()

    use_pagedjs = not args.no_pagedjs
    md = make_md()

    files = find_chapter_files(args.chapter)
    if not files:
        print("❌ 빌드할 챕터 파일을 찾지 못했습니다.", file=sys.stderr)
        return 1

    for md_path in files:
        print(f"📖 {md_path.name}")
        chapter = render_chapter(md_path, md)

        html_path = render_html_file(chapter)
        print(f"  ✅ HTML: {html_path.relative_to(PROJECT_ROOT)}")

        if args.html_only:
            continue

        pdf_path = OUTPUT_DIR / f"{chapter.md_path.stem}.pdf"
        render_pdf(html_path, pdf_path, use_pagedjs)
        print(f"  ✅ PDF : {pdf_path.relative_to(PROJECT_ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
