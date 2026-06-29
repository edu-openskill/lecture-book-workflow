# S1 결과 (2026-06-24)

## 검증 환경
- OS: Windows 11 Pro 10.0.26200
- codex: `C:\Users\ssarm\AppData\Roaming\npm\codex.ps1` (node wrapper → `@openai/codex` 0.140)
- 모델: gpt-5.5 (Codex CLI 기본값)

## Step 1: codex PATH 확인

```powershell
Get-Command codex | Select-Object Source
# Source: C:\Users\ssarm\AppData\Roaming\npm\codex.ps1
```

결과: PATH에서 `codex` 직접 호출 가능. `codex` = npm 전역 설치된 PowerShell 래퍼.

## Step 2: 헤드리스 exec 이미지 생성

### 최초 시도 (실패) — 출력 비캡처

```powershell
$codex = (Get-Command codex).Source
& $codex exec "<prompt>"
```

결과: exit 255. PowerShell `& operator`로 실행 시 codex가 TTY 기반 TUI를 열려고 시도 →
비대화형 환경에서 실패. 출력 캡처 불가.

### 작동하는 헤드리스 호출 (성공)

```powershell
$prompt = "다음 설명으로 이미지 한 장을 생성해서 PNG 파일로 저장해줘: <설명>"
$lastMsgFile = "output_last_msg.txt"
$prompt | node "C:\Users\ssarm\AppData\Roaming\npm\node_modules\@openai\codex\bin\codex.js" `
    exec --json --skip-git-repo-check -o $lastMsgFile "-"
```

핵심 플래그:
- `--json` : 이벤트를 stdout에 JSONL로 출력 (TUI 없이)
- `-o <FILE>` : 에이전트 마지막 메시지를 파일로 저장
- `-` : 프롬프트를 stdin에서 읽음 (piping 필요)
- `--skip-git-repo-check` : git repo 외부에서도 실행 가능

실행 결과:
- 소요 시간: ~56초 (09:10:59 → 09:11:55)
- exit 0
- 이미지 생성 확인: `C:\Users\ssarm\.codex\generated_images\019ef6f7-3ff9-7a41-97cf-c80126da856d\ig_0212c671404f1b5d016a3b20a75fc0819184057471b487b3a0.png` (671,963 bytes)

## JSONL 출력 패턴 (--json 모드)

```jsonl
{"type":"thread.started","thread_id":"019ef6f7-3ff9-7a41-97cf-c80126da856d"}
{"type":"turn.started"}
{"type":"item.completed","item":{"id":"item_0","type":"agent_message","text":"..."}}
{"type":"item.started","item":{"id":"item_1","type":"command_execution","command":"...","exit_code":null,"status":"in_progress"}}
{"type":"item.completed","item":{"id":"item_1","type":"command_execution","command":"...","exit_code":0,"status":"completed"}}
{"type":"item.completed","item":{"id":"item_2","type":"agent_message","text":"생성했습니다. ..."}}
{"type":"turn.completed","usage":{"input_tokens":53349,"cached_input_tokens":4864,"output_tokens":407,"reasoning_output_tokens":71}}
```

## 저장 경로 추출 방법

### 방법 1: thread_id → 폴더 매핑 (권장)

`thread.started` 이벤트에서 `thread_id`를 파싱 → 이미지 경로 조합:

```
$CODEX_HOME/generated_images/{thread_id}/ig_*.png
```

PowerShell 추출:
```powershell
$jsonOutput = $prompt | node <codex.js> exec --json ... "-" 2>&1
$threadId = ($jsonOutput | Where-Object { $_ -match '"thread.started"' } |
    ConvertFrom-Json).thread_id
$imgPath = "$env:USERPROFILE\.codex\generated_images\$threadId\ig_*.png"
$img = Get-ChildItem $imgPath | Select-Object -First 1
Write-Host "file:///$($img.FullName.Replace('\', '/'))"
```

### 방법 2: -o 플래그 (마지막 메시지)

`-o <FILE>` 로 에이전트 마지막 텍스트 메시지를 캡처. 생성 성공 시 내용:

```
생성했습니다. 요청하신 16:9 흰 배경 PNG 스타일의 흑백 선화 포물선 다이어그램입니다.
```

성공/실패 판별로 사용 가능. 경로 자체는 포함되지 않음.

### 저장 경로 출력 패턴

인터랙티브 모드의 `Saved to file:///...` 패턴은 `--json` 헤드리스 stdout에는 **나타나지 않음**.
대신 thread_id 기반 경로 조합이 신뢰할 수 있는 방법.

파일명 패턴: `ig_{sha1_or_hash}.png`

정규식 (파일시스템 glob 후 경로 조합):
```
C:\Users\<user>\.codex\generated_images\{thread_id}\ig_[0-9a-f]+\.png
```

또는 URI 형태:
```
file:///C:/Users/<user>/.codex/generated_images/{thread_id}/ig_[0-9a-f]+\.png
```

## 실제 실행 예시

검증된 완전한 invocation (PowerShell):

```powershell
$codexJs = "C:\Users\ssarm\AppData\Roaming\npm\node_modules\@openai\codex\bin\codex.js"
$lastMsgFile = "C:\path\to\last_msg.txt"
$prompt = "이미지를 생성해줘: <설명>"

# 실행 및 JSONL 캡처
$jsonLines = $prompt | node $codexJs exec --json --skip-git-repo-check -o $lastMsgFile "-"

# thread_id 추출
$threadEvent = $jsonLines | Where-Object { $_ -match '"type":"thread.started"' } | Select-Object -First 1
$threadId = ($threadEvent | ConvertFrom-Json).thread_id

# 이미지 경로 조합
$imgDir = "$env:USERPROFILE\.codex\generated_images\$threadId"
$img = Get-ChildItem "$imgDir\ig_*.png" | Select-Object -First 1
Write-Host "Generated: $($img.FullName)"
```

## 결론

- **codex 호출**: `<prompt> | node <codex.js> exec --json --skip-git-repo-check -o <last_msg_file> "-"`
- **헤드리스 이미지 생성**: **가능** (exit 0, 671KB PNG 확인, ~56초)
- **exec 명령**: `codex exec --json --skip-git-repo-check -o <file> "-"` (프롬프트는 stdin으로)
- **저장 경로 출력 패턴**: JSONL `thread.started.thread_id` → `$CODEX_HOME/generated_images/{thread_id}/ig_*.png`
- **결론**: **codex 어댑터 사용 가능** (manual 폴백 불필요)

### Task 11을 위한 인터페이스 값

| 변수 | 값 |
|------|-----|
| `CODEX_CMD` | `node C:\Users\ssarm\AppData\Roaming\npm\node_modules\@openai\codex\bin\codex.js` |
| `CODEX_EXEC_INVOCATION` | `echo "<prompt>" \| node <codex.js> exec --json --skip-git-repo-check -o <last_msg_file> "-"` |
| `CODEX_OUTPUT_PATTERN` | `thread_id` from JSONL `{"type":"thread.started","thread_id":"<uuid>"}` → `$CODEX_HOME/generated_images/<uuid>/ig_*.png` |
