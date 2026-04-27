"""ParentDocumentRetriever -- 자식 청크로 검색하고 부모(원본) 문서를 반환합니다."""

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


class ParentDocumentRetriever:
    """자식 청크로 검색 -> 부모(원본) 문서 반환."""

    def __init__(
        self,
        parent_docs: list[dict],
        child_chunks: list[dict],
        embeddings: Any | None = None,
    ) -> None:
        self.parent_docs = {doc["id"]: doc for doc in parent_docs}
        self.child_chunks = child_chunks
        self.embeddings = embeddings
        self._child_vectors: list[list[float]] | None = None

        if self.embeddings is not None:
            self._child_vectors = self.embeddings.embed_documents(
                [c["content"] for c in self.child_chunks]
            )

    def search(self, query: str, top_k: int = 2) -> list[dict]:
        """자식 청크에서 유사도가 높은 것을 찾고, 해당 부모 문서를 반환합니다."""
        # TODO: 자식 청크로 검색하고 부모 문서를 반환합니다.
        pass
