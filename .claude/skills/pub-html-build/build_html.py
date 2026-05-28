#!/usr/bin/env python3
"""
build_html.py — 마크다운 챕터를 HTML 프리뷰로 빌드.

흐름:
  chapters/NN-*.md
    → (커스텀 블록 + 코드블록 타이틀 전처리)
    → markdown-it-py
    → Jinja2 템플릿 병합
    → <프로젝트루트>/.build/NN-*.html

PDF 변환이 필요하면 별도 스킬 `pub-html-to-pdf`를 사용.

의존성:
  pip install markdown-it-py mdit-py-plugins jinja2 pygments
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import webbrowser
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

# ----- 경로 기준 ----------------------------------------------------------
# 스킬 내부 경로 (templates/styles는 스킬이 소유)
SKILL_DIR = Path(__file__).resolve().parent
SKILL_TEMPLATES = SKILL_DIR / "templates"
SKILL_STYLES = SKILL_DIR / "styles"

# 프로젝트 경로는 CLI --project-root로 주입. configure_paths()에서 설정.
PROJECT_ROOT: Path = None  # type: ignore[assignment]
CHAPTERS_DIR: Path = None  # type: ignore[assignment]
ASSETS_DIR: Path = None    # type: ignore[assignment]
BUILD_DIR: Path = None     # type: ignore[assignment]
PROJECT_TOKENS_OVERRIDE: Path = None  # type: ignore[assignment]


def configure_paths(project_root: Path) -> None:
    """CLI에서 --project-root 값이 확정된 뒤 전역 경로 변수를 설정."""
    global PROJECT_ROOT, CHAPTERS_DIR, ASSETS_DIR, BUILD_DIR, PROJECT_TOKENS_OVERRIDE
    PROJECT_ROOT = project_root.resolve()
    CHAPTERS_DIR = PROJECT_ROOT / "chapters"
    ASSETS_DIR = PROJECT_ROOT / "assets"
    BUILD_DIR = PROJECT_ROOT / ".build"
    # tokens.css 오버라이드 파일도 .build/ 안에서 관리 (저작·산출 한 폴더)
    override = BUILD_DIR / "tokens.css"
    PROJECT_TOKENS_OVERRIDE = override if override.exists() else None


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
    "memo": "memo-box",
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

    # 내면독백: `*text*` 또는 `_text_` 단독 문단 (이탤릭 표기 둘 다 허용 —
    # 일부 마크다운 포매터가 `*..*`를 `_.._`로 normalize하기 때문).
    # 단, 바로 앞 라인이 이미지 `![](..)`거나 본문이 `그림 N..` 패턴이면 캡션이므로 스킵.
    lines = md.split("\n")
    out: list[str] = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        marker = stripped[:1] if stripped else ""
        is_thought = (
            marker in ("*", "_")
            and stripped.endswith(marker)
            and not stripped.startswith(marker * 2)
            and not stripped.endswith(marker * 2)
            and len(stripped) >= 4
            and stripped.count(marker) == 2
        )
        if is_thought:
            prev = lines[i - 1].strip() if i > 0 else ""
            inner = stripped[1:-1].strip()
            if prev.startswith("![") or re.match(r"^그림 \d", inner):
                out.append(line)
                continue
            out.append(f'<p class="thought">{inner}</p>')
        else:
            out.append(line)
    return "\n".join(out)


# ========== 이미지 경로 보정 ================================================
IMG_RE = re.compile(r'<img\s+([^>]*?)src="([^"]+)"([^>]*)>', re.IGNORECASE)


def resolve_image_paths(html: str, md_file: Path) -> str:
    """
    마크다운의 이미지 경로(예: ../assets/CH01/...)를 빌드 HTML이 놓일
    .build/ 기준 상대경로(../assets/CH01/...)로 재작성.
    에셋 심링크 없이도 브라우저가 원본 에셋 파일에 접근할 수 있다.
    """
    def sub(m: re.Match) -> str:
        before, src, after = m.group(1), m.group(2), m.group(3)
        if src.startswith(("http://", "https://", "data:", "file://", "/")):
            return m.group(0)
        # 마크다운 기준 상대경로를 절대경로로 해석
        resolved = (md_file.parent / src).resolve()
        if not resolved.exists():
            print(f"  ⚠️  이미지 없음: {src} → {resolved}", file=sys.stderr)
        # .build/NN.html 기준 상대경로 계산 — 심링크 불필요
        target_rel = os.path.relpath(resolved, start=BUILD_DIR)
        return f'<img {before}src="{target_rel}"{after}>'

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


# ========== 다이어그램 캡션 래핑 ===========================================
DIAGRAM_CAPTION_RE = re.compile(
    r'(</div>)\s*<p><em>(그림\s+\d+[-\d]*\..*?)</em></p>',
    re.DOTALL,
)


def wrap_diagram_captions(html: str) -> str:
    """
    SVG·터미널 다이어그램 컨테이너 직후의 마크다운 이탤릭 캡션을
    `<div class="caption">`로 변환. PNG 이미지(`wrap_chapter_images`)와
    같은 가운데 정렬·작은 회색 이탤릭 스타일을 적용한다.

    매칭 패턴: `</div>` + `<p><em>그림 N-N. ...</em></p>`. 그림 번호 접두로
    시작하는 이탤릭만 잡으므로 일반 본문 이탤릭은 영향 없음.
    `wrap_chapter_images`가 PNG 케이스를 먼저 흡수하므로 이 단계에서는
    svg-figure·terminal-log 등 raw HTML 컨테이너 뒤 캡션만 남는다.
    """
    return DIAGRAM_CAPTION_RE.sub(
        lambda m: f'{m.group(1)}\n<div class="caption">{m.group(2)}</div>',
        html,
    )


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


def find_front_files() -> list[Path]:
    """book/front/ 의 preface·prologue·github-source 등 front matter 파일 목록.
    챕터와 같은 템플릿·CSS로 렌더된다."""
    front_dir = PROJECT_ROOT / "book" / "front"
    if not front_dir.exists():
        return []
    return sorted(f for f in front_dir.glob("*.md") if not f.name.endswith(".bak"))


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
    html = wrap_diagram_captions(html)
    html = resolve_image_paths(html, md_path)

    # 4. 제목 추출
    m = re.search(r"^#\s+(.*)", raw, re.MULTILINE)
    title = (m.group(1) if m else md_path.stem).strip()

    # 5. 챕터 번호 — NN-*.md 형식이면 파싱, front/ 문서(preface·prologue 등)는 0 고정
    try:
        n = int(md_path.name[:2])
    except ValueError:
        n = 0

    return Chapter(number=n, title=title, md_path=md_path, html=html)


# ========== alias (레포 루트 심링크 이름) 결정 ==============================
_VERSION_SUFFIX_RE = re.compile(r"_v\d+$", re.IGNORECASE)


def _resolve_alias() -> str:
    """
    프로젝트의 레포 루트 심링크 이름을 결정한다.
    우선순위:
      1. progress.json["alias"] (비어 있지 않으면 사용)
      2. progress.json["project"]에서 _vNN 접미어 제거
      3. 폴더명에서 _vNN 접미어 제거
    """
    progress = PROJECT_ROOT / "progress.json"
    project_field: str | None = None
    if progress.exists():
        try:
            data = json.loads(progress.read_text(encoding="utf-8"))
            alias = (data.get("alias") or "").strip()
            if alias:
                return alias
            project_field = (data.get("project") or "").strip() or None
        except (json.JSONDecodeError, OSError) as exc:
            print(f"  ⚠️  progress.json 읽기 실패 ({exc}). 폴더명으로 alias 결정.",
                  file=sys.stderr)

    base = project_field or PROJECT_ROOT.name
    return _VERSION_SUFFIX_RE.sub("", base)


def _ensure_repo_root_symlink() -> None:
    """레포 루트에 `<alias> → projects/<프로젝트폴더>` 심링크 자동 생성."""
    # 레포 루트 = PROJECT_ROOT의 두 단 위 (projects/<name>/ → <repo>/)
    repo_root = PROJECT_ROOT.parent.parent
    # 안전장치: .claude 폴더가 있는 위치만 레포 루트로 간주
    if not (repo_root / ".claude").is_dir():
        return
    alias = _resolve_alias()
    if not alias:
        return
    link = repo_root / alias
    target_rel = os.path.relpath(PROJECT_ROOT, start=repo_root)
    if link.is_symlink():
        current = os.readlink(link)
        if current == target_rel:
            return
        try:
            resolved_current = (repo_root / current).resolve()
        except (OSError, RuntimeError):
            resolved_current = None
        if resolved_current == PROJECT_ROOT:
            # 절대경로 등으로 박혀 있던 링크 → 상대경로로 갱신
            link.unlink()
            link.symlink_to(target_rel)
            print(f"  🔗 레포 루트 심링크 갱신: {alias} → {target_rel}")
            return
        print(
            f"  ⚠️  레포 루트 심링크 충돌: '{alias}'가 이미 {current}을(를) 가리킵니다.\n"
            f"       progress.json의 'alias' 필드로 고유 이름을 지정하세요.",
            file=sys.stderr,
        )
        return
    if link.exists():
        print(
            f"  ⚠️  레포 루트에 동명의 파일·폴더 존재: {alias}. 심링크 생성 생략.",
            file=sys.stderr,
        )
        return
    try:
        link.symlink_to(target_rel)
        print(f"  🔗 레포 루트 심링크 생성: {alias} → {target_rel}")
    except OSError as exc:
        print(f"  ⚠️  심링크 생성 실패 ({alias}): {exc}", file=sys.stderr)


# ========== Jinja2 템플릿 병합 =============================================
def ensure_build_symlinks() -> None:
    """
    .build/에 styles(스킬 CSS)를 노출한다.
    1순위: 상대 심링크 (스킬 원본 수정이 자동 반영됨)
    fallback: Windows 권한 부재 등으로 심링크가 실패하면 디렉토리 복사로 대체한다.
             매 빌드마다 스킬 원본으로 덮어써서 stale 사본을 방지한다.
    """
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    targets = {
        "styles": SKILL_STYLES,
    }

    for name, src in targets.items():
        link = BUILD_DIR / name
        rel = os.path.relpath(src, start=link.parent)

        if link.is_symlink():
            try:
                if os.readlink(link) == rel:
                    continue
            except OSError:
                pass
            link.unlink()
        elif link.exists():
            if link.is_dir():
                shutil.rmtree(link)
            else:
                link.unlink()

        try:
            link.symlink_to(rel)
        except OSError as exc:
            try:
                shutil.copytree(src, link)
            except OSError as copy_exc:
                print(
                    f"  ⚠️  styles 동기화 실패 {name}: 심링크 {exc} / 복사 {copy_exc}",
                    file=sys.stderr,
                )

    # 레포 루트에 책 alias 심링크는 만들지 않는다.
    # 챕터 md의 이미지 경로는 resolve_image_paths()가 .build/ 기준 상대경로로 재작성하므로
    # 프로젝트 내부 ../assets/만 참조하면 충분. 레포 루트 alias는 어떤 빌드 단계도 사용 안 함.
    # 필요 시 _ensure_repo_root_symlink()를 호출해 수동 활성화 가능 (함수 정의는 보존).


def render_html_file(chapter: Chapter) -> Path:
    """
    HTML 프리뷰 파일 생성. 브라우저에서 한 장으로 흐르게 읽을 수 있도록
    Paged.js는 로드하지 않는다.
    """
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    env = Environment(
        loader=FileSystemLoader(SKILL_TEMPLATES),
        autoescape=select_autoescape(["html"]),
    )
    tpl = env.get_template("chapter-template.html")

    ensure_build_symlinks()
    out_html = BUILD_DIR / f"{chapter.md_path.stem}.html"

    # tokens.css 오버라이드 존재 여부 매 빌드마다 재확인 (저자가 지울 수도 있음)
    has_override = (BUILD_DIR / "tokens.css").exists()

    html = tpl.render(
        chapter={"title": chapter.title, "html": chapter.html},
        fonts_css="./styles/fonts.css",
        tokens_css="./styles/tokens.css",
        base_css="./styles/base.css",
        components_css="./styles/components.css",
        diagrams_css="./styles/diagrams.css",
        print_css="./styles/print.css",
        pagedjs=False,
        tokens_override=has_override,
    )
    out_html.write_text(html, encoding="utf-8")
    return out_html


# ========== 브라우저 열기 (크로스 플랫폼) ===================================
def _file_url(path: Path) -> str:
    """Path → file:// URL (한글 경로도 안전하게 인코딩)."""
    return f"file://{quote(str(path.resolve()))}"


