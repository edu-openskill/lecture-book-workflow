// ── 표 스타일: Design 1 (파란 헤더, 흰 글씨) ──
// ──OVERRIDES──
#set table(
  stroke: (bottom: table-stroke-width + table-stroke-color),
  inset: (x: table-inset-x, y: table-inset-y),
  fill: (_, y) => if y == 0 { color-primary-dark } else if calc.odd(y) { table-odd-fill } else { white },
)

#show table.cell.where(y: 0): set text(fill: table-header-text-color, weight: table-header-weight)

#show table: it => {
  set text(size: table-size)
  block(above: table-margin-top, below: table-margin-bottom, breakable: true)[#it]
}
