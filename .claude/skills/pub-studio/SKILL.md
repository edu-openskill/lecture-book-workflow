# pub-studio — 프리뷰 에디터 + 검증 빌드

model: claude-sonnet-4-6
user_invocable: false

## 하는 일

MD→Typst→PDF/SVG 전체 파이프라인을 브라우저 프리뷰 에디터로 통합한다.
디자인 실시간 프리뷰, 개별 이미지 크기 제어, 레이아웃 검증 루프(build→check→auto-fix→rebuild)를 제공한다.

## 실행 흐름

publisher 에이전트가 이 스킬을 사용할 때의 흐름.

### 1. 사용자에게 프리뷰 제안

빌드 또는 디자인 작업 시작 전, 사용자에게 프리뷰 에디터 사용 여부를 묻는다.

> **프리뷰 에디터**를 사용하면 브라우저에서 실시간으로 디자인을 확인하며 작업할 수 있습니다.
> - 디자인 프리셋/폰트/여백 등을 즉시 변경하고 결과 확인
> - 개별 이미지 크기를 슬라이더로 조절
> - 레이아웃 이슈(빈 페이지, 고아줄) 자동 감지 + 수정
>
> **프리뷰를 사용할까요?**
> 1. 네, 프리뷰 에디터로 작업합니다 (Recommended)
> 2. 아니요, CLI에서 바로 PDF를 빌드합니다

### 2. 프리뷰 서버 실행

사용자가 1번을 선택하면 서버를 시작한다.

```bash
# 스킬 폴더 내 진입점 실행
python3 .claude/skills/pub-studio/references/preview.py              # 프로젝트 자동 감지
python3 .claude/skills/pub-studio/references/preview.py 사내AI비서_v2  # 프로젝트 지정
python3 .claude/skills/pub-studio/references/preview.py --port 8080   # 포트 지정
python3 .claude/skills/pub-studio/references/preview.py --file book/통합본.typ  # 파일 모드
```

서버가 `http://localhost:3333`에서 실행되면 브라우저가 자동으로 열린다.

### 3. 작업 루프

```
사용자: 디자인 변경 (브라우저 UI)
  → Stage 2 재조립 (~200ms) → SVG 프리뷰 갱신

사용자: 글 수정 (MD 파일 저장)
  → Stage 1 재빌드 (~5-10s) → Stage 2 → SVG 프리뷰 갱신

사용자: "Verified Build" 클릭
  → 검증 루프 (build→check→auto-fix→rebuild, 최대 3라운드)
  → 자동수정 결과 + 수동이슈 보고

사용자: "Export PDF" 클릭
  → 최종 PDF 내보내기
```

### 4. CLI 빌드 (프리뷰 미사용)

사용자가 2번을 선택하면 기존 `pdf-ty` 스킬로 바로 빌드한다.

## 아키텍처

```
preview.py  (얇은 진입점 ~40줄)
  └→ PreviewServer  (HTTP 라우팅)
       ├→ BuildCache       (2단계 캐시: Stage 1 file_hash, Stage 2 design_hash)
       ├→ BuildPipeline    (typst_builder.py 래핑)
       │    ├→ ImageRegistry   (개별 이미지 추적 + 오버라이드)
       │    └→ DesignEngine    (design_assembler.py 래핑)
       ├→ LayoutChecker    (pdf_layout_checker.py 래핑 + 심각도 분류)
       └→ VerificationLoop (build→check→fix 사이클, 최대 3라운드)
```

## 파일 구조

```
.claude/skills/pub-studio/
├── SKILL.md
└── references/
    ├── preview.py                 # 진입점 (얇은 래퍼 ~40줄)
    ├── preview_editor.html        # 브라우저 UI
    └── scripts/
        ├── __init__.py
        ├── models.py              # 데이터 클래스
        ├── build_cache.py         # 2단계 캐시
        ├── image_registry.py      # 개별 이미지 추적/오버라이드
        ├── build_pipeline.py      # MD→Typst→PDF/SVG
        ├── design_engine.py       # 컴포넌트 조립
        ├── layout_checker.py      # PDF 분석 + 심각도 분류
        ├── verification_loop.py   # build→check→fix 사이클
        └── preview_server.py      # HTTP 서버 + API
```

모든 파일이 스킬 폴더 안에 있으므로, 스킬을 복사하면 그대로 동작한다.

## 2단계 빌드 캐시

| 단계 | 트리거 | 소요 | 캐시 키 |
|------|--------|------|---------|
| Stage 1 | MD 파일 변경 | ~5-10s | file_hash (MD 내용 기반) |
| Stage 2 | 디자인 설정 변경 | ~200ms | design_hash (state 기반) |

디자인만 변경하면 Stage 2만 재실행 → 실시간 프리뷰.

## 검증 루프

```
Round 1: compile_pdf → analyze → auto_fixable 3건 + manual 1건
         → reduce_image_width() × 3 → assemble → write .typ
Round 2: compile_pdf → analyze → 0 auto_fixable + manual 1건
         → 종료, manual 1건 UI에 보고
```

자동수정 가능: `blank_page`, `orphan_content`, `large_image`
수동확인 필요: `low_usage`, `push_pattern`

## API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/api/project` | GET | 프로젝트 정보 |
| `/api/files` | GET | 파일 목록 |
| `/api/images` | GET | 감지된 이미지 목록 + 오버라이드 |
| `/api/layout-issues` | GET | 레이아웃 이슈 + 페이지별 사용률 |
| `/api/verification-status` | GET | 검증 진행 상태 |
| `/api/build-svg` | POST | SVG 프리뷰 빌드 |
| `/api/build-verified` | POST | 검증 루프 빌드 (백그라운드) |
| `/api/export-pdf` | POST | PDF 내보내기 |
| `/api/image-override` | POST | 개별 이미지 오버라이드 |

## 표지 디자인 위자드

`scripts/cover_generator.py`가 담당. 4단계 위자드로 표지를 만든다.

```
Step 1. 레이아웃    → wizard_step1_layout()   --cover-preview
Step 2. 그림자      → wizard_step2_shadow()   --cover-shadow
Step 3. 폰트 색상   → wizard_step3_color()    --cover-color
Step 4. 최종 확정   → wizard_step4_confirm()  --cover-confirm
```

각 단계에서 4변형 HTML UI(`assets/cover_preview.html`) 생성 → 유저 선택 → 다음 단계.
`--ebook` 플래그로 전자책 규격(750x1110px, 72ppi, JPG) 적용.

> 서브에이전트에서는 이미지 표시 불가. 메인 세션이 직접 실행한다. CLAUDE.md "인쇄소 실행 흐름" 참조.

## 의존 스킬

- `pub-build` — typst_builder.py, design_assembler.py
- `pub-layout-check` — pdf_layout_checker.py
- `pub-typst-design` — 템플릿, 컴포넌트, 변수
