---
name: image-optimize
description: "이미지 공백 자동 제거(autocrop) + Typst auto-image 자동 크기 조절"
allowed-tools: Bash(python3 *image_optimizer.py*)
---

# image-optimize — 이미지 최적화

## 스크립트

- **원본**: `references/scripts/image_optimizer.py` (스킬 소유)
- **프로젝트 참조**: `book/image_optimizer.py` (심볼릭 링크 → 스킬)

## 역할

1. **Autocrop**: 이미지의 위아래/좌우 흰 공백을 자동으로 잘라냄 (Pillow)
2. **Auto-image**: Typst 컴파일 시 남은 페이지 공간에 맞게 이미지 크기를 자동 조절

## 구성 요소

### 1. image_optimizer.py (독립 스크립트)

이미지 파일의 공백을 분석하고 제거하는 독립 도구.

```bash
# 전체 assets 디렉토리 처리
.pdf_venv/bin/python3 book/image_optimizer.py assets/

# 특정 파일만
.pdf_venv/bin/python3 book/image_optimizer.py assets/CH01/01_step1.png

# 분석만 (수정 안 함)
.pdf_venv/bin/python3 book/image_optimizer.py assets/ --dry-run
```

### 2. auto-image 함수 (book.typ 내장)

Typst의 `layout()` + `measure()`를 사용하여 런타임에 이미지 크기를 자동 조절.

```typst
#auto-image("path/to/image.png", alt: [설명], max-width: 0.6)
```

**동작 원리**:
1. `layout(size => ...)`: 현재 남은 페이지 공간 측정
2. `measure(image(...))`: 지정 너비에서의 이미지 높이 계산
3. 이미지가 남은 공간보다 크면 → 비율 유지하면서 축소
4. 축소 비율이 50% 미만이면 → 원래 크기로 다음 페이지에 배치

## 유형별 최대 너비

| 유형 | max-width | 파일명 패턴 |
|------|-----------|-----------|
| 챕터 오프닝 | 0.5 (50%) | `*chapter-opening*` |
| 실행 결과 캡처 | 0.65 (65%) | `*step1*`, `*step2*`, `*step3*`, `*step4*` |
| Mermaid (가로형, AR>2.0) | 0.75 (75%) | `*mermaid_*` — 종횡비 자동 감지 |
| Mermaid (중간, 1.0~2.0) | 0.55 (55%) | `*mermaid_*` — 종횡비 자동 감지 |
| Mermaid (세로형, AR<1.0) | 0.45 (45%) | `*mermaid_*` — 종횡비 자동 감지 |
| 기본 (개념도 등) | 0.6 (60%) | 그 외 |

### 유형별 테두리 style

`auto-image`의 `style` 파라미터로 이미지 테두리를 제어한다. `image_border_preset` CONFIG 값에 따라 Python 빌드가 경로 패턴별로 자동 주입.

| 경로 패턴 | 유형 | clean-border | shadow | primary-shadow | minimal |
|----------|------|-------------|--------|---------------|---------|
| `gemini/` | 개념도 | bordered | shadow | bordered-shadow | minimal |
| `terminal/` | 터미널 캡처 | minimal | shadow | shadow | minimal |
| `diagram/` | D2/Mermaid | minimal | shadow | shadow | minimal |
| 그 외 | 기본 | minimal | shadow | shadow | minimal |

**Mermaid 종횡비 자동 감지**: `_get_image_aspect_ratio()`가 렌더링된 PNG의 가로/세로 비율을 Pillow로 읽어 max-width를 자동 결정한다. 가로로 넓은 다이어그램은 넓게, 세로로 긴 다이어그램은 좁게 배치한다.

**이 값은 "최대"이며, 페이지에 안 들어가면 auto-image가 자동으로 줄인다.**

## 2열(side-image) 레이아웃 기준

이미지와 텍스트를 나란히 배치하는 2열 레이아웃 적용 기준.

### 2열 적용 조건 (모두 충족 시)

| 조건 | 2열 (side-image) | 1열 (auto-image) |
|------|-----------------|-----------------|
| **비율** | 정사각(0.8~1.2) 또는 세로형(<0.8) | 가로형(>1.3) |
| **원본 너비** | 650px 이하 | 800px 이상 |
| **유형** | 개념 일러스트, 비유 그림 | 터미널 캡처, 코드 결과 |
| **관련 텍스트** | 3문단+ 설명이 있음 | 캡션 1줄만 |

### 적용 방법

Markdown body 파일에서 raw Typst 블록으로 삽입:

````markdown
```{=typst}
#side-image("assets/CH01/01_example.png", [
텍스트 내용...

추가 문단...

#text(size: 8pt, fill: rgb("#6b7280"))[그림 캡션]
], img-width: 0.35)
```
````

### img-width 가이드

| 이미지 형태 | img-width | 설명 |
|------------|-----------|------|
| 정사각(~1.0) | 0.35~0.40 | 이미지와 텍스트 균형 |
| 세로형(<0.8) | 0.30~0.35 | 이미지 좁게, 텍스트 넓게 |
| 약간 가로(1.0~1.2) | 0.40~0.45 | 이미지 조금 넓게 |

### 주의사항

- **터미널 캡처, 코드 결과**는 항상 1열 — 축소하면 글자가 안 보임
- **머메이드 다이어그램**은 항상 1열 — 복잡한 흐름도는 넓게 봐야 함
- 2열 전환 전 반드시 **autocrop** 먼저 실행
- `book/body/` 파일만 수정, `chapters/` 원본은 절대 건드리지 않음

## 참조

- [image-rules.md](references/image-rules.md) — 이미지 규칙 상세
