# 코드 분석 v3

> v2(CH01~10, 2026-04) → v3(CH01~11, 2026-04) 갱신. CH11(ex11) "커넥트HR 에이전트 완성" 추가. 전 챕터 `requirements.txt` **버전 잠금 통일**. ex11에 레이어드 아키텍처 + 자식·부모 분리 인덱싱 + 챕터 10 하이브리드 파서 이식 + CH09 `ParentDocumentRetriever` 원본 복원 반영.

## 완성 코드 정보
- **경로**: `projects/사내AI비서_v2/code/rag-end/ex01~ex11/`
- **언어/프레임워크**: Python 3.12 / FastAPI + LangChain 0.3.21 + Ollama + ChromaDB + PostgreSQL
- **챕터**: CH01~CH11 (12개, CH03은 개념 챕터라 코드 없음)
- **원칙**: **각 ex는 독립 실행 가능**. 이전 챕터 코드를 직접 import하지 않고 구조·패턴을 복사·이식

---

## 전체 구조 (ex11 추가)

```
code/rag-end/
├── ex01/   RAG 첫 만남 (개념 증명)
├── ex02/   FastAPI + PostgreSQL CRUD
├── ex04/   VectorDB 구축 (텍스트 PDF)
├── ex05/   LCEL RAG Q&A 엔진
├── ex06/   통합 에이전트 (Tool Calling + ReAct)
├── ex07/   캐시·로깅·옵저버빌리티
├── ex08/   RAG 튜닝 — 검색 개선 (Chunking · Reranker · Hybrid)
├── ex09/   RAG 튜닝 — 질의 변환 (HyDE · Multi-Query · Parent Doc)
├── ex10/   PDF 이미지 + Vision LLM + RAG 평가
└── ex11/   커넥트HR 에이전트 완성 — 파이프라인 조립 + 근거 이미지
    ├── app/ (FastAPI + 채팅 UI, ex07 계승)
    ├── src/
    │   ├── pipeline.py              # Application: RagPipeline
    │   ├── evidence.py / evidence_capture.py  # 근거(정형 JSON · 비정형 PNG)
    │   ├── tuning/                  # Domain: 챕터 8·9·10 튜닝 원본 이식
    │   │   ├── query_expander.py    # CH09 약어 확장
    │   │   ├── bm25_retriever.py    # CH08 BM25 (rank-bm25)
    │   │   ├── ensemble_retriever.py# CH08 BM25 + ChromaDB 하이브리드
    │   │   ├── reranker.py          # CH08 CrossEncoderReranker 원본
    │   │   ├── parent_doc.py        # CH09 ParentDocumentRetriever 원본
    │   │   └── hybrid_parser.py     # CH10 pypdf → Vision 폴백
    │   └── tools/search_documents.py  # 자식·부모 분리 인덱싱
    ├── data/docs/                   # 실제 인덱싱 소스 (ex11 자체)
    ├── data/chroma_db/              # 자식 청크 벡터
    └── data/parent_docs.json        # 부모 페이지 원문 캐시
```

---

## 챕터 간 재사용 원칙

> **핵심**: 각 ex는 **독립 실행 가능한 완전한 프로젝트**로 설계. 이전 챕터 코드를 `from ex06.src... import`로 직접 가져오지 않는다. 대신 **필요한 파일을 같은 이름으로 ex 폴더에 복사**해서 import한다.

### 재사용 매트릭스 (ex11 포함)

| 관계 | 방식 | 예시 |
|------|------|------|
| ex05 → ex06 | 구조 전환 (함수 체인 → 클래스 에이전트) | LCEL `build_rag_chain()` → `IntegratedAgent` 클래스 |
| ex06 → ex07 | 구조 승계 + 기능 추가 | `IntegratedAgent` → `ConnectHRAgent` (캐시·모니터링) |
| ex07 → ex10 | UI·파이프라인 승계 + PDF 레이어 추가 | ex07 app/ 그대로, tuning/ 추가 |
| ex08·ex09 | 서빙 없는 독립 실습 | tuning/ 하위 실험만 |
| **ex08 → ex11** | **원본 클래스 복사** | `CrossEncoderReranker`·`BM25Retriever`가 `ex11/src/tuning/`에 그대로 |
| **ex09 → ex11** | **원본 클래스 복사** | `ParentDocumentRetriever`가 `ex11/src/tuning/parent_doc.py`에 그대로 |
| **ex10 → ex11** | **파서 모듈 이식** | `parse_pdf_hybrid`가 `ex11/src/tuning/hybrid_parser.py`로 복사 |
| **ex07 → ex11** | **에이전트·운영 래퍼 승계** | `cache.py`·`monitoring.py`·`router.py` 동명 복사 |

