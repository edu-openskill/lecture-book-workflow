# 글로벌 구조 규칙

산출물 구조, 버전 관리, 워크플로우 진행 규칙.

---

## 버전 관리

- 파일명에 `-vN` 접미사. 절대 덮어쓰지 않음 (`seed-v1.md → seed-v2.md`)

## 질문/선택 규칙

- 선택형 UI. 일반 4~10개, 추천은 첫 번째 + (Recommended)
- **STEP 1(씨앗) 의도 파악 시에만**. 선택지 3개 + "다시 추천해줘" 1개 (총 4개)
- 답변 즉시 answers.md에 기록
- 상수는 질문하지 않음 (톤, 스타일, 코드 분류 등)
- **저자 경험 질문 금지**. "이 분야 경험이 어때?" 등 저자 경험을 묻지 않음. AI가 "처음 접하는 사람의 전형적 경험"으로 범용 작성

## 워크플로우 진행

1. **한 STEP씩 진행**: 각 STEP의 산출물이 완성된 후 다음 STEP으로 넘어간다.
2. **자연스러운 대화**: 질문을 딱딱하게 나열하지 않고, 대화하듯 자연스럽게 진행한다.
3. **답변 즉시 저장**: 모든 STEP의 질문 답변을 `answers.md`에 기록한다. 유저의 수정 요청은 `review/revision-log.md`에 기록한다.
4. **STEP 완료 안내**: 각 STEP이 끝나면 다음 STEP 명령어를 안내한다.
5. **되돌아가기 허용**: 이전 STEP 산출물을 수정하고 싶으면 새 버전으로 생성한다.
6. **기본값 제안**: 답변이 어려운 항목은 합리적인 기본값을 제안한다.
7. **인사이트 질문**: 단순히 "뭐야?"가 아니라 "이건 생각해봤어?" 형태로 묻는다.
8. **의도가 필터다**: seed.md의 의도가 이후 모든 결정의 기준이다.
9. **상수는 질문하지 않는다**: 톤, 스타일, 챕터 구조, 코드 분류 등은 자동 적용한다.

## progress.json 운영 규칙

세션이 끊기거나 다시 시작할 때 현재 상태를 복구하는 파일.
템플릿: `.claude/progress-template.json` / 예시: `.claude/progress-example.json`

1. **STEP 시작 시**: 해당 step의 status를 `in_progress`로, `current_step` 업데이트
2. **산출물 생성 시**: artifact 경로와 artifact_version 업데이트
3. **검토 완료 시**: review 결과(pass/conditional_pass/fail) 업데이트
4. **STEP 완료 시**: status를 `done`으로
5. **챕터 추가 시**: step_5_chapters.chapters 배열에 push
6. **세션 재개 시**: progress.json 읽고 `current_step` + 미완료 항목 확인 후 이어가기
7. **`현재 상태` 명령어**: progress.json 기반으로 요약 출력

## 산출물 형식

- Markdown 형식, 파일명은 번호 접두사 (예: `01-시작하기.md`)
- 이미지. `![](경로)` — alt 텍스트 비움. 캡션은 이미지 아래 이탤릭(`*설명*`)으로 별도 작성
- 이미지 플레이스홀더. `[GEMINI PROMPT]`(개념도) / `[CAPTURE NEEDED]`(실습 캡처). 상세 → `rules/writing-chapters.md`

## 스킬 호출

- 검토 시 → `review` 스킬 호출
- 기획/갭 분석/분량 관리 시 → `planning` 스킬 호출
- progress.json 업데이트 시 → STEP 시작/완료/산출물 생성 시점에 즉시 반영

## 챕터 작성 규칙

### 챕터 헤더 blockquote
- 챕터 제목 바로 아래에 `>` blockquote로 버전/요약/핵심개념 작성
- 각 항목은 별도 `>` 라인으로 작성
- 형식: `> 한 줄 요약: ...` / `> 핵심 개념: ...`

### 이야기 파트
- 비유는 일상적인 것만, 페이지당 3개 이하

