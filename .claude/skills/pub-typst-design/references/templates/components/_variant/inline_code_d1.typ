// ── 인라인 코드: Design 1 (회색 배경 박스) ──
// ──OVERRIDES──
#show raw.where(block: false): it => {
  box(
    fill: inline-code-fill,
    inset: (x: 4pt, y: 2pt),
    radius: inline-code-radius,
    text(fill: inline-code-text-color, font: ("D2Coding", "RIDIBatang"))[#it]
  )
}