### 왜 직접 import하지 않나 + 왜 복사는 허용하나

1. **각 챕터 완결성** — 독자가 해당 챕터를 단독 실행할 수 있어야 함
2. **ex11의 특수성** — 최종 조립 챕터이므로 CH08·09·10의 핵심 클래스를 **원본 그대로** 써야 "튜닝과 실제 구현이 일치한다"는 책의 서사가 유지됨. 그래서 ex11은 이전 챕터들의 클래스를 `src/tuning/`에 **파일 단위로 복사**
3. **버전 진화 시연** — 같은 문제를 다른 각도(함수→클래스→기능 추가)로 푸는 과정이 학습 효과

---

## 벡터 DB 연결 패턴

| 챕터 | 라이브러리 | 인덱싱 구조 | 이유 |
|------|-----------|----------|------|
| ex01 | `langchain-chroma` | 단일 컬렉션 | RAG 개념 증명 |
| ex04 | `chromadb` raw | 단일 컬렉션 | 순수 임베딩·저장 |
| ex05 | `langchain-chroma` | 단일 컬렉션 | LCEL 파이프라인 연결 |
| ex06 | `chromadb` raw | 단일 컬렉션 | Tool 내부 단순 쿼리 |
| ex07 | `chromadb` raw + langchain-chroma 폴백 | 단일 컬렉션 | ex06 계승 |
| ex08 | `chromadb` | 단일 컬렉션 | 튜닝 실험 |
| ex10 | `chromadb` raw | 단일 컬렉션 | Tool 내부 사용 |
| **ex11** | **`chromadb` raw + 자식·부모 분리** | **자식 컬렉션(ChromaDB) + 부모 JSON** | CH09 `ParentDocumentRetriever` 원본 구조 반영 |

### ex11의 자식·부모 인덱싱

- **자식 컬렉션**: ChromaDB에 220자 청크 + `parent_id` metadata 저장
- **부모 저장소**: `ex11/data/parent_docs.json`에 페이지 단위 원문 저장
- **인덱싱 흐름**: `data/docs/*` → `hybrid_parser.parse_pdf_hybrid`(pypdf → Vision 폴백) → 페이지 텍스트 = 부모, 220자 쪼갬 = 자식
- **검색 흐름**: 쿼리 → BM25+Vector로 자식 검색 → CrossEncoder 리랭크 → `parent_id`로 부모 복원 (중복 제거)

---

## 핵심 기능 목록 (의도 안)

