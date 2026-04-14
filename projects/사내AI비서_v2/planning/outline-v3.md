# 뼈대 v3 — 통합 흐름 목차

> book_v6 기준. 이야기/기술 파트 분리 제거. 한 섹션 안에서 문제→코드→개념→결과가 자연스럽게 흐른다.

---

## 챕터 템플릿 (v6 확정)

```
1. 챕터 제목 + 오프닝 이미지 (gemini/NN_chapter-opening.png)
2. 챕터 미니맵  — "오늘 만들 것" 3~5개 컴포넌트 박스
3. 목표 박스    — "이번 챕터가 끝나면" 3줄 (괄호로 용어)
4. 준비하기 박스 — 소스 코드 / 실습 환경 / 라이브러리 / 팁 / 실습 순서
5. 본문 섹션 (N.1 ~ N.M) — 통합 흐름
   - 소제목 (h2)
   - 이야기 (캐릭터 대사 · 내면독백 · 비유)
   - 코드블록 (파일경로 + [실습 N] 뱃지)
   - 실행 명령 ([터미널] 뱃지)
   - 실행 결과 이미지 (terminal 캡처) + 캡션
   - 비교 도식 / 파이프라인 (HTML block)
   - 개념 정의 (term 클래스 강조)
   - GEMINI 개념도 (선택)
   - 팁 박스 (선택)
6. 용어 정리   — 비유·진짜용어·정식정의 3열 표
7. 이것만은 기억하자 — 3줄 + 다음 챕터 예고
```

### 커스텀 블록 문법 (마크다운)

```
:::minimap
- 아이콘 | 제목 | 기술명
...
:::

:::goal
- 목표 1
- 목표 2
- 목표 3
:::

:::prep
### 소스 코드 준비
테이블 또는 설명
### 실습 환경 구축
탭 구조 (macOS/Linux | Windows)
### 사용할 라이브러리
표
### 실습 순서
번호 리스트
:::

:::tip
팁 본문
:::

:::result-fail
실패 결과 본문
:::

:::result-ok
성공 결과 본문
:::

:::compare
### 제목
#### BAD | GOOD
- 단계 1 | 단계 1
- 단계 2 | 단계 2
:::

:::rag-pipeline
1. 색인 | 문서 → ChromaDB
2. 검색 | 질문 → 관련 청크
3. 생성 | 질문 + 청크 → LLM
:::
```

### 파일 경로 표기

- 본문: `ex01/step1_fail.py`
- 코드블록 타이틀: `ex01/step1_fail.py — LLM에게 직접 물어보기`
- 터미널 실행: `python step1_fail.py` (cwd 기준 파일명만)

### 코드블록 뱃지

| 종류 | 뱃지 | 색상 |
|-----|------|------|
| Python 실습 | `[실습 N]` | 파란색 |
| 터미널 명령 | `[터미널]` | 초록색 |

OS 구분은 코드블록 타이틀 텍스트로. 예: `— macOS / Linux`, `— Windows`.

### 이미지 경로

- 챕터 오프닝: `assets/CHNN/gemini/NN_chapter-opening.png`
- 개념도: `assets/CHNN/gemini/NN_*.png`
- 터미널 캡처: `assets/CHNN/terminal/NN_*.png`
- 다이어그램: `assets/CHNN/diagram/NN_*.png`

캡션은 이미지 아래 이탤릭. `![](경로)`의 alt 텍스트는 비움.

---

## 10개 챕터 구성

### Ch.1 — AI한테 물어봤더니 거짓말을 합니다
> 환각과 RAG의 첫 만남. **맛보기 챕터**: 스토리 몰입 중심, 깊은 기술 설명은 Ch.4~5에서.

**미니맵**: LLM 단독 호출 → 컨텍스트 주입 → RAG 파이프라인

**목표 3줄**:
- LLM이 **왜 거짓말(환각)**을 하는지 눈으로 확인한다
- 문서를 함께 주는 **컨텍스트 주입**과 그 한계를 이해한다
- **RAG 파이프라인**(색인→검색→생성)을 직접 돌려본다

