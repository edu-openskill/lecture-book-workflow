---
name: image-gen
description: [GEMINI/IMAGE PROMPT] 플레이스홀더를 Codex CLI 이미지로 자동 생성·교체. 코드·개념 트랙 공용. 챕터 완성 후 `이미지 생성` 시 로드.
---

# 이미지 자동화 스킬

## 로드 시점
- 챕터 집필 완료 후, `이미지 생성` 명령.

## 백엔드
- **Codex CLI**(구독 로그인, API 키 불필요). 헤드리스 호출: `node <npm-global>/@openai/codex/bin/codex.js exec --json --skip-git-repo-check -` (프롬프트 stdin). 평문 `codex exec "..."`는 non-TTY에서 실패.
- 생성 PNG는 `~/.codex/generated_images/{thread_id}/ig_*.png`에 저장됨(thread_id는 JSONL `thread.started`에서 파싱) → 스크립트가 `assets/CH{N}/`로 이동.

## 사용
```bash
# 한 챕터 처리
python .claude/skills/image-gen/scripts/image_gen.py <chapter.md> <project_root>
# 미리보기(생성 안 함)
python .claude/skills/image-gen/scripts/image_gen.py <chapter.md> <project_root> --dry-run
```
실패(헤드리스 불가) 시 플레이스홀더는 보존된다(manual 폴백).

## 참조
- `scripts/image_gen.py` — 스캔/생성/이동/교체
- `scripts/spike_codex.md` — S1 검증 결과(호출 방식)