| # | 기능 | 챕터 | 관련 코드 | 주요 기술 |
|---|------|------|----------|----------|
| 1 | LLM 환각 체험 | CH01 | ex01/step1_fail.py | ChatOllama |
| 2 | Context Injection | CH01 | ex01/step2_context.py | f-string 프롬프트 |
| 3 | RAG 기본 파이프라인 | CH01 | ex01/step3_rag.py | RetrievalQA, Chroma |
| 4 | 데이터 모델 | CH02 | ex02/app/models.py | dataclass |
| 5 | CRUD + FastAPI | CH02 | ex02/app/{crud,api}.py | psycopg2, Router |
| 6 | 문서 수집 전략 | CH03 | (개념) | — |
| 7 | 문서 파싱 | CH04 | ex04/src/extractor.py | pypdf, python-docx, openpyxl |
| 8 | Fixed 청킹 | CH04 | ex04/src/chunker.py | 500자 + 100자 오버랩 |
| 9 | 한국어 임베딩·저장 | CH04 | ex04/src/store.py | ko-sroberta-multitask → Chroma |
| 10 | LCEL RAG 파이프라인 | CH05 | ex05/src/rag_chain.py | Retriever\|Prompt\|LLM\|Parser |
| 11 | 멀티턴 대화 | CH05 | ex05/src/conversation.py | WindowMemory |
| 12 | 3단계 QueryRouter | CH06 | ex06/src/router.py | 규칙 → 스키마 → LLM |
| 13 | MCP 도구 4개 | CH06 | ex06/src/mcp_tools.py | @tool 4종 |
| 14 | ReAct Agent | CH06 | ex06/src/agent.py | create_tool_calling_agent |
| 15 | Agent 표준 구성 | CH07 | ex07/src/agent_config.py | ConnectHRAgent |
| 16 | 응답 캐시 | CH07 | ex07/src/cache.py | ResponseCache(TTL) + EmbeddingCache |
| 17 | 토큰 추적 | CH07 | ex07/src/monitoring.py | TokenTracker + Langfuse 훅 |
| 18 | 청킹 실험 | CH08 | ex08/tuning/step1_chunk_experiment/ | Fixed vs Semantic |
| 19 | 리랭커 | CH08 | ex08/tuning/step2_reranker/ | Cross-Encoder |
| 20 | 하이브리드 검색 | CH08 | ex08/tuning/step3_hybrid_search/ | BM25 + Vector |
| 21 | 쿼리 변환 | CH09 | ex09/tuning/step1_query_rewrite/ | HyDE, Multi-Query, 약어 |
| 22 | 고급 Retriever | CH09 | ex09/tuning/step2_advanced_retriever/ | Parent Doc, Self-Query |
| 23 | OCR 파싱 | CH10 | ex10/tuning/step1_document_parser/ocr.py | EasyOCR |
| 24 | Vision LLM 파싱 | CH10 | ex10/tuning/step1_document_parser/vision.py | qwen2.5vl:7b (기본) |
| 25 | 하이브리드 파서 | CH10 | ex10/tuning/step2_hybrid_parser/ | pypdf → Vision |
| 26 | RAG 평가 프레임워크 | CH10 | ex10/tuning/step3_eval_framework/ | Precision@k, Recall, Hallucination |
| **27** | **레이어드 RAG 파이프라인** | **CH11** | **ex11/src/pipeline.py** | **RagPipeline (Application) + tuning/(Domain)** |
| **28** | **자식·부모 분리 인덱싱** | **CH11** | **ex11/src/tools/search_documents.py** | **ChromaDB 자식 + parent_docs.json** |
| **29** | **근거 이미지 캡처** | **CH11** | **ex11/src/evidence_capture.py** | **PyMuPDF 페이지 렌더 → PNG** |
| **30** | **정형/비정형 근거 분기** | **CH11** | **ex11/app/chat_api.py** | **정형=JSON, 비정형=이미지** |

---

## 의존성 통일 정책 (v3 신규)

> **원칙**: 모든 챕터(ex01~ex11)의 `requirements.txt`는 **동일 패키지는 동일 버전**으로 잠근다. 각 챕터가 실제로 import하는 패키지만 포함하되, 버전 번호는 전 챕터가 한 세트로 맞는다.

### 기준 버전 세트 (전 챕터 공통)

| 카테고리 | 패키지 | 버전 |
|---------|-------|------|
| FastAPI 웹 | fastapi | 0.115.8 |
| FastAPI 웹 | uvicorn[standard] | 0.34.0 |
| FastAPI 웹 | jinja2 | 3.1.5 |
| FastAPI 웹 | python-multipart | 0.0.20 |
| LangChain | langchain | 0.3.21 |
| LangChain | **langchain-core** | **0.3.76** |
| LangChain | langchain-community | 0.3.20 |
| LangChain | langchain-ollama | 0.2.3 |
| LangChain | langchain-openai | 0.3.7 |
| LangChain | langchain-chroma | 0.2.6 |
| LangChain | langchain-huggingface | 0.1.2 |
| LangChain | langchain-text-splitters | 0.3.11 |
| LangChain | langchain-experimental | 0.3.4 |
| 벡터 DB·임베딩 | chromadb | 1.5.1 |
| 벡터 DB·임베딩 | sentence-transformers | 3.3.1 |
| 벡터 DB·임베딩 | huggingface-hub | 0.30.2 |
| 검색·튜닝 | rank-bm25 | 0.2.2 |
| 문서 파싱 | pypdf | 4.3.1 |
| 문서 파싱 | python-docx | 1.1.2 |
| 문서 파싱 | openpyxl | 3.1.5 |
| 문서 파싱 | PyMuPDF | 1.24.0 |
| 문서 파싱 | Pillow | 10.4.0 |
| OCR | easyocr | 1.7.2 |
| 수치 | numpy | 1.26.4 |
| DB | psycopg2-binary | 2.9.10 |
| DB | sqlalchemy | 2.0.35 |
| 유틸 | python-dotenv | 1.0.1 |
| 유틸 | pydantic | 2.10.6 |
| 유틸 | httpx | 0.28.1 |
| 유틸 | rich | 13.9.4 |
| 특수 | langchain-classic | 0.1.0 (ex01 전용) |
| 특수 | playwright | 1.50.0 (ex02 스크립트) |

