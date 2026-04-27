// ── 이미지 테두리 프리셋 샘플 ──
// 각 프리셋이 적용된 이미지를 비교할 수 있는 미리보기 파일.
// 사용법: typst compile image-border-samples.typ image-border-samples.pdf --root /
//
// 실제 이미지 경로를 sample-image 변수에 지정하세요.
// 이미지가 없으면 placeholder rect로 대체됩니다.

#set page(
  width: 188mm,
  height: 257mm,
  margin: (top: 20mm, bottom: 28mm, left: 20mm, right: 20mm),
)

#set text(
  font: ("RIDIBatang", "Apple SD Gothic Neo"),
  size: 10pt,
  lang: "ko",
  fill: rgb("#1a1a1a"),
)

// ── auto-image 함수 (book_base.typ에서 복사) ──
#let auto-image(path, alt: none, max-width: 0.7, style: "plain") = layout(size => context {
  let target-width = size.width * max-width
  let img = image(path, width: target-width)
  let img-size = measure(img)
  let caption-h = if alt != none { 28pt } else { 0pt }
  let needed = img-size.height + caption-h + 24pt

  let final-width = if needed > size.height and size.height > 120pt {
    let available = size.height - caption-h - 24pt
    let ratio = available / img-size.height
    if ratio >= 0.5 {
      target-width * ratio
    } else {
      target-width
    }
  } else {
    target-width
  }

  let styled-img = if style == "bordered" {
    block(
      stroke: 2pt + rgb("#2563eb"),
      radius: 4pt,
      clip: true,
      image(path, width: final-width)
    )
  } else if style == "shadow" {
    block(
      stroke: (
        left: 0.5pt + rgb("#e0e0e0"),
        top: 0.5pt + rgb("#e0e0e0"),
        right: 2pt + rgb("#c0c0c0"),
        bottom: 2pt + rgb("#c0c0c0"),
      ),
      radius: 4pt,
      clip: true,
      image(path, width: final-width)
    )
  } else if style == "bordered-shadow" {
    block(
      stroke: (
        left: 2pt + rgb("#2563eb"),
        top: 2pt + rgb("#2563eb"),
        right: 3pt + rgb("#1d4ed8"),
        bottom: 3pt + rgb("#1d4ed8"),
      ),
      radius: 4pt,
      clip: true,
      image(path, width: final-width)
    )
  } else if style == "minimal" {
    block(
      stroke: 0.5pt + rgb("#e5e7eb"),
      radius: 2pt,
      clip: true,
      image(path, width: final-width)
    )
  } else {
    image(path, width: final-width)
  }

  if alt != none {
    figure(styled-img, caption: [#alt])
  } else {
    align(center, styled-img)
  }
})

// ── 샘플 이미지 경로 (실제 프로젝트 이미지로 교체) ──
// 아래 경로를 실제 이미지 절대경로로 변경하세요.
#let sample-image = ""

// ══════════════════════════════════════
// 표지
// ══════════════════════════════════════
#align(center)[
  #v(60pt)
  #text(24pt, weight: "bold")[이미지 테두리 프리셋 샘플]
  #v(8pt)
  #line(length: 60%, stroke: 2pt + rgb("#2563eb"))
  #v(16pt)
  #text(12pt, fill: rgb("#6b7280"))[
    각 프리셋이 적용된 이미지를 비교하여 원하는 디자인을 선택하세요.
  ]
  #v(8pt)
  #text(10pt, fill: rgb("#9ca3af"))[
    sample-image 변수에 실제 이미지 경로를 지정한 후 컴파일하세요.
  ]
]

#v(40pt)

// ── 프리셋 목록 ──
#table(
  columns: (1fr, 2fr, 2fr),
  table.header(
    [프리셋], [개념도 (gemini)], [나머지 (terminal/diagram)],
  ),
  [*clean-border*], [bordered: 2pt #2563eb + radius 4pt], [minimal: 0.5pt #e5e7eb + radius 2pt],
  [*shadow*], [shadow: 비대칭 stroke], [shadow: 비대칭 stroke],
  [*primary-shadow*], [bordered-shadow: 프라이머리+그림자], [shadow: 비대칭 stroke],
  [*minimal*], [minimal: 0.5pt #e5e7eb], [minimal: 0.5pt #e5e7eb],
)

#pagebreak()

// ══════════════════════════════════════
// 프리셋 1: plain (기본값, 효과 없음)
// ══════════════════════════════════════
#text(16pt, weight: "bold")[프리셋: plain]
#v(4pt)
#text(10pt, fill: rgb("#6b7280"))[효과 없음. 기존 동작과 동일합니다.]
#v(12pt)

#if sample-image != "" {
  auto-image(sample-image, alt: [plain — 효과 없음], max-width: 0.6, style: "plain")
} else {
  align(center, block(
    width: 60%,
    height: 120pt,
    fill: rgb("#f3f4f6"),
    radius: 4pt,
    align(center + horizon, text(fill: rgb("#9ca3af"))[이미지 경로를 지정하세요])
  ))
}

