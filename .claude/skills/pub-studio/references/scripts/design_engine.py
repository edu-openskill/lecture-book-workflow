"""디자인 엔진 — design_assembler.py 래핑

컴포넌트 조립 + 오버라이드 생성을 OOP 인터페이스로 제공.
내부적으로 design_assembler 모듈에 100% 위임.
"""

from __future__ import annotations

import sys
from pathlib import Path

from models import DesignState

# design_assembler.py 위치를 sys.path에 추가
_SCRIPTS_DIR = (
    Path(__file__).resolve().parents[3]
    / "pub-build"
    / "references"
    / "scripts"
)


def _get_assembler():
    if str(_SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(_SCRIPTS_DIR))
    import design_assembler
    return design_assembler


class DesignEngine:
    """디자인 컴포넌트 조립 + 오버라이드 생성."""

    def parse_design_arg(self, arg: str) -> dict[str, str]:
        """디자인 인자를 파싱하여 컴포넌트 선택 딕셔너리로 변환.

        '1' 또는 '2'       → 프리셋 로드
        'body=2,heading=1'  → 기본 프리셋 1 + 오버라이드
        """
        da = _get_assembler()
        return da.parse_design_arg(arg)

    def generate_overrides(self, design_state: DesignState) -> tuple[str, str, str]:
        """(변수 오버라이드, 페이지 오버라이드, 크기 오버라이드) Typst 스니펫 생성."""
        da = _get_assembler()
        return da.generate_overrides(design_state.to_server_dict())

    def assemble_book_base(
        self,
        selection: dict[str, str],
        design_state: DesignState | None = None,
        skip_cover: bool = False,
        skip_toc: bool = False,
    ) -> str:
        """선택된 컴포넌트를 결합하여 완성된 book_base Typst 문자열 반환."""
        da = _get_assembler()
        ds_dict = design_state.to_server_dict() if design_state else None
        return da.assemble_book_base(
            selection,
            design_state=ds_dict,
            skip_cover=skip_cover,
            skip_toc=skip_toc,
        )

    def build_design_arg(self, design_state: DesignState) -> str | None:
        """DesignState.components → design_arg 문자열.

        예: 'body=d1,heading=d2' 또는 프리셋이면 '1'.
        """
        components = design_state.components
        if not components:
            return None
        vals = set(components.values())
        if vals == {"d1"}:
            return "1"
        if vals == {"d2"}:
            return "2"
        parts = [f"{k}={v}" for k, v in components.items()]
        return ",".join(parts)
