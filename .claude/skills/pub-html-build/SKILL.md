---
name: pub-html-build
description: Use when building a book project from Markdown chapters to HTML preview. Owns templates, design tokens, custom markdown blocks, and the HTML rendering pipeline. PDF conversion is handled by the separate `pub-html-to-pdf` skill. Self-contained — superpowers optional. Invoke with --project-root to point at the book source.
---

# pub-html-build

마크다운 챕터 → HTML 프리뷰 파이프라인. 챕터마다 글 모양을 수정·검토할 때 쓰는 **HTML 뷰 전담** 스킬. PDF 변환이 필요하면 별도 스킬 [`pub-html-to-pdf`](../pub-html-to-pdf/SKILL.md)를 호출한다.

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
python .claude/skills/pub-html-build/build_html.py \
  --project-root projects/<책> \
  --chapter N
```

옵션:

| 옵션 | 설명 |
|------|------|
| `--project-root PATH` (필수) | 책 프로젝트 루트 |
| `--chapter N` | 특정 챕터만 빌드. 생략 시 전체 챕터 |
| `--open` | 빌드 끝나면 **OS 기본 브라우저에 첫 챕터 자동 열기** (file://) |
| `--preview NAME` | 빌드 없이 `.build/preview/<NAME>.html`을 바로 브라우저로 열기. 스와치·재디자인 페이지 확인용 |

빌드가 끝나면 각 챕터별로 `file://…/.build/NN-….html` URL이 출력된다. **항상 `file://` 단일 경로**이므로 로컬 서버 불필요.

### 원칙 — HTTP 서버 기동 금지, `--preview` 로 브라우저 직접 열기

사용자가 **"서버 띄워줘"·"웹에 띄워줘"·"브라우저에 올려줘"** 라고 말해도 `python -m http.server` 같은 로컬 서버를 기동하지 않는다. 이유:

1. 빌드 산출물과 `file://` 로 한 경로만 남기자는 이 스킬의 리팩터 결정 (두 갈래 뷰 경로로 인한 캐시·상대경로 꼬임 방지)
2. 로컬 서버는 브라우저 히스토리·캐시·확장프로그램을 통한 유출 경로
3. 레포 루트에 `.claude`·비밀 파일 노출 위험
4. Permission hook이 이 의도를 강제 — HTTP 서버 기동을 차단한다

**항상 `--preview NAME` 또는 `--open`** 으로 Python `webbrowser` 모듈이 OS에 `file://` URL을 전달하게 한다. 이게 동일한 "브라우저에 띄운다" 효과를 낸다.

### 브라우저로 자동 열기 (크로스 플랫폼)

Python 내장 `webbrowser` 모듈이 OS별 기본 브라우저를 찾아 열어 준다 — **macOS·Windows·Linux 공통**으로 `--open` / `--preview` 옵션이 그대로 동작한다.

```bash
# 빌드 + 첫 챕터 자동 열기
python .claude/skills/pub-html-build/build_html.py \
  --project-root projects/사내AI비서_v2 --chapter 1 --open

# 프리뷰만 열기 (빌드 안 함)
python .claude/skills/pub-html-build/build_html.py \
  --project-root projects/사내AI비서_v2 --preview tokens-swatch

python .claude/skills/pub-html-build/build_html.py \
  --project-root projects/사내AI비서_v2 --preview ch01-redesign
```

수동으로 여는 방법(OS별 명령)도 여전히 유효:

| OS | 명령 |
|----|------|
| macOS | `open "projects/…/.build/01-….html"` |
| Windows (PowerShell) | `Invoke-Item "projects\…\.build\01-….html"` 또는 `start "" "…"` |
| Linux | `xdg-open "projects/…/.build/01-….html"` |

또는 브라우저 주소창에 빌드 로그의 `file://…` URL을 그대로 붙여 넣어도 된다.

## 산출 위치

```
projects/<책>/
├── chapters/ assets/ book/    (저작)
└── .build/                    (빌드 산출물 + 저자 오버라이드)
    ├── NN-*.html              (챕터별 HTML, 한 파일 한 챕터)
    ├── tokens.css             (프로젝트 브랜드 오버라이드 — 저자 편집)
    └── styles/ → 스킬 CSS 심링크 (상대경로)

레포 루트/
└── <alias> → projects/<책>    (자동 생성되는 단축 심링크)
```

- **레포 루트 alias 심링크**: 빌드 시 자동. `projects/<책>` 한 단 건너뛰어 `file://…/<alias>/.build/NN.html` 로 짧게 접근.
- alias 결정: `progress.json["alias"]` 우선 → 없으면 `progress.json["project"]` 또는 폴더명에서 `_vNN` 접미어 제거.
- 책이 여러 개일 때 이름 충돌이 나면 빌드 중 경고가 뜬다. `progress.json`의 `alias` 필드로 고유 이름 지정.
- 에셋(`../assets/CH_/*.png`)은 심링크 없이 상대경로로 직접 참조. 브라우저가 원본 `assets/`를 바로 연다.

## 새 책 초기화

```bash
bash .claude/skills/pub-html-build/scripts/init_book.sh projects/<새-책이름>
```

생성되는 구조:
- `chapters/` — 챕터 마크다운
- `assets/` — 이미지·다이어그램
- `book/{front,back}` — 프롤로그·에필로그 저작물
- `.build/tokens.css` — 브랜드 토큰 **오버라이드 템플릿** (저자 편집)

상세 절차는 [`modes/reuse.md`](modes/reuse.md) 참조.

## 파일 구조

```
pub-html-build/
├── SKILL.md                        # 이 문서 (진입점)
├── build_html.py                   # 파이프라인 진입점 (HTML 전용)
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
    ├── boxes/ fullmap/ cards/
    ├── comparisons/ pipelines/ captions/
    └── terminals/
```

## 디자인 토큰

브랜드 컬러·여백·반지름은 `styles/tokens.css`에서 CSS 변수로 관리. 프로젝트가 `<프로젝트>/.build/tokens.css`를 두면 스킬 토큰을 선택적으로 덮어쓴다 (CSS cascade). 이 파일은 **저자가 직접 편집**하는 저작물이지만 편의상 빌드 폴더에 같이 둔다.

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
markdown-it-py==3.0
mdit-py-plugins>=0.4
jinja2==3.1
pygments>=2.17
```

PDF 변환이 필요하면 [`pub-html-to-pdf`](../pub-html-to-pdf/SKILL.md)를 사용. 이 스킬은 HTML만 생성한다.
