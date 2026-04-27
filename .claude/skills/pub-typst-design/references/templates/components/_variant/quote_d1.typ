// ── 인용 블록: Design 1 (파란 좌측선) ──
// ──OVERRIDES──
#show quote.where(block: true): it => {
  block(
    width: 100%,
    above: quote-margin-top,
    below: quote-margin-bottom,
    inset: (left: quote-inset-x, right: quote-inset-x, top: quote-inset-y, bottom: quote-inset-y),
    stroke: (left: quote-stroke-width + color-quote-border),
    fill: color-quote-bg,
    radius: (right: quote-radius),
    {
      set par(justify: true, leading: 0.9em)
      text(size: quote-size, fill: quote-text-color)[#it.body]
    }
  )
}

// ── callout-box 호환 정의 ──
#let callout-box(label, body) = {
  block(
    width: 100%,
    above: quote-margin-top,
    below: quote-margin-bottom,
    inset: (left: quote-inset-x, right: quote-inset-x, top: quote-inset-y, bottom: quote-inset-y),
    stroke: (left: quote-stroke-width + color-quote-border),
    fill: color-quote-bg,
    radius: (right: quote-radius),
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
