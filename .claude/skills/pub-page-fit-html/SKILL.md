---
name: pub-page-fit-html
description: "HTML+Chromium 파이프라인 전용 자동 페이지 밀도 조정. pub-layout-check로 빈 공간·고아 페이지 감지 후 컴포넌트 density-scale을 단계적으로 축소해 재빌드·재분석 루프."
---

# pub-page-fit-html — HTML PDF 자동 밀도 조정

## 역할

`pub-html-build` + `pub-html-to-pdf` 로 만든 PDF를 `pub-layout-check`로 분석하고, **하단 공백·고아 페이지가 임계 이하**가 되도록 컴포넌트 padding·gap을 점진적으로 축소해서 재빌드·재분석을 자동 반복한다.

`pub-page-fit`은 Typst 전용 — 이 스킬은 **HTML+Chromium 경로 전용 대응**.

## 실행

```bash
.claude/skills/pub-html-to-pdf/.venv/bin/python \
  .claude/skills/pub-page-fit-html/auto_fit.py \
  --project-root projects/사내AI비서_v2 \
  --chapter 1
```

옵션:
| 옵션 | 기본 | 설명 |
|------|------|------|
| `--project-root PATH` | 필수 | 책 프로젝트 루트 |
| `--chapter N` | 필수 | 대상 챕터 번호 |
| `--max-iterations N` | 5 | 최대 반복 횟수 (기본 5회) |
| `--min-density N` | 0.75 | 최소 축소 한계 (0.75 = 25% 축소까지) |
| `--issue-threshold N` | 0.60 | 페이지 사용률 이 값 이하면 문제로 판정 (60%) |

## 동작 흐름

```
[1/5] density=1.00 → 빌드 → 분석
   p10 66% · p11 56% · p19 45% (3 이슈)

[2/5] density=0.95 → override CSS 갱신 → 재빌드 → 분석
   p10 72% · p11 61% · p19 48% (2 이슈)

[3/5] density=0.90 → ...
   p10 78% · p11 68% · p19 52% (1 이슈)

[4/5] density=0.85 → ...
   이슈 0 ✅ — 종료

→ .build/_pdf-density.css 확정 (density=0.85)
→ 최종 PDF: .build/pdf/01-*.pdf
```

## Density Scale 영향 대상

`.build/_pdf-density.css` 생성. scale 값에 따라 다음 컴포넌트 padding·gap·margin을 비례 축소:

- `.figure-group` padding·gap
- `.rag-pipeline-box` / `.rag-step` padding
- `.rag-step .s-meta` margin·padding
- `.llm-rag-split` padding·gap
- `.lrs-paths` / `.lrs-path` gap
- `.librarian-scene` padding
- `.terminal-log .tl-body` padding
- `.annotated-compare` / `.ac-block` padding·margin
- 본문 `p` margin-bottom·line-height

## 산출물

1. `.build/_pdf-density.css` — 적용된 density 고정값 CSS
2. `.build/pdf/NN-*.pdf` — 최종 PDF
3. stdout 로그 — 각 반복의 이슈 리스트·사용률

## 범위 밖

- Typst 파이프라인 (`pub-page-fit`이 담당)
- 이미지 max-width 자동 축소 (별도 스킬)
- 챕터 콘텐츠 재배치 (수동)
- multi-chapter 일괄 (단일 챕터만)

## 의존성

```
pymupdf  (pub-layout-check가 사용)
pub-html-build
pub-html-to-pdf
pub-layout-check
```

## 제한

- density 0.75 이하로 내려가도 이슈가 남으면: **수동 판단 필요** — 내용 자체를 줄이거나, figure-group 분해, 또는 `page-break-before: always` 강제
- 축소해도 가독성은 유지되지만 0.75 미만은 **컴포넌트가 답답**해 보일 수 있음
