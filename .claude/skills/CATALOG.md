# 스킬 카탈로그 (23개 + PM 13개 + 인쇄소 6개)

하나의 작업만 수행하고 결과를 돌려주는 원자적 도구. 판단하지 않는다.

> 상세 설계: `design/v3/스킬-검토모드-구조-v3.md`

---

## 스킬 폴더 구조

| 폴더 | 모델 | 담당 스킬 | 참조 파일 |
|------|------|----------|----------|
| `writing/` | `claude-sonnet-4-6` | C1, C2, C3, C4, C5, D2 | storytelling, style, box-style, project-buildup |
| `planning/` | `claude-sonnet-4-6` | B1, B2, B6, D6 | gap-analysis, pagination |
| `code/` | `claude-sonnet-4-6` | A1, A2, A3, A4, A5, B3, B4 | code-analysis, code-explanation |
| `visual/` | `claude-haiku-4-5-20251001` | B5 | mermaid, image |
| `image-analyzer/` | `claude-sonnet-4-6` | E1 | analysis-guide |
| `screenshot/` | — | — | terminal-capture, browser-capture, capture.py |
| `review/` | `claude-opus-4-6` | D1, D3, D4, D5 | review-rules |
| `pub-studio/` | `claude-sonnet-4-6` | — | 프리뷰 에디터 + 검증 빌드 (8개 모듈) |
| `pub-build/` | — | — | MD→Typst→PDF 빌드 파이프라인 |
| `pub-typst-design/` | — | — | Typst 템플릿 + 컴포넌트 |
| `pub-layout-check/` | — | — | PDF 레이아웃 분석 |
| `pub-page-fit/` | — | — | 레이아웃 자동수정 전략 |
| `pub-image-optimize/` | — | — | 이미지 공백제거 + 크기조절 |

---

## Tier 분류

| Tier | 수준 | 개수 | 어떤 스킬 |
|------|------|------|----------|
| **Tier 1** | 상세 (입력/출력/규칙/예시) | 7개 | 규칙이 없으면 결과가 불안정한 스킬 |
| **Tier 2** | 간략 (한 줄 + 입출력) | 9개 | 입출력만 알면 되는 스킬 |
| **Tier 3** | 목록 (한 줄 설명) | 6개 | AI가 자연스럽게 수행하는 스킬 |

---

## Tier 1 — 상세 정의 (7개)

| 스킬 | 하는 일 | 핵심 규칙 | 스킬 폴더 |
|------|---------|----------|----------|
| C1. 비유-생성기 | 기술 용어 → 일상 비유 | **기술 용어로 비유 금지** | writing/ |
| B3. 코드-태거 | 파일에 [실습/설명/참고] 태그 | [실습]=핵심(직접 작성), [설명]=읽기, [참고]=파일명만 | code/ |
| B6. 갭-분석기 | 목차 vs 도메인 표준 비교 | [필수/권장/선택] 우선순위 | planning/ |
| D3. 파트-분리-검증기 | 이야기/기술 파트 분리 검증 | 이야기 파트에 코드 블록 금지 | review/ |
| D4. 포맷-검증기 | 상수 준수 검증 | 구조, 코드 성격, 톤 체크 | review/ |
| D5. 의도-대조기 | seed.md 의도와 대조 | 범위 이탈, 깊이 초과 감지 | review/ |
| D6. 분량-계산기 | 예상 페이지 수 계산 | 1페이지 ≈ 500자 | planning/ |

## Tier 2 — 간략 정의 (9개)

