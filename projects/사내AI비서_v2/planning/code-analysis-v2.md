# 코드 분석 v2

> v1(CH01~08, 2026-01) → v2(CH01~10, 2026-04) 갱신. rag-end/ 구조로 리팩터링 반영, CH08 11개 실험을 CH08·CH09·CH10 세 챕터로 분리, Vision LLM/OCR/RAG 평가 추가.

## 완성 코드 정보
- **경로**: `projects/사내AI비서_v2/code/rag-end/ex01~ex10/`
- **언어/프레임워크**: Python 3.12 / FastAPI + LangChain 0.3.x + Ollama + ChromaDB + PostgreSQL
- **챕터**: CH01~CH10 (11개, CH03은 개념 챕터라 코드 없음)
- **원칙**: **각 ex는 독립 실행 가능**. 이전 챕터 코드를 직접 import하지 않고 구조·패턴만 승계

---

## 전체 구조

```
code/rag-end/
├── ex01/   RAG 첫 만남 (개념 증명)
│   ├── step1_fail.py / step2_context.py / step3_rag.py
│   └── requirements.txt  (langchain 0.3.x, chromadb)
│
├── ex02/   FastAPI + PostgreSQL CRUD
│   ├── app/{main,api,crud,database,models,schemas}.py
│   ├── docker-compose.yml  (container_name: metacoding_db — 최초 명명)
│   └── requirements.txt
│
├── ex04/   VectorDB 구축 (텍스트 PDF)
│   ├── src/{main,extractor,chunker,store,cli_search}.py
│   ├── data/docs/{hr,ops,finance}/*.pdf  (원본 텍스트 PDF)
│   └── data/chroma_db/  (빌드 후 생성)
│
├── ex05/   LCEL RAG Q&A 엔진
│   ├── src/{rag_chain,response_parser,conversation,vectorstore}.py
│   ├── app/{main,chat_api,session}.py
│   ├── data/docs/  (ex04와 동일 3개 PDF)
│   └── 특징: langchain-chroma wrapper 사용 (LCEL 체인 연결용)
│
├── ex06/   통합 에이전트 (Tool Calling + ReAct)
│   ├── src/{router,mcp_tools,agent,db_helper}.py
│   ├── app/{main,chat_api,database}.py
│   ├── tests/test_scenarios.py  (18 시나리오)
│   ├── docker-compose.yml  (container_name: ex06_postgres)
│   └── 특징: chromadb raw 사용 (tool 내부에서 직접 query)
│
├── ex07/   캐시·로깅·옵저버빌리티
│   ├── src/{agent_config,cache,monitoring,_agent_utils,agent_helpers}.py
│   ├── src/tools/{leave_balance,sales_sum,list_employees,search_documents}.py
│   ├── app/ (FastAPI + 채팅 UI)
│   ├── data/chroma_db/  (사전 빌드 동봉)
│   ├── docker-compose.yml  (container_name: ex07_postgres)
│   └── 특징: ex06 구조 재구현 + ResponseCache + TokenTracker + Langfuse 훅
│
├── ex08/   RAG 튜닝 — 검색 개선
│   ├── tuning/step1_chunk_experiment/  (Fixed vs Semantic)
│   ├── tuning/step2_reranker/          (Cross-Encoder)
│   ├── tuning/step3_hybrid_search/     (BM25 + Vector)
│   ├── data/markdown/  (파싱 결과 6개 md)
│   ├── data/test_questions.json  (30 평가 질문)
│   ├── data/schema.sql
│   ├── docker-compose.yml  (container_name: ex08_postgres)
│   └── 특징: 서빙 없음. 튜닝 실습만. 파싱 스킵(md 제공)
│
├── ex09/   RAG 튜닝 — 질의 변환 · 고급 검색기
│   ├── tuning/step1_query_rewrite/  (HyDE, Multi-Query, 약어)
│   ├── tuning/step2_advanced_retriever/  (Parent Doc, Self-Query)
│   ├── (data/ 폴더 없음 — `data.py`에 하드코딩된 딕셔너리·문서)
│   └── 특징: 서빙 없음. 파일 I/O 없음. 순수 실험
│
└── ex10/   PDF 이미지 + Vision LLM + RAG 평가
    ├── app/ (FastAPI + 채팅 UI, ex07 계승)
    ├── src/tools/search_documents.py (chromadb raw)
    ├── tuning/step1_document_parser/ (OCR vs Vision)
    ├── tuning/step2_hybrid_parser/   (pypdf → Vision 폴백)
    ├── tuning/step3_eval_framework/  (Precision@k, Hallucination)
    ├── data/docs/hr/HR_*.pdf  (스캔 변환본 — generate_real_pdfs.py로 이미지화)
    ├── data/docs/hr/HR_취업규칙_원본.pdf  (텍스트 PDF, ex04 원본 복사)
    └── 특징: CH10 교육 목적으로 원본 PDF를 일부러 스캔본으로 가공
```

