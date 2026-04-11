// ── 사내AI비서_v2 프로젝트 설정 ──
#let book-title = "환각에서 시작하는 RAG"
#let book-subtitle = "사내 AI 비서를 만들며 배우는 검색 증강 생성"
#let book-description = [FastAPI + LangChain + ChromaDB로 만드는 사내 AI 비서. 환각 체험에서 시작해 검색 품질 평가까지, 하나의 프로젝트로 RAG 전체 여정을 경험합니다.]
#let book-header-title = "환각에서 시작하는 RAG"
#let book-authors = "최주호, 류재성, 김주혁"
#let book-series = "특이점이 온 개발자"
#let book-series-sub = "개념편"
#let book-badges = ("RAG", "LangChain", "ChromaDB", "FastAPI", "LLM", "임베딩", "리랭킹", "HyDE", "Vision LLM")
#let book-publisher = "오픈스킬북스"
#let book-cover-image = "/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/cover.png"

// 조판 설정 변수 — 기본값은 Design 1 (클래식 블루)
// Design 2에서 body_d2.typ 상단에서 재정의. D1 파일은 값을 직접 사용 (기본값과 동일하므로)
// 소비자: _variant/body_d2.typ(재정의), _variant/heading_d2.typ, _variant/code_d2.typ

// 행간: 줄과 줄 사이 간격
#let body-leading = 1.0em
// 문단 간격: 문단과 문단 사이 간격 (heading/code/table에는 영향 없음)
#let paragraph-gap = 0pt
// 자간: 글자와 글자 사이 간격 (0pt = 기본)
#let body-tracking = 0pt
// 제목-문단 간격: 제목 아래 본문까지의 여백
#let heading-gap = 16pt
// 코드 블록: 구분선과 코드 사이 여백
#let code-inset-x = 16pt
#let code-inset-y = 14pt
// 코드 블록: 구분선 두께
#let code-rule-stroke = 1pt
// 코드 블록: 위아래 여백 — componentStyles 오버라이드 대상
#let code-margin-top = 8pt
#let code-margin-bottom = 8pt

// 제목 크기 — 에디터 오버라이드 대상
#let h1-size = 26pt
#let h2-size = 16pt
#let h3-size = 13pt
#let h4-size = 11pt
// 코드 블록 크기 — 에디터 오버라이드 대상
#let code-size = 8pt
// 인용/표/인라인코드 크기 — 에디터 오버라이드 대상
#let quote-size = 9pt
#let table-size = 8.5pt
#let inline-code-size = 8.5pt
// 목차 깊이 — 에디터 오버라이드 대상
#let toc-depth = 2
// 목차 항목 간격 — 에디터 오버라이드 대상 (문단 간격과 독립)
#let toc-spacing = 4pt

// 색상 변수 — 에디터 오버라이드 대상
#let color-primary = rgb("#2563eb")
#let color-primary-dark = rgb("#1e40af")
#let color-primary-light = rgb("#93c5fd")
#let color-text = rgb("#1a1a1a")
#let color-code-text = rgb("#1e40af")
#let color-quote-bg = rgb("#f5f8ff")
#let color-quote-border = rgb("#93b4e8")

// 제목 스타일 변수 — componentStyles 오버라이드 대상 (기본값 = Design 1)
// 색상 변수 뒤에 위치해야 함 (color-text, color-primary-dark 참조)
#let h1-top = 10pt
#let h1-weight = "bold"
#let h1-fill = color-text
#let h1-below = 14pt
#let h2-top = 24pt
#let h2-below = 14pt
#let h2-weight = "bold"
#let h2-fill = color-primary-dark
#let h2-inset-left = 12pt
#let h3-top = 16pt
#let h3-below = 14pt
#let h3-weight = "semibold"
#let h3-fill = rgb("#1e3a5f")
#let h4-top = 12pt
#let h4-below = 14pt
#let h4-weight = "semibold"
#let h4-fill = rgb("#374151")

// 본문 스타일 변수 — componentStyles 오버라이드 대상
#let strong-fill = rgb("#1e3a5f")
#let emph-fill = rgb("#6b7280")

// 코드블록 스타일 변수
#let code-fill = white
#let code-radius = 8pt
#let code-stroke-width = 1pt
#let code-stroke-color = rgb("#d1d5db")

// 인라인코드 스타일 변수
#let inline-code-fill = rgb("#f3f4f6")
#let inline-code-radius = 3pt
#let inline-code-text-color = color-code-text
#let inline-code-weight = "bold"

// 인용 스타일 변수
#let quote-text-color = rgb("#4b5563")
#let quote-stroke-width = 3pt
#let quote-inset-x = 14pt
#let quote-inset-y = 10pt
#let quote-radius = 4pt
#let quote-margin = 10pt
#let quote-margin-top = 10pt
#let quote-margin-bottom = 10pt

// 표 스타일 변수
#let table-stroke-width = 0.5pt
#let table-stroke-color = rgb("#e5e7eb")
#let table-inset-x = 10pt
#let table-inset-y = 8pt
#let table-header-weight = "medium"
#let table-header-text-color = white
#let table-odd-fill = rgb("#f8fafc")
#let table-margin-top = 0pt
#let table-margin-bottom = 0pt

// 목차 스타일 변수
#let toc-title-size = 24pt
#let toc-title-weight = "bold"
#let toc-title-line-stroke = 3pt
#let toc-level1-size = 11pt
#let toc-level3-size = 8.5pt
#let toc-level3-color = rgb("#6b7280")
#let toc-indent = 1.5em

// Figure 캡션 변수
#let figure-margin-top = 8pt
#let figure-margin-bottom = 4pt
#let figure-caption-gap = 2pt
#let figure-caption-size = 8pt
#let figure-caption-color = rgb("#6b7280")
#let figure-align = "center"

// 이미지 설정 변수 — 에디터 오버라이드 대상
#let img-gemini-width = 0.7
#let img-gemini-style = "bordered"
#let img-terminal-width = 0.7
#let img-terminal-style = "minimal"
#let img-diagram-width = 0.6
#let img-diagram-style = "minimal"
#let img-default-width = 0.6
#let img-default-style = "plain"


// ── Editor Design Overrides (variables) ──
#let color-primary = rgb("#2563eb")
#let color-text = rgb("#1a1a1a")
#let color-code-text = rgb("#1e40af")
#let color-quote-bg = rgb("#f5f8ff")
#let color-primary-dark = color-primary.darken(15%)
#let color-primary-light = color-primary.lighten(40%)
#let color-quote-border = color-quote-bg.darken(30%)
#let img-gemini-width = 0.5
#let img-gemini-style = "shadow"
#let img-terminal-width = 1.0
#let img-terminal-style = "minimal"
#let img-diagram-width = 1.0
#let img-diagram-style = "plain"
#let body-leading = 12pt
#let body-tracking = 0.5pt
#let paragraph-gap = 24pt

// 필수 외부 변수 (book.typ에서 정의):
//   book-title, book-subtitle, book-description, book-header-title

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
        columns: (auto, 1fr),
        column-gutter: 12pt,
        align(left)[#book-header-title],
        align(right, box(clip: true, width: 100%, inset: (y: 2pt))[
          #chapter-title.get()
        ]),
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


// ── Editor Design Overrides (page) ──
#set page(width: 210mm, height: 297mm, margin: (top: 25mm, bottom: 25mm, left: 25mm, right: 22mm))

// ── 본문 스타일: Design 1 (클래식 블루) ──
// ──OVERRIDES──
#set text(
  font: ("RIDIBatang", "Apple SD Gothic Neo"),
  size: 10pt,
  lang: "ko",
  fill: color-text,
)

#set par(
  leading: if body-leading < 4pt { 4pt } else { body-leading },
  spacing: 0pt,
  first-line-indent: 0pt,
  justify: true,
)


// ── Editor Design Overrides (sizes) ──
#set text(size: 12pt)
#set par(leading: 12pt)
#set text(tracking: 0.5pt)
#let h1-size = 16pt
#let h2-size = 14pt
#let h3-size = 13pt
#let h4-size = 13pt
#let code-size = 10pt
#let quote-size = 9pt
#let table-size = 10pt
#let inline-code-size = 12pt
#let toc-depth = 3
#let toc-spacing = 4pt

// ── 챕터 오프닝: Design 1 (클래식 블루) ──
// 넓은 상단 여백 + 큰 제목 + 파란 밑줄. 출판 표준의 여유로운 오프닝.
#show heading.where(level: 1): it => {
  chapter-title.update(it.body)
  pagebreak(weak: true)
  v(60pt)  // 상단 1/3 여백 (출판 표준)
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

// ── 제목 스타일: Design 2 (컴팩트 모노) ──
// D2 변수 재정의
#let h1-below = heading-gap
#let h2-top = 18pt
#let h2-fill = color-text
#let h3-top = 14pt
#let h3-fill = rgb("#374151")
#let h4-top = 10pt
#let h4-below = heading-gap
#let h4-weight = "medium"
#let h4-fill = rgb("#555555")
// ──OVERRIDES──
// ── componentStyles: heading ──
#let h1-top = 0pt
#let h1-weight = 800
#let h1-below = 16pt
#let h2-top = 24pt
#let h2-weight = 700
#let h2-fill = rgb("#3754e1")
#let h2-inset-left = 0pt
#let h2-below = 24pt
#let h3-top = 18pt
#let h3-weight = 700
#let h3-fill = rgb("#001061")
#let h3-below = 10pt
#let h4-top = 12pt
#let h4-weight = 500
#let h4-fill = rgb("#555555")
#let h4-below = 8pt

#show heading.where(level: 1): it => {
  chapter-title.update(it.body)
  counter(figure).update(0)
  pagebreak(weak: true)
  block(above: h1-top, below: h1-below, sticky: true)[
    #text(h1-size, weight: h1-weight, fill: h1-fill)[#it.body]
    #v(8pt)
    #line(length: 100%, stroke: 3pt + color-primary)
  ]
}

#show heading.where(level: 2): it => {
  block(above: h2-top, below: h2-below, width: 100%, sticky: true)[
    #text(h2-size, weight: h2-weight, fill: h2-fill)[#it.body]
  ]
}

#show heading.where(level: 3): it => {
  block(above: h3-top, below: h3-below, sticky: true)[
    #text(h3-size, weight: h3-weight, fill: h3-fill)[#it.body]
  ]
}

#show heading.where(level: 4): it => {
  block(above: h4-top, below: h4-below, sticky: true)[
    #text(h4-size, weight: h4-weight, fill: h4-fill)[#it.body]
  ]
}

// ── 코드 블록: Design 1 (둥근 테두리 박스) ──
// ──OVERRIDES──
// ── componentStyles: code ──
#let code-fill = rgb("#fafafa")
#let code-radius = 10pt

#show raw.where(block: true): it => {
  set text(size: code-size, weight: "bold", font: ("D2Coding", "RIDIBatang"))
  let mt = if code-margin-top < 4pt { 4pt } else { code-margin-top }
  let mb = if code-margin-bottom < 4pt { 4pt } else { code-margin-bottom }
  block(
    width: 100%,
    fill: code-fill,
    inset: (x: code-inset-x, y: code-inset-y),
    radius: code-radius,
    stroke: code-stroke-width + code-stroke-color,
    breakable: true,
    above: mt,
    below: mb,
    text(fill: color-text)[#it]
  )
}

// ── 인라인 코드: Design 2 (볼드 텍스트만) ──
#let inline-code-fill = none
#let inline-code-radius = 0pt
#let inline-code-text-color = rgb("#1e3a5f")
// ──OVERRIDES──
// ── componentStyles: inline_code ──
#let inline-code-weight = 800

#show raw.where(block: false): it => {
  text(weight: inline-code-weight, fill: inline-code-text-color)[#it]
}

// ── 인용 블록: Design 3 (콜아웃 박스 — 회색 배경, 라벨 강조) ──
#let quote-text-color = rgb("#333333")
#let quote-stroke-width = 0pt
#let quote-radius = 4pt
// ──OVERRIDES──
#show quote.where(block: true): it => {
  block(
    width: 100%,
    above: quote-margin-top,
    below: quote-margin-bottom,
    inset: (x: quote-inset-x, y: quote-inset-y),
    fill: rgb("#f5f5f5"),
    radius: quote-radius,
    stroke: none,
    {
      set par(justify: true, leading: 0.9em)
      text(size: quote-size, fill: quote-text-color)[#it.body]
    }
  )
}

// ── callout-box (동일 스타일 + 프라이머리 라벨) ──
#let callout-box(label, body) = {
  block(
    width: 100%,
    above: quote-margin-top,
    below: quote-margin-bottom,
    inset: (x: quote-inset-x, y: quote-inset-y),
    fill: rgb("#f5f5f5"),
    radius: quote-radius,
    stroke: none,
    {
      set par(justify: true, leading: 0.9em)
      if label == [] or label == none {
        text(size: quote-size, fill: quote-text-color)[#body]
      } else {
        text(size: quote-size)[#text(weight: "bold", fill: color-primary)[#label] #text(fill: quote-text-color)[#body]]
      }
    }
  )
}

// ── 표 스타일: Design 2 (회색 헤더, 검정 글씨, 좌측 정렬) ──
#let table-stroke-color = rgb("#d1d5db")
#let table-header-text-color = rgb("#1a1a1a")
#let table-header-weight = "bold"
#let table-odd-fill = rgb("#fafafa")
// ──OVERRIDES──
#set table(
  stroke: table-stroke-width + table-stroke-color,
  inset: (x: table-inset-x, y: table-inset-y),
  align: left,
  fill: (_, y) => if y == 0 { rgb("#e5e5e5") } else if calc.odd(y) { table-odd-fill } else { white },
)

#show table.cell.where(y: 0): set text(fill: table-header-text-color, weight: table-header-weight)

#show table: it => {
  set text(size: table-size)
  set par(justify: false)
  align(left, block(above: table-margin-top, below: table-margin-bottom, breakable: true)[#it])
}

// ── 볼드/이탤릭 ──
// ──OVERRIDES──
// ── componentStyles: figure ──
#let figure-margin-top = 10pt
#let figure-margin-bottom = 16pt
#let figure-caption-gap = 4pt
#let figure-caption-size = 8pt

#show strong: set text(fill: strong-fill)
#show emph: set text(fill: emph-fill)

// ── 수평선은 후처리에서 #v + block으로 변환됨 ──

// ── figure 스타일 (표/이미지 공통) ──
// par(spacing: 0pt) 환경에서 block(below:)가 무시되므로 v()로 명시적 여백 확보
#show figure: it => {
  let fig-align = if figure-align == "left" { left } else if figure-align == "right" { right } else { center }
  v(figure-margin-top)
  block[
    #align(fig-align, it.body)
    #if it.caption != none {
      v(figure-caption-gap)
      let ch = counter(heading.where(level: 1)).get().first()
      let fig-num = counter(figure).display()
      align(fig-align, text(figure-caption-size, fill: figure-caption-color)[그림 #ch\-#fig-num: #it.caption.body])
    }
  ]
  v(figure-margin-bottom)
}

// ── 링크 스타일 ──
#show link: it => {
  text(fill: color-primary)[#it]
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
      stroke: 2pt + color-primary,
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
        left: 2pt + color-primary,
        top: 2pt + color-primary,
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
    let fig-align = if figure-align == "left" { left } else if figure-align == "right" { right } else { center }
    v(figure-margin-top)
    block[#align(fig-align, styled-img)]
    v(figure-margin-bottom)
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

// ── 2열 이미지 (이미지 2개 나란히) ──
// 이미지 두 개를 좌우로 나란히 배치합니다.
// caption1, caption2: 각 이미지의 캡션 (없으면 캡션 없이 배치)
#let dual-image(path1, path2, caption1: none, caption2: none, gap: 16pt) = {
  v(8pt)
  grid(
    columns: (1fr, 1fr),
    column-gutter: gap,
    align: center,
    if caption1 != none { figure(image(path1, width: 100%), caption: [#caption1]) } else { image(path1, width: 100%) },
    if caption2 != none { figure(image(path2, width: 100%), caption: [#caption2]) } else { image(path2, width: 100%) },
  )
  v(8pt)
}

// ══════════════════════════════════════
// 표지 — 이미지 또는 텍스트
// ══════════════════════════════════════
// book.typ에서 정의 필요:
//   필수: book-title, book-subtitle, book-authors, book-header-title
//   선택: book-cover-image, book-series, book-series-sub, book-badges, book-publisher
#if book-cover-image != "" [
  #page(numbering: none, header: none, footer: none, margin: (top: 20pt, bottom: 20pt, left: 16pt, right: 16pt))[
    #image(book-cover-image, width: 100%, height: 100%, fit: "contain")
  ]
] else [
  #page(numbering: none, header: none, footer: none)[
    #v(28pt)
    #if book-series != "" [
      #pad(left: 28pt)[
        #text(10pt, fill: rgb("#94a3b8"), weight: "medium", tracking: 1pt)[
          #book-series
          #if book-series-sub != "" [ · #book-series-sub]
        ]
      ]
    ]
    #v(1fr)
    #align(center)[
      #line(length: 40%, stroke: 2pt + color-primary)
      #v(24pt)
      #text(42pt, weight: "bold", fill: color-primary-dark, tracking: 2pt)[#book-title]
      #v(16pt)
      #line(length: 60%, stroke: 0.5pt + color-primary-light)
      #v(16pt)
      #text(15pt, fill: rgb("#374151"), weight: "medium")[#book-subtitle]
      #v(28pt)
      #if book-badges.len() > 0 [
        #block(width: 85%)[
          #align(center)[
            #for (i, badge) in book-badges.enumerate() {
              box(
                inset: (x: 8pt, y: 4pt),
                radius: 12pt,
                fill: rgb("#f1f5f9"),
                stroke: 0.5pt + rgb("#e2e8f0"),
                text(9pt, fill: rgb("#475569"), weight: "medium")[#badge]
              )
              if i < book-badges.len() - 1 { h(5pt) }
            }
          ]
        ]
        #v(28pt)
      ]
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
      #text(11pt, fill: rgb("#4b5563"), weight: "medium")[#book-authors 지음]
      #v(14pt)
      #if book-publisher != "" [
        #text(9pt, fill: rgb("#9ca3af"), tracking: 1.5pt)[#book-publisher]
      ] else [
        #text(9pt, fill: rgb("#94a3b8"))[#book-header-title]
      ]
    ]
    #v(24pt)
  ]
]


#heading(outlined: false, level: 1)[머릿말]

RAG 관련 자료를 처음 찾아보셨을 때, 혹시 이런 느낌 아니었나요? "LangChain 공식 문서는 있는데… 이걸 어디서 어떻게 시작하지?"

#v(paragraph-gap)
"예제는 따라 했는데, 막상 내 문서를 넣으면 검색이 왜 이렇게 안 되"기본 RAG는 만들었는데, 정확도를 올리려면 뭘 건드려야 하지?”

#v(paragraph-gap)
이 책은 그 질문들에서 시작했습니다.

#heading(outlined: false, level: 2)[이 책에서 만드는 것]

처음부터 끝까지 하나의 프로젝트를 만듭니다.

#v(paragraph-gap)
사내 AI 비서 #strong[ConnectHR]입니다. 직원 정보를 조회하고, 인사 규정 문서를 검색하고, 두 가지를 한 번에 답해주는 시스템입니다. CH01에서 LLM 환각을 체험하고, CH10에서 성적표를 들고 마무리합니다.

#v(paragraph-gap)
조각난 예제가 아닙니다. 처음부터 끝까지, 하나의 프로젝트입니다.

#heading(outlined: false, level: 2)[다른 RAG 자료와 다른 점]

#strong[첫째, 실패부터 시작합니다.]

#v(paragraph-gap)
각 챕터는 잘 동작하는 코드가 아니라, 에러나 한계 상황에서 출발합니다. "왜 이게 안 되지?"를 먼저 경험하고, 그 이유를 찾고, 해결하는 순서입니다. 그 과정이 이해를 만듭니다.

#v(paragraph-gap)
#strong[둘째, 튜닝까지 다룹니다.]

#v(paragraph-gap)
대부분의 RAG 자료는 검색 결과가 나오는 순간 멈춥니다. 이 책은 "왜 엉뚱한 문서를 가져오나", "왜 같은 뜻인데 못 찾나"까지 파고듭니다. 검색 품질 튜닝(CH08), 질문 해석 개선(CH09), 성능 측정(CH10)까지 포함되어 있습니다.

#v(paragraph-gap)
#strong[셋째, 이야기로 읽힙니다.]

#v(paragraph-gap)
API 명세가 아니라 스토리입니다. 팀장의 지시에서 시작해서, 동료의 불만을 들으면서, ConnectHR이 한 단계씩 성장하는 이야기입니다. 비유와 상황으로 먼저 개념을 잡고, 그 다음에 코드로 들어갑니다.

#heading(outlined: false, level: 2)[이 책의 구조]

챕터마다 두 파트로 나뉩니다.

#v(paragraph-gap)
- #strong[이야기 파트] --- 왜 이게 필요한지, 상황으로 먼저 보여줍니다. 코드가 없습니다. 비유로 개념을 잡습니다.
- #strong[기술 파트] --- 비유를 정확한 용어로 정리하고, 코드로 구현합니다.

#v(paragraph-gap)
이야기 파트만 읽어도 흐름이 이해됩니다. 코드가 낯설다면 이야기 파트를 먼저 천천히 읽어보세요. 기술 파트는 그 다음에 와도 늦지 않습니다.

#heading(outlined: false, level: 2)[이 책이 맞는 분]

- Python 기초 문법은 알지만, LLM이나 RAG는 처음인 분
- 예제는 따라 해봤지만, 처음부터 끝까지 하나의 프로젝트를 만들어본 적 없는 분
- "이론은 알겠는데, 실제로 작동하는 걸 보고 싶다"는 분

#heading(outlined: false, level: 2)[마지막으로]

이 책은 정답을 알려주지 않습니다.

#v(paragraph-gap)
에러를 만나고, 왜 그런지 고민하고, 고치는 과정을 함께 걸어갑니다. ConnectHR이 완성될 때쯤이면, 단순히 코드를 복붙한 게 아니라 "왜 이렇게 만들었는지"를 이해하게 됩니다.

#v(paragraph-gap)
그게 이 책이 하고 싶은 것입니다.

#v(paragraph-gap)
자, 이제 시작해보겠습다.

#v(4pt)
#block(width: 100%, height: 0.5pt, fill: rgb("#e5e7eb"))
#v(4pt)

#heading(outlined: false, level: 1)[교육자료]

#heading(outlined: false, level: 2)[1. Git 레포지토리]

이 책에서는 두 개의 Git 레포지토리를 사용합니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([레포], [용도], [주소],),
    table.hline(),
    [#strong[rag-start]], [실습용. import와 데이터가 준비된 파일에 TODO를 채워넣습니다], [`https://github.com/metacoding-18-ai-applied-v4/rag-start`],
    [#strong[rag-end]], [완성 코드. 막히면 여기서 정답을 확인합니다], [`https://github.com/metacoding-18-ai-applied-v4/rag-end`],
  )]
  , kind: table
  )

#heading(outlined: false, level: 3)[1.1 실습 흐름]

+ #strong[rag-start] 레포를 클론합니다.
+ 챕터를 보면서 `[실습]` 파일의 TODO 부분에 코드를 작성합니다.
+ 막히면 #strong[rag-end] 완성 코드를 참고합니다.

```bash
git clone https://github.com/metacoding-18-ai-applied-v4/rag-start.git
cd rag-start
```

#heading(outlined: false, level: 3)[1.2 폴더 구조]

각 챕터는 하나의 예제 폴더에 대응합니다. 챕터를 진행할수록 폴더 번호가 올라가며 시스템이 한 단계씩 성장합니다.

```
rag-start/
├── ex01/    ← CH01: 환각과 RAG의 첫 만남
├── ex02/    ← CH02: 일단 사내 시스템부터
├── ex04/    ← CH04: 문서를 지식으로 바꾸다
├── ex05/    ← CH05: 드디어 답해준다
├── ex06/    ← CH06: 연차도 규정도 한번에
├── ex07/    ← CH07: 실제로 써보니
├── ex08/    ← CH08: 엉뚱한 문서를 가져온다
├── ex09/    ← CH09: 질문을 제대로 이해 못한다
└── ex10/    ← CH10: PDF 이미지까지 잡아라
```

#quote(block: true)[CH03은 이야기 챕터로 코드가 없습니다.]

#heading(outlined: false, level: 3)[1.3 코드 분류]

각 챕터의 코드 파일에는 세 가지 분류가 붙어 있습니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr, 1fr),
    align: (auto,auto,auto,auto,),
    table.header([분류], [의미], [rag-start 상태], [독자 액션],),
    table.hline(),
    [\[실습\]], [챕터 핵심 코드], [import + 데이터 + TODO 주석], [TODO를 채워 코드 작성],
    [\[설명\]], [중요하지만 핵심은 아닌 코드], [완성 코드 그대로], [코드를 읽고 이해],
    [\[참고\]], [이 챕터 주제가 아닌 코드], [완성 코드 그대로], [파일명과 한 줄 설명만 확인],
  )]
  , kind: table
  )

`[실습]` 파일에는 import, 상수, 더미 데이터, 테스트 입력값이 미리 준비되어 있습니다. 챕터를 따라 하며 `# TODO:` 주석 부분만 채워넣으면 됩니다. `[설명]`과 `[참고]` 파일은 실행에 필요한 완성 코드가 이미 들어 있으므로 수정하지 않습니다.

#heading(outlined: false, level: 2)[2. 환경 설정]

#heading(outlined: false, level: 3)[2.1 Python 설치]

이 책의 모든 예제는 Python #strong[3.12] 를 기준으로 작성됐습니다. 3.10\~3.12에서 동작하며 3.13 이상에서는 일부 패키지 호환성 문제가 있을 수 있습니다.

#heading(outlined: false, level: 4)[macOS]

```bash
# Homebrew로 설치
brew install python@3.12
```

#heading(outlined: false, level: 4)[Windows]

공식 사이트(https:/\/www.python.org/downloads/)에서 Python 3.12를 다운로드합니다. 설치 시 #strong["Add Python to PATH"] 체크박스를 반드시 선택하세요.

#heading(outlined: false, level: 3)[2.2 가상환경 설정]

예제마다 패키지 버전이 다를 수 있으므로 #strong[반드시 가상환경을 만들어서 진행하세요.]

```bash
# 가상환경 생성
python3.12 -m venv .venv

# 활성화 (macOS/Linux)
source .venv/bin/activate

# 활성화 (Windows)
.venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

가상환경이 활성화되면 터미널 프롬프트 앞에 `(.venv)` 가 표시됩니다.

#heading(outlined: false, level: 3)[2.3 Ollama 설치]

Ollama는 로컬 LLM을 실행하는 도구입니다. 공식 사이트(https:/\/ollama.com)에서 설치하세요.

```bash
# 설치 확인
ollama --version
```

#heading(outlined: false, level: 3)[2.4 LLM 모델 다운로드]

챕터별로 사용하는 모델이 다릅니다.

#figure(
  align(center)[#table(
    columns: 4,
    align: (auto,auto,auto,auto,),
    table.header([모델], [사용 챕터], [용도], [RAM],),
    table.hline(),
    [`deepseek-r1:8b`], [CH01\~05], [추론(Chain-of-Thought) 특화], [16GB 이상],
    [`nomic-embed-text`], [CH01], [임베딩 (CH04부터 ko-sroberta로 교체)], [---],
    [`llama3.1:8b`], [CH06\~10], [Tool Calling 지원], [16GB 이상],
    [`qwen2.5vl:7b`], [CH10], [비전 LLM (스캔 PDF 처리)], [16GB 이상],
  )]
  , kind: table
  )

```bash
# CH01~05 모델
ollama pull deepseek-r1:8b
ollama pull nomic-embed-text

# CH06~10 모델
ollama pull llama3.1:8b

# CH10 비전 모델
ollama pull qwen2.5vl:7b
```

#callout-box([RAM이 부족하거나 응답이 너무 느리면], [`.env`에서 `LLM_PROVIDER=openai`로 바꿔서 GPT-4o-mini를 쓸 수 있습니다. 단, API 비용이 발생합니다.])

#heading(outlined: false, level: 3)[2.5 .env 파일 설정]

각 예제 폴더의 `.env.example` 을 `.env` 로 복사한 뒤 값을 채워넣으세요.

```bash
cp .env.example .env
```

```
# LLM 설정
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-r1:8b      # CH01~05
# OLLAMA_MODEL=llama3.1:8b       # CH06~10 (Tool Calling 필요)

# OpenAI 사용 시
# LLM_PROVIDER=openai
# OPENAI_API_KEY=sk-...
# OPENAI_MODEL=gpt-4o-mini

# PostgreSQL (ex02 이후)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=rag_db
POSTGRES_USER=rag_user
POSTGRES_PASSWORD=rag_password

# 벡터DB + 임베딩
CHROMA_PERSIST_DIR=./data/chroma_db
EMBEDDING_MODEL=jhgan/ko-sroberta-multitask

# 비전 LLM (ex10)
VISION_MODEL=qwen2.5vl:7b
VISION_PROVIDER=ollama
# VISION_PROVIDER=openai  # 로컬 사양 부족 시
```

#heading(outlined: false, level: 3)[2.6 Docker (PostgreSQL)]

ex02 이후 예제는 PostgreSQL이 필요합니다. Docker Compose로 실행합니다.

```bash
docker compose up -d
```

PostgreSQL 16 Alpine 이미지를 사용하며 `data/schema.sql` 이 자동으로 초기화됩니다.

#heading(outlined: false, level: 3)[2.7 핵심 패키지 요약]

#figure(
  align(center)[#table(
    columns: 3,
    align: (auto,auto,auto,),
    table.header([패키지], [버전], [용도],),
    table.hline(),
    [`langchain`], [0.3.x], [RAG 파이프라인, 에이전트],
    [`chromadb`], [1.5.x], [벡터 데이터베이스],
    [`fastapi`], [0.115.x], [API 서버],
    [`sentence-transformers`], [3.3.x], [한국어 임베딩 모델],
    [`psycopg2-binary`], [2.9.x], [PostgreSQL 연결],
    [`pypdf`], [4.3.x], [PDF 파싱],
    [`python-docx`], [1.1.x], [DOCX 파싱],
    [`openpyxl`], [3.1.x], [XLSX 파싱],
    [`rank-bm25`], [0.2.x], [하이브리드 검색 (CH08)],
    [`easyocr`], [1.7.x], [OCR (CH10)],
  )]
  , kind: table
  )

각 예제 폴더의 `requirements.txt` 로 한 번에 설치할 수 있습니다.

```bash
pip install -r requirements.txt
```

#heading(outlined: false, level: 2)[3. 자주 만나는 오류]

#heading(outlined: false, level: 3)[3.1 `python` 명령어가 안 될 때]

macOS/Linux에서는 `python` 대신 `python3.12` 를 사용해야 할 수 있습니다.

```bash
# python이 안 되면
python3.12 --version
python3.12 -m venv .venv
```

#heading(outlined: false, level: 3)[3.2 `pip install` 에서 권한 오류]

가상환경 없이 시스템 Python에 설치하려고 하면 권한 오류가 발생합니다. 가상환경을 먼저 활성화하세요.

```bash
# 이렇게 하면 안 됩니다
pip install langchain  # PermissionError 또는 externally-managed-environment

# 이렇게 하세요
source .venv/bin/activate  # 먼저 가상환경 활성화
pip install -r requirements.txt
```

#heading(outlined: false, level: 3)[3.3 `pip` 대신 `pip3`]

`pip` 명령이 안 되면 `pip3` 를 사용하세요. 가상환경 안에서는 둘 다 동일합니다.

#heading(outlined: false, level: 3)[3.4 psycopg2-binary 설치 실패 (macOS Apple Silicon)]

M1/M2/M3 Mac에서 psycopg2-binary 설치가 실패할 수 있습니다.

```bash
# libpq 먼저 설치
brew install libpq
pip install psycopg2-binary
```

#heading(outlined: false, level: 3)[3.5 Ollama 연결 오류]

```
ConnectionRefusedError: Connection refused
```

Ollama 서버가 실행 중인지 확인하세요.

```bash
# Ollama 서버 실행
ollama serve

