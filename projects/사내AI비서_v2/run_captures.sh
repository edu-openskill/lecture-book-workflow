#!/bin/bash
set -e

BASE_DIR="/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2"
SCRIPT="$BASE_DIR/.claude/skills/screenshot/scripts/book_capture.py"

echo "=== CH08 Captures ==="
CWD="$BASE_DIR/projects/사내AI비서_v2/code/ex08"
ASSETS="$BASE_DIR/projects/사내AI비서_v2/assets/CH08"
mkdir -p "$ASSETS"

PYTHON="$CWD/.venv/bin/python"

"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step1_chunk_experiment --step 1-1" --cwd "$CWD" --output "$ASSETS/08_chunk-size.png" --title "step 1-1: 청크 크기 실험"
"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step1_chunk_experiment --step 1-2" --cwd "$CWD" --output "$ASSETS/08_overlap.png" --title "step 1-2: 오버랩 비율 실험"
"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step1_chunk_experiment --step 1-3" --cwd "$CWD" --output "$ASSETS/08_strategy-comparison.png" --title "step 1-3: 긴 문서 청킹 전략 비교"
"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step2_reranker" --cwd "$CWD" --output "$ASSETS/08_reranker.png" --title "Cross-Encoder 리랭킹 전/후 비교"
"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step3_hybrid_search" --cwd "$CWD" --output "$ASSETS/08_hybrid-search.png" --title "하이브리드 검색 (BM25 + Vector)"

echo "=== CH09 Captures ==="
CWD="$BASE_DIR/projects/사내AI비서_v2/code/ex09"
ASSETS="$BASE_DIR/projects/사내AI비서_v2/assets/CH09"
mkdir -p "$ASSETS"

PYTHON="$CWD/.venv/bin/python"

"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step1_advanced_retriever --step 1-1" --cwd "$CWD" --output "$ASSETS/09_parent-doc.png" --title "step 1-1: Parent Document Retriever"
"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step1_advanced_retriever --step 1-2" --cwd "$CWD" --output "$ASSETS/09_self-query.png" --title "step 1-2: Self-Query Retriever"
"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step1_advanced_retriever --step 1-3" --cwd "$CWD" --output "$ASSETS/09_compression.png" --title "step 1-3: Contextual Compression"

"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step2_query_rewrite --step 2-1" --cwd "$CWD" --output "$ASSETS/09_abbreviation.png" --title "step 2-1: 약어 / 동의어 확장"
"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step2_query_rewrite --step 2-2" --cwd "$CWD" --output "$ASSETS/09_hyde.png" --title "step 2-2: HyDE (가상 답변 검색)"
"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step2_query_rewrite --step 2-3" --cwd "$CWD" --output "$ASSETS/09_multi-query.png" --title "step 2-3: Multi-Query (다중 쿼리)"

echo "=== CH10 Captures ==="
CWD="$BASE_DIR/projects/사내AI비서_v2/code/ex10"
ASSETS="$BASE_DIR/projects/사내AI비서_v2/assets/CH10"
mkdir -p "$ASSETS"

PYTHON="$CWD/.venv/bin/python"

"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step1_document_parser --step 1-1" --cwd "$CWD" --output "$ASSETS/10_step1-1-ocr.png" --title "step 1-1: OCR 파싱 (EasyOCR)"
"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step1_document_parser --step 1-2" --cwd "$CWD" --output "$ASSETS/10_step1-2-vision.png" --title "step 1-2: Vision 파싱 (Qwen2.5-VL)"

"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step2_hybrid_parser --step 2-1" --cwd "$CWD" --output "$ASSETS/10_step2-1-hybrid.png" --title "step 2-1: 문자 수 기반 하이브리드 파싱"
"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step2_hybrid_parser --step 2-2" --cwd "$CWD" --output "$ASSETS/10_step2-2-textlayer.png" --title "step 2-2: 텍스트 레이어 기반 하이브리드 파싱"

# Note: CH10 parameters for step3 are likely --step 1~3, let's just use what was in the book (2-1 etc) or verify with --help
"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step3_eval_framework --step 2-1 --k 3" --cwd "$CWD" --output "$ASSETS/10_step3-1-questions.png" --title "step 3-1: 정확도 (Precision@k)"
"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step3_eval_framework --step 2-2 --k 3" --cwd "$CWD" --output "$ASSETS/10_step3-2-retrieval.png" --title "step 3-2: 재현율 (Recall@k)"
# Note: step 2-3 hallucination might take 1~3 mins, let's bump timeout if book_capture supports it? It doesn't seem to have timeout on the cmd directly. Wait, the command executes synchronously inside playbook. We will see.
"$PYTHON" "$SCRIPT" --cmd "'$PYTHON' -m tuning.step3_eval_framework --step 2-3" --cwd "$CWD" --output "$ASSETS/10_step3-3-hallucination.png" --title "step 3-3: 환각률 (Hallucination Rate)"

echo "Done"
