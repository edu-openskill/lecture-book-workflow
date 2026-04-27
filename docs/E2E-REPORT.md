# E2E 파이프라인 검증 보고서

- 커밋: `509aa17` (book_v5)
- 워크트리: `집필에이전트-v2-e2e-test/`
- 테스트 일시: 2026-03-18

---

## 1. 테스트 요약

| 단계 | 결과 | 비고 |
|------|------|------|
| mermaid_to_d2.py 변환 | PASS | 2개 Mermaid 블록 → 2개 D2 파일 정상 생성 |
| D2 → SVG 컴파일 (ELK) | PASS | `--layout elk --pad 40` 정상 컴파일 |
| SVG → 색상치환 → PNG | PASS | 01_01.png(30K, 465x472), 01_02.png(45K, 1548x668) |
| MD 전처리 | PASS | HTML 주석 제거, `<br>` → `\` 변환 |
| Pandoc (MD → Typst) | PASS | 64줄 Typst 소스 정상 생성 |
| Typst 컴파일 → PDF | PASS | 5페이지, 121KB. `--root` 옵션 필요 |
| 표지 + 목차 | PASS | book_base.typ 자동 생성 |
| 다이어그램 이미지 렌더링 | PASS (시각적 이슈) | 이미지가 PDF에 정상 표시됨. 단, 엣지 누락 문제 |
| 코드블록 구문 하이라이팅 | PASS | Python/bash 키워드 색상 구분 정상 |
| blockquote 스타일 | PASS | 좌측 파란 테두리 + 배경색 |
| 헤더/푸터 | PASS | 좌: 책 제목, 우: 챕터명, 하단: 페이지 번호 |

**전체 판정: CONDITIONAL PASS** — 파이프라인 동작은 정상이나, mermaid_to_d2.py에 2개 버그 존재

---

## 2. 발견된 문제

### BUG-1: 체인 엣지 미지원 (Critical)

**현상**: Mermaid의 체인 화살표 `A --> B --> C`가 첫 번째 엣지(`A -> B`)만 파싱됨

**Mermaid 원본**:
```
Q --> LLM1 --> A1
Q --> R --> DB
DB --> LLM2 --> A2
```

**생성된 D2 (01_01.d2)**: 6개 엣지 중 3개만 생성
```
Q -> LLM1     ← OK
Q -> R         ← OK
DB -> LLM2     ← OK
LLM1 -> A1     ← 누락
R -> DB        ← 누락
LLM2 -> A2     ← 누락
```

**PDF 영향**: p4 다이어그램에서 질문→LLM단독→환각답변, 질문→검색엔진→벡터DB 흐름이 끊어져 보임. 연결이 없는 고립 노드가 발생.

**원인**: `_RE_EDGE` 정규식이 한 줄에서 하나의 엣지만 매칭. `A --> B --> C`에서 `A --> B`만 캐치하고 `B --> C`를 놓침.

**수정 방향**: 엣지 파싱 후 나머지 문자열에서 추가 체인 엣지를 재귀적으로 탐색하거나, 체인 패턴 전용 정규식 추가.

### BUG-2: 크로스 서브그래프 엣지 경로 미완 (Major)

**현상**: 서브그래프 내부 노드 간 크로스 연결에서 fully-qualified 경로가 아닌 단순 ID 사용

**생성된 D2 (01_02.d2)**:
```
C -> E         ← Phase1.C → Phase2.E 여야 함
S -> CTX       ← Phase2.S → Phase3.CTX 여야 함
```

**PDF 영향**: p5 다이어그램 우하단에 C, S, E, CTX 노드가 별도로 생성되어 떠있음. 서브그래프 내부 노드와 연결되지 않고 새 노드가 만들어짐.

**원인**: `generate_d2()`에서 서브그래프 밖의 엣지를 생성할 때, 노드가 어느 서브그래프에 속하는지 역추적하여 `서브그래프ID.노드ID` 형태로 출력하지 않음.

**수정 방향**: 노드→서브그래프 매핑 딕셔너리를 구축하고, 엣지 생성 시 양쪽 노드의 소속을 확인하여 prefix 추가.

### ISSUE-3: 서브그래프 내부 체인 엣지 누락 (Major)

01_02.d2의 Phase1에서:
```
D --> P --> C    ← Mermaid 원본
D -> P            ← D2 (P -> C 누락)
```

Phase3에서:
```
CTX --> LLM --> ANS    ← Mermaid 원본
(모두 누락)              ← D2
```

BUG-1과 동일 원인이지만 서브그래프 내부에서도 발생.

### ISSUE-4: 빌드 스크립트 --root 필요 (Minor)

`typst compile`에 `--root` 옵션이 없으면 상대 경로 이미지 접근이 거부됨.
`build_pdf_typst.py`에서 자동으로 `--root` 설정하는지 확인 필요.

---

## 3. 정상 동작 확인 항목

### README 대조

| README 설명 | 테스트 결과 |
|------------|-----------|
| `python3 mermaid_to_d2.py --extract chapters/XX.md --outdir assets/` | PASS — 2개 블록 추출 + 변환 |
| `d2 --layout elk --pad 40 input.d2 output.svg` | PASS — ELK 레이아웃 꺾인선 |
| `rsvg-convert -d 144 -p 144 output.svg -o output.png` | PASS — 144 DPI PNG |
| sed 색상 치환 (모노톤) | PASS — streaks 패턴 제거 |
| Pandoc (MD → Typst) | PASS |
| Typst 컴파일 → PDF | PASS |
| `--design 1` (프리셋) | 미테스트 — build_pdf_typst.py의 design_assembler 단독 테스트 미실시 |

### 시각적 검증 (PDF 5페이지)

| 페이지 | 요소 | 상태 |
|--------|------|------|
| p1 | 표지 (제목/부제/설명/하단) | 정상 |
| p2 | 자동 목차 (outline) | 정상 |
| p3 | 챕터 오프닝 + blockquote + 이야기 파트 | 정상 |
| p4 | D2 이미지 01_01 + 파트 전환(수평선) + h2 | 정상 (엣지 누락은 데이터 문제) |
| p5 | D2 이미지 01_02 + 코드블록 + 닫기 | 정상 (크로스 연결 문제는 데이터 문제) |

---

## 4. 개선 방향

### 우선순위 HIGH

**H1. 체인 엣지 파싱** (BUG-1 + ISSUE-3 수정)
- `parse_mermaid()`에서 한 줄에 `-->` 가 2개 이상이면 분할하여 여러 엣지로 등록
- 예: `A --> B --> C` → `[("A","B",""), ("B","C","")]`
- 예상 수정 범위: `mermaid_to_d2.py`의 `_RE_EDGE` 및 엣지 파싱 루프

**H2. 크로스 서브그래프 경로** (BUG-2 수정)
- `generate_d2()`에서 서브그래프 밖 엣지 생성 시 노드→서브그래프 매핑 참조
- `node_to_subgraph = {"C": "Phase1", "E": "Phase2", ...}` 딕셔너리 구축
- 엣지 출력: `Phase1.C -> Phase2.E`

**H3. E2E 테스트 자동화 스크립트**
- 현재 수동으로 단계별 실행. `e2e_test.py` 스크립트로 자동화
- 테스트 마크다운 → mermaid_to_d2 → d2 compile → typst compile → PDF 존재 확인
- CI에서 실행 가능하도록 exit code 반환

### 우선순위 MEDIUM

**M1. build_pdf_typst.py 와의 통합 테스트**
- 현재 E2E는 파이프라인 각 단계를 수동 실행. 실제 `build_pdf_typst.py`의 `--chapter`, `--all`, `--design` 옵션 테스트 미실시
- design_assembler 컴포넌트 믹스매치 (`--design "body=2,heading=1"`) 테스트 필요

**M2. auto-image 크기 조절 검증**
- 이미지가 페이지 크기를 초과할 때 자동 축소가 정상 동작하는지 큰 이미지로 테스트
- p3→p4 페이지 넘김에서 auto-image 동작 확인 (현재 이미지가 다음 페이지로 넘어감 — 의도된 동작인지 검증)

**M3. layout-check 자동 루프**
- PDF 빌드 후 `pdf_layout_checker.py`와의 연동 테스트
- 하단 1/3 공백 감지 → image-optimize → rebuild 루프 검증

### 우선순위 LOW

**L1. Mermaid classDef 색상 매핑 정밀화**
- 현재 fill 색상 기반 대략적 매핑. 실제 프로젝트 다이어그램에서 누락되는 케이스 확인
- `style` 속성이 있는 Mermaid 노드에 대한 처리 추가

**L2. D2 노드 크기/폰트 자동 조절**
- 한국어 라벨이 긴 경우 노드가 좁아 텍스트가 잘릴 수 있음
- width/height를 라벨 길이에 비례하여 동적 조절 검토

**L3. Typst --root 자동 감지**
- build_pdf_typst.py에서 프로젝트 루트를 자동 감지하여 `--root` 전달

---

## 5. 테스트 산출물

```
e2e-test/
├── chapters/
│   └── 01-테스트챕터.md        ← 테스트용 Mermaid 포함 마크다운
├── assets/CH01/diagram/
│   ├── 01_01.d2                ← mermaid_to_d2.py 산출물 (LR: LLM vs RAG)
│   ├── 01_02.d2                ← mermaid_to_d2.py 산출물 (TD: RAG pipeline)
│   ├── 01_01.png               ← D2 → SVG → PNG (30K, 465x472)
│   └── 01_02.png               ← D2 → SVG → PNG (45K, 1548x668)
├── book/
│   ├── test-chapter.md         ← 이미지 참조 포함 마크다운
│   ├── test-chapter-preprocessed.md  ← 전처리 결과
│   ├── test-chapter.typ        ← Pandoc 변환 결과
│   ├── test-book-merged.typ    ← 변수 + book_base + 본문 병합
│   ├── book_base.typ           ← 템플릿 복사본
│   └── test-book.pdf           ← 최종 PDF (5페이지, 121KB)
└── E2E-REPORT.md               ← 이 보고서
```

---

## 6. 결론

인쇄소 파이프라인의 핵심 경로(Mermaid→D2→PNG→Typst→PDF)는 **E2E로 정상 동작**합니다. 표지, 목차, 챕터 오프닝, 이미지 렌더링, 코드블록 하이라이팅, blockquote 스타일 모두 출판 품질로 출력됩니다.

단, `mermaid_to_d2.py`의 **체인 엣지 파싱**(H1)과 **크로스 서브그래프 경로**(H2) 2개 버그를 수정해야 변환 결과가 원본 Mermaid와 동일한 흐름을 표현합니다. 이 2개를 수정하면 기존 10개 챕터의 20개 D2 파일도 재변환이 필요합니다.