### 파트 전환
- 이야기 → 기술 파트 전환 시 전환 문장만으로 자연스럽게 넘김. 예: "이제 직접 만들어 보겠습니다." (`---` 수평선 사용 금지)

### 레포 소개 (기술 파트 시작 직후)
- 레포 소개 블록 필수. URL 테이블만으로 끝내지 마라 → why-log.md#2026-03-15-3
- 형식: git clone → 파일 트리([실습]/[설명]/[참고]) → start/end 안내
- 파일 트리는 outline-vN.md 구조 그대로
- 닫기: "챕터를 따라 하며 코드를 작성하고, 막히면 완성 코드를 참고하세요"

### 챕터 공통
- 구조: 문제 → 기술소개 → 해결 → 결과
- 닫기: "이것만은 기억하자" + 다음 예고
- 이미지 플레이스홀더 필수. 실행 결과 → `[CAPTURE NEEDED]`, 흐름도 → `[GEMINI PROMPT]` → why-log.md#2026-03-15-1
- 이미지 캡션: 이미지 바로 아래에 `*설명*`만 작성. `그림 N-N:` 접두어 금지 (Typst가 자동 부여). `![](경로)`의 alt 텍스트는 비워둠
- `<img>` 경로 변경 시 실제 파일도 이동 필수 → why-log.md#2026-03-15-6

### 챕터 검토 (의도감시)
- 상세 체크리스트 → `review` 스킬 (skills/review/SKILL.md) 참조

## 에이전트 디스패치 규칙

1. 각 STEP의 workflow 파일 헤더에 명시된 에이전트를 순서대로 디스패치한다
2. STEP 완료 전 디스패치 체크리스트 대조 — 헤더에 명시된 에이전트 목록과 실제 호출된 에이전트 목록을 비교하여, 누락된 에이전트가 있으면 STEP을 완료하지 않고 누락분을 호출한다
3. illustrator는 유저 요청 시에만 디스패치한다. 챕터 글 작성(writer)과 검토(editor)는 자동, 이미지 생성은 유저가 코드 완성을 확인한 후 요청한다

## 세션 프롬프트 자동 생성

각 STEP/챕터 완료 시 `prompts/next-session-*.md`를 자동 생성한다.

| 완료 시점 | 생성 파일 |
|----------|----------|
| STEP 4 완료 | `next-session-CH01.md` |
| CH[N] 완료 | `next-session-CH[N+1].md` |
| 마지막 챕터 완료 | `next-session-마무리.md` |
| STEP 7 완료 | `next-session-인쇄소.md` |

### 챕터 프롬프트 템플릿

```markdown
# 다음 세션: CH[N+1] 집필

## 프로젝트
- 경로: projects/[책이름]/
- progress.json 확인 후 현재 상태 파악

## 워크플로우
- .claude/workflow/step5-챕터집필.md (실행 흐름)
- .claude/workflow/review-guide.md (검토 체크리스트)

## 컨텍스트 파일 (읽어야 할 것)
- planning/seed-v1.md (의도, 핵심 메시지, 의도 밖 범위)
- planning/outline-v1.md (CH[N+1] 섹션 — 코드 분류, 이미지 계획)
- planning/scenario-v1.md (해당 버전 시나리오)
- chapters/[이전 챕터].md (브릿지 문장 확인)
- answers.md (이전 STEP 답변 누적)
- review/feedback-log.md (이전 검토 피드백)
- review/revision-log.md (수정 이력)

## 이번 챕터 변수
- 핵심 개념: ...
- 버전: v0.[N+1]
- 코드 분류: [실습] N개, [설명] N개, [참고] N개
- 이전 챕터 브릿지: "..."
- 에셋 경로: assets/CH[N+1]/{diagram, terminal, gemini}/

## 에이전트 디스패치 순서
writer → editor (글 작성 → 검토)
이미지 생성(illustrator)은 코드 완성 확인 후 유저가 별도 요청

## 명령
`챕터 작성 [N+1]` 실행
```
