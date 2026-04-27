// ══════════════════════════════════════
// 목차: Design 2 (depth: 3)
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