| 스킬 | 입력 → 출력 | 스킬 폴더 |
|------|------------|----------|
| A1. 구조-스캐너 | 프로젝트 경로 → 디렉토리 트리 | code/ |
| A2. 기능-추출기 | 코드 파일 → 기능 목록 | code/ |
| A3. 기술스택-탐지기 | 빌드 파일 + 코드 → 기술 스택 목록 | code/ |
| A4. 의존성-매퍼 | 코드 파일 → 의존성 그래프 | code/ |
| A5. diff-생성기 | 버전A, 버전B → 차이 요약 | code/ |
| B1. 기능-정렬기 | 기능 목록 + 의존성 → 난이도순 정렬 | planning/ |
| B2. 스냅샷-설계기 | 정렬된 기능 + 시나리오 → 버전별 스냅샷 | planning/ |
| B4. 계층-생성기 | 태그 붙은 파일 목록 → 트리 시각화 | code/ |
| B5. 난이도-곡선기 | 챕터 목록 + 개념 수 → 난이도 곡선 | visual/ |

## Tier 3 — 목록 (6개)

| 스킬 | 한 줄 설명 | 스킬 폴더 |
|------|-----------|----------|
| C2. 요약기 | 텍스트를 지정 문장 수로 압축 | writing/ |
| C3. 브릿지-생성기 | 현재→다음 챕터 연결 문장 생성 | writing/ |
| C4. 제목-생성기 | 호기심 유발하는 제목 생성 (교과서 스타일 금지, 기술명 위주) | writing/ |
| C5. 용어-정의기 | 비유→진짜 용어→정식 정의 생성 | writing/ |
| D1. 용어-탐지기 | 비유 없이 등장하는 어려운 전문 용어 탐지 | review/ |
| D2. 톤-검사기 | 대화체/스토리텔링 톤 유지 여부 검사 | writing/ |

---

## STEP ↔ 스킬 매핑

| STEP | 사용 스킬 |
|------|----------|
| 1. 씨앗 | C2 + 인사이트 검토(D6) |
| 2. 코드 해부 | A1, A2, A3, A4 |
| 3. 시나리오+버전 | A5, B1, B2 + 인사이트 검토(B5, D6) |
| 4. 뼈대 | B3, B4, B5, B6, C4, D6 |
| 5. 챕터 집필 | C1, C2, C3, C5, D1, D2, D3, D4, E1 |
| 6. 프롤로그 | C2 |
| 7. 마무리 | C2, C4, D6 |

## 검토 모드 ↔ 참조 스킬

| 검토 모드 | 참조 스킬 |
|----------|----------|
| 인사이트 검토 (STEP 1~5) | A4, B5, B6, D6 |
| 의도감시 검토 (STEP 5) | D1, D4, D5 |
| 감수 검토 (전 STEP) | B5, D2, D6 |

---

## 22개 스킬 전체 매핑

| # | 스킬 | 시리즈 | STEP | 검토 모드 | 폴더 |
|---|------|--------|------|----------|------|
| A1 | 구조-스캐너 | A.코드분석 | 2 | — | code/ |
| A2 | 기능-추출기 | A.코드분석 | 2 | — | code/ |
| A3 | 기술스택-탐지기 | A.코드분석 | 2 | — | code/ |
| A4 | 의존성-매퍼 | A.코드분석 | 2 | 인사이트 | code/ |
| A5 | diff-생성기 | A.코드분석 | 3 | — | code/ |
| B1 | 기능-정렬기 | B.설계 | 3 | — | planning/ |
| B2 | 스냅샷-설계기 | B.설계 | 3 | — | planning/ |
| B3 | 코드-태거 | B.설계 | 4 | — | code/ |
| B4 | 계층-생성기 | B.설계 | 4 | — | code/ |
| B5 | 난이도-곡선기 | B.설계 | 4 | 인사이트, 감수 | visual/ |
| B6 | 갭-분석기 | B.설계 | 4 | 인사이트 | planning/ |
| C1 | 비유-생성기 | C.글쓰기 | 5 | — | writing/ |
| C2 | 요약기 | C.글쓰기 | 1, 5, 6, 7 | — | writing/ |
| C3 | 브릿지-생성기 | C.글쓰기 | 5 | — | writing/ |
| C4 | 제목-생성기 | C.글쓰기 | 4, 7 | — | writing/ |
| C5 | 용어-정의기 | C.글쓰기 | 5 | — | writing/ |
| D1 | 용어-탐지기 | D.검증 | 5 | 의도감시 | review/ |
| D2 | 톤-검사기 | D.검증 | 5 | 감수 | writing/ |
| D3 | 파트-분리-검증기 | D.검증 | 5 | — | review/ |
| D4 | 포맷-검증기 | D.검증 | 5 | 의도감시 | review/ |
| D5 | 의도-대조기 | D.검증 | — | 의도감시 | review/ |
| D6 | 분량-계산기 | D.검증 | 4, 7 | 인사이트, 감수 | planning/ |
| E1 | 이미지-분석기 | E.이미지 | 5 | — | image-analyzer/ |
| F1 | 출판정보-생성기 | F.출판 | 7 | — | pub-info/ |

