#!/bin/bash
# HTML → PNG 렌더 헬퍼 (Chrome headless)
# 사용: render-png.sh <html_path> <png_path> [width] [height]
set -e

CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
HTML_PATH="$1"
PNG_PATH="$2"
WIDTH="${3:-1120}"
HEIGHT="${4:-800}"

if [ ! -f "$HTML_PATH" ]; then
  echo "ERROR: HTML not found: $HTML_PATH" >&2
  exit 1
fi

# Chrome은 절대 Windows 경로 필요
ABS_HTML=$(cd "$(dirname "$HTML_PATH")" && pwd -W)/$(basename "$HTML_PATH")
ABS_PNG=$(cd "$(dirname "$PNG_PATH")" 2>/dev/null && pwd -W)/$(basename "$PNG_PATH") || ABS_PNG="$PNG_PATH"

"$CHROME" --headless --disable-gpu \
  --screenshot="$ABS_PNG" \
  --window-size="${WIDTH},${HEIGHT}" \
  --hide-scrollbars \
  --default-background-color=ffffffff \
  "file:///$ABS_HTML" 2>&1 | grep -v "DevTools\|Created TensorFlow\|Old Headless" | head -3

if [ ! -f "$PNG_PATH" ]; then
  echo "FAIL: $PNG_PATH not created" >&2
  exit 1
fi

# 흰 여백 자동 트림 (Pillow)
PYTHON="python"
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
"$PYTHON" "$SCRIPT_DIR/trim-png.py" "$PNG_PATH" 12 2>&1 | head -3

echo "OK: $PNG_PATH"
