# Why-Log

실수에서 배운 규칙을 기록한다. 각 항목은 YAML 블록으로 관리하며,
해당 규칙이 반영된 파일을 `rule_added_to`로 추적한다.

---

```yaml
# ── 캡처/스타일 ───────────────────────────────────────

- id: "2026-03-15-1"
  date: 2026-03-15
  category: capture
  summary: 서적용 캡처 — ANSI 색상 변환 금지 + 이미지 플레이스홀더 필수
  detail: >
    캡처 이미지에 ANSI 색상이 그대로 남고, 챕터에 이미지 플레이스홀더가 누락됨.
    근본 원인: 서적 캡처 시 스타일 규칙(블랙/볼드/여백)이 부재.
  rule_added_to:
    - .claude/rules/style.md
    - .claude/rules/structure.md

- id: "2026-03-15-2"
  date: 2026-03-15
  category: capture
  summary: 서적용 캡처 — Rich 출력 trailing 공백 제거
  detail: >
    색상/padding 수정 후에도 오른쪽 빈 공간 잔존. COLUMNS=100으로 Rich가
    줄 끝을 공백으로 채움. line.rstrip() + columns 축소로 해소.
  rule_added_to:
    - .claude/rules/style.md

# ── 구조/목차 ─────────────────────────────────────────

- id: "2026-03-15-3"
  date: 2026-03-15
  category: structure
  summary: 레포 소개 블록 필수 — URL 테이블만으로 끝내지 마라
  detail: >
    기술 파트 시작 시 git clone → 파일 트리 → start/end 안내 형식 필수.
    근본 원인: heading 레벨과 목차 depth의 연관을 점검하지 않음.
  rule_added_to:
    - .claude/rules/structure.md

- id: "2026-03-15-4"
  date: 2026-03-15
  category: build
  summary: 프로젝트 book_base.typ은 스킬 원본의 복사본 — 심볼릭 링크 사용
  detail: >
    스킬 원본 수정이 프로젝트에 반영되지 않음. 복사본이라 동기화 안 됨.
  rule_added_to:
    - skills/pub-typst-design/SKILL.md

# ── 레이아웃/공백 ─────────────────────────────────────

- id: "2026-03-15-5"
  date: 2026-03-15
  category: layout
  summary: PDF 페이지 하단 1/3 이상 공백 시 조치 필수
  detail: >
    이미지가 남은 공간에 안 들어가 다음 페이지로 밀림.
    최소 축소 비율이 높아서 중간 크기 공백을 활용하지 못함.
  rule_added_to:
    - .claude/agents/publisher/AGENT.md

# ── D2 다이어그램 디자인 ─────────────────────────────

- id: "2026-03-15-6"
  date: 2026-03-15
  category: design
  summary: D2 생성 시 샘플 디자인 classes 복사 필수 + img 경로 변경 시 파일도 이동
  detail: >
    새 D2 파일을 만들 때 classes를 직접 정의하여 디자인 불일치.
    img 경로만 바꾸고 파일을 이동하지 않아 이미지 깨짐.
  rule_added_to:
    - .claude/agents/publisher/AGENT.md
    - .claude/rules/structure.md

- id: "2026-03-15-7"
  date: 2026-03-15
  category: design
  summary: 다이어그램 강조색 금지 — 화이트로 통일
  detail: >
    danger/success 등 시맨틱 클래스에 빨강/초록 적용하여 디자인 불일치.
  rule_added_to:
    - .claude/agents/publisher/AGENT.md

# ── 빌드 파이프라인 ───────────────────────────────────

- id: "2026-03-15-8"
  date: 2026-03-15
  category: build
  summary: 빌드 후 레이아웃 자동 검수 미실행
  detail: >
    pub-layout-check 스킬이 빌드 파이프라인에 통합되지 않음.
    스킬 생성과 파이프라인 통합을 별개 작업으로 처리.
  rule_added_to:
    - typst_builder.py

- id: "2026-03-15-9"
  date: 2026-03-15
  category: layout
  summary: PDF 조판 세부 규칙 부재 — 6개 이슈
  detail: >
    인용 디자인, 터미널 이미지 크기, 코드 블록 간격, 용어표 열 균등 등
    콘텐츠 유형별 세분화 규칙 부재.
  rule_added_to:
    - book_base.typ
    - typst_builder.py
    - .claude/agents/publisher/AGENT.md

- id: "2026-03-15-10"
  date: 2026-03-15
  category: build
  summary: layout-check 후 자동 이미지 축소 + 재빌드 최대 3회 반복
  detail: >
    Mermaid 미변환 + callout 하이픈 + 공백 감지만 하고 자동 수정 없음.
    감지→수정→재빌드 루프 구현.
  rule_added_to:
    - .claude/agents/publisher/AGENT.md
    - typst_builder.py

- id: "2026-03-15-11"
  date: 2026-03-15
  category: design
  summary: D2 텍스트 잘림 — 박스 크기가 텍스트 길이 미고려
  detail: >
    모든 박스를 동일 width로 설정. flow 다이어그램 전용 이미지 비율도 부재.
  rule_added_to:
    - typst_builder.py

- id: "2026-03-15-12"
  date: 2026-03-15
  category: build
  summary: 이미지 비율 패턴 오탐 — overflow에 flow 매칭
  detail: >
    'flow' in path 부분 문자열이 context-overflow 등에 오탐.
  rule_added_to:
    - typst_builder.py

- id: "2026-03-15-13"
  date: 2026-03-15
  category: layout
  summary: low_usage 감지 기준 45% → 60%로 완화
  detail: >
    56% 사용률 페이지가 미감지. 터미널 이미지 0.95가 공백 밀림 유발.
  rule_added_to:
    - pdf_layout_checker.py
    - typst_builder.py

- id: "2026-03-15-14"
  date: 2026-03-15
  category: layout
  summary: 마지막 페이지 공백 — 이미지 축소로 해결 불가
  detail: >
    콘텐츠 양 자체 조정 필요. "더 알아보기" 통합으로 해소.
  rule_added_to: []

- id: "2026-03-15-15"
  date: 2026-03-15
  category: build
  summary: Mermaid 미변환이 프로젝트 전체가 아닌 챕터 단위로만 수행
  detail: >
    CH01만 변환하고 CH02 이후 점검 누락. 이미지 폴더 분류도 미준수.
  rule_added_to: []

- id: "2026-03-15-16"
  date: 2026-03-15
  category: build
  summary: autocrop tolerance 부재 — Gemini 이미지 연한 회색 배경 미제거
  detail: >
    순백(#FFFFFF)만 빈 공간으로 판단. ±10 tolerance 추가로 23개 이미지 추가 crop.
  rule_added_to:
    - typst_builder.py

- id: "2026-03-15-17"
  date: 2026-03-15
  category: layout
  summary: 이미지 크기 경로별 7가지 분기 → 3가지로 단순화
  detail: >
    개별 이슈 대응으로 패턴이 누적. 사용률 계산 공식도 함수 간 불일치.
  rule_added_to:
    - typst_builder.py
    - pdf_layout_checker.py

# ── 챕터 작성 ─────────────────────────────────────────

- id: "2026-03-15-19"
  date: 2026-03-15
  category: writing
  summary: 챕터 헤더 blockquote — 각 줄 끝 <br> 태그 필수
  detail: >
    CH01만 정상 출력. CH02 이후 <br> 누락으로 PDF에서 줄바꿈 깨짐.
  rule_added_to:
    - .claude/rules/structure.md

- id: "2026-03-15-20"
  date: 2026-03-15
  category: build
  summary: 인라인 코드 □ 깨짐 — 모노스페이스 폰트 미지정
  detail: >
    raw.where(block:false) show rule에서 it.text가 raw 해제하여 본문 폰트 적용.
  rule_added_to:
    - book_base.typ
    - .claude/rules/style.md

- id: "2026-03-15-21"
  date: 2026-03-15
  category: design
  summary: 시퀀스 다이어그램이 플로우차트로 작성됨
  detail: >
    D2 변환 시 direction:right 일률 적용. 본문 맥락의 다이어그램 유형 미반영.
  rule_added_to: []

- id: "2026-03-15-22"
  date: 2026-03-15
  category: writing
  summary: '"이번 버전: exNN → exNN" 메타데이터를 챕터에 넣지 마라'
  detail: >
    독자에게 불필요한 메타데이터. planning 문서에만 기록.
  rule_added_to:
    - .claude/agents/writer/AGENT.md

- id: "2026-03-15-23"
  date: 2026-03-15
  category: writing
  summary: 실습 순서를 다이어그램으로 만들지 마라 — 번호 목록 사용
  detail: >
    3~5단계 단순 순서는 번호 목록이 더 간결하고 지면 효율적.
  rule_added_to:
    - .claude/agents/writer/AGENT.md

- id: "2026-03-15-24"
  date: 2026-03-15
  category: design
  summary: D2 디자인 불일치 — 파란 배경 스타일 미준수
  detail: >
    일부 D2가 fill:#3b82f6 파란 배경. 흰배경+파란테두리 가이드 미준수.
  rule_added_to: []

- id: "2026-03-15-25"
  date: 2026-03-15
  category: writing
  summary: 줄바꿈이 너무 많다 — 문단 구성 원칙 부재
  detail: >
    같은 맥락의 문장이 빈 줄로 불필요하게 분리. 약 90건 합치기 수행.
  rule_added_to:
    - .claude/rules/style.md

- id: "2026-03-15-26"
  date: 2026-03-15
  category: capture
  summary: 캡처 전 console.rule() 잔존 여부 grep 점검 필수
  detail: >
    실험 스크립트가 console.rule() 사용하여 장식선이 캡처에 포함됨. 31건 교체.
  rule_added_to:
    - .claude/rules/code.md

# ── 2026-03-16 신규 ───────────────────────────────────

- id: "2026-03-16-1"
  date: 2026-03-16
  category: dispatch
  summary: STEP 완료 전 호출된 에이전트 목록 대조 필수
  detail: >
    디스패치 테이블의 에이전트 전체가 호출되었는지 검증하지 않아 누락 발생.
  rule_added_to:
    - .claude/rules/structure.md

- id: "2026-03-16-2"
  date: 2026-03-16
  category: dispatch
  summary: 디스패치 테이블 에이전트 순서 생략 금지
  detail: >
    챕터 작성 시 일러스트레이터를 건너뛰고 writer → editor만 호출하여
    다이어그램/캡처가 누락된 채 챕터가 완료 처리됨.
  rule_added_to:
    - .claude/rules/structure.md

# ── 2026-03-27 pub-studio 모듈화 ─────────────────────

- id: "2026-03-27-1"
  date: 2026-03-27
  category: build
  summary: 개별 이미지 목록 빈 상태 — stage 조건이 fetchImages 차단
  detail: >
    builder.js의 if (data.stage === 1) fetchImages() 조건이 stage 2
    캐시 빌드 시 이미지 목록 갱신을 차단. 조건 제거로 해소.
  rule_added_to:
    - static/js/builder.js

- id: "2026-03-27-2"
  date: 2026-03-27
  category: build
  summary: MD 문단 간격 미적용 — Typst par spacing 누락
  detail: >
    design_assembler.py에서 #set block(spacing:)만 설정.
    Typst 문단 간격은 #set par(spacing:)도 필요.
    block은 블록 요소 간 간격, par은 문단 내 줄 간격 제어.
  rule_added_to:
    - scripts/design_assembler.py

- id: "2026-03-27-3"
  date: 2026-03-27
  category: design
  summary: ES Module export let은 외부 모듈에서 재할당 불가
  detail: >
    export let foo; 후 다른 모듈에서 import { foo }; foo = 1; 하면
    TypeError. export const shared = {} 객체의 프로퍼티로 가변 상태를
    관리하는 패턴으로 해소.
  rule_added_to:
    - static/js/state.js

- id: "2026-03-27-4"
  date: 2026-03-27
  category: design
  summary: CSS 변형 하드코딩 → 동적 생성으로 전환
  detail: >
    book.css의 [data-design="d1"]/[data-design="d2"] 14개 규칙이
    하드코딩. 커스텀 변형(d3+)을 지원하려면 동적 CSS 생성 필수.
    BUILTIN_VARIANTS JSON + renderVariantCSS() + <style> 주입 패턴 채택.
  rule_added_to:
    - static/js/state.js
    - static/js/renderer.js
    - static/css/book.css
```