**섹션**:
- 1.1 그럴듯한 거짓말 — LLM 환각 (`ex01/step1_fail.py`)
- 1.2 교재를 펼쳐놓으면 — 컨텍스트 주입 (`ex01/step2_context.py`)
- 1.3 사서가 필요합니다 — RAG 파이프라인
  - 1.3.1 서가에 책 꽂기 — 임베딩·ChromaDB 인덱싱 (`ex01/step3_rag.py` 1부)
  - 1.3.2 사서에게 질문하기 — RetrievalQA 체인 (`ex01/step3_rag.py` 2부)
- 1.4 청킹, 있을 때와 없을 때 — 청킹 (`ex01/step4_no_chunking.py` vs `step3_rag.py`)
- 1.5 복잡한 질문 던져보기 — Chain-of-Thought 추론 (`ex01/step5_rag.py`)

**실습 파일**: `ex01/step1_fail.py`, `step2_context.py`, `step3_rag.py`, `step4_no_chunking.py`, `step5_rag.py` (5개)

**이미지**:
- gemini: `01_chapter-opening.png`, `01_hallucination-outsider.png`, `01_context-overflow.png`, `01_openbook-exam.png`, `01_journey-roadmap.png`
- diagram: `01_llm-vs-rag.png`
- terminal: `01_step1-hallucination.png`, `01_step2-context.png`, `01_step3-rag.png`, `01_no-chunking-compare.png`, `01_step4-rag.png`

---

### Ch.2 — 일단 사내 시스템부터
> FastAPI + PostgreSQL. 사내 데이터를 API로 노출. RAG 이전에 정형 시스템을 먼저 세운다.

**미니맵**: PostgreSQL · psycopg2 · FastAPI · REST API

**목표 3줄**:
- 사내 직원·연차·매출을 **PostgreSQL**로 구축한다
- **FastAPI**로 CRUD REST API를 만든다
- 대시보드에서 조회할 수 있는 **사내 데이터 허브**를 완성한다

**섹션**:
- 2.1 왜 먼저 정형부터인가 — 비정형만으로는 못 잡는 정보
- 2.2 PostgreSQL 띄우기 — docker-compose (간략)
- 2.3 dataclass로 모델 만들기 — Employee·LeaveBalance·Sale
- 2.4 연결 매니저와 CRUD — Context Manager 패턴
- 2.5 FastAPI로 엔드포인트 내기 — GET/POST
- 2.6 스키마 검증은 Pydantic에게

**실습 파일**: `ex02/app/{main.py, models.py, database.py, crud.py, api.py, schemas.py}`

---

### Ch.3 — 어떤 문서를 넣을까 (이론)
> 코드 없음. 문서 수집·분류 전략. RAG에 들어가기 전 "어떤 문서를, 어떻게 정리할까"를 확정한다.

**미니맵**: PDF · Word · Excel · HWP · 메타데이터 · 폴더 규칙

**목표 3줄**:
- 사내 문서 **4가지 형식**(PDF·Word·Excel·HWP)의 특징과 파싱 고려사항을 안다
- **메타데이터 표준**과 폴더 구조 규칙을 정의한다
- **재인덱싱 전략**(변경 감지·증분 빌드)을 설계한다

**섹션**:
- 3.1 형식별 특징 — PDF·DOCX·XLSX·HWP 장단
- 3.2 메타데이터 표준 — 부서·분류·버전·발행일
- 3.3 폴더 규칙 — HR/Finance/Ops/Security
- 3.4 재인덱싱 전략 — 타임스탬프 비교·증분 빌드

**실습 파일**: 없음 (이론 챕터)

---

### Ch.4 — 문서를 지식으로 바꾸다
> 파싱 → 청킹 → 임베딩 → ChromaDB 인덱싱. 오프라인 파이프라인의 본체.

**미니맵**: Extractor · Chunker · Embedder · ChromaDB

**목표 3줄**:
- PDF·DOCX·XLSX를 **통합 파서**로 마크다운 변환한다
- **Fixed-size 청킹**(500자+100오버랩)과 문서 구조 보존을 이해한다
- **ko-sroberta 임베딩**으로 ChromaDB에 저장하고 CLI로 검색한다

