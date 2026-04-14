---
name: pub-html-build
description: Use when building a book project from Markdown chapters to HTML/PDF. Owns templates, design tokens, custom markdown blocks, and the Playwright-based PDF pipeline. Self-contained — superpowers optional. Invoke with --project-root to point at the book source.
---

# pub-html-build

마크다운 챕터 → HTML → PDF(전자책) 파이프라인. 이 프로젝트의 **HTML 출판 경로 전담** 스킬이며, 디자인 컴포넌트 카탈로그·디자인 탐색 절차를 내장해 **superpowers 플러그인 없이도 자기완결적으로 동작**한다.

## 이 스킬을 언제 쓰는가 (2가지 모드)

| 시나리오 | 모드 | 문서 |
|---------|------|------|
| 디자인 그대로 재사용 (브랜드 컬러만 바꾸기) | **Reuse** | [`modes/reuse.md`](modes/reuse.md) |
| 새 컴포넌트·새 톤 탐색 | **Design Explore** | [`modes/design-explore.md`](modes/design-explore.md) |

두 모드 중 어느 쪽이 필요한지 모르겠다면 먼저 [`components-catalog/`](components-catalog/)를 훑어보라. **80% 이상** 재사용 가능하면 Reuse, 아니면 Design Explore.

## 컴포넌트 카탈로그

이 스킬이 제공하는 HTML/CSS 컴포넌트는 [`components-catalog/`](components-catalog/)에 6 카테고리로 정리돼 있다. 각 카테고리 README.md에 **5 항목** 포맷(언제 쓰는가 / HTML 예 / 렌더 CSS / 변형 / 피해야 할 것)으로 기록.

| 카테고리 | 담당 |
|---------|------|
| [boxes/](components-catalog/boxes/) | `:::`/`::::` directive 박스 (goal·prep·tip·note·term-box·remember) |
| [fullmap/](components-catalog/fullmap/) | 책 전체 구성도 (`.arch-fullmap` + `.afm-*`) |
| [cards/](components-catalog/cards/) | 청크·임베딩 카드 |
| [comparisons/](components-catalog/comparisons/) | A vs B 비교 (annotated-compare / overlap / reindex / cache-diff / dual-image) |
| [pipelines/](components-catalog/pipelines/) | 흐름·타임라인 (rag-pipeline / rc-timeline / ec-cabinet / wrapper-arch / journey) |
| [captions/](components-catalog/captions/) | 라벨·캡션·태그 |

전체 컴포넌트 목록 + 접두어 네임스페이스 규칙: [`components-catalog/inventory.md`](components-catalog/inventory.md)

## 빌드 실행

```bash
python .claude/skills/pub-html-build/build_pdf_html.py \
  --project-root projects/<책> \
  --chapter N
```

옵션:
- `--project-root PATH` (필수): 책 프로젝트 루트
- `--chapter N` (선택): 특정 챕터만 빌드
- `--html-only`: HTML 중간 산출물만 생성 (PDF 생략)
- `--no-pagedjs`: Chromium 기본 인쇄 (빠른 빌드)

## 새 책 초기화

```bash
bash .claude/skills/pub-html-build/scripts/init_book.sh projects/<새-책이름>
```

생성되는 구조:
- `chapters/` — 챕터 마크다운
- `assets/` — 이미지·다이어그램
- `book/{front,back,build,output}` — 빌드 산출물 레이어
- `book/tokens.css` — 브랜드 토큰 **오버라이드 템플릿**

상세 절차는 [`modes/reuse.md`](modes/reuse.md) 참조.

## 파일 구조

```
pub-html-build/
├── SKILL.md                        # 이 문서 (진입점)
├── build_pdf_html.py               # 파이프라인 진입점
├── scripts/
│   ├── init_book.sh                # 새 책 초기화
│   └── component_variants.SPEC.md  # 4축 변형 프리뷰 도구 스펙
├── templates/
│   └── chapter-template.html       # Jinja2 챕터 템플릿
├── styles/
│   ├── tokens.css                  # 디자인 토큰 (CSS 변수)
│   ├── fonts.css                   # 폰트 임베드
│   ├── base.css                    # 타이포그래피·기본 HTML·코드블록
│   ├── components.css              # 커스텀 블록 (:::goal, :::tip 등)
│   ├── diagrams.css                # 시각화 컴포넌트 (arch-fullmap 등)
│   └── print.css                   # @page 규칙
├── modes/                          # 2가지 진입 모드
│   ├── reuse.md                    # 기본 재사용
│   └── design-explore.md           # 디자인 탐색 (내장 7 질문 + 4축 변형)
└── components-catalog/             # 6 카테고리 카탈로그
    ├── README.md                   # 색인 + 추가 절차 + 접두어 규칙
    ├── inventory.md                # 전수 목록 + 네임스페이스
    ├── boxes/
    ├── fullmap/
    ├── cards/
    ├── comparisons/
    ├── pipelines/
    └── captions/
```

## 디자인 토큰

브랜드 컬러·여백·반지름은 `styles/tokens.css`에서 CSS 변수로 관리. 프로젝트가 `<프로젝트>/book/tokens.css`를 두면 스킬 토큰을 선택적으로 덮어쓴다 (CSS cascade).

주요 토큰 그룹:
- `--color-text` / `--color-text-muted` / `--color-text-subtle` / `--color-text-heading`
- `--color-accent` / `-bg` / `-border` / `-text` (브랜드 인디고)
- `--color-accent-warm` / `-text` (오렌지 보조)
- `--color-info` / `-bg` / `-text` (블루)
- `--color-success` / `--color-warning` / `--color-danger` (시맨틱 3색)
- `--space-xs` ~ `--space-3xl` / `--radius-sm` ~ `--radius-xl`
- `--fs-footnote` ~ `--fs-display`

## 코드 블록 배지

```markdown
```python [실습 N] ex01/file.py. 설명
...
```
```

| 배지 | 용도 | 색상 |
|------|-----|------|
| `[실습 N]` | TODO 있는 실습 코드 | 파랑 |
| `[터미널]` | bash/shell 명령 | 초록 |
| `[설명]` | 완성본 발췌 | 보라 |
| `[참고]` | 인프라 코드 | 회색 |

`# TODO:` 주석은 자동으로 노란 하이라이트가 적용된다. 구문 강조는 Pygments(서버사이드).

## superpowers 연계 (선택)

이 스킬은 **자기완결적**이지만, superpowers 플러그인이 있으면 더 풍부한 흐름이 가능하다.

| 단계 | superpowers 있는 경우 | 없는 경우 |
|------|---------------------|----------|
| 의도 수집 | `superpowers:brainstorming` 호출 → `planning/design-brief.md` | `modes/design-explore.md`의 내장 7 질문 |
| 대규모 리팩터 계획 | `superpowers:writing-plans` | 이 스킬 문서만으로 진행 |
| 변경 완료 검증 | `superpowers:verification-before-completion` | 각 모드 문서의 체크리스트 |

## 의존성

```
playwright==1.48
markdown-it-py==3.0
mdit-py-plugins>=0.4
jinja2==3.1
pygments>=2.17
```

Playwright Chromium 설치:
```bash
python -m playwright install chromium
```
