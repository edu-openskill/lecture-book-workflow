# 집필에이전트v3

기술 서적(100페이지 권장)을 이야기처럼 쓰는 워크플로우 시스템.
저자(도메인 전문가)와 하나의 AI(Claude)가 대화하며 책을 완성한다.

> **코드 워크플로우**는 완성 코드를 **만드는** 단계 (별도 설계).
> 이 워크플로우의 STEP 2에서 분석하는 완성 코드 = 코드 워크플로우의 산출물.

---

## 핵심 컨셉

이 시스템이 만드는 책은 **교과서가 아니라 이야기**다. 글쓰기 원칙은 `.claude/rules/style.md` 참조.

---

## 설계 철학

| 개념          | 정체       | 역할                                                                                        |
| ------------- | ---------- | ------------------------------------------------------------------------------------------- |
| **STEP**      | 흐름       | 1~7번까지 순서대로 진행하는 워크플로우 단계                                                 |
| **에이전트**  | 전문가     | 각 역할을 담당하는 서브에이전트 (writer, editor, illustrator, publisher, analyst-architect) |
| **스킬**      | 도구       | 하나의 작업만 수행하고 결과를 돌려주는 원자적 도구 (22개)                                   |
| **검토 모드** | 체크리스트 | 산출물 품질을 검증하는 관점과 질문 목록 (3개)                                               |

메인 세션이 workflow를 따라가며 전문 에이전트를 디스패치하고, 각 에이전트가 스킬을 써서 산출물을 만든다.

## 전체 워크플로우 (7 STEP)

```
Phase 1 ── 의도 확립
  STEP 1. 씨앗              "이 책은 뭐다"
Phase 2 ── 재료 파악
  STEP 2. 코드 해부          "재료가 뭐가 있지"
Phase 3 ── 이야기 설계
  STEP 3. 시나리오 + 버전     "어떤 순서로 이야기하지"
  STEP 4. 뼈대 세우기         "목차와 코드 실습 배치"
Phase 4 ── 집필
  STEP 5. 챕터 집필 (반복)    "쓴다"
Phase 5 ── 완성
  STEP 6. 프롤로그            "숲을 보여준다"
  STEP 7. 마무리              "머릿말, 맺음말"
Phase 6 ── 출판 (인쇄소)
  출판정보 생성               "서점 등록용 정보 생성"
  표지 디자인 위자드           "4단계 표지 제작"
  인쇄소                     "MD→PDF 조판 + 레이아웃 최적화"
```

---

## 명령어

| 명령어             | STEP | 산출물                               | 상세                                               |
| ------------------ | ---- | ------------------------------------ | -------------------------------------------------- |
| `새 책 만들기`     | —    | 프로젝트 디렉토리                    | 아래 참조                                          |
| `씨앗 심기`        | 1    | `planning/seed.md`                   | `.claude/workflow/step1-씨앗.md`                   |
| `코드 분석`        | 2    | `planning/code-analysis.md`          | `.claude/workflow/step2-코드해부.md`               |
| `시나리오 설계`    | 3    | `planning/scenario.md` + `versions/` | `.claude/workflow/step3-시나리오.md`               |
| `뼈대 세우기`      | 4    | `planning/outline.md`                | `.claude/workflow/step4-뼈대.md`                   |
| `챕터 작성 [N]`    | 5    | `chapters/NN-제목.md`                | `.claude/workflow/step5-챕터집필.md`               |
| `검토 [챕터]`      | —    | `review/feedback-log.md`             | `.claude/workflow/review-guide.md`                 |
| `프롤로그 생성`    | 6    | `book/프롤로그.md`                   | `.claude/workflow/step6-프롤로그.md`               |
| `마무리`           | 7    | `book/에필로그.md` 등                | `.claude/workflow/step7-마무리.md`                 |
| `이미지 분석`      | 5    | `[GEMINI PROMPT]` 플레이스홀더       | illustrator + image-analyzer 스킬                  |
| `출판정보 생성`    | 출판 | `book/publish-info-*.md`             | publisher + pub-info 스킬                          |
| `인쇄소`           | 출판 | `book/output/*.pdf`                  | Typst 파이프라인. 아래 "인쇄소 실행 흐름" 참조     |
| `HTML 빌드`        | 출판 | `book/output/*.pdf`                  | `pub-html-build` 스킬. 아래 "HTML 파이프라인" 참조 |
| `이어하기`         | —    | —                                    | `progress.json` + 최근 수정 파일로 상태 복구       |
| `현재 상태`        | —    | 터미널 출력                          | progress.json 기반                                 |
| `PM 전략 [서비스]` | —    | `docs/pm/[서비스]-전략.md`           | pm-strategist 에이전트                             |
| `퍼널 설계 [범위]` | —    | `docs/pm/[범위]-퍼널.md`             | pm-strategist 에이전트                             |
| `GTM [대상]`       | —    | `docs/pm/[대상]-GTM.md`              | pm-strategist 에이전트                             |

### `인쇄소` 실행 흐름

표지 위자드(메인 세션) → Publisher 서브에이전트(PDF 빌드) 순서로 실행.
- **Phase A**: 출판정보 확인 → 표지 디자인 위자드 (4단계) → 유저 선택. 상세: `.claude/agents/publisher/AGENT.md`
- **Phase B**: Publisher 디스패치 — 온보딩 → 디자인 → 다이어그램 → PDF → 검수. 상세: `.claude/agents/publisher/AGENT.md`

### HTML 파이프라인