# 또는 Ollama 앱을 실행하면 자동으로 서버가 시작됩니다
```

#heading(outlined: false, level: 3)[3.6 모델 다운로드 오류]

```
model not found
```

해당 모델을 아직 다운로드하지 않은 경우입니다. `ollama pull 모델명` 으로 다운로드하세요.

#v(4pt)
#block(width: 100%, height: 0.5pt, fill: rgb("#e5e7eb"))
#v(4pt)


// ══════════════════════════════════════
// 목차: Design 1 (depth: 2)
// ══════════════════════════════════════
#page(numbering: none, header: none, footer: none)[
  #set block(spacing: toc-spacing)
  #set par(spacing: toc-spacing)
  #v(30pt)
  #block(width: 100%, below: 12pt, {
    text(24pt, weight: "bold", fill: color-text)[목차]
    v(6pt)
    line(length: 100%, stroke: 3pt + color-primary)
  })
  #v(12pt)

  #show outline.entry.where(level: 1): set text(weight: "bold", size: 11pt)
  #show outline.entry.where(level: 1): it => {
    v(toc-spacing + 2pt)
    it
  }
  #show outline.entry.where(level: 3): set text(size: 8.5pt, fill: rgb("#6b7280"))

  #outline(
    title: none,
    indent: 1.5em,
    depth: toc-depth,
  )
]

// ══ CONTENT ══
= 들어가며: 사서를 키우다

ConnectHR 대시보드에 질문이 흘러가고 있었습니다. "연차 신청 절차 알려줘"가 들어오고 2초 뒤 출처와 함께 답변이 올라갑니다. 옆자리 동료가 "A 사원 연차 며칠 남았어? 사용 규정도 알려줘"라고 치자 DB에서 숫자를 꺼내고 문서에서 규정을 찾아 한 번에 답합니다. 캐시에 있던 질문은 0.1초 만에 돌아왔습니다.

#v(paragraph-gap)
#strong[오픈이]는 턱을 괴고 모니터를 바라봤습니다. 커서가 깜빡이는 입력창 위로 질문이 하나 더 올라갑니다. 또 답합니다. 아무도 놀라지 않습니다. 당연한 것처럼 질문하고 당연한 것처럼 답변을 받습니다.

#v(paragraph-gap)
#emph[4개월 전에는 환각이 뭔지도 몰랐는데.]

#v(paragraph-gap)
예전에는 저 질문에 AI가 자신 있게 거짓말을 했습니다. 지금은 아무도 그 시절을 기억하지 못합니다. 다만 시작은 또렷하게 남아 있습니다.

#v(paragraph-gap)
모니터를 바라보던 시선이 4개월 전으로 되감깁니다.

#v(paragraph-gap)
#strong[팀장]: "AI로 사내 문서 검색 시스템 만들어봐. 직원들이 규정이나 정책 찾는 게 번거롭다고 해서."

#v(paragraph-gap)
#emph[AI로? 사내 문서를? 나 혼자서?]

#v(paragraph-gap)
사수도 없었습니다. 옆자리는 비어 있고 물어볼 사람도 없었습니다. 노트북을 열고 ChatGPT에 그대로 쳐봤습니다.

#v(paragraph-gap)
"우리 회사 연차 규정이 어떻게 되나요?"

#v(paragraph-gap)
AI가 답합니다. 연차는 15일이고 3일 전까지 신청하면 된다고요.

#v(paragraph-gap)
#emph[오, 이거면 되는 거 아니야?]

#v(paragraph-gap)
서랍에서 규정집을 꺼냈습니다. 모니터 왼쪽에 세워놓고 오른쪽 화면의 AI 답변과 한 줄씩 대조하기 시작했습니다. 첫 줄부터 달랐습니다. 연차 일수가 틀렸습니다. 신청 기한도 틀렸습니다. 존재하지 않는 조항까지 지어냈습니다. 열 줄을 비교하는 동안 한 줄도 맞는 게 없었는데 화면 속 AI는 여전히 확신에 찬 어조였습니다. 규정집을 쥔 손가락 끝이 하얘졌습니다.

#v(paragraph-gap)
세상의 모든 공개 자료는 섭렵했지만 우리 회사 내부 문서는 본 적 없는 외부인. 모르면 모른다고 하면 될 텐데 그럴듯한 답을 만들어냅니다.

#v(paragraph-gap)
이게 #strong[환각(Hallucination)] 입니다.

#v(paragraph-gap)
그러면 문서를 직접 넣어주면 되지 않을까. 규정 내용을 통째로 프롬프트에 붙여봤습니다. 연차 규정 한 페이지를 넣었더니 제대로 답합니다. 됐다 싶어서 규정집 200페이지를 한꺼번에 넣었습니다. 토큰 한도를 넘겨서 잘려나갔습니다. 절반도 읽지 못한 AI가 앞부분만 가지고 다시 자신 있게 답하기 시작합니다.

#v(paragraph-gap)
환각이 돌아왔습니다.

#v(paragraph-gap)
#strong[팀장]: "전부 외우게 하지 말고 필요한 것만 찾아서 읽게 해."

#v(paragraph-gap)
그날 밤 샤워하다가 문득 떠오른 게 있었습니다. 대학교 오픈북 시험. 교과서 전체를 외울 필요 없이 문제가 나오면 해당 페이지를 펼쳐서 읽으면 됐습니다. AI한테도 똑같이 하면 됩니다. 질문이 들어올 때마다 200페이지 전체가 아니라 관련된 두세 페이지만 골라서 건네주면 되는 겁니다.

#v(paragraph-gap)
이게 #strong[RAG]입니다. 모든 걸 외우게 하는 대신 필요한 문서만 찾아서 읽게 하는 구조. 문서를 찾으려면 문서가 정리된 곳이 있어야 합니다. 그래서 도서관을 짓기로 했습니다.

#v(paragraph-gap)
도서관을 짓는 일은 생각보다 지저분했습니다.

#v(paragraph-gap)
건물부터 세워야 했습니다. "팀원 연차 며칠 남았어?" 같은 질문은 문서 어디에도 답이 없었습니다. 개인별 잔여 연차는 인사 DB에 들어 있었습니다. AI가 DB를 직접 뒤지게 할 수는 없으니 데이터를 꺼내주는 API를 따로 만들었습니다. 주방에 손님이 직접 들어가는 식당은 없으니까요. 주문을 받으면 웨이터가 주방에서 가져다줍니다.

#v(paragraph-gap)
그다음은 장서입니다. 공유 드라이브를 열었습니다. PDF, DOCX, XLSX, 심지어 HWP까지 300개가 넘는 파일이 한 폴더에 쌓여 있었습니다. "인사규정\_최종.docx" 옆에 "인사규정\_최종\_진짜최종.docx"가 있었고 어느 게 현행 문서인지 파일명만 봐서는 알 수 없었습니다. 스크롤을 내릴수록 눈앞이 아득해졌습니다.

#v(paragraph-gap)
#strong[팀장]: "쓰레기를 넣으면 쓰레기가 나와."

#v(paragraph-gap)
폐기 문서를 걸러내야 했습니다. 하나씩 열어보고 날짜를 확인하고 현행 여부를 체크합니다. 살릴 문서만 추려냈습니다. 형식별로 파싱하고 메타데이터를 붙이고 폴더 구조를 잡는 데만 며칠. 사서가 새 책을 받으면 바로 서가에 꽂지 않는 것처럼. 분류표를 확인하고 라벨을 붙이고 청구기호를 매긴 다음에야 서가에 올립니다.

#v(paragraph-gap)
문서를 골랐으면 서가에 꽂을 차례입니다. 마트에서 사온 재료를 봉지째 냉장고에 던지면 나중에 찾을 수 없습니다. 양파가 어디 있는지 고기는 아직 쓸 수 있는지 뒤져봐야 합니다. 제대로 하려면 손질하고 먹기 좋게 다듬고 용기에 나눠 담아야 합니다. 문서도 똑같았습니다. 텍스트를 꺼내고 적당한 크기로 자르고 숫자 배열로 변환해서 벡터DB에 저장합니다.

#v(paragraph-gap)
사람한테는 "연차"와 "유급 휴가"가 같은 말입니다. 기계한테는 아닙니다. 글자가 다르면 다른 단어입니다. 서가에 꽂힌 문서끼리 의미가 가까운지 먼지를 기계가 판단할 수 있도록 만드는 데까지 한 달이 걸렸습니다.

#v(paragraph-gap)
한 달 뒤. 서가에 문서가 꽂혀 있고 검색하면 관련 문서가 유사도 점수와 함께 나왔습니다. 동료 자리로 걸어가서 화면을 돌렸습니다.

#v(paragraph-gap)
#strong[동료]: "검색 결과 다섯 개를 던져주지 말고 그냥 답을 알려줘."

#v(paragraph-gap)
걸음을 멈추고 자리로 돌아왔습니다. 서가에서 책을 찾아오는 건 됐는데 그 책을 읽고 정리해서 답해주는 사람이 없었습니다.

#v(paragraph-gap)
도서관은 완성됐는데 사서가 없었습니다.

#v(paragraph-gap)
사서를 앉혔습니다. 질문을 듣고 서가에서 문서를 찾고 읽어서 정리하고 출처까지 알려주는 사서. "어떤 문서에서 이 답을 찾았는지" 반드시 보여주게 만들었습니다. 출처 없는 답변은 근거 없는 주장이니까요. 한 번 물어보고 끝이 아니라 대화를 이어갈 수 있는 기억력도 붙여줬습니다.

#v(paragraph-gap)
그제야 사서가 일을 시작합니다.

#v(paragraph-gap)
기뻐할 틈도 없이 새 문제가 터졌습니다.

#v(paragraph-gap)
#strong[동료]: "A 사원 연차 며칠? 그리고 연차 신청 절차 알려줘."

#v(paragraph-gap)
한 문장에 두 종류가 섞여 있었습니다. 잔여 연차는 DB에 있고 신청 절차는 문서에 있습니다. 사서는 서가의 문서밖에 모릅니다. DB 쪽 담당자를 부를 줄도 모릅니다. 이틀 동안 모니터 앞에서 화이트보드에 화살표를 그리고 지우고 다시 그렸습니다.

#v(paragraph-gap)
#strong[팀장]: "1층 안내데스크 가봤어? 거기 직원이 뭘 해?"

#v(paragraph-gap)
가만히 생각해봤습니다. 안내데스크 직원은 모든 업무를 직접 처리하지 않습니다. 이건 인사팀, 이건 총무팀, 이건 시설관리팀. 누구에게 물어봐야 하는지를 아는 게 그 사람의 역할입니다. 질문이 들어오면 유형을 분류하고 맞는 담당자를 호출합니다. DB를 조회하는 담당자, 문서를 검색하는 담당자, 둘 다 호출해서 합치는 담당자.

#v(paragraph-gap)
사서를 안내데스크 직원으로 승진시켰습니다.

#v(paragraph-gap)
이렇게 #strong[ConnectHR]이 태어났습니다.

#v(paragraph-gap)
ConnectHR을 동료들에게 풀어줬습니다.

#v(paragraph-gap)
#strong[동료]: "아까도 물어봤는데 또 20초나 기다려?"

#v(paragraph-gap)
같은 질문이 들어올 때마다 매번 처음부터 답을 만들고 있었습니다. 사서가 같은 책을 꺼내서 같은 페이지를 다시 읽고 같은 답을 다시 쓰고 있었던 겁니다. 10번 물어보면 10번 서가를 뒤집니다. 사서에게 메모장을 줬습니다. 한 번 답한 건 적어두고 같은 질문이 오면 메모를 보여줍니다. 20초가 0.1초가 됐습니다. 다만 메모장에는 유통기한을 뒀습니다. 규정이 바뀌었을 수도 있으니까요.

#v(paragraph-gap)
업무 일지도 쥐어줬습니다. 하루에 토큰을 얼마나 쓰는지, 비용은 얼마인지 기록하게 했습니다. 느린 질문이 어떤 건지도 따로 남겼습니다.

#v(paragraph-gap)
운영은 안정됐습니다. 빨라지니까 쓰는 사람이 늘었고 늘어나니까 그동안 보이지 않던 문제가 하나씩 터지기 시작합니다.

#v(paragraph-gap)
#strong[동료]: "병가 규정을 물어봤는데 출장 규정이 나왔어요."

#v(paragraph-gap)
#emph[뭐라고?]

#v(paragraph-gap)
퇴근길 지하철에서 노트북을 꺼냈습니다. 흔들리는 객차 안에서 로그를 열어봤습니다. LLM은 멀쩡했습니다. 받은 문서를 기반으로 성실하게 답했을 뿐입니다. 문제는 그 문서였습니다. 검색 결과를 하나씩 열어보니 사서가 서가에서 엉뚱한 책을 꺼내온 겁니다. 500자마다 기계적으로 잘라놓은 문서 조각에서 병가 규정 뒷부분과 출장 규정 앞부분이 한 덩어리로 섞여 있었습니다.

#v(paragraph-gap)
한 달 전에 꽂았던 서가를 다시 정리해야 했습니다.

#v(paragraph-gap)
가위로 일정하게 자르던 걸 의미 단위로 바꿨습니다. 문서에서 주제가 바뀌는 지점을 감지하고 거기서 끊게 했습니다. 검색 결과도 한 번 더 훑어서 관련 없는 문서를 걸러내게 합니다. 키워드로만 찾던 검색에 의미 검색을 합쳤습니다. 같은 질문을 넣었는데 답이 달라졌습니다. 검색을 바꿨을 뿐인데 사서가 다른 사람이 된 것 같았습니다.

#v(paragraph-gap)
검색이 좋아지니까 이번엔 질문이 문제였습니다.

#v(paragraph-gap)
#strong[동료]: "WFH 정책 알려줘."

#v(paragraph-gap)
ConnectHR이 멈칫했습니다. 문서에는 "재택근무"라고 적혀 있었으니까요. "휴가 규정 알려줘"도 마찬가지였습니다. 문서에는 "연차유급휴가"라고 돼 있습니다. 검색 엔진이 아무리 좋아도 질문 자체를 이해 못하면 소용없습니다.

#v(paragraph-gap)
초보 사서는 서가에서 "WFH"라는 글자만 찾습니다. 당연히 없습니다. 경험 많은 사서는 다릅니다.

#v(paragraph-gap)
#emph[WFH라면… 재택근무? Work From Home? 혹시 원격근무?]

#v(paragraph-gap)
떠올릴 수 있는 표현을 전부 떠올려서 각각 찾아봅니다. 사서에게 그 감각을 심어줬습니다. 약어를 풀어쓰고 동의어를 확장하고 한 질문을 여러 각도로 바꿔서 검색하게 했습니다. 그리고 답변에 근거를 붙였습니다. "이 문서의 3페이지에서 찾았습니다"라고 원본 이미지와 함께.

#v(paragraph-gap)
마지막 관문은 스캔 PDF였습니다.

#v(paragraph-gap)
총무팀이 보내준 오래된 사규집을 열었습니다. 조직도 PDF. 텍스트를 추출하려고 했는데 아무것도 나오지 않았습니다. 종이 문서를 스캐너에 올려서 찍은 거라 페이지 전체가 이미지입니다. 사람 눈에는 조직도의 박스와 화살표가 또렷하게 보이는데 기계한테는 그냥 점들의 배열일 뿐입니다. 텍스트 추출기를 아무리 돌려도 "대표이사경영지원본부기술개발본부"가 한 줄로 붙어 나왔습니다.

#v(paragraph-gap)
#emph[글자가 보이는데 읽을 수가 없어.]

#v(paragraph-gap)
사서에게 눈을 달아줬습니다. 글만 읽던 사서가 이미지를 보고 거기 적힌 내용을 파악하게 됐습니다.

#v(paragraph-gap)
그리고 성적표를 만들었습니다. "잘 되는 것 같다"는 느낌만으로는 어디를 고쳐야 할지 모릅니다. 찾아온 문서 중 몇 개가 정답이었는지. 정답 문서를 몇 개나 찾았는지. AI가 지어낸 답변은 없었는지. 이 지표들로 ConnectHR의 실력을 숫자로 측정했습니다. 느낌이 아니라 숫자입니다. 튜닝 전과 후를 비교했습니다. 숫자가 올라가는 걸 확인하고 나서야 의자 등받이에 등을 기댔습니다.

#v(paragraph-gap)
4개월이 지났습니다.

#v(paragraph-gap)
돌이켜보면 티켓 열 장이었습니다. 매번 모르는 단어 앞에서 멈췄고 검색하고 틀리고 다시 읽었습니다. 대단한 깨달음 같은 건 없었습니다. 하나를 풀면 다음 문제가 터졌고 그걸 또 풀었을 뿐입니다.

#v(paragraph-gap)
다만 한 가지 달라진 게 있습니다.

#v(paragraph-gap)
예전에는 "AI가 엉뚱한 답을 해"라는 말을 들으면 LLM을 의심했습니다. 지금은 검색을 의심합니다. 청킹을 확인하고 리랭킹을 떠올리고 쿼리를 바꿔봅니다. 이름을 외운 게 아니라 문제와 해결을 한 쌍으로 기억하게 된 겁니다.

#v(paragraph-gap)
이 책은 그 열 쌍의 기록입니다. #strong[오픈이]가 부딪혔던 문제가 있고 #strong[팀장]이 던져준 비유로 감을 잡은 뒤 직접 만들어보며 넘어가는 과정이 있습니다.

#v(paragraph-gap)
문제를 보고 어디를 건드려야 하는지 보이는 감각. 이 책이 드리고 싶은 건 그겁니다.

#v(paragraph-gap)
첫 번째 과제부터 시작하겠습니다.

= Ch.1: Hallucination과 RAG (ex01)

#quote(block: true)[한 줄 요약: LLM은 우리 회사 문서를 읽은 적이 없다. 문서를 직접 넣어줘야 한다. \
핵심 개념: LLM 환각, Context Injection, RAG]

== AI가 자신 있게 틀린 답을 말한다

=== 1.1 입사 3일 차, 첫 번째 임무

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH01/gemini/01_chapter-opening.png", alt: [AI가 자신 있게 내놓은 답이 사실이 아닐 때, RAG라는 해법이 시작됩니다], max-width: 0.7)

커넥트에 입사한 지 3일 차. 아직 사내 Wi-Fi 비밀번호를 포스트잇에 적어 모니터에 붙여놓던 시절입니다. 오전 10시, 팀장이 저를 바라보며 다가옵니다.

#v(paragraph-gap)
#strong[팀장]: "AI로 사내 문서 검색 시스템 만들어봐. 직원들이 규정이나 정책 찾는 게 번거롭다고 해서. 채팅창에 물어보면 바로 답해주는 거."

#v(paragraph-gap)
#emph[AI 비서. 사내 문서. 대화식 검색. 나 혼자서?]

#v(paragraph-gap)
#strong[오픈이]: "언제까지요?". #strong[팀장]: "급하진 않아. 2주 내로 간단한 프로토타입만."

#v(paragraph-gap)
노트북을 열고 ChatGPT를 실행했습니다.

#v(paragraph-gap)
#emph[ChatGPT도 뭐든 대답하잖아. LLM에게 직접 물어보면 되는 거 아니야?]

#v(paragraph-gap)
코드부터 짰습니다.

=== 1.2 LLM의 자신감 넘치는 거짓말

연차 규정을 예시로 물어봤습니다.

#v(paragraph-gap)
#strong[오픈이]: "우리 회사(커넥트)의 신입사원 연차 발생 규정이 어떻게 돼?"

#v(paragraph-gap)
LLM이 답했습니다.

#v(paragraph-gap)
#strong[LLM]: "커넥트 사의 신입사원 연차 규정은 근로기준법에 따라, 입사 후 1년 미만 기간에는 1개월 개근 시 1일의 유급휴가가 발생합니다. 1년 이상 근무 시에는 15일의 연차가 발생하며, 3년 이상 근무한 경우 1년마다 1일씩 추가됩니다…"

#v(paragraph-gap)
그럴듯했습니다. 공식적인 느낌도 났습니다. 입사할 때 받은 규정집을 꺼내 비교해봤습니다. 커넥트의 실제 규정은 이랬습니다.

#v(paragraph-gap)
#emph[신입사원은 입사 후 3년 동안은 연차가 없다. 대신 매월 1회 '리프레시 데이'를 유급으로 제공한다. 3년 근속 시 30일의 연차가 일시에 발생한다.]

#v(paragraph-gap)
#emph[잠깐, 뭐라고?]

#v(paragraph-gap)
다시 읽었습니다. 완전히 다른 내용이었습니다. LLM이 방금 그럴듯한 거짓말을 한 것입니다.

=== 1.3 Hallucination --- 왜 모르면서 아는 척하나

여기서 의문이 생깁니다. LLM은 왜 자신 있게 틀린 대답을 했을까요? LLM을 이렇게 가정해 보겠습니다. 입사 면접을 보러 온 외부인이라고요. 이 외부인은 세상에 공개된 거의 모든 자료를 읽었습니다. 인터넷, 뉴스, 책, 논문까지. 공개된 텍스트라면 뭐든 섭렵했습니다. 그래서 근로기준법은 완벽하게 알고 일반적인 회사 연차 제도도 줄줄 외웁니다. 그런데 커넥트의 내부 규정집은 공개된 적이 없습니다. 이 외부인이 읽을 방법이 없었어요.

#v(paragraph-gap)
문제는 이 외부인이 "모른다"고 솔직히 말하지 못한다는 점입니다. 질문을 받으면 자기가 아는 것 중에서 가장 비슷해 보이는 걸 자신감 있게 말합니다. "아마 일반적인 회사라면 이렇겠지"라는 추측인데, 마치 확실히 아는 것처럼 들립니다. 이게 #strong[LLM 환각(Hallucination)] 입니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH01/gemini/01_hallucination-outsider.png", alt: [LLM은 세상의 공개 데이터는 학습했지만, 우리 회사 내부 문서는 읽은 적이 없다.], max-width: 0.6)

GPT든 Claude든 Gemini든 마찬가지입니다. 학습 데이터에 없는 정보는 알 방법이 없습니다. 그런데 솔직히 "모른다"고 하지 않고 그럴듯하게 지어냅니다. 일반적인 내용과 비슷한 맥락일수록 더 자연스럽게 지어냅니다. 커넥트의 연차 규정은 공개된 인터넷 어디에도 없습니다. LLM이 알 수 없습니다. 근로기준법 기반으로 그럴듯한 답을 만들어낸 것뿐입니다.

=== 1.4 Context Injection --- 문서를 직접 넣어보기

생각해보면 해결책은 단순합니다. LLM이 모른다면 직접 알려주면 됩니다. 규정 내용을 통째로 프롬프트에 붙여서 다시 물어봤습니다.

#v(paragraph-gap)
#strong[오픈이]: 아래 \[커넥트 취업규칙\]을 참고해서 신입사원 연차 규정을 알려줘.

#v(paragraph-gap)
이번엔 달랐습니다. 커넥트의 실제 규정을 정확히 설명해줬습니다.

#v(paragraph-gap)
#emph[오, 이거면 되는 거 아니야?]

#v(paragraph-gap)
그런데 사내 문서가 규정집 하나가 아닙니다. 복지 정책, 보안 지침, 업무 가이드, 회의록, 프로젝트 문서까지 파일만 수십 개입니다. 매번 전부 복사해서 프롬프트에 붙이면 어떻게 됩니까? LLM에는 한 번에 처리할 수 있는 텍스트 길이 한도가 있습니다. 문서가 쌓일수록 한도를 넘기기 쉽습니다. 무엇보다 연차 규정을 물어보는데 보안 지침이나 복지 정책까지 다 넣어서 보내는 건 비효율적입니다. 관련 없는 내용이 섞일수록 LLM이 정작 필요한 부분을 놓치기 쉬워집니다.

#v(paragraph-gap)
문서를 통째로 넣는 방식은 임시방편이었습니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH01/gemini/01_context-overflow.png", alt: [문서를 통째로 넣는 방식의 한계. 문서가 늘어나면 프롬프트 창이 넘친다.], max-width: 0.6)

=== 1.5 RAG --- 오픈북 시험으로 바꾸기

더 나은 방법이 있습니다. LLM이 모든 사내 문서를 외울 필요는 없습니다. 사람도 비슷한 문제를 해결한 방식이 있습니다. 시험에서 모든 내용을 통째로 외우는 대신 오픈북을 허용하면 됩니다. 시험지가 나오면 그 문제와 관련된 페이지를 찾아서 보면서 답하는 방식입니다.

#v(paragraph-gap)
LLM도 마찬가지입니다. 사내 문서 전체를 외울 필요가 없습니다. 질문이 들어왔을 때 #strong[그 질문과 관련된 문서 조각만 찾아서 LLM에게 건네주면 됩니다.]

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH01/gemini/01_openbook-exam.png", alt: [클로즈드북 vs 오픈북. RAG는 LLM에게 오픈북 시험을 치르게 하는 것입니다.], max-width: 0.6)

이것이 #strong[RAG] --- Retrieval-Augmented Generation, 검색 증강 생성입니다. 흐름을 보면 이렇게 됩니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH01/diagram/01_llm-vs-rag.png", alt: [LLM 단독 호출과 RAG의 차이. RAG는 질문마다 관련 문서를 찾아서 LLM에 건네줍니다.], max-width: 0.6)

+ 사내 문서들을 미리 #strong[벡터 DB]에 조각으로 나눠 저장해 놓습니다 (오픈북 준비)
+ 질문이 들어오면, 그 질문과 의미가 비슷한 문서 조각을 벡터 DB에서 찾습니다 (관련 페이지 찾기)
+ 찾은 문서 조각 + 질문을 LLM에게 함께 넘깁니다
+ LLM이 그 문서를 보면서 답합니다 (오픈북으로 시험 보기)

#v(paragraph-gap)
이제 LLM이 우리 회사 규정을 외울 필요가 없습니다. 질문할 때마다 관련 규정을 찾아서 보여주면 되기 때문입니다. 어느 문서를 참고했는지도 함께 돌려줄 수 있습니다. 이번 챕터의 목표는 이 흐름을 직접 만들어보는 것입니다. 더미 문서 3개짜리 간단한 버전으로 시작하겠습니다. 실제 PDF 파싱이나 한국어 임베딩 모델 적용, DB 연동은 뒤 챕터에서 차례로 붙입니다.

#v(paragraph-gap)
이제 실습으로 LLM 환각을 직접 확인하고, RAG로 해결해보겠습니다.

== 환각을 잡는 RAG 파이프라인 만들기

=== 2.1 용어 정리

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([이야기 속 표현], [진짜 용어], [정식 정의],),
    table.hline(),
    ["자신감 넘치는 거짓말"], [LLM 환각 (Hallucination)], [LLM이 학습 데이터에 없는 정보를 그럴듯하게 만들어내는 현상],
    ["문서를 직접 붙여 넣기"], [Context Injection], [관련 정보를 프롬프트에 직접 넣어서 LLM에 제공하는 방법],
    ["오픈북 시험"], [RAG (Retrieval-Augmented Generation)], [외부 지식 저장소에서 관련 문서를 검색해 LLM 생성에 활용하는 방식],
    ["오픈북 준비"], [임베딩 + 벡터 DB 저장], [문서를 수치 벡터로 변환해 ChromaDB에 인덱싱하는 과정],
    ["관련 페이지 찾기"], [벡터 유사도 검색], [질문 벡터와 문서 벡터 간 코사인 유사도를 계산해 가장 관련 있는 문서를 반환],
  )]
  , kind: table
  )

=== 2.2 소스 코드 준비

이 책의 실습은 GitHub 레포를 클론해서 진행합니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([레포], [용도], [주소],),
    table.hline(),
    [#strong[rag-start]], [실습용 (빈 파일 --- 챕터 따라 코드 작성)], [`https://github.com/metacoding-18-ai-applied-v4/rag-start`],
    [#strong[rag-end]], [완성 코드 (막히면 참고)], [`https://github.com/metacoding-18-ai-applied-v4/rag-end`],
  )]
  , kind: table
  )

아직 클론하지 않았다면 터미널에서 아래 명령어를 실행해 보겠습니다.

```bash
git clone https://github.com/metacoding-18-ai-applied-v4/rag-start.git
cd rag-start/ex01
```

이미 클론하셨다면 `ex01` 폴더로 이동해 보겠습니다.

```bash
cd rag-start/ex01
```

```
ex01/
├── step1_fail.py            [실습] LLM 단독 호출 → 환각 체험
├── step2_context.py         [실습] 컨텍스트 직접 주입 → 임시 해결
├── step3_rag.py             [실습] RAG 기본 파이프라인 구성
├── step3_rag_no_chunking.py [실습] 청킹 없이 비교 → 차이 체감
└── step4_rag.py             [실습] 추론 심화 (Chain-of-Thought)
```

`[실습]` 파일에는 import와 데이터가 미리 준비되어 있습니다. 각 TODO의 `pass`를 지우고 챕터의 코드를 작성합니다. 막히는 부분이 있다면 rag-end의 완성 코드를 참고해 주시기 바랍니다.

=== 2.3 실습 환경 구축

#quote(block: true)[기본 환경(Python 3.12, Docker)이 없다면 #strong[교육자료]를 먼저 확인해 주시기 바랍니다.]

#callout-box([Apple Silicon(M1/M2/M3) 사용자], [psycopg2-binary 설치가 실패한다면 `brew install libpq`를 먼저 실행해 보시기 바랍니다.])

```bash
cd ex01
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Ollama가 실행 중인지 확인합니다. 터미널에서 `ollama list`를 입력했을 때 모델 목록이 나오면 이미 실행 중입니다. 목록이 안 나오면 macOS에서는 Ollama 앱을 실행하거나 `ollama serve`를 입력합니다. 모델이 아직 없다면 다운로드합니다.

```bash
ollama pull deepseek-r1:8b
ollama pull nomic-embed-text
```

#callout-box([팁: LLM 선택], [기본값은 Ollama + `deepseek-r1:8b`입니다(16GB RAM 이상 권장). RAM이 부족하거나 응답이 너무 느리면 `.env`에서 `LLM_PROVIDER=openai`로 바꿔서 GPT-4o-mini를 쓸 수도 있습니다. 단, API 비용이 발생합니다. `.env` 파일에 `OPENAI_API_KEY=sk-xxxxxx` 형태로 키를 등록해 사용하시면 됩니다. 상세 안내는 #strong[교육자료]를 확인해 주시기 바랍니다.])

이번 챕터에서는 #strong[LangChain]이라는 프레임워크를 사용합니다. LLM 호출, 벡터 검색, 체인 조립처럼 RAG에 필요한 부품을 제공하는 도구입니다. 여기서는 맛보기로만 쓰고 CH05에서 본격적으로 다룹니다.

#figure(
  align(center)[#table(
    columns: 2,
    align: (auto,auto,),
    table.header([패키지], [역할],),
    table.hline(),
    [`langchain-ollama`], [Ollama LLM/임베딩 연동],
    [`langchain-chroma`], [ChromaDB 벡터 저장소],
    [`langchain-classic`], [RetrievalQA 체인 (CH05에서 LCEL로 전환)],
    [`chromadb`], [벡터 DB],
  )]
  , kind: table
  )

#callout-box([팁: 지금은 개념만 잡으세요], [LangChain, 임베딩, 벡터 DB 같은 용어가 한꺼번에 나와서 부담스러울 수 있습니다. 지금은 "문서를 넣어주면 LLM이 정확하게 답한다"는 #strong[RAG의 개념]만 잡으면 충분합니다. 각 기술의 동작 원리는 CH04\~CH05에서 차근차근 다룹니다.])

=== 2.4 실습 순서

+ `step1_fail.py` --- LLM 단독 질문
+ `step2_context.py` --- 문서 직접 전달
+ `step3_rag.py` --- RAG 파이프라인
+ `step3_rag_no_chunking.py` --- 청킹 없이 비교
+ `step4_rag.py` --- 추론 심화

#v(paragraph-gap)
환각을 직접 체험하고(step1), 문서를 넣으면 달라지는 걸 확인한 뒤(step2), RAG로 조립합니다(step3). 그다음 청킹 없이 돌려서 차이를 체감하고(step3\_no\_chunking), 추론이 필요한 질문까지 던져봅니다(step4). #strong[step1부터 순서대로 실행해 보겠습니다.]

=== 2.5 실습 1 --- step1\_fail.py: LLM에게 직접 물어보기

`ex01/step1_fail.py`를 열어 두 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

```python
# step1_fail.py — TODO: ChatOllama로 deepseek-r1:8b 모델 연결 (temperature=0)

# 1. Ollama에서 deepseek-r1:8b 모델을 로드 (temperature=0: 가장 확률 높은 답변)
llm = ChatOllama(model="deepseek-r1:8b", temperature=0)
```

```python
# step1_fail.py — TODO: 질문 출력 → llm.invoke로 답변 받기 → 답변 출력

# 1. 질문을 터미널에 출력
console.print(f"[bold]질문:[/bold] {question}\n")
# 2. LLM에 질문을 보내고 답변을 받음
response = llm.invoke(question)
# 3. 답변을 출력
console.print(f"[bold]답변:[/bold]\n{response.content}")
```

`ChatOllama`는 LangChain이 Ollama LLM을 호출할 때 쓰는 래퍼입니다. `temperature=0`은 창의적 변형 없이 가장 확률 높은 답변을 내놓게 하는 설정입니다.

```bash
# 실행
python step1_fail.py
```

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH01/terminal/01_step1-hallucination.png", alt: [step1\_fail.py 실행 결과. 자신감 있게 답하지만 실제 커넥트 규정과 다르다.], max-width: 0.65)

답변을 읽어보면 "근로기준법에 따라 1년 미만은 매월 1일…" 같은 내용이 나옵니다. 공식적인 느낌도 나고 그럴듯합니다. 하지만 앞에서 봤듯이 커넥트의 실제 규정은 완전히 다릅니다. LLM은 커넥트라는 회사를 모릅니다. 학습 데이터에 없으니 일반적인 근로기준법 내용을 가져다 붙인 것입니다. 이것이 #strong[환각(Hallucination)] 입니다. 틀린 답을 자신감 있게 내놓았고, 출처도 없습니다.

=== 2.6 실습 2 --- step2\_context.py: 문서를 직접 넣어보기

step1에서 LLM이 거짓말하는 걸 봤습니다. 이번에는 #strong[규정 내용을 프롬프트에 직접 포함]시켜 봅니다. `ex01/step2_context.py`를 열어 두 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

```python
# step2_context.py — TODO: ChatOllama로 deepseek-r1:8b 모델 연결 (temperature=0)

# 1. step1과 동일하게 LLM 로드
llm = ChatOllama(model="deepseek-r1:8b", temperature=0)
```

LLM 아래에 `context_data`와 `question`이 이미 선언되어 있습니다. `context_data`에는 커넥트의 취업규칙 일부가, `question`에는 테스트 질문이 담겨 있습니다.

```python
# 정보를 변수에 담습니다 (아직 DB 안 씀)
context_data = """
[커넥트 취업규칙]
1. 신입사원은 입사 후 3년 동안은 연차가 없다. (파격적인 규정)
2. 대신 매월 1회 '리프레시 데이'를 유급으로 제공한다.
3. 3년 근속 시 30일의 연차가 일시에 발생한다.
"""

question = "우리 회사(커넥트)의 신입사원 연차 발생 규정이 어떻게 돼?"
```

step1에서는 LLM이 학습 데이터만으로 답했습니다. 이번에는 이 `context_data`를 프롬프트에 직접 넣어서 정답지를 건네줍니다.

```python
# step2_context.py — TODO: f-string으로 context_data와 question을 포함한 프롬프트 작성 → llm.invoke로 답변 받기 → 출력

# 1. 규정 문서(context_data)를 프롬프트에 직접 넣어서 LLM에 전달
prompt = f"""
아래 [참고 정보]를 보고 질문에 답해줘.
[참고 정보]
{context_data}

질문: {question}
"""

# 2. 질문 출력 → LLM 호출 → 답변 출력
console.print(f"[bold]질문:[/bold] {question}\n")
response = llm.invoke(prompt)
console.print(f"[bold]답변:[/bold]\n{response.content}")
```

step1과 달라진 부분은 `context_data`를 프롬프트에 직접 넣었다는 것뿐입니다. 문서를 넣으니 정확한 답변이 나옵니다. 하지만 문서가 수십 개로 늘어나면 매번 전부 붙일 수 없습니다. LLM이 한 번에 읽을 수 있는 텍스트 길이에는 한도가 있기 때문입니다. 이 한도를 #strong[컨텍스트 윈도우(Context Window)] 라고 합니다. 모델마다 크기가 다르지만, 수십 개 문서를 전부 넣기에는 부족합니다.

```bash
# 실행
python step2_context.py
```

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH01/terminal/01_step2-context.png", alt: [step2\_context.py 실행 결과. 문서를 직접 넣으니 정확하게 답한다.], max-width: 0.65)

이번에는 "3년 동안 연차 없음, 매월 리프레시 데이 1회"라는 커넥트의 실제 규정이 정확하게 답변으로 출력될 것입니다. step1과 코드 구조는 거의 같은데 결과가 완전히 달라졌습니다. 달라진 것은 `context_data`를 프롬프트에 넣었다는 것뿐입니다. LLM에게 정답지를 건네준 셈입니다. 환각이 사라진 건 좋지만, 이 방식은 문서가 늘어날수록 한계가 뚜렷합니다. 수십 개 문서를 매번 전부 붙일 수는 없기 때문입니다.

=== 2.7 실습 3 --- step3\_rag.py: RAG 파이프라인 구성

step2에서는 문서를 수동으로 넣었습니다. 이번에는 #strong[벡터 DB에 문서를 저장하고 질문에 맞는 문서를 자동으로 찾아오는] RAG 파이프라인을 만들어 보겠습니다. `ex01/step3_rag.py`를 열어 네 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

```python
# step3_rag.py — TODO: OllamaEmbeddings(nomic-embed-text)로 임베딩 생성 → Chroma.from_documents로 벡터DB 저장

# 1. 문서를 숫자 벡터로 변환하는 임베딩 모델 로드
embeddings = OllamaEmbeddings(model="nomic-embed-text")
# 2. 문서 3개를 벡터로 변환해서 ChromaDB에 저장
vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings)
```

```python
# step3_rag.py — TODO: vectorstore.as_retriever로 검색기 생성 (search_kwargs={"k": 3})

# 3. 질문과 가장 비슷한 문서 3개를 가져오는 검색기 생성
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
```

검색기를 만들었으니, 다음은 LLM에게 전달할 프롬프트를 살펴볼 차례입니다. 파일에 이미 작성되어 있는 프롬프트 템플릿입니다.

```python
# step3_rag.py — 프롬프트 템플릿 (파일에 이미 작성되어 있음)

template = """당신은 회사의 규정에 대해 설명해주는 AI 비서입니다.
아래의 참고 정보를 바탕으로 질문에 답하세요. 반드시 한국어로 답변해야 합니다.

참고 정보: {context}

질문: {question}
답변:"""
```

"참고 정보를 바탕으로 질문에 답하세요"라는 한 줄이 핵심입니다. LLM에게 제공된 문서에서만 답하도록 제약을 거는 겁니다. 이 기법을 #strong[그라운딩(Grounding)] 이라고 합니다. CH05에서 본격적으로 다룹니다.

#v(paragraph-gap)
이제 이 프롬프트를 사용해서 검색기와 LLM을 체인으로 연결합니다.

```python
# step3_rag.py — TODO: ChatOllama(deepseek-r1:8b) → RetrievalQA.from_chain_type으로 체인 조립

