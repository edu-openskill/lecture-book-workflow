# 이미지 생성 및 관리 규칙

## 0. 시각 자료 유형별 도구 선택

| 유형 | 도구 | 생성 시점 |
|------|------|----------|
| 흐름도, 아키텍처, 시퀀스 다이어그램 | **Mermaid** | 집필 중 즉시 |
| 개념 일러스트 / 비유 이미지 | **Codex(GPT) CLI 이미지** | 집필 완료 후 배치 생성 |
| 실습 결과 스크린샷 (터미널/UI) | **Direct Capture** | 예제 코드 실행 후 |

> 백엔드는 Codex(GPT) CLI([이미지 생성](image-gen 스킬))로 자동화된다(제미나이 아님). 표준 태그명은 `[IMAGE PROMPT]`이며, 레거시 `[GEMINI PROMPT]`도 하위호환으로 동일하게 인식된다.

집필 시점에는 생성 이미지와 실습 캡처를 만들 수 없으므로, 유형에 맞는 **플레이스홀더**를 삽입한다.
캡션은 집필 시점에 미리 작성한다.

---

## 0.5. 경로 규칙

모든 이미지(Codex 생성, 실습 캡처)는 **챕터별 단일 폴더**에 저장한다.

```
projects/{책이름}/
├── chapters/NN-제목.md        <- 챕터 원고
├── assets/
│   ├── CH01/                  <- CH01의 모든 이미지
│   ├── CH02/
│   └── ...
```

**두 가지 경로를 플레이스홀더에 모두 명시:**

| 용도 | 경로 기준 | 형식 | 예시 |
|------|----------|------|------|
| `path:` (스크립트용) | 프로젝트 루트 | `assets/CH{N}/{id}.png` | `assets/CH01/01_chapter-opening.png` |
| `![alt](src)` (마크다운) | 챕터 파일 위치 | `../assets/CH{N}/{id}.png` | `../assets/CH01/01_chapter-opening.png` |

> **주의**: 챕터 파일이 `chapters/` 안에 있으므로 `![alt](assets/...)` 는 오류. 반드시 `../assets/...` 를 사용한다.

---

## 1. 플레이스홀더 삽입 (2가지 방식)

### 방식 A — 개념 이미지: 이미지 프롬프트 플레이스홀더 (Codex/GPT)

개념 이미지를 삽입할 때 사용. 아이콘 사전(§2)을 참고하여 프롬프트까지 확정한다.

```markdown
<!-- [IMAGE PROMPT: {NN}_{identifier}]
path: assets/CH{N}/{NN}_{identifier}.png
{§3 베이스 스타일 + 프로젝트 아이콘 사전 조합 프롬프트}
Style: {style-tag}
-->
![{캡션}](../assets/CH{N}/{NN}_{identifier}.png)
*그림 {N}-{순번}: {캡션}*
```

**예시:**
```markdown
<!-- [IMAGE PROMPT: 03_rag-flow]
path: assets/CH03/03_rag-flow.png
Minimalist flat-design infographic illustrating RAG pipeline. Three stages:
Document → Embedding → Vector DB → Query → LLM Response.
White background, Korean labels, 16:9 aspect ratio.
Style: architecture-infographic
-->
![RAG 파이프라인](../assets/CH03/03_rag-flow.png)
*그림 3-2: RAG 파이프라인의 전체 흐름*
```

### 방식 B — 실습 결과: 캡처 필요 플레이스홀더

실습 섹션에서 실제 실행 결과 화면을 캡처해야 할 위치에 삽입한다.
생성 이미지가 아니므로 프롬프트 없이 **무엇을 캡처할지**만 명시한다.

```markdown
<!-- [CAPTURE NEEDED: {NN}_{identifier}
  path: assets/CH{N}/{NN}_{identifier}.png
  desc: {어떤 명령을 실행하고 어떤 상태를 보여주는지}
] -->
![{캡션}](../assets/CH{N}/{NN}_{identifier}.png)
*그림 {N}-{순번}: {캡션}*
```

**예시:**
```markdown
<!-- [CAPTURE NEEDED: 04_first-answer
  path: assets/CH04/04_first-answer.png
  desc: `python main.py` 실행 후 RAG 비서가 첫 번째 질문에 답변한 터미널 화면
] -->
![첫 번째 RAG 응답](../assets/CH04/04_first-answer.png)
*그림 4-3: 비서가 처음으로 올바른 답변을 돌려준 순간*
```

