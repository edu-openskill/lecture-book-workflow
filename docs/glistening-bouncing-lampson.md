# pub-studio — OOP 아키텍처 리팩토링 + 검증 루프 통합

## Context

publisher 에이전트의 빌드+검증 워크플로우를 프리뷰 에디터에 통합하여, 단일 스킬(`pub-studio`)로 MD→PDF 전체 과정을 처리한다. 기존 절차적 코드를 객체지향으로 리팩토링하고, 검증 루프(build→check→auto-fix→rebuild)와 개별 이미지 제어를 추가한다.

**설계 원칙**: 낮은 결합도, 높은 응집도, 얇은 실행 파일. 기존 코드는 래핑(위임)하여 재사용.

---

## 아키텍처 개요

```
┌──────────────┐
│  preview.py  │  진입점 (~30줄)
└──────┬───────┘
       │
┌──────▼───────┐
│PreviewServer │  HTTP 라우팅 (얇은 디스패처)
└──┬───┬───┬───┘
   │   │   │
┌──▼┐┌─▼──┐┌▼──────────────┐
│BC ││ IR ││VerificationLoop│
│   ││    ││ (build→check   │
│   ││    ││  →fix→rebuild) │
└───┘└────┘└──┬─────┬──────┘
              │     │
      ┌───────▼┐ ┌──▼──────────┐
      │Build   │ │Layout       │
      │Pipeline│ │Checker      │
      └───┬────┘ └─────────────┘
          │
    ┌─────▼──────┐
    │Design      │
    │Engine      │
    └────────────┘

BC = BuildCache, IR = ImageRegistry
```

**의존 방향**: PreviewServer → VerificationLoop → {BuildPipeline, LayoutChecker} → 기존 스크립트

---

## 파일 구조

```
.claude/skills/pub-studio/
├── SKILL.md
└── references/scripts/
    ├── __init__.py
    ├── models.py              # 데이터 클래스 (BuildConfig, DesignState, LayoutIssue, ImageInfo, BuildResult, VerificationResult)
    ├── build_cache.py         # BuildCache — 2단계 캐시 (preview.py _cache 추출)
    ├── image_registry.py      # ImageRegistry — 개별 이미지 추적/오버라이드 (NEW)
    ├── build_pipeline.py      # BuildPipeline — MD→Typst→PDF/SVG (typst_builder.py 래핑)
    ├── design_engine.py       # DesignEngine — 컴포넌트 조립 (design_assembler.py 래핑)
    ├── layout_checker.py      # LayoutChecker — PDF 분석 + 심각도 분류 (pdf_layout_checker.py 래핑)
    ├── verification_loop.py   # VerificationLoop — build→check→fix 사이클 (NEW)
    └── preview_server.py      # PreviewServer — HTTP 서버 (preview.py 리팩토링)

preview.py                      # 얇은 진입점 (~30줄): argparse → PreviewServer.start()
preview_editor.html             # UI (개별 이미지 패널 + 검증 루프 UI + 레이아웃 이슈 탭 추가)
```

**기존 스크립트는 수정하지 않고 그대로 유지** — 새 클래스가 import하여 위임:
- `.claude/skills/pub-build/references/scripts/typst_builder.py` (813줄)
- `.claude/skills/pub-build/references/scripts/design_assembler.py` (238줄)
- `.claude/skills/pub-layout-check/references/scripts/pdf_layout_checker.py` (273줄)

---

## 클래스 설계

### 1. models.py — 데이터 클래스