### 챕터별 실제 포함 패키지 집합

| 챕터 | 실제 import되는 외부 패키지 |
|------|------------------------|
| ex01 | langchain / langchain-core / langchain-community / langchain-ollama / langchain-chroma / langchain-classic / chromadb / rich |
| ex02 | fastapi / uvicorn / jinja2 / python-multipart / psycopg2-binary / sqlalchemy / python-dotenv / pydantic / playwright |
| ex04 | chromadb / sentence-transformers / huggingface-hub / pypdf / python-docx / openpyxl / python-dotenv |
| ex05 | ex04 + 전체 LangChain 스택 + fastapi·uvicorn·jinja2 + pydantic·httpx |
| ex06 | ex05 + psycopg2-binary·sqlalchemy |
| ex07 | ex06 + rich |
| ex08 | langchain·langchain-core·langchain-community·langchain-chroma·langchain-huggingface·langchain-text-splitters·langchain-experimental / chromadb / sentence-transformers / rank-bm25 / numpy / python-dotenv / rich |
| ex09 | langchain·langchain-core·langchain-community·langchain-huggingface / sentence-transformers / httpx / python-dotenv / rich |
| ex10 | chromadb / sentence-transformers / pypdf·python-docx·openpyxl·PyMuPDF·Pillow / easyocr / numpy / httpx / python-dotenv / rich |
| ex11 | ex07 전체 + rank-bm25 + PyMuPDF·Pillow (근거 이미지) |

### 통일의 효과

- **의존성 충돌 제거**: ex06~09의 `langchain-core==0.3.63`이 `langchain-chroma==0.2.6`(>=0.3.76 요구)과 부딪히던 문제 해소
- **단일 캐시 재사용**: `pip install` 시 동일 버전의 휠을 캐시에서 한 번 내려받고 전 챕터가 공유
- **교재 일관성**: "챕터 A에서 되던 게 챕터 B에서 안 된다"는 혼란 제거

---

## 기술 스택 (v3 기준)

### 핵심 (의도 안)

| 계층 | 기술 | 버전 | 역할 | 챕터 |
|------|------|------|------|------|
| LLM (Q&A·추론) | Ollama `deepseek-r1:8b` | — | CH05에서만 | CH05 |
| LLM (Tool Calling) | Ollama `llama3.1:8b` | — | 에이전트 기본 | CH06~11 |
| LLM (Vision) | Ollama `qwen2.5vl:7b` | — | **기본 권장** | CH10~11 |
| LLM (Vision 대안) | `minicpm-v`, `llama3.2-vision:11b` | — | 가볍게/고품질 옵션 | CH10 |
| LLM (클라우드) | OpenAI `gpt-4o-mini` | — | Vision + Tool Calling + JSON | CH05~11 |
| 프레임워크 | LangChain | 0.3.21 | RAG/Agent | CH01, CH05~11 |
| 벡터 DB | ChromaDB | 1.5.1 | 임베딩 저장/검색 | CH01, CH04~11 |
| 임베딩 | ko-sroberta-multitask | — | 한국어 768d | CH04~11 |
| 리랭커 모델 | `BAAI/bge-reranker-v2-m3` (CrossEncoder) | — | CH08·CH11 | CH08, CH11 |
| 웹 | FastAPI | 0.115.8 | REST + 채팅 UI | CH02, CH05~07, CH10~11 |
| DB | PostgreSQL | 16 | 정형 데이터 | CH02, CH06~08, CH10~11 |
| 검증 | Pydantic | 2.10.6 | 스키마 | CH02, CH05~11 |
| 문서 파싱 (텍스트) | pypdf, python-docx, openpyxl | 4.3.1 / 1.1.2 / 3.1.5 | CH04 기본 | CH04~07, CH10~11 |
| 문서 파싱 (스캔) | PyMuPDF(fitz), Pillow | 1.24 / 10.4 | 페이지 렌더링 | CH10~11 |
| OCR | EasyOCR | 1.7.2 | 한국어+영어 | CH10 |
| 키워드 검색 | rank-bm25 | 0.2.2 | Hybrid Search | CH08, CH11 |
| 고급 Retriever | langchain-experimental | 0.3.4 | Semantic Chunking | CH08 |
| Vision 호출 | httpx | 0.28.1 | Ollama API | CH09~11 |
| 콘솔 출력 | rich | 13.9.4 | Table/Panel | CH07~11 |

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
| 의존성 관리 | pip (uv는 선택, 책에는 미포함) |
| LLM 런타임 | Ollama (로컬) 또는 OpenAI API |
| 포트 | FastAPI 기본 8000. 충돌 시 `PORT=8011 python run.py`로 변경 가능 (ex11 기준) |

