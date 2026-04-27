# pub-html-build 스킬 추출 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `projects/사내AI비서_v2/book/` 안의 HTML→PDF 파이프라인을 `.claude/skills/pub-html-build/` 스킬로 추출해, 모든 책 프로젝트가 공용 컴포넌트·디자인 토큰·빌드 파이프라인을 재사용하도록 만든다.

**Architecture:** CSS 커스텀 프로퍼티(`:root { --color-accent: ... }`)로 디자인 토큰 중앙화 → 스킬이 `templates/`, `styles/`, `build_pdf_html.py`를 소유 → 프로젝트는 `book/tokens.css`(브랜드 오버라이드)와 `chapters/*.md`만 가짐. `build_pdf_html.py`는 `--project-root` 인자로 프로젝트 경로를 받아 어디서든 동작.

**Tech Stack:** Python 3.12, markdown-it-py, mdit-py-plugins, Jinja2, Playwright/Chromium, Paged.js, Bash (init script).

---

## File Structure

**스킬(공용 자산 소유자):**
```
.claude/skills/pub-html-build/
├── SKILL.md                           # 스킬 문서 + 사용법 (신규)
├── build_pdf_html.py                  # 파이프라인. 프로젝트 경로를 인자로 받음 (이동)
├── templates/
│   ├── chapter-template.html          # (이동)
│   └── book-template.html             # (이동)
├── styles/
│   ├── tokens.css                     # ★ 디자인 토큰 (CSS 변수) (신규)
│   ├── base.css                       # 타이포그래피·페이지·기본 레이아웃 (신규. book.css에서 분리)
│   ├── components.css                 # :::goal, :::tip, :::remember 등 커스텀 블록 (신규)
│   ├── diagrams.css                   # lcel-pipeline, librarian-flow, concept-card 등 시각화 (신규)
│   ├── print.css                      # @page 규칙 (이동)
│   └── fonts.css                      # (이동)
└── scripts/
    └── init_book.sh                   # 새 책에 tokens.css 오버라이드 심기 (신규)
```

**프로젝트(콘텐츠만 소유):**
```
projects/사내AI비서_v2/
├── chapters/                          # 그대로
├── assets/                            # 그대로
└── book/
    ├── tokens.css                     # 프로젝트별 브랜드 오버라이드 (선택, 신규)
    ├── front/                         # 그대로
    ├── back/                          # 그대로
    ├── build/                         # 그대로 (빌드 산출물)
    └── output/                        # 그대로 (PDF 최종)
```

기존 `projects/사내AI비서_v2/book/build_pdf_html.py`, `book/templates/`, `book/styles/book.css`는 **삭제**. 스킬이 대신함.

**CLAUDE.md 명령 매핑 업데이트:**
```
인쇄소 → 스킬 pub-html-build build --project-root projects/사내AI비서_v2
```

---

## Phase 1: CSS 토큰화 (in-place)

현재 `book/styles/book.css`에 ~400개 하드코딩된 hex 색상이 있다. 먼저 **프로젝트 내에서** 토큰으로 리팩토링해서 현재 빌드가 그대로 동작하는지 검증한 뒤, Phase 2에서 스킬로 이동한다.

### Task 1: tokens.css 파일 생성 및 책 템플릿에 링크

**Files:**
- Create: `projects/사내AI비서_v2/book/styles/tokens.css`
- Modify: `projects/사내AI비서_v2/book/templates/chapter-template.html`
- Verify: `projects/사내AI비서_v2/book/build/01-환각과-RAG의-첫-만남.html` 렌더 결과

- [ ] **Step 1: tokens.css 작성 — 현재 팔레트·여백·반지름·폰트 크기 추출**

