"""SelfQueryRetriever -- 쿼리에서 메타데이터 필터를 자동 추출하여 필터링 검색합니다."""

from __future__ import annotations

import math
from typing import Any


# ---------------------------------------------------------------------------
# 헬퍼
# ---------------------------------------------------------------------------

def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """두 벡터의 코사인 유사도를 계산합니다."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class SelfQueryRetriever:
    """쿼리에서 메타데이터 필터를 자동 추출하여 필터링 검색."""

    def __init__(
        self,
        documents: list[dict],
        topic_keywords: dict[str, list[str]] | None = None,
        embeddings: Any | None = None,
    ) -> None:
        self.documents = documents
        self.topic_keywords = topic_keywords or {}
        self.embeddings = embeddings

    def extract_filter(self, query: str) -> dict[str, str]:
        """쿼리에서 메타데이터 필터를 추출합니다."""
        filters: dict[str, str] = {}
        query_lower = query.lower()

        for topic, keywords in self.topic_keywords.items():
            if any(kw in query_lower for kw in keywords):
                filters["topic"] = topic
                break

        return filters

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """메타데이터 자동 필터링으로 검색합니다."""
        # TODO: 쿼리에서 메타데이터 필터를 추출하고 필터링 검색합니다.
        pass
