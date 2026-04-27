// ── 인용 블록: Design 2 (점선 박스) ──
#let quote-text-color = rgb("#333333")
#let quote-stroke-width = 1pt
#let quote-radius = 0pt
// ──OVERRIDES──
#show quote.where(block: true): it => {
  block(
    width: 100%,
    above: quote-margin-top,
    below: quote-margin-bottom,
    inset: (x: quote-inset-x, y: quote-inset-y),
    stroke: (
      dash: "dashed",
      paint: rgb("#aaaaaa"),
      thickness: quote-stroke-width,
    ),
    radius: quote-radius,
    {
      set par(justify: true, leading: 0.9em)
      text(size: quote-size, fill: quote-text-color)[#it.body]
    }
  )
}

// ── callout-box (회색 박스 + 프라이머리 라벨) ──
#let callout-box(label, body) = {
  block(
    width: 100%,
    above: quote-margin-top,
    below: quote-margin-bottom,
    inset: (x: quote-inset-x, y: quote-inset-y),
    fill: rgb("#f5f5f5"),
    radius: 4pt,
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
