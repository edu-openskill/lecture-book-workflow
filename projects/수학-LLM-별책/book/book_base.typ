// ── 범용 북 템플릿 (Typst) ──
// 원본: 스킬(pub-typst-design) 소유. 이 사본은 Windows 폰트(Noto Sans KR / Malgun Gothic)로 조정됨.
// 프로젝트의 book.typ에서 정의한 변수(book-title 등)를 사용합니다.

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

// ── 폰트 설정 (Windows: Noto Sans KR / Malgun Gothic) ──
#set text(
  font: ("Noto Sans KR", "Malgun Gothic"),
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
  set text(size: 8pt, weight: "bold", font: ("Consolas", "Noto Sans KR"))
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
    text(size: 8.5pt, fill: rgb("#1e40af"), font: ("Consolas", "Noto Sans KR"))[#it]
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
#let auto-image(path, alt: none, max-width: 0.7) = layout(size => context {
  let target-width = size.width * max-width
  let img = image(path, width: target-width)
  let img-size = measure(img)
  let caption-h = if alt != none { 28pt } else { 0pt }
  let needed = img-size.height + caption-h + 24pt

  let final-width = if needed > size.height and size.height > 120pt {
    let available = size.height - caption-h - 24pt
    let ratio = available / img-size.height
    if ratio >= 0.5 {
      target-width * ratio
    } else {
      target-width
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
    #line(length: 40%, stroke: 2pt + rgb("#2563eb"))
    #v(24pt)
    #text(32pt, weight: "bold", fill: rgb("#1e40af"), tracking: 1pt)[#book-title]
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
    #text(9pt, fill: rgb("#94a3b8"))[#book-tagline]
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
