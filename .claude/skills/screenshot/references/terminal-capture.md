# 터미널 스크린샷 캡처 워크플로우

## 스크립트 위치

```
.claude/skills/screenshot/scripts/terminal_screenshot.py  ← 핵심 엔진
.claude/skills/screenshot/scripts/capture.py               ← 배치 래퍼
```

## One-Command PNG 생성

`--png` 옵션으로 HTML 생성 + Playwright 캡처를 한 번에 수행한다.

```bash
python3 {SCRIPT} "{ACTUAL_COMMAND}" \
  --png {OUTPUT_PNG} \
  --display "{DISPLAY_COMMAND}" \
  --cwd {WORKING_DIR} \
  --title "{TITLE}" \
  --timeout 120
```

### 파라미터

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| `command` | Y | 실제 실행할 명령어 (venv 경로 포함 가능) |
| `--png` | Y | 출력 PNG 파일 경로 |
| `--display` | Y | 스크린샷에 표시할 깨끗한 명령어 |
| `--cwd` | Y | 명령어 실행 디렉토리 |
| `--title` | Y | 터미널 창 타이틀바에 표시할 제목 |
| `--timeout` | - | 타임아웃 초 (기본 60, 임베딩 등은 120 권장) |
| `--output` | - | HTML도 보존하려면 경로 지정 |

## 예시

```bash
SCRIPT=".claude/skills/screenshot/scripts/terminal_screenshot.py"
CH04="projects/사내AI비서_v2/code/CH04_벡터DB_구축"

python3 "$SCRIPT" \
  "$CH04/.venv/bin/python src/main.py" \
  --png "projects/사내AI비서_v2/assets/CH04/04_main-pipeline.png" \
  --display "python src/main.py" \
  --cwd "$CH04" \
  --title "전체 파이프라인 실행" \
  --timeout 120
```

## Display Command 규칙

`--display`에는 독자가 따라할 수 있는 깨끗한 명령어를 지정한다:

| Bad (절대경로) | Good (--display) |
|---|---|
| `/Users/me/.venv/bin/python src/main.py` | `python src/main.py` |
| `/opt/homebrew/bin/python3 src/cli_search.py --query '연차'` | `python src/cli_search.py --query '연차'` |

## 배치 캡처 (capture.py)

여러 스크린샷을 한 번에 생성:

```bash
python3 .claude/skills/screenshot/scripts/capture.py batch --config screenshots.json
```

`screenshots.json` 예시:
```json
{
  "cwd": "projects/사내AI비서_v2/code/CH04_벡터DB_구축",
  "assets_dir": "projects/사내AI비서_v2/assets/CH04",
  "venv": ".venv",
  "timeout": 120,
  "screenshots": [
    {
      "cmd": "python src/main.py",
      "filename": "04_main-pipeline.png",
      "title": "전체 파이프라인 실행"
    }
  ]
}
```

## 검증 체크리스트

캡처 후 반드시 확인:

1. **파일 존재**: PNG 파일이 생성되었는가
2. **파일 크기**: 5KB 이상인가 (빈 이미지 방지)
3. **내용 확인**: Read 도구로 이미지를 열어 확인
   - 하단이 잘리지 않았는가
   - prompt에 절대경로가 노출되지 않았는가
   - 이모지/특수문자가 정상 렌더링되었는가

## Troubleshooting

### Playwright 미설치
```bash
pip install playwright && playwright install chromium
```

### 한글 깨짐
- 인터넷 연결 필요 (Google Fonts Noto Sans KR 로드)
- 오프라인: macOS `Apple SD Gothic Neo` 폴백

### 이미지 잘림
`--output`으로 HTML을 보존하고 브라우저에서 직접 확인한다.

### 타임아웃
임베딩 모델 로드가 포함된 명령어는 `--timeout 120` 이상을 사용한다.

## 서적용 캡처 규칙

- ANSI 색상 코드를 임의로 변환하거나 제거하지 않는다. 원본 출력 그대로 캡처
- 불필요한 공백 줄을 삽입하지 않는다. 스크립트 출력 그대로 캡처
- trailing 공백을 제거한다. 줄 끝 공백이 남으면 캡처 이미지에 여백이 생긴다