**섹션**:
- 4.1 extractor 한 입구로 — 형식별 라우팅
- 4.2 PDF 파싱의 함정 — pypdf 한계와 우회
- 4.3 DOCX/XLSX 변환 — 구조 보존하며 마크다운으로
- 4.4 청킹 사이즈 선택 — 500/1000/2000 비교
- 4.5 임베딩과 저장 — ko-sroberta + ChromaDB
- 4.6 CLI로 검색해보기 — 유사도 점수 시각화

**실습 파일**: `ex04/src/{main.py, extractor.py, extract_pdf.py, extract_docx.py, extract_xlsx.py, chunker.py, store.py, cli_search.py}`

---

### Ch.5 — 드디어 답해준다
> RAG QA 엔진. LCEL 체인으로 Retriever→Prompt→LLM→Parser를 조립.

**미니맵**: Retriever · Prompt · LLM · Parser · WindowMemory

**목표 3줄**:
- **LCEL 체인**으로 Retriever|Prompt|LLM|Parser를 조립한다
- **답변에서 출처를 추출**하여 독자에게 근거를 제시한다
- **멀티턴 대화**(최근 5턴 WindowMemory)를 붙인다

**섹션**:
- 5.1 LCEL이라는 파이프라인 언어 — `|` 연산자로 조립
- 5.2 검색기 연결 — ChromaDB Retriever
- 5.3 프롬프트 설계 — "문서 기반으로만 답해주세요"
- 5.4 답변 파싱과 출처 추출 — response_parser
- 5.5 멀티턴 대화 — WindowMemory 5턴
- 5.6 FastAPI에 얹기 — POST /api/chat

**실습 파일**: `ex05/src/{rag_chain.py, response_parser.py, conversation.py}`, `ex05/app/{main.py, chat_api.py, session.py}`

---

### Ch.6 — 연차도, 규정도, 한번에
> RAG만으로 부족한 정형 질문. ReAct 패턴 에이전트로 MCP Tools까지 통합.

**미니맵**: Query Router · MCP Tools · LCEL Agent Chain (ReAct)

**목표 3줄**:
- **3단계 Query Router**(규칙→스키마→LLM)로 질문 유형을 분류한다
- **MCP Tools**(@tool 4개)로 DB 조회 함수를 에이전트에 연결한다
- **ReAct 패턴**으로 Agent Chain이 도구를 스스로 선택하게 만든다

**섹션**:
- 6.1 RAG만으론 부족하다 — "내 연차 며칠 남았어?"
- 6.2 Query Router 3단계 — 규칙·스키마·LLM
- 6.3 MCP Tools 만들기 — `@tool` 데코레이터
- 6.4 ReAct 패턴 — Think·Act·Observe 루프
- 6.5 에이전트 조립 — `create_tool_calling_agent`
- 6.6 18개 시나리오로 검증하기

**실습 파일**: `ex06/src/{router.py, mcp_tools.py, agent.py}`, `ex06/app/{main.py, chat_api.py, database.py}`, `ex06/tests/test_scenarios.py`

---

### Ch.7 — 실제로 써보니
> 배포 후 실사용자 피드백. 속도·비용 문제. 캐시·토큰 관리로 잡는다.

**미니마맵**: ResponseCache · TokenTracker · 로깅

**목표 3줄**:
- **ResponseCache**로 동일 질문 반복 비용을 줄인다
- **TokenTracker**로 사용량·비용을 모니터링한다
- **구조적 로깅**으로 실사용 패턴을 관찰한다

**섹션**:
- 7.1 써보니 문제가 보인다 — 동료의 불만
- 7.2 ResponseCache — 질문→답변 캐시
- 7.3 TokenTracker — 호출당 토큰/비용 집계
- 7.4 로깅 패턴 — 구조화된 JSON 로그
- 7.5 미니 대시보드 — 일간 사용량 · 캐시 적중률

**실습 파일**: `ex07/src/{cache.py, token_tracker.py, logger.py}`, `ex07/app/*`

---

### Ch.8 — 엉뚱한 문서를 가져온다
> 튜닝 서사 1막. 검색 품질 튜닝: 청킹·리랭커·하이브리드 검색.

