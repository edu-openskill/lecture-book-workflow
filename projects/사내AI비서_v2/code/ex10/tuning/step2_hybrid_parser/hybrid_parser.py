"""step2 — 하이브리드 파싱 전략 구현.

pypdf(fitz)가 의미 있는 양의 텍스트를 돌려주면 그대로 사용하고,
부족하면 Vision LLM으로 전환한다.
"""

import base64
import io
import os
from pathlib import Path

import fitz  # PyMuPDF
import httpx
import numpy as np
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
VISION_MODEL = os.getenv("VISION_MODEL", "qwen2.5vl:7b")
VISION_PROVIDER = os.getenv("VISION_PROVIDER", "ollama")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
VISION_TIMEOUT = int(os.getenv("VISION_TIMEOUT", "600"))

# pypdf 텍스트 임계값.
# - 이 미만이면 스캔본이거나 축 레이블만 있는 차트 페이지로 간주하고 Vision으로 전환.
# - 일반 텍스트 페이지는 보통 수백~수천 자가 나오므로 50자 기준은 여유 있게 안전하다.
MIN_TEXT_LENGTH = 50


def process_page_hybrid(
    page: fitz.Page,
    dpi: int = 150,
    vision_model: str | None = None,
) -> dict:
    """pypdf 텍스트가 충분하면 text_layer, 부족하면 Vision LLM."""
    text = page.get_text().strip()
    if len(text) >= MIN_TEXT_LENGTH:
        return {"strategy": "text_layer", "text": text, "char_count": len(text)}

    vision_text = _vision_page(page, dpi=dpi, model=vision_model)
    return {
        "strategy": "vision",
        "text": vision_text,
        "char_count": len(vision_text) if vision_text else 0,
    }


# ---------------------------------------------------------------------------
# 내부 헬퍼
# ---------------------------------------------------------------------------

def _vision_page(
    page: fitz.Page,
    dpi: int = 150,
    model: str | None = None,
) -> str:
    """페이지를 이미지로 렌더링한 뒤 Vision LLM에 전달한다."""
    pix = page.get_pixmap(dpi=dpi)
    img_bytes = pix.tobytes("png")
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    if VISION_PROVIDER == "openai":
        return _call_openai_vision(img_b64)
    return _call_ollama_vision(img_b64, model=model)


def _call_ollama_vision(img_b64: str, model: str | None = None) -> str:
    """Ollama Vision API를 호출한다."""
    try:
        resp = httpx.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": model or VISION_MODEL,
                "prompt": (
                    "이 문서 이미지를 분석하세요. "
                    "모든 텍스트, 표, 차트를 추출하고 "
                    "구조화된 Markdown 형식으로 출력하세요."
                ),
                "images": [img_b64],
                "stream": False,
            },
            timeout=float(VISION_TIMEOUT),
        )
        resp.raise_for_status()
        return resp.json().get("response", "")
    except Exception as e:
        return f"[Ollama Vision 실패: {str(e)[:80]}]"


def _call_openai_vision(img_b64: str) -> str:
    """OpenAI Vision API를 fallback으로 호출한다."""
    try:
        resp = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": OPENAI_VISION_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "이 문서 이미지를 분석하세요. "
                                    "모든 텍스트, 표, 차트를 추출하고 "
                                    "구조화된 Markdown 형식으로 출력하세요."
                                ),
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_b64}",
                                },
                            },
                        ],
                    }
                ],
                "max_tokens": 2000,
            },
            timeout=float(VISION_TIMEOUT),
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[OpenAI Vision 실패: {str(e)[:80]}]"
