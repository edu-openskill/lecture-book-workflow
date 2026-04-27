# Mode: Design Explore (디자인 탐색)

## 언제 쓰는가

- 카탈로그([`../components-catalog/`](../components-catalog/))에 없는 **새 컴포넌트**가 필요
- 책 전체 톤(레이아웃/타이포)을 바꾸고 싶음
- 브랜드 색상 이상의 디자인 방향 변경
- "이 책만의 정체성" 시각 요소 설계

## 원칙

- **superpowers 플러그인 없어도 완주 가능**: 내장 7 질문 + 강제 변형 4축으로 깊이·다양성 확보
- **카탈로그 우선**: 80% 이상 재사용 가능하면 [`reuse.md`](reuse.md)로 전환
- **자유 발상 금지**: 변형은 4축 프리셋 기반. 품질 편차 방지

## 절차 (4 단계)

### Step 1. 의도 수집 (내장 7 질문)

책 집필을 시작하는 저자에게 다음 7개를 **차례로** 묻는다. 모든 답을 받기 전 다음 단계 진행 금지.

저자 답변은 `projects/<책>/planning/design-brief.md`에 저장한다.

| # | 질문 |
|---|------|
| 1 | **타깃 독자** — 이 책을 누가 읽는가? (경력 N년 / 직무 / 관심사) |
| 2 | **톤** — 한 줄로 표현하면? (예: "조용하고 단단한" / "실험적이고 대담한" / "친근하고 부드러운") |
| 3 | **유사 책** — 디자인적으로 참고할 책/사이트 2~3개 (URL 있으면 함께) |
| 4 | **금기 요소** — 절대 들어가면 안 되는 것 (예: "이모지 금지", "네온 컬러 금지") |
| 5 | **주인공 컴포넌트** — 이 책에서 가장 자주 등장할 시각 요소 1~2개 (예: 실습 코드 박스, 대화문, 다이어그램) |
| 6 | **분량 감** — 한 챕터 평균 몇 페이지? 이미지/다이어그램 비중은? (저·중·고) |
| 7 | **파이프라인** — PDF 인쇄본도 만들 예정인가? (Y면 Typst 경유 가능, N이면 전자책만) |

**superpowers 연계 (선택)**: `superpowers:brainstorming` 스킬이 있으면 이 단계를 더 깊게 대화 형식으로 대체할 수 있다. 없어도 위 7 질문만으로 충분히 탐색 가능.

### Step 2. 카탈로그 우선 검토

답변을 기반으로 [`../components-catalog/`](../components-catalog/) 전수를 훑는다.

체크:
- [ ] 각 카테고리에서 **재사용 가능한 컴포넌트** 리스트 추출
- [ ] 총 필요 컴포넌트 대비 **재사용률** 계산 (예: 12개 필요 중 10개 재사용 → 83%)
- [ ] 80% 이상이면 [`reuse.md`](reuse.md)로 전환 (이 모드 종료)
- [ ] 80% 미만이면 "신규 설계 필요 컴포넌트" 리스트 확정

### Step 3. 신규 설계 — 강제 변형 4축

각 신규 컴포넌트에 대해 **반드시 4축 변형**을 뽑는다. 자유 발상 금지.

| 축 | 방향 | 특징 | 레퍼런스 |
|----|------|------|---------|
| **A. Editorial (고급)** | 여백 크게, 세리프 제목, 단색 액센트 | 차분·신중·전문성 | `Wired`, `The New Yorker` 디지털 |
| **B. Playful (캐주얼)** | 둥근 코너, 파스텔, 손글씨 느낌 | 친근·부드러움 | `Duolingo`, `Figma` 블로그 |
| **C. Technical (미니멀)** | 격자 정렬, 모노스페이스, 대비 | 정밀·기능성 | `Stripe Docs`, `Linear` |
| **D. Bold (대담)** | 큰 블록 컬러, 굵은 산세리프, 강한 그림자 | 강한 시선·에너지 | `Vercel`, `Posthog` 랜딩 |

각 변형을 HTML+CSS 미리보기 페이지로 만들어 저자가 선택한다 (표지 위자드와 동일 패턴).

```bash
# 예: .chapter-note 라는 신규 박스를 만들 때
python .claude/skills/pub-html-build/scripts/component_variants.py \
  --component chapter-note \
  --axes A,B,C,D \
  --out projects/<책>/design-preview/chapter-note.html
open projects/<책>/design-preview/chapter-note.html
```

(`component_variants.py`는 [`../scripts/component_variants.SPEC.md`](../scripts/component_variants.SPEC.md)에 스펙 명세. 실구현은 후속 PR에서.)

### Step 4. 선택 후 반영

저자가 변형 중 하나를 선택하면:

1. **CSS 추가** — `../styles/components.css`에 선택된 변형 CSS 블록 추가
   - 토큰 변수 필수 (`var(--color-*)`, `var(--font-*)`)
   - 이름 규칙은 [`../components-catalog/README.md`](../components-catalog/README.md#이름-규칙) 준수
   - `../components-catalog/inventory.md`의 "사용 중인 접두어 네임스페이스" 충돌 확인

2. **카탈로그 등록** — 알맞은 카테고리 `README.md`에 5 항목 추가
   - 언제 쓰는가
   - HTML 사용 예
   - 렌더 CSS (파일:라인)
   - 변형
   - 피해야 할 것

3. **첫 사용 챕터** 마크다운에 HTML 삽입 → 빌드 → 결과 확인

## 체크리스트

- [ ] `planning/design-brief.md`에 7 질문 모두 답변 기록됨
- [ ] 카탈로그 재사용률 계산됨
- [ ] 신규 컴포넌트별 4축 변형 모두 프리뷰됨
- [ ] 선택된 변형이 `styles/components.css`에 반영됨
- [ ] 카탈로그에 5 항목으로 등록됨
- [ ] 첫 사용 챕터에 HTML 삽입 후 빌드 성공

## 피해야 할 것

- **의도 수집 건너뛰기** — 7 질문 답을 받기 전 바로 변형 생성 금지
- **재사용률 체크 생략** — 카탈로그에 이미 있는 걸 모르고 새로 만들기
- **4축 중 일부만** — 4개 변형을 모두 보여주고 선택받는 게 원칙 (편견 방지)
- **이름 충돌 무시** — `rc-*` 처럼 이미 두 곳에 쓰이는 접두어 재사용
- **단일 사용 컴포넌트** — 한 챕터에서만 쓸 거라면 그냥 인라인 HTML로 해결 (카탈로그는 재사용 목적)

## superpowers 연계 가이드

설치 여부와 관계없이 이 스킬은 자기완결적이지만, 있으면 더 풍부해진다.

| 설치된 경우 | 없는 경우 |
|------------|----------|
| `superpowers:brainstorming` → Step 1 의도 수집 대체 (대화 깊이 증가) | 내장 7 질문 그대로 |
| `superpowers:writing-plans` → Step 3 신규 설계 전 플랜 작성 | 변형 4축을 바로 반영 |
| `superpowers:verification-before-completion` → Step 4 반영 후 검증 | 체크리스트 수동 확인 |

조건부 흐름:

```
if superpowers 설치됨:
    superpowers:brainstorming 호출 → planning/design-brief.md 저장
else:
    이 문서의 내장 7 질문 그대로 진행
```
