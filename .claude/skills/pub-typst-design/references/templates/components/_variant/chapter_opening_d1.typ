// ── 챕터 오프닝: Design 1 (클래식 블루) ──
// 넓은 상단 여백 + 큰 제목 + 파란 밑줄. 출판 표준의 여유로운 오프닝.
#show heading.where(level: 1): it => {
  chapter-title.update(it.body)
  pagebreak(weak: true)
  v(60pt)  // 상단 1/3 여백 (출판 표준)
  block(
    width: 100%,
    below: 16pt,
    sticky: true,
    {
      text(26pt, weight: "bold", fill: rgb("#1a1a1a"))[#it.body]
      v(8pt)
      line(length: 100%, stroke: 3pt + rgb("#2563eb"))
    }
  )
  v(14pt)
}
