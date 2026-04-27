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
