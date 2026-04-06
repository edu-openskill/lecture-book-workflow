// 조판 설정 변수 — 기본값은 Design 1 (클래식 블루)
// Design 2에서 body_d2.typ 상단에서 재정의. D1 파일은 값을 직접 사용 (기본값과 동일하므로)
// 소비자: _variant/body_d2.typ(재정의), _variant/heading_d2.typ, _variant/code_d2.typ

// 행간: 줄과 줄 사이 간격
#let body-leading = 1.0em
// 문단 간격: 문단과 문단 사이 간격 (heading/code/table에는 영향 없음)
#let paragraph-gap = 0pt
// 자간: 글자와 글자 사이 간격 (0pt = 기본)
#let body-tracking = 0pt
// 제목-문단 간격: 제목 아래 본문까지의 여백
#let heading-gap = 16pt
// 코드 블록: 구분선과 코드 사이 여백
#let code-inset-x = 16pt
#let code-inset-y = 14pt
// 코드 블록: 구분선 두께
#let code-rule-stroke = 1pt
// 코드 블록: 위아래 여백 — componentStyles 오버라이드 대상
#let code-margin-top = 8pt
#let code-margin-bottom = 8pt

// 제목 크기 — 에디터 오버라이드 대상
#let h1-size = 26pt
#let h2-size = 16pt
#let h3-size = 13pt
#let h4-size = 11pt
// 코드 블록 크기 — 에디터 오버라이드 대상
#let code-size = 8pt
// 인용/표/인라인코드 크기 — 에디터 오버라이드 대상
#let quote-size = 9pt
#let table-size = 8.5pt
#let inline-code-size = 8.5pt
// 목차 깊이 — 에디터 오버라이드 대상
#let toc-depth = 2
// 목차 항목 간격 — 에디터 오버라이드 대상 (문단 간격과 독립)
#let toc-spacing = 4pt

// 색상 변수 — 에디터 오버라이드 대상
#let color-primary = rgb("#2563eb")
#let color-primary-dark = rgb("#1e40af")
#let color-primary-light = rgb("#93c5fd")
#let color-text = rgb("#1a1a1a")
#let color-code-text = rgb("#1e40af")
#let color-quote-bg = rgb("#f5f8ff")
#let color-quote-border = rgb("#93b4e8")

// 제목 스타일 변수 — componentStyles 오버라이드 대상 (기본값 = Design 1)
// 색상 변수 뒤에 위치해야 함 (color-text, color-primary-dark 참조)
#let h1-top = 10pt
#let h1-weight = "bold"
#let h1-fill = color-text
#let h1-below = 14pt
#let h2-top = 24pt
#let h2-below = 14pt
#let h2-weight = "bold"
#let h2-fill = color-primary-dark
#let h2-inset-left = 12pt
#let h3-top = 16pt
#let h3-below = 14pt
#let h3-weight = "semibold"
#let h3-fill = rgb("#1e3a5f")
#let h4-top = 12pt
#let h4-below = 14pt
#let h4-weight = "semibold"
#let h4-fill = rgb("#374151")

// 본문 스타일 변수 — componentStyles 오버라이드 대상
#let strong-fill = rgb("#1e3a5f")
#let emph-fill = rgb("#6b7280")

// 코드블록 스타일 변수
#let code-fill = white
#let code-radius = 8pt
#let code-stroke-width = 1pt
#let code-stroke-color = rgb("#d1d5db")

// 인라인코드 스타일 변수
#let inline-code-fill = rgb("#f3f4f6")
#let inline-code-radius = 3pt
#let inline-code-text-color = color-code-text
#let inline-code-weight = "bold"

// 인용 스타일 변수
#let quote-text-color = rgb("#4b5563")
#let quote-stroke-width = 3pt
#let quote-inset-x = 14pt
#let quote-inset-y = 10pt
#let quote-radius = 4pt
#let quote-margin = 10pt
#let quote-margin-top = 10pt
#let quote-margin-bottom = 10pt

// 표 스타일 변수
#let table-stroke-width = 0.5pt
#let table-stroke-color = rgb("#e5e7eb")
#let table-inset-x = 10pt
#let table-inset-y = 8pt
#let table-header-weight = "medium"
#let table-header-text-color = white
#let table-odd-fill = rgb("#f8fafc")
#let table-margin-top = 0pt
#let table-margin-bottom = 0pt

// 목차 스타일 변수
#let toc-title-size = 24pt
#let toc-title-weight = "bold"
#let toc-title-line-stroke = 3pt
#let toc-level1-size = 11pt
#let toc-level3-size = 8.5pt
#let toc-level3-color = rgb("#6b7280")
#let toc-indent = 1.5em

// Figure 캡션 변수
#let figure-margin-top = 8pt
#let figure-margin-bottom = 4pt
#let figure-caption-gap = 2pt
#let figure-caption-size = 8pt
#let figure-caption-color = rgb("#6b7280")

// 이미지 설정 변수 — 에디터 오버라이드 대상
#let img-gemini-width = 0.7
#let img-gemini-style = "bordered"
#let img-terminal-width = 0.7
#let img-terminal-style = "minimal"
#let img-diagram-width = 0.6
#let img-diagram-style = "minimal"
#let img-default-width = 0.6
#let img-default-style = "plain"
