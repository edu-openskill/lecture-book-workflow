#!/usr/bin/env python3
"""
terminal_screenshot.py — 명령어 실행 결과를 터미널 스타일 PNG 스크린샷으로 저장

사용법:
    # HTML만 생성
    python terminal_screenshot.py "python src/main.py" --output screenshot.html

    # HTML + PNG 동시 생성 (Playwright로 .terminal 요소만 캡처)
    python terminal_screenshot.py "python src/main.py" --output screenshot.html --png result.png

    # PNG만 생성 (HTML은 임시 파일로 생성 후 삭제)
    python terminal_screenshot.py "python src/main.py" --png result.png

    # 작업 디렉토리 및 제목 지정
    python terminal_screenshot.py "ollama list" --png shot.png --cwd /path/to/project --title "Ollama 모델 목록"
"""

import argparse
import subprocess
import sys
import os
import tempfile
from pathlib import Path


HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500&display=swap');

  html, body {{
    margin: 0;
    padding: 0;
    background: transparent;
    height: auto;
  }}
  body {{
    padding: 20px;
    display: inline-block;
    width: 100%;
    box-sizing: border-box;
    font-family: 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic',
                 'Menlo', 'Monaco', 'Courier New', monospace;
  }}
  .terminal {{
    width: 860px;
    margin: 0 auto;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    border: 1px solid #d0d0d0;
    background: #ffffff;
  }}
  .titlebar {{
    background: #e0e0e0;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #c8c8c8;
  }}
  .dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }}
  .dot.red {{ background: #ff5f57; }}
  .dot.yellow {{ background: #ffbd2e; }}
  .dot.green {{ background: #28c940; }}
  .title {{
    color: #555;
    font-size: 12px;
    margin-left: 8px;
    flex: 1;
    text-align: center;
    font-weight: 500;
  }}
  .body {{
    padding: 20px 24px;
  }}
  .prompt {{
    color: #0066cc;
    font-size: 13px;
    margin-bottom: 10px;
    word-break: break-all;
    font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
  }}
  .prompt::before {{
    content: '$ ';
    color: #2a9d2a;
    font-weight: bold;
  }}
  .output {{
    color: #222222;
    font-size: 13px;
    line-height: 1.5;
    white-space: pre;
    word-break: normal;
    overflow-x: auto;
    font-family: Menlo, 'DejaVu Sans Mono', consolas, 'Courier New', monospace;
  }}
  .output pre {{
    margin: 0;
    font-family: inherit;
    font-size: inherit;
    line-height: inherit;
  }}
  .output code {{
    font-family: inherit;
  }}
  .output .err {{ color: #cc0000; font-weight: 500; }}
  .output .ok  {{ color: #2a9d2a; font-weight: 500; }}
</style>
</head>
<body>
<div class="terminal">
  <div class="titlebar">
    <div class="dot red"></div>
    <div class="dot yellow"></div>
    <div class="dot green"></div>
    <div class="title">{title}</div>
  </div>
  <div class="body">
    <div class="prompt">{command}</div>
    <div class="output">{output}</div>
  </div>
</div>
</body>
</html>
"""


def strip_ansi(text: str) -> str:
    """ANSI escape codes 제거"""
    import re
    return re.sub(r'\x1b\[[0-9;]*[mGKHJr]', '', text)


def escape_html(text: str) -> str:
    text = strip_ansi(text)
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


NOISE_KEYWORDS = [
    "deprecationwarning", "loading weights", "load report", "unexpected",
    "warning: you are", "position_ids", "huggingfacehub", "can be ignored",
    "langchaindeprecationwarning", "pip install", "import as",
    "notes:", "status", "it/s]", "it/s",
    "huggingfaceembeddings", "embeddings =", "model_kwargs",
]


def _filter_noise(text: str) -> str:
    """노이즈 라인을 제거한다."""
    lines = []
    for line in text.split("\n"):
        lower = line.lower().strip()
        if any(k in lower for k in NOISE_KEYWORDS):
            continue
        if lower.startswith("---") and "+" in lower:
            continue
        lines.append(line)
    return "\n".join(lines)


def _make_table_html(table_lines: list, title: str = "", compact: bool = False) -> str:
    """파싱된 테이블 행을 HTML <table>로 변환."""
    html = ""
    if title:
        html += f'<div style="text-align:center;font-size:12px;font-weight:bold;margin:6px 0 3px">{escape_html(title)}</div>'
    fs = "11px" if compact else "12px"
    pad = "4px 6px" if compact else "5px 10px"
    html += f'<table style="border-collapse:collapse;width:100%;font-size:{fs};margin:0 0 6px">'
    for tl in table_lines:
        cells = [c.strip() for c in tl.split("│")[1:-1]]
        if not cells:
            cells = [c.strip() for c in tl.split("┃")[1:-1]]
        if cells:
            # compact 모드: 긴 셀 30자 제한
            if compact:
                cells = [c[:30] + "…" if len(c) > 30 else c for c in cells]
            tag = "th" if "┃" in tl else "td"
            style = f'style="padding:{pad};border:1px solid #ddd;text-align:left;white-space:nowrap"'
            if tag == "th":
                style = f'style="padding:{pad};border:1px solid #ccc;background:#f5f5f5;font-weight:bold;text-align:left;white-space:nowrap"'
            html += "<tr>" + "".join(f"<{tag} {style}>{escape_html(c)}</{tag}>" for c in cells) + "</tr>"
    html += "</table>"
    return html


def _rich_table_to_html(text: str) -> str:
    """Rich 유니코드 테이블(┏━┳ 등)을 HTML <table>로 변환한다.
    테이블 2개 이상이면 2열(grid)로 배치."""
    cleaned = strip_ansi(text)
    lines = cleaned.split("\n")
    pre_lines = []      # 테이블 전 텍스트
    tables = []          # [(title, table_html), ...]
    post_lines = []      # 테이블 후 텍스트
    table_rows = []
    in_table = False
    title_candidate = ""
    tables_done = False

    for line in lines:
        stripped = line.strip()
        # 테이블 시작
        if stripped.startswith("┏") or stripped.startswith("╒"):
            in_table = True
            table_rows = []
            continue
        # 테이블 끝
        if in_table and (stripped.startswith("└") or stripped.startswith("╘")):
            in_table = False
            tables.append((title_candidate, table_rows[:]))  # (title, rows) 저장, 나중에 HTML 변환
            title_candidate = ""
            continue
        # 테이블 구분선
        if in_table and (stripped.startswith("┡") or stripped.startswith("├") or stripped.startswith("╞")):
            continue
        # 테이블 데이터 행
        if in_table and ("│" in stripped or "┃" in stripped):
            table_rows.append(stripped)
            continue
        # 테이블 밖
        if not in_table:
            # 제목 후보: 다음 줄이 ┏일 수 있음
            if stripped and not any(c in stripped for c in "┏┃│└┡━"):
                if title_candidate and not tables:
                    pre_lines.append(escape_html(title_candidate))
                title_candidate = stripped
            elif not stripped:
                if title_candidate and not tables:
                    pre_lines.append(escape_html(title_candidate))
                    title_candidate = ""
                if tables:
                    pass  # 테이블 사이 빈 줄 스킵
                else:
                    pre_lines.append("")
            else:
                if tables:
                    post_lines.append(escape_html(line))
                else:
                    pre_lines.append(escape_html(line))

    # 마지막 제목 후보 처리
    if title_candidate and not tables:
        pre_lines.append(escape_html(title_candidate))

    # 조립
    compact = len(tables) >= 2
    result = "\n".join(pre_lines)
    if tables:
        for title, rows in tables:
            result += "\n" + _make_table_html(rows, title, compact=compact)
    if post_lines:
        result += "\n" + "\n".join(post_lines)
    return result


def colorize_output(text: str) -> str:
    """Rich 출력을 HTML로 변환. 테이블은 <table>로, 나머지는 텍스트로."""
    text = _filter_noise(text)
    cleaned = strip_ansi(text)

    # 테이블이 있으면 변환
    if "┏" in cleaned or "╒" in cleaned:
        return _rich_table_to_html(text)

    # 테이블 없으면 기본 처리
    lines = []
    for line in cleaned.split("\n"):
        lower = line.lower()
        if any(k in lower for k in ["error", "traceback", "failed", "exception"]):
            lines.append(f'<span class="err">{escape_html(line)}</span>')
        elif any(k in lower for k in ["success", "done", "completed"]):
            lines.append(f'<span class="ok">{escape_html(line)}</span>')
        else:
            lines.append(escape_html(line))
    return "\n".join(lines)


def run_and_capture(command: str, cwd: str = None, timeout: int = 60) -> tuple[str, int]:
    """명령어를 PTY로 실행하여 Rich 유니코드 박스를 유지한다."""
    import select, pty, errno
    try:
        master_fd, slave_fd = pty.openpty()
        env = os.environ.copy()
        env["TERM"] = "xterm-256color"
        env["COLUMNS"] = "100"
        env["LINES"] = "50"
        proc = subprocess.Popen(
            command,
            shell=True,
            stdout=slave_fd,
            stderr=slave_fd,
            cwd=cwd,
            env=env,
            close_fds=True,
        )
        os.close(slave_fd)
        output_chunks = []
        while True:
            try:
                r, _, _ = select.select([master_fd], [], [], 1.0)
                if r:
                    data = os.read(master_fd, 4096)
                    if not data:
                        break
                    output_chunks.append(data.decode("utf-8", errors="replace"))
                elif proc.poll() is not None:
                    # 프로세스 종료 후 남은 데이터 읽기
                    try:
                        while True:
                            data = os.read(master_fd, 4096)
                            if not data:
                                break
                            output_chunks.append(data.decode("utf-8", errors="replace"))
                    except OSError:
                        pass
                    break
            except OSError as e:
                if e.errno == errno.EIO:
                    break
                raise
        os.close(master_fd)
        proc.wait(timeout=timeout)
        output = "".join(output_chunks)
        # \r\n → \n, carriage return 정리
        output = output.replace("\r\n", "\n").replace("\r", "")
        return output.strip(), proc.returncode
    except subprocess.TimeoutExpired:
        proc.kill()
        return f"[타임아웃: {timeout}초 초과]", 1
    except Exception as e:
        return f"[실행 오류: {e}]", 1


def capture_png(html_path: str, png_path: str) -> bool:
    """Playwright로 .terminal 요소만 캡처하여 PNG 저장"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[경고] playwright 미설치. pip install playwright && playwright install chromium")
        return False

    png_out = Path(png_path)
    png_out.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 920, "height": 800})
        page.goto(f"file://{os.path.abspath(html_path)}")
        page.wait_for_load_state("networkidle")
        # .terminal 요소만 캡처 → 여백 없이 딱 맞게
        terminal = page.locator(".terminal")
        terminal.screenshot(path=str(png_out))
        browser.close()

    print(f"PNG 저장: {png_out} ({png_out.stat().st_size // 1024}KB)")
    return True


def build_html(title: str, command: str, output: str) -> str:
    """터미널 스타일 HTML 생성"""
    # 출력이 너무 길면 마지막 100줄만
    lines = output.split("\n")
    if len(lines) > 100:
        output = f"[... 앞 {len(lines)-100}줄 생략 ...]\n" + "\n".join(lines[-100:])

    return HTML_TEMPLATE.format(
        title=title,
        command=escape_html(command),
        output=colorize_output(output),
    )


def main():
    parser = argparse.ArgumentParser(
        description="명령어 실행 결과를 터미널 스타일 스크린샷(PNG)으로 저장"
    )
    parser.add_argument("command", help="실행할 명령어")
    parser.add_argument("--output", default=None, help="출력 HTML 파일 경로")
    parser.add_argument("--png", default=None, help="출력 PNG 파일 경로")
    parser.add_argument("--cwd", default=None, help="작업 디렉토리")
    parser.add_argument("--title", default="Terminal", help="창 제목")
    parser.add_argument("--timeout", type=int, default=60, help="타임아웃(초)")
    parser.add_argument("--display", default=None, help="스크린샷에 표시할 명령어 (실제 실행과 다를 때)")
    parser.add_argument("--width", type=int, default=860, help="터미널 폭(px). 2열 테이블은 1200 권장")
    args = parser.parse_args()

    if not args.output and not args.png:
        parser.error("--output 또는 --png 중 하나는 지정해야 합니다.")

    cwd = args.cwd or os.getcwd()
    print(f"실행: {args.command}")
    print(f"경로: {cwd}")

    output, exit_code = run_and_capture(args.command, cwd=cwd, timeout=args.timeout)

    if not output:
        output = "(출력 없음)"

    display_cmd = args.display or args.command
    html = build_html(args.title, display_cmd, output)

    # HTML 저장
    html_path = args.output
    temp_html = False
    if not html_path:
        # PNG만 요청된 경우 임시 HTML 생성
        fd, html_path = tempfile.mkstemp(suffix=".html")
        os.close(fd)
        temp_html = True

    Path(html_path).parent.mkdir(parents=True, exist_ok=True)
    Path(html_path).write_text(html, encoding="utf-8")

    if not temp_html:
        print(f"HTML 저장: {html_path}")

    # PNG 캡처
    if args.png:
        capture_png(html_path, args.png)

    # 임시 HTML 정리
    if temp_html:
        os.unlink(html_path)

    print(f"종료 코드: {exit_code}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