#v(24pt)

// ══════════════════════════════════════
// 프리셋 2: bordered (프라이머리 컬러 테두리)
// ══════════════════════════════════════
#text(16pt, weight: "bold")[스타일: bordered]
#v(4pt)
#text(10pt, fill: rgb("#6b7280"))[2pt 프라이머리 컬러(#2563eb) 테두리 + radius 4pt. 개념도에 적합.]
#v(12pt)

#if sample-image != "" {
  auto-image(sample-image, alt: [bordered — 프라이머리 테두리], max-width: 0.6, style: "bordered")
} else {
  align(center, block(
    width: 60%,
    height: 120pt,
    fill: rgb("#f3f4f6"),
    stroke: 2pt + rgb("#2563eb"),
    radius: 4pt,
    align(center + horizon, text(fill: rgb("#2563eb"))[bordered 스타일 미리보기])
  ))
}

#v(24pt)

// ══════════════════════════════════════
// 프리셋 3: shadow (그림자 효과)
// ══════════════════════════════════════
#text(16pt, weight: "bold")[스타일: shadow]
#v(4pt)
#text(10pt, fill: rgb("#6b7280"))[오른쪽/아래 두꺼운 stroke로 입체감. 터미널 캡처, 다이어그램에 적합.]
#v(12pt)

#if sample-image != "" {
  auto-image(sample-image, alt: [shadow — 그림자 효과], max-width: 0.6, style: "shadow")
} else {
  align(center, block(
    width: 60%,
    height: 120pt,
    fill: rgb("#f3f4f6"),
    stroke: (
      left: 0.5pt + rgb("#e0e0e0"),
      top: 0.5pt + rgb("#e0e0e0"),
      right: 2pt + rgb("#c0c0c0"),
      bottom: 2pt + rgb("#c0c0c0"),
    ),
    radius: 4pt,
    align(center + horizon, text(fill: rgb("#6b7280"))[shadow 스타일 미리보기])
  ))
}

#v(24pt)

// ══════════════════════════════════════
// 프리셋 4: bordered-shadow (테두리 + 그림자)
// ══════════════════════════════════════
#text(16pt, weight: "bold")[스타일: bordered-shadow]
#v(4pt)
#text(10pt, fill: rgb("#6b7280"))[프라이머리 테두리 + 오른쪽/아래 진한 그림자. 강조가 필요한 개념도에 적합.]
#v(12pt)

#if sample-image != "" {
  auto-image(sample-image, alt: [bordered-shadow — 테두리 + 그림자], max-width: 0.6, style: "bordered-shadow")
} else {
  align(center, block(
    width: 60%,
    height: 120pt,
    fill: rgb("#f3f4f6"),
    stroke: (
      left: 2pt + rgb("#2563eb"),
      top: 2pt + rgb("#2563eb"),
      right: 3pt + rgb("#1d4ed8"),
      bottom: 3pt + rgb("#1d4ed8"),
    ),
    radius: 4pt,
    align(center + horizon, text(fill: rgb("#2563eb"))[bordered-shadow 스타일 미리보기])
  ))
}

#pagebreak()

// ══════════════════════════════════════
// 프리셋 5: minimal (얇은 회색 테두리)
// ══════════════════════════════════════
#text(16pt, weight: "bold")[스타일: minimal]
#v(4pt)
#text(10pt, fill: rgb("#6b7280"))[0.5pt 얇은 회색 테두리 + radius 2pt. 가장 가벼운 스타일.]
#v(12pt)

#if sample-image != "" {
  auto-image(sample-image, alt: [minimal — 얇은 테두리], max-width: 0.6, style: "minimal")
} else {
  align(center, block(
    width: 60%,
    height: 120pt,
    fill: rgb("#f3f4f6"),
    stroke: 0.5pt + rgb("#e5e7eb"),
    radius: 2pt,
    align(center + horizon, text(fill: rgb("#9ca3af"))[minimal 스타일 미리보기])
  ))
}