---

## 2. 캡처 가이드라인 (방식 B)

| 항목 | 기준 |
|------|------|
| 캡처 범위 | 전체 터미널 화면 (명령어 입력 줄 포함) |
| 해상도 | Retina/HiDPI 권장, 최소 1280px 너비 |
| 터미널 테마 | 라이트/다크 모두 허용; 인쇄 시 그레이스케일 고려 |
| 에러 화면 | 의도적 에러 예시는 빨간 텍스트 포함하여 그대로 캡처 |
| 민감 정보 | API 키, 비밀번호 등 실제 값은 블러 처리 후 캡처 |

### 스크린샷과 코드 블록 중복 금지

실행 결과를 보여줄 때 **스크린샷과 터미널 출력 코드 블록을 동시에 사용하지 않는다.**

| 상황 | 사용할 형식 |
|------|-----------|
| 스크린샷이 있는 경우 | 스크린샷만 사용. 코드 블록으로 같은 출력 반복 금지 |
| 스크린샷이 없는 경우 (플레이스홀더 단계) | 코드 블록으로 예상 출력 표시 |
| 소스 코드 (python, bash 등) | 실행 명령이므로 스크린샷과 무관하게 유지 |

> **핵심**: 스크린샷이 확보된 시점에서 동일 내용의 출력 코드 블록을 제거한다.

---

## 3. 이미지 베이스 스타일 (Codex/GPT)

모든 개념 이미지는 아래 베이스 프롬프트를 기반으로 생성한다.

**Base Prompt:**
```
A minimalist black and white technical diagram with a strict 16:9 aspect ratio
on a solid white background. No shading, no 3D effects, only clean thin line art.
The entire assembly of icons, lines, and text is perfectly centered globally
within the 16:9 frame, leaving generous and equal white space on all sides.
```

### 공통 심볼 패턴

| 대상 | 프롬프트 패턴 |
|------|-------------|
| 사람/사용자 | `minimalist line-art person icon labeled '{label}'` |
| 서버/컴퓨터 | `minimalist line-art server rack icon labeled '{label}'` |
| 데이터베이스 | `minimalist line-art cylinder database icon labeled '{label}'` |
| 문서/파일 | `minimalist line-art stack of papers icon labeled '{label}'` |
| AI/모델 | `minimalist line-art brain icon labeled '{label}'` |
| 클라우드 | `minimalist line-art cloud icon labeled '{label}'` |

---

## 4. 구도 및 여백 규칙

- **안전 여백**: 전체 다이어그램이 캔버스의 약 60~70% 차지
- **글로벌 센터링**: 전체 요소의 무게 중심을 16:9 프레임 정중앙에 배치

---

## 5. 이미지 삽입 및 캡션 규칙 (이미지 준비 후)

플레이스홀더를 실제 이미지로 교체할 때 `<img>` 태그 + `width` 속성을 사용한다.
HTML 주석 블록은 제거한다.

### 이미지 사이즈 규칙

모든 이미지는 `<img>` HTML 태그로 삽입하고, **`width="720"`** 을 기본값으로 사용한다.

| 유형 | width | 용도 |
|------|-------|------|
| 전체 화면 캡처 | `720` | 기본값 |
| 터미널 출력 | `720` | 기본값 |
| 다이어그램/개념도 | `720` | 기본값 |

> `![alt](src)` 대신 반드시 `<img src="..." width="720" alt="...">` 를 사용한다.
> 캡션은 `<img>` 태그 다음 빈 줄 뒤에 작성한다.

**Before (플레이스홀더):**
```markdown
<!-- [IMAGE PROMPT: 03_rag-flow]
path: assets/CH03/03_rag-flow.png
...prompt...
-->
![RAG 파이프라인](../assets/CH03/03_rag-flow.png)
*그림 3-2: RAG 파이프라인의 전체 흐름*
```

**After (이미지 준비 완료):**
```markdown
<img src="../assets/CH03/03_rag-flow.png" width="720" alt="RAG 파이프라인">

*그림 3-2: RAG 파이프라인의 전체 흐름*
```

- **파일명 형식**: 소문자 영문, 밑줄, 하이픈 (예: `03_rag-flow.png`)
- **캡션**: 플레이스홀더에서 작성한 것을 그대로 사용
