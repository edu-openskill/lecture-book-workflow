---
name: image-gen
description: [IMAGE PROMPT] (레거시 [GEMINI PROMPT]도 인식) 플레이스홀더를 Codex(GPT) CLI 이미지로 자동 생성·교체. 코드·개념 트랙 공용. 챕터 완성 후 `이미지 생성` 시 로드.
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

## 두 갈래: 생성형(`[IMAGE PROMPT]`) vs 결정론(`[PLOT SCRIPT]`)

`image_gen.py`는 **생성형** 이미지(`[IMAGE PROMPT]`, 비유·정성 개념)만 처리한다.
**정확한 수식·좌표 그래프**(함수 곡선, 곡선 위의 점·화살표, 등고선)는 생성형이 곡선
연속성·점 위치를 보장 못 하므로(Ch.8 ex1이 깨진 이유), `[PLOT SCRIPT]` 플레이스홀더 +
**`plot_gen.py`**(matplotlib 결정론 실행)로 처리한다. 어느 갈래로 보낼지의 판정 기준은
`visual/references/image.md` §0(검산 기준).

```bash
# 정확한 그래프: [PLOT SCRIPT] 블록의 matplotlib 코드를 실행해 PNG 생성·교체
python .claude/skills/image-gen/scripts/plot_gen.py <chapter.md> <project_root>
python .claude/skills/image-gen/scripts/plot_gen.py <chapter.md> <project_root> --dry-run
```
- 코드 안에서 출력은 변수 `OUT`(절대경로)로 저장. 깜빡해도 러너가 현재 figure를 자동 저장.
- 한글 폰트(Malgun Gothic 등)·`unicode_minus=False`·`Agg` 백엔드는 러너가 미리 설정.
- 코드 오류 시 해당 플레이스홀더는 보존된다(다른 그림은 계속 처리).

> 한 챕터에 두 종류가 섞여 있으면 `image_gen.py`와 `plot_gen.py`를 **둘 다** 돌린다(서로 다른 태그만 건드리므로 순서 무관).

## 참조
- `scripts/image_gen.py` — `[IMAGE PROMPT]` 스캔/생성(Codex)/이동/교체
- `scripts/plot_gen.py` — `[PLOT SCRIPT]` 스캔/실행(matplotlib)/저장/교체
- `scripts/spike_codex.md` — S1 검증 결과(호출 방식)