```css
/* projects/사내AI비서_v2/book/styles/tokens.css */
:root {
  /* ===== 색상: 기본 ===== */
  --color-text: #1e293b;          /* 본문 */
  --color-text-muted: #64748b;    /* 보조 텍스트 */
  --color-text-faint: #94a3b8;    /* 캡션·힌트 */
  --color-bg: #ffffff;
  --color-surface: #fafbfc;       /* 카드 배경 */
  --color-surface-alt: #f1f5f9;   /* 라벨 배경 */

  /* ===== 색상: 테두리 ===== */
  --color-border: #e2e8f0;        /* 기본 테두리 */
  --color-border-strong: #cbd5e0; /* 강조 테두리 */
  --color-border-dashed: #edf0f5; /* 점선·구분선 */

  /* ===== 색상: 액센트 (브랜드) ===== */
  --color-accent: #4f46e5;        /* 인디고 메인 */
  --color-accent-bg: #eef2ff;     /* 액센트 배경 */
  --color-accent-border: #c7d2fe; /* 액센트 테두리 */
  --color-accent-text: #3730a3;   /* 액센트 위 텍스트 */

  /* ===== 색상: 시맨틱 ===== */
  --color-success: #059669;
  --color-success-bg: #d1fae5;
  --color-warning: #b45309;
  --color-warning-bg: #fef08a;
  --color-danger: #dc2626;
  --color-danger-bg: #fee2e2;

  /* ===== 여백 ===== */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 12px;
  --space-lg: 16px;
  --space-xl: 20px;
  --space-2xl: 24px;

  /* ===== 반지름 ===== */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 10px;

  /* ===== 폰트 크기 ===== */
  --fs-tiny: 10px;
  --fs-xs: 11px;
  --fs-sm: 12px;
  --fs-md: 13px;
  --fs-base: 14px;
  --fs-lg: 15px;
  --fs-xl: 17px;

  /* ===== 폰트 패밀리 ===== */
  --font-body: "Pretendard", -apple-system, sans-serif;
  --font-mono: "JetBrains Mono", Consolas, monospace;
}
```

- [ ] **Step 2: chapter-template.html에 tokens.css를 book.css보다 먼저 링크**

```html
<link rel="stylesheet" href="{{ fonts_css }}">
<link rel="stylesheet" href="{{ tokens_css }}">
<link rel="stylesheet" href="{{ book_css }}">
<link rel="stylesheet" href="{{ print_css }}" media="print">
```

- [ ] **Step 3: build_pdf_html.py에 tokens_css 전달 추가**

`render_html_file` 함수에서:
```python
html = tpl.render(
    chapter={"title": chapter.title, "html": chapter.html},
    fonts_css="./styles/fonts.css",
    tokens_css="./styles/tokens.css",
    book_css="./styles/book.css",
    print_css="./styles/print.css",
    pagedjs=pagedjs,
)
```

- [ ] **Step 4: 빌드 + 결과 확인**

```bash
cd "projects/사내AI비서_v2"
.pdf_venv/bin/python3 book/build_pdf_html.py --chapter 1 --html-only
grep tokens.css book/build/01-*.html
```

Expected: `<link rel="stylesheet" href="./styles/tokens.css">` 출력. HTML 렌더가 깨지지 않음.

- [ ] **Step 5: 커밋**

```bash
git add projects/사내AI비서_v2/book/styles/tokens.css projects/사내AI비서_v2/book/templates/chapter-template.html projects/사내AI비서_v2/book/build_pdf_html.py
git commit -m "feat(html-pipeline): tokens.css 도입 — 디자인 토큰 중앙화 시작"
```

---

### Task 2: book.css의 기본 색상 토큰으로 치환

**Files:**
- Modify: `projects/사내AI비서_v2/book/styles/book.css`

- [ ] **Step 1: 전역 검색으로 치환 대상 확인**

`grep -n "#1e293b\|#64748b\|#fafbfc\|#e2e8f0" book/styles/book.css | wc -l` → 약 50~100개 예상.

- [ ] **Step 2: 색상 치환 (Edit tool replace_all)**

`book.css`에서 다음 치환 수행 (정확히 이 순서, 긴 값부터):
- `#fafbfc` → `var(--color-surface)`
- `#e2e8f0` → `var(--color-border)`
- `#1e293b` → `var(--color-text)`
- `#64748b` → `var(--color-text-muted)`
- `#94a3b8` → `var(--color-text-faint)`
- `#f1f5f9` → `var(--color-surface-alt)`
- `#cbd5e0` → `var(--color-border-strong)`
- `#edf0f5` → `var(--color-border-dashed)`
- `#4f46e5` → `var(--color-accent)`
- `#eef2ff` → `var(--color-accent-bg)`
- `#c7d2fe` → `var(--color-accent-border)`
- `#3730a3` → `var(--color-accent-text)`
- `#059669` → `var(--color-success)`
- `#d1fae5` → `var(--color-success-bg)`
- `#dc2626` → `var(--color-danger)`
- `#fee2e2` → `var(--color-danger-bg)`

