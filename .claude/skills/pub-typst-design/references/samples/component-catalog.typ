// ── 디자인 컴포넌트 카탈로그 ──
// 각 컴포넌트의 Design 1 / Design 2를 나란히 비교합니다.
// 사용법: typst compile component-catalog.typ component-catalog.pdf --font-path ~/Library/Fonts

#set page(
  width: 188mm,
  height: 257mm,
  margin: (top: 20mm, bottom: 28mm, left: 20mm, right: 20mm),
  numbering: "1",
  number-align: center,
)

#set text(
  font: ("RIDIBatang", "Apple SD Gothic Neo"),
  size: 9pt,
  lang: "ko",
  fill: rgb("#1a1a1a"),
)

#set par(leading: 0.8em, justify: true)

// ── 헬퍼 ──
#let label-box(number, name, desc) = {
  block(
    width: 100%,
    inset: (x: 12pt, y: 8pt),
    fill: rgb("#f0f4ff"),
    radius: 4pt,
    stroke: 1pt + rgb("#2563eb"),
    {
      text(12pt, weight: "bold", fill: rgb("#1e40af"))[#number. #name]
      h(8pt)
      text(9pt, fill: rgb("#6b7280"))[#desc]
    }
  )
}

#let divider() = {
  v(4pt)
  line(length: 100%, stroke: 0.5pt + rgb("#e5e7eb"))
  v(4pt)
}

#let sample-text = [사내 AI 비서 시스템은 RAG(Retrieval-Augmented Generation) 기술을 활용하여 사내 문서에서 정확한 답변을 제공합니다. FastAPI로 백엔드를 구성하고, ChromaDB에 문서를 벡터화하여 저장합니다.]

// ══════════════════════════════════════
// 표지
// ══════════════════════════════════════
#page(numbering: none)[
  #v(1fr)
  #align(center)[
    #line(length: 40%, stroke: 2pt + rgb("#2563eb"))
    #v(24pt)
    #text(32pt, weight: "bold", fill: rgb("#1e40af"))[디자인 컴포넌트 카탈로그]
    #v(16pt)
    #line(length: 60%, stroke: 0.5pt + rgb("#93c5fd"))
    #v(16pt)
    #text(12pt, fill: rgb("#374151"))[각 컴포넌트의 디자인 옵션을 비교합니다]
    #v(48pt)
    #block(
      width: 80%,
      inset: (x: 20pt, y: 16pt),
      radius: 4pt,
      fill: rgb("#f8fafc"),
      stroke: 0.5pt + rgb("#e2e8f0"),
    )[
      #text(9pt, fill: rgb("#64748b"))[
        PDF 빌드 시 `--design` 옵션으로 컴포넌트별 디자인을 선택할 수 있습니다.\
        프리셋: `--design 1` (클래식 블루) / `--design 2` (컴팩트 모노)\
        믹스매치: `--design "body=2,heading=1,code=2,table=2"`
      ]
    ]
  ]
  #v(1fr)
]