# 4. LLM 로드
llm = ChatOllama(model="deepseek-r1:8b", temperature=0)
# 5. 검색기 + LLM을 체인으로 연결 (검색된 문서를 LLM에 자동 전달)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)
```

`chain_type_kwargs={"prompt": PROMPT}`는 위에서 만든 프롬프트 템플릿을 체인에 주입하는 옵션입니다. 이걸 넣지 않으면 LangChain 기본 프롬프트가 사용되는데, 한국어 답변을 요구하는 우리 프롬프트를 쓰려면 직접 넘겨줘야 합니다. `return_source_documents=True`는 LLM의 답변뿐 아니라 검색에 사용된 원본 문서도 결과에 포함시키는 옵션입니다. 이 옵션이 없으면 `result["result"]`\(답변)만 돌아오고, 켜면 `result["source_documents"]`에 어떤 문서를 참고했는지까지 함께 돌아옵니다.

```python
# step3_rag.py — TODO: qa_chain.invoke로 질문 실행 → 검색된 문서(근거) 출력 → AI 답변 출력

# 6. 질문 실행 — 검색 + LLM 답변이 한 번에 동작
result = qa_chain.invoke({"query": question})

# 7. 어떤 문서를 참고했는지 출처 출력
console.print("\n--- 검색된 문서(근거) ---")
for doc in result["source_documents"]:
    console.print(f"[{doc.metadata['source']}]: {doc.page_content}")

# 8. AI 답변 출력
console.print("\n--- AI 답변 ---")
console.print(result["result"])
```

step2에서는 문서를 수동으로 넣었지만, 이번에는 질문에 맞는 문서를 자동으로 찾아옵니다.

```bash
# 실행
python step3_rag.py
```

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH01/terminal/01_step3-rag.png", alt: [step3\_rag.py 실행 결과. \[인사규정\] 문서를 찾아서 답변하고, 어디서 가져왔는지 출처까지 보여준다.], max-width: 0.65)

이제 답변과 함께 어느 문서를 참고했는지가 깔끔하게 출력되는 것을 확인할 수 있습니다. step2에서는 문서를 수동으로 넣어줬지만 이번에는 #strong[질문에 맞는 문서를 자동으로 찾아왔습니다.] 환각이 사라지고 명확한 출처가 생겼습니다.

=== 2.8 실습 4 --- step3\_rag\_no\_chunking.py: 청킹이 왜 필요한가

실습 3 --- step3\_rag.py에서 문서 3개를 #strong[각각 따로] 벡터 DB에 저장했습니다. 이번에는 반대로, 모든 문서를 #strong[하나의 덩어리로 합쳐서] 저장하면 어떻게 되는지 비교해 보겠습니다. `ex01/step3_rag_no_chunking.py`를 열면 step3\_rag.py와 거의 같지만 두 군데가 다릅니다. TODO의 `pass`를 지우고 작성합니다.

```python
# step3_rag_no_chunking.py — TODO: OllamaEmbeddings(nomic-embed-text)로 임베딩 생성 → Chroma.from_documents로 벡터DB 저장 (docs_bad 사용)

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma.from_documents(documents=docs_bad, embedding=embeddings)
```

step3\_rag.py에서는 문서 3개를 따로 저장했지만, 여기서는 모든 문서를 하나의 거대한 Document(`docs_bad`)로 합쳐서 저장합니다. 조각내지 않고 통째로 넣는 겁니다.

```python
# step3_rag_no_chunking.py — TODO: vectorstore.as_retriever로 검색기 생성 (search_kwargs={"k": 1})

# 3. 검색기 및 프롬프트 설정 (통째로 하나뿐이므로 k=1로 검색해도 전체가 다 나옴)
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
```

문서가 하나뿐이므로 `k=1`로도 전체가 다 나옵니다. step3\_rag.py의 `k=3`과 비교해 보세요. 나머지 코드(LLM 로드, 체인 조립, 질문 실행)는 step3\_rag.py와 동일하니 그대로 작성하면 됩니다.

```bash
# 실행
python step3_rag_no_chunking.py
```

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH01/terminal/01_no-chunking-compare.png", alt: [step3\_rag\_no\_chunking.py 실행 결과. 답변은 나오지만 문서를 통째로 넣었기 때문에 출처 구분이 없다.], max-width: 0.6)

답변 자체는 나오지만, 문서 전체가 하나의 덩어리이므로 "어떤 문서에서 가져왔는지"를 구분할 수 없습니다. step3\_rag.py에서는 인사규정만 깔끔하게 찾아왔던 것과 비교해 보세요. 관련 없는 내용이 섞이면 LLM이 정작 필요한 부분을 놓치기 쉽습니다. 문서를 조각으로 나누는 것, 즉 #strong[청킹(Chunking)] 이 왜 필요한지 바로 체감하실 수 있을 겁니다. 청킹 전략의 상세 비교는 CH08(검색 품질 튜닝)에서 다룹니다.

=== 2.9 실습 5 --- step4\_rag.py: 추론이 필요한 질문

step3\_rag.py까지의 질문은 "규정이 뭐야?" 같은 단순 검색이었습니다. 이번에는 #strong[규정을 찾아서 읽고 계산까지 해야 하는 질문]을 던져보겠습니다. `ex01/step4_rag.py`의 TODO를 `pass`를 지우고 작성합니다. 코드 구조는 step3\_rag.py와 동일하므로 TODO도 같은 방식으로 작성하면 됩니다. 달라진 건 파일에 준비된 #strong[질문]뿐입니다.

```python
question = "입사 6개월차 신입인데 리프레시 데이 2번 썼어. 몇 번 남았는지 규정 기반으로 계산해줘."
```

"리프레시 데이는 매월 1회 → 6개월이면 6번 → 2번 썼으면 4번 남음"처럼, 규정을 읽고 계산까지 해야 답할 수 있는 질문입니다.

```bash
# 실행
python step4_rag.py
```

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH01/terminal/01_step4-rag.png", alt: [step4\_rag.py 실행 결과. 규정을 바탕으로 리프레시 데이 잔여 횟수를 계산해 낸 모습이다.], max-width: 0.65)

검색된 문서(근거)와 함께 "매월 1회 × 6개월 = 6번, 2번 사용 → 4번 남음"이라는 계산 과정이 포함된 답변이 출력됩니다. 단순히 규정을 찾아오는 것을 넘어, LLM이 규정을 읽고 추론까지 해낸 겁니다.

=== 2.10 이것만은 기억하세요

- #strong[LLM은 우리 회사 문서를 읽은 적이 없습니다.] 아무리 자신감 있게 답해도 사내 정보는 우리가 직접 넣어줘야 합니다.
- #strong[RAG는 오픈북 시험입니다.] LLM이 모든 걸 외울 필요 없이 질문마다 관련 문서를 찾아보면서 답합니다.
- 이 챕터의 `RetrievalQA`는 LangChain이 만들어둔 완성품입니다. "RAG가 동작한다"를 체험하기엔 좋지만, 응답을 가공하거나 대화 기록을 붙이려면 내부를 건드려야 합니다. CH05에서 LCEL 파이프라인으로 교체하여 각 단계를 직접 조립합니다.
- 다음 챕터에서는 AI 비서가 조회할 실제 사내 시스템(직원, 연차, 매출 DB)을 FastAPI로 만들어 봅니다.

= Ch.2: FastAPI CRUD (ex02)

#quote(block: true)[한 줄 요약: AI 비서가 조회할 사내 시스템을 실행해보고 구조를 파악한다. API는 웨이터처럼 요청을 받아 DB에서 데이터를 가져다준다. \
핵심 개념: REST API, CRUD 패턴]

== AI 비서가 조회할 사내 시스템

=== 1.1 AI가 대답 못 하는 질문

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH02/gemini/02_chapter-opening.png", alt: [사내 AI 비서의 뼈대를 세우고, 첫 번째 시스템을 구성합니다], max-width: 0.7)

지난 챕터에서 RAG의 기본 개념을 알았습니다. 사내 문서를 벡터 DB에 넣어두면 질문할 때 관련 문서를 찾아서 답할 수 있다는 것.

#v(paragraph-gap)
좋습니다. 그런데 팀장이 저를 바라보며 말을 꺼냅니다.

#v(paragraph-gap)
#strong[팀장]: "문서 검색만 되면 안 되지." \
"'팀원 연차 몇 개 남았어?', '이번 달 개발팀 매출 얼마야?' 이런 것도 답해줘야지."

#v(paragraph-gap)
#emph[잠깐. 연차 잔여일은 문서에 적혀있는 게 아닌데?]

#v(paragraph-gap)
직원 데이터베이스에서 실시간으로 조회해야 하는 데이터입니다. 매출도 마찬가지입니다. 문서 검색으로는 절대 답할 수 없습니다.

#v(paragraph-gap)
AI 비서가 진짜 업무를 도우려면 사내 데이터를 조회할 수 있는 시스템이 먼저 있어야 합니다. AI가 "팀원 연차 잔여일을 알려줘"라고 부탁할 대상. 그게 없었던 것입니다.

#v(paragraph-gap)
그래서 이번 챕터에서는 AI 비서보다 먼저 #strong[사내 시스템]을 실행해 보겠습니다. 코드를 하나하나 뜯어보지는 않을 것입니다. 완성된 시스템을 띄워보고 "이런 데이터를 이렇게 조회할 수 있구나"를 확인하는 것이 목표입니다.

=== 1.2 직원 · 연차 · 매출

사내 데이터를 조회하려면 REST API가 필요합니다. AI 비서가 "팀원 연차 몇 개?"라고 물으면 API가 DB에서 찾아다 주는 구조입니다. CH06에서 #strong[MCP(Model Context Protocol)] 를 통해 AI가 직접 이 API를 호출하게 됩니다. 지금은 "AI가 쓸 시스템을 먼저 확인해두는 것"에 집중하겠습니다.

#v(paragraph-gap)
이 시스템이 관리할 데이터는 세 종류입니다.

#v(paragraph-gap)
#strong[직원(Employee)] --- 사번, 이름, 부서, 직급, 입사일. "EMP001 김철수 개발팀 대리."

#v(paragraph-gap)
#strong[연차(LeaveBalance)] --- 누가, 몇 년도에, 총 연차가 며칠이고, 사용한 게 며칠인지. "김민수의 2025년: 총 15일, 사용 3일, 잔여 12일."

#v(paragraph-gap)
#strong[매출(Sale)] --- 어느 부서가, 언제, 얼마를, 뭘 팔았는지. "개발팀 2025-03-01 5,000,000원 SI프로젝트."

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH02/gemini/02_erd-diagram.png", alt: [사내 시스템의 세 테이블. 직원을 중심으로 연차가 연결되고, 매출은 부서 단위로 독립 관리된다.], max-width: 0.6)

#v(paragraph-gap)
이 세 테이블에 대해 CRUD(등록/조회/수정/삭제) API를 제공하는 시스템. 그것이 이번 챕터에서 확인할 내용입니다.

=== 1.3 ConnectHR

테이블 구조를 팀장에게 보여주러 갔습니다. 화이트보드에 그린 테이블 구조를 훑어보던 팀장이 한마디 던집니다.

#v(paragraph-gap)
#strong[팀장]: "이 AI 비서, 이름이 뭐야?"

#v(paragraph-gap)
#emph[이름이요? 그냥 'AI 비서'라고 부르고 있었는데…]

#v(paragraph-gap)
#strong[팀장]: "프로젝트에 이름이 없으면 회의할 때 불편해. 우리 회사가 #strong[커넥트]잖아. HR 데이터 다루는 AI 비서니까… #strong[ConnectHR] 어때?"

#v(paragraph-gap)
커넥트의 HR 비서. 짧고 뭘 하는지 바로 알 수 있습니다.

#v(paragraph-gap)
#strong[오픈이]: "좋네요. ConnectHR."

#v(paragraph-gap)
이름이 붙으니 프로젝트가 진짜 시작된 느낌입니다. 지금은 사내 시스템만 있는 빈 껍데기지만 앞으로 챕터를 거듭하면서 #strong[ConnectHR]이 한 단계씩 성장합니다. 문서를 읽고 질문에 답하고 DB도 조회하며, 결국 진짜 사내 비서가 되는 여정입니다.

#v(paragraph-gap)
이제 실습으로 사내 시스템을 직접 실행해보겠습니다.

== ConnectHR API 서버 구축하기

=== 2.1 용어 정리

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([이야기 속 표현], [진짜 용어], [정식 정의],),
    table.hline(),
    ["식당 웨이터"], [#strong[REST API]], [HTTP 메서드(GET/POST/PATCH/DELETE)로 자원을 조작하는 인터페이스],
    ["메뉴판의 네 동작"], [#strong[CRUD]], [Create, Read, Update, Delete --- 데이터의 기본 4가지 조작],
    ["주방"], [#strong[PostgreSQL]], [관계형 데이터베이스. 테이블 형태로 데이터를 저장하고 SQL로 조회],
    ["주문서 양식"], [#strong[Pydantic]], [요청/응답 데이터의 구조와 검증 규칙을 정의하는 Python 라이브러리],
  )]
  , kind: table
  )

=== 2.2 소스 코드 준비

클론한 레포에서 이번 챕터의 폴더로 이동합니다.

```bash
cd rag-start/ex02
```

```
ex02/
├── run.py                 [참고] 서버 플로우 실행
├── docker-compose.yml     [참고] PostgreSQL 컨테이너
├── requirements.txt       [참고] 의존성 목록
├── app/
│   ├── main.py            [참고] FastAPI 진입점
│   ├── api.py             [참고] REST API 엔드포인트
│   ├── crud.py            [참고] DB CRUD 로직
│   ├── database.py        [참고] PostgreSQL 연결
│   ├── models.py          [참고] 도메인 dataclass
│   ├── schemas.py         [참고] Pydantic 데이터 검증
│   └── views.py           [참고] 관리자 웹 라우터
├── data/
│   └── schema.sql         [참고] 기본 테이블 및 샘플 데이터
├── templates/             [참고] 웹 UI HTML
└── static/                [참고] 웹 CSS/JS
```

=== 2.3 실습 환경 준비

#quote(block: true)[기본 환경(Python 3.12, Docker)이 없다면 #strong[교육자료]를 먼저 확인해 주시길 바랍니다.]

```bash
cd ex02
cp .env.example .env
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
docker compose up -d
pip install -r requirements.txt
```

`docker compose up -d`를 실행하면 PostgreSQL 컨테이너가 시작되면서 `data/schema.sql`이 자동 실행됩니다. 직원 5명, 연차, 매출 데이터가 미리 입력되어 있어 바로 조회할 수 있습니다.

#callout-box([Apple Silicon(M1/M2/M3) 사용자], [psycopg2-binary 설치가 실패한다면 `brew install libpq`를 먼저 실행해 보시기 바랍니다.])

#figure(
  align(center)[#table(
    columns: 2,
    align: (auto,auto,),
    table.header([패키지], [역할],),
    table.hline(),
    [`fastapi`], [웹 API 서버],
    [`uvicorn`], [ASGI 서버],
    [`jinja2`], [HTML 템플릿 엔진],
    [`psycopg2-binary`], [PostgreSQL 드라이버],
    [`pydantic`], [요청/응답 데이터 검증],
    [`python-dotenv`], [환경 변수 관리],
    [`python-multipart`], [폼 데이터 파싱],
  )]
  , kind: table
  )

=== 2.4 실습 순서

+ `python run.py` --- 서버 시작
+ `/docs` --- Swagger UI 확인
+ CRUD 테스트 --- POST, GET, PATCH, DELETE
+ `/admin/` --- 웹 UI 확인

#v(paragraph-gap)
서버를 실행하고 Swagger UI(`/docs`)에서 API를 직접 호출해 보고, 웹 UI(`/admin/`)를 통해 일반 사용자 화면도 확인해 보시기 바랍니다.

```bash
# 실행
python run.py
```

브라우저에서 `http://localhost:8000/docs`를 열면 #strong[Swagger UI]가 뜹니다. FastAPI가 코드에서 자동으로 만들어주는 API 문서입니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH02/terminal/02_swagger-ui.png", max-width: 0.6) #auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH02/terminal/02_api-test-employee.png", max-width: 0.6)

#v(paragraph-gap)
#emph[Swagger UI에서 직원 등록(POST) 후 조회(GET)한 결과]

#v(paragraph-gap)
직원, 연차, 매출 --- 세 영역의 API가 보입니다. 직접 클릭하여 구조를 살펴 보시기 바랍니다.

#v(paragraph-gap)
POST 요청으로 직원을 등록하고 GET으로 조회하면, 우리가 방금 입력한 직원의 정보가 확인될 것입니다. 나아가 수정(PATCH)과 삭제(DELETE) 기능도 완벽하게 지원합니다. 우리가 목표로 했던 네 가지 기본 동작(CRUD)이 모두 정상 작동함을 증명한 셈입니다.

#v(paragraph-gap)
자, 그런데 Swagger UI는 어디까지나 API 검증용 화면입니다. 시스템에는 코드를 모르는 일반 사용자도 데이터를 다룰 수 있는 웹 화면이 포함되어 있습니다. 브라우저 창에서 `http://localhost:8000/admin/`을 열어 어떻게 생겼는지 살펴보겠습니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH02/terminal/02_admin-dashboard.png", alt: [Jinja2 템플릿으로 만든 관리자 대시보드. 직원, 연차, 매출 현황을 한눈에 볼 수 있다.], max-width: 0.6)

#v(paragraph-gap)
직원 관리 메뉴에서 사번과 이름, 부서, 직급, 입사일을 입력하고 등록하면 아래 목록에 바로 나타납니다. 기존 직원 5명에서 홍길동 사원이 추가된 것을 확인할 수 있습니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH02/terminal/02_admin-employee-create.png", alt: [웹 UI에서 직원을 등록하면 목록에 바로 반영된다. API를 몰라도 CRUD가 된다.], max-width: 0.6)

#v(paragraph-gap)
API는 뒷단의 배관이고 웹 UI는 수도꼭지입니다. 사용자는 수도꼭지만 틀면 되고 물이 어떤 배관을 타고 오는지 몰라도 됩니다. 나중에 AI 비서도 같은 배관(API)을 사용합니다. 다만 수도꼭지 대신 코드로 작동시킬 뿐입니다.

#quote(block: true)[`Ctrl + C`를 눌러 서버를 종료해 줍니다. Docker 컨테이너도 `docker compose down` 명령어로 깔끔하게 정리해 두겠습니다.]

=== 2.5 API 엔드포인트 목록

이 시스템이 제공하는 API 전체 목록입니다. CH06에서 AI 비서가 MCP로 이 API를 호출하게 됩니다.

#figure(
  align(center)[#table(
    columns: 3,
    align: (auto,auto,auto,),
    table.header([메서드], [경로], [설명],),
    table.hline(),
    [GET], [`/api/employees`], [직원 목록 조회 (이름/부서 필터)],
    [POST], [`/api/employees`], [직원 등록],
    [GET], [`/api/employees/{emp_no}`], [직원 상세 조회],
    [PATCH], [`/api/employees/{emp_no}`], [직원 정보 수정],
    [DELETE], [`/api/employees/{emp_no}`], [직원 삭제],
    [GET], [`/api/leaves`], [연차 목록 조회 (직원/연도 필터)],
    [POST], [`/api/leaves`], [연차 등록],
    [POST], [`/api/leaves/usage`], [연차 사용 등록],
    [PATCH], [`/api/leaves/{emp_no}/{year}`], [연차 정보 수정],
    [GET], [`/api/sales`], [매출 목록 조회 (부서/기간 필터)],
    [POST], [`/api/sales`], [매출 등록],
    [GET], [`/api/sales/dept-summary`], [부서별 매출 합계],
  )]
  , kind: table
  )

#callout-box([팁: 코드가 궁금하다면], [`code/ex02/app/` 폴더에 전체 소스가 있습니다. FastAPI + psycopg2 + Pydantic 조합으로 만들어져 있습니다. 이 책의 핵심 주제가 아니므로 상세한 코드 설명은 생략하지만, 관심이 있으시다면 언제든 직접 읽어보시는 것을 바랍니다.])

=== 2.6 더 알아보기

#strong[Swagger UI] --- FastAPI는 코드에서 API 문서를 자동 생성합니다. Pydantic 스키마에 적어둔 필드 설명과 타입이 그대로 문서에 나옵니다. `/docs`는 Swagger UI, `/redoc`은 ReDoc 스타일로 볼 수 있습니다.

#v(paragraph-gap)
#strong[DeptSummary] --- `GET /api/sales/dept-summary`는 부서별 매출 합계를 반환합니다. CH06에서 AI 비서의 `sales_sum` 도구가 이 엔드포인트를 호출해서 "개발팀 매출 얼마야?"에 답하게 됩니다.

=== 2.7 이것만은 기억하세요

- #strong[AI 비서가 조회할 사내 시스템이 준비됐습니다.] API는 식당 웨이터처럼 요청을 받아 DB에서 데이터를 가져다줍니다.
- #strong[CRUD 네 가지면 거의 모든 데이터를 관리할 수 있습니다.] 등록하고 조회하고 수정하고 삭제하기.
- 다음 챕터에서는 AI 비서에게 먹일 사내 문서를 어떻게 수집하고 정리할지 설계합니다.

= Ch.3: 문서 표준과 메타데이터 (ex03)

#quote(block: true)[한 줄 요약: AI에게 좋은 답을 원하면 좋은 문서를 넣어야 한다. 도서관처럼 분류하고 라벨을 붙이자. \
핵심 개념: 문서 품질, 메타데이터, 청킹 전략 사전 설계, 재인덱싱 전략]

== 도서관처럼 문서를 정리하다

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH03/gemini/03_chapter-opening.png", alt: [수백 개의 사내 문서 중 어떤 것을 AI에게 먹여야 할지 고르는 순간], max-width: 0.7)

=== 1.1 "이걸 다 넣어야 해?"

CH02에서 사내 시스템은 만들었습니다. 직원, 연차, 매출 데이터는 API로 조회할 수 있습니다. 이제 AI 비서의 나머지 절반인 #strong[문서 검색]을 본격적으로 준비할 차례입니다.

#v(paragraph-gap)
CH01에서 더미 문서 3개로 RAG를 돌려봤습니다. 잘 됐습니다. 그래서 이번에는 사내 공유 드라이브에 있는 문서를 전부 긁어서 벡터 DB에 밀어 넣어봤습니다.

#v(paragraph-gap)
#emph[이건 금방이겠지.]

#v(paragraph-gap)
결과는 참담했습니다. "병가 규정 알려줘"라고 물었더니 2년 전 폐기된 규정을 근거로 답변합니다. "연차 15일입니다"라고 자신 있게 답하는데, 실제로는 규정이 바뀌어서 20일입니다. 환각보다 나쁩니다. 출처까지 달려 있으니까 그걸 믿게 되거든요.

#v(paragraph-gap)
#strong[동료]: "야, 연차 15일이라고 했는데 인사팀에서 20일이래. AI 비서한테 물어봤다고 했다가 혼났어."

#v(paragraph-gap)
#emph[…아.] 그제야 공유 드라이브를 다시 열었습니다. 마우스 휠을 굴리는데 파일 목록이 끝없이 내려갑니다. 취업규칙.pdf, 보안지침\_v3\_최종\_진짜최종.docx, 2024년\_복지정책.xlsx, 회의록\_0301.hwp, 프로젝트\_보고서.pptx…

#v(paragraph-gap)
#emph[300개… 이걸 하나하나 다 열어봐야 하나?]

#v(paragraph-gap)
의자를 뒤로 밀고 천장을 올려다봤습니다. 형식이 제각각입니다. PDF도 있고 워드도 있고 엑셀도 있고, 심지어 한글 파일까지 있습니다. 어떤 건 최신이고 어떤 건 2년 전 문서입니다. 이걸 정리하지 않고 통째로 넣으니까 이 꼴이 난 것입니다.

=== 1.2 문서 필터링 기준

#strong[팀장]: "도서관 가면 책 아무 데나 꽂아?"

#v(paragraph-gap)
한마디에 머리가 맑아졌습니다. 새 책이 기증되면 사서가 바로 서가에 꽂지 않습니다.

#v(paragraph-gap)
+ #strong[먼저 분류합니다] --- 이 책이 어느 분야인지, 대여 가능한지, 최신판인지 확인합니다.
+ #strong[라벨을 붙입니다] --- 청구기호(위치), 저자, 출판년도, 키워드를 기록합니다.
+ #strong[서가에 꽂습니다] --- 분류에 맞는 위치에 넣습니다.

#v(paragraph-gap)
라벨 없이 마구잡이로 꽂아놓으면 어떻게 될까요? 나중에 찾을 수가 없습니다. "경영학 개론이 어딨지?" 하면서 서가 전체를 뒤집게 됩니다. 사내 문서도 마찬가지입니다. 벡터 DB에 넣기 전에 #strong[분류하고 라벨을 붙이고 정리하는 단계]가 필요합니다. 이 단계를 건너뛰면 검색 품질이 엉망이 됩니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH03/gemini/03_document-pipeline.png", alt: [사내 문서를 벡터 DB에 넣기까지. 정리 없이 넣으면 검색 품질이 떨어진다.], max-width: 0.6)

=== 1.3 넣을 문서와 뺄 문서

모든 문서를 넣을 필요는 없습니다. 오히려 필요 없는 문서가 섞여 들어가면 검색 품질이 떨어집니다. 동료가 당한 것처럼 폐기된 규정이 검색되면 곤란합니다.

#v(paragraph-gap)
#strong[넣어야 할 것]: 현재 유효한 규정, 정책, 가이드. 자주 질문받는 내용이 담긴 문서.

#v(paragraph-gap)
#strong[빼야 할 것]: 폐기된 문서, 개인 메모, 초안, 중복 문서(같은 내용의 v1/v2/v3).

#v(paragraph-gap)
간단한 기준 하나면 충분합니다. "이 문서를 신입사원에게 줘도 되나?" 된다면 넣고, 아니라면 뺍니다.

=== 1.4 포맷 통일 --- Markdown 변환

PDF, DOCX, XLSX --- 형식이 제각각입니다. 이걸 그대로 벡터 DB에 넣을 수는 없습니다. 벡터 DB는 #strong[텍스트]만 이해하기 때문입니다.

#v(paragraph-gap)
해외 지사에서 보고서가 도착했다고 상상해보겠습니다. 미국 지사는 영어로, 일본 지사는 일본어로, 프랑스 지사는 프랑스어로 보냈습니다. 이 보고서를 우리 팀원 누구나 검색하고 읽으려면? 먼저 #strong[한국어로 번역]해서 하나의 언어로 통일해야 합니다. PDF/DOCX/XLSX도 같은 문제입니다. 형식이 제각각이면 벡터 DB가 읽지 못합니다. 먼저 #strong[하나의 텍스트 형태]로 바꿔야 합니다.

#v(paragraph-gap)
이 책에서는 #strong[Markdown]으로 통일합니다. 왜 Markdown을 사용할까요?

#v(paragraph-gap)
- LLM이 가장 잘 이해하는 포맷입니다. 훈련 데이터에 Markdown이 대량 포함되어 있어서 `# 제목`이나 `- 목록` 같은 구조를 자연스럽게 인식합니다.
- 제목이 보존됩니다. PDF의 큰 글씨, DOCX의 "제목 1" 스타일이 `# 제목`으로 바뀝니다.
- 표도 보존됩니다. 엑셀 시트가 `| 열1 | 열2 |` 형태로 바뀝니다.
- 사람도 읽을 수 있습니다. 변환 결과가 제대로인지 눈으로 바로 확인할 수 있습니다.

#callout-box([Tip], [반드시 Markdown이어야 하는 건 아닙니다. 일반 텍스트(plain text)나 JSON으로 변환해도 벡터 DB에 넣을 수 있습니다. 다만 Markdown은 제목·표·목록 같은 #strong[문서 구조를 보존하면서도 가볍다]는 점에서 RAG 파이프라인에 가장 널리 쓰입니다.])

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH03/diagram/03_parser-flow.png", alt: [파서가 다양한 형식을 Markdown 텍스트로 통일한다. 그래야 청킹하고 검색할 수 있다.], max-width: 0.6)

=== 1.5 메타데이터 태깅

도서관에서 책에 붙이는 정보가 있죠. 청구기호, 저자, 분야, 출판년도. 문서 세계에서는 이걸 #strong[메타데이터]라고 부릅니다. 메타데이터가 왜 중요할까요? AI 비서에게 "보안 관련 규정 알려줘"라고 물었을 때 메타데이터에 `file_name: SEC_보안규정`이 있으면 보안 문서를 바로 식별합니다. 없으면? 모든 문서를 처음부터 끝까지 뒤져야 합니다.

#v(paragraph-gap)
어떤 메타데이터를 붙일지는 프로젝트마다 다릅니다. 작성자, 부서, 보안등급, 유효기간 등 필요한 정보가 다양합니다. 우리는 최소한의 것만 쓰기로 했습니다. #strong[파서가 파일명과 경로에서 자동으로 추출할 수 있는 것]만 사용합니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([메타데이터], [추출 방식], [예시],),
    table.hline(),
    [파일명 (file\_name)], [파일에서 자동], [`HR_취업규칙_v1.0.pdf`],
    [파일 형식 (file\_type)], [확장자에서 자동], [`pdf`],
    [원본 경로 (source\_path)], [폴더 구조에서 자동], [`docs/hr/HR_취업규칙_v1.0.pdf`],
    [문서 ID (doc\_id)], [파일명에서 자동 생성], [`hr_취업규칙_v1_0`],
    [페이지 (page)], [파싱 시 자동], [`1`],
  )]
  , kind: table
  )

사람이 직접 입력하는 항목이 하나도 없습니다. 대신 #strong[파일명에 정보를 담는 것]이 중요합니다. `HR_취업규칙_v1.0.pdf`처럼 분류(HR)와 버전(v1.0)을 파일명에 넣으면 파서가 알아서 메타데이터로 만들어줍니다.

=== 1.6 청킹 전략 사전 설계

CH01에서 이미 경험했습니다. 문서를 통째로 넣으면 검색 정확도가 떨어집니다. 적절한 크기로 #strong[조각(chunk)] 을 내야 합니다. 조각 크기를 어떻게 정해야 할까요? 너무 작으면 문맥이 잘리게 됩니다. "신입사원은 3년 동안 연차가 없다" 다음 줄에 "대신 리프레시 데이를 제공한다"가 있는데 잘못 자르면 "연차가 없다"만 나오게 됩니다.

#v(paragraph-gap)
너무 크면 CH01의 노청킹 실험처럼 관련 없는 내용까지 함께 검색 결과에 딸려오게 됩니다.

#v(paragraph-gap)
지금은 전체적인 설계만 살펴두겠습니다. 실제 구현은 다음 장인 CH04(VectorDB 구축)에서 차례대로 진행해 보겠습니다.

#figure(
  align(center)[#table(
    columns: 4,
    align: (auto,auto,auto,auto,),
    table.header([전략], [크기], [오버랩], [적합한 경우],),
    table.hline(),
    [고정 크기], [500자], [100자], [규정, 매뉴얼 (구조화된 문서)],
    [문단 기준], [문단 단위], [---], [보고서, 회의록 (자연스러운 구분)],
    [의미 기준], [가변], [---], [긴 문서, 주제 전환이 잦은 문서],
  )]
  , kind: table
  )

#quote(block: true)[이 책에서는 CH04에서 #strong[고정 크기(500자 + 100자 오버랩)] 로 시작하고, CH08(검색 품질 튜닝)에서 의미 기준 청킹과 비교 실험을 합니다.]

=== 1.7 재인덱싱 전략

사내 문서는 살아있습니다. 취업규칙이 개정되고 새 보안지침이 나오고 복지정책이 바뀝니다. 벡터 DB에 한 번 넣어놓고 끝이 아닙니다. 재인덱싱을 안 하면 어떻게 됩니까? 1.1에서 동료가 당한 것과 똑같은 일이 반복됩니다. 규정이 바뀌었는데 벡터 DB에는 옛날 문서가 그대로 남아있기 때문입니다.

#v(paragraph-gap)
재인덱싱에는 두 가지 방식이 있습니다. #strong[전체 재인덱싱] --- 모든 문서를 지우고 처음부터 다시 넣습니다. 간단하지만 시간이 오래 걸립니다. #strong[증분 재인덱싱] --- 변경된 문서만 업데이트합니다. 빠르지만 "어떤 문서가 변경됐는지" 추적해야 합니다.

#quote(block: true)[이 책에서는 문서 수가 적으므로 #strong[전체 재인덱싱]으로 충분합니다. 문서가 수천 개 이상이면 증분 방식을 고려합니다.]

=== 1.8 docs/ 폴더 구조

정리해 보겠습니다. 우리 사내 AI 비서에 넣을 문서는 다음과 같은 구조로 관리하도록 하겠습니다.

```
data/docs/
├── hr/                              ← 분류가 폴더명
│   ├── HR_취업규칙_v1.0.pdf          ← 분류_제목_버전이 파일명
│   └── HR_정보보안서약서.pdf
├── security/
│   └── SEC_보안규정_v1.0.docx
├── finance/
│   ├── FIN_2025_상반기_매출현황.xlsx
│   └── FIN_부서별_예산기안서.xlsx
└── ops/
    └── OPS_신규서비스_런칭전략.pdf
```

별도의 메타데이터 파일을 만들 필요가 없습니다. #strong[폴더 구조와 파일명이 곧 메타데이터]이기 때문입니다. 소스 코드 준비

== 문서 표준과 수집 규칙 설계하기

=== 2.1 용어 정리

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([비유], [진짜 용어], [정식 정의],),
    table.hline(),
    [하나의 언어로 번역], [파싱 (Parsing)], [다양한 형식(PDF/DOCX/XLSX)에서 텍스트를 추출해 통일된 형태로 변환하는 과정],
    [도서관에서 책에 붙이는 정보], [메타데이터 (Metadata)], [문서 자체 내용이 아닌 문서에 대한 정보 (파일명, 형식, 경로 등)],
    [적절한 크기로 조각내기], [청킹 (Chunking)], [긴 문서를 벡터 DB에 저장할 수 있는 크기로 분할하는 과정],
    [잘못 자르면 문맥이 잘린다], [오버랩 (Overlap)], [청크 경계에서 문맥이 잘리지 않도록 앞뒤를 겹치게 자르는 기법],
    [규정이 바뀌었는데 옛날 문서가 그대로], [재인덱싱 (Re-indexing)], [변경되거나 추가된 문서를 벡터 DB에 반영하는 과정],
    [전부 긁어서 밀어 넣었더니 엉망], [GIGO (Garbage In, Garbage Out)], [입력 데이터 품질이 출력 품질을 결정한다는 원칙],
  )]
  , kind: table
  )

=== 2.2 문서 표준 규칙 (템플릿)

실제 프로젝트에서 사내 문서를 관리할 때 참고할 규칙입니다.

#v(paragraph-gap)
#strong[\1. 파일 형식 제한]

#figure(
  align(center)[#table(
    columns: 3,
    align: (auto,auto,auto,),
    table.header([허용 형식], [파서], [비고],),
    table.hline(),
    [PDF], [pypdf], [텍스트 기반. 이미지 PDF는 CH10에서 OCR 처리],
    [DOCX], [python-docx], [표, 목록 포함 가능],
    [XLSX], [openpyxl], [표 형태 데이터 (규정 비교표 등)],
    [TXT/MD], [기본 읽기], [가장 깔끔],
  )]
  , kind: table
  )