```python
@dataclass
class ImageInfo:
    path: str                          # 절대 경로
    rel_path: str                      # 프로젝트 상대 경로
    category: str                      # "gemini" | "terminal" | "diagram" | "default"
    default_width: float               # 0.0~1.0
    default_style: str
    aspect_ratio: float | None = None
    override_width: float | None = None
    override_style: str | None = None

    @property
    def effective_width(self) -> float: ...
    @property
    def effective_style(self) -> str: ...

@dataclass
class LayoutIssue:
    page: int
    issue_type: str                    # blank_page, orphan_content, low_usage, large_image, push_pattern
    severity: str                      # "auto_fixable" | "manual"
    message: str
    suggestion: str
    fix_action: str | None = None
    image_path: str | None = None
    target_width: float | None = None

@dataclass
class BuildResult:
    success: bool
    typ_path: Path | None
    pdf_path: Path | None
    svg_dir: Path | None
    page_count: int
    duration: float
    stage_run: int                     # 0=cached, 1=stage1, 2=stage2
    images_detected: list[ImageInfo]
    error: str | None = None

@dataclass
class VerificationResult:
    round_number: int
    issues: list[LayoutIssue]
    auto_fixed: list[LayoutIssue]
    manual_remaining: list[LayoutIssue]
    build_result: BuildResult

@dataclass
class DesignState:
    """UI state 전체를 타입화. from_dict()/to_dict() 지원."""
    preset: str
    components: dict[str, str]
    fonts: dict[str, str]
    typo: dict[str, float]
    margins: dict[str, int]
    images: dict[str, dict]            # 카테고리 기본값
    image_overrides: dict[str, dict]   # 개별 이미지: {"path": {width, style}}
    colors: dict[str, str]
    page: dict[str, str]
    typo_sizes: dict[str, float]
    toc_depth: int
```

### 2. BuildCache — 2단계 캐시

```python
class BuildCache:
    """preview.py의 _cache dict를 클래스로 추출."""

    # Stage 1 캐시: file_hash → raw_typ
    # Stage 2 캐시: design_hash → svg_dir, page_count, typ_path
    # 파일 모드: mode, file_path, file_designable, file_content

    def compute_file_hash(project_path, files_dict) -> str: ...
    def compute_design_hash(design_state) -> str: ...
    def is_stage1_valid(file_hash) -> bool: ...
    def is_stage2_valid(design_hash) -> bool: ...
    def update_stage1(raw_typ, file_hash, images): ...
    def update_stage2(svg_dir, page_count, typ_path, design_hash): ...
    def load_typ_file(file_path, extract_fn) -> tuple[bool, bool]: ...
    def reset_to_project_mode(): ...
```

**마이그레이션**: `preview.py` lines 375-448의 `_cache` dict + `_compute_*`, `_load_typ_file`, `_reset_to_project_mode` 함수를 클래스로 이동.

### 3. ImageRegistry — 개별 이미지 추적 (NEW)

```python
class ImageRegistry:
    """Stage 1에서 감지된 이미지를 추적하고, 개별 오버라이드를 적용."""

    def scan_raw_typ(raw_typ: str) -> list[ImageInfo]:
        """raw .typ에서 #auto-image() 호출을 파싱하여 이미지 목록 구축."""

    def get_all() -> list[ImageInfo]: ...
    def get_by_category(category) -> list[ImageInfo]: ...

    def set_override(path, width=None, style=None): ...
    def load_overrides(overrides: dict[str, dict]): ...
    def clear_overrides(): ...

    def apply_overrides(raw_typ: str) -> str:
        """오버라이드가 있는 이미지의 max-width/style을 regex로 교체.
        오버라이드 없는 이미지는 카테고리 변수 참조 유지."""

    def reduce_image_width(path, step=0.05) -> float:
        """자동 수정용: 이미지 width를 한 단계 축소 (최소 0.3)."""

    def to_dict() -> dict: ...
```

**핵심 메커니즘**: `apply_overrides()`는 Stage 2 시작 시 호출. `#auto-image("path", ..., max-width: img-gemini-width)` → 오버라이드 있으면 `max-width: 0.55`로 교체.

### 4. BuildPipeline — 빌드 엔진

