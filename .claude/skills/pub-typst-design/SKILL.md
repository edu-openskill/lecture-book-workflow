---
name: typst-design
description: "Typst 템플릿의 타이포그래피, 페이지 설정, 스타일 규칙 관리"
---

# typst-design — Typst 템플릿 디자인

## 구조

| 파일 | 위치 | 역할 |
|------|------|------|
| `book_base.typ` | **스킬 소유** (`references/templates/`) | 범용 스타일 (폰트, 여백, heading, 코드, 표, 표지, 목차, auto-image) |
| `book.typ` | **프로젝트** (`book/templates/`) | 프로젝트별 설정 (제목, 부제, 설명, 헤더 제목) |

프로젝트의 `book.typ`에서 변수를 정의하고, 스킬의 `book_base.typ`이 그 변수를 사용한다.
빌드 엔진이 Python 레벨에서 `book.typ` → `book_base.typ` → 본문 순서로 concat한다.

## 역할

`book_base.typ`의 스타일 규칙을 관리한다.
새 프로젝트에서 `book.typ`만 작성하면 동일한 스타일을 재사용할 수 있다.

## 프로젝트 설정 변수 (book.typ)

```typst
#let book-title = "책 제목"
#let book-subtitle = "부제"
#let book-description = [설명 텍스트]
#let book-header-title = "헤더에 표시할 제목"
```

## 새 프로젝트에서 사용하기

1. `book/templates/book.typ` 작성 (위 4개 변수만)
2. `book/templates/book_base.typ` → 스킬 심볼릭 링크 생성
3. `python3 book/build_pdf_typst.py` 실행

## 컴포넌트 디자인 시스템

`book_base.typ`을 shared + variant 컴포넌트로 분해하여 믹스매치 가능.

```
components/
├── _shared/          # 디자인 공통 (page, variables, misc, image, cover)
├── _variant/         # 디자인별 (body/heading/code/inline_code/quote/table/toc × d1/d2)
└── presets.json      # 프리셋 정의 (1: 클래식 블루, 2: 컴팩트 모노)
```

| 카테고리 | Design 1 (클래식 블루) | Design 2 (컴팩트 모노) |
|---------|---------------------|---------------------|
| body | 10pt, leading 1.0em | 8pt, leading 8pt |
| heading | h1:26pt, h2:파란바 | h1:16pt, h2:심플 |
| code | 둥근 테두리 | 위아래 회색선 |
| inline_code | 회색 배경 박스 | 볼드만 |
| quote | 파란 좌측선 | 점선 박스 |
| table | 파란 헤더 | 회색 헤더 |
| toc | depth: 2 | depth: 3 |

카탈로그 PDF: `references/samples/component-catalog.pdf`

## 참조

- [typography.md](references/typography.md) — 타이포그래피 규칙 상세
