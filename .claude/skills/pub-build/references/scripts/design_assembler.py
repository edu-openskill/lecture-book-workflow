"""디자인 컴포넌트 어셈블러 — 유저 선택에 따라 book_base 내용을 조립

사용법:
  from design_assembler import parse_design_arg, assemble_book_base
  selection = parse_design_arg("1")           # 프리셋 1
  selection = parse_design_arg("body=2,heading=1")  # 믹스매치
  result = assemble_book_base(selection)       # 조립된 Typst 문자열
"""

import json
import re
from pathlib import Path

COMPONENTS_DIR = (
    Path(__file__).resolve().parents[3]
    / "pub-typst-design"
    / "references"
    / "templates"
    / "components"
)

# 결합 순서 (Typst 스코프 순서 중요)
ASSEMBLY_ORDER = [
    ("_shared", "00-variables.typ"),
    ("_shared", "01-page.typ"),
    ("_variant", "body_{sel}.typ"),
    ("_variant", "chapter_opening_{sel}.typ"),
    ("_variant", "heading_{sel}.typ"),
    ("_variant", "code_{sel}.typ"),
    ("_variant", "inline_code_{sel}.typ"),
    ("_variant", "quote_{sel}.typ"),
    ("_variant", "table_{sel}.typ"),
    ("_shared", "80-misc.typ"),
    ("_shared", "85-image.typ"),
    ("_shared", "90-cover.typ"),
    ("_variant", "toc_{sel}.typ"),
]

VARIANT_KEYS = ["body", "chapter_opening", "heading", "code", "inline_code", "quote", "table", "toc"]

OVERRIDE_MARKER = "// ──OVERRIDES──"

# _shared 파일 → componentStyles 키 매핑 (변형 파일처럼 오버라이드 주입)
SHARED_STYLE_MAP = {
    "80-misc.typ": "figure",
}
PRE_TOC_MARKER = "// ── PRE_TOC_CONTENT ──"

# variants.json 위치 (커스텀 변형 저장소)
VARIANTS_FILE = Path(__file__).resolve().parents[2] / "pub-studio" / "references" / "variants.json"

# CSS property key → Typst variable name
# prefix_camelCase → typst-kebab-case
COMPONENT_STYLE_MAP = {
    "heading": {
        "h1_marginTop": "h1-top",
        "h1_fontWeight": "h1-weight",
        "h1_color": "h1-fill",
        "h1_marginBottom": "h1-below",
        "h2_marginTop": "h2-top",
        "h2_fontWeight": "h2-weight",
        "h2_color": "h2-fill",
        "h2_paddingLeft": "h2-inset-left",
        "h2_marginBottom": "h2-below",
        "h3_marginTop": "h3-top",
        "h3_fontWeight": "h3-weight",
        "h3_color": "h3-fill",
        "h3_marginBottom": "h3-below",
        "h4_marginTop": "h4-top",
        "h4_fontWeight": "h4-weight",
        "h4_color": "h4-fill",
        "h4_marginBottom": "h4-below",
    },
    "body": {
        "p_textIndent": "_set_par_indent",
        "p_textAlign": "_set_par_justify",
        "strong_fontWeight": "_show_strong_weight",
        "strong_color": "strong-fill",
        "emph_color": "emph-fill",
    },
    "code": {
        "background": "code-fill",
        "borderRadius": "code-radius",
        "code_marginTop": "code-margin-top",
        "code_marginBottom": "code-margin-bottom",
        "code_paddingX": "code-inset-x",
        "code_paddingY": "code-inset-y",
    },
    "inline_code": {
        "color": "inline-code-text-color",
        "fontWeight": "inline-code-weight",
        "background": "inline-code-fill",
        "borderRadius": "inline-code-radius",
    },
    "quote": {
        "color": "quote-text-color",
        "background": "color-quote-bg",
        "quote_marginTop": "quote-margin-top",
        "quote_marginBottom": "quote-margin-bottom",
    },
    "table": {
        "th_color": "table-header-text-color",
        "th_fontWeight": "table-header-weight",
        "oddTd_background": "table-odd-fill",
        "table_marginTop": "table-margin-top",
        "table_marginBottom": "table-margin-bottom",
    },
    "figure": {
        "figure_marginTop": "figure-margin-top",
        "figure_marginBottom": "figure-margin-bottom",
        "figure_captionGap": "figure-caption-gap",
        "figure_captionSize": "figure-caption-size",
    },
}