def open_in_browser(path: Path) -> bool:
    """
    OS 기본 브라우저에서 file:// URL 열기.
    webbrowser 모듈이 내부적으로 OS별 분기(macOS open / Windows start / Linux xdg-open).
    """
    if not path.exists():
        print(f"  ⚠️  열 파일이 없음: {path}", file=sys.stderr)
        return False
    url = _file_url(path)
    try:
        webbrowser.open(url)
        print(f"  🌐 브라우저에서 열림")
        return True
    except Exception as exc:
        print(f"  ⚠️  브라우저 열기 실패: {exc}", file=sys.stderr)
        print(f"      수동으로 열기: {url}")
        return False


def resolve_preview_target(name: str) -> Path:
    """--preview NAME → .build/preview/NAME.html 경로. 확장자·슬래시 허용."""
    if not name.endswith(".html"):
        name = f"{name}.html"
    return BUILD_DIR / "preview" / name


# ========== 메인 ============================================================
def main() -> int:
    parser = argparse.ArgumentParser(description="마크다운 챕터 → HTML 프리뷰 빌더")
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
        help="특정 챕터 번호만 빌드 (예: --chapter 1)",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="빌드 후 OS 기본 브라우저에서 첫 챕터를 자동으로 연다 (file:// URL)",
    )
    parser.add_argument(
        "--preview",
        type=str,
        default=None,
        metavar="NAME",
        help=(
            "빌드 없이 .build/preview/<NAME>.html 을 브라우저로 연다. "
            "예: --preview tokens-swatch (확장자 생략 가능)"
        ),
    )
    parser.add_argument(
        "--front",
        action="store_true",
        help="book/front/*.md (preface·prologue·github-source 등)만 빌드",
    )
    args = parser.parse_args()

    configure_paths(args.project_root)

    # --preview: 빌드 건너뛰고 프리뷰 파일만 열기
    if args.preview:
        target = resolve_preview_target(args.preview)
        print(f"👁  프리뷰: {target.relative_to(PROJECT_ROOT) if target.is_relative_to(PROJECT_ROOT) else target}")
        return 0 if open_in_browser(target) else 1

    md = make_md()

    if args.front:
        files = find_front_files()
        if not files:
            print("❌ book/front/*.md 가 없습니다.", file=sys.stderr)
            return 1
    else:
        files = find_chapter_files(args.chapter)
        if not files:
            print("❌ 빌드할 챕터 파일을 찾지 못했습니다.", file=sys.stderr)
            return 1

    first_html: Path | None = None
    for md_path in files:
        print(f"📖 {md_path.name}")
        chapter = render_chapter(md_path, md)

        html_path = render_html_file(chapter)
        print(f"  ✅ HTML: {html_path.relative_to(PROJECT_ROOT)}")
        print(f"  🔗 열기: {_file_url(html_path)}")
        if first_html is None:
            first_html = html_path

    if args.open and first_html is not None:
        print()
        open_in_browser(first_html)

    return 0


if __name__ == "__main__":
    sys.exit(main())
