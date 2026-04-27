"""ContextualCompressionRetriever -- 검색 후 관련 문장만 압축하여 반환합니다."""

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


def _compress(query: str, document: str) -> str:
    """문서에서 쿼리와 관련된 문장만 추출합니다 (ContextualCompression 핵심)."""
    query_words = set(query.lower().split())
    sentences = [s.strip() for s in document.replace("\n", ". ").split(".") if s.strip()]

    relevant: list[str] = []
    for sentence in sentences:
        sentence_words = set(sentence.lower().split())
        overlap = len(query_words & sentence_words)
        if overlap >= 1 and len(sentence) > 10:
            relevant.append(sentence)

    return ". ".join(relevant[:3]) if relevant else document[:100]


class ContextualCompressionRetriever:
    """검색 후 관련 문장만 압축하여 반환."""

    def __init__(
        self,
        documents: list[dict],
        embeddings: Any | None = None,
    ) -> None:
        self.documents = documents
        self.embeddings = embeddings

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """검색 + 압축을 수행합니다."""
        # TODO: 검색 결과에서 질문과 관련된 문장만 압축합니다.
        pass