---

## 챕터 간 재사용 원칙

> **핵심**: 각 ex는 **독립 실행 가능한 완전한 프로젝트**로 설계됨. 이전 챕터 코드를 `from ex06.src... import`로 직접 가져오지 않고, **구조와 패턴을 학습해 새 요구사항에 맞게 재구현**한다.

### 재사용 매트릭스

| 관계 | 방식 | 예시 |
|------|------|------|
| ex05 → ex06 | **구조 전환** (함수 체인 → 클래스 에이전트) | LCEL `build_rag_chain()` → `IntegratedAgent` 클래스 |
| ex06 → ex07 | **구조 승계 + 기능 추가** | `IntegratedAgent` → `ConnectHRAgent` (캐시·모니터링 추가) |
| ex07 → ex10 | **UI·파이프라인 승계 + PDF 레이어 추가** | ex07 app/ 구조 그대로, tuning/ 추가 |
| ex08·ex09 | **서빙 없는 독립 실습** | tuning/ 하위에 실험만. app/ 없음 |

### 왜 직접 import하지 않나?
1. **교육적 이유** — 각 챕터를 읽는 독자가 이전 챕터를 실행 안 해도 완결된 코드를 볼 수 있음
2. **버전 진화 시연** — 같은 문제를 다른 각도(함수→클래스→기능 추가)로 푸는 과정이 학습 효과
3. **복붙 아니라 성장** — ex06의 router.py를 ex07이 수정 없이 가져오면 "왜 이 파일이 필요한지"가 흐려짐

---

## 벡터 DB 연결 패턴

두 가지 접근이 공존. **챕터 목적에 따라 구분**.

| 챕터 | 라이브러리 | 이유 |
|------|-----------|------|
| ex01 | `langchain-chroma` | RAG 개념 증명 — 짧은 체인이 전부 |
| ex04 | `chromadb` | 순수 임베딩·저장에 집중, LCEL 체인 없음 |
| ex05 | `langchain-chroma` | LCEL 파이프라인(`retriever \| prompt \| llm`) 연결 |
| ex06 | `chromadb` raw | Tool 내부에서 단순 쿼리만. wrapper 불필요 |
| ex07 | `chromadb` raw + langchain-chroma 폴백 | ex06 계승, 필요 시 wrapper로 전환 가능 |
| ex08 | `chromadb` | 튜닝 실험에 직접 제어 필요 (BM25 병행 등) |
| ex10 | `chromadb` raw | Tool 내부 사용. ex07 패턴 유지 |

> **통일 정책**: `requirements.txt`에는 **두 라이브러리 모두 설치**하되, 실제 import는 챕터별 목적에 맞춤. 독자는 어떤 챕터든 pip install 한 번으로 끝.

---

## 핵심 기능 목록 (의도 안)

