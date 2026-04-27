#!/usr/bin/env python3
"""집필에이전트 v2 — PDF 디자인 프리뷰 서버

실행 (프로젝트 루트에서):
    python3 .claude/skills/pub-studio/references/preview.py                    # 프로젝트 자동 감지
    python3 .claude/skills/pub-studio/references/preview.py 사내AI비서_v2       # 프로젝트 지정
    python3 .claude/skills/pub-studio/references/preview.py --port 8080        # 포트 지정
    python3 .claude/skills/pub-studio/references/preview.py --file book/통합본.typ  # 파일 모드
"""

import argparse
import sys
from pathlib import Path

# pub-studio 스크립트 디렉토리를 path에 추가
_SCRIPTS_DIR = Path(__file__).parent / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from preview_server import PreviewServer, select_project, HTML_FILE, DEFAULT_PORT


def main():
    parser = argparse.ArgumentParser(description="PDF 디자인 프리뷰 서버")
    parser.add_argument("project", nargs="?", help="프로젝트 이름 (생략 시 선택)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"포트 (기본: {DEFAULT_PORT})")
    parser.add_argument("--file", type=str, default=None, help=".typ 파일 경로 (파일 모드)")
    args = parser.parse_args()

    if not HTML_FILE.exists():
        print(f"오류: {HTML_FILE} 파일이 없습니다.")
        sys.exit(1)

    project_path = select_project(args.project)
    server = PreviewServer(project_path, port=args.port, initial_file=args.file)
    server.start()


if __name__ == "__main__":
    main()