#quote(block: true)[HWP, PPT는 이 책에서 다루지 않습니다. 가능하시다면 PDF로 변환 후 사용해 주시길 바랍니다.]

#strong[\2. 메타데이터 --- 파일명 규칙]

#v(paragraph-gap)
별도의 JSON 파일은 만들지 않습니다. 파서가 파일명과 경로에서 자동 추출하기 때문에 #strong[파일명 규칙]이 중요합니다.

#quote(block: true)[\[분류\]#emph[\[제목\]]\[버전\].확장자

#v(paragraph-gap)
예시: HR\_취업규칙\_v1.0.pdf → file\_name: HR\_취업규칙\_v1.0.pdf SEC\_보안규정\_v1.0.docx → file\_type: docx FIN\_2025\_상반기\_매출현황.xlsx → source\_path: data/docs/finance/…]

#strong[\3. 청킹 설계 가이드]

#figure(
  align(center)[#table(
    columns: 3,
    align: (auto,auto,auto,),
    table.header([항목], [권장값], [이유],),
    table.hline(),
    [기본 크기], [500자], [한국어 기준 2\~3문단. 의미 단위와 대략 일치],
    [오버랩], [100자], [청크 경계에서 문맥 유지],
    [최소 크기], [100자], [너무 짧은 청크는 의미 없음 → 이전 청크에 병합],
  )]
  , kind: table
  )

#strong[\4. 재인덱싱 운영 가이드]

#figure(
  align(center)[#table(
    columns: 3,
    align: (auto,auto,auto,),
    table.header([시점], [방식], [실행],),
    table.hline(),
    [규정 개정 시], [전체 재인덱싱], [수동 트리거],
    [주기적], [전체 재인덱싱], [월 1회 (문서 수 적을 때)],
    [문서 추가 시], [해당 문서만 추가], [기존 인덱스 유지],
  )]
  , kind: table
  )

=== 2.3 더 알아보기

#strong[문서 품질 체크리스트] --- 벡터 DB에 넣기 전에 함께 점검해 볼 항목입니다. - (1) 현재 유효한 문서인가? - (2) 중복 문서가 없는가? - (3) 텍스트 추출이 가능한가(이미지만 있는 PDF 아닌가)? - (4) 메타데이터가 기록되어 있는가?

#v(paragraph-gap)
#strong[한국어 청킹의 특수성] --- 영어는 단어 사이에 공백이 있어서 토큰 수 기반 청킹이 자연스럽습니다. 한국어는 띄어쓰기 단위가 영어보다 크고 조사가 붙기 때문에 같은 500자라도 정보 밀도가 다를 수 있습니다. CH08에서 의미 기반 청킹(Semantic Chunking)과 비교 실험을 진행해 보겠습니다.

#v(paragraph-gap)
#strong[메타데이터 필터링] --- 이 프로젝트에서 쓰는 ChromaDB는 저장할 때 메타데이터를 함께 넣을 수 있고 검색할 때 `where={"file_type": "pdf"}`처럼 필터를 걸 수 있습니다. 지금은 메타데이터를 검색 결과의 출처 표시용으로 활용하지만 문서가 많아지면 필터링으로 검색 범위를 좁히는 것도 가능합니다.

#callout-box([Tip], [메타데이터 필터링은 벡터 DB마다 문법이 다릅니다. ChromaDB는 `where={"key": "value"}` 딕셔너리 방식이고 Pinecone은 `filter={"key": {"$eq": "value"}}` 처럼 MongoDB 스타일 연산자를 씁니다. PostgreSQL 기반 pgvector는 아예 SQL `WHERE` 절로 필터링합니다. 문법만 다를 뿐 "메타데이터로 검색 범위를 좁힌다"는 개념은 동일합니다.])

=== 2.4 이것만은 기억하세요

- #strong[AI에게 좋은 답을 원하면 좋은 문서를 넣어야 합니다.] 쓰레기를 넣으면 결국 쓰레기가 나오게 됩니다(Garbage In, Garbage Out).
- #strong[PDF/DOCX/XLSX는 먼저 Markdown 텍스트로 통일해야 합니다.] 형식이 다르면 올바른 청킹도, 검색도 불가능해집니다.
- #strong[폴더 구조와 파일명이 곧 메타데이터입니다.] 파서가 자동으로 추출하므로 파일명 규칙을 지켜 주시길 바랍니다.
- 다음 챕터에서는 이 문서를 실제로 파싱하고 청킹해서 벡터 DB에 저장해 보겠습니다.

= Ch.4: 파싱 · 청킹 · 임베딩 · ChromaDB (ex04)

#quote(block: true)[한 줄 요약: 문서는 조각내야 찾는다. 손질(파싱), 다지기(청킹), 양념(임베딩), 냉장고(벡터DB). \
핵심 개념: 문서 파싱, 청킹, 임베딩, 벡터 저장/검색, 임베딩 모델 선택 기준]

== 요리처럼 문서를 손질하다

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH04/gemini/04_chapter-opening.png", alt: [문서를 잘게 쪼개고 벡터로 변환하여 검색 가능한 지식으로 만듭니다], max-width: 0.7)

=== 1.1 "정리는 했는데, 어떻게 넣지?"

CH03에서 사내 문서를 정리했습니다. 분류도 마쳤고 메타데이터 라벨도 부착했습니다. 이제 이 문서들을 벡터 DB에 넣어서 AI 비서가 검색할 수 있게 만들 차례입니다.

#v(paragraph-gap)
그런데 문서를 그냥 통째로 넣으면 될까요? CH01에서 이미 경험했습니다. 더미 문서 3개는 괜찮았습니다. 하지만 실제 사내 문서는 다릅니다. 취업규칙만 해도 수십 페이지인데, 이걸 통째로 넣으면 "연차 몇 일이야?"라고 물었을 때 보안규정이랑 매출 현황까지 딸려옵니다. 문서를 #strong[검색 가능한 지식]으로 바꾸려면 몇 단계를 거쳐야 합니다.

=== 1.2 네 단계 파이프라인

#strong[팀장]: "재료 손질 안 하고 요리해본 적 있어?"

#v(paragraph-gap)
냉장고에 식재료를 넣는 걸 생각해보겠습니다. 마트에서 사온 재료를 봉지째로 냉장고에 던져 넣으면 어떻게 될까요? 나중에 찾을 수가 없습니다. 양파가 어디 있는지, 고기는 아직 쓸 수 있는지 뒤져봐야 알 수 있습니다. 제대로 하려면 이런 과정을 거칩니다.

#v(paragraph-gap)
+ #strong[손질한다] --- 흙을 씻고, 껍질을 벗기고, 뼈를 발라낸다. 먹을 수 없는 부분을 제거한다.
+ #strong[다진다] --- 요리에 맞게 적당한 크기로 자른다. 너무 크면 익지 않고, 너무 작으면 형체가 없어진다.
+ #strong[양념한다] --- 소금에 절이거나 밑간을 한다. 나중에 바로 쓸 수 있게 맛을 입힌다.
+ #strong[냉장고에 정리한다] --- 라벨을 붙이고, 구분해서 넣는다. "닭가슴살 --- 3월 5일 --- 볶음용"

#v(paragraph-gap)
사내 문서도 똑같습니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([요리 과정], [문서 처리], [무슨 일이 벌어지나],),
    table.hline(),
    [손질], [#strong[파싱] (Parsing)], [PDF/DOCX/XLSX에서 텍스트를 꺼낸다],
    [다지기], [#strong[청킹] (Chunking)], [텍스트를 적당한 크기로 조각낸다],
    [양념], [#strong[임베딩] (Embedding)], [텍스트 조각을 숫자 벡터로 변환한다],
    [냉장고 정리], [#strong[벡터 DB 저장]], [벡터를 ChromaDB에 넣고 검색 가능하게 한다],
  )]
  , kind: table
  )

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH04/gemini/04_vectordb-pipeline.png", alt: [문서를 벡터 DB에 넣는 과정은 요리의 손질 → 다지기 → 양념 → 냉장고 정리와 같다.], max-width: 0.6)

=== 1.3 파싱 --- 문서에서 텍스트 꺼내기

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH04/gemini/04_example_hr_rules.png", alt: [예제로 포함된 취업규칙 PDF 파일의 원본 화면], max-width: 0.6)

위 예제로 들어가 있는 취업규칙 PDF 파일을 확인해 보겠습니다. 사람 눈에는 글자가 보이지만 컴퓨터 입장에서는 그냥 바이너리 데이터입니다. "취업규칙 제1조"라는 텍스트를 꺼내려면 #strong[파서(Parser)] 가 필요합니다.

#v(paragraph-gap)
문제는 형식마다 파서가 다르다는 점입니다. PDF는 PDF 파서가, DOCX는 DOCX 파서가, XLSX는 XLSX 파서가 필요합니다. CH03에서 허용한 형식 세 가지, 그대로입니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([형식], [파서 라이브러리], [특징],),
    table.hline(),
    [PDF], [pypdf], [텍스트 기반 PDF에서 페이지별 텍스트 추출],
    [DOCX], [python-docx], [단락(Paragraph)과 표(Table) 추출, 제목을 마크다운으로 변환],
    [XLSX], [openpyxl], [시트별 셀 데이터를 행 단위로 읽기],
  )]
  , kind: table
  )

그런데 모든 PDF가 잘 읽히는 건 아닙니다. #strong[이미지로 된 PDF] (스캔한 문서나 캡처 화면)는 텍스트가 아예 추출되지 않습니다. 이 문제는 CH10에서 OCR과 Vision LLM으로 해결합니다. 지금은 텍스트 기반 문서만 다룹니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH04/diagram/04_parser-select.png", alt: [파일 확장자에 따라 적절한 파서를 선택한다. 통합 함수 하나로 자동 분기.], max-width: 0.6)

#v(paragraph-gap)
실제 우리 프로젝트의 `data/docs/` 폴더. 6개 문서가 있습니다.

```
data/docs/
├── hr/
│   ├── HR_취업규칙_v1.0.pdf
│   └── HR_정보보안서약서.pdf
├── security/
│   └── SEC_보안규정_v1.0.docx
├── finance/
│   ├── FIN_2025_상반기_매출현황.xlsx
│   └── FIN_부서별_예산기안서.xlsx
└── ops/
    └── OPS_신규서비스_런칭전략.pdf
```

CH03에서 설계한 분류 구조 그대로입니다. 이 6개 문서를 파싱하면, 순수 텍스트가 추출됩니다.

=== 1.4 청킹 --- 적당한 크기로 자르기

텍스트를 꺼냈습니다. 그런데 취업규칙 전문이 한 덩어리로 들어가면 안 됩니다. CH01에서 겪은 바로 그 문제입니다 --- 문서가 너무 크면 관련 없는 내용까지 딸려옵니다.

#v(paragraph-gap)
요리에서 재료를 다지듯이 텍스트를 #strong[적당한 크기의 조각(chunk)] 으로 잘라야 합니다.

#v(paragraph-gap)
CH03에서 설계한 대로 #strong[고정 크기 500자 + 100자 오버랩]으로 갑니다.

#v(paragraph-gap)
처음에는 오버랩 없이 500자씩 딱딱 잘라봤습니다.

#v(paragraph-gap)
#emph[500자마다 자르면… 문장 중간에서 잘리는 거 아니야?]

#v(paragraph-gap)
맞습니다. 실제로 어떻게 잘리는지 보겠습니다.

#v(paragraph-gap)
오버랩 없이 500자에서 딱 자르면 이렇게 됩니다.

```
[청크 1] ...신입사원은 입사 후 처음 3년 동안은 법정 연차가 발생하지 않습니다.
[청크 2] 대신 매월 1회의 유급 '리프레시 데이'를 휴가로 사용할 수 있습니다...
```

"연차가 없다"만 남고 "대신 리프레시 데이가 있다"는 다음 조각으로 넘어갔습니다. AI 비서가 청크 1만 검색하면 "연차 없음"이라고만 답합니다.

#v(paragraph-gap)
100자 오버랩을 주면 앞뒤 조각이 겹칩니다.

```
[청크 1] ...신입사원은 입사 후 처음 3년 동안은 법정 연차가 발생하지 않습니다.
          대신 매월 1회의 유급 '리프레시 데이'를 휴가로...
[청크 2] ...법정 연차가 발생하지 않습니다. 대신 매월 1회의 유급 '리프레시
          데이'를 휴가로 사용할 수 있습니다. 3년 근속 시 30일의 연차가...
```

어느 조각을 검색하든 "연차 없음 + 리프레시 데이" 문맥이 이어집니다.

#v(paragraph-gap)
각 조각에는 #strong[메타데이터]도 함께 붙습니다. CH03에서 설계한 라벨이 여기서 쓰입니다.

```json
{
  "text": "신입사원은 입사 후 처음 3년 동안은 법정 연차가 발생하지 않습니다. 대신 매월 1회의 유급 '리프레시 데이'를 휴가로...",
  "metadata": {
    "file_name": "HR_취업규칙_v1.0.pdf",
    "file_type": "pdf",
    "source_path": "data/docs/hr/HR_취업규칙_v1.0.pdf",
    "doc_id": "hr_취업규칙_v1_0",
    "page": 3
  }
}
```

나중에 AI 비서가 "이 답변의 출처는 취업규칙 3페이지입니다"라고 말할 수 있는 이유가 바로 이 메타데이터입니다.

=== 1.5 임베딩 --- 의미를 숫자로 바꾸기

텍스트를 자르고 라벨을 붙이는 것까지는 사람이 이해할 수 있는 작업입니다.

#v(paragraph-gap)
하지만 여기서부터 좀 다릅니다. "연차 사용 규정"이라는 텍스트를 컴퓨터가 이해할 수 있을까요? 컴퓨터는 자연어 글자를 모릅니다. 단지 숫자만 연산할 수 있습니다. #strong[임베딩(Embedding)] 은 텍스트의 #strong[의미]를 숫자 벡터(768개의 숫자 리스트)로 바꾸는 과정입니다. 여기서 핵심은 단순히 글자를 숫자로 치환하는 게 아니라 #strong[의미가 비슷한 텍스트는 비슷한 숫자]가 된다는 점입니다.

#v(paragraph-gap)
"연차 사용 규정" → \[0.12, -0.34, 0.87, …\] "휴가 관련 정책" → \[0.11, -0.33, 0.85, …\] ← 비슷! "매출 현황 보고서" → \[-0.45, 0.22, -0.11, …\] ← 완전 다름

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH04/gemini/04_embedding-concept.png", alt: [임베딩은 의미가 비슷한 텍스트를 가까운 좌표에 배치한다. "연차"를 검색하면 의미상 가까운 문서들이 먼저 발견된다.], max-width: 0.6)

#v(paragraph-gap)
벡터 검색의 핵심이 바로 이것입니다. "연차 사용 규정"을 검색하면 숫자가 비슷한 "휴가 관련 정책" 청크를 찾아올 수 있습니다. 키워드가 정확히 일치하지 않아도 의미가 가까우면 찾아냅니다.

#v(paragraph-gap)
그런데 "숫자가 비슷하다"는 걸 어떻게 판단할까요? 768개나 되는 숫자를 하나하나 비교할 수는 없습니다. 여기서 #strong[코사인 유사도(Cosine Similarity)] 라는 방법을 씁니다. 벡터를 좌표 위의 #strong[화살표]라고 생각해 보겠습니다. 두 화살표가 같은 방향을 가리키면 의미가 비슷한 거고, 반대 방향이면 의미가 다른 겁니다. 코사인 유사도는 이 #strong[두 화살표 사이의 각도]를 측정합니다.

#v(paragraph-gap)
- 같은 방향(각도 0°) → 유사도 #strong[1] (완전히 같은 의미)
- 직각(90°) → 유사도 #strong[0] (관련 없음)
- 반대 방향(180°) → 유사도 #strong[\-1] (반대 의미)

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH04/gemini/04_cosine-similarity.png", alt: [코사인 유사도의 각도에 따른 값의 변화], max-width: 0.6)

#v(paragraph-gap)
"연차 사용 규정"과 "휴가 관련 정책"은 거의 같은 방향을 가리킵니다. "매출 현황 보고서"는 완전히 다른 방향입니다. 벡터 DB는 이 각도를 계산해서 가장 비슷한 방향의 문서부터 순서대로 가져옵니다.

==== 왜 ko-sroberta-multitask인가?

임베딩 모델은 여러 가지가 있습니다. OpenAI의 text-embedding-ada-002도 있고 다국어 모델도 존재합니다. 우리는 #strong[ko-sroberta-multitask]를 선택했습니다. 이유는 간단합니다.

#v(paragraph-gap)
+ #strong[한국어에 특화됐다] --- 한국어 문장 유사도 태스크로 파인튜닝된 모델입니다. "연차"와 "휴가"가 의미상 가깝다는 걸 잘 잡아냅니다.
+ #strong[로컬에서 돌릴 수 있다] --- OpenAI 임베딩은 API 호출 과정에서 과금이 발생합니다. 반면 ko-sroberta는 단일 다운로드만 마치면 로컬 환경에서 무료로 사용할 수 있습니다.
+ #strong[사내 문서에 적합하다] --- 사내 민감 정보를 외부 API에 보내지 않아도 됩니다. 보안 규정 관점에서도 안전합니다.

#quote(block: true)[CH08(검색 품질 튜닝)에서 다른 임베딩 모델과 비교 실험을 해봅니다. 지금은 ko-sroberta로 시작하고, 나중에 더 나은 선택지가 있는지 확인합니다.]

=== 1.6 ChromaDB --- 벡터 DB에 저장

양념까지 끝난 재료를 냉장고에 정리합니다. 라벨 붙이고 구분해서 나중에 바로 꺼낼 수 있게.

#v(paragraph-gap)
#strong[ChromaDB]가 우리의 냉장고입니다. CH01에서 이미 써봤지만 그때는 `Chroma.from_documents()` 명령 한 줄로 끝냈습니다. 이번에는 우리가 직접 넣습니다. ChromaDB에 저장하는 항목은 네 가지입니다.

#figure(
  align(center)[#table(
    columns: 3,
    align: (auto,auto,auto,),
    table.header([저장 항목], [내용], [예시],),
    table.hline(),
    [id], [청크 고유 ID], [`hr_취업규칙_v1_0_text_p001_c0003`],
    [document], [청크 텍스트 원문], ["제5조 연차유급휴가는…"],
    [embedding], [768차원 벡터], [\[0.12, -0.34, …\]],
    [metadata], [출처 정보], [{file\_name: "HR\_취업규칙\_v1.0.pdf", page: 3}],
  )]
  , kind: table
  )

저장할 때 #strong[upsert] 연산을 사용합니다. 같은 ID가 이미 존재하면 덮어쓰고, 없으면 새로 추가합니다. 파이프라인을 여러 번 실행해도 저장소에서 데이터가 중복되지 않습니다. CH03에서 설계한 #strong[전체 재인덱싱] 전략과 방향이 맞닿는 부분입니다.

#v(paragraph-gap)
손질(파싱) → 다지기(청킹) → 양념(임베딩) → 냉장고 정리(벡터 DB 저장). 네 단계를 알았습니다. 기술 파트에서 직접 파이프라인을 돌려보고 "연차 사용 규정"이 정말 검색되는지 확인해 보겠습니다.

#v(paragraph-gap)
이제 실습으로 문서를 벡터 DB에 저장하는 파이프라인을 만들어 보겠습니다.

== 인덱싱 파이프라인 직접 돌려보기

=== 2.1 용어 정리

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([이야기 속 표현], [진짜 용어], [정식 정의],),
    table.hline(),
    ["손질"], [파싱 (Parsing)], [파일 형식(PDF/DOCX/XLSX)에서 순수 텍스트를 추출하는 과정],
    ["다지기"], [청킹 (Chunking)], [긴 텍스트를 벡터 DB에 적합한 크기로 분할하는 과정. 고정 크기 500자 + 100자 오버랩],
    ["양념"], [임베딩 (Embedding)], [텍스트의 의미를 768차원 숫자 벡터로 변환하는 과정],
    ["냉장고"], [벡터 DB (Vector Database)], [벡터를 저장하고, 유사한 벡터를 빠르게 검색하는 특수 데이터베이스],
    ["의미가 비슷한 숫자"], [코사인 유사도 (Cosine Similarity)], [두 벡터 사이의 각도로 유사도를 측정. 1에 가까울수록 유사],
    ["덮어쓰기"], [업서트 (Upsert)], [같은 ID가 있으면 업데이트, 없으면 삽입하는 연산],
  )]
  , kind: table
  )

=== 2.2 소스 코드 준비

클론한 레포에서 이번 챕터의 폴더로 이동합니다.

```bash
cd rag-start/ex04
```

=== 2.3 실습 환경 구축

#quote(block: true)[기본 환경(Python 3.12)이 없다면 #strong[교육자료]를 먼저 확인해 주시기 바랍니다.]

```bash
cp .env.example .env
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

#figure(
  align(center)[#table(
    columns: 3,
    align: (auto,auto,auto,),
    table.header([패키지], [버전], [역할],),
    table.hline(),
    [pypdf], [4.3.1], [PDF 텍스트 추출],
    [python-docx], [1.1.2], [DOCX 단락/표 추출],
    [openpyxl], [3.1.5], [XLSX 셀 데이터 추출],
    [sentence-transformers], [3.3.1], [ko-sroberta 임베딩 모델],
    [chromadb], [1.5.1], [벡터 DB (로컬 영속)],
  )]
  , kind: table
  )

#quote(block: true)[ko-sroberta-multitask 모델은 최초 실행 시 HuggingFace에서 자동 다운로드됩니다 (약 400MB). 이후에는 로컬 캐시를 사용합니다.]

```
ex04/
├── requirements.txt
├── data/
│   ├── docs/                      ← 사내 문서 원본
│   │   ├── hr/                    (PDF 2개)
│   │   ├── security/              (DOCX 1개)
│   │   ├── finance/               (XLSX 2개)
│   │   └── ops/                   (PDF 1개)
│   ├── markdown/                  ← 파싱 결과 (실행 시 생성)
│   └── chroma_db/                 ← ChromaDB 영속 저장소 (실행 시 생성)
└── src/
    ├── chunker.py       [실습] 청킹 핵심 로직 (TODO 1개)     ◀ CH04 핵심
    ├── store.py         [실습] ChromaDB 저장+검색 (TODO 2개)
    ├── main.py          [실습] 파이프라인 조립 (TODO 5개)
    ├── cli_search.py    [실습] 벡터 검색 CLI (TODO 4개)
    ├── _chunk_utils.py  [참고] 청크 생성/메타데이터 결합
    ├── _store_utils.py  [참고] 임베딩 모델 로딩/컬렉션 관리
    ├── _pipeline_utils.py [참고] argparse/마크다운 저장
    ├── _search_utils.py [참고] 유사도 변환/출력 포맷
    ├── extractor.py     [설명] 형식별 텍스트 추출 통합 모듈
    ├── extract_pdf.py   [참고] PDF 파싱 → Markdown 변환
    ├── extract_docx.py  [참고] DOCX 파싱 → Markdown 변환
    └── extract_xlsx.py  [참고] XLSX 파싱 → Markdown 변환
```

`[실습]` 파일에는 함수 시그니처와 힌트가 준비되어 있습니다. 챕터를 따라 하며 TODO를 하나씩 채워 넣어 보겠습니다. `[참고]` 파일은 보조 함수가 완성되어 있으니 열어볼 필요 없이 import만으로 동작합니다. 막히는 부분이 있다면 rag-end의 완성 코드를 참고해 주시기 바랍니다.

=== 2.4 실습 순서

+ `chunker.py` --- 청킹 핵심 로직 작성 (다지기)
+ `store.py` --- 벡터DB 저장+검색 작성 (양념+냉장고)
+ `main.py` --- 파이프라인 조립 작성 (손질부터 저장까지 연결)
+ `cli_search.py` --- 검색 CLI 작성 (유저가 터미널에서 질문하는 도구)
+ `main.py --step 1` --- step1(손질/파싱)만 실행해서 결과 확인
+ `main.py` --- step1+step2 전체 파이프라인 실행 (파싱→청킹→임베딩→벡터DB)
+ `cli_search.py` --- 터미널에서 직접 질문을 입력해 벡터 검색 테스트

#v(paragraph-gap)
실습에 들어가기 전에 앞에서 다뤘던 4단계 파이프라인의 전체 흐름을 코드 관점에서 보겠습니다.

#v(paragraph-gap)
#emph[\[다이어그램\]]

#v(paragraph-gap)
#emph[손질(파싱) → 다지기(청킹) → 양념(임베딩) → 냉장고(ChromaDB) → 꺼내기(검색). 각 실습에서 이 파이프라인의 한 부분씩 만들어 봅니다.]

=== 2.5 실습 1: 청킹 핵심 로직 (chunker.py)

#emph[\[다이어그램\]]

#v(paragraph-gap)
#emph[파란색 영역이 실습 1 범위입니다. 파싱된 텍스트가 chunker.py로 들어가 청크 단위로 잘린 뒤 다음 단계로 넘어갑니다.]

#v(paragraph-gap)
앞에서 "다지기" 역할을 맡았던 청킹을 직접 코드로 만들어 봅니다. `ex04/src/chunker.py`를 열어 `split_text_into_chunks` TODO의 `pass`를 지우고 아래 코드를 작성합니다.

#v(paragraph-gap)
이 함수는 두 개의 매개변수를 받습니다. `chunk_size`는 한 조각의 최대 글자 수(기본값 500), `overlap`은 앞뒤 조각이 겹치는 글자 수(기본값 100)입니다. 두 값 모두 `main.py`에서 CLI 옵션(`--chunk-size`, `--overlap`)으로 넘어오는 상수이고, 실습 3에서 파이프라인을 조립할 때 확인할 수 있습니다.

```python
# chunker.py — TODO: chunk_size 단위로 텍스트를 자르되, overlap만큼 겹치게 합니다

chunks = []                          # 결과를 담을 리스트
step = chunk_size - overlap          # 다음 청크 시작 위치 (500-100=400자씩 이동)
start = 0                           # 현재 위치

while start < len(text):            # 텍스트 끝까지 반복
    end = start + chunk_size         # 현재 위치에서 500자 잘라내기
    chunk = text[start:end].strip()  # 앞뒤 공백 제거
    if chunk:                        # 빈 문자열이 아니면
        chunks.append(chunk)         # 결과에 추가
    start += step                    # 400자 뒤로 이동 (100자 겹침)

return chunks
```

`step = chunk_size - overlap`이 핵심입니다. 500 - 100 = 400자씩 이동하니까, 앞 청크의 마지막 100자가 다음 청크의 처음 100자와 겹칩니다. 1.4에서 "연차가 없다"만 남고 "리프레시 데이가 있다"가 잘려나갔던 문제를 이 겹침이 해결합니다.

#v(paragraph-gap)
각 청크에는 출처 추적용 메타데이터가 함께 붙습니다. `_chunk_utils.py`는 `[참고]` 파일로, 직접 작성하지 않아도 import만으로 동작합니다. 그 안의 `build_text_chunk` 함수가 청크 텍스트에 아래 메타데이터를 결합합니다.

#figure(
  align(center)[#table(
    columns: 3,
    align: (auto,auto,auto,),
    table.header([필드], [예시], [용도],),
    table.hline(),
    [`id`], [`hr_취업규칙_v1_0_text_p003_c0005`], [ChromaDB upsert 키],
    [`file_name`], [`HR_취업규칙_v1.0.pdf`], [출처 파일명],
    [`page`], [`3`], [출처 페이지],
    [`chunk_index`], [`5`], [문서 내 순번],
  )]
  , kind: table
  )

=== 2.6 실습 2: 벡터DB 저장+검색 (store.py)

#emph[\[다이어그램\]]

#v(paragraph-gap)
#emph[파란색 영역이 실습 2 범위입니다. 청크를 벡터로 변환해 ChromaDB에 저장하고, 질문 벡터로 유사한 청크를 검색하는 과정까지 store.py 하나에서 처리합니다.]

#v(paragraph-gap)
실습 1에서 다진 청크를 이제 양념(임베딩)해서 냉장고(ChromaDB)에 넣습니다. `ex04/src/store.py`를 열어 두 TODO의 `pass`를 지우고 아래 코드를 각각 작성합니다.

#v(paragraph-gap)
첫 번째 함수 `store_chunks_to_chroma`는 "양념 + 냉장고 정리"를 한 번에 처리합니다. 코드에 등장하는 매개변수부터 짚어보겠습니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([매개변수], [역할], [기본값],),
    table.hline(),
    [`embedding_model_name`], [임베딩에 사용할 모델 이름], [`"jhgan/ko-sroberta-multitask"` (1.5에서 선택한 한국어 특화 모델)],
    [`chroma_dir`], [ChromaDB 데이터가 저장되는 폴더 경로], [`"data/chroma_db"`],
    [`collection_name`], [ChromaDB 안에서 이 문서 세트를 묶는 이름], [`"company_docs"`],
  )]
  , kind: table
  )

세 값 모두 `main.py`에서 CLI 옵션으로 넘어오는 상수입니다. 기본값을 바꾸지 않아도 동작하지만, 나중에 다른 모델이나 컬렉션으로 실험하고 싶을 때 옵션만 바꾸면 됩니다.

#v(paragraph-gap)
코드 안에는 `[참고]` 파일에서 가져오는 보조 함수도 등장합니다. 직접 작성하지 않아도 import만으로 동작하지만 역할만 알아두겠습니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([보조 함수], [파일], [하는 일],),
    table.hline(),
    [`load_embedding_model()`], [`_store_utils.py`], [ko-sroberta 모델을 메모리에 올립니다 (최초 1회 \~400MB 다운로드)],
    [`get_or_create_collection()`], [`_store_utils.py`], [ChromaDB 컬렉션이 없으면 생성, 있으면 기존 반환 (코사인 유사도)],
    [`embed_chunks()`], [`_store_utils.py`], [청크 텍스트를 768차원 벡터로 변환하고 ChromaDB 형식에 맞게 정리],
  )]
  , kind: table
  )

코드에 `BATCH_SIZE`\(기본값 64)라는 상수가 등장합니다. 청크를 ChromaDB에 한꺼번에 넣지 않고 64개씩 묶어서 넣는 단위입니다. 메모리가 부족하면 줄이고, 여유가 있으면 늘릴 수 있습니다.

#v(paragraph-gap)
이제 코드를 작성합니다.

```python
# store.py — TODO: 위 4단계를 순서대로 구현합니다

# 1. ko-sroberta 임베딩 모델 로드 (최초 실행 시 ~400MB 다운로드, 이후 캐시)
model = load_embedding_model(embedding_model_name)

# 2. ChromaDB 클라이언트 생성 — 디스크에 영속 저장 (프로그램 종료해도 유지)
client = chromadb.PersistentClient(
    path=chroma_dir,
    settings=Settings(anonymized_telemetry=False),
)
# 컬렉션이 없으면 생성, 있으면 기존 컬렉션 반환. cosine 유사도 사용
collection = get_or_create_collection(client, collection_name)

# 3. 청크 텍스트를 768차원 벡터로 변환 + ChromaDB용 데이터 정리
ids, documents, embeddings, metadatas = embed_chunks(chunks, model)

# 4. 배치 단위로 upsert — 같은 ID가 있으면 덮어쓰기 (중복 방지)
for batch_start in range(0, len(ids), BATCH_SIZE):
    batch_end = batch_start + BATCH_SIZE
    collection.upsert(
        ids=ids[batch_start:batch_end],
        documents=documents[batch_start:batch_end],
        embeddings=embeddings[batch_start:batch_end],
        metadatas=metadatas[batch_start:batch_end],
    )

return {
    "collection_name": collection_name,
    "chroma_dir": chroma_dir,
    "total_chunks": len(chunks),
    "collection_count": collection.count(),
}
```

코드 흐름을 따라가 보겠습니다. 1번에서 1.5에서 선택한 ko-sroberta 모델을 메모리에 올립니다. 2번에서 `PersistentClient`로 ChromaDB를 디스크에 영속 저장하도록 열어줍니다. 프로그램을 종료해도 데이터가 남습니다. 3번의 `embed_chunks`가 실제 양념 작업으로, 텍스트를 768개의 숫자 벡터로 변환합니다. 4번에서 `BATCH_SIZE`개씩 묶어 `upsert`합니다. upsert는 1.6에서 나온 것처럼, 같은 ID가 있으면 덮어쓰고 없으면 새로 추가하는 연산입니다.

#v(paragraph-gap)
두 번째 함수 `search_chroma`는 반대 방향입니다. 저장할 때와 #strong[같은 모델]로 질문을 벡터로 바꾸고, ChromaDB에서 가장 가까운 청크를 찾아옵니다.

```python
# store.py — TODO: 쿼리 임베딩 → collection.query() → 결과 정리

# 1. 질문 텍스트를 벡터로 변환 (저장할 때와 같은 모델 사용)
model = load_embedding_model(embedding_model_name)
query_embedding = model.encode([query], normalize_embeddings=True).tolist()

# 2. 저장된 ChromaDB를 열고 컬렉션 가져오기
client = chromadb.PersistentClient(
    path=str(Path(chroma_dir).resolve()),
    settings=Settings(anonymized_telemetry=False),
)
collection = client.get_collection(name=collection_name)

# 3. 쿼리 벡터와 가장 가까운 청크 top_k개 검색
results = collection.query(
    query_embeddings=query_embedding,
    n_results=top_k,
    include=["documents", "distances", "metadatas"],
)

# 4. 검색 결과를 순위별 딕셔너리 리스트로 정리
search_results = []
docs = results.get("documents", [[]])[0]
dists = results.get("distances", [[]])[0]
metas = results.get("metadatas", [[]])[0]

for rank, (doc, dist, meta) in enumerate(zip(docs, dists, metas), start=1):
    search_results.append({
        "rank": rank, "text": doc,
        "distance": round(dist, 4), "metadata": meta,
    })

return search_results
```

1번에서 `model.encode([query])`로 질문 텍스트를 벡터로 변환합니다. `normalize_embeddings=True`는 벡터 길이를 1로 정규화해서 코사인 유사도 계산을 정확하게 만들어줍니다. 3번의 `collection.query()`가 ChromaDB에서 코사인 거리가 가까운 순서대로 `top_k`개를 가져옵니다. 반환되는 `distance`는 0(완전 일치)\~2(완전 반대) 범위의 코사인 거리입니다. 저장할 때와 검색할 때 #strong[같은 임베딩 모델]을 써야 한다는 점이 중요합니다. 모델이 다르면 벡터 공간 자체가 달라져서 비교가 무의미해집니다.

=== 2.7 실습 3: 파이프라인 조립 (main.py)

#emph[\[다이어그램\]]

#v(paragraph-gap)
#emph[파란색 영역이 실습 3 범위입니다. 문서 원본에서 시작해 파싱, 청킹, 임베딩, 벡터 DB 저장까지 전체 흐름을 main.py 한 파일에서 조립합니다.]

#v(paragraph-gap)
실습 1에서 `split_text_into_chunks`\(다지기)를, 실습 2에서 `store_chunks_to_chroma`\(양념+냉장고)와 `search_chroma`\(꺼내기)를 만들었습니다. 이제 이 부품들을 하나의 파이프라인으로 연결합니다. `ex04/src/main.py`를 열어 세 TODO의 `pass`를 지우고 아래 코드를 각각 작성합니다.

#v(paragraph-gap)
첫 번째 함수 `step1_python_parsing`은 "손질" 단계입니다. `[설명]` 파일인 `extractor.py`가 형식별 파서를 자동 선택해서 텍스트를 꺼냅니다. 이 함수를 별도 step으로 분리한 이유가 있습니다. `--step 1`로 파싱만 먼저 실행하면 `data/markdown/` 폴더에 마크다운 파일이 생성됩니다. 이걸 열어서 원본 문서와 대조해 보면 텍스트가 제대로 추출됐는지 #strong[눈으로 확인]할 수 있습니다. 파싱이 깨진 상태에서 청킹과 임베딩까지 돌리면 시간만 낭비하기 때문에, 손질 결과를 먼저 점검하는 단계입니다.

```python
# main.py — TODO: extract_all_from_directory()로 문서 추출 → 마크다운 저장

