---
name: pub-html-build
description: Use when building a book project from Markdown chapters to HTML/PDF. Owns templates, design tokens, custom markdown blocks, and the Playwright-based PDF pipeline. Invoke with --project-root to point at the book source.
---

# pub-html-build — HTML→PDF 책 빌드 스킬

## 개요

마크다운 챕터를 HTML로 렌더하고 Paged.js + Playwright로 PDF를 출력한다.
**디자인 토큰** (`styles/tokens.css`)과 **커스텀 블록 시스템** (`:::goal`, `:::tip` 등)을 책 전체 프로젝트가 공유한다. 프로젝트 측은 콘텐츠(`chapters/*.md`)와 자산(`assets/`)만 소유한다.

## 디렉토리 구조

```
pub-html-build/
├── SKILL.md
├── build_pdf_html.py           # 파이프라인 진입점 (Task 7에서 이동)
├── templates/
│   └── chapter-template.html   # Jinja2 챕터 템플릿
├── styles/
│   ├── tokens.css              # 디자인 토큰 (CSS 변수)
│   ├── fonts.css               # 폰트 임베드
│   ├── base.css                # 타이포그래피·기본 HTML·코드블록
│   ├── components.css          # 커스텀 블록 (:::goal, :::tip 등)
│   ├── diagrams.css            # 시각화 컴포넌트 (lcel-pipeline 등)
│   └── print.css               # @page 규칙
└── scripts/
    └── init_book.sh            # 새 책 프로젝트 초기화 스크립트
```

## 사용법

### 빌드

```bash
python .claude/skills/pub-html-build/build_pdf_html.py \
  --project-root projects/<책이름> \
  --chapter 1
```

옵션:
- `--project-root PATH` (필수): 책 프로젝트 루트 디렉토리
- `--chapter N` (선택): 특정 챕터만 빌드
- `--html-only`: HTML 중간 산출물만 생성 (PDF 생략)
- `--no-pagedjs`: Chromium 기본 인쇄 (Paged.js 비활성화)

### 새 책 시작

```bash
bash .claude/skills/pub-html-build/scripts/init_book.sh projects/new-book
```

프로젝트에 `book/tokens.css`(브랜드 오버라이드 템플릿)를 심는다.

## 디자인 토큰

브랜드 컬러·여백·반지름은 `styles/tokens.css`에서 CSS 변수로 관리. 프로젝트가 `{project}/book/tokens.css`를 두면 스킬 토큰을 선택적으로 덮어쓸 수 있다.

주요 토큰 그룹:
- `--color-text`/`--color-text-muted`/`--color-text-subtle`/`--color-text-heading`
- `--color-accent`/`-bg`/`-border`/`-text` (브랜드 인디고)
- `--color-accent-warm`/`-text` (오렌지 보조 액센트)
- `--color-info`/`-bg`/`-text` (블루 계열)
- `--color-success`/`--color-warning`/`--color-danger` (시맨틱 3색 세트)
- `--space-xs` ~ `--space-3xl` / `--radius-sm` ~ `--radius-xl`
- `--fs-footnote` ~ `--fs-display`

## 커스텀 블록

마크다운에 `:::block-name ... :::` 형태로 사용:

- `:::goal` — 챕터 목표 박스
- `:::prep` / `:::prep-section-md` — 준비 섹션
- `:::tip` — 팁 박스
- `:::note` — 일반 메모
- `:::remember` — 챕터 말미 회상 박스
- `:::term-box` — 용어 설명
- `:::compare` — 비교 박스
- `:::rag-pipeline` — RAG 파이프라인 3단계
- `:::journey` — 여정 카드
- `:::result-fail` / `:::result-ok` — 결과 박스

## 코드 블록 배지

```markdown
```python [실습 N] ex01/file.py. 설명
...
```
```

배지 종류:
- `[실습 N]` — TODO 있는 실습 코드 (파란 배지)
- `[터미널]` — bash/shell 명령 (초록 배지)
- `[설명]` — 완성본 발췌 (보라 배지)
- `[참고]` — 인프라 코드 (회색 배지)

`# TODO:` 주석은 자동으로 노란 하이라이트가 적용된다. 구문 강조는 Pygments가 서버사이드에서 처리.

## 의존성

```
playwright==1.48
markdown-it-py==3.0
mdit-py-plugins>=0.4
jinja2==3.1
pygments>=2.17
```

Playwright Chromium 설치 필요:
```bash
python -m playwright install chromium
```
