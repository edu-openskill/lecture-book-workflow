// ── 볼드/이탤릭 ──
// ──OVERRIDES──
#show strong: set text(fill: strong-fill)
#show emph: set text(fill: emph-fill)

// ── 수평선은 후처리에서 #v + block으로 변환됨 ──

// ── figure 스타일 (표/이미지 공통) ──
// above/below를 명시하여 par(spacing)의 영향 차단
#show figure: it => {
  block(above: figure-margin-top, below: figure-margin-bottom)[
    #align(center, it.body)
    #if it.caption != none {
      v(figure-caption-gap)
      let ch = counter(heading.where(level: 1)).get().first()
      let fig-num = counter(figure).display()
      align(center, text(figure-caption-size, fill: figure-caption-color)[그림 #ch\-#fig-num: #it.caption.body])
    }
  ]
}

// ── 링크 스타일 ──
#show link: it => {
  text(fill: color-primary)[#it]
}