# 1. docs_dir(data/docs/) 안의 PDF/DOCX/XLSX를 한꺼번에 파싱
results = extract_all_from_directory(docs_dir)
# 2. 파싱 결과를 data/markdown/에 .md 파일로 저장 (눈으로 확인용)
save_results_as_markdown(results)
return results
```

두 번째 함수 `step2_embed_and_store`에서 실습 1\~2의 함수가 합류합니다. `chunk_all_documents` 안에서 실습 1의 `split_text_into_chunks`가 호출되고, 그 결과가 실습 2의 `store_chunks_to_chroma`로 들어갑니다.

```python
# main.py — TODO: chunk_all_documents()로 청킹 → store_chunks_to_chroma()로 저장

# 1. 파싱 결과를 500자+100자 오버랩으로 청킹 (실습 1에서 만든 split_text_into_chunks 호출)
all_chunks = chunk_all_documents(python_results, chunk_size, overlap)
# 2. 청크를 임베딩하여 ChromaDB에 저장 (실습 2에서 만든 store_chunks_to_chroma 호출)
store_result = store_chunks_to_chroma(
    chunks=all_chunks,
    chroma_dir=chroma_dir,
    collection_name=collection_name,
    embedding_model_name=embedding_model_name,
)
return store_result
```

`main()` 함수에도 TODO가 있습니다. 이 함수가 파이프라인의 지휘자 역할입니다. CLI 옵션 `--step`에 따라 어떤 단계를 실행할지 결정합니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr, 1fr),
    align: (auto,auto,auto,auto,),
    table.header([step], [함수], [비유], [하는 일],),
    table.hline(),
    [1], [`step1_python_parsing`], [손질(파싱)], [문서에서 텍스트 추출 → 마크다운 저장],
    [2], [`step2_embed_and_store`], [다지기+양념+냉장고], [청킹 → 임베딩 → ChromaDB 저장],
  )]
  , kind: table
  )

`--step 1`이면 파싱만, `--step 2`면 청킹+임베딩+저장만, 옵션 없이 실행하면 둘 다 순서대로 돌립니다. `pass`를 지우고 아래 코드를 작성합니다.

```python
# main.py — TODO: 1 in steps_to_run이면 step1_python_parsing 실행

if 1 in steps_to_run:
    python_results = step1_python_parsing(docs_dir=args.docs_dir)
```

```python
# main.py — TODO: 2 in steps_to_run이면 step2_embed_and_store 실행

if 2 in steps_to_run:
    # step1 결과가 없으면 자동으로 step1을 먼저 실행
    if not python_results:
        python_results = step1_python_parsing(docs_dir=args.docs_dir)
    step2_embed_and_store(
        python_results=python_results,
        chroma_dir=args.chroma_dir,
        collection_name=args.collection,
        embedding_model_name=args.embedding_model,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
    )
```

step2를 실행하면 step1 결과가 필요합니다. 아직 파싱하지 않았다면 step2가 자동으로 step1을 먼저 실행합니다. 독자가 `--step 2`만 단독으로 실행해도 에러 없이 동작하도록 만든 안전장치입니다.

#v(paragraph-gap)
TODO를 모두 채웠으면 #strong[전체를 한 번에 돌리기 전에 파싱만 먼저] 확인합니다.

```bash
# 파싱만 실행
python src/main.py --step 1
```

파싱이 끝나면 `data/markdown/` 폴더에 마크다운 파일이 생성됩니다. `data/markdown/HR_취업규칙_v1.0.md`를 열어보겠습니다.

```markdown
# HR_취업규칙_v1.0.pdf

- 파일 형식: pdf
- 추출 글자 수: 1916자

## 페이지 1

취업규칙  ( 다 단  편 집 형 )문서번호 : HR-2026-001
버전: v2.0 (Draft)
대외비  (Confidential)
4. 휴가  및  리 프 레 시  (Leave & Refresh)
4.1 스마트  휴 가  승 인  (Smart Approval)
...
```

파일 정보가 상단에 요약되어 있고 `## 페이지 1`처럼 페이지 단위로 텍스트가 잘 추출된 걸 볼 수 있습니다. #strong[파싱이 잘 됐는지 눈으로 확인하는 과정], 이 단계를 건너뛰지 않도록 주의해야 합니다.

#quote(block: true)[파싱은 RAG의 첫 단추입니다. 여기서 텍스트가 깨지면 뒤에서 아무리 고쳐도 소용이 없습니다. 생성된 `data/markdown/` 폴더 결과물을 반드시 확인하여 원문과 꼼꼼히 대조해 보시길 바랍니다.]

파싱 결과가 깨끗하면 이제 전체 파이프라인을 실행합니다.

```bash
# 전체 실행
python src/main.py

# 청크 크기를 바꿔보고 싶다면
python src/main.py --chunk-size 300 --overlap 50
```

`--chunk-size` 옵션으로 청크 크기를 바꿀 수 있습니다.

#v(paragraph-gap)
+ #strong[Step 1: 손질(파싱) + 마크다운 변환] --- `data/docs/`의 6개 문서에서 텍스트를 추출하고 마크다운으로 변환하여 `data/markdown/`에 저장합니다.
+ #strong[Step 2: 다지기 + 양념 + 저장] --- 마크다운 텍스트를 청크로 자르고 임베딩한 뒤 ChromaDB에 넣습니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH04/terminal/04_pipeline-result.png", alt: [6개 사내 문서가 마크다운으로 변환된 뒤, 18개 청크로 잘려 벡터 DB에 저장됐다.], max-width: 0.6)

=== 2.8 실습 4: 벡터 검색 CLI (cli\_search.py)

#emph[\[다이어그램\]]

#v(paragraph-gap)
#emph[파란색 영역이 실습 4 범위입니다. 사용자의 질문을 벡터로 변환해 ChromaDB에 보내고, 유사도가 높은 청크를 돌려받는 검색 흐름을 cli\_search.py에서 구현합니다.]

#v(paragraph-gap)
파이프라인을 돌렸으면 이제 #strong[검색이 작동하는지 직접 확인해 보겠습니다.] `ex04/src/cli_search.py`를 열어 두 TODO의 `pass`를 지우고 아래 코드를 각각 작성합니다. 코드에서 `search_chroma()`를 호출할 때 두 매개변수가 등장합니다. `embedding_model_name`은 저장할 때와 같은 임베딩 모델 이름(기본값 `"jhgan/ko-sroberta-multitask"`)이고, `top_k`는 검색 결과로 돌려받을 최대 청크 개수(기본값 5)입니다. 둘 다 `main()` 함수의 CLI 옵션에서 넘어옵니다.

```python
# cli_search.py — TODO: search_chroma()로 검색 실행 → 결과 출력

# 1. 앞에서 만든 search_chroma로 벡터 검색 실행
results = search_chroma(
    query=query, chroma_dir=chroma_dir,
    collection_name=collection_name,
    embedding_model_name=embedding_model_name, top_k=top_k,
)
# 2. 결과를 순위별로 터미널에 출력
for result in results:
    print_search_result(result)
```

```python
# cli_search.py — TODO: while 루프로 input() 반복 → run_single_query() 호출

# 1. 사용자 입력을 반복적으로 받음
while True:
    query = input("검색 쿼리를 입력하십시오: ").strip()
    # 2. 종료 명령이면 루프 탈출
    if query.lower() in {"quit", "exit", "q"}:
        break
    # 3. 입력된 쿼리로 검색 실행
    run_single_query(query, top_k, chroma_dir, collection_name, embedding_model_name)
```

`main()` 함수의 TODO도 채워줍니다. `--query`가 있으면 단일 쿼리, 없으면 대화형 모드로 실행합니다.

```python
# cli_search.py — TODO: 단일 쿼리 모드 — run_single_query() 호출

run_single_query(
    query=args.query, top_k=args.top_k,
    chroma_dir=args.chroma_dir,
    collection_name=args.collection,
    embedding_model_name=args.embedding_model,
)
```

```python
# cli_search.py — TODO: 대화형 반복 검색 모드 — run_interactive_mode() 호출

run_interactive_mode(
    top_k=args.top_k,
    chroma_dir=args.chroma_dir,
    collection_name=args.collection,
    embedding_model_name=args.embedding_model,
)
```

TODO를 모두 채운 뒤 실행합니다.

```bash
# 실행: 단일 쿼리
python src/cli_search.py --query "휴가 규정" --top-k 3

# 실행: 대화형 모드 (반복 검색)
python src/cli_search.py
```

검색 결과의 유사도는 어떻게 계산될까요? ChromaDB는 코사인 #strong[거리] (0\~2)를 반환합니다. 직관적이지 않으므로 #strong[유사도] (0\~100%)로 변환합니다.

```python
# cli_search.py — 유사도 변환

def format_distance_as_similarity(distance: float) -> float:
    """코사인 거리를 백분율 유사도로 변환합니다."""
    return max(0.0, (1.0 - distance / 2.0)) * 100
```

거리가 0이면 유사도 100%(완전 일치), 거리가 2로 도출되면 유사도 0%(완전 의미 반대 대척점) 상태입니다. "휴가 규정" 텍스트 키워드를 검색했을 때 출력 엔진상에서 검색 스코어가 71%가 나왔다면, 역으로 코사인 거리 환산 지표로 따졌을 때 약 0.58에 해당하는 수치라는 명확한 뜻입니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH04/terminal/04_cli-search.png", alt: ["휴가 규정"을 검색하자 취업규칙에서 글로벌 노마드, 스마트 휴가 승인 등의 관련 내용을 찾아냈다.], max-width: 0.38)

#v(paragraph-gap)
1\~3위 모두 취업규칙에서 휴가(글로벌 노마드, 스마트 휴가, 워케이션) 관련 내용을 찾아왔습니다. 모델이 문맥을 잘 파악해서 정답을 찾아낸 거예요. 다만 유사도가 71%대로 아주 높지는 않고 `--top-k 5`처럼 검색수를 늘리면 전혀 관계없는 문서가 억지로 딸려올 수도 있습니다. 벡터 DB는 키워드 매칭이 아니라 '그나마 의미가 가까운 순서'대로 k개를 무조건 채워서 가져오기 때문입니다. 검색 품질을 높이는 심화 기법은 CH08에서 집중적으로 다룹니다.

#callout-box([참고: 검색 결과는 다를 수 있습니다], [임베딩 모델의 버전이나 PC 환경 등에 따라 검색된 청크의 순서나 유사도 수치(%)는 책의 예시와 조금 다르게 나올 수 있습니다. 최상위(Top 1\~3) 검색 결과에 취업규칙의 휴가/연차 관련 내용이 잘 나왔다면 정상적으로 벡터 DB가 구축된 것입니다.])

=== 2.9 \[설명\] extractor.py --- 형식별 텍스트 추출

실습 3에서 `step1_python_parsing`을 실행하면 6개 문서가 자동으로 파싱됐습니다. PDF는 pypdf로, DOCX는 python-docx로, XLSX는 openpyxl로. 그런데 우리가 파서를 직접 고른 적이 없습니다. 누가 골라준 걸까요?

#v(paragraph-gap)
1.3의 파서 선택 다이어그램을 떠올려 보면, 파일 확장자에 따라 파서가 자동으로 갈라졌습니다. extractor.py가 바로 그 자동 분기를 담당하는 코드입니다.

```python
# extractor.py — 핵심 구조

def extract_text(file_path: str | Path) -> dict:
    """파일 형식을 자동 감지하여 텍스트를 추출하는 통합 함수."""
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()

    extractor_map = {
        ".pdf": extract_from_pdf,
        ".docx": extract_from_docx,
        ".xlsx": extract_from_xlsx,
    }

    if suffix not in extractor_map:
        raise ValueError(f"지원하지 않는 파일 형식입니다: '{suffix}'")

    return extractor_map[suffix](file_path)
```

`extractor_map` 딕셔너리가 확장자와 파서 함수를 연결하는 매핑 테이블입니다. `.pdf`가 들어오면 `extract_from_pdf`를, `.docx`면 `extract_from_docx`를 호출합니다. 나중에 새 형식을 지원하고 싶으면 이 딕셔너리에 한 줄만 추가하면 됩니다.

#v(paragraph-gap)
PDF 파서를 예로 보겠습니다. 예제 문서 중 `HR_취업규칙_v1.0.pdf`를 떠올려 보면, 사람 눈에는 "제1조 목적" 같은 글자가 보이지만 파일 안에는 바이너리 데이터만 들어 있습니다. pypdf 라이브러리가 이 바이너리에서 텍스트를 페이지별로 꺼내줍니다.

```python
# extractor.py — PDF 파서

def extract_from_pdf(file_path: str | Path) -> dict:
    """PDF 파일에서 텍스트를 페이지별로 추출합니다."""
    file_path = Path(file_path)

    pages_data = []
    with open(file_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""
            pages_data.append({"page": page_num, "text": page_text.strip()})

    full_text = "\n\n".join(p["text"] for p in pages_data if p["text"])
    return {
        "source_path": str(file_path.resolve()),
        "file_name": file_path.name,
        "file_type": "pdf",
        "pages": pages_data,
        "full_text": full_text,
    }
```

`pypdf.PdfReader`로 PDF를 열고, 페이지를 하나씩 돌면서 `page.extract_text()`로 텍스트를 꺼냅니다. 여기서 주의할 부분이 `or ""`입니다. 예제 파일 중 `HR_정보보안서약서.pdf`는 스캔한 이미지로만 구성된 PDF입니다. 이런 파일은 텍스트 레이어가 아예 없어서 `extract_text()`가 `None`을 반환합니다. `or ""`가 없으면 바로 다음의 `.strip()`에서 `None.strip()` 에러가 나기 때문에, `None` 대신 빈 문자열로 바꿔주는 안전장치입니다. 실제로 이 파일은 파싱해도 텍스트 청크가 0개로 나옵니다.

#v(paragraph-gap)
이미지 기반 PDF를 읽으려면 OCR이나 Vision LLM이 필요합니다. 이 문제는 CH10에서 해결합니다. 지금은 텍스트 기반 PDF만 파싱된다는 한계만 알고 넘어갑니다.

#v(paragraph-gap)
형식별 파서 함수는 각각 다른 라이브러리를 사용하지만 모두 같은 구조의 딕셔너리를 반환합니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr, 1fr),
    align: (auto,auto,auto,auto,),
    table.header([함수], [라이브러리], [핵심 동작], [주의점],),
    table.hline(),
    [`extract_from_pdf()`], [pypdf], [페이지별 `extract_text()` 호출], [이미지 기반 PDF는 빈 문자열 반환 (CH10에서 해결)],
    [`extract_from_docx()`], [python-docx], [단락 순회 + Heading → 마크다운 헤더 변환], [페이지 개념 없음 (전체가 1페이지)],
    [`extract_from_xlsx()`], [openpyxl], [시트별 행 단위 읽기 → 마크다운 표 변환], [첫 행을 헤더로 사용],
  )]
  , kind: table
  )

#strong[응답 반환 구조] --- 세 파서 모두 같은 형태입니다:

```python
{
    "source_path": "절대 경로",
    "file_name": "파일명",
    "file_type": "pdf | docx | xlsx",
    "pages": [{"page": 번호, "text": "텍스트"}, ...],
    "full_text": "전체 텍스트"
}
```

=== 2.10 더 알아보기

#strong[왜 마크다운으로 변환하나요?] --- 임베딩 모델은 훈련 데이터에 마크다운이 대량 포함되어 있어서 `# 제목`, `| 표 |`, `- 목록` 같은 구조를 잘 이해합니다. PDF 바이너리를 그대로 넣는 것보다 마크다운으로 변환한 텍스트가 검색 품질이 좋습니다. `extract_pdf.py`, `extract_docx.py`, `extract_xlsx.py`를 개별 실행하면 파일 하나씩 변환 결과를 확인할 수 있습니다.

#v(paragraph-gap)
#strong[배치 크기 튜닝] --- `BATCH_SIZE = 64`가 기본값입니다. 메모리가 부족하면 줄이고, 여유가 있으면 늘릴 수 있습니다. ko-sroberta는 CPU에서도 동작하지만 GPU가 있으면 더 빠릅니다.

=== 2.11 이것만은 기억하세요

- #strong[문서는 조각내야 찾습니다.] 손질(파싱) → 다지기(청킹) → 양념(임베딩) → 냉장고 정리(벡터 DB). 이 네 단계가 RAG의 기초 체력입니다.
- #strong[임베딩은 "의미를 숫자로 바꾸는 것"입니다.] 키워드가 달라도 의미가 비슷하면 좌표 상에서 가까운 벡터가 됩니다.
- 다음 챕터에서는 이 벡터 DB를 활용해서 #strong[진짜 질문-답변 엔진(RAG Q&A)] 을 만듭니다. "연차 몇 일이야?"라고 물으면 검색한 문서를 근거로 LLM이 자연어로 답변해주는 시스템입니다.

= Ch.5: LCEL 파이프라인 (ex05)

#quote(block: true)[한 줄 요약: 검색은 재료, 답변은 요리다. LCEL 파이프라인이 이 레시피다. \
핵심 개념: LCEL 파이프라인, 출처 강제(Source Grounding), WindowMemory 멀티턴]

== 검색에서 답변까지, 사서가 완성되다

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH05/gemini/05_chapter-opening.png", alt: [저장된 지식을 바탕으로 AI가 드디어 사내 질문에 답합니다], max-width: 0.7)

#v(paragraph-gap)
지난 챕터에서 사내 문서를 벡터 DB에 저장하고 CLI로 검색까지 해봤습니다. "연차 사용 규정"을 검색하면 관련 문서 조각이 유사도 점수와 함께 나왔습니다. 그런데 문제가 생겼습니다.

=== 1.1 "그냥 답을 알려줘"

벡터 검색을 사내 시스템에 붙이고 일주일쯤 지났을 때였습니다.

#v(paragraph-gap)
#strong[동료]: "야, 병가 쓸 때 증빙 서류 필요해?" \
"연차 몇 일 남았는지 어떻게 확인해?" \
"신규 서비스 런칭 전략 문서 어디 있어?"

#v(paragraph-gap)
동료들의 질문이 하루에 서너 번씩 날아왔습니다. 매번 같은 유형입니다. 답은 전부 사내 문서 어딘가에 있는데 말입니다.

#v(paragraph-gap)
처음엔 벡터 검색 결과를 공유해 보았습니다.

```
[1] HR_취업규칙_v1.0 (p.3) — 유사도: 87.2%
    "제15조(병가) 질병이나 부상으로 인하여 직무를 수행할 수 없을 때에는..."

[2] HR_취업규칙_v1.0 (p.4) — 유사도: 81.5%
    "병가 기간이 3일 이상인 경우에는 의사의 진단서를..."
```

돌아오는 반응은 한결같았습니다.

#v(paragraph-gap)
#strong[동료]: "이걸 내가 읽어?" \
"그냥 답을 알려줘."

#v(paragraph-gap)
#emph[맞습니다. 사람들은 문서 조각을 원하는 게 아니라, #strong[답변]을 원합니다.]

#v(paragraph-gap)
검색 결과 5개를 받아서 직접 읽고 "아, 3일 미만이면 증빙 불필요고 3일 이상이면 진단서가 필요하구나"라고 해석하는 건 결국 사람 몫이었습니다. 벡터 검색은 #strong[재료를 찾아주는 것]이지 #strong[요리를 해주는 것]이 아니었습니다.

#v(paragraph-gap)
이번 챕터에서는 그 "요리"를 해줄 #strong[RAG Q&A 엔진]을 만들어 보겠습니다. 질문하면 문서를 검색하고 검색 결과를 읽어서 자연어로 답변해 주는 시스템입니다.

=== 1.2 검색에서 답변으로

지금까지 만든 벡터 검색은 #strong[도서관의 검색 시스템]과 비슷합니다. "한국 역사"를 검색하면 관련 책이 어디 있는지 알려줍니다. 하지만 그 책을 직접 꺼내서 읽어보고 핵심을 정리해서 답해주지는 않습니다.

#v(paragraph-gap)
우리에게 필요한 건 #strong[AI 비서]입니다. AI 비서에게 "조선시대 과거 제도가 뭐야?"라고 물으면 이런 일이 벌어집니다.

#v(paragraph-gap)
+ #strong[질문을 듣는다] --- "조선 과거 제도"가 핵심이군
+ #strong[서가에서 책을 찾는다] --- 한국사 개론 3장 부근을 꺼냄
+ #strong[읽고 답변을 정리한다] --- "문과·무과·잡과 세 종류가 있었습니다"
+ #strong[출처를 알려준다] --- "한국사 개론 3장에 나와 있어요"

#v(paragraph-gap)
이 네 단계가 바로 RAG Q&A 파이프라인입니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH05/diagram/05_rag-qa-flow.png", alt: [RAG Q&A 흐름 --- 질문이 들어오면 벡터 검색으로 문서 조각을 찾고, LLM이 읽어서 자연어 답변을 만듭니다], max-width: 0.6)

벡터 검색(CH04)은 2번까지였습니다. 이번 챕터에서 3번과 4번을 추가합니다. AI 비서가 문서를 찾는 것뿐 아니라 #strong[읽고 답변까지 해주는] 시스템을 만드는 것입니다.

=== 1.3 LCEL --- 파이프 연산자로 조립하기

AI 비서가 일하는 순서를 코드로 옮기려면 어떻게 해야 할까요? 검색 → 프롬프트 → LLM → 파싱, 각 단계를 직접 이어 붙여도 되지만 이걸 편하게 해주는 도구가 있습니다. #strong[LangChain]은 검색, 프롬프트, LLM 호출 같은 단계를 부품으로 제공하고 이 부품을 조립할 수 있게 해주는 Python 프레임워크입니다. RAG 시스템을 만들 때 가장 널리 쓰입니다. LangChain은 이 조립을 #strong[파이프(|) 연산자]로 합니다. LCEL(LangChain Expression Language)이라고 부릅니다. 파이프는 주방의 레시피와 같습니다.

#quote(block: true)[질문 → #strong[검색]\(벡터 DB에서 문서 조각 찾기) → #strong[프롬프트]\(찾은 문서 + 질문을 합치기) → #strong[LLM]\(읽고 답변 생성) → #strong[파싱]\(답변 텍스트 추출)]

각 단계가 파이프(|)로 연결되고, 앞 단계의 출력이 다음 단계의 입력이 됩니다. 요리 레시피 순서와 똑같습니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH05/diagram/05_lcel-pipeline.png", alt: [LCEL 파이프라인 구조 --- 각 단계가 파이프 연산자로 연결됩니다], max-width: 0.6)

이 구조의 장점은 #strong[블록을 바꿀 수 있다]는 것입니다. LLM을 DeepSeek에서 GPT-4o로 바꾸고 싶으면? LLM 블록만 교체하면 됩니다. 검색 방식을 바꾸고 싶으면? 검색 블록만 교체하면 됩니다.

=== 1.4 Source Grounding --- 출처 강제

AI 비서에게 한 가지 더 요구할 게 있습니다. #strong[출처]입니다.

#v(paragraph-gap)
CH01에서 LLM이 그럴듯하게 거짓말하는 걸 봤습니다. RAG로 문서를 넣어줬다고 환각이 완전히 사라지는 것은 아닙니다. LLM은 문서에 없는 내용을 지어내기도 합니다. CH01의 step3에서 프롬프트에 "참고 정보를 바탕으로 답하세요"라는 제약을 넣었던 것을 기억하시나요? 이번에는 더 엄격하게 규칙을 넣습니다.

#quote(block: true)["반드시 제공된 문서에서만 답하세요. 답변 마지막에 출처를 명시하세요. 문서에서 찾을 수 없으면 '확인되지 않습니다'라고 답하세요."]

이걸 #strong[출처 강제(Source Grounding)] 라고 부릅니다. LLM에게 "근거 없이 답하지 마"라고 제한을 거는 것입니다. 출처가 붙으면 독자가 직접 확인할 수도 있고, 신뢰도가 훨씬 올라갑니다.

=== 1.5 WindowMemory --- 멀티턴 대화

도서관에서 사서에게 묻습니다.

#v(paragraph-gap)
#strong[방문자]: "한국 역사 관련 책 어디 있어요?"

#v(paragraph-gap)
#strong[사서]: "2층 인문학 서가에 있습니다. '한국사 편지'가 가장 인기 있어요."

#v(paragraph-gap)
바로 이어서 묻습니다.

#v(paragraph-gap)
#strong[방문자]: "그러면 거기에 세계사 책도 있어?"

#v(paragraph-gap)
여기서 "거기"가 가리키는 건 무엇일까요? #strong[2층 인문학 서가]입니다. 이전 대화를 기억하고 있어야 "거기 = 2층 인문학 서가"라는 맥락을 이해할 수 있습니다.

#v(paragraph-gap)
사람이라면 당연히 기억합니다. 하지만 LLM은 기본적으로 #strong[기억력이 없습니다]. 매 요청이 독립적이라 이전에 뭘 물어봤는지 모릅니다. 그래서 #strong[대화 히스토리]를 직접 관리해야 합니다. 이전 대화를 메모해뒀다가 새 질문이 올 때마다 같이 넘겨주는 것입니다. 다만 모든 대화를 다 기억할 수는 없으니 #strong[최근 5턴만 유지]하는 슬라이딩 윈도우 방식을 씁니다.

#v(paragraph-gap)
AI 비서가 메모장을 들고 있다고 생각하면 됩니다. 새 메모가 들어오면 가장 오래된 메모를 지우고 항상 최근 5장만 남깁니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH05/gemini/05_sliding-window.png", alt: [메모장에 6번째 메모가 들어오면 가장 오래된 1번째가 빠진다. 항상 최근 5장만 유지.], max-width: 0.6)

=== 1.6 이번 버전에서 뭘 만드나

ex05에서는 네 가지를 추가합니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([기능], [비유], [코드],),
    table.hline(),
    [LCEL 파이프라인], [AI 비서의 업무 순서 (검색→읽기→답변)], [`rag_chain.py`],
    [출처 강제 프롬프트], ["근거 문서를 대"], [`RAG_SYSTEM_PROMPT`],
    [멀티턴 대화], [최근 5장짜리 메모장], [`conversation.py`],
    [채팅 웹 UI], [창구 --- 질문을 입력하면 답변이 나오는 화면], [`chat.html`, `chat.js`],
  )]
  , kind: table
  )

FastAPI 서버에 채팅 UI까지 붙입니다. 브라우저에서 바로 질문하실 수 있습니다. ex04에서 재료를 다 모았습니다. 이번 챕터(ex05)에서 직접 #strong[요리]해 보겠습니다. 검색만 하던 시스템이 답변을 해 줄 것입니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH05/gemini/05_rag-qa-result.png", alt: [문서를 검색하고, 읽어서, 출처와 함께 자연어로 답변합니다.], max-width: 0.6)

#v(paragraph-gap)
이제 실습으로 검색 결과를 답변으로 바꾸는 체인을 만들어 보겠습니다.

== LCEL 파이프라인과 멀티턴 대화 구현하기

=== 2.1 용어 정리

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([이야기 속 표현], [진짜 이름], [정의],),
    table.hline(),
    [부품 + 조립 도구], [#strong[LangChain]], [LLM 애플리케이션에 필요한 부품(Retriever, Prompt, LLM, Parser)을 제공하고 파이프라인으로 조립할 수 있게 해주는 Python 프레임워크],
    [AI 비서의 업무 순서], [#strong[LCEL 파이프라인]], [LangChain Expression Language. 파이프 연산자(`\|`)로 Retriever → Prompt → LLM → Parser를 연결하는 체인 조립 방식],
    [근거를 대], [#strong[출처 강제(Source Grounding)]], [프롬프트에 "제공된 문서에서만 답하고 출처를 명시하라"는 제약을 거는 기법. 환각을 줄이고 답변 신뢰도를 높인다],
    [5장짜리 메모장], [#strong[WindowMemory]], [최근 N턴의 대화만 유지하는 슬라이딩 윈도우 방식의 대화 히스토리 관리. `deque(maxlen=k)` 기반],
    [파이프(`\|`)], [#strong[LCEL 파이프 연산자]], [`A \| B`는 A의 출력을 B의 입력으로 전달. Unix 파이프(`cat file \| grep`)와 같은 개념],
    [메모장 관리인], [#strong[ConversationManager]], [세션별로 WindowMemory를 관리하고, TTL 기반으로 만료된 세션을 정리하는 클래스],
  )]
  , kind: table
  )

=== 2.2 소스 코드 준비

클론한 레포에서 이번 챕터의 폴더로 이동합니다.

```bash
cd rag-start/ex05
```

=== 2.3 실습 환경 구축

#quote(block: true)[기본 환경(Python 3.12, Ollama)이 없다면 #strong[교육자료]를 먼저 확인해 주시기 바랍니다.]

CH01에서 썼던 `RetrievalQA`는 LangChain이 만들어둔 완성품이라 간편하지만, 응답 파싱이나 대화 메모리를 끼워 넣을 수가 없었습니다. 이번 챕터에서는 LCEL 파이프라인으로 바꿔서 검색, 프롬프트, LLM, 파서 각 단계를 직접 조립합니다.

```bash
cp .env.example .env
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
ollama pull deepseek-r1:8b
pip install -r requirements.txt
```

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([패키지], [버전], [역할],),
    table.hline(),
    [`langchain`], [0.3.21], [체인 조립 프레임워크],
    [`langchain-community`], [0.3.20], [HuggingFaceEmbeddings 등 커뮤니티 통합],
    [`langchain-ollama`], [0.2.3], [Ollama LLM 연결],
    [`langchain-openai`], [0.3.7], [OpenAI LLM 연결 (선택)],
    [`langchain-chroma`], [0.2.6], [ChromaDB Retriever 래퍼],
    [`fastapi`], [0.115.8], [웹 API 서버],
    [`uvicorn`], [0.34.0], [ASGI 서버],
  )]
  , kind: table
  )

`.env` 핵심 설정입니다. 코드를 보기 전에 각 상수의 역할부터 파악해 두면 흐름이 잘 읽힙니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([상수], [기본값], [역할],),
    table.hline(),
    [`LLM_PROVIDER`], [`ollama`], [사용할 LLM 제공자 (`ollama` 또는 `openai`)],
    [`OLLAMA_MODEL`], [`deepseek-r1:8b`], [Ollama에서 사용할 모델 이름],
    [`EMBEDDING_MODEL`], [`jhgan/ko-sroberta-multitask`], [문서 임베딩(벡터화)에 사용할 모델],
    [`RETRIEVER_TOP_K`], [`5`], [질문당 검색해서 가져올 관련 문서 조각 개수],
    [`CONVERSATION_WINDOW_SIZE`], [`5`], [LLM 프롬프트에 포함할 최근 대화 유지 턴(Turn) 수],
  )]
  , kind: table
  )

```shell
# 사용할 LLM 제공자 (ollama 또는 openai)
LLM_PROVIDER=ollama
# Ollama에서 사용할 모델 이름
OLLAMA_MODEL=deepseek-r1:8b
# 문서 임베딩(벡터화)에 사용할 모델
EMBEDDING_MODEL=jhgan/ko-sroberta-multitask
# ChromaDB 데이터가 저장될 로컬 영구 저장소 경로
CHROMA_PERSIST_DIR=./data/chroma_db
# 질문당 검색해서 가져올 관련 문서 조각 개수
RETRIEVER_TOP_K=5
# LLM 프롬프트에 포함할 최근 대화 유지 턴(Turn) 수
CONVERSATION_WINDOW_SIZE=5
```

#callout-box([팁: LLM 선택], [기본값은 Ollama + `deepseek-r1:8b`입니다. 이후 챕터 부터는`.env`에서 `LLM_PROVIDER=openai`로 바꾸면 GPT-4o-mini도 쓸 수 있습니다. (단, API 비용이 발생합니다. .env 파일에 OPENAI\_API\_KEY=sk-xxxxxx 형태로 key를 등록해서 사용하십시오.)])

```
ex05/
├── run.py                  [참고] 서버 플로우 실행
├── .env                    [참고] 환경 변수
├── README.md               [참고] 프로젝트 설명서
├── requirements.txt        [참고] 의존성 목록
├── data/                   
│   ├── docs/               [참고] 원본 PDF/Word 문서 저장소
│   ├── markdown/           [참고] 마크다운 변환 문서 저장소
│   └── chroma_db/          [참고] 생성된 벡터 DB 영구 저장소
├── src/
│   ├── rag_chain.py        [실습] LCEL 파이프라인 + 출처 강제 프롬프트
│   ├── conversation.py     [실습] WindowMemory(k=5) 멀티턴 대화
│   ├── llm_factory.py      [참고] LLM 인스턴스 생성 (Ollama/OpenAI 분기)
│   ├── vectorstore.py      [참고] ChromaDB Retriever 생성 + 문서 파싱/청킹
│   ├── session_manager.py  [참고] 세션별 ConversationManager + RAG 체인 싱글턴 관리
│   └── response_parser.py  [설명] DeepSeek <think> 제거 + 출처 추출
├── templates/
│   ├── base.html           [참고] 공통 레이아웃
│   └── chat.html           [참고] 채팅 UI 페이지
├── static/
│   ├── css/chat.css        [참고] 채팅 UI 스타일
│   └── js/chat.js          [참고] 질문 전송 + 답변 렌더링
└── app/
    ├── main.py             [참고] FastAPI 앱 진입점 + UI 라우팅
    ├── chat_api.py         [설명] POST /api/chat 엔드포인트
    └── session.py          [참고] 세션 쿠키 관리
```

`[실습]` 파일에는 import와 데이터가 미리 준비되어 있습니다. 챕터를 따라 하며 TODO 부분을 하나씩 채워 넣어 보겠습니다. 막히는 부분이 있다면 rag-end의 완성 코드를 참고해 주시기 바랍니다.

=== 2.4 실습 순서

+ `rag_chain.py` --- RAG 파이프라인 구축
+ `conversation.py` --- 멀티턴 대화 메모리
+ `chat_api.py` --- API 엔드포인트 확인
+ `python run.py` --- 서버 실행 + 웹 UI 테스트

#v(paragraph-gap)
핵심 코드를 먼저 작성하고 마지막에 서버를 띄워 채팅 UI에서 챗봇과 대화해 보겠습니다. 실습에 들어가기 전에 질문이 들어온 뒤 답변이 나가기까지의 전체 흐름을 먼저 보겠습니다.

#v(paragraph-gap)
#emph[\[다이어그램\]]

#v(paragraph-gap)
#emph[질문이 `/api/chat`으로 들어오면 AI 비서가 메모장(대화 히스토리)을 확인하고, 서가(벡터 DB)에서 관련 문서를 검색한 뒤, 출처와 함께 답변을 돌려줍니다. 이번 실습에서 이 흐름을 하나씩 만들어 봅니다.]

#v(paragraph-gap)
질문이 `/api/chat`으로 들어온 뒤 답변이 나가기까지 전체 흐름을 담당하는 라우터부터 살펴보겠습니다.

=== 2.5 \[설명\] chat\_api.py --- POST /api/chat

이 라우터 코드는 `ex05/app/chat_api.py` 파일에 있습니다. AI 비서에게 질문을 전달하는 창구 역할입니다. 웹 브라우저나 API 클라이언트가 여기로 질문을 보냅니다.

