# 타이포그래피 규칙

> 기준: 국내 IT 출판사 관행 + 해외 기술 서적 표준 (docs/book-design-guide.md 참조)

## 페이지 설정

| 항목 | 값 | 근거 |
|------|-----|------|
| 판형 | **46배판 (188x257mm)** | 국내 IT 서적 사실상 표준 |
| 상단 여백 | 20mm | 출판 표준 15~20mm |
| 하단 여백 | 28mm | 아래 > 위 (시각적 안정감) |
| 안쪽 여백 (Gutter) | 25mm | 제본 여백 포함 (22~28mm) |
| 바깥쪽 여백 | 16mm | 안쪽 > 바깥쪽 (비대칭) |
| 줄간격 | 1.0em (≈본문 크기의 200%) | 권장 140~200%, 가독성 확보 |
| 양쪽 정렬 | true | 출판 표준 |
| 첫 줄 들여쓰기 | 0pt | 기술서적 관행 |

## 폰트 체계

| 용도 | 폰트 | 크기 | 비고 |
|------|------|------|------|
| 본문 | KoPubDotum_Pro, Apple SD Gothic Neo | 10pt | IT 서적 표준 9.5~10.5pt |
| h1 (챕터) | Bold | 26pt | 본문 대비 2.6x (권장 2.5~3x) |
| h2 (섹션) | Bold | 16pt | 본문 대비 1.6x (권장 1.6~2x) |
| h3 (소제목) | SemiBold | 13pt | 본문 대비 1.3x (권장 1.2~1.4x) |
| h4 (하위제목) | SemiBold | 11pt | 본문 대비 1.1x (권장 1~1.2x) |
| 코드 블록 | Menlo, KoPubDotum_Pro | 8pt | 본문보다 2pt 작게 (권장 8~9pt) |
| 인라인 코드 | Menlo, KoPubDotum_Pro | 8.5pt | 연회색 배경 |
| 캡션 | KoPubDotum_Pro | 8pt | 회색(#6b7280) |
| 헤더 | KoPubDotum_Pro | 8pt | 회색(#999999) |
| 푸터 | KoPubDotum_Pro | 9pt | 회색(#888888) |

## 헤더 (머릿말)

- **좌측**: 책 제목 (book-header-title 변수)
- **우측**: 현재 챕터명 (h1 state 추적)
- **구분선**: 0.3pt 연회색
- **표지/목차**: 숨김 (page-num > 2일 때만 표시)

## 푸터

- 하단 중앙, 페이지 번호
- 표지/목차: 숨김

## heading 규칙

### h1 (챕터 오프닝)

| 요소 | 값 | 근거 |
|------|-----|------|
| 상단 여백 | 60pt | 페이지 상단 1/3 비움 (출판 표준) |
| 제목 크기 | 26pt Bold | |
| 밑줄 | 3pt 파란선 | |
| 하단 간격 | 14pt | |
| pagebreak | weak: true | 항상 새 페이지에서 시작 |
| sticky | true | 고아 방지 |

### h2~h4

- 모두 `sticky: true`로 heading이 페이지 하단에 혼자 남지 않도록 방지
- **제목 위 여백 > 아래 여백** (소속 관계 표현)
  - h2: 위 24pt, 아래 8pt+6pt
  - h3: 위 16pt, 아래 6pt+4pt
  - h4: 위 12pt, 아래 4pt+2pt

## 코드 블록

```typst
fill: white                      // 흰 배경
stroke: 1pt + rgb("#d1d5db")     // 회색 테두리
inset: (x: 16pt, y: 14pt)       // 패딩 5~8mm
radius: 8pt
breakable: true                  // 긴 코드도 페이지를 넘길 수 있음
weight: "bold"                   // 볼드 텍스트
text(fill: rgb("#1a1a1a"))       // 어두운 텍스트
```

**breakable: true** — 긴 코드 블록이 페이지 하단에서 잘리지 않고 빈 공간을 만드는 문제 해결.

## 인용 블록 (blockquote)

```typst
above/below: 10pt                       // 본문과 간격 (권장 10~15mm)
inset: (left/right: 14pt, top/bottom: 10pt)  // 내부 패딩
stroke: (left: 3pt + rgb("#93b4e8"))    // 파란 좌측 바
fill: rgb("#f5f8ff")                     // 연파란 배경
text(size: 9pt, fill: rgb("#4b5563"))    // 작은 회색 텍스트
leading: 0.9em                           // 인용 전용 행간
```

## 표 스타일

- 헤더 행: 파란 배경(#1e40af) + 흰 텍스트
- 홀수 행: 연회색(#f8fafc)
- 짝수 행: 흰색
- 테두리: 하단만 연회색 0.5pt

## 볼드/이탤릭

- **볼드**: 네이비(#1e3a5f)
- *이탤릭*: 회색(#6b7280)

## 표지

```typst
#page(numbering: none, header: none, footer: none)[
  book-title (42pt, 파란 볼드)     // 프로젝트 변수
  book-subtitle (15pt)              // 프로젝트 변수
  book-description (10.5pt, 회색)   // 프로젝트 변수
]
```

## 목차

**주의**: 목차에서 `#heading`을 사용하면 h1 show rule의 `pagebreak(weak: true)`가 트리거되어 빈 페이지 발생. 반드시 직접 텍스트 스타일링 사용:

```typst
// 올바른 방법
text(24pt, weight: "bold")[목차]

// 잘못된 방법 (빈 페이지 생성)
#heading(outlined: false, level: 1)[목차]
```

## 이미지 배치 기준

| 항목 | 값 |
|------|-----|
| 이미지-텍스트 간격 | 상하 8pt |
| 캡션 스타일 | 8pt, 회색(#6b7280), 중앙 정렬 |
| 캡션-이미지 간격 | 2pt |
| 캡션 형식 | "그림 N-M: 설명" |
| auto-image 기본 max-width | 0.7 (70%) |
| side-image 기본 img-width | 0.35 (35%) |

## 이미지 테두리 프리셋

`auto-image`의 `style` 파라미터로 이미지 테두리를 제어한다. 프로젝트 CONFIG의 `image_border_preset` 값에 따라 Python 빌드 스크립트가 경로 패턴별로 style을 자동 주입한다.

### style 값

| style | 시각 효과 | Typst 구현 |
|-------|----------|-----------|
| `"plain"` | 효과 없음 (기본값) | `image(path, width: ...)` |
| `"bordered"` | 프라이머리 컬러 테두리 | `stroke: 2pt + #2563eb, radius: 4pt` |
| `"shadow"` | 오른쪽/아래 그림자 | 비대칭 stroke (우/하 2pt #c0c0c0) |
| `"bordered-shadow"` | 프라이머리 테두리 + 그림자 | 비대칭 stroke (우/하 3pt #1d4ed8) |
| `"minimal"` | 얇은 회색 테두리 | `stroke: 0.5pt + #e5e7eb, radius: 2pt` |

### 프리셋 (경로→style 매핑)

| 프리셋 | 개념도 (gemini/) | 나머지 (terminal/diagram/) |
|--------|-----------------|--------------------------|
| `clean-border` | bordered | minimal |
| `shadow` | shadow | shadow |
| `primary-shadow` | bordered-shadow | shadow |
| `minimal` | minimal | minimal |
| `plain` | plain | plain |

### 적용 방법

프로젝트 `build_pdf_typst.py`의 CONFIG에 추가:
```python
CONFIG = {
    ...
    "image_border_preset": "clean-border",  # 프리셋명
}
```

### 샘플

프리셋 비교 샘플: `skills/pub-typst-design/references/samples/image-border-samples.typ`