| # | 기능 | 챕터 | 관련 코드 | 주요 기술 |
|---|------|------|----------|----------|
| 1 | LLM 환각 체험 | CH01 | ex01/step1_fail.py | ChatOllama, deepseek-r1:8b |
| 2 | Context Injection | CH01 | ex01/step2_context.py | f-string 프롬프트 |
| 3 | RAG 기본 파이프라인 | CH01 | ex01/step3_rag.py | RetrievalQA, Chroma |
| 4 | 청킹 효과 비교 | CH01 | ex01/step3_rag_no_chunking.py | - |
| 5 | 데이터 모델 | CH02 | ex02/app/models.py | dataclass |
| 6 | CRUD + FastAPI | CH02 | ex02/app/{crud,api}.py | psycopg2, Router |
| 7 | 문서 수집 전략 | CH03 | (개념) | - |
| 8 | 문서 파싱 | CH04 | ex04/src/extractor.py | pypdf, python-docx, openpyxl |
| 9 | Fixed 청킹 | CH04 | ex04/src/chunker.py | 500자 + 100자 오버랩 |
| 10 | 한국어 임베딩·저장 | CH04 | ex04/src/store.py | ko-sroberta-multitask → Chroma |
| 11 | CLI 검색 | CH04 | ex04/src/cli_search.py | 유사도 시각화 |
| 12 | LCEL RAG 파이프라인 | CH05 | ex05/src/rag_chain.py | Retriever\|Prompt\|LLM\|Parser |
| 13 | 멀티턴 대화 | CH05 | ex05/src/conversation.py | WindowMemory(k=5) |
| 14 | 채팅 API | CH05 | ex05/app/chat_api.py | POST /api/chat + 세션 |
| 15 | 3단계 QueryRouter | CH06 | ex06/src/router.py | 규칙 → 스키마 → LLM |
| 16 | MCP 도구 4개 | CH06 | ex06/src/mcp_tools.py | @tool 4종 |
| 17 | ReAct Agent | CH06 | ex06/src/agent.py | create_tool_calling_agent |
| 18 | Agent 표준 구성 | CH07 | ex07/src/agent_config.py | ConnectHRAgent |
| 19 | 응답 캐시 | CH07 | ex07/src/cache.py | ResponseCache(TTL) + EmbeddingCache |
| 20 | 토큰 추적 | CH07 | ex07/src/monitoring.py | TokenTracker + Langfuse 훅 |
| 21 | 청킹 실험 | CH08 | ex08/tuning/step1_chunk_experiment/ | Fixed vs Semantic |
| 22 | 리랭커 | CH08 | ex08/tuning/step2_reranker/ | Cross-Encoder |
| 23 | 하이브리드 검색 | CH08 | ex08/tuning/step3_hybrid_search/ | BM25 + Vector |
| 24 | 쿼리 변환 | CH09 | ex09/tuning/step1_query_rewrite/ | HyDE, Multi-Query, 약어 |
| 25 | 고급 Retriever | CH09 | ex09/tuning/step2_advanced_retriever/ | Parent Doc, Self-Query |
| 26 | OCR 파싱 | CH10 | ex10/tuning/step1_document_parser/ocr.py | EasyOCR |
| 27 | Vision LLM 파싱 | CH10 | ex10/tuning/step1_document_parser/vision.py | minicpm-v/qwen2.5vl |
| 28 | 하이브리드 파서 | CH10 | ex10/tuning/step2_hybrid_parser/ | pypdf → Vision (text 있으면 text_layer) |
| 29 | RAG 평가 프레임워크 | CH10 | ex10/tuning/step3_eval_framework/ | Precision@k, Recall, Hallucination |

---

## 의도 밖 기능 (제외)

| 기능 | 관련 코드 | 제외 이유 |
|------|----------|----------|
| Admin UI (Jinja2+CSS) | ex02 views.py, templates/ | 프론트엔드 제외 |
| 채팅 UI 스타일링 | ex05~07, ex10 templates/static/ | 프론트엔드 제외 |
| Docker/Postgres 심화 | docker-compose.yml | 간략 안내만 |
| Langfuse 연동 상세 | ex07 monitoring.py 일부 | 존재만 언급 |
| RAGAS 자동 평가 | ex08 eval 일부 | "더 알아보기" 수준 |
| 문서 캡처·이미지 근거 | 초기 계획에 있었으나 삭제 | 범위 초과 |

---

## 기술 스택 (v2 기준)

### 핵심 (의도 안)

| 계층 | 기술 | 버전 | 역할 | 챕터 |
|------|------|------|------|------|
| LLM (Q&A·추론) | Ollama `deepseek-r1:8b` | — | CH05에서만 | CH05 |
| LLM (Tool Calling) | Ollama `llama3.1:8b` | — | CH06~ 기본 | CH06~10 |
| LLM (Vision) | Ollama `minicpm-v:latest` | — | 기본 권장 | CH10 |
| LLM (Vision 대안) | `qwen2.5vl:7b`, `llama3.2-vision:11b` | — | 품질 우선 옵션 | CH10 |
| LLM (클라우드) | OpenAI `gpt-4o-mini` | — | Vision + Tool Calling + JSON 모두 지원 | CH05~10 |
| 프레임워크 | LangChain | 0.3.x | RAG/Agent | CH01~10 |
| 벡터 DB | ChromaDB | 1.5.1 | 임베딩 저장/검색 | CH01, CH04~10 |
| 벡터 DB wrapper | langchain-chroma | 0.2.6 | LCEL 연결용 | CH05 |
| 임베딩 | ko-sroberta-multitask | — | 한국어 768d | CH04~10 |
| 웹 | FastAPI | 0.115.x | REST + 채팅 UI | CH02, CH05~07, CH10 |
| DB | PostgreSQL | 16 | 정형 데이터 | CH02, CH06~08, CH10 |
| DB 드라이버 | psycopg2-binary | 2.9.10 | SQL 직접 | 동상 |
| 검증 | Pydantic | 2.10.x | 스키마 | CH02, CH05~10 |
| 문서 파싱 (텍스트) | pypdf, python-docx, openpyxl | — | CH04 기본 | CH04~07 |
| 문서 파싱 (스캔) | PyMuPDF(fitz), Pillow | 1.24 / 10.4 | 페이지 렌더링 | CH10 |
| OCR | EasyOCR | 1.7.2 | 한국어+영어 | CH10 |
| 키워드 검색 | rank-bm25 | 0.2.2 | Hybrid Search | CH08 |
| 리랭커 | Cross-Encoder (sentence-transformers 내장) | — | 재정렬 | CH08 |
| 고급 Retriever | langchain-experimental | 0.3.4 | Semantic Chunking | CH08 |
| Vision 호출 | httpx | 0.28.x | Ollama API | CH10 |
| 콘솔 출력 | rich | 13.9.x | Table/Panel | CH07~10 |

