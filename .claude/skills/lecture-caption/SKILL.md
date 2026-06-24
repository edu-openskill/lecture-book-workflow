---
name: lecture-caption
model: claude-sonnet-4-6
description: 유튜브 자동자막(.vtt)을 받아 정제하고 판서 대본과 정렬한다. 영상 STT를 직접 돌리지 않고 유튜브가 만든 자막을 2차 원고 소스로 변환. "자막 추출" 명령에서 로드.
---

# 유튜브 자막 스킬

강의 영상을 유튜브에 올린 뒤, 유튜브 **자동자막(.vtt)** 을 내려받아 책의 2차 소스로 만든다.
영상 본체 다운로드·로컬 Whisper·ffmpeg 불필요.

## 로드 시점

| 명령 | 상황 |
|------|------|
| `자막 추출 [강번호 또는 URL]` | 업로드 끝난 강의 자막을 소스로 변환 |

## 입력 / 출력

| | |
|---|---|
| 입력 | 유튜브 영상 URL (+ 정렬용 `sources/NN강/판서대본.md`) |
| 출력 | `sources/NN강/caption-raw.vtt`, `caption-clean.md`, `정렬표.md` |

## 3단계 파이프라인

```
1. 다운로드   scripts/fetch_captions.py URL -> caption-raw.vtt
              (yt-dlp --write-auto-subs --sub-lang ko --skip-download)
2. 정제       VTT 태그·타임코드·중복행 제거 -> 문장 복원 -> 용어 교정 사전 적용
              -> caption-clean.md   (references/caption-cleanup.md 규칙)
3. 정렬       판서대본 슬라이드 제목(헤딩) 기준으로 자막 구간 매핑 -> 정렬표.md
```

## 도구 4종 (원자적)

| 스킬 | 입력 -> 출력 | 핵심 규칙 |
|------|------------|----------|
| Cap1. 자막-다운로더 | URL -> caption-raw.vtt | `fetch_captions.py`. 자동자막 우선, 수동자막 있으면 그것 우선 |
| Cap2. VTT-정제기 | caption-raw.vtt -> 평문 | 타임코드·`<c>` 태그·중복행 제거, 문장 단위 복원 |
| Cap3. 용어-교정기 | 평문 -> caption-clean.md | 도메인 용어 오타 교정(컨텍스트/어텐션/RAG/MCP/벡터/할루시네이션 …). 사전은 references |
| Cap4. 대본-정렬기 | caption-clean.md + 판서대본.md -> 정렬표.md | 슬라이드 제목 매칭으로 자막 구간을 슬라이드에 붙임 |

## 사용 메모

- yt-dlp는 사전 설치 필요: `pip install -U yt-dlp --break-system-packages`
- 비공개/일부공개라도 **본인 계정 영상**이면 자막 추출 가능(쿠키 필요 시 `--cookies-from-browser`).
- 한국어 자동자막이 아직 생성 중이면 업로드 후 잠시 기다렸다 재시도.
- **자막은 보강용.** 없거나 품질이 낮으면 판서대본 단독으로 진행한다(책은 그래도 나온다).

## 참조 파일

| 파일 | 용도 |
|------|------|
| `scripts/fetch_captions.py` | 자막 다운로드 (yt-dlp 래퍼) |
| `references/caption-cleanup.md` | 정제 규칙 + 용어 교정 사전 |
