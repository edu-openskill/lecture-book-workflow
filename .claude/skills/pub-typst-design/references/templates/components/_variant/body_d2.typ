// ── 본문 스타일: Design 2 (컴팩트 모노) ──

// 변수 재정의 (Design 2 값)
#let body-leading = 8pt
#let body-tracking = 0pt
#let heading-gap = body-leading
#let code-inset-x = 16pt
#let code-inset-y = 6pt
#let code-rule-stroke = 2pt
// Design 2 제목/코드/목차 기본값
#let h1-size = 16pt
#let h2-size = 10pt
#let h3-size = 10pt
#let h4-size = 10pt
#let code-size = 6pt
#let toc-depth = 3
#let quote-size = 9pt
#let table-size = 8pt
#let inline-code-size = 8pt
// ──OVERRIDES──

#set text(
  font: ("RIDIBatang", "Apple SD Gothic Neo"),
  size: 8pt,
  lang: "ko",
  fill: color-text,
  tracking: body-tracking,
)

#set par(
  leading: if body-leading < 4pt { 4pt } else { body-leading },
  spacing: 0pt,
  first-line-indent: 0pt,
  justify: true,
)
