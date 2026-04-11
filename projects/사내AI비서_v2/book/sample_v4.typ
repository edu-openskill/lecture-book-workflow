// ── 책 변수 정의 ──
#let book-title = "사내 AI 비서 만들기"
#let book-subtitle = "RAG로 똑똑한 사내 문서 검색 시스템 구축하기"
#let book-description = [LLM에 검색을 더해 사내 문서를 정확하게 답변하는 AI 비서를 만드는 과정을 이야기로 풀어냅니다. Mermaid→D2 변환 + Typst PDF 빌드 파이프라인 E2E 샘플입니다.]
#let book-header-title = "사내 AI 비서 만들기"

// ── book_base 템플릿 ──
#include "templates/book_base.typ"

// ══════════════════════════════════════
// CH01. 왜 RAG인가
// ══════════════════════════════════════

= CH01. 왜 RAG인가 — LLM의 한계를 넘어서

#quote(block: true)[
한 줄 요약: RAG는 LLM에 검색을 더해 환각을 줄이는 기술입니다 \
핵심 개념: RAG, LLM, 벡터DB, 임베딩
]

어느 날 팀장이 물었습니다.

#strong[팀장]: "우리 사내 문서를 AI에게 물어보면 답해줄 수 있을까?"

#strong[나]: "ChatGPT는 우리 회사 문서를 모릅니다."

(그렇다면 어떻게 해야 할까?)

답은 간단합니다. #strong[검색] 을 붙이면 됩니다. LLM이 모르는 정보를 외부에서 찾아다 주는 것, 이것이 바로 #strong[RAG(Retrieval-Augmented Generation)] 입니다.

도서관 사서를 떠올려 보세요. 질문을 받으면 서가에서 관련 책을 찾아오고, 그 책을 참고해서 답변합니다. RAG도 똑같습니다. 사서가 아무리 박학다식해도 도서관에 없는 책의 내용은 답할 수 없습니다. 반대로, 아무리 어려운 질문이라도 관련 책만 찾아오면 정확히 답할 수 있습니다.

LLM도 마찬가지입니다. 학습 데이터에 없는 사내 문서, 최신 규정, 내부 시스템 정보는 아무리 똑똑한 모델이라도 알 수 없습니다. 하지만 질문이 들어올 때 관련 문서를 먼저 검색해서 LLM에게 건네주면, 정확한 답변이 가능해집니다.

아래 다이어그램은 LLM 단독 방식과 RAG 방식의 차이를 보여줍니다.

#auto-image("../assets/sample/diagram/01_llm-vs-rag.png", alt: "LLM 단독 vs RAG 비교", max-width: 0.85)

왼쪽 경로를 보면, 질문이 LLM에 바로 들어갑니다. LLM은 학습 데이터만으로 답변하기 때문에 사내 문서에 대한 질문에는 그럴듯하지만 틀린 답변, 이른바 #strong[환각(hallucination)] 을 만들어냅니다.

오른쪽 경로는 다릅니다. 질문이 먼저 검색 엔진을 거쳐 벡터DB에서 관련 문서를 찾아옵니다. 이 문서를 #strong[컨텍스트] 로 LLM에 함께 전달하면, LLM은 근거 있는 정확한 답변을 생성합니다.

// ── 파트 전환 ──
#v(12pt)
#block(width: 100%, stroke: (bottom: 1pt + rgb("#e5e7eb")), below: 12pt)[]

이제 직접 만들어 보겠습니다.

== 프로젝트 구조

이 책에서는 두 개의 Git 레포지토리를 사용합니다.

#table(
  columns: (1fr, 2fr),
  [*레포*], [*용도*],
  [`ai-qa-lag`], [완성본. 동작하는 전체 코드],
  [`ai-qa-lag-ex`], [예제 템플릿. 빈 파일을 채워가며 실습],
)

```bash
git clone https://github.com/example/ai-qa-lag-ex.git
cd ai-qa-lag-ex
```

```
ai-qa-lag-ex/
├── main.py          [실습] 진입점
├── config.py        [설명] 환경 설정
├── loader.py        [실습] 문서 로더
├── retriever.py     [실습] 검색기
└── README.md        [참고]
```

챕터를 따라 하며 코드를 작성하고, 막히면 완성 코드를 참고하세요.

=== RAG 파이프라인 전체 흐름

아래 다이어그램은 RAG 시스템의 전체 파이프라인을 보여줍니다. 크게 세 단계로 나뉩니다.

#auto-image("../assets/sample/diagram/02_rag-pipeline.png", alt: "RAG 파이프라인 — 문서 준비 → 검색 → 답변 생성", max-width: 0.5)

#strong[문서 준비] 단계에서는 사내 문서를 로딩하고, 파싱하고, 적절한 크기로 청킹합니다. #strong[검색] 단계에서는 사용자 질문을 임베딩으로 변환하고 벡터DB에서 유사도 검색을 수행합니다. #strong[답변 생성] 단계에서는 검색된 문서 조각을 컨텍스트로 조립하고, LLM에 전달하여 최종 답변을 만듭니다.

=== 핵심 코드

아래 코드를 `main.py`에 작성합니다.

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. 벡터 스토어 생성
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)

# 2. 검색기 설정
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 3. 프롬프트 템플릿
prompt = ChatPromptTemplate.from_template("""
다음 컨텍스트를 참고하여 질문에 답변하세요.

컨텍스트: {context}
질문: {question}
""")

# 4. 체인 구성
chain = prompt | ChatOpenAI() | StrOutputParser()

# 5. 실행
context = retriever.invoke("연차 규정이 어떻게 되나요?")
answer = chain.invoke({
    "context": context,
    "question": "연차 규정이 어떻게 되나요?"
})
print(answer)
```

=== 이것만은 기억하자

RAG는 #strong[검색 + 생성] 의 조합입니다. LLM이 모르는 정보를 검색으로 보완하면, 환각 없는 정확한 답변을 얻을 수 있습니다. 사서가 책을 찾아오듯, 검색 엔진이 문서를 찾아다 주는 것이 핵심입니다.

다음 챕터에서는 API를 통해 외부 서비스와 연결하는 방법을 알아봅니다. 우리가 만든 RAG 시스템을 실제 서비스로 띄우는 첫걸음입니다.
