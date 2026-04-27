"""레이아웃 분석기 — pdf_layout_checker.py 래핑 + 심각도 분류

PDF를 분석하여 레이아웃 이슈를 감지하고,
자동 수정 가능 여부에 따라 분류한다.
"""

from __future__ import annotations

import sys
from pathlib import Path

from models import LayoutIssue, ImageInfo

# pdf_layout_checker.py 위치
_CHECKER_DIR = (
    Path(__file__).resolve().parents[3]
    / "pub-layout-check"
    / "references"
    / "scripts"
)


def _get_checker():
    if str(_CHECKER_DIR) not in sys.path:
        sys.path.insert(0, str(_CHECKER_DIR))
    import pdf_layout_checker
    return pdf_layout_checker


class LayoutChecker:
    """PDF 레이아웃 분석 + 자동수정 가능 여부 분류."""

    AUTO_FIXABLE_TYPES = {"blank_page", "orphan_content", "large_image"}

    # 이미지 width 축소 단계
    WIDTH_STEPS = [0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3]

    def __init__(self, skip_pages: set[int] | None = None):
        self._skip_pages = skip_pages or {1, 2}

    def analyze(self, pdf_path: Path) -> list[LayoutIssue]:
        """PDF 레이아웃 분석 → LayoutIssue 목록.

        pdf_layout_checker.analyze_layout()에 위임 후
        결과를 LayoutIssue 데이터 클래스로 변환.
        """
        checker = _get_checker()
        raw_issues = checker.analyze_layout(str(pdf_path), skip_pages=self._skip_pages)

        issues = []
        for raw in raw_issues:
            issue_type = raw.get("type", "unknown")
            severity = (
                "auto_fixable" if issue_type in self.AUTO_FIXABLE_TYPES else "manual"
            )
            issues.append(LayoutIssue(
                page=raw.get("page", 0),
                issue_type=issue_type,
                severity=severity,
                message=raw.get("message", ""),
                suggestion=raw.get("suggestion", ""),
            ))
        return issues

    def classify_issues(
        self, issues: list[LayoutIssue]
    ) -> tuple[list[LayoutIssue], list[LayoutIssue]]:
        """이슈를 (auto_fixable, manual)로 분리."""
        auto = [i for i in issues if i.severity == "auto_fixable"]
        manual = [i for i in issues if i.severity == "manual"]
        return auto, manual

    def suggest_fixes(
        self,
        issues: list[LayoutIssue],
        images: list[ImageInfo],
    ) -> list[LayoutIssue]:
        """자동수정 가능 이슈에 구체적 수정 액션을 채움.

        - large_image: 해당 페이지 이미지 width를 다음 단계로 축소
        - orphan_content: 이전 페이지 최대 이미지 width 5% 감소
        - blank_page: pagebreak 제거 플래그
        """
        # 이미지를 경로로 인덱싱
        img_by_path = {img.rel_path: img for img in images}

        for issue in issues:
            if issue.issue_type == "large_image":
                issue.fix_action = "reduce_image_width"
                # 가장 큰 이미지를 축소 대상으로 (단순 휴리스틱)
                if images:
                    # 현재 페이지의 이미지를 특정할 수 없으므로
                    # 가장 넓은 이미지를 대상으로
                    widest = max(images, key=lambda i: i.effective_width)
                    issue.image_path = widest.rel_path
                    issue.current_width = widest.effective_width
                    issue.target_width = self._next_step_down(widest.effective_width)

            elif issue.issue_type == "orphan_content":
                issue.fix_action = "reduce_nearby_image"
                if images:
                    widest = max(images, key=lambda i: i.effective_width)
                    issue.image_path = widest.rel_path
                    issue.current_width = widest.effective_width
                    issue.target_width = max(
                        widest.effective_width - 0.05, 0.3
                    )

            elif issue.issue_type == "blank_page":
                issue.fix_action = "remove_pagebreak"

        return issues

    def get_page_usage(self, pdf_path: Path) -> list[dict]:
        """페이지별 사용률 (UI 바 차트용)."""
        checker = _get_checker()
        try:
            import fitz
        except ImportError:
            return []

        doc = fitz.open(str(pdf_path))
        result = []
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            page_num = page_idx + 1

            if page_num in self._skip_pages:
                result.append({"page": page_num, "usage": 100, "label": "표지/목차"})
                continue

            content_top = checker.TOP_MARGIN_PT
            content_bottom = checker.A4_HEIGHT_PT - checker.BOTTOM_MARGIN_PT
            blocks = page.get_text("dict")["blocks"]
            content_blocks = [
                b for b in blocks
                if b["type"] in (0, 1)
                and b["bbox"][1] >= content_top - 5
                and b["bbox"][3] <= content_bottom + 5
            ]

            if not content_blocks:
                result.append({"page": page_num, "usage": 0, "label": "빈 페이지"})
                continue

            max_y = max(b["bbox"][3] for b in content_blocks)
            usage = min(
                (max_y - content_top) / checker.CONTENT_HEIGHT * 100, 100
            )
            label = ""
            if usage < 30:
                label = "고아"
            elif usage < 50:
                label = "빈 공간"
            result.append({"page": page_num, "usage": round(usage, 1), "label": label})

        doc.close()
        return result

    def _next_step_down(self, current: float) -> float:
        """현재 width보다 한 단계 작은 값 반환."""
        for step in self.WIDTH_STEPS:
            if step < current - 0.01:
                return step
        return 0.3  # 최소값
