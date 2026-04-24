---
name: pub-html-to-pdf
description: Use when you already built an HTML preview with `pub-html-build` and need to rasterize it to an A4 PDF via headless Chromium. Optional — the book's canonical PDF path is `pub-build` (Typst); this skill is kept as a fallback/utility to share a single chapter as a PDF.
---

# pub-html-to-pdf

`pub-html-build`이 만든 `.build/NN-*.html`을 **Playwright Chromium**으로 열어 A4 PDF로 내린다. Paged.js를 선택적으로 주입해 페이지 조판을 강제할 수 있다.

## 언제 쓰는가

- 챕터 프리뷰 한 장을 **PDF 파일로 공유**해야 할 때 (카카오톡·메일 첨부 등)
- 정식 전자책 PDF는 이 스킬의 출력이 아니라 `pub-build`(Typst 파이프라인)의 결과임에 유의

HTML 프리뷰만 필요하면 이 스킬은 호출하지 않는다.

## 빌드 실행

```bash
python .claude/skills/pub-html-to-pdf/build_pdf.py \
  --project-root projects/사내AI비서_v2 \
  --chapter 11
```

- 입력: `projects/사내AI비서_v2/.build/11-*.html`
- 출력: `projects/사내AI비서_v2/.build/pdf/11-*.pdf`

입력 HTML이 없으면 먼저 `pub-html-build`로 빌드하라는 에러를 띄운다.

## 옵션

| 옵션 | 기본 | 설명 |
|------|------|------|
| `--project-root PATH` | 필수 | 책 프로젝트 루트 |
| `--chapter N` | (전체) | 특정 챕터만 PDF로. 생략 시 `.build/` 안 모든 HTML을 순회 |
| `--no-pagedjs` | off | Paged.js 주입 없이 Chromium 기본 인쇄 규칙으로 렌더 (훨씬 빠름, 조판 품질은 낮음) |

## 의존성

```
playwright==1.48
```

Chromium 설치:

```bash
python -m playwright install chromium
```

## 파이프라인상의 위치

```
chapters/NN-*.md
   │  (pub-html-build)
   ▼
.build/NN-*.html  ←── 프리뷰 뷰 (브라우저에서 file://)
   │  (pub-html-to-pdf, 선택)
   ▼
.build/pdf/NN-*.pdf
```

정식 전자책은 이 경로가 아니라 `chapters/**.md → pub-build(Typst) → .pdf-build/*.pdf`.
