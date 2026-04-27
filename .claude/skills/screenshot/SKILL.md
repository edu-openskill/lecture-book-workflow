---
name: screenshot
description: 터미널 실행 결과와 브라우저 웹 UI를 PNG 스크린샷으로 생성하는 스킬. terminal_screenshot.py(터미널)와 Playwright MCP(브라우저)를 지원한다. 챕터 집필 완료 후 [CAPTURE NEEDED] 플레이스홀더를 실제 이미지로 교체할 때 사용.
---

# 스크린샷 스킬

## 로드 시점

| 상황 | 설명 |
|------|------|
| 챕터 집필 완료 후 | `[CAPTURE NEEDED]` 플레이스홀더를 실제 캡처로 교체 |
| 실습 결과 확인 시 | 예제 코드 실행 결과를 PNG로 저장 |

## 핵심 규칙

- 스크린샷 명령어에 절대경로/venv 경로를 노출하지 않는다 (`--display` 사용)
- 출력 PNG는 `{project}/assets/CH{N}/terminal/`에 저장한다 (브라우저 캡처는 별도 서브폴더)
- 파일명: `{NN}_{설명}.png` (예: `06_main-pipeline.png`)
- 캡처 후 반드시 PNG 파일 존재와 크기(>5KB)를 검증한다
- **터미널 출력** → `scripts/terminal_screenshot.py` 또는 `scripts/capture.py` 사용
- **브라우저 웹 UI** → Playwright MCP 도구 사용

## 참조 파일

| 파일 | 로드 시점 |
|------|---------|
| `references/terminal-capture.md` | 터미널 스크린샷 생성 시 |
| `references/browser-capture.md` | 브라우저 웹 UI 캡처 시 |
