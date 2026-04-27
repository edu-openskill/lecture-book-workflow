// ── 코드 블록: Design 2 (위아래 회색 실선) ──
#let code-fill = white
#let code-radius = 0pt
#let code-stroke-width = 0pt
#let code-stroke-color = white
// ──OVERRIDES──
#show raw.where(block: true): it => {
  set text(size: code-size, weight: "bold", font: ("D2Coding", "RIDIBatang"))
  let mt = if code-margin-top < 4pt { 4pt } else { code-margin-top }
  let mb = if code-margin-bottom < 4pt { 4pt } else { code-margin-bottom }
  block(above: mt, below: mb, width: 100%, breakable: true)[
    #line(length: 100%, stroke: code-rule-stroke + rgb("#999999"))
    #block(
      width: 100%,
      fill: code-fill,
      inset: (x: code-inset-x, y: code-inset-y),
      radius: code-radius,
      stroke: none,
      text(fill: color-text)[#it]
    )
    #line(length: 100%, stroke: code-rule-stroke + rgb("#999999"))
  ]
}