// ══════════════════════════════════════
// 프리셋 요약
// ══════════════════════════════════════
#page(numbering: none)[
  #v(20pt)
  #text(20pt, weight: "bold")[프리셋 요약]
  #v(8pt)
  #line(length: 100%, stroke: 2pt + rgb("#2563eb"))
  #v(16pt)

  #table(
    columns: (80pt, 1fr, 1fr),
    stroke: 0.5pt + rgb("#d1d5db"),
    inset: (x: 10pt, y: 8pt),
    fill: (_, y) => if y == 0 { rgb("#1e40af") } else { white },
    table.cell(fill: rgb("#1e40af"))[#text(fill: white, weight: "bold")[컴포넌트]],
    table.cell(fill: rgb("#1e40af"))[#text(fill: white, weight: "bold")[1. 클래식 블루]],
    table.cell(fill: rgb("#1e40af"))[#text(fill: white, weight: "bold")[2. 컴팩트 모노]],
    [본문], [10pt, 행간 1.0em], [8pt, 행간 8pt],
    [챕터 오프닝], [상단 60pt 여백 + 26pt 제목], [여백 없음 + 16pt 제목],
    [제목], [h2: 파란 좌측바, h3: 13pt], [h2: 10pt 심플, h3: 10pt],
    [코드블록], [둥근 테두리 박스 (radius 8pt)], [위아래 회색 실선],
    [인라인코드], [회색 배경 박스], [볼드 텍스트만],
    [인용], [파란 좌측선 + 연한 배경], [점선 박스],
    [표], [파란 헤더 + 흰 글씨], [회색 헤더 + 검정 글씨],
    [목차], [depth: 2], [depth: 3],
    [이미지 테두리], [#text(size: 7.5pt)[plain / bordered / shadow / bordered-shadow / minimal]], [#text(size: 7.5pt)[디자인 공통 (image\_border\_preset으로 제어)]],
    [이미지 레이아웃], [#text(size: 7.5pt)[auto-image / side-image / dual-image]], [#text(size: 7.5pt)[디자인 공통 (함수 파라미터로 제어)]],
  )
]

// ══════════════════════════════════════
// 챕터 오프닝 (chapter_opening)
// ══════════════════════════════════════
#pagebreak()
#label-box("챕터 오프닝", "chapter_opening", "챕터 시작 페이지 레이아웃 (h1)")
#v(12pt)

#text(11pt, weight: "bold", fill: rgb("#1e40af"))[챕터 오프닝 1 — 클래식 블루 (넓은 여백)]
#v(6pt)
#block(
  width: 100%,
  height: 200pt,
  inset: 12pt,
  stroke: 0.5pt + rgb("#d1d5db"),
  radius: 4pt,
  fill: white,
)[
  // 상단 여백 시뮬레이션
  #v(50pt)
  #block(width: 100%, below: 16pt, {
    text(26pt, weight: "bold", fill: rgb("#1a1a1a"))[Ch.1: 환각과 RAG의 첫 만남]
    v(8pt)
    line(length: 100%, stroke: 3pt + rgb("#2563eb"))
  })
  #v(8pt)
  #block(
    width: 100%,
    inset: (left: 10pt, y: 6pt),
    stroke: (left: 2pt + rgb("#93b4e8")),
    fill: rgb("#f5f8ff"),
    radius: (right: 4pt),
  )[
    #text(8pt, fill: rgb("#4b5563"))[
      한 줄 요약: LLM은 우리 회사 문서를 읽은 적이 없다.\
      핵심 개념: LLM 환각, Context Injection, RAG
    ]
  ]
]
#v(4pt)
#text(8pt, fill: rgb("#6b7280"))[상단 60pt 여백으로 출판 표준의 여유로운 챕터 시작. 26pt 큰 제목 + 파란 밑줄.]

#v(16pt)

#text(11pt, weight: "bold", fill: rgb("#1e40af"))[챕터 오프닝 2 — 컴팩트 모노 (최소 여백)]
#v(6pt)
#block(
  width: 100%,
  height: 200pt,
  inset: 12pt,
  stroke: 0.5pt + rgb("#d1d5db"),
  radius: 4pt,
  fill: white,
)[
  // 여백 없이 바로 시작
  #block(width: 100%, below: 8pt, {
    text(16pt, weight: "bold", fill: rgb("#1a1a1a"))[Ch.1: 환각과 RAG의 첫 만남]
    v(8pt)
    line(length: 100%, stroke: 3pt + rgb("#2563eb"))
  })
  #v(4pt)
  #block(
    width: 100%,
    inset: (x: 10pt, y: 6pt),
    stroke: (dash: "dashed", paint: rgb("#aaaaaa"), thickness: 1pt),
  )[
    #text(8pt, fill: rgb("#333333"))[
      한 줄 요약: LLM은 우리 회사 문서를 읽은 적이 없다.\
      핵심 개념: LLM 환각, Context Injection, RAG
    ]
  ]
  #v(8pt)
  #text(8pt)[사내 AI 비서 시스템은 RAG 기술을 활용하여 사내 문서에서 정확한 답변을 제공합니다. FastAPI로 백엔드를 구성하고, ChromaDB에 문서를 벡터화하여 저장합니다. 이 챕터에서는 LLM 환각의 원인을 살펴보고 RAG가 이를 어떻게 해결하는지 알아봅니다.]
]
#v(4pt)
#text(8pt, fill: rgb("#6b7280"))[상단 여백 없이 바로 시작. 16pt 제목 + 본문이 곧바로 이어져 페이지 활용 극대화.]