- [ ] **Step 3: 빌드 + 비교**

```bash
.pdf_venv/bin/python3 book/build_pdf_html.py --chapter 1 --html-only
open book/build/01-환각과-RAG의-첫-만남.html   # 시각 검증: 색상 동일해야 함
```

Expected: 치환 전과 동일한 모양. 색 변화 없음.

- [ ] **Step 4: 잔존 하드코딩 색상 확인**

```bash
grep -cE "#[0-9a-fA-F]{6}" book/styles/book.css
```

줄어든 것 확인 (초기 400 → ~100 이하). 남은 건 액센트 변형·그림자 등 token에 없는 특수 색이므로 다음 단계에서 개별 처리.

- [ ] **Step 5: 커밋**

```bash
git add projects/사내AI비서_v2/book/styles/book.css
git commit -m "refactor(css): 기본 색상 토큰으로 치환 (그레이 스케일 + 액센트 + 시맨틱)"
```

---

### Task 3: book.css의 잔존 특수 색상 토큰화

**Files:**
- Modify: `projects/사내AI비서_v2/book/styles/tokens.css`
- Modify: `projects/사내AI비서_v2/book/styles/book.css`

- [ ] **Step 1: 남은 색상 식별**

```bash
grep -oE "#[0-9a-fA-F]{6}" book/styles/book.css | sort | uniq -c | sort -rn
```

상위 20개 보고. 대표적으로: 코드 블록 배경 `#1e293b`(대/중)·`#0f172a`(진), 노란색 강조 `#fef08a`·`#713f12`, 자주색 `#5b21b6`·`#ede9fe` 등.

- [ ] **Step 2: tokens.css에 추가 변수 선언**

```css
/* tokens.css에 추가 */
:root {
  /* ===== 색상: 코드 블록 ===== */
  --color-code-bg: #1e293b;
  --color-code-bg-dark: #0f172a;
  --color-code-text: #e2e8f0;

  /* ===== 색상: 하이라이트 ===== */
  --color-highlight-bg: #fef08a;
  --color-highlight-text: #713f12;

  /* ===== 색상: 보라 (청크 3번, 부가 강조) ===== */
  --color-violet: #5b21b6;
  --color-violet-bg: #ede9fe;

  /* ===== 색상: 주황 (경고·디버그) ===== */
  --color-orange: #92400e;
  --color-orange-bg: #fef3c7;
  --color-orange-border: #fcd34d;

  /* ===== 그림자 ===== */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
  --shadow-md: 0 2px 6px rgba(0, 0, 0, 0.06);
}
```

- [ ] **Step 3: book.css에 치환 적용**

위 변수에 해당하는 hex를 `var(--...)`로 치환. (Edit tool replace_all 반복)

- [ ] **Step 4: 빌드 + 비교**

```bash
.pdf_venv/bin/python3 book/build_pdf_html.py --chapter 4 --html-only
```

Ch4에는 코드 블록·청크 시각화·임베딩 예시 등 다양한 색이 들어있어 검증에 적합.

- [ ] **Step 5: 잔존 hex 재확인**

```bash
grep -cE "#[0-9a-fA-F]{6}" book/styles/book.css
```

50 이하로 감소 확인. 나머지는 단발성 색(특정 블록 전용)이므로 그대로 둬도 무방.

- [ ] **Step 6: 커밋**

```bash
git add projects/사내AI비서_v2/book/styles/tokens.css projects/사내AI비서_v2/book/styles/book.css
git commit -m "refactor(css): 코드 블록·하이라이트·특수 색상 토큰화 완료"
```

---

### Task 4: book.css를 base/components/diagrams로 분리

**Files:**
- Create: `projects/사내AI비서_v2/book/styles/base.css`
- Create: `projects/사내AI비서_v2/book/styles/components.css`
- Create: `projects/사내AI비서_v2/book/styles/diagrams.css`
- Delete: `projects/사내AI비서_v2/book/styles/book.css` (내용을 3파일로 분산)
- Modify: `projects/사내AI비서_v2/book/templates/chapter-template.html`
- Modify: `projects/사내AI비서_v2/book/build_pdf_html.py`