---

## 챕터 간 코드 진화 흐름 (v3)

```
CH01 (ex01): LLM 단독 → Context Injection → RAG (개념 증명)
  ↓
CH02 (ex02): FastAPI + PostgreSQL CRUD (정형 기반)
  ↓
CH03 (없음):  사내 문서 수집 전략 (개념만)
  ↓
CH04 (ex04): 파싱 → 청킹 → 임베딩 → ChromaDB
  ↓
CH05 (ex05): LCEL RAG 파이프라인 + 멀티턴
  ↓
CH06 (ex06): Tool Calling + ReAct Agent (정형+비정형 통합)
  ↓
CH07 (ex07): Agent 표준화 + 캐시 + 로깅
  ↓
CH08 (ex08): 검색 튜닝 — Chunking · Reranker · Hybrid (실험)
  ↓
CH09 (ex09): 질의 변환 — HyDE · Multi-Query · Parent Doc (실험)
  ↓
CH10 (ex10): 이미지 문서 — OCR · Vision LLM · RAG 평가
  ↓
CH11 (ex11): 완성 — 레이어드 파이프라인 조립 + 자식·부모 인덱싱 + 근거 이미지
```

CH08·CH09는 실험이고, **CH11에서 비로소 이 실험들이 단일 파이프라인으로 조립**되어 운영 UI와 결합된다.

---

## 기획서 매핑 (갱신)

| 코드 챕터 | 기획서 PART | 비고 |
|---------|----------|------|
| CH01 | — | LLM 환각 체험 도입 |
| CH02 | PART 1 | FastAPI CRUD |
| CH03 | PART 2 | 문서 수집 전략 (개념) |
| CH04 | PART 3 | VectorDB 구축 |
| CH05 | PART 4 | RAG Q&A 엔진 |
| CH06 | PART 5 | 통합 에이전트 |
| CH07 | PART 6 | 캐시·모니터링 |
| CH08 | PART 7 (1/3) | 검색 튜닝 |
| CH09 | PART 7 (2/3) | 질의 변환 |
| CH10 | PART 7 (3/3) | 이미지 문서 + 평가 |
| **CH11** | **PART 8 (완성)** | **파이프라인 조립 + 근거 이미지** |

---

## 점검 이력

- **v1 (2026-01)**: CH01~08, 11개 튜닝 실험을 CH08 한 챕터에 몰아넣은 초안
- **v2 (2026-04)**: CH08·CH09·CH10 분할, ex01~ex10 rag-end 구조, Vision LLM/OCR/평가 추가, chromadb vs langchain-chroma 사용 패턴 명시, Python 3.12 고정, `container_name: ex0N_postgres` 통일
- **v3 (2026-04)**: CH11(ex11) 추가 — 레이어드 아키텍처 + 자식·부모 분리 인덱싱 + CH08·CH09 원본 클래스(`CrossEncoderReranker`·`BM25Retriever`·`ParentDocumentRetriever`) 이식 + CH10 `parse_pdf_hybrid` 이식. **전 챕터 `requirements.txt` 버전 잠금 통일**(기준: ex11 충돌 없는 조합, `langchain-core==0.3.76`). Vision 기본 모델 `minicpm-v` → `qwen2.5vl:7b`로 교체. ex11 `run.py`에 `PORT`·`UVICORN_RELOAD` 환경변수 지원.
