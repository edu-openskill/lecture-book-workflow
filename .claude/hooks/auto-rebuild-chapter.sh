#!/usr/bin/env bash
# auto-rebuild-chapter.sh
# PostToolUse 훅 — Edit/Write가 projects/*/chapters/NN-*.md를 건드리면
# 해당 챕터를 HTML로 자동 재빌드한다.
#
# Claude Code가 hook을 호출할 때 stdin으로 JSON을 보낸다. 우리는
# tool_input.file_path만 본다. 챕터 md가 아니면 조용히 종료.

set -euo pipefail

# stdin에서 JSON 읽고 file_path 추출 (jq 사용, 없으면 grep fallback)
input="$(cat)"
if command -v jq >/dev/null 2>&1; then
  file_path="$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty')"
else
  file_path="$(printf '%s' "$input" | grep -oE '"file_path"[[:space:]]*:[[:space:]]*"[^"]+"' | head -1 | sed 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')"
fi

# 챕터 md인지 확인
if [[ -z "$file_path" ]]; then
  exit 0
fi
if [[ "$file_path" != *"/chapters/"*.md ]]; then
  exit 0
fi
# legacy 폴더는 제외
if [[ "$file_path" == *"/chapters/legacy/"* ]]; then
  exit 0
fi

# 챕터 번호 추출 (파일명 앞 2자리)
basename="$(basename "$file_path")"
chapter_num="$(echo "$basename" | grep -oE '^[0-9]{2}' || true)"
if [[ -z "$chapter_num" ]]; then
  exit 0
fi

# 프로젝트 루트 찾기 — chapters/의 부모
project_root="$(dirname "$(dirname "$file_path")")"
project_name="$(basename "$project_root")"

# 스킬 빌드 스크립트 경로
repo_root="${CLAUDE_PROJECT_DIR:-$(pwd)}"
build_script="$repo_root/.claude/skills/pub-html-build/build_html.py"

if [[ ! -f "$build_script" ]]; then
  echo "⚠️  auto-rebuild: 빌드 스크립트를 찾지 못했습니다: $build_script" >&2
  exit 0
fi

# Python 실행기 선택 (프로젝트 venv 우선, 없으면 시스템)
if [[ -x "$project_root/.pdf_venv/bin/python3" ]]; then
  py="$project_root/.pdf_venv/bin/python3"
elif [[ -x "$project_root/.venv/bin/python3" ]]; then
  py="$project_root/.venv/bin/python3"
else
  py="python3"
fi

# 빌드 (백그라운드, HTML만). 실패해도 편집은 방해하지 않음
# 10자리 챕터 번호를 int로 주입
chapter_int="$((10#$chapter_num))"
(
  cd "$repo_root"
  "$py" "$build_script" \
    --project-root "$project_root" \
    --chapter "$chapter_int" 2>&1 | tail -1
) &

exit 0