- [ ] **Step 1: book.css의 주석 섹션 파악**

```bash
grep -nE "^\s*/\*" book/styles/book.css | head -30
```

기존 구조: typography → 카드·박스 → 코드블록 → 다이어그램 → 특수 컴포넌트.

- [ ] **Step 2: base.css — 타이포그래피·페이지·기본 요소**

포함 대상: body/h1~h6/p/table/blockquote/pre/code 기본 스타일, `.container`, `.chapter-image` 등.

Write로 `base.css` 생성. `book.css`의 해당 부분을 복사.

- [ ] **Step 3: components.css — 커스텀 블록**

포함 대상: `.goal-box`, `.prep-section-md`, `.tip`, `.prep-note`, `.term-box`, `.remember`, `.result`, `.dialogue`, `.speaker`, `.thought`, `.code-block`, `.cb-title`, `.badge` 등.

- [ ] **Step 4: diagrams.css — 시각화 컴포넌트**

포함 대상: `.annotated-compare`(ac-*), `.rag-pipeline-box`(rag-*, s-*), `.journey-forward`(jf-*), `.chunk-with-meta`(cwm-*), `.embed-example-row`(eer-*), `.exec-flow`(ef-*), `.overlap-text-demo`(otd-*), `.arch-fullmap`(afm-*, am-*), `.dual-image`, `.librarian-flow`(lf-*), `.lcel-pipeline`(lp-*), `.concept-card`(cc-*), `.search-results`(sr-*), `.reindex-compare`(rc-*).

- [ ] **Step 5: book.css 삭제 + 템플릿 업데이트**

```html
<!-- chapter-template.html -->
<link rel="stylesheet" href="{{ fonts_css }}">
<link rel="stylesheet" href="{{ tokens_css }}">
<link rel="stylesheet" href="{{ base_css }}">
<link rel="stylesheet" href="{{ components_css }}">
<link rel="stylesheet" href="{{ diagrams_css }}">
<link rel="stylesheet" href="{{ print_css }}" media="print">
```

`build_pdf_html.py`의 `render_html_file`도 3개 CSS 전달하도록 수정 (기존 `book_css` 제거).

- [ ] **Step 6: 빌드 전체 챕터 검증**

```bash
for n in 1 2 3 4 5; do
  .pdf_venv/bin/python3 book/build_pdf_html.py --chapter $n --html-only
done
```

모든 챕터가 오류 없이 빌드되고, 시각적으로 이전과 동일해야 함.

- [ ] **Step 7: 커밋**

```bash
git rm projects/사내AI비서_v2/book/styles/book.css
git add projects/사내AI비서_v2/book/styles/base.css projects/사내AI비서_v2/book/styles/components.css projects/사내AI비서_v2/book/styles/diagrams.css
git add projects/사내AI비서_v2/book/templates/chapter-template.html projects/사내AI비서_v2/book/build_pdf_html.py
git commit -m "refactor(css): book.css를 base/components/diagrams 3개 파일로 분리"
```

---

## Phase 2: 스킬 추출

### Task 5: 스킬 디렉토리 골격 생성

**Files:**
- Create: `.claude/skills/pub-html-build/SKILL.md`
- Create: `.claude/skills/pub-html-build/styles/` (빈 디렉토리)
- Create: `.claude/skills/pub-html-build/templates/` (빈 디렉토리)
- Create: `.claude/skills/pub-html-build/scripts/` (빈 디렉토리)

- [ ] **Step 1: SKILL.md 작성**

```markdown
---
name: pub-html-build
description: Use when building a book project from Markdown chapters to HTML/PDF. Owns templates, design tokens, and the Playwright-based pipeline. Invoke with project path.
---

# pub-html-build — HTML→PDF 책 빌드 스킬

## 개요

마크다운 챕터를 HTML로 렌더하고 Paged.js + Playwright로 PDF를 출력한다.
디자인 토큰(`styles/tokens.css`)과 커스텀 블록 시스템(`:::goal`, `:::tip` 등)을 공용으로 제공한다.

## 사용법

### 빌드

```bash
python .claude/skills/pub-html-build/build_pdf_html.py \
  --project-root projects/사내AI비서_v2 \
  --chapter 1