// ══════════════════════════════════════
// 본문 (body)
// ══════════════════════════════════════
#pagebreak()
#label-box("본문", "body", "글꼴 크기, 행간, 자간")
#v(12pt)

#text(11pt, weight: "bold", fill: rgb("#1e40af"))[본문 1 — 클래식 블루 (10pt, leading 1.0em)]
#v(6pt)
#block(
  width: 100%,
  inset: 12pt,
  stroke: 0.5pt + rgb("#d1d5db"),
  radius: 4pt,
)[
  #set text(size: 10pt)
  #set par(leading: 1.0em, justify: true)
  #sample-text
]

#v(16pt)
#text(11pt, weight: "bold", fill: rgb("#1e40af"))[본문 2 — 컴팩트 모노 (8pt, leading 8pt)]
#v(6pt)
#block(
  width: 100%,
  inset: 12pt,
  stroke: 0.5pt + rgb("#d1d5db"),
  radius: 4pt,
)[
  #set text(size: 8pt)
  #set par(leading: 8pt, justify: true)
  #sample-text
]

// ══════════════════════════════════════
// 제목 (heading)
// ══════════════════════════════════════
#pagebreak()
#label-box("제목", "heading", "h2~h4 스타일 (h1은 챕터 오프닝)")
#v(12pt)

#text(11pt, weight: "bold", fill: rgb("#1e40af"))[제목 1 — 클래식 블루]
#v(6pt)
#block(
  width: 100%,
  inset: 12pt,
  stroke: 0.5pt + rgb("#d1d5db"),
  radius: 4pt,
)[
  // h2
  #block(
    width: 100%,
    below: 8pt,
    inset: (left: 12pt),
    stroke: (left: 4pt + rgb("#2563eb")),
    text(16pt, weight: "bold", fill: rgb("#1e40af"))[환경 설정]
  )
  // h3
  #v(8pt)
  #text(13pt, weight: "semibold", fill: rgb("#1e3a5f"))[Python 설치]
  #v(6pt)
  // h4
  #text(11pt, weight: "semibold", fill: rgb("#374151"))[가상환경 생성]
]

#v(16pt)
#text(11pt, weight: "bold", fill: rgb("#1e40af"))[제목 2 — 컴팩트 모노]
#v(6pt)
#block(
  width: 100%,
  inset: 12pt,
  stroke: 0.5pt + rgb("#d1d5db"),
  radius: 4pt,
)[
  // h2
  #text(10pt, weight: "bold", fill: rgb("#1a1a1a"))[환경 설정]
  #v(6pt)
  // h3
  #text(10pt, weight: "semibold", fill: rgb("#374151"))[Python 설치]
  #v(6pt)
  // h4
  #text(10pt, weight: "medium", fill: rgb("#555555"))[가상환경 생성]
]

// ══════════════════════════════════════
// 코드블록 (code)
// ══════════════════════════════════════
#pagebreak()
#label-box("코드블록", "code", "블록 코드 스타일")
#v(12pt)

#text(11pt, weight: "bold", fill: rgb("#1e40af"))[코드블록 1 — 클래식 블루 (둥근 테두리)]
#v(6pt)
#block(
  width: 100%,
  fill: white,
  inset: (x: 16pt, y: 14pt),
  radius: 8pt,
  stroke: 1pt + rgb("#d1d5db"),
)[
  #set text(size: 8pt, weight: "bold", font: ("D2Coding", "RIDIBatang"))
  ```python
  from fastapi import FastAPI
  from langchain.vectorstores import Chroma

  app = FastAPI()
  vectorstore = Chroma(persist_directory="./chroma_db")
  ```
]

