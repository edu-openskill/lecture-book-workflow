# D2 다이어그램 빌드 스킬

model: claude-sonnet-4-6
user_invocable: true
trigger: ["D2 빌드", "다이어그램 생성", "/d2"]

## 하는 일

D2 언어로 다이어그램을 작성하고, O'Reilly 모노톤 스타일로 PNG를 생성합니다.

## 디자인 규칙

### 색상 (3종류만 사용)

| 스타일 | fill | stroke | 용도 |
|--------|------|--------|------|
| **진한 회색** | `#f0f0f0` | black | 입력/시작점 (질문, 문서, 사용자) |
| **화이트** | `white` | black | 처리/결과 노드 (LLM, 에이전트, 변환, 답변) |
| **점선** | `white` | black + stroke-dash: 4 | 문제/불확실 (환각, 오류) |

### 특수 노드

| 노드 | shape | fill | 용도 |
|------|-------|------|------|
| DB | cylinder | `#eeeeee` | 데이터베이스 |
| 분기점 | diamond | white | 라우터, 파서 선택 |
| 핵심 분기 | hexagon | white + stroke-width: 2 | QueryRouter 등 중요 분기만 |
| 컨테이너 | rectangle | transparent + stroke-dash: 5 | Phase, 그룹 |

### 공통 스타일

- `border-radius: 8` — 모든 사각형 노드
- `direction: right` — 가로 흐름 기본 (세로 금지)
- 화살표 색상: `style.stroke: "#222222"` (인라인 지정)
- 레이아웃: ELK (`--layout elk`)

### 01번 전용 (classes 시스템)

```d2
classes: {
  phase: { shape: rectangle; style: { fill: transparent; stroke: black; stroke-width: 2; border-radius: 8; stroke-dash: 5; font-size: 16 } }
  question: { shape: rectangle; style: { fill: "#f0f0f0"; stroke: black; stroke-width: 1; border-radius: 8; font-size: 14 } }
  llm: { shape: hexagon; style: { fill: white; stroke: black; stroke-width: 2; font-size: 15; shadow: true } }
  hallucination: { shape: rectangle; style: { fill: white; stroke: black; stroke-width: 1; border-radius: 8; stroke-dash: 4 } }
  orchestrator: { shape: rectangle; style: { fill: white; stroke: black; stroke-width: 1; border-radius: 8 } }
  retriever: { shape: rectangle; style: { fill: white; stroke: black; stroke-width: 1; border-radius: 8 } }
  db: { shape: rectangle; style: { fill: "#eeeeee"; stroke: black; stroke-width: 1; border-radius: 8 } }
  answer: { shape: rectangle; style: { fill: white; stroke: black; stroke-width: 2; border-radius: 8 } }
}
```

## 빌드 파이프라인

D2 → SVG → 색상 치환(흑백) → PNG

```bash
# 1. D2 → SVG (ELK 레이아웃, 테마 없음)
d2 --layout elk --pad 40 input.d2 output.svg

# 2. 테마 잔여 색상 → 흑백 치환
sed -e 's/#0D32B2/#222222/g' \
    -e 's/#F7F8FE/#FFFFFF/g' \
    -e 's/#EDF0FD/#FFFFFF/g' \
    -e 's/#E3E9FD/#FFFFFF/g' \
    -e 's/#EEF1F8/#FFFFFF/g' \
    -e 's/fill:url(#streaks-bright[^)]*)/fill:#FFFFFF/g' \
    -e 's/fill:url(#streaks-darker[^)]*)/fill:#FFFFFF/g' \
    -e 's/fill:url(#streaks-normal[^)]*)/fill:#FFFFFF/g' \
    -e 's/fill:url(#streaks-dark[^)]*)/fill:#FFFFFF/g' \
    output.svg > output_mono.svg

# 3. SVG → PNG (144 DPI)
rsvg-convert -d 144 -p 144 output_mono.svg -o output.png

# 4. 정리
rm output.svg output_mono.svg
```

## Mermaid → D2 변환

기존 챕터의 Mermaid 다이어그램을 D2로 자동 변환한다.

```bash
# 단일 .mmd 파일 변환
python3 mermaid_to_d2.py input.mmd output.d2

# 마크다운에서 Mermaid 블록 추출 + 일괄 변환
python3 mermaid_to_d2.py --extract chapters/01-시작.md --outdir assets/CH01/diagram/
```

- 프로젝트 classes 템플릿 자동 적용 (start-end, process, danger, success, storage, decision, step, group-box)
- Mermaid classDef → D2 class 자동 매핑 (fill 색상 기반)
- subgraph → D2 group-box 블록 변환
- 변환 후 수동 검수 필수 (노드 크기, 레이아웃 조정)

스크립트: `references/scripts/mermaid_to_d2.py`

## 꺾인선 라우팅

`--layout elk` 사용 시 자동으로 직각 꺾인선(orthogonal) 라우팅이 적용된다.
기본 레이아웃(`dagre`)은 곡선을 생성하므로 반드시 `--layout elk`을 사용한다.

## 일괄 빌드

```bash
cd projects/사내AI비서_v2/assets/diagrams
./build_diagrams.sh
```

## 의존성

| 도구 | 설치 | 용도 |
|------|------|------|
| d2 | `brew install d2` | D2 → SVG 컴파일 |
| rsvg-convert | `brew install librsvg` | SVG → PNG 변환 |

## 다이어그램 목록

| 파일 | 챕터 | 내용 |
|------|------|------|
| 01_rag-comparison | CH01 | LLM 단독 vs RAG 비교 |
| 02_api-restaurant | CH02 | API = 웨이터 비유 |
| 03_parser-pipeline | CH03 | 파서 → 청킹 → 벡터DB |
| 04_parser-dispatch | CH04 | 확장자별 파서 분기 |
| 05_rag-qa-flow | CH05 | RAG Q&A 흐름 |
| 05_lcel-pipeline | CH05 | LCEL 파이프 연결 |
| 06_tool-vs-mcp | CH06 | @tool vs MCP 비교 |
| 06_agent-architecture | CH06 | QueryRouter + ReAct |
| 06_sequence-crud | CH06 | CRUD 시퀀스 |
| 09_ch08-vs-ch09 | CH09 | 검색 전/중/후 비교 |
| 09_sequence-pipeline | CH09 | 전체 파이프라인 시퀀스 |
