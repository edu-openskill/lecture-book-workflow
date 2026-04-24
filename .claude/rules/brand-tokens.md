# 브랜드 토큰 단일 진실원 규칙

오픈스킬북스의 색·여백·타이포는 **한 파일**에서만 정의된다.

- **단일 진실원**: `.claude/skills/pub-html-build/styles/tokens.css`
- **책별 변주 (선택)**: `projects/<책>/.build/tokens.css` — 없으면 스킬 기본값
- **시각 가이드**: `projects/<책>/.build/preview/tokens-swatch.html` (브랜드에 포함되는 그룹만 노출)
- **카탈로그 인덱스**: `projects/<책>/.build/preview/components-catalog-index.html` (각 컴포넌트가 어떤 토큰 쓰는지)

## 토큰 그룹

| 그룹 | 변수 접두어 | 성격 | 브랜드 노출 |
|------|----------|------|----------|
| **Primary** | `--color-accent*` | 메인 (인디고). 링크·버튼·강조·박스 테두리 | ✅ swatch에 노출 |
| **Secondary** | `--color-accent-warm*` | 보조 (오렌지). `:::remember`·`:::tip`·`.term`·h1 번호·미니맵·user 아이콘 | ✅ swatch에 노출 |
| **Info** | `--color-info*` | 정보 블루. 정보 박스·링크 보조 | ✅ swatch에 노출 |
| **Neutral** | `--color-text*` / `--color-bg` / `--color-surface*` / `--color-border*` | 무채색 텍스트·배경·테두리 | ✅ swatch에 노출 |
| **Utility · 상태변수** | `--color-success*` / `--color-warning*` / `--color-danger*` | 진단 상태 표시 | ❌ **swatch 노출 금지** · 축소 대상 |

## 컴포넌트 배경 원칙 — 흰 배경 기본

모든 HTML 컴포넌트(다이어그램·터미널·비교 박스 등)의 **본문 영역은 흰 배경(`#fff`)** 을 기본으로 한다. 이유:
- **독서 가독성**: 본문 바탕(body)이 흰색이므로 컴포넌트도 흰색일 때 시선 흐름이 끊기지 않는다
- **인쇄·PDF 일관성**: Chromium headless PDF 렌더에서 회색 배경 재현 차이 회피
- **종이 독서 경험**: 전자책은 결국 종이처럼 읽힘 — 컴포넌트가 종이 위 "카드"로 보이게

### 적용
- `.terminal-log` (chrome + body), `.rag-pipeline-box` (컨테이너), `.figure-group` 래퍼, `.annotated-compare` 컨테이너, `.librarian-scene` 컨테이너 등 **컴포넌트의 최상위 배경은 `#fff`**
- 내부 역할 분리는 **색이 아닌 테두리·그림자·악센트(heading·뱃지)** 로 표현
- 색을 대량으로 채우지 않는다 — 시각 강조는 테두리 색·뱃지 색으로 충분

### 예외 (허용)
- `:::goal` / `:::tip` / `:::remember` / `:::note` / `:::term-box` / `:::prep` 등 **boxes 계열** directive — 약한 색 배경(`--color-accent-bg`·`--color-accent-warm-bg`·무채색 계열) 허용
- 비교 강조: `.annotated-compare .ac-block.llm / .truth`처럼 **반드시 대비가 필요한 블록**만 약한 색 배경
- 번호 뱃지·태그: 점·원·사각 뱃지는 진한 색 배경 OK

**원칙 요약**: "흰 종이 위에 테두리만 그어 박스를 만든다"가 기본. 색은 포인트에만.

## Elevation (그림자) — 이미지·다이어그램 공용

HTML 다이어그램은 **이미지와 같은 시각 무게**를 갖도록 공용 그림자 토큰을 공유한다.

