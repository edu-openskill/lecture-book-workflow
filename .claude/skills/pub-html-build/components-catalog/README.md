# components-catalog

`pub-html-build` 스킬이 제공하는 HTML/CSS 컴포넌트의 카탈로그. 새 챕터를 집필할 때 **여기서 조립**하면 된다. 없는 컴포넌트는 [`../modes/design-explore.md`](../modes/design-explore.md)로 신규 설계.

## 카테고리

| 디렉토리 | 담당 |
|---------|------|
| [boxes/](boxes/) | `:::`/`::::` directive + 박스형 블록 (goal·prep·tip·note·term-box·remember) |
| [fullmap/](fullmap/) | 책 전체 구성도 (`.arch-fullmap` + `.afm-*`) |
| [cards/](cards/) | 개별 카드 (청크·임베딩 카드) |
| [comparisons/](comparisons/) | 비교형 시각 요소 (A vs B, before/after) |
| [pipelines/](pipelines/) | 흐름·타임라인·파이프라인 |
| [captions/](captions/) | 인라인 라벨·캡션·태그 |

전체 목록은 [inventory.md](inventory.md) 참조.

## 컴포넌트 추가 절차 (4단계)

1. **카탈로그 검색** — 기존 6 카테고리에서 비슷한 게 있는지 확인 ([inventory.md](inventory.md))
2. **이름 충돌 확인** — `grep -rE "^\.이름-후보" ../styles/` 로 CSS에 동명 클래스가 없는지 검증
3. **CSS 추가** — `../styles/components.css`에 클래스 정의 (토큰 변수 필수: `var(--color-*)`, `var(--font-*)`)
4. **카탈로그 등록** — 알맞은 카테고리 `README.md`에 **5 항목**으로 기록
   - 언제 쓰는가
   - HTML 사용 예
   - CSS 위치 (파일:라인)
   - 변형(Variants)
   - 피해야 할 것

## 이름 규칙

- 접두어 2~4자로 컴포넌트 군 식별
  - `cwm-*`: chunk with meta
  - `eer-*`: embedding example row
  - `afm-*`: architecture full map
  - `rl-*`: react-loop caption
  - `otd-*`: overlap text demo
  - `jf-*`: journey forward
- 상태/변형은 modifier (`.ac-strike`, `.afm-faint`, `.afm-on`)
- 새 접두어는 **3글자 이상**, 기존과 겹치지 않게 (현재 사용 중인 접두어는 inventory.md 참조)

## 사용 중인 접두어 네임스페이스

카테고리별로 배정된 접두어. 신규 컴포넌트 생성 시 충돌 회피.

| 접두어 | 용도 | 카테고리 |
|-------|------|---------|
| `afm-` | architecture full map | fullmap |
| `cwm-` | chunk with meta | cards |
| `eer-` | embedding example row | cards |
| `ac-` | annotated compare | comparisons |
| `otd-` | overlap text demo | comparisons |
| `rc-` | reindex-compare (CH03) / rc-timeline (CH07) | comparisons + pipelines (주의: 충돌) |
| `rag-` | rag pipeline | pipelines |
| `jf-` | journey forward | pipelines |
| `s-` | rag-step 내부 (pipeline 전용) | pipelines |
| `rl-` | react-loop caption | captions |
| `mm-` | minimap | 글로벌 |
| `at-` | arch-tree | 글로벌 |
