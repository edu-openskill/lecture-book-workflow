# 코드 분석

## 완성 코드 정보
- **경로**: `projects/사내AI비서_v2/code/`
- **언어/프레임워크**: Python 3.10+ / FastAPI + LangChain 0.3.x + Ollama + ChromaDB + PostgreSQL
- **챕터**: CH01~CH08 (9개)
- **참고**: CH03은 개념 챕터 (코드 없음, 기획서 ai-list.pdf PART 2 참조)
- **참고**: CH01은 기획서에 없던 신규 추가 챕터

## 전체 구조

```
code/
├── CH01_LLM의_한계와_RAG의_필요성/
│   ├── step1_fail.py              # LLM 단독 → 환각
│   ├── step2_context.py           # Context Injection → 임시 해결
│   ├── step3_rag.py               # RAG + 청킹 → 성공
│   ├── step3_rag_no_chunking.py   # RAG 미청킹 → 비교
│   ├── step4_rag.py               # RAG + 추론 → 심화
│   └── requirements.txt
│
├── CH02_FastAPI_기본_시스템/
│   ├── app/
│   │   ├── main.py        # FastAPI 앱 + 라우터 등록
│   │   ├── models.py      # dataclass (Employee, LeaveBalance, Sale)
│   │   ├── schemas.py     # Pydantic 요청/응답 스키마
│   │   ├── database.py    # psycopg2 연결 (Context Manager)
│   │   ├── crud.py        # DB CRUD 함수
│   │   ├── views.py       # [제외] Jinja2 Admin UI
│   │   └── api.py         # REST API 라우터
│   ├── templates/          # [제외] HTML 템플릿
│   ├── static/             # [제외] CSS
│   ├── docker-compose.yml  # [간략] PostgreSQL 16
│   └── requirements.txt
│
├── CH03_사내문서_수집전략/          # [개념 챕터 — 코드 없음]
│   └── (기획서 ai-list.pdf PART 2 참조)
│       # 문서 종류, 형식 지원, 표준 규칙, 메타데이터, 수집 파이프라인
│
├── CH04_VectorDB_구축/
│   ├── src/
│   │   ├── main.py         # 파이프라인 오케스트레이션
│   │   ├── extractor.py    # PDF/DOCX/XLSX 통합 파서
│   │   ├── extract_pdf.py  # PDF 파싱 (pypdf)
│   │   ├── extract_docx.py # DOCX 파싱 (python-docx)
│   │   ├── extract_xlsx.py # XLSX 파싱 (openpyxl)
│   │   ├── chunker.py      # Fixed-size 청킹 (500자+100오버랩)
│   │   ├── store.py        # ko-sroberta 임베딩 + ChromaDB
│   │   └── cli_search.py   # CLI 검색 (유사도 시각화)
│   ├── data/
│   │   ├── docs/           # 원본 문서 (HR/Finance/Ops/Security)
│   │   ├── markdown/       # 파싱 결과
│   │   └── chroma_db/      # 벡터 저장소
│   └── requirements.txt
│
├── CH05_RAG_QA_엔진/
│   ├── src/
│   │   ├── rag_chain.py       # LCEL 파이프라인 (Retriever|Prompt|LLM|Parser)
│   │   ├── response_parser.py # 답변 파싱 + 출처 추출
│   │   └── conversation.py    # WindowMemory 멀티턴 (최근 5턴)
│   ├── app/
│   │   ├── main.py        # FastAPI 앱
│   │   ├── chat_api.py    # POST /api/chat
│   │   └── session.py     # 세션 쿠키 관리
│   ├── templates/          # [제외] 채팅 UI
│   ├── static/             # [제외] CSS
│   └── requirements.txt
│
├── CH06_통합_에이전트_설계/
│   ├── src/
│   │   ├── router.py      # 3단계 QueryRouter (규칙→스키마→LLM)
│   │   ├── mcp_tools.py   # @tool 4개 (leave_balance, sales_sum, list_employees, search_documents)
│   │   └── agent.py       # ReAct Agent (create_tool_calling_agent)
│   ├── app/
│   │   ├── main.py        # FastAPI 앱
│   │   ├── chat_api.py    # 에이전트/RAG 모드 선택
│   │   └── database.py    # [간략] PostgreSQL 연결
│   ├── tests/
│   │   └── test_scenarios.py  # 18개 시나리오 테스트
│   ├── templates/          # [제외]
│   ├── docker-compose.yml  # [간략]
│   └── requirements.txt
│
├── CH07_LangChain_연결/
│   ├── src/
│   │   ├── main.py          # CLI 대화형 + 데모 모드
│   │   ├── agent_config.py  # ConnectHRAgent (LCEL RAG Chain + AgentExecutor)
│   │   ├── monitoring.py    # JSON 로깅 + TokenTracker + [간략]Langfuse
│   │   ├── cache.py         # ResponseCache(TTL) + EmbeddingCache(파일)
│   │   └── tools/
│   │       ├── leave_balance.py
│   │       ├── sales_sum.py
│   │       ├── list_employees.py
│   │       └── search_documents.py
│   ├── app/                 # FastAPI 웹 앱
│   ├── templates/           # [제외]
│   └── requirements.txt
│
├── CH08_RAG_튜닝/
│   ├── src/
│   │   ├── main.py            # 듀얼모드 CLI (에이전트+실험)
│   │   ├── agent_config.py    # CH07 기반 Agent
│   │   ├── router.py          # 3단계 QueryRouter
│   │   └── eval_framework.py  # Precision@k, Recall@k, Hallucination Rate
│   ├── tuning/
│   │   ├── chunk_experiment.py      # 실험1: Fixed vs Semantic 청킹
│   │   ├── retriever_experiment.py  # 실험2: k값, threshold
│   │   ├── reranker.py             # 실험3: Cross-Encoder 리랭킹
│   │   ├── hybrid_search.py        # 실험4: BM25+Vector (alpha)
│   │   ├── advanced_retriever.py   # 실험5: Parent/SelfQuery/Compression
│   │   ├── query_rewrite.py        # 실험6: HyDE, Multi-Query, 약어
│   │   ├── document_parser.py      # 실험7: 라이브러리 vs vLLM
│   │   ├── document_capture.py     # 실험8: 문서 캡처+인제스천
│   │   └── evidence_pipeline.py    # 실험9: 답변 근거 시스템
│   ├── data/
│   │   └── test_questions.json     # 30개 테스트 질문
│   └── requirements.txt
│
└── README.md
```

