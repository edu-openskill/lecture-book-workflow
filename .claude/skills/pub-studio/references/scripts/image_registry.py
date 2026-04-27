"""이미지 레지스트리 — 개별 이미지 추적 + 오버라이드

Stage 1에서 감지된 모든 이미지를 추적하고,
사용자의 개별 이미지 오버라이드를 Stage 2에서 적용한다.
"""

from __future__ import annotations

import re
from pathlib import Path

from models import ImageInfo

# #auto-image("path", alt: [...], max-width: 0.7, style: "plain") 파싱용
# style은 "quoted" 또는 variable-name 모두 매칭
_AUTO_IMAGE_RE = re.compile(
    r'#auto-image\(\s*"([^"]+)"'          # 경로 (group 1)
    r'(?:,\s*alt:\s*\[([^\]]*)\])?'        # alt (group 2, captured)
    r'(?:,\s*max-width:\s*([\w.\-]+))?'    # max-width (group 3) — 숫자 or 변수명
    r'(?:,\s*style:\s*(?:"([^"]*)"|[\w\-]+))?' # style (group 4, quoted만 캡처)
    r'[^)]*\)'                             # 나머지 인자 + 닫기
)

# 카테고리 감지 패턴
_CH_RE = re.compile(r'CH(\d+)', re.IGNORECASE)


def _compute_figure_labels(images: dict):
    """챕터 기반 그림 번호를 각 ImageInfo에 할당."""
    ch_counters = {}
    front_counter = 0
    for img in sorted(images.values(), key=lambda i: i.rel_path):
        m = _CH_RE.search(img.rel_path)
        if m:
            ch = int(m.group(1))
            ch_counters[ch] = ch_counters.get(ch, 0) + 1
            img.figure_label = f"그림 {ch}-{ch_counters[ch]}"
        else:
            front_counter += 1
            img.figure_label = f"그림 서-{front_counter}"


_CATEGORY_PATTERNS = {
    "gemini": re.compile(r"gemini|concept|개념", re.IGNORECASE),
    "terminal": re.compile(r"terminal|console|터미널", re.IGNORECASE),
    "diagram": re.compile(r"diagram|flow|흐름|mermaid", re.IGNORECASE),
}


def _detect_category(path: str) -> str:
    """경로에서 이미지 카테고리를 추론."""
    for cat, pattern in _CATEGORY_PATTERNS.items():
        if pattern.search(path):
            return cat
    return "default"


def _parse_width(raw: str | None) -> float:
    """max-width 값을 float로 변환. 변수명이면 기본값 0.7."""
    if raw is None:
        return 0.7
    try:
        return float(raw)
    except ValueError:
        # 변수 참조 (img-gemini-width 등) → 카테고리 기본값
        if "gemini" in raw:
            return 0.7
        if "terminal" in raw:
            return 0.7
        if "diagram" in raw:
            return 0.6
        return 0.7


