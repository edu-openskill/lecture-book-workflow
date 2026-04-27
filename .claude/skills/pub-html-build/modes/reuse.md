# Mode: Reuse (기본 재사용)

## 언제 쓰는가

새 책이 기존 디자인(타이포·박스·카드·다이어그램)을 그대로 재사용하고, **브랜드 색상/로고만** 바꾸는 경우. 이 스킬의 **기본 모드**.

## 전제 조건

- `.claude/skills/pub-html-build/` 스킬이 설치돼 있다
- `components-catalog/`에 필요한 컴포넌트가 이미 있다 (없으면 [`design-explore.md`](design-explore.md)로)
- 커스텀 디자인 토큰(컬러·폰트) 수준의 변경만 필요하다

## 절차 (5 단계)

### 1. 새 책 초기화

```bash
bash .claude/skills/pub-html-build/scripts/init_book.sh projects/<새-책이름>
```

스크립트가 생성하는 것:
- `chapters/` — 챕터 마크다운 디렉토리
- `assets/` — 이미지/다이어그램 에셋
- `book/{front,back}` — 프롤로그·에필로그 저작물
- `.build/` — 빌드 산출물 폴더
- `.build/tokens.css` — 브랜드 토큰 **오버라이드 템플릿** (이걸 수정하면 됨)

### 2. 브랜드 토큰 오버라이드

`projects/<새-책이름>/.build/tokens.css`를 연다.

가능한 변수 (스킬 기본 토큰 `styles/tokens.css`에서 오버라이드):

| 변수 | 용도 | 예시 기본값 |
|------|-----|------------|
| `--color-accent-warm` | 강조 색(따뜻한 톤) | `#dd6b20` |
| `--color-accent-warm-text` | 강조 텍스트 색 | `#9c4221` |
| `--color-text-heading` | 제목 색 | `#2d3748` |
| `--color-text-secondary` | 보조 텍스트 | `#4a5568` |
| `--color-text-muted` | 흐린 텍스트 | `#718096` |
| `--color-text-subtle` | 더 흐린 텍스트 | `#a0aec0` |
| `--color-border` | 기본 테두리 | `#e2e8f0` |
| `--color-border-dashed` | 점선/연한 테두리 | `#cbd5e0` |
| `--color-info` | 정보 파랑 | `#3182ce` |
| `--font-body` | 본문 폰트 family | `"Pretendard", ...` |
| `--font-heading` | 제목 폰트 | `"Pretendard", ...` |
| `--font-mono` | 코드/모노스페이스 | `"JetBrains Mono", ...` |

**기본 토큰 파일 건드리지 않음**. 수정 대상은 오직 `<프로젝트>/.build/tokens.css` 하나.

### 3. 컴포넌트 조립 (카탈로그에서)

챕터 원고 작성 시 [`../components-catalog/`](../components-catalog/)에서 필요한 블록을 복사해 붙여넣는다.

카테고리 색인:

| 카테고리 | 쓸 때 |
|---------|-------|
| [boxes/](../components-catalog/boxes/) | 챕터 목표·준비·팁·용어·기억 박스 |
| [fullmap/](../components-catalog/fullmap/) | 챕터 끝 "전체 구성도에서 챕터 N의 자리" |
| [cards/](../components-catalog/cards/) | 청크 카드·임베딩 예시 |
| [comparisons/](../components-catalog/comparisons/) | A vs B, before/after |
| [pipelines/](../components-catalog/pipelines/) | 흐름·타임라인 |
| [captions/](../components-catalog/captions/) | 이미지 캡션·태그 |

각 카테고리 README.md에 **"언제 쓰는가 / HTML 예 / 변형 / 피해야 할 것"** 5항목이 정리돼 있다. 그대로 따라 쓰면 된다.

### 4. 빌드

```bash
python .claude/skills/pub-html-build/build_html.py \
  --project-root projects/<새-책이름> \
  --chapter 1
```

옵션:
- `--project-root PATH` (필수)
- `--chapter N` (선택, 특정 챕터만 빌드)

빌드가 끝나면 각 챕터별로 `🔗 열기: file://…/.build/NN-….html` URL이 출력된다.

### 5. 결과 확인

- `projects/<책>/.build/NN-제목.html` — 챕터 HTML 프리뷰
- 빌드 로그에 출력된 `file://…` URL을 브라우저 주소창에 붙이거나 아래 옵션 사용
- 첫 빌드 이후 레포 루트에 `<alias>` 심링크가 자동 생성되어 `file://…/<alias>/.build/NN.html` 로도 접근 가능

브라우저 자동 열기(크로스 플랫폼, Python `webbrowser` 모듈):

```bash
# 빌드 + 브라우저 자동 열기
python .claude/skills/pub-html-build/build_html.py \
  --project-root projects/<책> --chapter 1 --open

# 이미 빌드된 프리뷰 파일만 열기 (tokens-swatch 등)
python .claude/skills/pub-html-build/build_html.py \
  --project-root projects/<책> --preview tokens-swatch
```

macOS·Windows·Linux 공통으로 같은 명령이 동작. PDF가 필요하면 [`pub-html-to-pdf`](../../pub-html-to-pdf/SKILL.md) 스킬 호출.

## 체크리스트

- [ ] `init_book.sh` 실행 → 프로젝트 디렉토리 생성됨
- [ ] `.build/tokens.css`에 오버라이드 적용됨 (기본 토큰 파일은 건드리지 않음)
- [ ] 각 챕터가 카탈로그 컴포넌트로만 조립됨 (신규 CSS 추가 없음)
- [ ] 빌드 성공 — HTML 프리뷰가 `file://` URL로 열림
- [ ] 브랜드 색상이 의도대로 반영됨

## 이 모드로 충분하지 않을 때

- 카탈로그에 없는 **새 컴포넌트**가 필요 → [`design-explore.md`](design-explore.md)
- 전체 톤/타이포/레이아웃을 다르게 → [`design-explore.md`](design-explore.md)
- 챕터 형식을 바꾸고 싶음 (예: "서문" 같은 특수 섹션) → [`design-explore.md`](design-explore.md)

## 참고

- 오버라이드 메커니즘: `build_html.py`는 프로젝트 `.build/tokens.css`를 `./styles/tokens.css` 뒤에 삽입해 스킬 기본 토큰보다 우선순위가 높다. CSS cascade 원리.
- 기본 토큰 변경 원할 시: 스킬 자체 개선이므로 별도 PR (스킬 레벨 변경은 모든 책에 영향).
