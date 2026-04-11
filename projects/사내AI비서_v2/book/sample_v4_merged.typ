// ── 책 변수 정의 ──
#let book-title = "사내 AI 비서 만들기"
#let book-subtitle = "RAG로 똑똑한 사내 문서 검색 시스템 구축하기"
#let book-description = [LLM에 검색을 더해 사내 문서를 정확하게 답변하는 AI 비서를 만드는 과정을 이야기로 풀어냅니다.]
#let book-header-title = "사내 AI 비서 만들기"

// ── 범용 북 템플릿 (Typst) ──
// 이 파일은 스킬(pub-typst-design) 소유. 프로젝트에서 심볼릭 링크로 참조.
// 프로젝트의 book.typ에서 정의한 변수(book-title 등)를 사용합니다.
//
// 필수 변수 (book.typ에서 정의):
//   #let book-title = "책 제목"
//   #let book-subtitle = "부제"
//   #let book-description = [설명]
//   #let book-header-title = "헤더 표시 제목"

// ── 챕터 추적 (헤더용) ──
#let chapter-title = state("chapter-title", none)

// ── 페이지 설정 ──
// 46배판 (188x257mm) — 국내 IT 서적 표준 판형
#set page(
  width: 188mm,
  height: 257mm,
  margin: (top: 20mm, bottom: 28mm, left: 20mm, right: 20mm),
  numbering: "1",
  number-align: center,
  header: context {
    let page-num = counter(page).get().first()
    if page-num > 2 {
      set text(8pt, fill: rgb("#999999"))
      grid(
        columns: (1fr, 1fr),
        align(left)[#book-header-title],
        align(right)[#chapter-title.get()],
      )
      v(2pt)
      line(length: 100%, stroke: 0.3pt + rgb("#dddddd"))
    }
  },
  footer: context {
    let page-num = counter(page).get().first()
    if page-num > 2 {
      align(center, text(9pt, fill: rgb("#888888"))[#counter(page).display()])
    }
  },
)

// ── 폰트 설정 ──
#set text(
  font: ("KoPubDotum_Pro", "Apple SD Gothic Neo"),
  size: 10pt,
  lang: "ko",
  fill: rgb("#1a1a1a"),
)

#set par(
  leading: 1.0em,
  first-line-indent: 0pt,
  justify: true,
)

// ── 제목 스타일 ──
#show heading.where(level: 1): it => {
  chapter-title.update(it.body)
  pagebreak(weak: true)
  v(60pt)  // 챕터 오프닝: 상단 1/3 여백 (출판 표준)
  block(
    width: 100%,
    below: 16pt,
    sticky: true,
    {
      text(26pt, weight: "bold", fill: rgb("#1a1a1a"))[#it.body]
      v(8pt)
      line(length: 100%, stroke: 3pt + rgb("#2563eb"))
    }
  )
  v(14pt)
}

#show heading.where(level: 2): it => {
  v(24pt)
  block(
    width: 100%,
    below: 8pt,
    sticky: true,
    inset: (left: 12pt),
    stroke: (left: 4pt + rgb("#2563eb")),
    text(16pt, weight: "bold", fill: rgb("#1e40af"))[#it.body]
  )
  v(6pt)
}

#show heading.where(level: 3): it => {
  v(16pt)
  block(
    below: 6pt,
    sticky: true,
    text(13pt, weight: "semibold", fill: rgb("#1e3a5f"))[#it.body]
  )
  v(4pt)
}

#show heading.where(level: 4): it => {
  v(12pt)
  block(
    below: 4pt,
    sticky: true,
    text(11pt, weight: "semibold", fill: rgb("#374151"))[#it.body]
  )
  v(2pt)
}

// ── 코드 블록 (페이지 넘김 허용) ──
#show raw.where(block: true): it => {
  set text(size: 8pt, weight: "bold", font: ("Menlo", "KoPubDotum_Pro"))
  block(
    width: 100%,
    fill: white,
    inset: (x: 16pt, y: 14pt),
    radius: 8pt,
    stroke: 1pt + rgb("#d1d5db"),
    breakable: true,
    text(fill: rgb("#1a1a1a"))[#it]
  )
}

// ── 인라인 코드 ──
#show raw.where(block: false): it => {
  box(
    fill: rgb("#f3f4f6"),
    inset: (x: 4pt, y: 2pt),
    radius: 3pt,
    text(size: 8.5pt, fill: rgb("#1e40af"), font: ("Menlo", "KoPubDotum_Pro"))[#it]
  )
}

// ── 인용 블록 (blockquote) ──
#show quote.where(block: true): it => {
  block(
    width: 100%,
    above: 10pt,
    below: 10pt,
    inset: (left: 14pt, right: 14pt, top: 10pt, bottom: 10pt),
    stroke: (left: 3pt + rgb("#93b4e8")),
    fill: rgb("#f5f8ff"),
    radius: (right: 4pt),
    {
      set par(justify: true, leading: 0.9em)
      text(size: 9pt, fill: rgb("#4b5563"))[#it.body]
    }
  )
}

// ── 표 스타일 ──
#set table(
  stroke: (bottom: 0.5pt + rgb("#e5e7eb")),
  inset: (x: 10pt, y: 8pt),
  fill: (_, y) => if y == 0 { rgb("#1e40af") } else if calc.odd(y) { rgb("#f8fafc") } else { white },
)