#v(40pt)

// ══════════════════════════════════════
// 프리셋 조합 비교 (나란히)
// ══════════════════════════════════════
#text(16pt, weight: "bold")[프리셋 조합 비교]
#v(4pt)
#text(10pt, fill: rgb("#6b7280"))[각 프리셋이 개념도/나머지에 적용하는 스타일 조합.]
#v(16pt)

#table(
  columns: (1fr, 1fr),
  table.header([개념도 (gemini/)], [나머지 (terminal/diagram/)]),

  // clean-border
  block(inset: 8pt)[
    #text(9pt, weight: "bold")[clean-border]
    #v(4pt)
    #block(width: 100%, height: 60pt, fill: rgb("#f3f4f6"),
      stroke: 2pt + rgb("#2563eb"), radius: 4pt,
      align(center + horizon, text(8pt, fill: rgb("#2563eb"))[bordered]))
  ],
  block(inset: 8pt)[
    #text(9pt, weight: "bold")[clean-border]
    #v(4pt)
    #block(width: 100%, height: 60pt, fill: rgb("#f3f4f6"),
      stroke: 0.5pt + rgb("#e5e7eb"), radius: 2pt,
      align(center + horizon, text(8pt, fill: rgb("#9ca3af"))[minimal]))
  ],

  // shadow
  block(inset: 8pt)[
    #text(9pt, weight: "bold")[shadow]
    #v(4pt)
    #block(width: 100%, height: 60pt, fill: rgb("#f3f4f6"),
      stroke: (left: 0.5pt + rgb("#e0e0e0"), top: 0.5pt + rgb("#e0e0e0"),
               right: 2pt + rgb("#c0c0c0"), bottom: 2pt + rgb("#c0c0c0")),
      radius: 4pt,
      align(center + horizon, text(8pt, fill: rgb("#6b7280"))[shadow]))
  ],
  block(inset: 8pt)[
    #text(9pt, weight: "bold")[shadow]
    #v(4pt)
    #block(width: 100%, height: 60pt, fill: rgb("#f3f4f6"),
      stroke: (left: 0.5pt + rgb("#e0e0e0"), top: 0.5pt + rgb("#e0e0e0"),
               right: 2pt + rgb("#c0c0c0"), bottom: 2pt + rgb("#c0c0c0")),
      radius: 4pt,
      align(center + horizon, text(8pt, fill: rgb("#6b7280"))[shadow]))
  ],

  // primary-shadow
  block(inset: 8pt)[
    #text(9pt, weight: "bold")[primary-shadow]
    #v(4pt)
    #block(width: 100%, height: 60pt, fill: rgb("#f3f4f6"),
      stroke: (left: 2pt + rgb("#2563eb"), top: 2pt + rgb("#2563eb"),
               right: 3pt + rgb("#1d4ed8"), bottom: 3pt + rgb("#1d4ed8")),
      radius: 4pt,
      align(center + horizon, text(8pt, fill: rgb("#2563eb"))[bordered-shadow]))
  ],
  block(inset: 8pt)[
    #text(9pt, weight: "bold")[primary-shadow]
    #v(4pt)
    #block(width: 100%, height: 60pt, fill: rgb("#f3f4f6"),
      stroke: (left: 0.5pt + rgb("#e0e0e0"), top: 0.5pt + rgb("#e0e0e0"),
               right: 2pt + rgb("#c0c0c0"), bottom: 2pt + rgb("#c0c0c0")),
      radius: 4pt,
      align(center + horizon, text(8pt, fill: rgb("#6b7280"))[shadow]))
  ],

  // minimal
  block(inset: 8pt)[
    #text(9pt, weight: "bold")[minimal]
    #v(4pt)
    #block(width: 100%, height: 60pt, fill: rgb("#f3f4f6"),
      stroke: 0.5pt + rgb("#e5e7eb"), radius: 2pt,
      align(center + horizon, text(8pt, fill: rgb("#9ca3af"))[minimal]))
  ],
  block(inset: 8pt)[
    #text(9pt, weight: "bold")[minimal]
    #v(4pt)
    #block(width: 100%, height: 60pt, fill: rgb("#f3f4f6"),
      stroke: 0.5pt + rgb("#e5e7eb"), radius: 2pt,
      align(center + horizon, text(8pt, fill: rgb("#9ca3af"))[minimal]))
  ],
)
