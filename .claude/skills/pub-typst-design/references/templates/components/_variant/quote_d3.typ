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