### 간략/제외 (의도 밖)

| 기술 | 역할 | 수준 |
|------|------|------|
| Docker Compose | PostgreSQL 컨테이너 | 간략 (up/down만) |
| Jinja2 | HTML 템플릿 | 존재 언급 |
| Langfuse | LLM 모니터링 | 훅만 |
| RAGAS | RAG 자동 평가 | 더 알아보기 |

---

## Python / OS / 실행 환경

| 항목 | 값 |
|------|-----|
| Python | **3.12 고정** (모든 챕터 실습 코드에 `python3.12` 박혀 있음) |
| OS | macOS, Linux, Windows 10+ |
| 가상환경 | 챕터별 `.venv` (독립 실행 원칙) |
| 의존성 관리 | pip (uv는 선택 사항, 책에는 미포함) |
| LLM 런타임 | Ollama (로컬) 또는 OpenAI API |

---

## 챕터 간 코드 진화 흐름

```
CH01 (ex01): LLM 단독 → Context Injection → RAG (개념 증명)
  ↓
CH02 (ex02): FastAPI + PostgreSQL CRUD (정형 기반)
  ↓
CH03 (없음):  사내 문서 수집 전략 (개념만)
  ↓
CH04 (ex04): 파싱 → 청킹 → 임베딩 → ChromaDB (비정형 기반)
  ↓
CH05 (ex05): LCEL RAG 파이프라인 + 멀티턴 (QA 엔진)
  ↓
CH06 (ex06): Tool Calling + ReAct Agent (정형+비정형 통합)
  ↓
CH07 (ex07): Agent 표준화 + 캐시 + 로깅 (운영 안정화)
  ↓
CH08 (ex08): 검색 튜닝 — Chunking · Reranker · Hybrid
  ↓
CH09 (ex09): 질의 변환 — HyDE · Multi-Query · Parent Doc
  ↓
CH10 (ex10): 이미지 문서 — OCR · Vision LLM · RAG 평가
```

---

## 기획서 매핑 (갱신)

| 코드 챕터 | 기획서 PART | 비고 |
|---------|----------|------|
| CH01 | — | 기획서에 없음. LLM 환각 체험으로 도입 |
| CH02 | PART 1 | FastAPI CRUD |
| CH03 | PART 2 | 문서 수집 전략 (개념) |
| CH04 | PART 3 | VectorDB 구축 |
| CH05 | PART 4 | RAG Q&A 엔진 |
| CH06 | PART 5 | 통합 에이전트 |
| CH07 | PART 6 | LangChain 연결 |
| CH08 | PART 7 (쪼갬 1/3) | 검색 튜닝 |
| CH09 | PART 7 (쪼갬 2/3) | 질의 변환 |
| CH10 | PART 7 (쪼갬 3/3) | 이미지 문서 + 평가 |
| — | PART 8 | 배포/운영 → 제외 |

---

## 점검 이력

- **v1 (2026-01)**: CH01~08, 11개 튜닝 실험을 CH08 한 챕터에 몰아넣은 초안
- **v2 (2026-04)**: CH08·CH09·CH10로 분할. ex01~ex10 rag-end/ 구조로 리팩터링. Vision LLM/OCR/평가 추가. chromadb vs langchain-chroma 사용 패턴 명시. Python 3.12 명시. OPENAI_MODEL 전부 gpt-4o-mini로 통일. container_name 규칙 통일(ex0N_postgres)
