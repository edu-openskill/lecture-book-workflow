// ── 인라인 코드: Design 2 (볼드 텍스트만) ──
#let inline-code-fill = none
#let inline-code-radius = 0pt
#let inline-code-text-color = rgb("#1e3a5f")
// ──OVERRIDES──
#show raw.where(block: false): it => {
  text(weight: inline-code-weight, fill: inline-code-text-color)[#it]
}