class ImageRegistry:
    """Stage 1에서 감지된 이미지를 추적하고, 개별 오버라이드를 적용."""

    def __init__(self):
        self._images: dict[str, ImageInfo] = {}  # path → ImageInfo

    def scan_raw_typ(self, raw_typ: str) -> list[ImageInfo]:
        """raw .typ에서 #auto-image() 호출을 파싱하여 이미지 목록 구축.

        기존 이미지의 오버라이드는 보존하면서 목록을 갱신한다.
        """
        found: dict[str, ImageInfo] = {}

        for match in _AUTO_IMAGE_RE.finditer(raw_typ):
            path = match.group(1)
            alt = match.group(2) or ""
            raw_width = match.group(3)
            style = match.group(4) or "plain"

            # 기존 오버라이드 보존
            existing = self._images.get(path)
            override_width = existing.override_width if existing else None
            override_style = existing.override_style if existing else None

            category = _detect_category(path)
            default_width = _parse_width(raw_width)

            # 상대 경로 추출 (assets/ 이하)
            rel_path = path
            if "/assets/" in path:
                rel_path = "assets/" + path.split("/assets/", 1)[1]

            found[path] = ImageInfo(
                path=path,
                rel_path=rel_path,
                category=category,
                default_width=default_width,
                default_style=style,
                override_width=override_width,
                override_style=override_style,
                alt=alt,
            )

        _compute_figure_labels(found)
        self._images = found
        return list(found.values())

    def get_all(self) -> list[ImageInfo]:
        """모든 등록된 이미지를 경로순으로 반환."""
        return sorted(self._images.values(), key=lambda i: i.rel_path)

    def get_by_category(self, category: str) -> list[ImageInfo]:
        """카테고리별 이미지 필터링."""
        return [i for i in self._images.values() if i.category == category]

    def set_override(
        self,
        path: str,
        width: float | None = None,
        style: str | None = None,
    ):
        """특정 이미지에 개별 오버라이드 설정."""
        if path in self._images:
            img = self._images[path]
            if width is not None:
                img.override_width = width
            if style is not None:
                img.override_style = style

    def load_overrides(self, overrides: dict[str, dict]):
        """design_state.imageOverrides에서 벌크 로드.

        overrides 형식: {"path/to/image.png": {"width": 60, "style": "bordered"}}
        width는 0~100 퍼센트 → 0.0~1.0으로 변환.
        """
        for path, cfg in overrides.items():
            # 절대 경로 또는 상대 경로로 매칭 시도
            target = self._find_image(path)
            if target is None:
                continue
            if "width" in cfg:
                w = cfg["width"]
                target.override_width = w / 100 if w > 1 else w
            if "style" in cfg:
                target.override_style = cfg["style"]

    def clear_overrides(self):
        """모든 개별 오버라이드 제거."""
        for img in self._images.values():
            img.override_width = None
            img.override_style = None

    def apply_overrides(self, raw_typ: str) -> str:
        """오버라이드가 있는 이미지의 max-width/style을 교체.

        오버라이드 없는 이미지는 원본 그대로 (카테고리 변수 참조 유지).
        """
        result = raw_typ

        for path, img in self._images.items():
            if img.override_width is None and img.override_style is None:
                continue

            # 해당 이미지의 #auto-image 라인을 찾아 교체
            escaped_path = re.escape(path)
            pattern = re.compile(
                rf'(#auto-image\(\s*"{escaped_path}"[^)]*?)'
                rf'max-width:\s*[\w.\-]+'
                rf'([^)]*)\)'
            )

            def _replace_width(m):
                prefix = m.group(1)
                suffix = m.group(2)
                new_width = f"max-width: {img.effective_width}"

                # style도 교체
                if img.override_style is not None:
                    suffix = re.sub(
                        r'style:\s*"[^"]*"',
                        f'style: "{img.effective_style}"',
                        suffix,
                    )
                return f"{prefix}{new_width}{suffix})"

            result = pattern.sub(_replace_width, result)

        return result

    def reduce_image_width(self, path: str, step: float = 0.05) -> float:
        """자동 수정용: 이미지 width를 한 단계 축소.

        현재 effective_width에서 step만큼 감소. 최소 0.3.
        반환값: 새 effective_width.
        """
        target = self._find_image(path)
        if target is None:
            return 0.7

        current = target.effective_width
        new_width = max(current - step, 0.3)
        target.override_width = round(new_width, 2)
        return target.effective_width

    def to_dict(self) -> dict:
        """API 응답용 직렬화."""
        return {
            "images": [img.to_dict() for img in self.get_all()],
            "count": len(self._images),
        }

    def _find_image(self, path: str) -> ImageInfo | None:
        """절대 경로, 상대 경로, 파일명으로 이미지 검색."""
        # 직접 매칭
        if path in self._images:
            return self._images[path]
        # 상대 경로 매칭
        for img in self._images.values():
            if img.rel_path == path or img.path.endswith(path):
                return img
        return None