#show table.cell.where(y: 0): set text(fill: white, weight: "medium")

#show table: it => {
  set text(size: 8.5pt)
  block(breakable: true)[#it]
}

// ── 볼드/이탤릭 ──
#show strong: set text(fill: rgb("#1e3a5f"))
#show emph: set text(fill: rgb("#6b7280"))

// ── 수평선은 후처리에서 #v + block으로 변환됨 ──

// ── figure 스타일 ──
#show figure: it => {
  v(8pt)
  align(center, it.body)
  if it.caption != none {
    v(2pt)
    align(center, text(8pt, fill: rgb("#6b7280"))[#it.caption.body])
  }
  v(4pt)
}

// ── 링크 스타일 ──
#show link: it => {
  text(fill: rgb("#2563eb"))[#it]
}

// ── 자동 크기 조절 이미지 ──
// 남은 페이지 공간을 감지하여 이미지 크기를 자동으로 조절합니다.
// max-width: 이미지 최대 너비 비율 (0.0~1.0)
// style: 이미지 테두리 프리셋
//   "plain"          — 효과 없음 (기본값)
//   "bordered"       — 프라이머리 컬러(#2563eb) 테두리
//   "shadow"         — 오른쪽/아래 그림자 효과
//   "bordered-shadow" — 프라이머리 테두리 + 그림자
//   "minimal"        — 얇은 회색 테두리
// 이미지가 남은 공간보다 크면 자동 축소, 너무 작아지면 다음 페이지로 넘김
#let auto-image(path, alt: none, max-width: 0.7, style: "plain") = layout(size => context {
  let target-width = size.width * max-width
  let img = image(path, width: target-width)
  let img-size = measure(img)
  let caption-h = if alt != none { 28pt } else { 0pt }
  let needed = img-size.height + caption-h + 24pt

  let final-width = if needed > size.height and size.height > 120pt {
    // 남은 공간에 맞게 축소 시도
    let available = size.height - caption-h - 24pt
    let ratio = available / img-size.height
    if ratio >= 0.5 {
      target-width * ratio
    } else {
      target-width  // 너무 작아지면 원래 크기 (다음 페이지로)
    }
  } else {
    target-width
  }

  // 스타일별 이미지 래핑
  let styled-img = if style == "bordered" {
    block(
      stroke: 2pt + rgb("#2563eb"),
      radius: 4pt,
      clip: true,
      image(path, width: final-width)
    )
  } else if style == "shadow" {
    block(
      stroke: (
        left: 0.5pt + rgb("#e0e0e0"),
        top: 0.5pt + rgb("#e0e0e0"),
        right: 2pt + rgb("#c0c0c0"),
        bottom: 2pt + rgb("#c0c0c0"),
      ),
      radius: 4pt,
      clip: true,
      image(path, width: final-width)
    )
  } else if style == "bordered-shadow" {
    block(
      stroke: (
        left: 2pt + rgb("#2563eb"),
        top: 2pt + rgb("#2563eb"),
        right: 3pt + rgb("#1d4ed8"),
        bottom: 3pt + rgb("#1d4ed8"),
      ),
      radius: 4pt,
      clip: true,
      image(path, width: final-width)
    )
  } else if style == "minimal" {
    block(
      stroke: 0.5pt + rgb("#e5e7eb"),
      radius: 2pt,
      clip: true,
      image(path, width: final-width)
    )
  } else {
    image(path, width: final-width)
  }

  if alt != none {
    figure(styled-img, caption: [#alt])
  } else {
    align(center, styled-img)
  }
})

// ── 사이드 이미지 (2열 레이아웃) ──
// 작은 이미지를 텍스트 옆에 나란히 배치합니다.
// img-width: 이미지 열 너비 비율 (0.0~1.0), 나머지가 텍스트 열
#let side-image(path, body, img-width: 0.35, gap: 16pt) = {
  v(8pt)
  grid(
    columns: (img-width * 100% - gap / 2, 1fr),
    column-gutter: gap,
    align: (center + horizon, left + top),
    image(path, width: 100%),
    body,
  )
  v(8pt)
}