```python
class BuildPipeline:
    """typst_builder.py를 래핑. 캐시는 소유하지 않음 (호출자가 관리)."""

    def __init__(self, config: dict):
        self._image_registry = ImageRegistry()

    @property
    def image_registry(self) -> ImageRegistry: ...

    def build_raw_typ(front, chapters, back) -> str:
        """Stage 1: MD 통합 → Pandoc → 후처리 → raw .typ.
        완료 후 image_registry.scan_raw_typ() 자동 호출."""

    def assemble_final_typ(raw_typ, design_state, skip_cover=False, skip_toc=False) -> str:
        """Stage 2: image_registry.apply_overrides() → design 조립 → merge."""

    def compile_svg(typ_path, svg_dir) -> int: ...
    def compile_pdf(typ_path, pdf_path) -> bool: ...
```

**마이그레이션**: `typst_builder.build_raw_typ()`, `merge_template_and_content()`, `typst_compile_svg()`, `typst_compile()`에 위임. 추가된 것은 `image_registry` 통합.

### 5. DesignEngine — 디자인 조립

```python
class DesignEngine:
    """design_assembler.py 래핑. 순수 위임."""

    def parse_design_arg(arg) -> dict[str, str]: ...
    def generate_overrides(design_state) -> tuple[str, str, str]: ...
    def assemble_book_base(selection, design_state=None, skip_cover=False, skip_toc=False) -> str: ...
```

**마이그레이션**: `design_assembler.py` 함수에 100% 위임.

### 6. LayoutChecker — 레이아웃 분석 + 심각도 분류

```python
class LayoutChecker:
    """pdf_layout_checker.py 래핑 + 자동수정 가능 여부 분류."""

    AUTO_FIXABLE = {"blank_page", "orphan_content", "large_image"}

    def analyze(pdf_path) -> list[LayoutIssue]:
        """pdf_layout_checker.analyze_layout() → LayoutIssue 변환."""

    def classify_issues(issues) -> tuple[list[LayoutIssue], list[LayoutIssue]]:
        """(auto_fixable, manual)로 분리."""

    def suggest_fixes(issues, image_registry) -> list[LayoutIssue]:
        """자동수정 가능 이슈에 fix_action, target_width 채움.
        - large_image: 다음 단계 width (0.7→0.6→0.5→0.4)
        - orphan_content: 이전 페이지 최대 이미지 width 5% 감소
        - blank_page: pagebreak 제거 플래그"""

    def get_page_usage(pdf_path) -> list[dict]: ...
```

**마이그레이션**: `pdf_layout_checker.analyze_layout()`, `print_report()`에 위임. `classify_issues()`와 `suggest_fixes()`는 새 로직.

### 7. VerificationLoop — 빌드→검증→수정 사이클 (NEW)

```python
class VerificationLoop:
    """최대 3라운드: build → check → auto-fix → rebuild."""

    MAX_ROUNDS = 3

    def __init__(self, pipeline: BuildPipeline, checker: LayoutChecker): ...

    def run(self, typ_path, pdf_path, raw_typ, design_state, staging_dir) -> VerificationResult:
        """검증 루프 실행.
        1. PDF 컴파일
        2. 레이아웃 분석
        3. 자동수정 가능 이슈 → ImageRegistry 오버라이드 적용
        4. Stage 2 재조립 → 재컴파일
        5. 반복 (이슈 없거나 3라운드 도달 시 종료)
        최종 manual 이슈 목록 반환."""

    def _apply_fixes(self, issues: list[LayoutIssue]): ...
```

**검증 흐름**:
```
Round 1: compile_pdf → analyze → 3 auto_fixable + 1 manual
         → reduce_image_width() × 3 → assemble_final_typ → write .typ
Round 2: compile_pdf → analyze → 0 auto_fixable + 1 manual
         → 종료, manual 1건 UI에 보고
```

### 8. PreviewServer — HTTP 서버

