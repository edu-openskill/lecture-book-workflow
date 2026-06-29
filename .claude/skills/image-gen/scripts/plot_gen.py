#!/usr/bin/env python3
"""[PLOT SCRIPT] 플레이스홀더 스캔 → matplotlib 코드 실행(결정론적) → PNG 저장 → <img> 교체.

생성형(image_gen.py)과 달리, 수식·좌표가 '맞아야만 하는' 그래프(함수 곡선, 곡선 위의
점·화살표 주석, 등고선)를 코드로 계산해 그린다. 곡선 연속성·점 위치가 구조적으로 보장된다.

플레이스홀더 형식:
    <!-- [PLOT SCRIPT: 08_ex1-converge]
    path: assets/CH08/08_ex1-converge.png
    ```python
    import numpy as np, matplotlib.pyplot as plt
    f = lambda x: x**2 - 4*x + 7
    ...
    fig.savefig(OUT, dpi=150, bbox_inches='tight')   # OUT = 러너가 주입하는 절대경로
    ```
    -->
    ![캡션](../assets/CH08/08_ex1-converge.png)
    *그림 8-5: ...*

규칙:
- 코드 안에서 출력 파일은 변수 OUT(절대경로 str)으로 저장한다. 저장을 깜빡해도
  러너가 현재 figure를 OUT으로 자동 저장한다(폴백).
- 한글 폰트(Malgun Gothic 등)와 unicode_minus=False는 러너가 미리 설정한다.
"""
import re
import json
from dataclasses import dataclass
from pathlib import Path

@dataclass
class PlotPlaceholder:
    id: str
    path: str
    code: str
    raw_block: str       # 주석+이미지줄+캡션 전체(교체 대상)
    img_line: str
    caption: str | None

_BLOCK = re.compile(
    r'<!--\s*\[PLOT SCRIPT:\s*(?P<id>[^\]]+)\]\s*\n'
    r'(?P<body>.*?)\n-->\s*\n'
    r'(?P<img>!\[[^\]]*\]\([^)]+\))'
    r'(?:\s*\n(?P<caption>\*[^\n]+\*))?',
    re.S,
)
_PATH = re.compile(r'^\s*path:\s*(?P<path>\S+)\s*$', re.M)
_FENCE = re.compile(r'```(?:python|py)?\s*\n(?P<code>.*?)\n```', re.S)


def _extract_code(body: str) -> str:
    """body에서 path:줄을 제거하고, ```python 펜스가 있으면 그 안을, 없으면 나머지를 코드로."""
    no_path = _PATH.sub('', body)
    fm = _FENCE.search(no_path)
    if fm:
        return fm.group('code').strip('\n')
    return no_path.strip('\n')


def scan_placeholders(md_text: str) -> list[PlotPlaceholder]:
    out = []
    for m in _BLOCK.finditer(md_text):
        body = m.group('body')
        pm = _PATH.search(body)
        out.append(PlotPlaceholder(
            id=m.group('id').strip(),
            path=(pm.group('path') if pm else ''),
            code=_extract_code(body),
            raw_block=m.group(0),
            img_line=m.group('img'),
            caption=(m.group('caption') or None),
        ))
    return out


def _md_src_from_img_line(img_line: str) -> str:
    m = re.search(r'!\[[^\]]*\]\((?P<src>[^)]+)\)', img_line)
    return m.group('src') if m else ''


def _alt_from_img_line(img_line: str) -> str:
    m = re.search(r'!\[(?P<alt>[^\]]*)\]', img_line)
    return m.group('alt') if m else ''


def replace_placeholder(md_text: str, ph: PlotPlaceholder, width: int = 720) -> str:
    src = _md_src_from_img_line(ph.img_line)
    alt = _alt_from_img_line(ph.img_line)
    img_tag = f'<img src="{src}" width="{width}" alt="{alt}">'
    repl = img_tag + (('\n\n' + ph.caption) if ph.caption else '')
    return md_text.replace(ph.raw_block, repl)


_FONT_CANDIDATES = ('Malgun Gothic', 'AppleGothic', 'NanumGothic',
                    'Noto Sans CJK KR', 'Noto Sans KR')


def _configure_matplotlib():
    """Agg 백엔드 + 한글 폰트 + 마이너스 기호. 한 번만 설정."""
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import font_manager
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in _FONT_CANDIDATES:
        if name in available:
            matplotlib.rcParams['font.family'] = name
            break
    matplotlib.rcParams['axes.unicode_minus'] = False


def run_plot_script(code: str, out_path: str) -> bool:
    """matplotlib 코드를 실행해 out_path에 PNG를 만든다. 성공하면 True."""
    _configure_matplotlib()
    import matplotlib.pyplot as plt
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    ns = {'__name__': '__plot__', 'OUT': str(out_path)}
    try:
        exec(compile(code, '<plot-script>', 'exec'), ns)
        # 폴백: 코드가 저장을 안 했으면 현재 figure를 저장
        if not Path(out_path).exists() and plt.get_fignums():
            plt.gcf().savefig(out_path, dpi=150, bbox_inches='tight')
    except Exception as e:  # 코드 오류 시 메시지만 보고하고 플레이스홀더 보존
        print(f"    └ 실행 오류: {type(e).__name__}: {e}")
        return False
    finally:
        plt.close('all')
    return Path(out_path).exists()


def process_file(md_path, project_root, dry_run: bool = False) -> int:
    md_path = Path(md_path); project_root = Path(project_root)
    text = md_path.read_text(encoding='utf-8')
    phs = scan_placeholders(text)
    count = 0
    for ph in phs:
        if dry_run:
            print(f"[dry-run] {ph.id} → {ph.path} ({len(ph.code.splitlines())}줄 코드)")
            count += 1
            continue
        target = project_root / ph.path
        ok = run_plot_script(ph.code, str(target))
        if not ok:
            print(f"[skip] 플롯 실패: {ph.id} (플레이스홀더 보존)")
            continue
        text = replace_placeholder(text, ph)
        count += 1
        print(f"[ok] {ph.id} → {ph.path}")
    md_path.write_text(text, encoding='utf-8')
    return count


if __name__ == "__main__":
    import sys
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if len(args) < 2:
        print("usage: plot_gen.py <chapter.md> <project_root> [--dry-run]")
        sys.exit(1)
    n = process_file(args[0], args[1], dry_run=dry)
    print(f"처리: {n}장")