def _css_value_to_typst(key: str, value: str) -> str:
    """CSS 속성값을 Typst 값으로 변환."""
    if not value:
        return ""

    # 특수 핸들러 (body set rules)
    if key.startswith("_set_"):
        return value

    # weight: CSS number → Typst int, named → Typst string
    if "weight" in key.lower() or "Weight" in key:
        if value.isdigit():
            return value  # 800 → 800 (정수)
        return f'"{value}"'  # "bold" → "bold" (문자열)

    # color: hex → rgb(), var() → 무시
    if "color" in key.lower() or "fill" in key.lower() or "Color" in key:
        if value.startswith("var("):
            return ""
        if value.startswith("#"):
            return f'rgb("{value}")'
        return ""

    # length: px/pt/em → Typst length
    m = re.match(r"^([\d.]+)\s*(px|pt|em|mm)?$", value)
    if m:
        num, unit = m.group(1), m.group(2) or "pt"
        if unit == "px":
            unit = "pt"
        return f"{num}{unit}"

    return f'"{value}"'


def generate_component_override(component: str, props: dict) -> str:
    """단일 컴포넌트의 componentStyles → Typst 오버라이드 스니펫.

    heading, code 등: #let 변수 오버라이드
    body: #set par() 오버라이드
    """
    if not props:
        return ""

    style_map = COMPONENT_STYLE_MAP.get(component, {})
    if not style_map:
        return ""

    lines = []

    for css_key, typst_target in style_map.items():
        val = props.get(css_key)
        if val is None:
            continue

        # body: #set rules
        if typst_target == "_set_par_indent":
            typst_val = _css_value_to_typst("length", val)
            if typst_val:
                lines.append(f"#set par(first-line-indent: {typst_val})")
        elif typst_target == "_set_par_justify":
            if val == "justify":
                lines.append("#set par(justify: true)")
            else:
                lines.append("#set par(justify: false)")
        elif typst_target == "_show_strong_weight":
            # CSS font-weight → Typst weight
            weight_map = {"400": "regular", "500": "medium", "600": "semibold",
                          "700": "bold", "800": "extrabold", "900": "black"}
            tw = weight_map.get(str(val), str(val))
            lines.append(f'#show strong: set text(weight: "{tw}")')
        else:
            # #let variable override
            typst_val = _css_value_to_typst(typst_target, val)
            if typst_val:
                lines.append(f"#let {typst_target} = {typst_val}")

    return "\n".join(lines)


def load_preset(preset_id: str) -> dict[str, str]:
    """프리셋 ID로 컴포넌트 선택 딕셔너리를 로드"""
    presets_path = COMPONENTS_DIR / "presets.json"
    with open(presets_path, encoding="utf-8") as f:
        presets = json.load(f)
    if preset_id not in presets:
        available = ", ".join(presets.keys())
        raise ValueError(f"프리셋 '{preset_id}' 없음. 사용 가능: {available}")
    return dict(presets[preset_id]["components"])


def load_preset_overrides(preset_id: str) -> dict:
    """프리셋의 overrides를 design_state 형식으로 반환. 없으면 빈 dict."""
    presets_path = COMPONENTS_DIR / "presets.json"
    with open(presets_path, encoding="utf-8") as f:
        presets = json.load(f)
    return dict(presets.get(preset_id, {}).get("overrides", {}))


def parse_design_arg(arg: str) -> dict[str, str]:
    """디자인 인자를 파싱하여 컴포넌트 선택 딕셔너리로 변환

    '1' 또는 '2'       → 프리셋 로드
    'body=2,heading=1'  → 기본 프리셋 1 + 오버라이드
    """
    arg = arg.strip()
    # 프리셋 번호(숫자)면 해당 프리셋 로드
    presets_path = COMPONENTS_DIR / "presets.json"
    with open(presets_path, encoding="utf-8") as f:
        all_presets = json.load(f)
    if arg in all_presets:
        return load_preset(arg)

    # 믹스매치: 기본값은 프리셋 1, 지정된 키만 오버라이드
    selection = load_preset("1")
    parts = [p.strip() for p in arg.split(",")]
    for part in parts:
        if "=" not in part:
            raise ValueError(f"잘못된 형식: '{part}'. 'key=value' 형태 필요")
        key, val = part.split("=", 1)
        key = key.strip()
        val = val.strip()
        if key not in VARIANT_KEYS:
            available = ", ".join(VARIANT_KEYS)
            raise ValueError(f"알 수 없는 컴포넌트: '{key}'. 사용 가능: {available}")
        selection[key] = f"d{val}" if not val.startswith("d") else val
    return selection


