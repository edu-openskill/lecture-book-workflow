"""pub-studio 데이터 모델

모든 클래스 간 교환되는 데이터 구조를 정의한다.
외부 의존성 없이 dataclass만 사용.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ImageInfo:
    """Stage 1에서 감지된 단일 이미지 정보."""

    path: str  # 절대 경로
    rel_path: str  # 프로젝트 상대 경로
    category: str  # "gemini" | "terminal" | "diagram" | "default"
    default_width: float  # 0.0~1.0
    default_style: str  # "plain" | "bordered" | "shadow" | "bordered-shadow" | "minimal"
    aspect_ratio: float | None = None  # width / height
    override_width: float | None = None
    override_style: str | None = None
    alt: str = ""
    figure_label: str = ""

    @property
    def effective_width(self) -> float:
        return self.override_width if self.override_width is not None else self.default_width

    @property
    def effective_style(self) -> str:
        return self.override_style if self.override_style is not None else self.default_style

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "rel_path": self.rel_path,
            "category": self.category,
            "default_width": self.default_width,
            "default_style": self.default_style,
            "aspect_ratio": self.aspect_ratio,
            "override_width": self.override_width,
            "override_style": self.override_style,
            "effective_width": self.effective_width,
            "effective_style": self.effective_style,
            "alt": self.alt,
            "figure_label": self.figure_label,
        }


@dataclass
class LayoutIssue:
    """PDF에서 감지된 단일 레이아웃 문제."""

    page: int
    issue_type: str  # blank_page, orphan_content, low_usage, large_image, push_pattern
    severity: str  # "auto_fixable" | "manual"
    message: str
    suggestion: str
    fix_action: str | None = None  # 예: "reduce_image_width"
    image_path: str | None = None
    current_width: float | None = None
    target_width: float | None = None

    def to_dict(self) -> dict:
        d = {
            "page": self.page,
            "type": self.issue_type,
            "severity": self.severity,
            "message": self.message,
            "suggestion": self.suggestion,
        }
        if self.fix_action:
            d["fix_action"] = self.fix_action
        if self.image_path:
            d["image_path"] = self.image_path
        if self.target_width is not None:
            d["target_width"] = self.target_width
        return d


@dataclass
class BuildResult:
    """빌드 파이프라인 실행 결과."""

    success: bool
    typ_path: Path | None = None
    pdf_path: Path | None = None
    svg_dir: Path | None = None
    page_count: int = 0
    duration: float = 0.0
    stage_run: int = 0  # 0=cached, 1=stage1, 2=stage2
    images_detected: list[ImageInfo] = field(default_factory=list)
    error: str | None = None

    def to_dict(self) -> dict:
        return {
            "ok": self.success,
            "page_count": self.page_count,
            "duration": round(self.duration, 2),
            "stage": self.stage_run if self.stage_run > 0 else "cached",
            "error": self.error,
        }


@dataclass
class VerificationResult:
    """검증 루프 실행 결과."""

    round_number: int
    issues: list[LayoutIssue] = field(default_factory=list)
    auto_fixed: list[LayoutIssue] = field(default_factory=list)
    manual_remaining: list[LayoutIssue] = field(default_factory=list)
    build_result: BuildResult | None = None

    def to_dict(self) -> dict:
        return {
            "rounds": self.round_number,
            "total_issues": len(self.issues),
            "auto_fixed": [i.to_dict() for i in self.auto_fixed],
            "manual_remaining": [i.to_dict() for i in self.manual_remaining],
        }


@dataclass
class DesignState:
    """UI에서 전송되는 디자인 설정 전체를 타입화."""

    preset: str = "1"
    components: dict[str, str] = field(default_factory=lambda: {
        "body": "d1", "heading": "d1", "code": "d1",
        "inline_code": "d1", "quote": "d1", "table": "d1", "toc": "d1",
    })
    fonts: dict[str, str] = field(default_factory=lambda: {
        "body": '"RIDIBatang", serif', "code": '"D2Coding", monospace',
    })
    typo: dict[str, float] = field(default_factory=lambda: {
        "size": 10, "tracking": 0, "leading": 1.5, "paragraphGap": 8,
    })
    margins: dict[str, int] = field(default_factory=lambda: {
        "top": 20, "bottom": 28, "left": 22, "right": 17,
    })
    images: dict[str, dict] = field(default_factory=lambda: {
        "gemini": {"preset": "bordered", "width": 70},
        "terminal": {"preset": "minimal", "width": 70},
        "diagram": {"preset": "minimal", "width": 60},
    })
    image_overrides: dict[str, dict] = field(default_factory=dict)
    colors: dict[str, str] = field(default_factory=lambda: {
        "primary": "#2563eb", "text": "#1a1a1a",
        "codeText": "#1e40af", "quoteBg": "#f5f8ff",
    })
    page: dict[str, str] = field(default_factory=lambda: {
        "format": "B5_4x6배판", "outputMode": "pod",
    })
    typo_sizes: dict[str, float] = field(default_factory=lambda: {
        "h1": 26, "h2": 16, "h3": 13, "h4": 11,
        "code": 8, "quote": 9, "table": 8.5, "inlineCode": 8.5,
    })
    toc_depth: int = 2
    toc_spacing: float = 4
    table_first_col_ratio: float = 1.0
    table_overrides: dict[str, list] = field(default_factory=dict)
    component_styles: dict[str, dict] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> DesignState:
        """UI에서 전송된 dict를 DesignState로 변환."""
        if not d:
            return cls()
        defaults = cls()
        return cls(
            preset=d.get("preset", "1"),
            components=d.get("components", defaults.components),
            fonts=d.get("fonts", defaults.fonts),
            typo=d.get("typo", defaults.typo),
            margins=d.get("margins", defaults.margins),
            images=d.get("images", defaults.images),
            image_overrides=d.get("imageOverrides", d.get("image_overrides", {})),
            colors=d.get("colors", defaults.colors),
            page=d.get("page", defaults.page),
            typo_sizes=d.get("typoSizes", d.get("typo_sizes", defaults.typo_sizes)),
            toc_depth=d.get("tocDepth", d.get("toc_depth", 2)),
            toc_spacing=d.get("tocSpacing", d.get("toc_spacing", 4)),
            table_first_col_ratio=d.get("tableFirstColRatio", d.get("table_first_col_ratio", 1.0)),
            table_overrides=d.get("tableOverrides", d.get("table_overrides", {})),
            component_styles=d.get("componentStyles", d.get("component_styles", {})),
        )

    def to_dict(self) -> dict:
        """서버↔UI 호환 dict로 변환."""
        return {
            "preset": self.preset,
            "components": self.components,
            "fonts": self.fonts,
            "typo": self.typo,
            "margins": self.margins,
            "images": self.images,
            "imageOverrides": self.image_overrides,
            "colors": self.colors,
            "page": self.page,
            "typoSizes": self.typo_sizes,
            "tocDepth": self.toc_depth,
            "tocSpacing": self.toc_spacing,
            "tableFirstColRatio": self.table_first_col_ratio,
            "tableOverrides": self.table_overrides,
            "componentStyles": self.component_styles,
        }

    def to_server_dict(self) -> dict:
        """기존 서버 코드 호환용 dict (design_assembler.generate_overrides 입력)."""
        return {
            "colors": self.colors,
            "typo": self.typo,
            "typoSizes": self.typo_sizes,
            "margins": self.margins,
            "page": self.page,
            "images": self.images,
            "tocDepth": self.toc_depth,
            "tocSpacing": self.toc_spacing,
            "tableFirstColRatio": self.table_first_col_ratio,
            "tableOverrides": self.table_overrides,
            "componentStyles": self.component_styles,
        }