#v(16pt)
#text(11pt, weight: "bold", fill: rgb("#1e40af"))[코드블록 2 — 컴팩트 모노 (위아래 실선)]
#v(6pt)
#line(length: 100%, stroke: 2pt + rgb("#999999"))
#block(
  width: 100%,
  fill: white,
  inset: (x: 16pt, y: 6pt),
)[
  #set text(size: 6pt, weight: "bold", font: ("D2Coding", "RIDIBatang"))
  ```python
  from fastapi import FastAPI
  from langchain.vectorstores import Chroma

  app = FastAPI()
  vectorstore = Chroma(persist_directory="./chroma_db")
  ```
]
#line(length: 100%, stroke: 2pt + rgb("#999999"))

// ══════════════════════════════════════
// 인라인 코드 (inline_code)
// ══════════════════════════════════════
#v(24pt)
#label-box("인라인코드", "inline_code", "본문 내 코드 조각")
#v(12pt)

#text(11pt, weight: "bold", fill: rgb("#1e40af"))[인라인코드 1 — 클래식 블루 (회색 배경)]
#v(6pt)
#block(
  width: 100%,
  inset: 12pt,
  stroke: 0.5pt + rgb("#d1d5db"),
  radius: 4pt,
)[
  FastAPI에서 #box(fill: rgb("#f3f4f6"), inset: (x: 4pt, y: 2pt), radius: 3pt, text(size: 8.5pt, fill: rgb("#1e40af"), font: ("D2Coding", "RIDIBatang"))[vectorstore.similarity_search()]) 메서드를 호출하면 유사도 검색이 실행됩니다.
]

#v(12pt)
#text(11pt, weight: "bold", fill: rgb("#1e40af"))[인라인코드 2 — 컴팩트 모노 (볼드)]
#v(6pt)
#block(
  width: 100%,
  inset: 12pt,
  stroke: 0.5pt + rgb("#d1d5db"),
  radius: 4pt,
)[
  FastAPI에서 #text(weight: "bold", fill: rgb("#1e3a5f"), font: ("D2Coding", "RIDIBatang"))[vectorstore.similarity_search()] 메서드를 호출하면 유사도 검색이 실행됩니다.
]

// ══════════════════════════════════════
// 인용 (quote)
// ══════════════════════════════════════
#pagebreak()
#label-box("인용", "quote", "blockquote + callout-box")
#v(12pt)

#text(11pt, weight: "bold", fill: rgb("#1e40af"))[인용 1 — 클래식 블루 (파란 좌측선)]
#v(6pt)
#block(
  width: 100%,
  above: 10pt,
  below: 10pt,
  inset: (left: 14pt, right: 14pt, top: 10pt, bottom: 10pt),
  stroke: (left: 3pt + rgb("#93b4e8")),
  fill: rgb("#f5f8ff"),
  radius: (right: 4pt),
)[
  #set par(justify: true, leading: 0.9em)
  #text(size: 9pt, fill: rgb("#4b5563"))[RAG는 LLM이 외부 지식을 참조하여 답변하는 기술입니다. 환각(Hallucination)을 줄이고 최신 정보를 반영할 수 있습니다.]
]

#v(12pt)
#text(11pt, weight: "bold", fill: rgb("#1e40af"))[인용 2 — 컴팩트 모노 (점선 박스)]
#v(6pt)
#block(
  width: 100%,
  above: 10pt,
  below: 10pt,
  inset: (x: 14pt, y: 10pt),
  stroke: (dash: "dashed", paint: rgb("#aaaaaa"), thickness: 1pt),
  radius: 0pt,
)[
  #set par(justify: true, leading: 0.9em)
  #text(fill: rgb("#333333"))[RAG는 LLM이 외부 지식을 참조하여 답변하는 기술입니다. 환각(Hallucination)을 줄이고 최신 정보를 반영할 수 있습니다.]
]

