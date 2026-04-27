---
name: build
description: "마크다운을 Typst 경유 PDF로 빌드하는 파이프라인 실행"
allowed-tools: Bash(python3 *build_pdf_typst.py*)
---

# build — PDF 빌드

## 구조

| 파일 | 위치 | 역할 |
|------|------|------|
| `typst_builder.py` | **스킬 소유** (`references/scripts/`) | 범용 빌드 엔진 (파이프라인 로직 전체) |
| `build_pdf_typst.py` | **프로젝트** (`book/`) | 프로젝트별 설정 (챕터 목록, 경로, 제목) |

프로젝트의 `build_pdf_typst.py`가 스킬의 `typst_builder.py`를 import하여 `build(config)` 호출.

## 역할

프로젝트 설정(`CONFIG` dict) + 범용 엔진(`typst_builder.build()`)으로 PDF 변환을 수행한다.

## 파이프라인 (6단계)

```
[1/6] 마크다운 통합 + 전처리
      ├── HTML 주석 제거
      ├── 이미지 경로 절대경로 변환
      ├── Mermaid 다이어그램 렌더링 (PNG)
      └── <br> 태그 변환 (코드 블록 보존)

[2/6] 이미지 공백 자동 제거
      └── Pillow autocrop (padding 6px)

[3/6] Pandoc 변환 (MD → Typst)
      └── pipe_tables + fenced_code_blocks, -citations

[4/6] 후처리 + 템플릿 병합
      ├── 이미지 → #auto-image() 변환
      ├── 한국어 라벨 제거
      ├── 수평선 처리
      └── book.typ 템플릿 병합

[5/6] Typst 컴파일 (TYP → PDF)
      └── --font-path ~/Library/Fonts --root /

[6/6] 레이아웃 분석
      └── pdf_layout_checker.py 자동 실행
```

## 실행

```bash
cd projects/{프로젝트}
.pdf_venv/bin/python3 book/build_pdf_typst.py
```

## 의존성

- `typst` (brew install typst)
- `pandoc` (brew install pandoc)
- `npx @mermaid-js/mermaid-cli` (Mermaid 렌더링)
- `Pillow` (pip install Pillow, 이미지 autocrop)
- `PyMuPDF` (pip install PyMuPDF, 레이아웃 분석)

## `--design` 옵션

컴포넌트 단위로 디자인을 선택하여 PDF를 빌드한다.

```bash
# 프리셋 (전체 컴포넌트 동일 디자인)
python3 book/build_pdf_typst.py --design 1    # 클래식 블루
python3 book/build_pdf_typst.py --design 2    # 컴팩트 모노

# 믹스매치 (컴포넌트별 선택, 기본값 프리셋 1)
python3 book/build_pdf_typst.py --design "body=2,heading=1,code=2,table=2"
```

`--design` 생략 시 기존 `book_base.typ`을 사용 (하위호환).

## 설정 변경 포인트

| 항목 | 파일 | 위치 |
|------|------|------|
| 포함 파일 목록 | 프로젝트 `build_pdf_typst.py` | `CONFIG["front"]`, `CONFIG["chapters"]`, `CONFIG["back"]` |
| 출력 파일명 | 프로젝트 `build_pdf_typst.py` | `CONFIG["output_pdf"]` |
| 이미지 유형별 최대 너비 | 스킬 `typst_builder.py` | `_detect_image_max_width()` |
| 후처리 규칙 | 스킬 `typst_builder.py` | `fix_typst_content()` |

## 새 프로젝트에서 사용하기

1. 프로젝트의 `book/build_pdf_typst.py`를 복사
2. `CONFIG`의 경로와 챕터 목록만 변경
3. `python3 book/build_pdf_typst.py` 실행
4. 엔진(`typst_builder.py`)은 스킬에서 자동 로드

## 참조

- [build-pipeline.md](references/build-pipeline.md) — 파이프라인 상세 규칙
