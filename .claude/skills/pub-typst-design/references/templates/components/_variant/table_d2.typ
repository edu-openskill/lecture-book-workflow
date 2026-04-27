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
