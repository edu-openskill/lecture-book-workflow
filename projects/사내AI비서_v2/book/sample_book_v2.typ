// ── 사내AI비서_v2 프로젝트 설정 ──
#let book-title = "사내 AI 비서"
#let book-subtitle = "환각부터 평가까지, RAG의 모든 것"
#let book-description = [FastAPI + LangChain + ChromaDB로 만드는 사내 AI 비서. 환각 체험에서 시작해 검색 품질 평가까지, 하나의 프로젝트로 RAG 전체 여정을 경험합니다.]
#let book-header-title = "사내 AI 비서"

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
// 이미지가 남은 공간보다 크면 자동 축소, 너무 작아지면 다음 페이지로 넘김
#let auto-image(path, alt: none, max-width: 0.7) = layout(size => context {
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

  if alt != none {
    figure(image(path, width: final-width), caption: [#alt])
  } else {
    align(center, image(path, width: final-width))
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

= Ch.1: 질문을 던지면 답이 온다
<ch.1-질문을-던지면-답이-온다>
#quote(block: true)[
한 줄 요약: AI 비서는 질문을 받아 문서에서 답을 찾아주는 시스템입니다. 핵심 개념: RAG, 임베딩, 벡터 검색
]

#v(12pt)
#line(length: 100%, stroke: 0.5pt + rgb("#e5e7eb"))
#v(12pt)

회의가 끝나고 자리로 돌아왔습니다. #strong[팀장] 이 슬랙에 메시지를 남겼습니다.

#strong[팀장]: "지난달 인사 규정 변경된 거 정리해서 보내줘. 오늘 중으로."

문서함을 뒤졌습니다. 공유 드라이브, 위키, 메일 첨부파일. 30분이 지나도 원본을 못 찾았습니다. (이런 일이 한두 번이 아닌데.)

같은 질문을 슬랙 봇에 던졌다고 상상해봅시다. 3초 만에 해당 문서의 정확한 단락이 돌아옵니다. 이것이 #strong[RAG(검색 증강 생성)] 의 힘입니다.

도서관 사서를 떠올려 보세요. 질문을 받으면 서가에서 관련 책을 찾고, 해당 페이지를 펴서 답을 읽어줍니다. RAG도 같은 원리입니다. 다만 서가 대신 #strong[벡터 데이터베이스] 를, 사서 대신 #strong[LLM] 을 사용합니다.

=== 이것만은 기억하자
<이것만은-기억하자>
- RAG는 "검색 + 생성"입니다. 검색이 정확해야 생성도 정확합니다.
- 다음 챕터에서는 이 사서에게 책을 꽂아주는 작업, 즉 문서를 벡터로 변환하는 #strong[임베딩] 을 다룹니다.

#v(12pt)
#line(length: 100%, stroke: 0.5pt + rgb("#e5e7eb"))
#v(12pt)

이제 직접 만들어 보겠습니다.

== 기술 파트
<기술-파트>
=== 용어 정리
<용어-정리>
#figure(
  align(center)[#table(
    columns: 3,
    align: (auto,auto,auto,),
    table.header([이야기 속 비유], [진짜 용어], [정식 정의],),
    table.hline(),
    [도서관 사서], [LLM], [대규모 언어 모델. 텍스트를 이해하고 생성합니다],
    [서가에서 책 찾기], [벡터 검색], [의미 유사도 기반 문서 검색],
    [책을 서가에 꽂기], [임베딩], [텍스트를 숫자 벡터로 변환],
  )]
  , kind: table
  )

=== 이번 챕터 파일 구조
<이번-챕터-파일-구조>
```
v0.1/
├── main.py        [실습] 메인 진입점
├── config.py      [설명] 환경 설정
└── README.md      [참고] 프로젝트 설명
```

=== 실습: main.py
<실습-main.py>
아래 코드를 `main.py`에 작성합니다.

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

question = "지난달 인사 규정 변경 사항이 뭐야?"
response = llm.invoke(question)
print(response.content)
```

이 코드는 아직 RAG가 아닙니다. 단순히 LLM에게 질문을 던질 뿐입니다. LLM은 학습 데이터에 없는 사내 규정을 알 수 없으므로, 엉뚱한 답을 만들어냅니다.

=== 더 알아보기
<더-알아보기>
- LangChain 공식 문서의 RAG 튜토리얼
- OpenAI Embeddings API 가이드