- **단일 진실원**: `tokens.css`의 `--shadow-figure` (현재 `none` — 그림자 비활성화, 테두리만으로 경계 표시)
- **적용 대상**:
  - 이미지: `.chapter-image img`
  - 단독 다이어그램: `.arch11`, `.terminal-log`, `.rag-pipeline-box`, `.llm-rag-split`, `.librarian-scene`, `.annotated-compare`
  - 묶음 래퍼: `.figure-group` (여러 다이어그램을 하나의 "그림 N-N" 단위로 묶을 때)
- **중첩 금지**: `.figure-group > *`는 `box-shadow: none !important`. 래퍼에만 그림자를 남긴다.
- **신규 다이어그램 추가 시**: 단독 사용 컴포넌트는 `box-shadow: var(--shadow-figure)` 셀렉터 목록에 편입한다.

## Utility(상태변수) 축소 정책

1. **새 컴포넌트는 사용 금지** — Primary·Secondary·Info·무채색으로 상태·좋음/나쁨을 표현한다
2. **기존 컴포넌트는 점진 교체** — 의미 손실 없이 축소 가능한 곳부터
3. **의미 구분이 반드시 필요한 곳**(예: embed good/bad, proc-compare ef-ok/fail)은 유지 또는 Primary·Info 2색 대비로 대체 검토
4. 변수 자체는 아직 유지(기존 59곳 렌더 보호). 사용처 0이 되면 그때 `tokens.css`에서 삭제

## 수정 시 세 파일 동기화 규칙

컴포넌트의 색 변수를 수정·추가·삭제할 때는 **반드시 세 위치를 함께 업데이트**한다. 하나만 건드리면 다음 세션에서 상태가 어긋난다.

```
1. 컴포넌트 CSS
   .claude/skills/pub-html-build/styles/{base,components,diagrams,print}.css

2. 카탈로그 문서 (컴포넌트가 어떤 토큰 쓰는지 기록)
   .claude/skills/pub-html-build/components-catalog/<category>/README.md
   .claude/skills/pub-html-build/components-catalog/inventory.md

3. 토큰 파일 (새 변수 추가·기존 변수 삭제·섹션 주석)
   .claude/skills/pub-html-build/styles/tokens.css
```

추가로 프리뷰 2개도 같이 갱신:

```
4. Swatch 프리뷰 — 브랜드 그룹에 변경이 있으면
   projects/<책>/.build/preview/tokens-swatch.html

5. 카탈로그 인덱스 프리뷰 — 컴포넌트 색 뱃지
   projects/<책>/.build/preview/components-catalog-index.html
```

## 챕터를 손볼 때

챕터 마크다운(`chapters/NN-*.md`)에서 컴포넌트를 쓰는 방법을 바꾸면(새 클래스 도입·기존 클래스 제거), 그 결과 카탈로그·토큰도 바뀌었을 수 있다. 챕터 편집 직후 이 세 곳을 점검:

- [ ] 컴포넌트 CSS가 더 이상 쓰이지 않는 클래스를 지우거나 새 클래스를 추가했나
- [ ] 카탈로그 README·inventory가 이 컴포넌트를 여전히 정확히 기술하나
- [ ] tokens.css에 새 변수가 필요하거나 기존 변수가 쓰이지 않게 됐나

## 책별 오버라이드

각 프로젝트의 `.build/tokens.css`에서 변수 일부만 재선언하면 해당 책에만 적용(CSS cascade). 스킬 기본 토큰은 변경하지 않는다. 예:

```css
/* projects/별책/.build/tokens.css */
:root {
  --color-accent: #059669;          /* 이 책만 그린 톤 */
  --color-accent-bg: #d1fae5;
}
```

## 관련 파일

- 렌더 파이프라인 스킬: `.claude/skills/pub-html-build/`
- 컴포넌트 카탈로그: `.claude/skills/pub-html-build/components-catalog/`
- 빌드 커맨드: `python .claude/skills/pub-html-build/build_html.py --project-root projects/<책> --preview tokens-swatch`
