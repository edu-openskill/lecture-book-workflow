"""Multi-Query -- 하나의 질문을 여러 관점으로 재작성하고 병합 검색합니다."""

from __future__ import annotations

import math
import os
from typing import Any

from rich.console import Console

console = Console()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")


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


def _call_ollama(prompt: str) -> str | None:
    """Ollama API를 httpx로 호출합니다. 실패 시 None 반환."""
    try:
        import httpx

        resp = httpx.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=60.0,
        )
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except Exception as exc:
        console.print(f"[yellow]Ollama 호출 실패: {exc}[/yellow]")
        return None


def _call_openai(prompt: str) -> str | None:
    """OpenAI API를 호출합니다. 실패 시 None 반환."""
    try:
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content.strip()
    except Exception as exc:
        console.print(f"[yellow]OpenAI 호출 실패: {exc}[/yellow]")
        return None


def _call_llm(prompt: str) -> str | None:
    """LLM_PROVIDER 환경변수에 따라 Ollama 또는 OpenAI를 호출합니다."""
    if LLM_PROVIDER == "openai" and OPENAI_API_KEY:
        return _call_openai(prompt)
    return _call_ollama(prompt)


# ---------------------------------------------------------------------------
# 점수 계산 / 검색 헬퍼
# ---------------------------------------------------------------------------

def _score_with_embedding(
    text: str,
    documents: list[dict],
    embeddings: Any,
) -> list[tuple[float, dict]]:
    """임베딩 기반으로 텍스트와 문서들의 유사도를 계산합니다."""
    text_vec = embeddings.embed_query(text)
    doc_vecs = embeddings.embed_documents([d["content"] for d in documents])
    return [
        (_cosine_similarity(text_vec, dv), doc)
        for dv, doc in zip(doc_vecs, documents)
    ]


def _score_with_keyword(
    text: str,
    documents: list[dict],
) -> list[tuple[float, dict]]:
    """키워드 매칭으로 텍스트와 문서들의 유사도를 계산합니다."""
    words = set(text.lower().split())
    scored: list[tuple[float, dict]] = []
    for doc in documents:
        dw = set(doc["content"].lower().split())
        s = len(words & dw) / len(words) if words else 0.0
        scored.append((s, doc))
    return scored


def _to_results(
    scored: list[tuple[float, dict]],
    top_k: int = 3,
) -> list[dict]:
    """점수 리스트를 정렬하여 상위 top_k개 결과 딕셔너리로 변환합니다."""
    scored_sorted = sorted(scored, key=lambda x: x[0], reverse=True)
    return [
        {
            "content": doc["content"],
            "source": doc.get("source", ""),
            "score": round(score, 4),
        }
        for score, doc in scored_sorted[:top_k]
    ]


def _generate_queries_rule(query: str, num_queries: int = 3) -> list[str]:
    """규칙 기반으로 다양한 쿼리를 생성합니다 (LLM fallback)."""
    console.print("[dim]  (규칙 기반 Multi-Query fallback 사용)[/dim]")
    return [
        query,
        f"{query}에 대한 규정이 있습니까?",
        f"{query} 관련 정책 안내",
        f"{query} 절차 및 방법",
    ][:num_queries + 1]


# ---------------------------------------------------------------------------
# 공개 함수
# ---------------------------------------------------------------------------

def generate_multi_queries(
    query: str,
    num_queries: int = 3,
) -> list[str]:
    """다양한 관점의 쿼리를 생성합니다. LLM 실패 시 규칙 기반 fallback."""
    prompt = (
        f"다음 질문을 {num_queries}가지 다른 방식으로 재표현하십시오.\n"
        "각 질문은 같은 정보를 구하지만 다른 표현 방식을 사용해야 합니다.\n"
        "번호 없이 각 질문을 한 줄씩 출력하십시오.\n\n"
        f"원본 질문: {query}\n\n"
        "재표현된 질문들:"
    )
    # TODO: LLM을 호출하고 결과를 줄 단위로 파싱합니다.
    pass


def search_multi_query(
    queries: list[str],
    documents: list[dict],
    embeddings: Any | None = None,
    top_k: int = 3,
) -> list[dict]:
    """다중 쿼리로 검색하고 결과를 병합합니다."""
    # TODO: 다중 쿼리 각각으로 검색하고 최고 점수 기준으로 병합합니다.
    pass