```python
class PreviewServer:
    """HTTP 라우팅. 모든 로직은 위의 클래스에 위임."""

    def __init__(self, project_path, port=3333, initial_file=None):
        self._cache = BuildCache()
        self._pipeline = BuildPipeline(config)
        self._checker = LayoutChecker()
        self._verifier = VerificationLoop(self._pipeline, self._checker)
        self._staging_dir = project_path / ".pdf-build"

    def start(self): ...

    # GET 핸들러
    def handle_get_project(self) -> dict: ...
    def handle_get_files(self) -> dict: ...
    def handle_get_blocks(self, path) -> dict: ...
    def handle_get_images(self) -> dict: ...          # NEW — 이미지 목록
    def handle_get_mode(self) -> dict: ...
    def handle_get_svg_meta(self) -> dict: ...
    def handle_get_svg_page(self, page_num) -> bytes: ...
    def handle_get_layout_issues(self) -> dict: ...   # NEW — 레이아웃 이슈

    # POST 핸들러
    def handle_post_save(self, data) -> dict: ...
    def handle_post_build_svg(self, data) -> dict: ...
    def handle_post_build_verified(self, data) -> dict: ...     # NEW — 검증 빌드
    def handle_post_export_pdf(self, data) -> dict: ...
    def handle_post_image_override(self, data) -> dict: ...     # NEW — 개별 이미지
    def handle_post_load_file(self, data) -> dict: ...
    def handle_post_switch_mode(self, data) -> dict: ...
```

**마이그레이션**: `preview.py`의 `PreviewHandler.do_GET/do_POST` 내부 로직을 메서드별로 분리. `PreviewHandler`는 URL 라우팅만 담당하는 얇은 디스패처로 남음. `parse_md_to_blocks()`, `blocks_to_md()` 등 순수 함수는 모듈 레벨 함수로 유지.

---

## .pdf-build/ 스테이징 디렉토리

```
projects/{책이름}/.pdf-build/
├── integrated.md           # Stage 1: 통합 MD
├── raw.typ                 # Stage 1: Pandoc 후처리 결과
├── final.typ               # Stage 2: 디자인 조립 결과
├── preview.pdf             # 검증용 PDF
├── preview_svg/            # SVG 프리뷰 페이지
├── _mermaid_images/        # Mermaid 렌더링
└── build.log               # 빌드 로그
```

최종 PDF만 `book/output/`으로 복사. `.gitignore`에 `.pdf-build/` 추가.

---

## API 엔드포인트 변경

| 엔드포인트 | 메서드 | 상태 | 설명 |
|-----------|--------|------|------|
| `/api/images` | GET | **NEW** | 감지된 이미지 목록 + 오버라이드 |
| `/api/layout-issues` | GET | **NEW** | 현재 레이아웃 이슈 |
| `/api/build-verified` | POST | **NEW** | 검증 루프 빌드 (백그라운드 스레드) |
| `/api/verification-status` | GET | **NEW** | 검증 진행 상태 폴링 |
| `/api/image-override` | POST | **NEW** | 개별 이미지 오버라이드 설정 |
| `/api/build-svg` | POST | 수정 | Stage 1 후 ImageRegistry 자동 채움 |
| 기존 엔드포인트 | - | 유지 | 변경 없음 |

**`/api/build-verified` 응답 예시:**
```json
{
  "ok": true,
  "page_count": 120,
  "duration": 8.5,
  "verification": {
    "rounds": 2,
    "auto_fixed": [{"page": 45, "type": "large_image", "fix": "width 0.7→0.6"}],
    "manual_remaining": [{"page": 78, "type": "low_usage", "suggestion": "..."}]
  },
  "svg_base": "/api/svg/"
}
```

---

## UI 변경 (preview_editor.html)

### 1. 개별 이미지 패널
기존 카테고리 컨트롤(gemini/terminal/diagram) 유지 + 하단에 접을 수 있는 개별 이미지 리스트 추가.
- 첫 빌드 후 `/api/images`로 채움
- 각 이미지: 썸네일 + 경로 + 카테고리 뱃지 + width 슬라이더 + style 드롭다운 + 초기화 버튼
- 변경 시 `/api/image-override` POST → `scheduleDesignRebuild()`

