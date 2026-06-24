#!/usr/bin/env python3
"""
유튜브 자동자막(.vtt) 다운로더 — lecture-caption 스킬의 Cap1.

사용:
    python3 fetch_captions.py <youtube_url> [출력디렉토리] [언어코드]

예:
    python3 fetch_captions.py "https://youtu.be/XXXX" sources/05강 ko

의존:
    pip install -U yt-dlp --break-system-packages

동작:
    - 수동 자막이 있으면 우선, 없으면 자동자막(--write-auto-subs) 사용
    - 영상 본체는 받지 않음(--skip-download)
    - 결과를 <출력디렉토리>/caption-raw.vtt 로 저장
"""
import subprocess
import sys
import shutil
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    url = sys.argv[1]
    out_dir = Path(sys.argv[2] if len(sys.argv) > 2 else ".")
    lang = sys.argv[3] if len(sys.argv) > 3 else "ko"
    out_dir.mkdir(parents=True, exist_ok=True)

    if shutil.which("yt-dlp") is None:
        sys.exit("yt-dlp 가 없습니다. 먼저: pip install -U yt-dlp --break-system-packages")

    tmpl = str(out_dir / "caption")
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-subs",          # 수동 자막 있으면 우선
        "--write-auto-subs",     # 없으면 자동자막
        "--sub-langs", lang,
        "--sub-format", "vtt",
        "--convert-subs", "vtt",
        "-o", tmpl,
        url,
    ]
    print("실행:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    # yt-dlp는 caption.<lang>.vtt 형태로 저장 -> caption-raw.vtt 로 정규화
    candidates = sorted(out_dir.glob("caption*.vtt"))
    if not candidates:
        sys.exit("자막 파일을 찾지 못했습니다. 자동자막이 아직 생성 중이거나 비공개일 수 있습니다.")
    target = out_dir / "caption-raw.vtt"
    candidates[0].replace(target)
    # 부수 자막 정리
    for c in out_dir.glob("caption*.vtt"):
        if c != target:
            c.unlink()
    print("저장 완료:", target)


if __name__ == "__main__":
    main()
