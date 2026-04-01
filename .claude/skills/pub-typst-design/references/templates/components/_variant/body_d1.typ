// ── 본문 스타일: Design 1 (클래식 블루) ──
// ──OVERRIDES──
#set text(
  font: ("RIDIBatang", "Apple SD Gothic Neo"),
  size: 10pt,
  lang: "ko",
  fill: color-text,
)

#set par(
  leading: if body-leading < 4pt { 4pt } else { body-leading },
  spacing: 0pt,
  first-line-indent: 0pt,
  justify: true,
)