def generate_overrides(design_state: dict) -> tuple[str, str, str]:
    """에디터 디자인 상태 → (변수 오버라이드, 페이지 오버라이드, 크기 오버라이드) Typst 스니펫

    크기 오버라이드는 body 컴포넌트 직후(Slot 2.5)에 주입되어
    body_d2.typ의 재정의를 덮어쓸 수 있다.
    """
    var_lines = []
    page_lines = []
    size_lines = []

    # 색상 (#let — show rules 전에)
    colors = design_state.get("colors", {})
    COLOR_MAP = {
        "primary": "color-primary",
        "text": "color-text",
        "codeText": "color-code-text",
        "quoteBg": "color-quote-bg",
    }
    for js_key, typst_var in COLOR_MAP.items():
        val = colors.get(js_key)
        if val:
            var_lines.append(f'#let {typst_var} = rgb("{val}")')
    if colors.get("primary"):
        var_lines.append('#let color-primary-dark = color-primary.darken(15%)')
        var_lines.append('#let color-primary-light = color-primary.lighten(40%)')

    # 인용 테두리: quoteBg에서 파생
    if colors.get("quoteBg"):
        var_lines.append('#let color-quote-border = color-quote-bg.darken(30%)')

    # 이미지 변수 오버라이드
    images = design_state.get("images", {})
    IMAGE_MAP = {
        "gemini": ("img-gemini-width", "img-gemini-style"),
        "terminal": ("img-terminal-width", "img-terminal-style"),
        "diagram": ("img-diagram-width", "img-diagram-style"),
    }
    for category, (width_var, style_var) in IMAGE_MAP.items():
        img_cfg = images.get(category, {})
        width = img_cfg.get("width")
        if width is not None:
            var_lines.append(f'#let {width_var} = {width / 100}')
        preset = img_cfg.get("preset")
        if preset:
            var_lines.append(f'#let {style_var} = "{preset}"')

    # 타이포그래피 변수 (#let)
    typo = design_state.get("typo", {})
    if typo.get("leading") is not None:
        var_lines.append(f'#let body-leading = {typo["leading"]}pt')
    if typo.get("tracking") is not None:
        var_lines.append(f'#let body-tracking = {typo["tracking"]}pt')
    if typo.get("paragraphGap") is not None:
        var_lines.append(f'#let paragraph-gap = {typo["paragraphGap"]}pt')

    # 본문 타이포 오버라이드 (Slot 2.5: body 직후 → 항상 우선)
    if typo.get("size"):
        size_lines.append(f'#set text(size: {typo["size"]}pt)')
    if typo.get("leading") is not None:
        size_lines.append(f'#set par(leading: {typo["leading"]}pt)')
    if typo.get("tracking") is not None:
        size_lines.append(f'#set text(tracking: {typo["tracking"]}pt)')
    # paragraphGap은 변수로 처리 (show par: set block(below:)에서 사용)
    # #set par(spacing:)는 사용하지 않음 — 모든 블록에 영향을 주기 때문

    # 개별 요소 크기 (Slot 2.5: body 직후, heading/code 직전)
    typo_sizes = design_state.get("typoSizes", {})
    SIZE_MAP = {
        "h1": "h1-size", "h2": "h2-size", "h3": "h3-size", "h4": "h4-size",
        "code": "code-size",
        "quote": "quote-size", "table": "table-size", "inlineCode": "inline-code-size",
    }
    for js_key, typst_var in SIZE_MAP.items():
        val = typo_sizes.get(js_key)
        if val is not None:
            size_lines.append(f'#let {typst_var} = {val}pt')

    # 목차 깊이
    toc_depth = design_state.get("tocDepth")
    if toc_depth is not None:
        size_lines.append(f'#let toc-depth = {int(toc_depth)}')

    # 목차 간격 (문단 간격과 독립)
    toc_spacing = design_state.get("tocSpacing")
    if toc_spacing is not None:
        size_lines.append(f'#let toc-spacing = {toc_spacing}pt')

    # 페이지 (#set page — cascading)
    PAGE_SIZES = {
        "A4_국배판": (210, 297), "B5_4x6배판": (188, 254),
        "크라운판": (176, 248), "신국판": (152, 225),
        "A5_국판": (148, 210), "A6_국반판": (105, 148),
    }
    page = design_state.get("page", {})
    margins = design_state.get("margins", {})

    page_parts = []
    fmt = page.get("format")
    if fmt and fmt in PAGE_SIZES:
        w, h = PAGE_SIZES[fmt]
        page_parts.append(f"width: {w}mm")
        page_parts.append(f"height: {h}mm")
    if margins:
        m_parts = []
        for key in ("top", "bottom", "left", "right"):
            if key in margins:
                m_parts.append(f"{key}: {margins[key]}mm")
        if m_parts:
            page_parts.append(f"margin: ({', '.join(m_parts)})")
    if page_parts:
        page_lines.append(f"#set page({', '.join(page_parts)})")

    return ("\n".join(var_lines), "\n".join(page_lines), "\n".join(size_lines))