```python
# chat_api.py — prefix="/api"로 실제 URL은 /api/chat

router = APIRouter(prefix="/api", tags=["chat"])

@router.post("/chat")
async def chat_endpoint(body: ChatRequest, request: Request):
    # 세션 ID: 요청 본문 > 쿠키 > 신규 생성 순으로 결정
    session_id = body.session_id or get_session_id(request)

    # 대화 매니저에서 이전 대화 히스토리 조회
    conv_manager = get_conversation_manager()
    history_text = conv_manager.get_history_text(session_id)

    # RAG 체인과 Retriever 로드
    chain, retriever = get_rag_chain()

    # Retriever로 관련 문서 검색 (출처 표시에 사용)
    docs = retriever.invoke(question)

    # LCEL 체인 실행: {"question": ..., "history": ...} 형식으로 입력
    # 체인 내부에서 question → 검색 → 포맷 → 프롬프트 → LLM 순서로 처리
    raw_answer = chain.invoke(
        {
            "question": question,   # ① 검색 및 프롬프트에 사용
            "history": history_text,  # ② 이전 대화 맥락 주입
        }
    )

    # 응답 구조 생성 (answer 정제 + sources 추출)
    response_data = build_response(raw_answer=raw_answer, docs=docs)

    # 세션 히스토리에 이번 대화 저장
    conv_manager.save_turn(
        session_id=session_id,
        question=question,
        answer=response_data["answer"],
    )
```

전체 흐름이 한눈에 들어옵니다. 세션 확인 → 히스토리 조회 → 문서 검색 → 체인 실행 → 응답 정제 → 히스토리 저장. AI 비서가 질문을 받고 → 메모장 확인하고 → 서가에서 문서 꺼내고 → 읽고 답변하고 → 메모장에 기록하는 과정과 같습니다.

=== 2.6 실습 1: LCEL 파이프라인 (rag\_chain.py)

#emph[\[다이어그램\]]

#v(paragraph-gap)
#emph[파란색이 실습 1에서 만드는 부분입니다. 검색 → 맥락 조립 → 답변 생성 파이프라인을 LCEL로 만듭니다.]

#v(paragraph-gap)
앞에서 AI 비서의 업무 순서를 말씀드렸습니다. 질문 받기 → 문서 찾기 → 읽고 답변하기. 이 순서를 코드로 옮기는 것이 실습 1입니다. `chat_api.py`의 3\~5단계에서 호출되는 핵심 파이프라인이에요. `ex05/src/rag_chain.py`를 열어 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

#v(paragraph-gap)
파일 상단에 import와 프롬프트 템플릿(`RAG_SYSTEM_PROMPT`, `RAG_HUMAN_PROMPT`)은 이미 준비되어 있습니다. 프롬프트에는 세 가지 제약이 들어 있습니다. "제공된 문서에서만 답하라", "출처를 명시하라", "모르면 모른다고 하라". 1.4에서 다룬 출처 강제(Source Grounding)가 바로 이것입니다.

```python
# rag_chain.py — TODO: 검색된 Document를 "[문서 N] 출처: ..." 텍스트로 변환

# 1. 검색된 Document 리스트를 프롬프트에 넣을 텍스트로 변환
parts = []
for i, doc in enumerate(docs, start=1):
    source = doc.metadata.get("source", "알 수 없음")
    page = doc.metadata.get("page", "-")
    parts.append(f"[문서 {i}] 출처: {source} (p.{page})\n{doc.page_content}")
return "\n\n".join(parts)
```

```python
# rag_chain.py — TODO: build_llm()으로 LLM 생성 ~ (chain, retriever) 튜플 반환

# 1. LLM 인스턴스 생성 (llm_factory.py에서 Ollama/OpenAI 선택)
llm = build_llm()
# 2. ChromaDB에서 문서를 검색하는 Retriever 생성
retriever = build_retriever()

# 3. 시스템 프롬프트 + 사용자 프롬프트 조립
prompt = ChatPromptTemplate.from_messages([
    ("system", RAG_SYSTEM_PROMPT),
    ("human", RAG_HUMAN_PROMPT),
])

# 4. LCEL 파이프로 체인 조립 — 질문→검색→포맷→프롬프트→LLM→텍스트 추출
chain = (
    {
        "context": itemgetter("question") | retriever | _format_docs,
        "history": itemgetter("history"),
        "question": itemgetter("question"),
    }
    | prompt
    | llm
    | StrOutputParser()
)

# 5. 체인과 검색기를 함께 반환
return chain, retriever
```

`chain` 변수 하나에 AI 비서의 업무 순서가 통째로 들어 있습니다. 흐름을 따라가 보겠습니다.

#v(paragraph-gap)
- `itemgetter("question") | retriever | _format_docs` --- 질문 텍스트를 꺼내서 벡터 DB를 검색하고, 찾은 문서를 `[문서 1] 출처: ... / 내용...` 텍스트로 포맷합니다. 실습 1의 첫 번째 코드블록에서 만든 `_format_docs`가 여기서 호출됩니다.
- `| prompt | llm | StrOutputParser()` --- 포맷된 문서 + 대화 히스토리 + 질문을 프롬프트로 조립하고, LLM을 호출한 뒤, 응답에서 텍스트만 뽑아냅니다.

#v(paragraph-gap)
CH01에서 `RetrievalQA.from_chain_type()` 한 줄로 끝냈던 걸 이번에는 파이프 연산자로 직접 조립한 것입니다. 블랙박스가 아니라 각 단계가 눈에 보이니까, 나중에 검색 방식을 바꾸거나 프롬프트를 수정할 때 해당 블록만 교체하면 됩니다.

#v(paragraph-gap)
`build_llm()` 함수는 `llm_factory.py`에 분리되어 있습니다. `.env`의 `LLM_PROVIDER` 값에 따라 Ollama 또는 OpenAI를 선택합니다. `temperature=0.1`로 낮춘 건 의도적입니다. Q&A 비서는 창의적인 답변이 아니라 #strong[정확한 답변]이 필요하기 때문입니다.

#v(paragraph-gap)
`rag_chain.py`에서 import하는 인프라 함수들은 직접 작성하지 않는 `[참고]` 파일에 있습니다. 역할만 파악해 두면 됩니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([파일], [함수], [역할],),
    table.hline(),
    [`llm_factory.py`], [`build_llm()`], [`.env` 설정에 따라 Ollama/OpenAI LLM 인스턴스 생성],
    [`vectorstore.py`], [`build_retriever()`], [ChromaDB Retriever 생성 (DB 없으면 CH04 로직으로 자동 구축)],
    [`vectorstore.py`], [`_parse_and_chunk_docs()`], [PDF/DOCX/XLSX 파싱 → 청킹 (CH04에서 만든 extractor·chunker 재사용)],
  )]
  , kind: table
  )

=== 2.7 \[설명\] response\_parser.py --- 답변 정제

#emph[\[다이어그램\]]

#v(paragraph-gap)
#emph[파란색이 이번 섹션에서 설명하는 부분입니다. LLM 원문에서 추론 태그를 제거하고 출처를 추출합니다.]

#v(paragraph-gap)
CH01에서 `RetrievalQA`를 쓸 때는 이런 고민이 없었습니다. 검색부터 답변 생성까지 내부에서 알아서 처리해 줬으니까요. 하지만 LCEL로 파이프라인을 직접 조립하면 LLM이 내놓는 원문 응답을 우리가 직접 다루게 됩니다. 문제는 이 원문이 깔끔하지 않다는 점입니다.

#v(paragraph-gap)
특히 DeepSeek R1 모델은 답변 앞에 `<think>...</think>` 태그로 자기 추론 과정을 덧붙여서 내보냅니다. 사용자에게 보여줄 답변에 LLM의 속마음이 섞여 있으면 곤란하겠죠? `ex05/src/response_parser.py`가 이 정리를 맡습니다. 추론 태그를 걷어내고, 출처 정보를 뽑아서 깔끔한 응답 구조로 만들어 줍니다.

```python
# response_parser.py — LLM 원문에서 <think> 태그 제거 + 빈 응답 처리

def parse_answer_text(raw_answer):
    """LLM 원문 응답에서 <think>...</think> 태그를 제거하고 답변 텍스트만 반환한다."""
    text = raw_answer
    # DeepSeek R1의 <think> 추론 토큰 제거
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = text.strip()

    # 빈 문자열이면 기본 메시지 반환
    if not text:
        text = "답변을 생성하지 못했습니다. 다시 시도해 주세요."
    return text
```

`re.sub`으로 `<think>...</think>` 태그를 통째로 지웁니다. `re.DOTALL` 플래그가 있어야 태그 안에 줄바꿈이 있어도 매칭됩니다. LLM의 추론 과정은 사용자에게 보여줄 필요가 없으니까요. 정제 후 빈 문자열이면 기본 메시지를 반환해서 빈 응답을 방지합니다.

```
LLM 원문:  <think>연차 규정을 찾아보자...</think> 신입사원은 3년간 연차가 없습니다.
정제 후:   신입사원은 3년간 연차가 없습니다.
```

`build_response()` 함수는 정제된 답변과 출처를 하나의 딕셔너리로 묶습니다.

```python
# response_parser.py — 정제된 답변 + 출처를 하나의 응답으로 조립

def build_response(raw_answer, docs):
    """LLM 원문 응답과 검색 문서로부터 최종 API 응답 딕셔너리를 구성한다."""
    answer = parse_answer_text(raw_answer)
    sources = parse_sources_from_docs(docs)
    return {"answer": answer, "sources": sources}
```

API 응답 형태는 이렇습니다.

```json
{
  "answer": "3일 미만 병가는 증빙이 불필요하고, 3일 이상은 의사 진단서가 필요합니다.",
  "sources": [
    {"doc": "HR_취업규칙_v1.0", "page": 3, "snippet": "제15조(병가) 질병이나..."}
  ]
}
```

=== 2.8 실습 2: 멀티턴 대화 (conversation.py)

#emph[\[다이어그램\]]

#v(paragraph-gap)
#emph[파란색이 실습 2에서 만드는 부분입니다. 이전 대화를 기억하고 기록하는 메모장을 만듭니다.]

#v(paragraph-gap)
1.5에서 "5장짜리 메모장"이라고 표현했던 바로 그 메모장을 코드로 만듭니다. "그러면"이 무엇을 가리키는지 AI가 알려면 이전 대화를 기억해야 합니다. `WindowMemory` 클래스가 이 역할을 맡습니다. `ex05/src/conversation.py`를 열어 세 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

#v(paragraph-gap)
코드에 등장하는 매개변수부터 짚어보겠습니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([매개변수], [기본값], [역할],),
    table.hline(),
    [`k`], [`5`], [유지할 최근 대화 턴 수. `.env`의 `CONVERSATION_WINDOW_SIZE`에서 넘어옴],
    [`human_prefix`], [`"사용자"`], [히스토리에서 사용자 발화를 표시하는 접두어],
    [`ai_prefix`], [`"AI 비서"`], [히스토리에서 AI 발화를 표시하는 접두어],
  )]
  , kind: table
  )

```python
# conversation.py — TODO: self._turns의 (question, answer) 쌍을 순회하며
#                         "human_prefix: question\nai_prefix: answer" 형식으로 조합

class WindowMemory:
    def __init__(self, k=5, human_prefix="사용자", ai_prefix="AI 비서"):
        self.k = k
        self.human_prefix = human_prefix
        self.ai_prefix = ai_prefix
        self._turns = deque(maxlen=k)  # 최근 k턴만 유지, 넘치면 오래된 것부터 삭제

    def get_history(self):
        # TODO: self._turns의 (question, answer) 쌍을 순회하며
        # 1. 저장된 대화를 "사용자: 질문 / AI: 답변" 텍스트로 변환
        lines = []
        for question, answer in self._turns:
            lines.append(f"{self.human_prefix}: {question}")
            lines.append(f"{self.ai_prefix}: {answer}")
        return "\n".join(lines)

    def save_turn(self, question, answer):
        # TODO: (question, answer) 튜플을 self._turns에 추가
        # 1. 질문-답변 1턴을 메모장에 저장
        self._turns.append((question, answer))

    def clear(self):
        # TODO: self._turns 초기화
        # 1. 메모장 비우기
        self._turns.clear()
```

세 메서드의 역할을 정리하면 이렇습니다.

#v(paragraph-gap)
+ #strong[`get_history()`] --- 저장된 대화를 `"사용자: 질문\nAI 비서: 답변"` 텍스트로 변환합니다. 이 텍스트가 실습 1에서 만든 LCEL 체인의 `{history}`에 들어갑니다.
+ #strong[`save_turn()`] --- 질문-답변 1턴을 `(question, answer)` 튜플로 `_turns`에 추가합니다. `deque(maxlen=k)` 덕분에 6번째가 들어오면 1번째가 자동으로 밀려납니다.
+ #strong[`clear()`] --- 대화 초기화. 새 세션을 시작하거나 사용자가 "대화 지우기"를 누르면 호출됩니다.

#v(paragraph-gap)
`get_history()`가 반환하는 텍스트가 실제로 어떻게 생겼는지 보겠습니다.

```
사용자: 병가 쓸 때 증빙 필요해?
AI 비서: 3일 미만은 불필요하고, 3일 이상은 진단서가 필요합니다.
사용자: 그러면 연차로 대체할 수 있어?
AI 비서: 네, 병가 대신 연차를 사용할 수 있습니다.
```

LLM이 이 히스토리를 보면 "그러면"이 병가를 가리킨다는 걸 이해할 수 있습니다.

#v(paragraph-gap)
`WindowMemory`를 세션별로 관리하는 기능은 `session_manager.py`에 분리되어 있습니다. 실습 1의 `rag_chain.py`에서 `build_llm()` 같은 인프라 함수를 import했던 것처럼, 여기서도 세션 관리는 별도 모듈이 담당합니다. `ConversationManager`는 여러 사용자(세션)의 메모장을 따로 관리하는 래퍼입니다. 세션별로 `WindowMemory`를 하나씩 만들고 TTL(기본 1시간)이 지나면 자동으로 정리합니다. 손님이 1시간 넘게 안 오면 메모장을 치우는 거라고 생각하면 됩니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([파일], [함수/메서드], [역할],),
    table.hline(),
    [`session_manager.py`], [`ConversationManager`], [세션별 WindowMemory 관리 + TTL 기반 만료 정리],
    [`session_manager.py`], [`get_conversation_manager()`], [ConversationManager 싱글턴 반환],
    [`session_manager.py`], [`get_history_text(session_id)`], [해당 세션의 대화 히스토리를 텍스트로 반환],
    [`session_manager.py`], [`save_turn(session_id, q, a)`], [질문-답변 1턴을 세션에 저장],
  )]
  , kind: table
  )

#callout-box([주의: 메모리 기반입니다], [`ConversationManager`의 세션 데이터는 서버 메모리에만 존재합니다. 서버를 재시작하면 대화 히스토리가 사라집니다. 실전 운영 환경에서는 Redis 같은 외부 저장소를 쓰는 게 일반적입니다. (CH07에서 운영을 위한 캐시 개념을 배우지만, 실습 환경의 복잡도를 낮추기 위해 외부 서비스(Redis) 연동 대신 인메모리 방식을 유지합니다.)])

#callout-box([팁: 다른 메모리 방식도 있습니다], [슬라이딩 윈도우(최근 N턴 유지)는 가장 단순한 방식입니다. 대화가 길어지면 앞부분이 통째로 사라지는 단점이 있습니다. 다른 접근도 있습니다. - #strong[Summary Memory] --- LLM이 이전 대화를 요약해서 저장. 긴 대화도 맥락을 유지하지만 요약할 때마다 LLM을 한 번 더 호출합니다. - #strong[Token Buffer Memory] --- 턴 수가 아니라 토큰 수 기준으로 제한. LLM의 컨텍스트 창을 효율적으로 사용합니다. - #strong[Summary Buffer Memory] --- 최근 대화는 원문 그대로, 오래된 대화는 요약. 위 두 방식의 절충안입니다.

#v(paragraph-gap)
이 책에서는 구현이 간단하고 LLM 추가 호출이 없는 슬라이딩 윈도우를 씁니다.])

=== 2.9 실행 결과

핵심 코드를 모두 살펴봤습니다. 이제 서버를 실행하고 브라우저에서 직접 질문해 보겠습니다. FastAPI 서버를 실행해 봅니다.

```bash
# 주의: Ollama가 미리 실행되어 있어야 합니다. (ollama serve 또는 앱 실행)
# FastAPI 서버 실행
python run.py
```

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH05/terminal/05_server-start.png", alt: [서버가 시작되면 채팅 UI 주소가 함께 출력됩니다.], max-width: 0.6)

#v(paragraph-gap)
브라우저에서 `http://localhost:8000/chat`을 열어 보겠습니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH05/terminal/05_chat-ui.png", alt: [브라우저에서 바로 질문할 수 있는 채팅 창구입니다. AI 비서가 자리에 앉았습니다.], max-width: 0.6)

#v(paragraph-gap)
"병가 쓸 때 증빙 서류가 필요한가요?"를 입력하고 잠시 기다려 봅니다.

#callout-box([참고: 첫 답변 대기 시간], [로컬 환경에서 모델을 처음 메모리에 올리고 추론하는 과정에서 약 60\~120초 정도 시간이 소요될 수 있습니다. 응답이 올 때까지 조금만 기다려주세요!])

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH05/terminal/05_chat-response.png", alt: [문서를 검색하고, 읽어서, 출처와 함께 자연어로 답변합니다.], max-width: 0.6)

#v(paragraph-gap)
이어서 "그러면 연차로 대체할 수 있어?"를 입력해 봅니다. 이전 대화를 기억하고 병가 맥락을 이어서 답변합니다. AI 비서가 메모장을 보고 있다는 뜻임을 알 수 있습니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH05/terminal/05_chat-response-followup.png", alt: [이전 대화 맥락(병가)을 기억하고 답변을 이어나갑니다.], max-width: 0.6)

#quote(block: true)[`Ctrl + C`를 눌러 서버를 종료해 주시기 바랍니다.]

=== 2.10 더 알아보기

#strong[LCEL vs 레거시 체인] --- LangChain 초기에는 `RetrievalQA`, `ConversationalRetrievalChain` 같은 미리 만들어진 체인을 썼습니다. 하지만 내부가 블랙박스라 커스터마이징이 어려웠습니다. LCEL은 각 단계를 파이프로 직접 조립하기 때문에 어디에 무슨 로직이 들어가는지 명확하게 보입니다. LangChain 0.2 이후부터는 LCEL이 권장 방식입니다.

#v(paragraph-gap)
#strong[temperature와 RAG] --- Q&A 시스템에서 `temperature=0.1`을 쓰는 건 일반적입니다. 0에 가까울수록 LLM이 확률 높은 토큰을 선택하므로 일관된 답변이 나옵니다. 반대로 창의적 글쓰기에서는 0.7\~1.0을 씁니다. RAG에서 temperature를 높이면 문서에 없는 내용을 "창작"할 위험이 커집니다.

#v(paragraph-gap)
#strong[윈도우 크기 튜닝] --- `CONVERSATION_WINDOW_SIZE=5`는 최근 5턴을 기억한다는 뜻입니다. 이 숫자를 키우면 맥락을 더 많이 유지할 수 있지만 프롬프트가 길어져서 연산 비용이 올라가고 응답이 느려집니다. 상용 API 모델은 아주 큰 컨텍스트 창을 지원하므로 대화 내용을 전부 밀어 넣어도 무리 없이 동작합니다. 하지만 실습에서 쓰려는 로컬 LLM(DeepSeek-R1:8B) 환경에서는 컨텍스트 창 제한과 처리 속도를 고려하면 최근 5턴만 유지하는 슬라이딩 윈도우가 현실적인 적정선입니다.

=== 2.11 이것만은 기억하세요

- #strong[검색은 재료, 답변은 요리입니다.] 벡터 검색으로 재료(문서 조각)를 찾고 LLM이 요리(자연어 답변)로 만들어줍니다. LCEL 파이프라인이 이 레시피입니다.
- #strong[출처 없는 답변은 근거 없는 주장입니다.] 프롬프트에 출처 강제를 넣어 환각을 잡습니다.
- 다음 챕터에서는 이 Q&A 엔진과 CH02의 사내 시스템(DB)을 합쳐서 "김대리 연차 개수와 사용 규정은?"이라는 #strong[복합 질문]에 답하는 #strong[통합 에이전트]를 만듭니다.

= Ch.6: QueryRouter와 ReAct Agent (ex06)

#quote(block: true)[한 줄 요약: CH05의 AI 비서가 질문 분류와 도구 호출을 배워 통합 에이전트로 진화한다. \
핵심 개념: QueryRouter (3단계 라우팅), 도구(Tool) --- \@tool 데코레이터, ReAct 패턴 + AgentExecutor]

== 안내데스크가 질문을 분류한다

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH06/gemini/06_chapter-opening.png", alt: [연차 조회와 규정 검색, 성격이 다른 두 질문을 하나의 시스템으로 처리합니다], max-width: 0.7)

=== 1.1 RAG가 답 못 하는 질문

CH05에서 RAG Q&A 엔진을 완성했습니다. 질문을 입력하면 사내 문서에서 내용을 찾아 답해주는 엔진입니다. 출처까지 같이 나오니 꽤 만족스러웠습니다.

#v(paragraph-gap)
옆자리 동료가 다가옵니다.

#v(paragraph-gap)
#strong[동료]: "이게 그 AI 비서예요? 한번 써봐도 되죠?"

#v(paragraph-gap)
#strong[오픈이]: "당연하죠. 뭐든 물어보세요."

#v(paragraph-gap)
동료가 채팅창에 질문을 입력합니다.

#v(paragraph-gap)
#strong[동료]: "A 사원 남은 연차는? 그리고 연차 신청 절차 알려줘."

#v(paragraph-gap)
잠시 후.

```
죄송합니다. 해당 직원에 대한 정보를 찾지 못했습니다.
```

동료가 고개를 갸웃합니다.

#v(paragraph-gap)
#strong[동료]: "직원 이름도 모르는 AI 비서예요?"

#v(paragraph-gap)
#emph[아…]

#v(paragraph-gap)
RAG는 사내 문서에서 'A 사원'을 찾으려고 했습니다. 당연히 없죠. 직원 연차 정보는 문서가 아니라 DB에 있으니까요. CH02에서 PostgreSQL에 저장해둔 데이터입니다. 문서 검색이 아니라 DB 조회가 필요한 질문인데 AI 비서는 그 차이를 몰랐습니다.

=== 1.2 정형 데이터와 비정형 데이터

지금 만들어둔 것을 돌이켜보면:

#v(paragraph-gap)
- #strong[ex02] 에서 직원/연차/매출 데이터를 PostgreSQL DB에 저장하는 API를 만들었습니다.
- #strong[ex04\~ex05] 에서 사내 문서를 벡터DB에 넣고 검색하는 RAG 엔진을 만들었습니다.

#v(paragraph-gap)
두 개가 따로 놀고 있습니다. AI 비서는 RAG만 쓸 줄 알지 DB에 어떻게 접근하는지는 모릅니다.

#v(paragraph-gap)
"A 사원 연차 몇 개?" → PostgreSQL에서 숫자를 조회하는 질문. "연차 신청 절차?" → 취업규칙 문서를 검색하는 질문. "A 사원 연차 + 신청 절차?" → 둘 다 필요한 복합 질문.

#v(paragraph-gap)
진짜 AI 비서가 되려면 이 두 가지를 상황에 맞게 골라 쓰거나, 필요하면 동시에 써야 합니다.

=== 1.3 Q&A 엔진에서 통합 에이전트로

회사에 처음 입사한 날을 떠올려 보겠습니다. 낯선 건물에 들어서자마자 1층 안내데스크로 향했을 것입니다. "인사 관련 서류는 어디서 받아요?" 물으면 안내 직원이 "3층 인사팀"이라고 알려줍니다. 복잡한 질문이면 여러 부서를 동시에 안내해주기도 합니다.

#v(paragraph-gap)
CH05의 AI 비서도 이런 안내 역할을 했습니다. 문서를 찾아서 답해주는 것까지는 잘 해냈죠. 그런데 질문이 다양해지면서 AI 비서 혼자서는 감당이 안 되기 시작합니다. "연차 며칠 남았어?"는 문서가 아니라 DB를 뒤져야 하고, "연차 잔여 + 신청 절차"는 DB와 문서를 동시에 봐야 합니다.

#v(paragraph-gap)
AI 비서가 질문을 분류하는 체계를 갖추고 필요한 도구를 직접 호출할 수 있게 되면 어떨까요? 질문의 종류를 판단하고(QueryRouter), 맞는 도구를 골라 실행하고(Tool), 결과를 종합해서 답하는(Agent) 시스템을 갖추는 것입니다.

#v(paragraph-gap)
#strong[AI 비서]: "인사팀은 3층이에요. 엘리베이터 내리셔서 오른쪽입니다."

#v(paragraph-gap)
#strong[AI 비서]: "교육 신청은 3층 인사팀이고, 노트북은 2층 IT 지원팀이에요. 두 곳 다 가셔야 해요."

#v(paragraph-gap)
AI 비서도 이렇게 되어야 합니다. 질문을 보고 DB가 필요한지 문서가 필요한지 아니면 둘 다인지 판단하게 됩니다. 판단이 끝나면 각 담당자(도구)에게 작업을 맡기고 결과를 하나로 묶어서 답해 주게 됩니다. CH05의 AI 비서가 질문 분류 + 도구 호출을 배워서 #strong[통합 에이전트]로 진화하는 것, 이번 챕터에서 만들 #strong[통합 에이전트]가 바로 이 AI 비서입니다.

=== 1.4 QueryRouter -- 3단계 질문 분류

에이전트 안에는 #strong[QueryRouter]라는 AI 비서의 '판단 규칙'이 들어 있습니다. 모든 질문은 3단계를 거쳐 분류되는데, 베테랑 AI 비서가 질문을 받고 어느 담당자에게 보낼지 판단하는 방식과 똑같습니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH06/gemini/06_receptionist-analogy.png", alt: [사용자의 질문 유형에 맞게 알맞은 도구를 배정하는 AI 비서.], max-width: 0.6)

#v(paragraph-gap)
#strong[1단계: 단어만 듣고 바로 알기 (키워드 매칭)] 가장 빠르고 확실한 방법입니다. - "연차", "매출"이 들리면 DB(정형 데이터) 담당자에게 보냅니다. - "절차", "규정"이 들리면 문서(비정형 데이터) 담당자에게 보냅니다. - 둘 다 들리면 양쪽 모두에게 보냅니다(복합 질문).

#v(paragraph-gap)
#strong[2단계: 전문 용어 파악하기 (컬럼명 매칭)] 일상적인 단어가 없다면 혹시 개발자가 쓴 `remaining_days`나 `emp_no` 같은 DB 컬럼명(전문 용어)이 섞여 있는지 확인해 봅니다. 발견되면 DB 담당자에게 넘겨주게 됩니다.

#v(paragraph-gap)
#strong[3단계: 꼼꼼하게 문맥 따져보기 (LLM 판단)] 단어만으로 도저히 모르겠으면 시간이 조금 걸리더라도 대규모 언어 모델(LLM)에게 직접 물어봐서 최종 목적지를 정하게 됩니다.

#v(paragraph-gap)
대부분의 질문은 바로 알아듣는 #strong[1단계]에서 끝납니다. 2단계와 3단계는 혹시 모를 상황을 대비한 '예비책'입니다. 쉬운 건 빠르게 처리하고 어려운 것만 시간 들여 고민하는 구조입니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH06/gemini/06_query-router.png", alt: [대부분의 질문은 1단계 키워드 매칭에서 끝납니다. 모호할 때만 더 비싼 방법을 씁니다.], max-width: 0.6)

=== 1.5 \@tool -- 에이전트용 도구

라우터가 방향을 정하면 에이전트가 도구 목록에서 맞는 것을 골라 쓰게 됩니다. 지금 만들어둔 도구는 네 가지입니다.

#figure(
  align(center)[#table(
    columns: 3,
    align: (auto,auto,auto,),
    table.header([도구], [역할], [비유],),
    table.hline(),
    [`leave_balance`], [직원 연차 잔여 조회], [인사팀 연차 담당자],
    [`sales_sum`], [부서별 매출 합계 조회], [재무팀 집계 담당자],
    [`list_employees`], [직원 목록 조회], [인사팀 명부 담당자],
    [`search_documents`], [문서 벡터 검색], [문서실 AI 비서],
  )]
  , kind: table
  )

AI 에이전트가 외부 기능을 호출하는 방법은 크게 두 가지가 있습니다. 하나는 Anthropic이 만든 #strong[MCP(Model Context Protocol)] 입니다. 도구를 별도 서버로 분리하고 표준 메시지 규격으로 통신하는 방식이라 어떤 프레임워크에서든 같은 도구를 재사용할 수 있습니다. 다른 하나는 LangChain의 `@tool` 데코레이터입니다. 같은 프로세스 안에서 함수를 직접 호출하니 설정이 간단합니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH06/diagram/06_tool-vs-mcp.png", alt: [LangChain \@tool 데코레이터와 MCP 방식의 도구 호출 비교], max-width: 0.6)

핵심 개념은 같습니다. "AI가 함수의 이름과 설명을 보고 스스로 호출한다." 이 책에서는 `@tool`로 원리를 익혀 보겠습니다. 원리를 이해하면 MCP로 확장하는 건 어렵지 않습니다.

#v(paragraph-gap)
각 도구 함수에 `@tool` 데코레이터와 독스트링(설명)을 붙여두면 LangChain이 도구의 이름과 설명, 파라미터를 자동으로 읽어갑니다. 코드는 기술 파트에서 직접 확인해 보겠습니다. 에이전트는 이 정보를 보고 "이 질문에는 어떤 도구가 맞지?"를 판단하게 됩니다. 이처럼 LLM이 상황에 맞는 도구를 스스로 골라서 호출하는 기능을 #strong[도구 호출(Tool Calling)] 이라고 합니다. 모든 LLM이 지원하는 건 아니라서 OpenAI의 `gpt-4o-mini` 나 Ollama의 `llama3.1:8b` 처럼 Tool Calling을 지원하는 모델을 골라야 합니다.

#v(paragraph-gap)
독스트링이 중요한 이유가 여기 있습니다. 함수 설명이 불명확하면 에이전트가 엉뚱한 도구를 고릅니다. AI 비서에게 각 도구가 무슨 일을 하는지 제대로 알려줘야 제대로 골라 쓰는 것과 마찬가지입니다.

=== 1.6 ReAct -- 생각하고 행동하고 확인한다

도구가 준비되었습니다. 이제 에이전트가 이 도구를 어떻게 쓰는지 볼까요. 에이전트의 두뇌는 #strong[ReAct 패턴]으로 동작합니다. Reason(추론) + Act(행동). 이름이 거창해 보이지만 원리는 단순합니다. 생각하고 행동하는 걸 반복하게 됩니다.

#v(paragraph-gap)
"A 사원 연차 얼마 남았고 연차 신청 절차는?" 이런 질문이 들어오면:

#v(paragraph-gap)
+ #strong[생각]: "연차 잔여를 알려면 leave\_balance 도구를 써야 해."
+ #strong[행동]: `leave_balance("A사원")` 호출 → DB에서 8일 반환
+ #strong[관찰]: "8일이구나. 이제 신청 절차도 찾아야 해."
+ #strong[생각]: "절차는 문서에 있을 거야. search\_documents 써야지."
+ #strong[행동]: `search_documents("연차 신청 절차")` 호출 → 취업규칙에서 절차 발견
+ #strong[관찰]: "이제 다 알았다."
+ #strong[최종 답변 생성]: "A 사원 연차 8일 남아 있고요, 규정에 따르면 3일 전까지…"

#v(paragraph-gap)
이 과정을 최대 10회까지 반복할 수 있습니다. 한 번에 답을 못 찾으면 다시 생각하고 다시 행동하게 됩니다. 도중에 오류가 나도 포기하지 않고 다른 방법을 시도하게 됩니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH06/diagram/06_react-flow.png", alt: [질문이 들어오면 QueryRouter가 분류하고, 에이전트가 ReAct 패턴으로 필요한 도구를 순서대로 호출합니다.], max-width: 0.6)

=== 1.7 AgentExecutor로 통합

동료가 다시 같은 질문을 입력합니다.

#v(paragraph-gap)
#strong[동료]: "A 사원 연차 몇 일 남았어요? 그리고 연차 신청 절차도 알려주세요."

#v(paragraph-gap)
이번엔 통합 에이전트가 답합니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH06/terminal/06_chat-hybrid-demo.png", alt: [한 번의 질문으로 AI 비서가 필요한 도구를 알아서 골라 정보를 조합해줍니다.], max-width: 0.6)

#v(paragraph-gap)
결과를 보고 동료가 고개를 끄덕입니다.

#v(paragraph-gap)
#strong[동료]: "이제 진짜 비서 같은데요."

#v(paragraph-gap)
#emph[해냈다!]

#v(paragraph-gap)
그럼 지금부터 이 AI 비서, #strong[통합 에이전트]를 직접 만들어 보겠습니다.

=== 1.8 이번 버전에서 뭘 만드나

ex06에서는 세 가지를 통합합니다.

#figure(
  align(center)[#table(
    columns: 3,
    align: (auto,auto,auto,),
    table.header([기능], [비유], [코드],),
    table.hline(),
    [3단계 질문 분류기], [AI 비서의 판단 기준], [`router.py`],
    [도구(Tool) 4개], [각 담당 도구], [`mcp_tools.py`],
    [통합 에이전트 (ReAct 패턴)], [AI 비서 전체], [`agent.py`],
  )]
  , kind: table
  )

이제 실습으로 DB 조회와 문서 검색을 하나로 합쳐 보겠습니다.

== 라우터, 도구, 통합 에이전트 조립하기

