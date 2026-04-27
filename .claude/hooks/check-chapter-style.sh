#!/bin/bash
# chapters/*.md 또는 book/*.md 수정 시 금지 패턴을 강제 차단하는 PreToolUse 훅
# stdin: JSON { tool_name, tool_input: { file_path, old_string?, new_string?, content? } }

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# chapters/ 또는 book/ 경로가 아니면 즉시 통과
if [[ "$FILE_PATH" != *"/chapters/"* ]] && [[ "$FILE_PATH" != *"/book/"* ]]; then
    exit 0
fi

# 검사 대상 텍스트 추출 (Edit의 new_string 또는 Write의 content)
TEXT=$(echo "$INPUT" | jq -r '.tool_input.new_string // .tool_input.content // empty')

if [ -z "$TEXT" ]; then
    exit 0
fi

VIOLATIONS=""

# 금지 패턴 검사
if echo "$TEXT" | grep -q '이것이야말로'; then
    VIOLATIONS="${VIOLATIONS}설교 패턴: '이것이야말로' 사용 금지 (style.md). "
fi

if echo "$TEXT" | grep -q '이것이 바로'; then
    VIOLATIONS="${VIOLATIONS}반복 강조: '이것이 바로...이유' 패턴 금지 (style.md). "
fi

if echo "$TEXT" | grep -qP '[\x{1F600}-\x{1F64F}\x{1F300}-\x{1F5FF}\x{1F680}-\x{1F6FF}\x{1F1E0}-\x{1F1FF}\x{2600}-\x{26FF}\x{2700}-\x{27BF}]'; then
    VIOLATIONS="${VIOLATIONS}이모지 사용 금지 (style.md). "
fi

if echo "$TEXT" | grep -qP '^## (이야기 파트|기술 파트)'; then
    VIOLATIONS="${VIOLATIONS}라벨형 H2 금지: '## 이야기 파트/기술 파트' 대신 자연스러운 제목 사용 (style.md). "
fi

if echo "$TEXT" | grep -qP '^---$'; then
    VIOLATIONS="${VIOLATIONS}수평선(---) 사용 금지: 파트 전환은 문장으로 (style.md). "
fi

if echo "$TEXT" | grep -q '비로소\|드디어\|마침내\|진정한'; then
    VIOLATIONS="${VIOLATIONS}AI 선호어 감지: '비로소/드디어/마침내/진정한' 사용 지양 (writing-chapters.md). "
fi

# 위반 있으면 deny
if [ -n "$VIOLATIONS" ]; then
    echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"스타일 위반: ${VIOLATIONS}\"}}"
    exit 0
fi

exit 0
