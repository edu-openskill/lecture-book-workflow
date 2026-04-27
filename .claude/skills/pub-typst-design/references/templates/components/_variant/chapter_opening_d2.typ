// ── 챕터 오프닝: Design 2 (컴팩트 모노) ──
// 최소 여백 + 작은 제목. 밀도 높은 배치 우선.
#show heading.where(level: 1): it => {
  chapter-title.update(it.body)
  pagebreak(weak: true)
  block(
    width: 100%,
    below: heading-gap,
    sticky: true,
    {
      text(16pt, weight: "bold", fill: rgb("#1a1a1a"))[#it.body]
      v(8pt)
      line(length: 100%, stroke: 3pt + rgb("#2563eb"))
    }
  )
  v(heading-gap)
}
