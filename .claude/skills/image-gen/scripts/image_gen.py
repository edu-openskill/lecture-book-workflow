#!/usr/bin/env python3
"""이미지 플레이스홀더 스캔 → Codex 생성 → 경로 이동 → <img> 교체."""
import re
from dataclasses import dataclass

@dataclass
class Placeholder:
    id: str
    path: str
    prompt: str
    raw_block: str   # 주석+이미지줄+캡션 전체(교체 대상)
    img_line: str
    caption: str | None

_BLOCK = re.compile(
    r'<!--\s*\[(?:GEMINI|IMAGE) PROMPT:\s*(?P<id>[^\]]+)\]\s*\n'
    r'(?P<body>.*?)\n-->\s*\n'
    r'(?P<img>!\[[^\]]*\]\([^)]+\))'
    r'(?:\s*\n(?P<caption>\*[^\n]+\*))?',
    re.S,
)
_PATH = re.compile(r'^\s*path:\s*(?P<path>\S+)\s*$', re.M)

def scan_placeholders(md_text: str) -> list[Placeholder]:
    out = []
    for m in _BLOCK.finditer(md_text):
        body = m.group('body')
        pm = _PATH.search(body)
        path = pm.group('path') if pm else ''
        # prompt = body에서 path:줄과 Style:줄 제외
        lines = [l for l in body.splitlines()
                 if not l.strip().startswith('path:')]
        prompt = '\n'.join(l for l in lines if l.strip()).strip()
        out.append(Placeholder(
            id=m.group('id').strip(),
            path=path,
            prompt=prompt,
            raw_block=m.group(0),
            img_line=m.group('img'),
            caption=(m.group('caption') or None),
        ))
    return out