**미니맵**: Chunk Strategy · Reranker · Hybrid Search (BM25+Dense)

**목표 3줄**:
- **청킹 전략**(사이즈·오버랩·구조 기반)을 비교 실험한다
- **리랭커**(Cross-Encoder)로 Top-K 재정렬의 효과를 확인한다
- **하이브리드 검색**(BM25+Dense)으로 검색 적중률을 높인다

**섹션**:
- 8.1 잘못된 문서를 가져왔다 — 오답 케이스 분석
- 8.2 청킹 사이즈 실험 — 500/1000/2000
- 8.3 오버랩의 역할 — 100/200/300
- 8.4 리랭커 투입 — BGE-reranker
- 8.5 하이브리드 검색 — BM25 + Dense 랭크 퓨전

**실습 파일**: `ex08/src/{chunk_experiment.py, reranker.py, hybrid_search.py}`

---

### Ch.9 — 질문을 제대로 이해 못한다
> 튜닝 서사 2막. 쿼리 전처리: 쿼리 재작성·확장·의도 분류.

**미니맵**: Query Rewriter · Query Expander · Intent Classifier

**목표 3줄**:
- **쿼리 재작성**으로 모호한 질문을 명확한 검색 쿼리로 바꾼다
- **쿼리 확장**(HyDE·동의어)으로 재현율을 높인다
- **의도 분류**로 검색 경로를 분기한다

**섹션**:
- 9.1 뉘앙스가 날아간다 — "저번달 매출 좀"
- 9.2 쿼리 재작성 — LLM에게 정형화 맡기기
- 9.3 HyDE — 가상 답변 생성 후 임베딩
- 9.4 동의어 확장 — 사내 용어 사전
- 9.5 의도 분류 — FAQ·검색·계산 분기

**실습 파일**: `ex09/src/{query_rewriter.py, hyde.py, synonym_expander.py, intent_classifier.py}`

---

### Ch.10 — PDF 이미지까지 잡아라
> 튜닝 서사 3막. 멀티모달 RAG: 이미지·표·도식을 VLM으로 처리.

**미니맵**: PDF Image Extractor · VLM (Vision Language Model) · Image Embedding

**목표 3줄**:
- **PDF에서 이미지·표·도식**을 추출한다
- **VLM**(LLaVA 등)으로 이미지를 설명문으로 변환해 벡터화한다
- **멀티모달 검색**으로 "이 도표 어디 나왔지?" 같은 질문을 해결한다

**섹션**:
- 10.1 "규정 그림표에 답 있는데요" — 텍스트 RAG의 마지막 허들
- 10.2 PDF 이미지 추출 — PyMuPDF
- 10.3 VLM으로 캡셔닝 — LLaVA·Llama-Vision
- 10.4 이미지 설명문을 벡터화 — 텍스트 인덱스 재활용
- 10.5 멀티모달 검색 체인 — 이미지+텍스트 통합

**실습 파일**: `ex10/src/{pdf_image_extractor.py, vlm_captioner.py, multimodal_chain.py}`

---

## 실습 파일 번호 규칙

- **섹션 N.X와 실습 파일명의 숫자가 일치**한다 (예: 1.4 → `step4_*.py`)
- 섹션 하위(1.3.1, 1.3.2) 같은 경우 같은 파일의 1부/2부로 나눠 설명
- 파일명 형식: `stepN_<이름>.py` 또는 `stepN_<이름>_<변형>.py`

---

## book_v5 대비 변경점

| 변경 | 이유 |
|-----|------|
| 이야기/기술 파트 분리 제거 | 독자가 같은 내용을 두 번 읽는 느낌 제거 |
| 챕터 미니맵 추가 | 전체 숲은 서문에, 챕터 상단엔 "오늘 만들 것"만 |
| 목표 박스 추가 | 챕터가 끝나면 뭐가 되는지 한 박스로 |
| 파일명 vs 섹션번호 일치 | `step3_rag_no_chunking` → `step4_no_chunking` (1.4 대응) |
| 오프닝에 캐릭터/내면독백 우선 | 설명문 시작 금지 |
| 2단계 뱃지 통일 | "bash" → "터미널"로 Windows 독자 혼동 제거 |