#v(16pt)
#text(10pt, weight: "semibold", fill: rgb("#374151"))[callout-box (Design 2 전용 함수, Design 1에서도 호환)]
#v(6pt)
#block(
  width: 100%,
  above: 10pt,
  below: 10pt,
  inset: (x: 14pt, y: 10pt),
  fill: rgb("#f5f5f5"),
  radius: 4pt,
  stroke: none,
)[
  #set par(justify: true, leading: 0.9em)
  #text(weight: "bold", fill: rgb("#2563eb"))[참고] #text(fill: rgb("#333333"))[callout-box는 라벨이 있는 인용 블록입니다. 두 디자인 모두에서 사용 가능합니다.]
]

// ══════════════════════════════════════
// 표 (table)
// ══════════════════════════════════════
#pagebreak()
#label-box("표", "table", "표 헤더 + 셀 스타일")
#v(12pt)

#text(11pt, weight: "bold", fill: rgb("#1e40af"))[표 1 — 클래식 블루 (파란 헤더)]
#v(6pt)
#{
  set text(size: 8.5pt)
  table(
    columns: (1fr, 1fr, 1fr),
    stroke: (bottom: 0.5pt + rgb("#e5e7eb")),
    inset: (x: 10pt, y: 8pt),
    fill: (_, y) => if y == 0 { rgb("#1e40af") } else if calc.odd(y) { rgb("#f8fafc") } else { white },
    table.cell(fill: rgb("#1e40af"))[#text(fill: white, weight: "medium")[도구]],
    table.cell(fill: rgb("#1e40af"))[#text(fill: white, weight: "medium")[역할]],
    table.cell(fill: rgb("#1e40af"))[#text(fill: white, weight: "medium")[버전]],
    [FastAPI], [백엔드 API], [0.104],
    [LangChain], [LLM 프레임워크], [0.1.x],
    [ChromaDB], [벡터 저장소], [0.4.x],
  )
}

#v(16pt)
#text(11pt, weight: "bold", fill: rgb("#1e40af"))[표 2 — 컴팩트 모노 (회색 헤더)]
#v(6pt)
#{
  set text(size: 8pt)
  set par(justify: false)
  table(
    columns: (1fr, 1fr, 1fr),
    stroke: 0.5pt + rgb("#d1d5db"),
    inset: (x: 10pt, y: 8pt),
    align: left,
    fill: (_, y) => if y == 0 { rgb("#e5e5e5") } else if calc.odd(y) { rgb("#fafafa") } else { white },
    table.cell(fill: rgb("#e5e5e5"))[#text(fill: rgb("#1a1a1a"), weight: "bold")[도구]],
    table.cell(fill: rgb("#e5e5e5"))[#text(fill: rgb("#1a1a1a"), weight: "bold")[역할]],
    table.cell(fill: rgb("#e5e5e5"))[#text(fill: rgb("#1a1a1a"), weight: "bold")[버전]],
    [FastAPI], [백엔드 API], [0.104],
    [LangChain], [LLM 프레임워크], [0.1.x],
    [ChromaDB], [벡터 저장소], [0.4.x],
  )
}

// ══════════════════════════════════════
// 목차 (toc) — 설명만
// ══════════════════════════════════════
#v(24pt)
#label-box("목차", "toc", "outline depth 차이")
#v(12pt)

#block(
  width: 100%,
  inset: 12pt,
  stroke: 0.5pt + rgb("#d1d5db"),
  radius: 4pt,
)[
  #text(10pt, weight: "bold")[목차 1] — depth: 2 (h1, h2까지 표시)\
  #text(10pt, weight: "bold")[목차 2] — depth: 3 (h1, h2, h3까지 표시)\
  \
  #text(9pt, fill: rgb("#6b7280"))[목차 스타일은 동일하며, 표시 깊이만 다릅니다. 실제 목차는 빌드된 PDF에서 확인할 수 있습니다.]
]

// ══════════════════════════════════════
// 이미지 테두리 (image border)
// ══════════════════════════════════════
#pagebreak()
#label-box("이미지 테두리", "image_border", "auto-image의 style 파라미터")
#v(8pt)

#text(9pt, fill: rgb("#6b7280"))[빌드 시 `image_border_preset` 설정으로 프로젝트 전체에 적용합니다. 개념도(gemini/)와 나머지(terminal/diagram/)에 각각 다른 style이 매핑됩니다.]
#v(12pt)

// ── plain ──
#text(10pt, weight: "bold", fill: rgb("#1e40af"))[1. plain — 효과 없음 (기본값)]
#v(4pt)
#align(center, image("sample-diagram.png", width: 55%))

#v(12pt)

// ── bordered ──
#text(10pt, weight: "bold", fill: rgb("#1e40af"))[2. bordered — 프라이머리 컬러 테두리]
#v(4pt)
#align(center, block(
  stroke: 2pt + rgb("#2563eb"),
  radius: 4pt,
  clip: true,
  image("sample-diagram.png", width: 55%)
))

#v(12pt)

// ── shadow ──
#text(10pt, weight: "bold", fill: rgb("#1e40af"))[3. shadow — 그림자 효과]
#v(4pt)
#align(center, block(
  stroke: (
    left: 0.5pt + rgb("#e0e0e0"),
    top: 0.5pt + rgb("#e0e0e0"),
    right: 2pt + rgb("#c0c0c0"),
    bottom: 2pt + rgb("#c0c0c0"),
  ),
  radius: 4pt,
  clip: true,
  image("sample-diagram.png", width: 55%)
))

