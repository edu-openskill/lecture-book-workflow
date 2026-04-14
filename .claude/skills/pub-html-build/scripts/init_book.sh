#!/usr/bin/env bash
# .claude/skills/pub-html-build/scripts/init_book.sh
# 새 책 프로젝트 골격 생성 + 선택적 tokens.css 오버라이드 템플릿 심기.
#
# 사용:
#   bash init_book.sh <project-root>
# 예:
#   bash init_book.sh projects/new-book

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "사용법: $0 <project-root>"
  echo "예:    $0 projects/new-book"
  exit 1
fi

PROJECT_ROOT="$1"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [[ -d "$PROJECT_ROOT" ]]; then
  echo "⚠️  이미 존재하는 디렉토리입니다: $PROJECT_ROOT"
  echo "    기존 구조를 유지한 채 누락된 디렉토리만 추가합니다."
fi

# 디렉토리 구조 생성
mkdir -p "$PROJECT_ROOT/chapters"
mkdir -p "$PROJECT_ROOT/assets"
mkdir -p "$PROJECT_ROOT/book/build"
mkdir -p "$PROJECT_ROOT/book/output"
mkdir -p "$PROJECT_ROOT/book/front"
mkdir -p "$PROJECT_ROOT/book/back"

# tokens.css 오버라이드 템플릿 (이미 있으면 건드리지 않음)
TOKENS_OVERRIDE="$PROJECT_ROOT/book/tokens.css"
if [[ -f "$TOKENS_OVERRIDE" ]]; then
  echo "ℹ️  tokens.css 오버라이드 파일이 이미 존재합니다: $TOKENS_OVERRIDE"
else
  cat > "$TOKENS_OVERRIDE" <<'EOF'
/* 프로젝트별 디자인 토큰 오버라이드
 *
 * 스킬 기본 토큰(.claude/skills/pub-html-build/styles/tokens.css)을
 * 덮어쓸 변수만 여기에 선언합니다. 비워 두면 스킬 기본값을 그대로 사용합니다.
 *
 * 예: 브랜드 액센트를 블루 계열로 바꾸기
 *   :root {
 *     --color-accent: #2563eb;
 *     --color-accent-bg: #dbeafe;
 *     --color-accent-border: #93c5fd;
 *     --color-accent-text: #1e40af;
 *   }
 */
EOF
  echo "✅ tokens.css 오버라이드 템플릿 생성: $TOKENS_OVERRIDE"
fi

echo ""
echo "✅ 프로젝트 초기화 완료: $PROJECT_ROOT"
echo ""
echo "디렉토리 구조:"
echo "  $PROJECT_ROOT/"
echo "    chapters/          # 마크다운 챕터 (NN-제목.md)"
echo "    assets/            # 이미지·다이어그램"
echo "    book/"
echo "      tokens.css       # 브랜드 오버라이드 (선택)"
echo "      front/ back/     # 프롤로그·에필로그"
echo "      build/ output/   # 빌드 산출물"
echo ""
echo "다음 단계:"
echo "  1. chapters/01-*.md 작성"
echo "  2. 필요 시 book/tokens.css에서 브랜드 색상 오버라이드"
echo "  3. 빌드:"
echo "     python $SKILL_DIR/build_pdf_html.py \\"
echo "       --project-root $PROJECT_ROOT --chapter 1 --html-only"