## 핵심 기능 (의도 안)

| # | 기능 | 챕터 | 관련 코드 | 주요 기술 |
|---|------|------|----------|----------|
| 1 | LLM 환각 체험 | CH01 | step1_fail.py | ChatOllama, deepseek-r1:8b |
| 2 | Context Injection | CH01 | step2_context.py | f-string 프롬프트 |
| 3 | RAG 기본 파이프라인 | CH01 | step3_rag.py | RetrievalQA, OllamaEmbeddings, Chroma |
| 4 | 청킹 효과 비교 | CH01 | step3_rag_no_chunking.py | 청킹 유무 비교 |
| 5 | RAG + 추론 | CH01 | step4_rag.py | Chain-of-Thought 질문 |
| 6 | 데이터 모델 | CH02 | models.py | dataclass (Employee, LeaveBalance, Sale) |
| 7 | 데이터 검증 | CH02 | schemas.py | Pydantic Field() 검증 |
| 8 | DB 연결 패턴 | CH02 | database.py | Context Manager, psycopg2 |
| 9 | CRUD 함수 | CH02 | crud.py | 매개변수화 쿼리, RETURNING |
| 10 | REST API | CH02 | api.py | FastAPI Router, HTTPException |
| 11 | 문서 수집 전략 | CH03 | (개념) | 문서 종류, 형식별 지원, 교재용 추천 세트 |
| 12 | 문서 표준 규칙 | CH03 | (개념) | 파일명 규칙, 메타데이터, 섹션 헤더, 개정 이력 |
| 13 | 문서 파싱 | CH04 | extractor.py | pypdf, python-docx, openpyxl |
| 14 | Fixed-size 청킹 | CH04 | chunker.py | 500자, 100자 오버랩, 메타데이터 |
| 15 | 한국어 임베딩+저장 | CH04 | store.py | ko-sroberta-multitask, ChromaDB upsert |
| 16 | CLI 벡터 검색 | CH04 | cli_search.py | 코사인 유사도, 시각화 |
| 17 | LCEL RAG 파이프라인 | CH05 | rag_chain.py | Retriever\|Prompt\|LLM\|Parser |
| 18 | 출처 강제 프롬프트 | CH05 | rag_chain.py | "[출처: 문서명]" 형식 강제 |
| 19 | 응답 파싱 | CH05 | response_parser.py | DeepSeek `<think>` 제거, 출처 추출 |
| 20 | 멀티턴 대화 | CH05 | conversation.py | WindowMemory(k=5), 세션 TTL |
| 21 | 채팅 API | CH05 | chat_api.py | POST /api/chat, 세션 쿠키 |
| 22 | 3단계 QueryRouter | CH06 | router.py | 규칙→스키마→LLM 폴백 |
| 23 | MCP 도구 4개 | CH06 | mcp_tools.py | @tool: leave_balance, sales_sum, list_employees, search_documents |
| 24 | ReAct Agent | CH06 | agent.py | create_tool_calling_agent, AgentExecutor |
| 25 | Agent 표준 구성 | CH07 | agent_config.py | ConnectHRAgent, LCEL RAG Chain |
| 26 | @tool 모듈화 | CH07 | tools/*.py | 도구별 파일 분리, 에러 핸들링 |
| 27 | 응답 캐시 | CH07 | cache.py | ResponseCache(TTL), EmbeddingCache(파일) |
| 28 | 토큰 추적 | CH07 | monitoring.py | TokenTracker, 비용 계산 |
| 29 | CLI 대화형+데모 | CH07 | main.py | 멀티턴, stats, demo 모드 |
| 30 | 청킹 실험 | CH08 | chunk_experiment.py | Fixed vs Semantic, 크기/오버랩 |
| 31 | Retriever 튜닝 | CH08 | retriever_experiment.py | k값, threshold |
| 32 | 리랭킹 | CH08 | reranker.py | Cross-Encoder 재정렬 |
| 33 | 하이브리드 검색 | CH08 | hybrid_search.py | BM25+Vector, alpha |
| 34 | 고급 Retriever | CH08 | advanced_retriever.py | Parent, SelfQuery, Compression |
| 35 | Query Rewrite | CH08 | query_rewrite.py | HyDE, Multi-Query, 약어 확장 |
| 36 | 답변 근거 시스템 | CH08 | evidence_pipeline.py | 이미지+DB 근거 동시 제공 |
| 37 | 평가 프레임워크 | CH08 | eval_framework.py | Precision@k, Recall@k, Hallucination Rate |
| 38 | 고급 문서 파싱 | CH08 | document_parser.py | 라이브러리 비교, vLLM 멀티모달 |
| 39 | 문서 캡처+인제스천 | CH08 | document_capture.py | OCR 캡처, 자동 인제스천 파이프라인 |

## 의도 밖 기능 (제외)

| 기능 | 관련 코드 | 제외 이유 |
|------|----------|----------|
| Admin UI (Jinja2+CSS) | CH02 views.py, templates/, static/ | 프론트엔드 UI 제외 |
| 채팅 UI (HTML+JS) | CH05~08 templates/, static/ | 프론트엔드 UI 제외 |
| Docker/PostgreSQL 세팅 | CH02,06~08 docker-compose.yml | 간략 안내만 |
| Langfuse 연동 상세 | CH07 monitoring.py 일부 | 존재 언급만, 설정 제외 |
| RAGAS 자동 평가 | CH08 eval_framework.py 일부 | 더 알아보기 수준 |

## 기술 스택 정리

### 핵심 (의도 안)

| 계층 | 기술 | 역할 | 챕터 |
|------|------|------|------|
| LLM | Ollama + deepseek-r1:8b | 로컬 LLM 추론 | CH01~08 |
| LLM 대안 | OpenAI gpt-4o-mini | 클라우드 LLM (선택) | CH05~08 |
| 프레임워크 | LangChain 0.3.x | RAG/Agent 프레임워크 | CH01~08 |
| 벡터DB | ChromaDB 1.5 | 임베딩 저장/검색 | CH01,04~08 |
| 임베딩 | ko-sroberta-multitask | 한국어 임베딩 (768d) | CH04~08 |
| 웹 | FastAPI 0.115+ | REST API | CH02,05~08 |
| DB | PostgreSQL 16 | 정형 데이터 (직원/연차/매출) | CH02,06~08 |
| DB 드라이버 | psycopg2 | SQL 직접 실행 | CH02,06~08 |
| 검증 | Pydantic 2.10+ | 요청/응답 스키마 | CH02,05~08 |
| 문서 파싱 | pypdf, python-docx, openpyxl | PDF/DOCX/XLSX 텍스트 추출 | CH04~08 |
| 키워드 검색 | rank-bm25 | BM25 하이브리드 검색 | CH08 |
| 리랭킹 | Cross-Encoder | 검색 결과 재정렬 | CH08 |
| Vision LLM | LLaVA / Qwen2-VL (Ollama) | 이미지 캡션 생성 (인덱싱) | CH08 |
| OCR | EasyOCR | 이미지 텍스트 추출 | CH08 |
| 문서 파싱 고급 | PyMuPDF | 고급 PDF 파싱 | CH08 |

### 간략/제외 (의도 밖)

| 기술 | 역할 | 수준 |
|------|------|------|
| Docker Compose | PostgreSQL 컨테이너 | 간략 (docker-compose up만) |
| Jinja2 | HTML 템플릿 | 제외 |
| Langfuse | LLM 모니터링 | 언급만 |
| RAGAS | RAG 자동 평가 | 더 알아보기 |

## 기술 의존성 메모

| 선행 개념 | 필요한 챕터 | 비고 |
|----------|-----------|------|
| Python 기초 | 전체 | 독자 배경지식 (가정) |
| REST API 개념 | CH02~ | HTTP 메서드, JSON |
| SQL 기초 | CH02,06~08 | SELECT, INSERT, JOIN |
| 벡터/임베딩 개념 | CH04~ | 코사인 유사도 — 비유로 설명 |
| LangChain LCEL | CH05~ | 파이프 연산자 `|` — CH05에서 도입 |
| Agent/Tool Calling | CH06~ | ReAct 패턴 — CH06에서 도입 |

## 챕터 간 코드 진화 흐름

```
CH01: LLM 단독 → Context Injection → RAG (개념 증명) [신규]
  ↓
CH02: FastAPI + PostgreSQL CRUD (정형 데이터 기반)
  ↓
CH03: 사내 문서 수집 전략 + 문서 표준 (개념 챕터, 코드 없음)
  ↓
CH04: 문서 파싱 → 청킹 → 임베딩 → ChromaDB (비정형 데이터 기반)
  ↓
CH05: LCEL 파이프라인 + 출처 강제 + 멀티턴 (RAG 엔진)
  ↓
CH06: QueryRouter + MCP 도구 + ReAct Agent (정형+비정형 통합)
  ↓
CH07: Agent 표준화 + 캐시 + 로깅 + 토큰 추적 (운영 안정화)
  ↓
CH08: 11개 튜닝 실험 + 평가 프레임워크 (성능 최적화)
```

## 기획서 매핑

| 코드 챕터 | 기획서 PART | 비고 |
|---------|----------|------|
| CH01 (신규) | — | 기획서에 없음. LLM 환각 체험 → RAG 필요성 도입 |
| CH02 | PART 1 | FastAPI CRUD 사내 시스템 |
| CH03 | PART 2 | 문서 수집 전략 + 표준 (코드 없음) |
| CH04 | PART 3 | VectorDB 구축 |
| CH05 | PART 4 | RAG Q&A 엔진 |
| CH06 | PART 5 | 통합 에이전트 (MCP + RAG) |
| CH07 | PART 6 | LangChain 연결 + 운영 |
| CH08 | PART 7 | RAG 튜닝 (11개 실험) |
| — | PART 0 | 미리보기 → 반영 (프롤로그 또는 별도 챕터, STEP 3에서 확정) |
| — | PART 0.5 | 환경 설정 → 반영 (부록 또는 별도 챕터, STEP 3에서 확정) |
| — | PART 8 | 배포/운영 → **제외** |