```

옵션:
- `--project-root PATH` (필수): 책 프로젝트 루트
- `--chapter N` (선택): 특정 챕터만 빌드
- `--html-only`: HTML 중간 산출물만 생성 (PDF 생략)
- `--no-pagedjs`: Chromium 기본 인쇄 (Paged.js 비활성화)

### 새 책 시작

```bash
bash .claude/skills/pub-html-build/scripts/init_book.sh projects/new-book
```

이 명령이 프로젝트에 `book/tokens.css`(브랜드 오버라이드 템플릿)를 심는다.

## 디자인 토큰

브랜드 컬러·여백·반지름은 `styles/tokens.css`에서 CSS 변수로 관리.
프로젝트가 `{project}/book/tokens.css`를 두면 스킬 토큰을 덮어쓴다.

## 커스텀 블록

- `:::goal` / `:::prep` / `:::tip` / `:::note`
- `:::remember` / `:::term-box`
- `:::compare` / `:::rag-pipeline` / `:::journey`
- `:::result-fail` / `:::result-ok`

## 의존성

```
playwright==1.48
markdown-it-py==3.0
mdit-py-plugins>=0.4
jinja2==3.1
```
```

- [ ] **Step 2: 디렉토리 생성**

```bash
mkdir -p .claude/skills/pub-html-build/{styles,templates,scripts}
```

- [ ] **Step 3: 커밋**

```bash
git add .claude/skills/pub-html-build/SKILL.md
git commit -m "feat(skill): pub-html-build 스킬 골격 생성"
```

---

### Task 6: 스킬로 템플릿·스타일 이동

**Files:**
- Move: `projects/사내AI비서_v2/book/templates/*` → `.claude/skills/pub-html-build/templates/`
- Move: `projects/사내AI비서_v2/book/styles/{tokens,base,components,diagrams,print,fonts}.css` → `.claude/skills/pub-html-build/styles/`

- [ ] **Step 1: 파일 이동 (git mv)**

```bash
git mv projects/사내AI비서_v2/book/templates/chapter-template.html .claude/skills/pub-html-build/templates/
git mv projects/사내AI비서_v2/book/templates/book-template.html .claude/skills/pub-html-build/templates/
rmdir projects/사내AI비서_v2/book/templates

git mv projects/사내AI비서_v2/book/styles/tokens.css .claude/skills/pub-html-build/styles/
git mv projects/사내AI비서_v2/book/styles/base.css .claude/skills/pub-html-build/styles/
git mv projects/사내AI비서_v2/book/styles/components.css .claude/skills/pub-html-build/styles/
git mv projects/사내AI비서_v2/book/styles/diagrams.css .claude/skills/pub-html-build/styles/
git mv projects/사내AI비서_v2/book/styles/print.css .claude/skills/pub-html-build/styles/
git mv projects/사내AI비서_v2/book/styles/fonts.css .claude/skills/pub-html-build/styles/
rmdir projects/사내AI비서_v2/book/styles
```

- [ ] **Step 2: 커밋 (빌드는 다음 태스크에서 스크립트 수정 후)**

```bash
git commit -m "refactor(skill): templates/styles 파일을 스킬로 이동"
```

---

### Task 7: build_pdf_html.py를 스킬로 이동 + 프로젝트 루트 파라미터화

**Files:**
- Move: `projects/사내AI비서_v2/book/build_pdf_html.py` → `.claude/skills/pub-html-build/build_pdf_html.py`
- Modify: `.claude/skills/pub-html-build/build_pdf_html.py` (경로 상수들을 인자 기반으로)

- [ ] **Step 1: 파일 이동**

```bash
git mv projects/사내AI비서_v2/book/build_pdf_html.py .claude/skills/pub-html-build/build_pdf_html.py
```

- [ ] **Step 2: 경로 상수 섹션 교체**

`build_pdf_html.py` 상단의 경로 블록을 다음과 같이 변경:

```python
# ----- 경로 기준 ----------------------------------------------------------
SKILL_DIR = Path(__file__).resolve().parent
SKILL_STYLES = SKILL_DIR / "styles"
SKILL_TEMPLATES = SKILL_DIR / "templates"

# 프로젝트 경로는 CLI 인자에서 설정 (main에서 채움)
PROJECT_ROOT: Path = None  # type: ignore
CHAPTERS_DIR: Path = None  # type: ignore
ASSETS_DIR: Path = None    # type: ignore
BUILD_DIR: Path = None     # type: ignore
OUTPUT_DIR: Path = None    # type: ignore


def configure_paths(project_root: Path) -> None:
    """CLI에서 project_root가 확정된 뒤 전역 경로 변수를 세팅한다."""
    global PROJECT_ROOT, CHAPTERS_DIR, ASSETS_DIR, BUILD_DIR, OUTPUT_DIR
    PROJECT_ROOT = project_root.resolve()
    CHAPTERS_DIR = PROJECT_ROOT / "chapters"
    ASSETS_DIR = PROJECT_ROOT / "assets"
    BUILD_DIR = PROJECT_ROOT / "book" / "build"
    OUTPUT_DIR = PROJECT_ROOT / "book" / "output"
```

- [ ] **Step 3: 심볼릭 링크 타겟 수정 (ensure_build_symlinks)**

스킬 styles 링크를 추가:

```python
def ensure_build_symlinks() -> None:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    targets = {
        "styles": SKILL_STYLES,      # ← 스킬의 styles 참조
        "assets": ASSETS_DIR,
    }
    # 프로젝트가 tokens.css 오버라이드를 가지고 있으면 우선 적용
    project_tokens = PROJECT_ROOT / "book" / "tokens.css"
    if project_tokens.exists():
        targets["tokens-override.css"] = project_tokens
    # ... 이하 기존 로직
```

- [ ] **Step 4: 템플릿 로더 경로 수정**

```python
# render_html_file 안에서
env = Environment(
    loader=FileSystemLoader(SKILL_TEMPLATES),   # ← 스킬 templates
    ...
)
```

- [ ] **Step 5: argparse에 `--project-root` 추가**

```python
parser.add_argument(
    "--project-root",
    type=Path,
    required=True,
    help="책 프로젝트 루트 경로 (예: projects/사내AI비서_v2)",
)
# main() 안에서
args = parser.parse_args()
configure_paths(args.project_root)
```

- [ ] **Step 6: 템플릿에 tokens-override 주입 (선택)**

`chapter-template.html`에 프로젝트 오버라이드 링크 추가:

```html
<link rel="stylesheet" href="./styles/tokens.css">
{% if tokens_override %}
<link rel="stylesheet" href="./tokens-override.css">
{% endif %}
<link rel="stylesheet" href="./styles/base.css">
...
```

`render_html_file`에서 `tokens_override = (PROJECT_ROOT / "book" / "tokens.css").exists()` 를 전달.

- [ ] **Step 7: 빌드 테스트**

```bash
python .claude/skills/pub-html-build/build_pdf_html.py \
  --project-root "projects/사내AI비서_v2" \
  --chapter 1 \
  --html-only
```

Expected: `projects/사내AI비서_v2/book/build/01-*.html` 정상 생성.

- [ ] **Step 8: 커밋**

```bash
git add .claude/skills/pub-html-build/build_pdf_html.py .claude/skills/pub-html-build/templates/chapter-template.html
git commit -m "feat(skill): build_pdf_html.py를 프로젝트 루트 파라미터화"
```

---

### Task 8: Phase 2 회귀 테스트 — 전체 챕터 + PDF 빌드

**Files:**
- (파일 변경 없음. 명령 실행만)

- [ ] **Step 1: 전체 챕터 HTML 빌드**

```bash
for n in 1 2 3 4 5; do
  python .claude/skills/pub-html-build/build_pdf_html.py \
    --project-root "projects/사내AI비서_v2" --chapter $n --html-only
done
```

모두 에러 없이 HTML 생성되는지 확인.

- [ ] **Step 2: 챕터 1 PDF 빌드 + 시각 검증**

```bash
python .claude/skills/pub-html-build/build_pdf_html.py \
  --project-root "projects/사내AI비서_v2" --chapter 1
open projects/사내AI비서_v2/book/output/01-*.pdf
```

PDF가 이전 버전과 레이아웃·색상·타이포그래피 동일해야 함. 차이 발견 시 원인 추적.

- [ ] **Step 3: 프로젝트 book/ 폴더 정리 확인**

```bash
ls projects/사내AI비서_v2/book/
```