=== 2.1 용어 정리

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([비유], [기술 용어], [정식 정의],),
    table.hline(),
    [AI 비서 전체], [#strong[에이전트 (Agent)]], [사용자의 질문을 받아 스스로 판단하고, 필요한 도구를 선택·실행해서 최종 답변을 만들어내는 자율적 프로그램],
    [AI 비서의 분류 기준], [#strong[QueryRouter]], [사용자 질문을 분석해서 처리 경로(structured / unstructured / hybrid)를 결정하는 분류기],
    [각 담당자], [#strong[도구(Tool)]], [LangChain `@tool` 데코레이터로 선언된 함수. 에이전트가 선택해서 실행할 수 있는 원자적 작업 단위],
    [생각→행동→관찰 반복], [#strong[ReAct 패턴]], [Reason(추론) + Act(행동)의 반복으로 복잡한 질문을 단계적으로 해결하는 에이전트 실행 전략],
    [반복 실행기], [#strong[AgentExecutor]], [ReAct 루프를 실행하고 도구 호출을 관리하는 LangChain 컴포넌트],
  )]
  , kind: table
  )

=== 2.2 소스 코드 준비

클론한 레포에서 이번 챕터의 폴더로 이동합니다.

```bash
cd rag-start/ex06
```

```
ex06/
├── run.py                 [실습] 서버 플로우 실행
├── src/
│   ├── router.py          [실습] 3단계 QueryRouter
│   ├── mcp_tools.py       [실습] @tool 4개 (leave_balance, sales_sum, list_employees, search_documents)
│   ├── agent.py           [실습] 통합 에이전트 (IntegratedAgent)
│   ├── llm_factory.py     [참고] LLM 인스턴스 생성 (Ollama/OpenAI 분기)
│   ├── db_helper.py       [참고] PostgreSQL 쿼리 + ChromaDB 벡터스토어 구축
│   └── agent_helpers.py   [참고] 에이전트 결과 파싱/직렬화/폴백 유틸
├── app/
│   ├── main.py            [설명] FastAPI 앱 진입점
│   ├── chat_api.py        [설명] 에이전트/RAG 모드 선택 API
│   ├── admin_crud.py      [참고] 관리자 대시보드 DB CRUD
│   ├── admin_views.py     [참고] 관리자 대시보드 라우터
│   └── database.py        [참고] PostgreSQL 연결 래퍼
├── templates/
│   ├── chat.html          [참고] 채팅 웹 UI
│   ├── dashboard.html     [참고] 관리자 대시보드
│   ├── employees.html     [참고] 직원 관리 화면
│   ├── leaves.html        [참고] 휴가 관리 화면
│   └── sales.html         [참고] 매출 관리 화면
└── static/
    ├── css/chat.css       [참고] UI 스타일
    └── js/chat.js         [참고] 채팅 로직
```

`[실습]` 파일에는 import와 데이터가 미리 준비되어 있습니다. 챕터를 따라 하며 TODO의 `pass`를 지우고 코드를 하나씩 작성합니다. 막히는 부분이 있다면 rag-end의 완성 코드를 참고해 주시기 바랍니다.

=== 2.3 실습 환경 구축

#quote(block: true)[기본 환경(Python 3.12, Ollama, Docker)이 없다면 #strong[교육자료]를 먼저 확인해 주시기 바랍니다.]

```bash
cd ex06
cp .env.example .env
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
docker compose up -d       # PostgreSQL 실행
pip install -r requirements.txt
```

#callout-box([이전 챕터 Docker 종료], [CH02의 Docker가 실행 중이라면 `cd ex02 && docker compose down`으로 먼저 종료해 주시기 바랍니다. 같은 포트를 사용합니다.])

#figure(
  align(center)[#table(
    columns: 2,
    align: (auto,auto,),
    table.header([패키지], [역할],),
    table.hline(),
    [`langchain`], [체인/에이전트 프레임워크],
    [`langchain-ollama`], [Ollama LLM 연결],
    [`langchain-openai`], [OpenAI LLM 연결 (선택)],
    [`langchain-huggingface`], [HuggingFace 임베딩],
    [`chromadb`], [벡터 DB],
    [`psycopg2-binary`], [PostgreSQL 드라이버],
    [`fastapi`], [웹 API 서버],
  )]
  , kind: table
  )

#callout-box([주의], [Ollama에서 Tool Calling을 지원하는 모델을 골라야 합니다. 모든 모델이 Tool Calling을 지원하는 것은 아닙니다.])

참고로 "툴 콜링"은 LLM 제공사마다 명칭이 다릅니다. 개념은 같지만 API 형식이 다르기 때문에 LangChain 같은 프레임워크가 이 차이를 추상화해줍니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([제공사], [명칭], [API 형식],),
    table.hline(),
    [OpenAI (GPT)], [Function Calling / Tool Use], [`tool_calls` 필드로 응답],
    [Anthropic (Claude)], [Tool Use], [`tool_use` 블록으로 응답],
    [Google (Gemini)], [Function Calling], [`function_call` 파트로 응답],
    [Ollama (로컬)], [Tool Calling], [모델마다 지원 여부 다름],
  )]
  , kind: table
  )

Ollama에서 실행 가능한 로컬 모델의 Tool Calling 지원 현황입니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr, 1fr),
    align: (auto,center,center,auto,),
    table.header([모델], [Tool Calling], [한국어], [비고],),
    table.hline(),
    [#strong[llama3.1:8b]], [O], [O], [이 책에서 사용. 툴 콜링 안정성과 한국어 품질의 균형이 좋음],
    [qwen2.5:7b], [O], [O], [한국어 품질 우수. 대안으로 적합],
    [mistral:7b], [O], [△], [영어 중심. 한국어 사내 문서에는 불리],
    [deepseek-r1:8b], [X], [O], [추론(Chain-of-Thought) 특화. 툴 콜링 미지원],
    [llava:7b], [X], [X], [비전 특화. 툴 콜링·한국어 모두 미지원],
  )]
  , kind: table
  )

이 책에서는 #strong[llama3.1:8b] 를 사용합니다. 8B 크기로 16GB RAM에서 무리 없이 돌아가고, 툴 콜링 정확도와 한국어 응답 품질이 가장 균형 잡혀 있기 때문입니다.

```bash
ollama pull llama3.1:8b
```

`.env` 핵심 설정:

```
# Ollama 사용 시
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.1:8b   # Tool Calling 필수

# OpenAI 사용 시 (권장)
# LLM_PROVIDER=openai
# OPENAI_API_KEY=sk-... 
# OPENAI_MODEL=gpt-4o-mini
```

=== 2.4 실습 순서

+ `router.py` --- 3단계 질문 분류기
+ `mcp_tools.py` --- DB/문서 검색 도구
+ `agent.py` --- 통합 에이전트 조립 (ReAct 패턴)
+ `python run.py` --- 서버 실행 + 복합 질문 테스트

#v(paragraph-gap)
QueryRouter부터 도구, 통합 에이전트 순서로 작성하고 마지막에 서버를 띄워 테스트해 보겠습니다.

#v(paragraph-gap)
#emph[\[다이어그램\]]

#v(paragraph-gap)
#emph[질문이 안내데스크(QueryRouter)를 거쳐 담당자(도구)에게 전달되고, 에이전트가 결과를 묶어 답변합니다.]

#v(paragraph-gap)
다이어그램을 보며 전체 흐름을 먼저 파악해 보겠습니다. 질문이 안내데스크(QueryRouter)에 도착하면, 1.4에서 본 3단계 판단으로 "이 손님은 인사팀(DB)으로 보낼지, 문서실로 보낼지, 둘 다 보낼지"를 결정합니다. 방향이 정해지면 에이전트가 1.6의 ReAct 패턴대로 생각→행동→관찰을 반복하며 담당 도구를 호출합니다. 담당자들이 결과를 가져오면 에이전트가 하나로 묶어 답변을 돌려줍니다.

=== 2.5 실습 1: QueryRouter --- 3단계 질문 분류기 (router.py)

#emph[\[다이어그램\]]

#v(paragraph-gap)
#emph[파란색이 실습 1에서 만드는 부분입니다. 질문을 정형/비정형/혼합으로 분류하는 QueryRouter를 만듭니다.]

#v(paragraph-gap)
에이전트가 도구를 무작정 고르는 것보다 질문의 의미를 먼저 파악하고 방향을 잡아주면 성능이 훨씬 좋아집니다. 이를 위해 3단계로 질문을 분류하는 `QueryRouter`를 작성합니다. `ex06/src/router.py`를 열어 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

==== 1단계: 라우팅 판단 기준 키워드 정의

파일 상단에 이미 준비된 상수부터 확인해 볼까요. `router.py`에는 세 종류의 키워드 사전이 준비되어 있습니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr),
    align: (auto,auto,),
    table.header([상수], [역할],),
    table.hline(),
    [`STRUCTURED_KEYWORDS`], ["연차", "매출", "목록" 등 DB(정형 데이터) 조회와 관련된 단어],
    [`UNSTRUCTURED_KEYWORDS`], ["절차", "규정", "어떻게" 등 문서(비정형 데이터) 검색과 관련된 단어],
    [`SCHEMA_TERMS`], [`remaining_days`, `emp_no` 등 DB 컬럼명을 질문에서 직접 매칭할 때 쓰는 사전],
  )]
  , kind: table
  )

```python
# router.py — 상수 (파일에 이미 작성되어 있음)

# 정형 데이터(DB) 관련 키워드 — 숫자/통계/명단 조회
STRUCTURED_KEYWORDS = [
    "잔여", "잔량", "연차", "휴가", "남은", "몇 일", "며칠",
    "매출", "합계", "총액", "금액", "얼마", "실적",
    "목록", "명단", "직원", "사원", "리스트", "조회",
    "통계", "평균", "부서별", "합산", "입사일", "날짜"
]

# 비정형 데이터(문서) 관련 키워드 — 절차/정책/안내
UNSTRUCTURED_KEYWORDS = [
    "절차", "방법", "어떻게", "규정", "정책", "기준",
    "온보딩", "입사 안내", "가이드", "매뉴얼",
    "복지", "혜택", "보안", "출장", "비용",
    "설명해", "무엇인가", "어떤가",
]

# DB 스키마 컬럼/테이블명 — Step 2 매칭 대상
SCHEMA_TERMS = {
    "remaining_days": "structured", "used_days": "structured",
    "amount": "structured", "total_amount": "structured",
    "emp_no": "structured", "hire_date": "structured",
}
```

"연차", "매출", "목록" 같은 키워드가 있으면 DB 조회(structured)로, "규정", "절차", "어떻게" 같은 키워드가 있으면 문서 검색(unstructured)으로 분류합니다. `SCHEMA_TERMS`는 DB 컬럼명이 질문에 직접 언급될 때 사용합니다.

==== 2단계: QueryRouter 공개 인터페이스 구현

분류기 클래스를 선언하고 외부에서 호출할 `classify_query` 메서드를 먼저 작성해 보겠습니다. 규칙 기반 -\> 스키마 기반 -\> LLM 기반(폴백) 3단계 판별 구조가 어떻게 연결되는지 눈여겨보시길 바랍니다.

```python
# router.py — TODO: classify_query — 3단계로 질문 분류 (키워드 → 스키마 → LLM)

    def classify_query(self, query):
        """질문을 분석하여 처리 경로를 반환한다."""
        # 1. 규칙 기반 키워드 매칭
        step1_result = self._step1_rule_based(query)
        if step1_result is not None:
            return step1_result

        # 2. DB 스키마 컬럼명 매칭
        step2_result = self._step2_schema_based(query)
        if step2_result is not None:
            return step2_result

        # 3. LLM 판단 (폴백)
        if self._llm is not None:
            step3_result = self._step3_llm_based(query)
            if step3_result is not None:
                return step3_result

        # 4. 기본값: 비정형으로 처리
        return "unstructured"
```

==== 3단계: 내부 구현 메서드 (3단계 판단 로직)

인터페이스에서 호출한 `_step1_rule_based`, `_step2_schema_based`, `_step3_llm_based` 를 실제로 구현하는 코드입니다. 가장 저렴하고 빠른 키워드 매칭을 먼저 돌리고 그래도 안 될 때만 LLM을 호출합니다. 속도와 비용을 동시에 잡는 구조입니다.

#v(paragraph-gap)
#strong[Step 1: 규칙 기반 키워드 매칭] --- 가장 빠르고 저렴합니다. 대부분의 질문은 여기서 끝납니다.

```python
# router.py — TODO: _step1_rule_based — 키워드 매칭으로 경로 결정

def _step1_rule_based(self, query):
    query_lower = query.lower()

    # 1. STRUCTURED/UNSTRUCTURED 키워드 히트 수 계산
    structured_hits = sum(1 for kw in STRUCTURED_KEYWORDS if kw in query_lower)
    unstructured_hits = sum(1 for kw in UNSTRUCTURED_KEYWORDS if kw in query_lower)

    # 2. 양쪽 모두 히트 시 — 한 쪽이 2배 이상 우세하면 그 쪽, 아니면 hybrid
    if structured_hits > 0 and unstructured_hits > 0:
        if structured_hits > unstructured_hits * 2:
            return "structured"
        if unstructured_hits > structured_hits * 2:
            return "unstructured"
        return "hybrid"

    # 3. 한 쪽만 히트 시 — 해당 경로 반환
    if structured_hits > 0:
        return "structured"
    if unstructured_hits > 0:
        return "unstructured"
    return None
```

#strong[Step 2: DB 스키마 컬럼명 매칭] --- 키워드로 안 잡히면 DB 테이블 컬럼명과 대조합니다.

```python
# router.py — TODO: _step2_schema_based — DB 컬럼명 매칭으로 경로 결정

def _step2_schema_based(self, query):
    query_lower = query.lower()
    for term in SCHEMA_TERMS:
        if term in query_lower:
            return SCHEMA_TERMS[term]
    return None
```

#strong[Step 3: LLM 판단 (폴백)] --- 1, 2단계로 안 잡히는 모호한 질문만 LLM에 넘깁니다. 비용이 드니까 마지막 수단입니다.

```python
# router.py — TODO: _step3_llm_based — LLM에게 질문 분류 위임

def _step3_llm_based(self, query):
    prompt = f"""다음 질문을 아래 세 가지 유형 중 하나로 분류하세요.
    질문: {query}
    유형:
    - structured: 숫자, 통계, 목록 등 데이터베이스 조회가 필요한 질문
    - unstructured: 절차, 정책, 설명 등 문서 검색이 필요한 질문
    - hybrid: 두 가지가 모두 필요한 복합 질문
    반드시 JSON 형식으로만 답하세요:
    {{"route": "structured|unstructured|hybrid", "reason": "한 줄 근거"}}"""

    # 1. LLM에 질문 분류 요청
    response = self._llm.invoke(prompt)
    content = response.content if hasattr(response, "content") else str(response)
    # 2. <think> 태그 제거
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    # 3. JSON 추출 후 route 반환
    json_match = re.search(r"\{.*\}", content, re.DOTALL)
    if json_match:
        parsed = json.loads(json_match.group())
        route = parsed.get("route", "unstructured")
        if route in ("structured", "unstructured", "hybrid"):
            return route
    return None
```

3단계의 순서가 중요합니다. 확실한 신호(키워드)를 먼저 확인하고, 모호할 때만 비싼 방법(LLM 호출)을 씁니다.

=== 2.6 실습 2: \@tool 데코레이터 --- 에이전트용 도구 만들기 (mcp\_tools.py)

#emph[\[다이어그램\]]

#v(paragraph-gap)
#emph[파란색이 실습 2에서 만드는 부분입니다. 에이전트가 호출할 도구(DB조회, 문서검색)를 \@tool로 정의합니다.]

#v(paragraph-gap)
실습 1에서 QueryRouter가 질문의 방향을 잡아줬습니다. 이제 실제로 일할 도구가 필요합니다. 1.5에서 소개한 `@tool` 데코레이터를 기억하시나요? 함수에 데코레이터만 붙이면 에이전트가 이름과 설명을 읽고 스스로 판단해서 도구를 호출합니다. `ex06/src/mcp_tools.py`를 열어 네 함수의 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

#v(paragraph-gap)
여기서 #strong[Docstring(설명적 주석)] 이 매우 중요합니다. 에이전트가 이 내용을 읽고 어떤 도구를 호출할지, 인자(Arguments)는 무엇인지 파악하기 때문입니다. Docstring은 이미 파일에 작성되어 있으니 내용을 확인해 보시기 바랍니다.

#v(paragraph-gap)
이 코드에서 import하는 인프라 함수는 `db_helper.py`에 분리되어 있습니다. 직접 작성하지 않는 \[참고\] 파일이니 역할만 확인하고 넘어가면 됩니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([파일], [함수], [역할],),
    table.hline(),
    [`db_helper.py`], [`run_query(sql, params)`], [PostgreSQL 쿼리 실행 및 결과 반환],
    [`db_helper.py`], [`get_vectorstore()`], [ChromaDB 벡터스토어 연동 객체 반환],
  )]
  , kind: table
  )

==== 정형 데이터(DB) 조회 도구 3개

```python
# mcp_tools.py — TODO: leave_balance — 사번/이름으로 연차 조회

    # 1. DB 조회 (사번 또는 이름)
    if emp_no.startswith("E") and emp_no[1:].isdigit():
        rows = run_query(
            """
            SELECT e.emp_no, e.name, e.department,
                   l.total_days, l.used_days,
                   (l.total_days - l.used_days) AS remaining_days
            FROM employees e
            LEFT JOIN leave_balance l ON e.emp_no = l.emp_no
            WHERE e.emp_no = %s
            """,
            (emp_no,),
        )
    else:
        rows = run_query(
            """
            SELECT e.emp_no, e.name, e.department,
                   l.total_days, l.used_days,
                   (l.total_days - l.used_days) AS remaining_days
            FROM employees e
            LEFT JOIN leave_balance l ON e.emp_no = l.emp_no
            WHERE e.name LIKE %s
            """,
            (f"%{emp_no}%",),
        )

    # 2. DB 결과가 있으면 반환
    if rows:
        return rows[0]

    # 3. 결과 없으면 에러 반환
    return {"error": f"직원 '{emp_no}'을(를) 찾을 수 없습니다. {DB_ERROR_MSG}"}
```

사번(`E001`)이면 사번으로, 이름이면 LIKE 검색으로 DB를 조회합니다. 결과가 없으면 에러 메시지를 반환합니다.

#v(paragraph-gap)
`sales_sum` 함수의 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

```python
# mcp_tools.py — TODO: sales_sum — 부서별 매출 합계 조회

    # 1. 파라미터 기본값 처리
    start = start_date or "2024-11-01"
    end = end_date or "2024-12-31"

    # 2. DB 조회 (부서 필터 적용)
    dept_filter = f"AND e.department LIKE '%{dept}%'" if dept else ""
    rows = run_query(
        f"""
        SELECT e.department, e.name AS employee_name,
               SUM(s.amount) AS total_amount, COUNT(*) AS record_count
        FROM sales s
        JOIN employees e ON s.emp_no = e.emp_no
        WHERE s.sale_date BETWEEN %s AND %s {dept_filter}
        GROUP BY e.department, e.name
        ORDER BY total_amount DESC
        """,
        (start, end),
    )

    # 3. DB 결과 가공
    if rows:
        grand_total = sum(int(r.get("total_amount") or 0) for r in rows)
        return {
            "total_amount": grand_total,
            "record_count": len(rows),
            "dept_filter": dept or "전체",
            "period": f"{start} ~ {end}",
            "top5": rows[:5],
        }

    # 4. 결과 없으면 에러 반환
    return {"error": DB_ERROR_MSG, "dept_filter": dept or "전체", "period": f"{start} ~ {end}"}
```

기간과 부서 필터를 조합해서 매출 합계를 구합니다. 상위 5건을 함께 반환하여 에이전트가 구체적인 수치를 답변에 포함할 수 있게 합니다.

#v(paragraph-gap)
`list_employees` 함수의 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

```python
# mcp_tools.py — TODO: list_employees — 직원 목록 조회

    # 1. 조건 조립 (부서/이름 필터)
    conditions = []
    params = []
    sql_base = "SELECT emp_no, name, department, position, hire_date FROM employees "
    
    if dept:
        conditions.append("department LIKE %s")
        params.append(f"%{dept}%")
    if name:
        conditions.append("name LIKE %s")
        params.append(f"%{name}%")
        
    if conditions:
        sql = sql_base + " WHERE " + " AND ".join(conditions) + " ORDER BY name"
    else:
        sql = sql_base + " ORDER BY department, name"

    rows = run_query(sql, tuple(params))

    # 2. DB 결과 반환
    if rows:
        return {"employees": rows, "count": len(rows), "filter": {"dept": dept, "name": name}}

    # 3. 결과 없으면 에러 반환
    return {"error": DB_ERROR_MSG, "employees": [], "count": 0, "dept_filter": dept or "전체"}
```

부서와 이름 필터를 동적으로 조립하여 직원 목록을 조회합니다. 조건이 없으면 전체 직원을 부서순으로 반환합니다.

==== 3단계: 비정형 데이터(문서) 검색 도구 만들기

마지막으로 ChromaDB를 이용해 사내 문서를 벡터 검색하는 도구를 작성합니다. `search_documents` 함수의 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

```python
# mcp_tools.py — TODO: search_documents — 벡터 검색으로 관련 문서 조회

    # 1. ChromaDB 컬렉션 가져오기
    collection = get_vectorstore()
    if collection is not None:
        try:
            # 2. 벡터 검색 수행
            results = collection.query(query_texts=[query], n_results=k)

            # 3. 결과를 content/source/score 형태로 가공
            docs = []
            for i, doc in enumerate(results["documents"][0]):
                docs.append({
                    "content": doc,
                    "source": results["metadatas"][0][i].get("source", "unknown"),
                    "score": round(1 - results["distances"][0][i], 4),
                })
            return {"results": docs, "total_found": len(docs)}
        except Exception:
            pass

    # 4. 실패 시 빈 결과 반환
    return {"results": [], "total_found": 0}
```

파일 하단의 `ALL_TOOLS` 리스트는 네 가지 도구를 하나로 묶은 것입니다.

```python
ALL_TOOLS = [leave_balance, sales_sum, list_employees, search_documents]
```

이 리스트를 에이전트에게 건네면 에이전트는 "내가 쓸 수 있는 도구가 이 네 가지구나"라고 인식합니다.

#v(paragraph-gap)
에이전트가 어떤 도구를 호출할지는 `"""부서별 또는 전체 매출 합계를 조회한다."""` 같은 독스트링(Docstring)을 보고 결정합니다.

=== 2.7 실습 3: 통합 에이전트 조립하기 (agent.py)

#emph[\[다이어그램\]]

#v(paragraph-gap)
#emph[파란색이 실습 3에서 만드는 부분입니다. 실습 1의 라우터와 실습 2의 도구를 조립하여 에이전트가 ReAct 패턴으로 답변을 생성합니다.]

#v(paragraph-gap)
앞서 만든 라우터와 도구를 합쳐서 완성형 어시스턴트를 만들어 보겠습니다.

#v(paragraph-gap)
`ex06/src/agent.py`를 열어 두 메서드(`_build_agent_executor`, `run`)의 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

#v(paragraph-gap)
`IntegratedAgent` 클래스는 앞에서 만든 AI 비서의 질문 분류기(QueryRouter)와 도구(mcp\_tools)를 연결하는 껍데기입니다. 클래스 선언과 `__init__`은 이미 파일에 있으니 열어서 확인해 보시기 바랍니다. 파일 상단의 #strong[SYSTEM\_PROMPT]도 함께 보면 좋습니다. LLM에게 "당신은 누구이고, 무엇을 할 수 있고, 어떤 규칙을 지켜야 하는지"를 알려주는 지시문입니다.

==== \_build\_agent\_executor --- 에이전트 생성

`create_tool_calling_agent`는 LLM에게 "이 도구를 쓸 수 있다"고 알려주는 에이전트를 만들고, #strong[AgentExecutor]는 "생각 → 도구 호출 → 결과 확인" 루프를 반복 실행하는 실행기입니다.

```python
# agent.py — TODO: _build_agent_executor — 프롬프트 + Agent + Executor 조립

    def _build_agent_executor(self):
        """LangChain AgentExecutor를 생성한다."""
        from langchain.agents import AgentExecutor, create_tool_calling_agent
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

        # 1. 프롬프트 구성 (system + history + input + scratchpad)
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # 2. Tool Calling Agent 생성
        agent = create_tool_calling_agent(
            llm=self._llm,
            tools=ALL_TOOLS,
            prompt=prompt,
        )

        # 3. AgentExecutor 래핑 (중간 단계 반환 활성화)
        return AgentExecutor(
            agent=agent,
            tools=ALL_TOOLS,
            verbose=False,
            return_intermediate_steps=True,
            max_iterations=10,
            handle_parsing_errors=True,
        )
```

프롬프트가 4개 파트로 구성되어 있습니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr),
    align: (auto,auto,),
    table.header([파트], [역할],),
    table.hline(),
    [`system` (SYSTEM\_PROMPT)], ["당신은 누구이고 어떤 도구를 쓸 수 있는지" 규칙],
    [`chat_history`], [이전 대화 내용 (없으면 생략)],
    [`{input}`], [사용자 질문],
    [`agent_scratchpad`], [에이전트의 메모장 --- "leave\_balance 호출 → 결과 확인 → search\_documents 호출 → 결과 확인" 과정이 여기에 쌓임],
  )]
  , kind: table
  )

`agent_scratchpad`가 ReAct의 핵심입니다. 에이전트가 도구를 호출할 때마다 결과를 여기에 적어두고, 다음에 뭘 할지 판단합니다.

#v(paragraph-gap)
`IntegratedAgent` 에서 쓰는 인프라 함수는 별도 모듈로 분리해 두었습니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([파일], [함수], [역할],),
    table.hline(),
    [`llm_factory.py`], [`build_llm()`], [`LLM_PROVIDER` 환경변수에 따라 Ollama/OpenAI 중 선택],
    [`agent_helpers.py`], [`parse_agent_result(steps)`], [중간 단계에서 DB 결과 / 문서 결과를 분리 추출],
    [`agent_helpers.py`], [`serialize_steps(steps)`], [도구 호출 로그를 JSON 직렬화 가능한 형태로 변환],
  )]
  , kind: table
  )

==== 3단계: 라우팅 및 답변 생성 로직 실행

사용자의 질문이 들어왔을 때 맨 먼저 `QueryRouter`를 태우고, `AgentExecutor`에 전달하여 답변을 받아내는 최종 파이프라인 메서드입니다. `run` 메서드의 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

```python
# agent.py — TODO: run — 질문 분류 → 에이전트 실행 → 응답 정리

    def run(self, query):
        """질문을 처리하고 통합 응답을 반환한다."""
        # 1. 질문 유형 분류 (라우터 활용)
        query_type = self._router.classify_query(query)

        # 2. 에이전트 실행 (없으면 폴백)
        if self._agent_executor is None:
            return fallback_response(self._llm, query, query_type)

        try:
            result = self._agent_executor.invoke({"input": query})
            answer = result.get("output", "답변을 생성하지 못했습니다.")
            steps = result.get("intermediate_steps", [])

            # 3. DeepSeek-R1 <think> 태그 제거
            answer = clean_think_tags(answer)

            # 4. 중간 단계에서 정형/비정형 데이터 추출
            structured_data, unstructured_data = parse_agent_result(steps)

            # 5. 결과 딕셔너리 반환
            return {
                "answer": answer,
                "query_type": query_type,
                "structured_data": structured_data,
                "unstructured_data": unstructured_data,
                "steps": serialize_steps(steps),
            }
        except Exception as e:
            return {
                "answer": f"처리 중 오류가 발생했습니다: {e}",
                "query_type": query_type,
                "structured_data": {},
                "unstructured_data": [],
                "steps": [],
            }
```

`run` 메서드는 사용자의 질문이 들어왔을 때 가장 먼저 실행되는 관문입니다. 흐름을 정리하면 이렇습니다.

#v(paragraph-gap)
+ #strong[질문 분류]: `QueryRouter` 를 돌려서 이 질문이 정형(DB 대상)인지 비정형(문서 대상)인지 복합인지 판단합니다. 에이전트가 어떤 도구를 집중적으로 써야 할지 미리 힌트를 얻는 셈입니다.
+ #strong[에이전트 실행]: `AgentExecutor` 에 질문을 넘기면 에이전트가 도구를 골라 실행하며 ReAct 루프를 돕니다. 최종 답변과 중간 단계 기록을 모아옵니다.
+ #strong[잡음 제거 및 기록 추출]: DeepSeek-R1 같은 사색형(Reasoning) 모델은 `<think>` 태그 내부에 사고 과정을 남기는데 이를 지워주고 로깅 목적으로 호출된 DB와 문서 내역을 정리해서 반환합니다.

=== 2.8 실행 결과

실습 환경 구축을 마쳤다면 서버를 실행해 보겠습니다.

```bash
# 실행
python run.py
```

브라우저에서 `http://localhost:8000`으로 접속하면 채팅 화면이 열리게 됩니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH06/terminal/06_chat-initial.png", alt: [서버를 실행하면 브라우저에서 에이전트 채팅 인터페이스가 열립니다.], max-width: 0.6)

#v(paragraph-gap)
이번에는 채팅부터 시작하지 않고 #strong[관리자 대시보드]에서 데이터를 직접 추가해 보겠습니다.

==== 신입사원 등록

사이드바에서 #strong[직원 관리]를 클릭해 봅니다. `/admin/employees` 페이지가 열리게 됩니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH06/terminal/06_admin-employees.png", alt: [관리자 대시보드 --- 직원 관리 화면. 신입사원 홍길동을 등록합니다.], max-width: 0.6)

#v(paragraph-gap)
신입사원을 등록해 보겠습니다.

#v(paragraph-gap)
- #strong[이름]: 홍길동
- #strong[부서]: 개발부
- #strong[직급]: 사원
- #strong[입사일]: 2026-01-01

#v(paragraph-gap)
#strong[등록] 버튼을 누르면 사번이 자동으로 부여됩니다. 기존 데이터에 E001\~E010이 있으니 `E011`이 됩니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH06/terminal/06_admin-employees-list.png", alt: [등록 완료. 직원 목록에 E011 홍길동이 추가되었습니다.], max-width: 0.6)

==== 채팅으로 확인

이제 사이드바에서 #strong[통합 채팅]을 클릭해 봅니다. 채팅창에 이렇게 입력해 보겠습니다.

```
홍길동 입사일 언제야?
```

잠시 기다리면 에이전트가 답합니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH06/terminal/06_chat-crud-result.png", alt: [방금 등록한 신입사원의 정보를 에이전트가 DB에서 찾아 답합니다.], max-width: 0.6)

#v(paragraph-gap)
방금 대시보드에서 등록한 데이터를 에이전트가 찾아냈습니다. 무슨 일이 벌어진 건지 시퀀스 다이어그램으로 살펴보겠습니다.

#v(paragraph-gap)
#emph[\[다이어그램: 사용자: 홍길동 입사일 언제야? → QueryRouter 키워드 매칭 → 통합 에이전트 (ReAct 패턴) → ReAct 패턴 → 01 THINK: list\_employees 도구를 써야지 → 02 ACT: list\_employees('홍길동')\]]

#v(paragraph-gap)
#emph[QueryRouter에서 통합 에이전트, DB 조회, 자연어 답변까지의 흐름입니다]

#v(paragraph-gap)
+ QueryRouter가 "입사일"이라는 키워드를 보고 `structured` #strong[\(정형)] 로 분류했습니다.
+ 에이전트가 ReAct 패턴으로 `list_employees` 도구를 골랐습니다.
+ `list_employees` 가 PostgreSQL에서 "홍길동"을 찾아 결과를 돌려줬습니다.
+ 에이전트가 결과를 읽고 자연어 답변을 만들었습니다.

#v(paragraph-gap)
대시보드에서 데이터를 넣고 채팅에서 바로 물어보는 것, DB와 AI가 연결된 에이전트의 핵심입니다.

==== 복합 질문도 테스트

이번에는 DB와 문서를 동시에 써야 하는 질문을 던져 보겠습니다.

```bash
홍길동 연차 몇 일 남았어? 그리고 연차 신청 규정은?
```

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH06/terminal/06_hybrid-response.png", alt: [연차 잔여(DB)와 신청 규정(문서)을 동시에 가져옵니다.], max-width: 0.6)

#v(paragraph-gap)
에이전트가 `leave_balance` -\> `search_documents` 순서로 두 도구를 호출했습니다. 한 번의 질문으로 DB 조회와 문서 검색을 동시에 해낸 것입니다.

#quote(block: true)[`Ctrl + C`를 눌러 서버를 종료해 주시기 바랍니다. Docker 컨테이너도 `docker compose down`으로 정리해 주시기 바랍니다.]

=== 2.9 더 알아보기

#strong[QueryRouter 없이 에이전트만 써도 되지 않나요?]

#v(paragraph-gap)
에이전트에게 모든 판단을 맡기면 매번 LLM 호출이 발생합니다. 간단한 "연차 조회" 질문에도 "어떤 도구를 쓸까?" 고민하는 LLM 비용이 붙습니다. QueryRouter가 빠르게 사전 분류를 해주면 에이전트가 처음부터 방향을 잡고 시작할 수 있습니다.

#v(paragraph-gap)
#strong[Ollama와 OpenAI 중 어떤 걸 써야 하나요?]

#v(paragraph-gap)
에이전트에서는 Tool Calling이 핵심입니다. LLM이 "지금 어떤 도구를 써야지"를 스스로 결정해야 하기 때문입니다. OpenAI의 `gpt-4o-mini`는 Tool Calling 성능이 검증되어 있어 결과가 안정적입니다. Ollama를 쓸 때는 반드시 Tool Calling을 지원하는 모델(`llama3.1:8b`)을 골라야 합니다. `.env`에서 `LLM_PROVIDER=openai`로 바꾸면 나머지 코드는 그대로입니다. `build_llm()` 함수가 환경 변수를 보고 알아서 LLM을 바꿔주기 때문입니다.

=== 2.10 이것만은 기억하세요

- #strong[AI 비서가 통합 에이전트로 진화했습니다.] 질문을 분류하고 도구를 호출하여 답변합니다.
- QueryRouter가 질문을 분류하고, `@tool` 데코레이터가 도구를 만들고, 에이전트가 ReAct 패턴으로 반복 실행하면서 답을 완성합니다.

#v(paragraph-gap)
다음 챕터(ex07)에서는 이 에이전트를 실제로 운영하면서 생기는 문제를 다룹니다. 같은 질문에 매번 LLM을 호출하는 비용 문제, 응답이 느려지는 속도 문제, 그리고 누가 얼마나 쓰는지 모르는 추적 문제입니다.

= Ch.7: 캐시와 모니터링 (ex07)

#quote(block: true)[한 줄 요약: 통합 에이전트에 메모장과 업무 일지를 달아, 같은 질문엔 바로 답하고 하루 사용량을 기록한다. 핵심 개념: ResponseCache(TTL), EmbeddingCache, TokenTracker, ConnectHRAgent]

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH07/gemini/07_chapter-opening.png", alt: [팀원이 실제로 사용하면서 드러나는 속도 문제와 운영 사각지대를 마주합니다], max-width: 0.7)

== 사서에게 메모장이 필요해졌다

=== 1.1 일주일 뒤, 불만이 시작되다

CH06에서 통합 에이전트를 완성했습니다. 질문을 분류하고 도구를 골라 실행하는 AI 비서. 동료도 "이제 진짜 비서 같은데요"라고 했습니다. 오픈이는 자리에 앉아 모니터를 바라보며 속으로 작은 보람을 느꼈습니다.

#v(paragraph-gap)
일주일이 흘렀습니다.

#v(paragraph-gap)
오전 10시. 슬랙 알림이 연달아 울립니다. 오픈이가 채널을 열었습니다.

#v(paragraph-gap)
#strong[동료]: "병가 증빙 서류 뭐가 필요한지 아까도 물어봤는데, 또 물어보니까 또 20초 걸리네요."

#v(paragraph-gap)
20초. 커서만 깜빡이는 화면을 바라보며 기다리는 20초는 꽤 깁니다.

#v(paragraph-gap)
#emph[같은 질문인데 왜 매번 처음부터 찾는 거야…]

#v(paragraph-gap)
#strong[동료]: "우리 팀에서 하루에 30번은 쓰는 것 같은데, 얼마나 쓰고 있는 건지 파악이 안 돼요."

#v(paragraph-gap)
오픈이가 터미널을 열어 로그를 뒤져봤습니다. 호출 횟수나 응답 시간을 정리해둔 곳이 없었습니다. 하루에 몇 건 처리하는지, 평균 응답 시간이 얼마인지. 아무 기록도 없었습니다.

#v(paragraph-gap)
문제는 또 있었습니다. 간간이 슬랙에 올라오는 "에러가 났어요" 메시지. 확인해 보면 네트워크 타임아웃이거나 LLM 파싱 실패. 잠깐 뒤에 다시 물어보면 정상인데 사용자 입장에서는 "고장났다"고 느낄 수밖에 없죠. ex06의 에이전트는 에러가 한 번 나면 그대로 멈춰버렸습니다.

=== 1.2 캐시 -- 사서의 메모장 두 권

오픈이가 팀장 자리로 갔습니다. 노트북 화면에 슬랙 불만 메시지를 띄워 보여줬습니다.

#v(paragraph-gap)
#strong[팀장]: "같은 질문에 매번 서가를 뒤지는 사서가 있으면 어떻겠어?"

#v(paragraph-gap)
#strong[오픈이]: "비효율적이죠."

