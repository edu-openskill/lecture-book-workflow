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

import json
from pathlib import Path

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

def parse_thread_id(stdout: str) -> str | None:
    """codex --json JSONL에서 thread.started의 thread_id 추출."""
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith('{'):
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        if obj.get('type') == 'thread.started' and obj.get('thread_id'):
            return obj['thread_id']
    return None

def find_generated_image(thread_id: str, codex_home=None) -> Path | None:
    """thread_id 폴더에서 생성된 ig_*.png를 찾는다."""
    home = Path(codex_home) if codex_home else (Path.home() / '.codex')
    hits = sorted((home / 'generated_images' / thread_id).glob('ig_*.png'))
    return hits[0] if hits else None

def _md_src_from_img_line(img_line: str) -> str:
    m = re.search(r'!\[[^\]]*\]\((?P<src>[^)]+)\)', img_line)
    return m.group('src') if m else ''

def _alt_from_img_line(img_line: str) -> str:
    m = re.search(r'!\[(?P<alt>[^\]]*)\]', img_line)
    return m.group('alt') if m else ''

def replace_placeholder(md_text: str, ph: Placeholder, width: int = 720) -> str:
    src = _md_src_from_img_line(ph.img_line)
    alt = _alt_from_img_line(ph.img_line)
    img_tag = f'<img src="{src}" width="{width}" alt="{alt}">'
    repl = img_tag + (('\n\n' + ph.caption) if ph.caption else '')
    return md_text.replace(ph.raw_block, repl)

import os
import shutil
import subprocess
from pathlib import Path

def _default_codex_js() -> str:
    base = os.environ.get('APPDATA') or str(Path.home())
    return str(Path(base) / 'npm' / 'node_modules' / '@openai' / 'codex' / 'bin' / 'codex.js')

def run_codex_image(prompt: str, codex_js=None, codex_home=None) -> str | None:
    """codex --json 헤드리스로 이미지 생성 → 생성 PNG 경로 반환. (S1 검증된 호출)
    프롬프트는 stdin으로 전달. 평문 `codex exec "..."`는 non-TTY에서 실패하므로
    `node codex.js exec --json --skip-git-repo-check -` 를 쓴다."""
    codex_js = str(codex_js or _default_codex_js())
    full = '다음 설명으로 이미지 한 장을 생성해서 PNG 파일로 저장해줘:\n' + prompt
    res = subprocess.run(
        ['node', codex_js, 'exec', '--json', '--skip-git-repo-check', '-'],
        input=full, capture_output=True, text=True, encoding='utf-8',
    )
    tid = parse_thread_id(res.stdout)
    if not tid:
        return None
    img = find_generated_image(tid, codex_home)
    return str(img) if img else None

def process_file(md_path, project_root, generate=run_codex_image,
                 dry_run: bool = False) -> int:
    md_path = Path(md_path); project_root = Path(project_root)
    text = md_path.read_text(encoding='utf-8')
    phs = scan_placeholders(text)
    count = 0
    for ph in phs:
        if dry_run:
            print(f"[dry-run] {ph.id} → {ph.path}")
            count += 1
            continue
        saved = generate(ph.prompt)
        if not saved:
            print(f"[skip] 생성 실패: {ph.id}")
            continue
        target = project_root / ph.path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(saved), str(target))
        text = replace_placeholder(text, ph)
        count += 1
        print(f"[ok] {ph.id} → {ph.path}")
    md_path.write_text(text, encoding='utf-8')
    return count