Expected 출력: `build/ front/ back/ assets/ output/ (선택) tokens.css`.
`templates/`, `styles/`, `build_pdf_html.py`, `book.css`가 **없음**을 확인.

- [ ] **Step 4: 커밋은 불필요 (검증만)**

---

## Phase 3: 편의 기능

### Task 9: init_book.sh — 새 책 시작 스크립트

**Files:**
- Create: `.claude/skills/pub-html-build/scripts/init_book.sh`

- [ ] **Step 1: 스크립트 작성**

```bash
#!/usr/bin/env bash
# .claude/skills/pub-html-build/scripts/init_book.sh
# 사용: bash init_book.sh <project-root>
# 예:   bash init_book.sh projects/new-book

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "사용법: $0 <project-root>"
  echo "예:    $0 projects/new-book"
  exit 1
fi

PROJECT_ROOT="$1"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# 디렉토리 구조 생성
mkdir -p "$PROJECT_ROOT/chapters"
mkdir -p "$PROJECT_ROOT/assets"
mkdir -p "$PROJECT_ROOT/book/build"
mkdir -p "$PROJECT_ROOT/book/output"
mkdir -p "$PROJECT_ROOT/book/front"
mkdir -p "$PROJECT_ROOT/book/back"

# tokens.css 오버라이드 템플릿 생성 (주석만 있는 빈 파일)
cat > "$PROJECT_ROOT/book/tokens.css" <<'EOF'
/* 프로젝트별 디자인 토큰 오버라이드
 *
 * 스킬 기본 토큰(pub-html-build/styles/tokens.css)을 덮어쓸 변수만 여기에 선언합니다.
 * 전체 토큰 목록은 스킬 tokens.css를 참조하세요.
 *
 * 예: 브랜드 액센트를 파란색으로 바꾸기
 *   :root {
 *     --color-accent: #2563eb;
 *     --color-accent-bg: #dbeafe;
 *     --color-accent-border: #93c5fd;
 *     --color-accent-text: #1e40af;
 *   }
 */
EOF

echo "✅ 프로젝트 초기화 완료: $PROJECT_ROOT"
echo ""
echo "다음 단계:"
echo "  1. chapters/01-*.md 작성"
echo "  2. 필요시 book/tokens.css에서 브랜드 오버라이드"
echo "  3. 빌드:"
echo "     python $SKILL_DIR/build_pdf_html.py --project-root $PROJECT_ROOT --chapter 1"
```

- [ ] **Step 2: 실행 권한**

```bash
chmod +x .claude/skills/pub-html-build/scripts/init_book.sh
```

- [ ] **Step 3: 자체 테스트 (임시 프로젝트 생성 후 삭제)**

```bash
bash .claude/skills/pub-html-build/scripts/init_book.sh /tmp/test-book
ls /tmp/test-book
cat /tmp/test-book/book/tokens.css
rm -rf /tmp/test-book
```

Expected: 디렉토리 + `book/tokens.css` 주석 파일 생성.

- [ ] **Step 4: 커밋**

```bash
git add .claude/skills/pub-html-build/scripts/init_book.sh
git commit -m "feat(skill): init_book.sh — 새 책 프로젝트 초기화 스크립트"
```

---

### Task 10: CLAUDE.md 명령 매핑 업데이트

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: 현재 명령 위치 확인**

```bash
grep -n "인쇄소\|build_pdf" CLAUDE.md
```

- [ ] **Step 2: 명령어 표 업데이트**

사내AI비서_v2 프로젝트용 HTML 파이프라인 명령을 추가:

```markdown
| 인쇄소 (HTML) | 출판 | `book/output/*.pdf` | 아래 "HTML 파이프라인" 참조 |
```

섹션 추가:
```markdown
### HTML 파이프라인 실행

```bash
python .claude/skills/pub-html-build/build_pdf_html.py \
  --project-root projects/<책이름> \
  --chapter N
```

옵션: `--html-only`(PDF 생략), `--no-pagedjs`(빠른 빌드).
새 책 시작: `bash .claude/skills/pub-html-build/scripts/init_book.sh projects/<책이름>`.
```

- [ ] **Step 3: 커밋**

```bash
git add CLAUDE.md
git commit -m "docs: CLAUDE.md에 pub-html-build 스킬 사용법 추가"
```

---

### Task 11: 메모리 업데이트 — 새 스킬의 존재

**Files:**
- Create: `/Users/nomadlab/.claude/projects/-Users-nomadlab-Desktop-----workspace-coding-study--------v2/memory/project_pub_html_skill.md`
- Modify: `/Users/nomadlab/.claude/projects/-Users-nomadlab-Desktop-----workspace-coding-study--------v2/memory/MEMORY.md`

- [ ] **Step 1: 메모리 파일 작성**

```markdown
---
name: pub-html-build 스킬 도입
description: HTML→PDF 파이프라인을 스킬로 추출. templates/styles/build_pdf_html.py가 .claude/skills/pub-html-build/에 있음. 프로젝트는 chapters/ + 선택적 book/tokens.css만 보유.
type: project
---

사내AI비서_v2 책 빌드용으로 만든 HTML→PDF 파이프라인을 공용 스킬로 추출(2026-04-14 완료).

**Why:** 다음 책 프로젝트에서도 같은 컴포넌트(lcel-pipeline, librarian-flow, concept-card 등)와 커스텀 블록(:::goal, :::tip 등)을 재사용해야 한다. 하드코딩된 400개 hex 색상을 CSS 변수로 중앙화해 브랜드 교체가 가능해짐.

**How to apply:**
- 새 책 시작: `bash .claude/skills/pub-html-build/scripts/init_book.sh projects/새책`
- 브랜드 색 변경: `projects/새책/book/tokens.css`에서 `--color-accent` 등 오버라이드
- 빌드: `python .claude/skills/pub-html-build/build_pdf_html.py --project-root projects/새책 --chapter N`
- 컴포넌트 추가/수정은 스킬의 `styles/diagrams.css` 또는 `styles/components.css`에서
```

- [ ] **Step 2: MEMORY.md에 한 줄 추가**

```markdown
- [project_pub_html_skill.md](project_pub_html_skill.md) — HTML→PDF 파이프라인 스킬화. 디자인 토큰 + 커스텀 블록 시스템 공용화 (2026-04-14)
```

- [ ] **Step 3: 커밋 (메모리는 git 관리 밖이면 skip)**

---

## Self-Review

### 1. Spec coverage

사용자 요구:
- ✅ HTML→PDF 파이프라인 공통화 → Phase 2 (Task 5~8)
- ✅ 글의 상세 디테일(컴포넌트) 공통화 → Phase 1 (Task 4, diagrams.css/components.css 분리) + Task 6 스킬 이동
- ✅ 디자인 토큰 적용 → Phase 1 (Task 1~3)
- ✅ 다른 유저가 새 책 써도 적용되는 구조 → Task 9 (init_book.sh), Task 10 (CLAUDE.md)

### 2. Placeholder scan

- 모든 태스크에 명시적 파일 경로, 실제 코드·명령 포함
- "적절한 에러 처리" 같은 모호 문구 없음

### 3. Type consistency

- `--project-root` 인자 이름 일관 (Task 7·8·9·10)
- `configure_paths()` 함수명 Task 7에서만 등장, 다른 곳에서 참조 없음 (일관성 OK)
- 토큰 이름(`--color-accent`, `--color-surface` 등) Task 1·2·3·9·11 모두 동일
- 파일 이름(`tokens.css`, `base.css`, `components.css`, `diagrams.css`) 전 태스크 일관

### 4. 위험 요소

- **Task 2·3 대량 치환**: `replace_all`로 `#1e293b` 같은 흔한 값을 치환할 때 코드 블록 배경색 등 의도하지 않은 부분까지 바뀔 수 있음. → Task 3에서 `grep -oE | sort | uniq -c`로 잔존 hex를 확인하는 단계 삽입. Task 4 분리 후 시각 비교 필수.
- **Task 4 파일 분리**: 규칙 순서가 바뀌면 CSS cascade로 스타일이 깨질 수 있음. → 템플릿에 base → components → diagrams 순으로 로드 (현재 book.css의 원래 순서 유지).
- **심볼릭 링크**: macOS symlink 지원 이슈 시 `BUILD_DIR`로 복사하는 대안 필요 (현재 스크립트는 symlink 실패 시 경고 출력 후 계속).

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-04-14-pub-html-build-skill.md`. Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
