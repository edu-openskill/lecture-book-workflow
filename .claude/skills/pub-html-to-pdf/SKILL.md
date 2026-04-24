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

---

## PDF 빌드 규칙 (Chromium headless 대응)

Playwright Chromium이 `file:///…/01-*.html` 을 열어 PDF로 저장하는 과정에서 여러 번 재현된 이슈와 그 해법. 새 챕터·새 컴포넌트를 추가할 때 반드시 이 규칙을 따라야 PDF가 의도대로 렌더된다.

### R1. Chromium은 주기적으로 재설치해야 한다 (조용한 실패)

Playwright CLI가 `playwright install chromium` 업데이트를 요구하면 `build_pdf.py`는 **에러 없이 조용히 종료**한다. 빌드 로그 마지막 줄이 `✅ PDF: …` 가 아니라 `║ <3 Playwright Team ║` 같은 설치 안내라면 빌드 실패다.

```bash
cd .claude/skills/pub-html-to-pdf
.venv/bin/python -m playwright install chromium
```

**검증**: `ls -la <pdf>` 로 mtime 이 방금 시각과 일치하는지 확인. 일치 안 하면 빌드 안 된 것.

### R2. `body { background: … }` 를 명시하지 말라

Chromium PDF 렌더는 body 배경을 `print_background=True` 경로로 포함시키는데, **sRGB 색 프로파일 변환 과정에서 `#ffffff`를 `#fdf5ec` 같은 warm tone**으로 찍어낸다. body 배경을 **미지정**으로 두면 Chromium이 paper color(순백)을 사용해 이 문제가 사라진다.

```css
/* ❌ */
body { background: #ffffff; }

/* ✅ */
body { /* background 속성 자체를 쓰지 않음 */ }
```

### R3. `print-color-adjust: exact` 전역 적용

Chromium headless PDF는 인쇄 절약 모드가 기본이라 **box-shadow·배경색·뱃지 색을 축소/생략**한다. `print.css`에 아래를 넣어야 의도한 색/그림자가 찍힌다.

```css
* {
  -webkit-print-color-adjust: exact !important;
  print-color-adjust: exact !important;
}
```

### R4. 모든 다이어그램·이미지·figure 래퍼에 `page-break-inside: avoid`

A4 페이지 경계가 컴포넌트 한가운데를 가르지 않도록 `print.css`에 나열:

```css
.figure-group, .librarian-scene, .llm-rag-split, .rag-pipeline-box,
.annotated-compare, .terminal-log, .arch11, .code-block {
  page-break-inside: avoid;
  break-inside: avoid;
}
```

**신규 컴포넌트를 추가할 때** 이 목록에 편입하는 것이 기본 체크리스트.

### R5. 한글 글리프 겹침 방지

원인 두 가지:
1. **리거처**: 인접 자모가 리거처로 묶이다 metric 엇갈림 → `font-feature-settings: 'liga' off`
2. **Synthetic bold**: Pretendard 700 weight 파일을 CDN에서 못 받을 때 Chromium이 regular 파일을 두 번 그려 굵게 표시 → 글자가 **이중으로 겹쳐 보임**. `font-synthesis: none` 으로 차단

```css
body {
  font-feature-settings: 'liga' off;
  font-synthesis: none;  /* ← synthetic bold 차단. 굵은 글씨 겹침의 주원인 */
  word-break: keep-all;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
```

`font-synthesis: none` 적용 시 CDN 로드 실패로 weight 파일이 없으면 **정상 weight(400) 렌더**로 fallback (겹침 없이 얇게 표시). 굵게는 안 보이지만 글자가 망가지지 않는다.

### R6. `font-family`에 한글 fallback을 **명시**

JetBrains Mono 등 monospace를 직접 쓰면 한글 글리프가 없어 시스템 fallback이 개입, metric이 틀어진다. 한글이 함께 찍히는 영역은 fallback을 반드시 명시.

