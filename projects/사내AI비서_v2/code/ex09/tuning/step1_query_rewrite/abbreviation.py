"""약어/동의어 확장 -- ABBREVIATION_MAP, SYNONYM_MAP을 사용하여 쿼리를 풀어씁니다."""

from __future__ import annotations

from .data import ABBREVIATION_MAP, SYNONYM_MAP


def expand_abbreviations(query: str) -> dict:
    """쿼리의 약어와 동의어를 확장합니다.

    Returns:
        {"original": str, "expanded": str, "applied": list[str]}
    """
    # TODO: 쿼리의 약어와 동의어를 확장합니다.
    pass