---

## PM 스킬 (pm-strategist 에이전트 전용, 13개)

외부 설치 스킬 3개에서 파생된 PM 전략 스킬. `pm-strategist` 에이전트가 소유한다.

| # | 스킬 | 시리즈 | 하는 일 | 출처 스킬 |
|---|------|--------|---------|----------|
| PM1 | 비전-설계 | PM.전략 | 제품 비전 + From→To 내러티브 | product-management |
| PM2 | 포지셔닝 | PM.전략 | April Dunford 포지셔닝 | product-management + marketing-strategy-pmm |
| PM3 | 로드맵 | PM.전략 | Outcome 기반 Now/Next/Later | product-management |
| PM4 | 우선순위 | PM.전략 | RICE/ICE 스코어링 + Kill 조건 | product-management |
| PM5 | PMF-측정 | PM.전략 | Sean Ellis 설문 + 리텐션 | product-management |
| F1 | 밸류-래더 | F.퍼널 | 가치 사다리 설계 | funnel-architect |
| F2 | 퍼널-타입 | F.퍼널 | 목적별 퍼널 유형 선택 | funnel-architect |
| F3 | 훅-스토리-오퍼 | F.퍼널 | 전환 카피 프레임워크 | funnel-architect |
| F4 | 트래픽-온도 | F.퍼널 | Cold/Warm/Hot 매칭 | funnel-architect |
| G1 | ICP-정의 | G.GTM | 이상적 고객 프로필 | marketing-strategy-pmm |
| G2 | 경쟁-분석 | G.GTM | 배틀카드 + Win/Loss | marketing-strategy-pmm |
| G3 | 런치-플레이북 | G.GTM | 출시 전/중/후 체크리스트 | marketing-strategy-pmm |
| G4 | 메시징 | G.GTM | 메시징 계층 구조 | marketing-strategy-pmm |

---

## 인쇄소 스킬 (publisher 에이전트 → pub-studio 통합, 6개)

MD→PDF 빌드 + 디자인 프리뷰 + 레이아웃 검증을 처리하는 출판 파이프라인 스킬.

| # | 스킬 | 하는 일 | 폴더 |
|---|------|---------|------|
| P1 | pub-studio | 프리뷰 에디터 + 검증 빌드 통합 (OOP 8모듈) | pub-studio/ |
| P2 | pub-build | MD→Typst→PDF 빌드 파이프라인 | pub-build/ |
| P3 | pub-typst-design | Typst 템플릿 + 컴포넌트 디자인 | pub-typst-design/ |
| P4 | pub-layout-check | PDF 레이아웃 분석 (빈 페이지, 고아줄, 공백) | pub-layout-check/ |
| P5 | pub-page-fit | 레이아웃 자동수정 전략 | pub-page-fit/ |
| P6 | pub-image-optimize | 이미지 공백제거(autocrop) + 크기조절 | pub-image-optimize/ |

### 의존 관계

```
pub-studio (통합)
  ├→ pub-build (빌드 엔진)
  ├→ pub-typst-design (템플릿)
  ├→ pub-layout-check (분석)
  ├→ pub-page-fit (자동수정 전략)
  └→ pub-image-optimize (이미지 최적화)
```
