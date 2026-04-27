# PDF 빌드 가이드 (Typst)

## 파이프라인 상세

### 1단계: 전처리 (Python)

기존 `build_pdf.py`와 동일한 전처리 로직을 사용합니다.

- **HTML 주석 제거**: `<!-- [GEMINI PROMPT ...] -->`, `<!-- [CAPTURE NEEDED ...] -->`, 기타 주석
- **이미지 경로 변환**: 마크다운 상대경로 → 절대경로 (Typst가 file:// 없이 절대경로로 이미지를 찾음)
- **Mermaid 렌더링**: `npx @mermaid-js/mermaid-cli`로 코드블록 → PNG 변환, `_mermaid_images/` 폴더에 저장

### 2단계: Pandoc 변환

```bash
pandoc input.md -f markdown+pipe_tables+fenced_code_blocks -t typst -o output.typ --wrap=none
```

- `--wrap=none`: 한국어 줄바꿈 방지
- 코드 블록의 언어 태그가 Typst에 그대로 전달되어 구문 하이라이팅에 사용됨

### 3단계: 후처리

Pandoc의 Typst 출력에서 알려진 문제를 수정합니다.

| 문제 | 원인 | 수정 |
|------|------|------|
| `!#link("path")[alt]` | Pandoc 이미지 변환 버그 | `#figure(image(...))` |
| `<한국어-라벨>` | 한국어 제목 라벨 | 제거 |
| `#horizontalrule` | 수평선 변환 | Typst `#line()` |
| 표 헤더 미스타일링 | 기본 표 스타일 | 파란 배경 추가 |

### 4단계: 템플릿 병합

`book/templates/book.typ` 템플릿 내용을 Pandoc 변환 결과 앞에 삽입합니다.

템플릿 포함 요소:
- 페이지/폰트 설정
- 제목 show rules (h1~h4)
- 코드/인용/표 스타일
- 표지 페이지
- 자동 목차

### 5단계: Typst 컴파일

```bash
typst compile output.typ output.pdf --font-path ~/Library/Fonts/
```

---

## 트러블슈팅

### 폰트를 찾을 수 없다

```
error: failed to find font "RIDIBatang"
```

**해결**: `--font-path`에 RIDIBatang, D2Coding 폰트가 있는 디렉토리를 지정합니다.

```bash
# 현재 설치된 폰트 확인
typst fonts --font-path ~/Library/Fonts/ | grep -E "RIDI|D2"
```

### Mermaid 렌더링 실패

```
[다이어그램: 노드1 → 노드2]
```

**해결**: Node.js와 npm이 설치되어 있는지 확인합니다.

```bash
node --version
npx @mermaid-js/mermaid-cli --version
```

### Pandoc 변환 실패

**해결**: Pandoc 3.0+ 버전이 필요합니다 (Typst writer 내장).

```bash
pandoc --version
# 3.0 미만이면 업데이트
brew upgrade pandoc
```

### 이미지가 표시되지 않는다

Typst는 `file://` 접두사 없이 절대경로를 사용합니다. `build_pdf_typst.py`의 `fix_image_paths()`가 자동으로 처리합니다.

---

## 파일 순서

빌드에 포함되는 파일 순서:

```
FRONT:
  1. book/front/preface.md        (서문)
  2. book/front/prologue-v4.md    (들어가며)

CHAPTERS:
  3. chapters/01-환각과-RAG의-첫-만남.md
  4. chapters/02-일단-사내-시스템부터.md
  5. chapters/03-어떤-문서를-넣을까.md
  6. chapters/04-문서를-지식으로-바꾸다.md
  7. chapters/05-드디어-답해준다.md
  8. chapters/06-연차도-규정도-한번에.md
  9. chapters/07-실제로-써보니.md

BACK:
  10. (부록 없음 — 심화 내용은 각 챕터 기술 파트에 포함)
```

챕터를 추가하려면 `build_pdf_typst.py`의 `CHAPTERS` 리스트에 경로를 추가합니다.

---

## Typst 템플릿 수정

`book/templates/book.typ`에서 스타일을 변경할 수 있습니다.

### 색상 팔레트

| 용도 | 색상 코드 | 사용 위치 |
|------|----------|----------|
| 본문 텍스트 | `#1a1a1a` | body |
| h1 밑줄 | `#2563eb` | heading level 1 |
| h2 텍스트/왼쪽바 | `#1e40af` | heading level 2 |
| h3 텍스트 | `#1e3a5f` | heading level 3 |
| 코드 배경 | `#1e293b` | raw block |
| 인용 왼쪽바 | `#93b4e8` | blockquote |
| 인용 배경 | `#f5f8ff` | blockquote |
| 볼드 텍스트 | `#1e3a5f` | strong |

### 표지 수정

`book.typ`의 표지 섹션에서 제목, 부제, 태그라인을 직접 수정합니다.