def _load_custom_variant(component: str, variant_id: str) -> dict | None:
    """variants.json에서 커스텀 변형의 properties를 로드."""
    if not VARIANTS_FILE.exists():
        return None
    try:
        with open(VARIANTS_FILE, encoding="utf-8") as f:
            store = json.load(f)
        return store.get("variants", {}).get(component, {}).get(variant_id)
    except (json.JSONDecodeError, KeyError):
        return None


def _inject_at_marker(content: str, override: str) -> str:
    """파일 내용의 // ──OVERRIDES── 마커 위치에 오버라이드를 주입.

    마커가 없으면 파일 앞에 주입 (fallback).
    """
    if OVERRIDE_MARKER in content:
        before, after = content.split(OVERRIDE_MARKER, 1)
        return before + OVERRIDE_MARKER + f"\n{override}\n" + after
    return f"{override}\n{content}"


def assemble_book_base(selection: dict[str, str],
                       design_state: dict | None = None,
                       skip_cover: bool = False,
                       skip_toc: bool = False) -> str:
    """선택된 컴포넌트를 결합하여 완성된 book_base Typst 문자열 반환

    design_state가 주어지면 변수/페이지 오버라이드를 적절한 위치에 주입.
    skip_cover=True면 90-cover.typ 건너뜀.
    skip_toc=True면 toc_*.typ 건너뜀.
    """
    var_override, page_override, size_override = ("", "", "")
    component_styles = {}
    if design_state:
        var_override, page_override, size_override = generate_overrides(design_state)
        component_styles = design_state.get("componentStyles", {})

    parts = []
    for i, (subdir, pattern) in enumerate(ASSEMBLY_ORDER):
        # 표지/목차 스킵
        if skip_cover and pattern == "90-cover.typ":
            continue
        if skip_toc and "{sel}" in pattern and pattern.split("_{sel}")[0] == "toc":
            continue

        if "{sel}" in pattern:
            key = pattern.split("_{sel}")[0]
            filename = pattern.replace("{sel}", selection[key])
        else:
            key = None
            filename = pattern
        filepath = COMPONENTS_DIR / subdir / filename

        # d3+ 커스텀 변형: .typ 파일 없으면 d1 기반 + variants.json 오버라이드
        custom_variant_props = None
        if not filepath.exists() and key:
            variant_id = selection[key]
            if variant_id not in ("d1", "d2"):
                custom_variant_props = _load_custom_variant(key, variant_id)
                fallback = pattern.replace("{sel}", "d1")
                filepath = COMPONENTS_DIR / subdir / fallback
            if not filepath.exists():
                raise FileNotFoundError(f"컴포넌트 파일 없음: {filepath}")

        file_content = filepath.read_text(encoding="utf-8")

        # 커스텀 변형 properties → 오버라이드 주입
        if custom_variant_props:
            props = {k: v for k, v in custom_variant_props.items() if k != "name"}
            comp_override = generate_component_override(key, props)
            if comp_override:
                file_content = _inject_at_marker(
                    file_content,
                    f"// ── custom variant: {key}/{selection[key]} ──\n{comp_override}",
                )

        # 변형 파일에 componentStyles 오버라이드 주입 (마커 기반)
        style_key = key or SHARED_STYLE_MAP.get(filename)
        if style_key and component_styles.get(style_key):
            comp_override = generate_component_override(style_key, component_styles[style_key])
            if comp_override:
                file_content = _inject_at_marker(
                    file_content,
                    f"// ── componentStyles: {style_key} ──\n{comp_override}",
                )

        parts.append(file_content)

        # Slot: PRE_TOC 마커 (90-cover 직후, toc 직전)
        if pattern == "90-cover.typ" and not skip_cover:
            parts.append(f"\n{PRE_TOC_MARKER}\n")

        # Slot 0.5: 변수 오버라이드 (00-variables 직후)
        if i == 0 and var_override:
            parts.append(f"\n// ── Editor Design Overrides (variables) ──\n{var_override}\n")
        # Slot 1.5: 페이지 오버라이드 (01-page 직후)
        if i == 1 and page_override:
            parts.append(f"\n// ── Editor Design Overrides (page) ──\n{page_override}\n")
        # Slot 2.5: 크기 오버라이드 (body 직후, heading/code 직전)
        if i == 2 and size_override:
            parts.append(f"\n// ── Editor Design Overrides (sizes) ──\n{size_override}\n")

    return "\n".join(parts)


if __name__ == "__main__":
    import sys

    arg = sys.argv[1] if len(sys.argv) > 1 else "1"
    sel = parse_design_arg(arg)
    print(f"선택: {sel}")
    result = assemble_book_base(sel)
    print(f"결합 완료: {len(result)} chars, {result.count(chr(10))} lines")