#v(paragraph-gap)
#strong[팀장]: "그럼 뭐가 필요해?"

#v(paragraph-gap)
잠시 생각했습니다.

#v(paragraph-gap)
#emph[메모장. 한 번 찾은 답을 적어두는 메모장이 있으면 되잖아.]

#v(paragraph-gap)
오픈이가 화이트보드에 펜을 잡았습니다. 마커 뚜껑을 딸깍 열고 네모 두 개를 그렸습니다.

#v(paragraph-gap)
첫 번째 메모장. 누군가 "병가 증빙 서류가 뭐예요?"라고 물었습니다. 사서가 서가를 뒤져서 답을 찾았습니다. 그 답을 메모장에 적어둡니다. 30분 뒤에 같은 질문이 또 오면 서가에 가지 않고 메모장을 읽어줍니다. 다만 메모장에는 유통기한이 있습니다. 규정이 바뀌었을 수도 있으니까요. 1시간이 지나면 메모를 지우고 다시 서가에서 찾아옵니다.

#v(paragraph-gap)
두 번째 메모장. 사서가 문서를 검색하려면 질문 문장을 숫자 배열로 바꿔야 합니다. 이 변환에도 시간이 걸리는데, 같은 문장을 매번 다시 변환할 필요는 없습니다. 한 번 계산한 결과를 파일에 적어두면 다음에는 바로 꺼내 씁니다.

#v(paragraph-gap)
#strong[팀장]: "그 메모장에 유통기한을 붙이는 게 핵심이야. 너무 오래된 메모를 읽어주면 안 되니까."

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH07/gemini/07_cache-concept.png", alt: [같은 질문이 또 오면 서가에 가지 않고 메모장을 읽어줍니다. 임베딩 변환 결과도 파일로 보관합니다.], max-width: 0.6)

#v(paragraph-gap)
오픈이가 고개를 끄덕였습니다.

=== 1.3 TokenTracker와 Retry -- 업무 일지와 재시도 매뉴얼

동료의 두 번째 불만이 떠올랐습니다. "얼마나 쓰고 있는 건지 파악이 안 돼요."

#v(paragraph-gap)
#strong[오픈이]: "사용량 추적이 안 되고 있어요. 하루에 몇 건 처리하는지, 응답 시간이 평균 얼마인지 아무것도 모릅니다."

#v(paragraph-gap)
#strong[팀장]: "사서한테 업무 일지를 쓰게 해."

#v(paragraph-gap)
업무 일지. 매 질문마다 한 줄씩 기록을 남기는 겁니다. 몇 시에 어떤 질문을 받았고 응답에 몇 초 걸렸는지. 토큰을 얼마나 사용했는지. 이 기록이 쌓이면 "이번 주 평균 응답 시간이 얼마야?"에 답할 수 있게 됩니다.

#v(paragraph-gap)
#emph[로컬 모델이니까 비용은 0원이지만, 응답 시간이랑 사용량은 알아야 하잖아.]

#v(paragraph-gap)
지금은 Ollama라서 비용은 0원이지만, 토큰 수와 응답 시간을 기록해두는 습관이 먼저입니다.

#v(paragraph-gap)
에러 문제도 간단합니다. 사서에게 매뉴얼 한 장을 주면 됩니다. "한 번 실패하면 3번까지 다시 시도해. 시도 사이에는 2초씩 쉬고." 네트워크가 잠깐 끊기거나 모델이 과부하에 걸리는 일시적 문제는 잠깐 뒤에 재시도하면 대부분 풀립니다.

=== 1.4 ConnectHRAgent -- 세 가지를 달아보다

화이트보드에 정리한 내용을 코드로 옮기기 시작합니다. 메모장 두 개, 업무 일지 하나, 재시도 매뉴얼 하나.

#v(paragraph-gap)
#emph[오, 이거면 불만이 싹 사라지겠는데?]

#v(paragraph-gap)
캐시를 붙이고 같은 질문을 다시 던져봤습니다. 0.1초. 20초가 0.1초로 줄었습니다. 오픈이가 의자 등받이에 기대며 모니터를 바라봤습니다.

#v(paragraph-gap)
슬랙에 결과를 공유하려고 스크린샷을 찍는데, 터미널에 에러 로그가 한 줄 찍혔습니다. "시도 1/3 실패: timeout." 순간 멈칫했습니다. 하지만 바로 아래에 "시도 2/3 성공"이라는 줄이 이어졌습니다.

#v(paragraph-gap)
재시도가 작동한 것입니다. ex06이었으면 그대로 멈춰서 사용자에게 에러를 던졌을 장면. 오픈이가 조용히 주먹을 쥐었습니다.

#v(paragraph-gap)
동료에게 다시 써보라고 했습니다.

#v(paragraph-gap)
#strong[동료]: "어? 이번엔 바로 나오는데요?"

#v(paragraph-gap)
#strong[오픈이]: "같은 질문은 메모장에서 꺼내주거든요."

#v(paragraph-gap)
#strong[동료]: "사용량은 확인할 수 있어요?"

#v(paragraph-gap)
토큰 추적 로그를 열어 보여줬습니다. 오늘 총 47건 처리. 캐시 적중률 72%. 평균 응답 시간 3.2초. 캐시에 걸린 질문은 0.1초도 안 걸리니까 전체 평균을 확 끌어내린 수치입니다.

#v(paragraph-gap)
동료가 고개를 끄덕입니다.

#v(paragraph-gap)
#strong[동료]: "이제 좀 쓸 만하네요."

#v(paragraph-gap)
이제 그 메모장과 업무 일지, 재시도 매뉴얼을 직접 만들어 보겠습니다.

== 캐시, 모니터링, 재시도를 코드로 만들기

=== 2.1 용어 정리

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([이야기 속 표현], [진짜 이름], [정의],),
    table.hline(),
    [답변 메모장 (유통기한 있음)], [#strong[ResponseCache]], [TTL(유효시간) 기반 인메모리 응답 캐시. SHA-256 해시 키로 질문을 식별하고 만료 전까지 동일 질문에 캐시된 답변을 반환한다],
    [임베딩 메모장 (파일 저장)], [#strong[EmbeddingCache]], [파일 기반 임베딩 벡터 캐시. pickle로 벡터를 저장하고 프로세스 재시작 후에도 유지된다],
    [업무 일지], [#strong[TokenTracker]], [LLM 호출별 입출력 토큰 수, 응답 시간, 비용(API 전환 시)을 누적 집계하는 추적기],
    [메모장+재시도가 붙은 AI 비서], [#strong[ConnectHRAgent]], [ex06의 IntegratedAgent에 캐시, 모니터링, 재시도를 통합한 운영용 에이전트],
    [3번까지 다시 시도], [#strong[Retry 로직]], [LLM 호출 실패 시 최대 N회까지 재시도하는 안정성 패턴. 재시도 사이에 대기 시간을 포함한다],
  )]
  , kind: table
  )

=== 2.2 소스 코드 준비

클론한 레포에서 이번 챕터의 폴더로 이동합니다.

```bash
cd rag-start/ex07
```

```
ex07/
├── run.py                    서버 실행 진입점
├── src/
│   ├── agent_config.py     [실습] ConnectHRAgent — 캐시/모니터링/재시도 통합
│   ├── _agent_utils.py            완성 코드 (AgentExecutor 구성 + 재시도)
│   ├── cache.py            [실습] ResponseCache(TTL) + EmbeddingCache
│   ├── _cache_utils.py            완성 코드 (해시 키 생성 + 캐시 통계)
│   ├── monitoring.py       [설명] TokenTracker + setup_logging
│   ├── _monitoring_utils.py       완성 코드 (비용 계산 + Langfuse 연동)
│   ├── llm_factory.py      [참고] LLM 인스턴스 생성 (Ollama/OpenAI 분기)
│   ├── agent_helpers.py    [참고] RAG 체인 구성 + 라우팅 매핑
│   ├── router.py           [참고] 3단계 QueryRouter (CH06에서 작성)
│   └── tools/
│       ├── __init__.py     [참고] 도구 패키지 초기화
│       ├── leave_balance.py  [참고] 연차 조회 도구
│       ├── sales_sum.py      [참고] 매출 합계 도구
│       ├── list_employees.py [참고] 직원 목록 도구
│       └── search_documents.py [참고] 문서 검색 도구
├── app/
│   ├── main.py             [참고] FastAPI 앱 진입점
│   ├── chat_api.py         [참고] Agent API 엔드포인트
│   └── database.py         [참고] PostgreSQL 연결
├── templates/
│   └── chat.html           [참고] 채팅 웹 UI
└── static/
    ├── css/chat.css        [참고] UI 스타일
    └── js/chat.js          [참고] 채팅 로직
```

`[실습]` 파일에는 import와 상수가 미리 준비되어 있습니다. 챕터를 따라 하며 TODO의 `pass`를 지우고 코드를 작성합니다. `_utils` 접두사가 붙은 파일은 완성 코드로, 실습 파일에서 import해 사용하는 보조 함수가 담겨 있습니다. 막히면 rag-end의 완성 코드를 참고해 주시기 바랍니다.

=== 2.3 실습 환경 구축

#quote(block: true)[기본 환경(Python 3.12, Ollama, Docker)이 없다면 #strong[교육자료]를 먼저 확인해 주시기 바랍니다.]

```bash
cd ex07
cp .env.example .env
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
docker compose up -d       # PostgreSQL 실행
pip install -r requirements.txt
```

#callout-box([이전 챕터 Docker 종료], [CH06의 Docker가 실행 중이라면 `cd ex06 && docker compose down`으로 먼저 종료해 주시기 바랍니다.])

#figure(
  align(center)[#table(
    columns: 2,
    align: (auto,auto,),
    table.header([패키지], [역할],),
    table.hline(),
    [`langchain`], [체인/에이전트 프레임워크],
    [`langchain-ollama`], [Ollama LLM 연결],
    [`langchain-chroma`], [ChromaDB Retriever],
    [`sentence-transformers`], [ko-sroberta 임베딩],
    [`psycopg2-binary`], [PostgreSQL 드라이버],
    [`fastapi`], [웹 API 서버],
  )]
  , kind: table
  )

=== 2.4 실습 순서

+ `cache.py` -- 답변 메모장 + 임베딩 메모장
+ `monitoring.py` -- 업무 일지 + JSON 로깅
+ `agent_config.py` -- 메모장과 일지를 단 운영용 에이전트
+ `python run.py` -- 서버 실행 + 캐시 적중 확인

#v(paragraph-gap)
ex07에서 새로 추가되는 파일은 `cache.py`와 `monitoring.py` 두 개입니다. `agent_config.py`는 ex06의 에이전트를 이 둘로 감싸는 역할이고, 나머지는 ex06에서 가져와 구조만 정리한 것입니다.

#v(paragraph-gap)
#emph[\[다이어그램: 질문 입력 → ResponseCache 조회 → 캐시 응답 즉시 반환 → QueryRouter 분류 → 경로별 실행 (RAG/Agent) → TokenTracker 기록\]]

#v(paragraph-gap)
#emph[질문이 들어오면 먼저 메모장(캐시)을 뒤지고, 없을 때만 서가(LLM)에 갑니다]

#v(paragraph-gap)
메모장(ResponseCache)을 먼저 만들고, 업무 일지(TokenTracker)를 만든 뒤, ConnectHRAgent에서 이 둘을 조립하는 순서입니다. 부품을 먼저 만들고 마지막에 하나로 합칩니다.

=== 2.5 실습 1: ResponseCache + EmbeddingCache -- 사서의 메모장 두 권 (cache.py)

#emph[\[다이어그램: 질문 입력 → ResponseCache 조회 → QueryRouter 분류 → 경로별 실행 → TokenTracker 기록 → ResponseCache 저장\]]

#v(paragraph-gap)
#emph[파란색이 실습 1에서 만드는 부분입니다. 질문이 메모장에 있는지 확인하고, 없으면 새로 찾은 답을 메모장에 적어둡니다.]

#v(paragraph-gap)
팀장이 말한 유통기한 있는 메모장, 그리고 벡터 변환 결과를 파일로 적어두는 메모장. 이 두 권을 코드로 만들어 봅니다. `ex07/src/cache.py`를 열어 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

==== 상수와 보조 함수

파일 상단의 import와 상수, 그리고 `_cache_utils.py`에서 가져오는 보조 함수는 이미 준비되어 있습니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([상수], [기본값], [역할],),
    table.hline(),
    [`DEFAULT_RESPONSE_TTL`], [3600 (초)], [메모장의 유통기한. 1시간이 지나면 메모를 지운다],
    [`DEFAULT_EMBEDDING_CACHE_DIR`], [`./outputs/embedding_cache`], [임베딩 벡터를 저장할 디렉토리 경로],
    [`DEFAULT_RESPONSE_CACHE_MAX_SIZE`], [1000], [메모장에 적을 수 있는 최대 항목 수],
  )]
  , kind: table
  )

`_cache_utils.py`는 완성 코드입니다. 캐시 키 생성(`make_response_key`)과 통계 집계(`response_cache_stats`), 임베딩 파일 읽기/쓰기(`embedding_get`, `embedding_set`) 등 반복적인 보조 로직이 들어 있습니다. 실습에서는 이 함수를 import해서 사용합니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([보조 함수], [파일], [역할],),
    table.hline(),
    [`make_response_key(query, context)`], [`_cache_utils.py`], [query와 context를 합쳐 SHA-256 해시 키를 생성],
    [`response_cache_stats(cache)`], [`_cache_utils.py`], [캐시 통계(항목 수, 적중률, TTL)를 딕셔너리로 반환],
    [`response_cache_clear(cache)`], [`_cache_utils.py`], [만료된 캐시 항목을 제거하고 삭제 수를 반환],
    [`embedding_get(cache_dir, text, _)`], [`_cache_utils.py`], [파일에서 임베딩 벡터를 조회. (벡터, 히트, 미스) 튜플 반환],
    [`embedding_set(cache_dir, text, emb)`], [`_cache_utils.py`], [임베딩 벡터를 pickle 파일로 저장],
  )]
  , kind: table
  )

==== 1단계: ResponseCache -- 유통기한 있는 답변 메모장

`ResponseCache` 클래스의 `get`과 `set` 메서드를 채워 봅니다. 같은 질문이 또 오면 서가에 가지 않고 메모장을 읽어주는 부분입니다.

```python
# cache.py — TODO: get — 캐시에서 응답을 조회 (TTL 만료 체크)

    def get(self, query, context=""):
        """캐시에서 응답을 조회합니다 (TTL 만료 체크)."""
        # 1. 질문을 해시 키로 변환
        key = make_response_key(query, context)

        # 2. 메모장에서 키 조회
        entry = self._store.get(key)
        if entry is None:
            self._misses += 1
            return None

        # 3. 유통기한 확인
        value, expires_at = entry
        if time.time() > expires_at:
            del self._store[key]
            self._misses += 1
            return None

        # 4. 유효하면 적중 카운트 증가 후 반환
        self._hits += 1
        return value
```

`_store` 딕셔너리에 `(값, 만료시각)` 튜플이 저장되어 있습니다. 현재 시각이 만료시각을 지나면 해당 항목을 삭제하고 `None`을 반환합니다. 팀장이 말한 "유통기한"이 바로 이 만료시각 비교입니다.

```python
# cache.py — TODO: set — 캐시에 응답을 저장 (max_size 초과 시 가장 오래된 항목 제거)

    def set(self, query, value, context=""):
        """캐시에 응답을 저장합니다 (max_size 초과 시 LRU 정리)."""
        # 1. 질문을 해시 키로 변환
        key = make_response_key(query, context)

        # 2. 메모장이 꽉 찼으면 유통기한이 가장 임박한 메모를 지운다
        if len(self._store) >= self.max_size:
            oldest_key = min(self._store, key=lambda k: self._store[k][1])
            del self._store[oldest_key]

        # 3. 만료 시각을 계산하여 저장
        expires_at = time.time() + self.ttl
        self._store[key] = (value, expires_at)
```

`max_size`\(기본 1,000)를 넘기면 만료 시각이 가장 가까운 항목부터 제거합니다. 새 항목은 현재 시각 + TTL(기본 3,600초)을 만료 시각으로 기록합니다.

#v(paragraph-gap)
`clear()`와 `stats()` 메서드는 `_cache_utils.py`의 보조 함수를 호출하는 래퍼로 이미 작성되어 있습니다.

==== 2단계: EmbeddingCache -- 벡터 변환 결과를 파일에 적어두기

문서 검색 때마다 질문을 벡터로 변환하는 작업이 반복됩니다. 한 번 계산한 벡터를 파일에 저장해두면 다음에는 계산 없이 바로 꺼내 씁니다.

```python
# cache.py — TODO: get_or_compute — 캐시 히트면 반환, 미스면 계산 후 저장

    def get_or_compute(self, text, compute_fn):
        """캐시 히트면 반환, 미스면 compute_fn으로 계산 후 저장합니다."""
        # 1. 파일 캐시에서 조회
        emb, hits_delta, misses_delta = embedding_get(self.cache_dir, text, None)
        self._hits += hits_delta
        self._misses += misses_delta

        # 2. 히트면 바로 반환
        if emb is not None:
            return emb

        # 3. 미스면 직접 계산
        emb = compute_fn(text)

        # 4. 결과를 파일에 저장
        embedding_set(self.cache_dir, text, emb)
        return emb
```

`embedding_get`은 텍스트의 SHA-256 해시로 `.pkl` 파일을 찾아봅니다. 파일이 있으면 pickle로 읽어서 벡터를 반환하고, 없으면 `compute_fn`이 직접 임베딩을 계산합니다. ResponseCache와 다른 점은 저장 위치가 메모리가 아니라 #strong[파일]이라는 것입니다. 서버를 재시작해도 임베딩 캐시는 남아 있습니다.

==== 3단계: 싱글턴 인스턴스

파일 하단의 싱글턴은 이미 준비되어 있습니다.

```python
# cache.py — 싱글턴 인스턴스 (파일에 이미 작성되어 있음)

response_cache = ResponseCache(
    ttl=int(os.getenv("CACHE_TTL", str(DEFAULT_RESPONSE_TTL))),
    max_size=int(os.getenv("CACHE_MAX_SIZE", str(DEFAULT_RESPONSE_CACHE_MAX_SIZE))),
)
```

모듈이 임포트될 때 인스턴스가 하나 생성됩니다. 어디서든 `from .cache import response_cache`로 같은 인스턴스를 공유합니다. `.env`에서 `CACHE_TTL`과 `CACHE_MAX_SIZE` 값을 바꿀 수 있습니다.

#quote(block: true)[#strong[ResponseCache vs EmbeddingCache 비교]

#figure(
  align(center)[#table(
    columns: 3,
    align: (auto,auto,auto,),
    table.header([], [ResponseCache], [EmbeddingCache],),
    table.hline(),
    [저장 위치], [메모리], [파일 (`.pkl`)],
    [재시작 시], [사라짐], [유지됨],
    [TTL], [있음 (기본 1시간)], [없음 (영구)],
    [용도], [LLM 응답 재사용], [임베딩 벡터 재계산 방지],
  )]
  , kind: table
  )]

=== 2.6 설명 1: TokenTracker + JSON 로깅 -- 사서의 업무 일지 (monitoring.py)

메모장(캐시) 다음은 업무 일지(모니터링)입니다. 팀장이 "업무 일지를 쓰게 해"라고 한 것을 코드로 옮겨 봅니다. 이 파일은 `[설명]`이므로 완성 코드를 살펴보겠습니다.

#v(paragraph-gap)
#emph[\[이미지 누락: \]] #emph[TokenTracker가 매 호출마다 토큰 수와 응답 시간을 기록하고, JSON 로거가 구조화된 로그를 남깁니다]

==== TokenTracker -- 호출별 사용량 기록

`monitoring.py`의 `TokenTracker` 클래스를 살펴봅니다.

```python
# monitoring.py — TokenTracker.record() (완성 코드)

    # 간략한 비용 기준 (달러/1000토큰, 참고용)
    COST_PER_1K_TOKENS = {
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "deepseek-r1:8b": {"input": 0.0, "output": 0.0},  # 로컬 모델: 무료
        "llama3.1:8b": {"input": 0.0, "output": 0.0},      # 로컬 모델: 무료
    }

    def record(self, model, input_tokens, output_tokens, operation="chat", latency_ms=0.0):
        """토큰 사용량을 기록합니다."""
        # 1. 모델별 비용 계산
        cost_usd = calculate_cost(model, input_tokens, output_tokens, self.COST_PER_1K_TOKENS)

        # 2. 레코드 저장
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": model,
            "operation": operation,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "cost_usd": cost_usd,
            "latency_ms": round(latency_ms, 2),
        }
        self._records.append(record)

        # 3. 누적 토큰 수 업데이트
        self._total_input_tokens += input_tokens
        self._total_output_tokens += output_tokens
```

`COST_PER_1K_TOKENS` 테이블에 모델별 단가가 들어 있습니다. `llama3.1:8b`는 로컬 모델이라 비용이 0입니다. `record()`를 호출할 때마다 토큰 수, 응답 시간, 비용이 한 줄씩 쌓입니다.

#v(paragraph-gap)
`summary()` 메서드는 `_monitoring_utils.py`의 `token_summary`를 호출해서 누적 통계(총 호출 수, 총 토큰, 평균 응답 시간)를 딕셔너리로 돌려줍니다.

==== setup\_logging -- JSON 구조화 로그

로그를 `print`로 찍으면 나중에 파싱이 어렵습니다. JSON 형식으로 남기면 로그 수집 도구가 바로 읽을 수 있습니다.

```python
# monitoring.py — setup_logging (완성 코드)

def setup_logging(level="INFO", use_json=True, log_file=None):
    """애플리케이션 로깅 시스템을 설정합니다."""
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    root_logger.handlers.clear()

    # JSON 포맷 또는 일반 포맷 선택
    if use_json:
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
```

`setup_logging(use_json=True)`로 설정하면 로그가 JSON 한 줄로 출력됩니다.

```json
{"timestamp": "2026-03-05T09:15:23Z", "level": "INFO", "logger": "src.agent_config", "message": "[ConnectHRAgent] 처리 완료 (경로: rag, 소요: 1523ms)"}
```

운영 환경에서 Elasticsearch나 CloudWatch 같은 시스템에 로그를 보낼 때 JSON 형식이 파싱하기 쉽습니다.

==== LangfuseMonitor (선택)

`LangfuseMonitor` 클래스는 외부 모니터링 도구인 #strong[Langfuse]와의 연동 래퍼입니다. `.env`에 `LANGFUSE_PUBLIC_KEY`와 `LANGFUSE_SECRET_KEY`를 설정하면 자동 활성화됩니다. 패키지가 설치되지 않아도 코드는 정상 동작합니다. 이 책에서는 TokenTracker의 로컬 기록에 집중하고, Langfuse 상세는 다루지 않습니다.

=== 2.7 실습 2: ConnectHRAgent -- 메모장과 일지를 단 운영용 에이전트 (agent\_config.py)

#emph[\[다이어그램: ConnectHRAgent (실습 2) → ResponseCache 조회 → QueryRouter 분류 → 경로별 실행 (RAG/Agent) → TokenTracker 기록 → ResponseCache 저장\]]

#v(paragraph-gap)
#emph[실습 2에서 전체 흐름을 하나로 조립합니다. 실습 1의 메모장과 설명 1의 업무 일지가 ConnectHRAgent 안에서 만납니다.]

#v(paragraph-gap)
실습 1에서 만든 메모장(ResponseCache)과 설명 1에서 살펴본 업무 일지(TokenTracker)를 하나의 에이전트로 조립합니다. ex06의 IntegratedAgent를 감싸서 운영에 필요한 안전장치를 모두 달아주는 작업입니다. `ex07/src/agent_config.py`를 열어 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

==== 준비된 코드 확인

import, 시스템 프롬프트(`SYSTEM_PROMPT`), `ConnectHRAgent` 클래스 선언과 `__init__`은 이미 파일에 준비되어 있습니다.

#v(paragraph-gap)
`__init__`에서 주목할 부분은 ex06에 없던 import입니다. `cache`에서 `response_cache`를, `monitoring`에서 `token_tracker`와 `langfuse_monitor`를 가져옵니다. 실습 1에서 만든 메모장과 설명 1에서 본 업무 일지를 여기서 불러오는 것입니다.

#v(paragraph-gap)
`_agent_utils.py`의 보조 함수도 확인해 봅니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([보조 함수], [파일], [역할],),
    table.hline(),
    [`build_agent_executor(llm, tools, prompt)`], [`_agent_utils.py`], [AgentExecutor를 구성. `max_iterations=10`, `max_execution_time=60` 적용],
    [`run_with_retry(executor, query, history)`], [`_agent_utils.py`], [최대 3회 재시도. 시도 간 2초 대기],
  )]
  , kind: table
  )

`build_agent_executor`가 만드는 AgentExecutor는 CH06과 같은 구조입니다. 달라진 점은 `max_iterations`\(최대 반복 10회)와 `max_execution_time`\(60초 타임아웃)을 상수로 분리해서 무한 루프나 과도한 실행을 방지한다는 것입니다.

#v(paragraph-gap)
`run_with_retry`가 재시도 매뉴얼입니다. 실패하면 2초 쉬고 다시 시도하고, 3번 모두 실패하면 에러 메시지를 반환합니다.

==== ConnectHRAgent.run() -- 캐시 조회부터 기록까지

`run` 메서드의 TODO를 채워 봅니다. 질문이 들어왔을 때 메모장을 먼저 확인하고, 없으면 서가에 가서 찾고, 결과를 업무 일지에 기록하고, 메모장에 적어두는 전체 흐름입니다.

```python
# agent_config.py — TODO: run — 캐시→라우팅→실행→추적→저장

    def run(self, query, chat_history=None, use_cache=True):
        """사용자 질문을 처리하고 답변을 반환합니다."""
        start_time = time.time()

        # 1. 메모장(캐시) 조회
        if use_cache:
            cached = response_cache.get(query)
            if cached is not None:
                cached["from_cache"] = True
                return cached

        # 2. QueryRouter로 경로 결정
        route = classify_route(query, router=self._router)

        # 3. 경로별 실행 — RAG 또는 Agent
        if route == "rag" and self.rag_chain is not None:
            try:
                answer = self.rag_chain.invoke(query)
                result = {
                    "output": answer,
                    "route": route,
                    "intermediate_steps": [],
                    "from_cache": False,
                }
            except Exception:
                result = run_with_retry(self.agent_executor, query, chat_history)
                result["route"] = "agent_fallback"
                result["from_cache"] = False
        elif self.agent_executor is not None:
            result = run_with_retry(self.agent_executor, query, chat_history)
            result["route"] = route
            result["from_cache"] = False
        else:
            result = {
                "output": "죄송합니다. 에이전트 서비스를 사용할 수 없습니다.",
                "route": "error",
                "intermediate_steps": [],
                "from_cache": False,
            }

        # 4. 업무 일지(TokenTracker)에 기록
        latency_ms = (time.time() - start_time) * 1000
        provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        if provider == "openai":
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        else:
            model = os.getenv("OLLAMA_MODEL", "deepseek-r1:8b")
        token_tracker.record(
            model=model,
            input_tokens=len(query.split()) * 2,
            output_tokens=len(result["output"].split()) * 2,
            operation="agent_run",
            latency_ms=latency_ms,
        )

        # 5. Langfuse 추적 전송 (선택)
        langfuse_monitor.trace(
            name="agent_run",
            input_data=query,
            output_data=result["output"],
            metadata={"route": result["route"], "latency_ms": latency_ms},
        )

        # 6. 메모장(캐시)에 저장
        if use_cache:
            response_cache.set(query, result)

        return result
```

`run()` 메서드의 흐름을 정리해 보면 이렇습니다.

#v(paragraph-gap)
#strong[1(캐시 조회)과 6(캐시 저장)] -- 실습 1에서 만든 ResponseCache가 여기서 동작합니다. 같은 질문이 캐시에 있으면 바로 반환하고, 새로운 답변은 캐시에 적어둡니다. 질문이 30번 반복되면 첫 번째만 LLM을 호출하고 나머지 29번은 메모장에서 읽어줍니다.

#v(paragraph-gap)
#strong[3(경로별 실행)] -- CH06에서 만든 QueryRouter가 질문을 분류하고, RAG 경로면 rag\_chain을 호출합니다. RAG가 실패하면 Agent로 폴백합니다. Agent 경로에서는 `run_with_retry`가 최대 3번까지 재시도합니다.

#v(paragraph-gap)
#strong[4(토큰 기록)] -- 설명 1에서 본 TokenTracker에 매 호출 기록을 남깁니다. `len(query.split()) * 2`는 한국어 기준 대략적인 토큰 추정치입니다. Ollama는 응답에 토큰 수를 포함하지 않기 때문에 추정값을 씁니다.

#v(paragraph-gap)
파일 하단의 싱글턴(`get_agent()`)은 이미 준비되어 있습니다. 어디서든 `get_agent()`를 호출하면 같은 ConnectHRAgent 인스턴스를 공유합니다.

=== 2.8 \[참고\] 도구 모듈화

ex06에서 `mcp_tools.py` 하나에 도구 4개가 몰려 있었습니다. ex07에서는 `tools/` 디렉토리 아래에 파일 하나당 도구 하나씩 분리했습니다.

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([파일], [도구], [역할],),
    table.hline(),
    [`tools/leave_balance.py`], [`get_leave_balance(name)`], [직원 연차 잔여 조회],
    [`tools/sales_sum.py`], [`get_sales_sum(department)`], [부서별 매출 합계 조회],
    [`tools/list_employees.py`], [`list_employees(department)`], [직원 목록 조회],
    [`tools/search_documents.py`], [`search_documents(query)`], [문서 벡터 검색],
  )]
  , kind: table
  )

기능은 CH06과 동일합니다. 도구가 늘어나면 파일만 추가하면 됩니다.

=== 2.9 실행 결과

코드 작성이 끝났습니다. 서버를 띄우고 메모장과 업무 일지가 실제로 동작하는지 확인해 보겠습니다.

```bash
python run.py
```

서버가 시작되면 브라우저에서 `http://localhost:8000`으로 접속합니다.

==== 1. 첫 질문 -- 에이전트가 도구를 호출한다

채팅창에 "김민준 연차 잔여일수 알려줘"를 입력해 봅니다. 터미널 로그를 위에서 아래로 따라가 보겠습니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH07/terminal/07_log-first-query.png", alt: [첫 질문 처리 흐름입니다. 에이전트가 도구를 호출하고, 업무 일지에 기록하고, 메모장에 적어둡니다.], max-width: 0.6)

#v(paragraph-gap)
+ #strong[질문 수신] -- ConnectHRAgent가 질문을 받습니다.
+ #strong[AgentExecutor 체인 시작] -- LLM이 질문을 분석하고 `get_leave_balance` 도구를 선택합니다.
+ #strong[도구 호출] -- DB에서 김민준의 연차를 조회합니다.
+ #strong[LLM 응답 생성] -- 조회 결과를 자연어 답변으로 만듭니다.
+ #strong[TokenTracker 기록] -- 토큰 수와 소요 시간을 업무 일지에 남깁니다.
+ #strong[ResponseCache 저장] -- 답변을 메모장에 적어둡니다. 3,600초 후 만료됩니다.

==== 2. 캐시 적중 -- 같은 질문엔 메모장에서 바로 답한다

같은 질문을 다시 입력해 봅니다. 터미널 로그가 확연히 달라집니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH07/terminal/07_log-cache-hit.png", alt: [같은 질문을 반복하면 메모장에서 즉시 반환합니다. LLM을 호출하지 않습니다.], max-width: 0.6)

#figure(
  align(center)[#table(
    columns: 3,
    align: (auto,auto,auto,),
    table.header([], [첫 질문], [캐시 적중],),
    table.hline(),
    [LLM 호출], [2회 (분석 + 생성)], [0회],
    [DB 조회], [1회], [0회],
    [소요 시간], [\~16초], [즉시],
    [로그], [AgentExecutor 체인 전체], [`[ResponseCache] 적중` 한 줄],
  )]
  , kind: table
  )

`잔여 TTL: 3386초` -- 메모장에 적힌 지 약 3분이 지났다는 뜻입니다(3600 - 3386 = 214초). TTL이 0이 되면 메모가 만료되고, 다음에 같은 질문이 들어오면 다시 서가에서 찾아옵니다.

==== 3. 상태 확인 대시보드

사이드바의 #strong["상태 확인"] 을 클릭합니다. 캐시 적중률과 토큰 사용량을 한눈에 볼 수 있습니다.

#v(paragraph-gap)
#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_v2/assets/CH07/terminal/07_stats-dashboard.png", alt: [상태 확인 페이지에서 캐시 적중률과 토큰 사용량을 확인합니다], max-width: 0.6)

#v(paragraph-gap)
세 가지 카드가 표시됩니다.

#v(paragraph-gap)
- #strong[서버 상태] -- 서버가 정상(ok)인지, 버전은 무엇인지 보여줍니다.
- #strong[응답 캐시 (ResponseCache)] -- 적중률 83.33%는 6번 질문 중 5번을 메모장에서 답했다는 뜻입니다. 미스(Miss) 1건은 첫 질문입니다.
- #strong[토큰 사용량 (TokenTracker)] -- 입력/출력 토큰 수와 추정 비용을 표시합니다. 로컬 모델(Ollama)은 비용이 \$0으로 표시됩니다.

#v(paragraph-gap)
이 대시보드는 `http://localhost:8000/api/stats` API의 JSON 데이터를 웹 UI로 시각화한 화면입니다.

#quote(block: true)[`Ctrl + C`를 눌러 서버를 종료해 주시기 바랍니다. Docker 컨테이너도 `docker compose down`으로 정리해 주시기 바랍니다.]

=== 2.10 더 알아보기

#strong[TTL을 얼마로 설정해야 합니까?]

#v(paragraph-gap)
사내 문서가 자주 갱신되면 짧게(30분), 변동이 거의 없으면 길게(24시간) 설정하시길 권장합니다. 기본값 1시간은 대부분의 사내 환경에 적합합니다. `.env` 파일에서 `CACHE_TTL=3600` 값을 조정할 수 있습니다.

#v(paragraph-gap)
#strong[ResponseCache가 메모리 기반이면 서버 재시작 시 사라지지 않습니까?]

#v(paragraph-gap)
그렇습니다. 운영 환경에서는 Redis 같은 외부 캐시를 사용하는 것이 일반적입니다. 이 책에서는 개념 이해를 위해 인메모리 구현체를 사용합니다. Redis로 변경하려면 `get()`과 `set()` 메서드를 Redis 클라이언트 호출로 교체하면 됩니다.

#v(paragraph-gap)
#strong[토큰 수가 추정값인 이유는 무엇입니까?]

#v(paragraph-gap)
Ollama는 응답에 토큰 사용량을 포함하지 않습니다. `단어 수 x 2`는 한국어 기준 대략적인 추정치입니다.

=== 2.11 이것만은 기억하세요

- #strong[같은 질문엔 메모장(캐시)으로 답합니다.] ResponseCache가 유통기한(TTL) 동안 답변을 기억해서 LLM 재호출을 막습니다.
- #strong[운영은 기록에서 시작합니다.] TokenTracker가 매 호출의 토큰 수와 응답 시간을 기록합니다. 기록이 쌓여야 개선할 수 있습니다.

#v(paragraph-gap)
다음 챕터에서는 이 에이전트의 #strong[검색 품질]을 개선합니다. "엉뚱한 문서를 가져온다"는 문제를 청킹 최적화와 리랭킹, 하이브리드 검색으로 해결해 봅니다.

#v(4pt)
#block(width: 100%, height: 0.5pt, fill: rgb("#e5e7eb"))
#v(4pt)