#pagebreak()
#label-box("이미지 테두리", "image_border", "계속")
#v(12pt)

// ── bordered-shadow ──
#text(10pt, weight: "bold", fill: rgb("#1e40af"))[4. bordered-shadow — 테두리 + 그림자]
#v(4pt)
#align(center, block(
  stroke: (
    left: 2pt + rgb("#2563eb"),
    top: 2pt + rgb("#2563eb"),
    right: 3pt + rgb("#1d4ed8"),
    bottom: 3pt + rgb("#1d4ed8"),
  ),
  radius: 4pt,
  clip: true,
  image("sample-diagram.png", width: 55%)
))

#v(12pt)

// ── minimal ──
#text(10pt, weight: "bold", fill: rgb("#1e40af"))[5. minimal — 얇은 회색 테두리]
#v(4pt)
#align(center, block(
  stroke: 0.5pt + rgb("#e5e7eb"),
  radius: 2pt,
  clip: true,
  image("sample-diagram.png", width: 55%)
))

#v(16pt)

// ── 프리셋 매핑 표 ──
#text(11pt, weight: "bold")[프리셋 → style 매핑]
#v(6pt)
#{
  set text(size: 8.5pt)
  table(
    columns: (1fr, 1fr, 1fr),
    stroke: (bottom: 0.5pt + rgb("#e5e7eb")),
    inset: (x: 10pt, y: 8pt),
    fill: (_, y) => if y == 0 { rgb("#1e40af") } else if calc.odd(y) { rgb("#f8fafc") } else { white },
    table.cell(fill: rgb("#1e40af"))[#text(fill: white, weight: "medium")[프리셋명]],
    table.cell(fill: rgb("#1e40af"))[#text(fill: white, weight: "medium")[개념도 (gemini/)]],
    table.cell(fill: rgb("#1e40af"))[#text(fill: white, weight: "medium")[나머지]],
    [clean-border], [bordered], [minimal],
    [shadow], [shadow], [shadow],
    [primary-shadow], [bordered-shadow], [shadow],
    [minimal], [minimal], [minimal],
  )
}

// ══════════════════════════════════════
// 이미지 레이아웃 (image layout)
// ══════════════════════════════════════
#pagebreak()
#label-box("이미지 레이아웃", "image_layout", "auto-image / side-image / dual-image")
#v(12pt)

#text(11pt, weight: "bold", fill: rgb("#1e40af"))[레이아웃 1 — 1열 기본 (auto-image)]
#v(4pt)
#text(9pt, fill: rgb("#6b7280"))[가장 기본적인 배치. 이미지가 페이지 너비의 일정 비율을 차지하며, 남은 공간에 맞춰 자동 축소됩니다.]
#v(8pt)
#align(center, block(
  stroke: 0.5pt + rgb("#e5e7eb"),
  radius: 4pt,
  clip: true,
  image("sample-diagram.png", width: 70%)
))
#align(center, text(8pt, fill: rgb("#6b7280"))[LLM 단독 vs RAG 비교])