```css
/* ❌ */
.tl-body { font-family: 'JetBrains Mono', monospace; }

/* ✅ */
.tl-body {
  font-family: 'JetBrains Mono', 'Pretendard', -apple-system,
               'Apple SD Gothic Neo', 'Noto Sans KR', monospace, sans-serif;
}
```

### R7. flex/grid 컨테이너는 `overflow: hidden` + 자식 `min-width: 0`

A4 폭은 좁다(658px). flex row 내 노드가 누적되면 자연 wrap 안 되고 **밖으로 튀어나간다**. 아래 두 규칙이 안전장치.

```css
.llm-rag-split {
  overflow: hidden;
  display: grid;
  grid-template-columns: auto 1fr;
}
.lrs-paths,
.lrs-path {
  min-width: 0;  /* flex 자식이 intrinsic size를 무시하도록 */
}
```

### R8. 그림자·테두리는 토큰화 + 중첩 금지

모든 다이어그램이 같은 무게를 갖도록 `--shadow-figure` 공용 토큰 사용. 래퍼(`.figure-group`) 안에 들어간 자식은 그림자 중복을 피하도록:

```css
.figure-group > * {
  margin: 0 !important;
  box-shadow: none !important;
}
```

### R9. PDF 뷰어별 렌더 차이 인지

| 뷰어 | 특성 |
|---|---|
| **Preview.app (macOS)** | 권장. 페이지 종이 흰색, 주변은 뷰어 UI 회색 |
| **PDFgear.app** | Night Mode·Eye-protection 등 기본 필터가 켜진 경우 회색 오버레이 |
| **Chrome / Safari** | PDF 내부 배경 원본 그대로 |
| **Acrobat Reader** | 권장. 색 프로파일 정확 |

문제 신고가 들어오면 **뷰어 차이인지 PDF 자체 이슈인지**를 먼저 확인. `pdftoppm` 으로 PNG 추출해 픽셀 측정하면 PDF 자체 상태 검증 가능:

```bash
pdftoppm -png -r 180 <input>.pdf /tmp/page
python3 -c "from PIL import Image; im=Image.open('/tmp/page-01.png'); print(im.getpixel((300,400)))"
```

순백 `(255,255,255)`이면 PDF 문제 없음, 뷰어 이슈.

### R10b. 코드블록 긴 줄 PDF 오버플로우

`.code-block`은 screen에서 `overflow-x: auto`로 가로 스크롤 처리하지만 **PDF에서는 스크롤 불가** → 긴 주석(`# TODO: ...`)이 박스를 뚫고 나간다. `@media print`에서 wrap으로 강제 전환 필요.

```css
.code-block {
  overflow: visible !important;
  white-space: pre-wrap !important;
  word-break: break-all !important;
  overflow-wrap: anywhere !important;
}
.code-block * {
  white-space: pre-wrap !important;
  word-break: break-all !important;
}
```

`code-block *`까지 적용해야 내부 `<span>`(문법 하이라이트·TODO 배지) 도 wrap.

### R10. `media="print"` 의 애매한 적용

`chapter-template.html`은 `print.css`를 `<link media="print">`로 로드. Playwright `emulate_media('print')`로 활성화되지만 **타이밍 이슈**가 간헐 발생. 페이지 전환 효과·애니메이션은 `@media print`가 아닌 루트에 두는 쪽이 안전.

---

## 빌드 검증 체크리스트

새 챕터 PDF 빌드 후 아래를 확인:

- [ ] `ls -la <pdf>` mtime 이 방금 빌드 시각인지 (R1)
- [ ] `pdftoppm`으로 여백 픽셀 `(255,255,255)` 확인 (R2·R3)
- [ ] 다이어그램이 페이지 경계에서 쪼개지지 않는지 (R4)
- [ ] 한글 글리프 겹침 없는지 (R5·R6)
- [ ] 컴포넌트가 외곽 border 밖으로 튀어나가지 않는지 (R7)
- [ ] Preview.app·Chrome 두 군데에서 동일하게 보이는지 (R9)