마크다운 → HTML → PDF 빌드. 상세: `.claude/skills/pub-html-build/SKILL.md`

```bash
python .claude/skills/pub-html-build/build_pdf_html.py --project-root projects/<책이름> --chapter N
```

### `새 책 만들기`

```bash
bash .claude/skills/pub-html-build/scripts/init_book.sh projects/<새-책이름>
```

디렉토리 구조 자동 생성 + `progress.json` 복사 → STEP 1 시작.

---

## 프로젝트 폴더 구조

```
projects/[책이름]/
├── progress.json               ← 상태 관리 (세션 끊김 시 복구용)
├── answers.md                  ← 모든 STEP 질문 답변 누적
├── planning/                   ← STEP 1~4 산출물
├── chapters/                   ← STEP 5 산출물 (원본, 에셋 경로 유지)
├── book/                       ← 인쇄소 조립 폴더 (출판용 복사본)
│   └── output/book.pdf
├── code/                       ← 원천 소스코드 (수정하지 않음)
├── [완성본 레포]/                ← 완성 코드 (code/에서 챕터별 분해)
├── [예제 레포]/                  ← 예제 스켈레톤 (완성본을 복사 → TODO+pass)
├── versions/                   ← code/를 기반으로 만든 버전별 예제 코드
├── assets/                     ← 챕터별 이미지
├── questions/                  ← 인사이트 질문 장바구니
│   ├── pending/
│   └── done/
└── review/                     ← 검토 모드 피드백 + 수정 이력
```

---

## 상수 — 절대 질문하지 않는다

저자에게 묻지 않고 자동 적용. 문체/구조 상수는 `.claude/rules/style.md`, `.claude/rules/code.md` 참조.

### 독자 상수

| 상수      | 값                                              |
| --------- | ----------------------------------------------- |
| 독자 수준 | 배경지식 있음, 이 책의 주제만 모름              |
| 책 유형   | 개념서                                          |
| 코드 비중 | 낮음 (이야기 파트에 코드 없음, 기술 파트에서만) |

---

## 검토 모드 (3개)

산출물 완성 후 체크리스트를 돌리는 검증 단계. 상세: `.claude/workflow/review-guide.md`

| 검토 모드    | 발동 시점 | 핵심                                               |
| ------------ | --------- | -------------------------------------------------- |
| **인사이트** | STEP 1~5  | 저자가 놓친 부분을 짚어주는 추가 질문              |
| **의도감시** | STEP 5    | seed.md 의도에서 벗어나지 않았는지 검증            |
| **감수**     | 전 STEP   | 기술 감수자 + 독자 대변인 + 이야기 편집장 3인 관점 |

---

## 프로젝트 관리

- 현재 작업 중인 프로젝트는 `projects/` 아래에서 가장 최근 수정된 폴더로 자동 감지한다.
- 여러 프로젝트가 있을 경우 사용자에게 어떤 프로젝트인지 확인한다.
- 프로젝트 전환은 "프로젝트 전환 [이름]"으로 가능하다.

---

## 규칙 체계

규칙은 **한 곳에서만 정의**한다 (Single Source of Truth). 에이전트/스킬 파일은 규칙을 복제하지 않고 `rules/`를 참조한다.

| 규칙 파일                           | 적용 범위             | 내용                                                     |
| ----------------------------------- | --------------------- | -------------------------------------------------------- |
| `.claude/rules/style.md`            | 전역                  | 톤, 편집, 금지패턴, 글쓰기 원칙, 출력 형식               |
| `.claude/rules/code.md`             | 전역                  | 코드블록, 파일유형, Git레포, 스크립트 출력 규칙          |
| `.claude/rules/structure.md`        | 전역                  | 버전관리, 워크플로우 진행, progress.json, 질문/선택 규칙 |
| `.claude/rules/storytelling.md`     | 전역                  | 소설 작법, 캐릭터, 비유, 대화체, 챕터 패턴               |
| `.claude/rules/writing-chapters.md` | `chapters/**`         | 실습 규칙, 비유 전략, 플레이스홀더 (paths 스코핑)        |
| `.claude/rules/chapter-format.md`   | `chapters/**`         | 실습 챕터 12단계 포맷 템플릿 (paths 스코핑)              |
| `.claude/rules/writing-preface.md`  | `book/front/preface*` | 머릿말 패턴 (paths 스코핑)                               |
| `.claude/rules/writing-epilogue.md` | `book/back/epilogue*` | 맺음말 패턴 (paths 스코핑)                               |

### Hooks (강제 차단)

`chapters/` 또는 `book/` 파일 수정 시 `.claude/hooks/check-chapter-style.sh`가 PreToolUse 훅으로 실행된다. 금지 패턴(설교, 이모지, 라벨형 H2, 수평선, AI 선호어) 위반 시 Edit/Write를 차단한다.

## 참조

| 위치                               | 내용                                                                                    |
| ---------------------------------- | --------------------------------------------------------------------------------------- |
| `.claude/rules/`                   | 규칙 8개 (위 표 참조)                                                                   |
| `.claude/hooks/`                   | PreToolUse 훅 (챕터 스타일 강제)                                                        |
| `.claude/skills/CATALOG.md`        | 22개 스킬 카탈로그                                                                      |
| `.claude/agents/`                  | 에이전트 6개 (analyst-architect, writer, editor, illustrator, publisher, pm-strategist) |
| `.claude/workflow/step[N]-*.md`    | STEP별 실행 가이드                                                                      |
| `.claude/workflow/review-guide.md` | 검토 모드 체크리스트                                                                    |