#v(20pt)

#text(11pt, weight: "bold", fill: rgb("#1e40af"))[레이아웃 2 — 텍스트 + 이미지 (side-image)]
#v(4pt)
#text(9pt, fill: rgb("#6b7280"))[작은 이미지를 텍스트 옆에 나란히 배치합니다. 비유 이미지에 적합합니다.]
#v(8pt)
#grid(
  columns: (45%, 1fr),
  column-gutter: 16pt,
  align: (center + horizon, left + top),
  image("sample-diagram.png", width: 100%),
  [
    #text(9pt)[
      왼쪽 경로는 LLM 단독 방식입니다. 질문이 바로 LLM에 들어가고, 학습 데이터만으로 답변합니다. 사내 문서에 대한 질문에는 환각이 발생합니다.

      오른쪽 경로는 RAG 방식입니다. 질문이 먼저 검색 엔진을 거쳐 벡터DB에서 관련 문서를 찾고, 이를 LLM에 컨텍스트로 전달하여 정확한 답변을 생성합니다.
    ]
  ],
)

#v(20pt)

#text(11pt, weight: "bold", fill: rgb("#1e40af"))[레이아웃 3 — 이미지 2개 나란히 (dual-image)]
#v(4pt)
#text(9pt, fill: rgb("#6b7280"))[이미지 두 개를 좌우로 나란히 배치합니다. 비교 설명에 적합합니다.]
#v(8pt)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 16pt,
  align: center,
  [
    #block(
      stroke: 0.5pt + rgb("#e5e7eb"),
      radius: 4pt,
      clip: true,
      image("sample-diagram.png", width: 100%)
    )
    #v(4pt)
    #text(8pt, fill: rgb("#6b7280"))[LLM 단독 vs RAG 비교]
  ],
  [
    #block(
      stroke: 2pt + rgb("#2563eb"),
      radius: 4pt,
      clip: true,
      image("sample-diagram.png", width: 100%)
    )
    #v(4pt)
    #text(8pt, fill: rgb("#6b7280"))[같은 이미지, bordered 스타일 적용]
  ],
)

#v(20pt)

// ── 레이아웃 함수 요약 ──
#text(11pt, weight: "bold")[레이아웃 함수 요약]
#v(6pt)
#{
  set text(size: 8.5pt)
  table(
    columns: (1fr, 1.5fr, 1.5fr),
    stroke: (bottom: 0.5pt + rgb("#e5e7eb")),
    inset: (x: 10pt, y: 8pt),
    fill: (_, y) => if y == 0 { rgb("#1e40af") } else if calc.odd(y) { rgb("#f8fafc") } else { white },
    table.cell(fill: rgb("#1e40af"))[#text(fill: white, weight: "medium")[함수]],
    table.cell(fill: rgb("#1e40af"))[#text(fill: white, weight: "medium")[용도]],
    table.cell(fill: rgb("#1e40af"))[#text(fill: white, weight: "medium")[파라미터]],
    [`auto-image`], [1열 이미지 (기본)], [max-width, style, alt],
    [`side-image`], [텍스트 + 이미지 2열], [img-width (기본 35%), gap],
    [`dual-image`], [이미지 2개 나란히], [caption1, caption2, gap],
  )
}