### 2. 검증 빌드 버튼
프리뷰 툴바에 "Verified Build" 버튼 추가.
- 클릭 → 스피너 + "Verifying... (round 1/3)"
- 완료 → 결과 배너: 초록(이슈 없음) / 노랑(자동수정 N건 + 수동 M건)
- 수동 이슈 클릭 → 해당 페이지로 이동

### 3. 레이아웃 이슈 탭
탭바에 "Layout Issues" 추가.
- 페이지별 사용률 바 차트
- 이슈 목록 (심각도 뱃지 + 클릭→해당 페이지)

### 4. 빌드 모드 표시
- 글 편집 시: "Content edit — Stage 1 rebuild required (~5-10s)"
- 디자인 변경 시: "Design change — Stage 2 only (~200ms)"

---

## 구현 순서

### Phase 1: Foundation (models + cache)
1. `models.py` — 데이터 클래스 생성
2. `build_cache.py` — `preview.py` `_cache` 추출
3. 단위 테스트

### Phase 2: Service Wrappers
4. `design_engine.py` — `design_assembler.py` 래핑
5. `build_pipeline.py` — `typst_builder.py` 래핑
6. `layout_checker.py` — `pdf_layout_checker.py` 래핑 + 심각도 분류

### Phase 3: New Features
7. `image_registry.py` — scan/override/apply 로직
8. `verification_loop.py` — build→check→fix 사이클

### Phase 4: Server Refactor
9. `preview_server.py` — PreviewServer 클래스 (라우트 메서드 분리)
10. `preview.py` — 얇은 진입점으로 교체
11. 새 API 엔드포인트 추가

### Phase 5: UI
12. 개별 이미지 패널 (sidebar)
13. 검증 루프 UI (버튼 + 상태 + 결과)
14. 레이아웃 이슈 탭

### Phase 6: Integration
15. `.pdf-build/` 스테이징 디렉토리 통합
16. `pub-studio` SKILL.md 작성
17. CATALOG.md 업데이트

---

## 검증

1. **단위 테스트**: 각 클래스 독립 테스트 (BuildCache, ImageRegistry, LayoutChecker.classify_issues)
2. **기존 동작 보존**: 리팩토링 후 프로젝트 모드 + 파일 모드 빌드가 동일 결과 출력
3. **개별 이미지 제어**: 이미지 width 변경 → SVG에서 해당 이미지 크기 변화 확인
4. **검증 루프**: 의도적으로 큰 이미지 포함 → 자동 축소 → 2라운드 후 이슈 감소 확인
5. **UI 통합**: Playwright MCP로 브라우저 테스트 — 이미지 슬라이더 조작, 검증 빌드 실행, 이슈 패널 확인
6. **회귀 테스트**: 기존 프리뷰 기능 (디자인 프리셋 전환, 파일 모드, PDF 내보내기) 정상 동작

---

## 주요 참조 파일

| 파일 | 역할 | 줄 수 |
|------|------|-------|
| `preview.py` | 리팩토링 대상 (서버) | 882 |
| `preview_editor.html` | UI 확장 대상 | 1,483 |
| `.claude/skills/pub-build/references/scripts/typst_builder.py` | 래핑 대상 (빌드) | 813 |
| `.claude/skills/pub-build/references/scripts/design_assembler.py` | 래핑 대상 (디자인) | 238 |
| `.claude/skills/pub-layout-check/references/scripts/pdf_layout_checker.py` | 래핑 대상 (분석) | 273 |
| `.claude/skills/pub-typst-design/references/templates/components/_shared/85-image.typ` | auto-image 함수 | 110 |
| `.claude/skills/pub-page-fit/SKILL.md` | 자동수정 전략 참조 | 76 |