// ══════════════════════════════════════
// 표지
// ══════════════════════════════════════
#page(numbering: none, header: none, footer: none)[
  #v(1fr)
  #align(center)[
    // 상단 장식선
    #line(length: 40%, stroke: 2pt + rgb("#2563eb"))
    #v(24pt)
    #text(42pt, weight: "bold", fill: rgb("#1e40af"), tracking: 2pt)[#book-title]
    #v(16pt)
    #line(length: 60%, stroke: 0.5pt + rgb("#93c5fd"))
    #v(16pt)
    #text(15pt, fill: rgb("#374151"), weight: "medium")[#book-subtitle]
    #v(48pt)
    #block(
      width: 70%,
      inset: (x: 20pt, y: 16pt),
      radius: 4pt,
      fill: rgb("#f8fafc"),
      stroke: 0.5pt + rgb("#e2e8f0"),
      text(10.5pt, fill: rgb("#64748b"))[#book-description]
    )
  ]
  #v(1fr)
  #align(center)[
    #text(9pt, fill: rgb("#94a3b8"))[RAG 실전 가이드]
  ]
  #v(20pt)
]

// ══════════════════════════════════════
// 목차 (자동 생성)
// ══════════════════════════════════════
#page(numbering: none, header: none, footer: none)[
  #v(30pt)
  #block(width: 100%, below: 12pt, {
    text(24pt, weight: "bold", fill: rgb("#1a1a1a"))[목차]
    v(6pt)
    line(length: 100%, stroke: 3pt + rgb("#2563eb"))
  })
  #v(12pt)

  #show outline.entry.where(level: 1): set text(weight: "bold", size: 11pt)
  #show outline.entry.where(level: 1): it => {
    v(6pt)
    it
  }
  #show outline.entry.where(level: 3): set text(size: 8.5pt, fill: rgb("#6b7280"))

  #outline(
    title: none,
    indent: 1.5em,
    depth: 2,
  )
]

// ══════════════════════════════════════
// 본문 시작 — 이 아래에 Pandoc 변환 내용이 들어갑니다
// ══════════════════════════════════════

// ── book_base 템플릿 ──

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
