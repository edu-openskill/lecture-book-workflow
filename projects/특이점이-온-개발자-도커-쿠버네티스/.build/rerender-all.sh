#!/bin/bash
# 전체 HTML → PNG 일괄 재렌더 (trim 자동 적용)
# 윈도우 사이즈는 넉넉히 주고 trim이 알아서 잘라줌
set -e

cd "$(dirname "$0")/.."

# 특수 매핑: HTML 이름과 PNG 이름이 다른 경우
declare -A SPECIAL_MAP=(
  ["network-isolation"]="ch2-step1-namespace1"
  ["port-forwarding"]="ch2-step2-dnat1"
  ["dns-resolution"]="ch2-step3-dns1"
  ["container-virtualization"]="chap02-container"
)

WIDTH=1200
HEIGHT=1400
COUNT=0
SKIPPED=0

for HTML in \
  assets/CH02/*.html \
  assets/CH02/diagram/*.html \
  assets/CH03/*.html \
  assets/CH04/*.html \
  assets/CH05/*.html; do

  [ -f "$HTML" ] || continue

  NAME=$(basename "$HTML" .html)
  DIR=$(dirname "$HTML")

  # 특수 매핑 적용
  PNG_NAME="${SPECIAL_MAP[$NAME]:-$NAME}"
  PNG="$DIR/$PNG_NAME.png"

  bash .build/render-png.sh "$HTML" "$PNG" "$WIDTH" "$HEIGHT" > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    COUNT=$((COUNT + 1))
    echo "[$COUNT] $HTML → $PNG"
  else
    SKIPPED=$((SKIPPED + 1))
    echo "SKIP: $HTML"
  fi
done

echo "---"
echo "완료: $COUNT 장 / 스킵: $SKIPPED 장"
