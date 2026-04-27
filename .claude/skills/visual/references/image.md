# 이미지 생성 및 관리 규칙

## 0. 시각 자료 유형별 도구 선택

| 유형 | 도구 | 서브폴더 | 생성 시점 |
|------|------|---------|----------|
| 흐름도, 아키텍처 | **Mermaid / D2** | `diagram/` | 집필 중 즉시 |
| 시퀀스/단계 흐름 (ReAct, 파이프라인) | **플로우 카드** | `diagram/` | 유저 요청 시 (메인 세션) |
| 개념 인포그래픽 / 비유 이미지 | **Gemini Image** | `gemini/` | 집필 완료 후 배치 생성 |
| 실습 결과 스크린샷 (터미널/UI) | **Direct Capture** | `terminal/` | 예제 코드 실행 후 |

개념도는 **인포그래픽 스타일로 비유를 시각화**한다. 추상적 개념을 일상적 사물로 치환하여 한눈에 이해할 수 있도록 한다.

집필 시점에는 Gemini 이미지와 실습 캡처를 만들 수 없으므로, 유형에 맞는 **플레이스홀더**를 삽입한다.
캡션은 집필 시점에 미리 작성한다.

---

## 0.5. 경로 규칙

모든 이미지는 **챕터별 폴더 + 유형별 서브폴더**에 저장한다.

```
projects/{책이름}/
├── chapters/NN-제목.md        <- 챕터 원고
├── assets/
│   ├── CH01/
│   │   ├── diagram/           <- Mermaid/D2 렌더링
│   │   ├── terminal/          <- 터미널 캡처
│   │   └── gemini/            <- Gemini 개념도
│   ├── CH02/
│   │   ├── diagram/
│   │   ├── terminal/
│   │   └── gemini/
│   └── ...
```

**두 가지 경로를 플레이스홀더에 모두 명시:**

| 용도 | 경로 기준 | 형식 | 예시 |
|------|----------|------|------|
| `path:` (스크립트용) | 프로젝트 루트 | `assets/CH{N}/{subfolder}/{id}.png` | `assets/CH01/gemini/01_auth-flow.png` |
| `![alt](src)` (마크다운) | 챕터 파일 위치 | `../assets/CH{N}/{subfolder}/{id}.png` | `../assets/CH01/gemini/01_auth-flow.png` |

**서브폴더 매핑:**
| 플레이스홀더 | 서브폴더 |
|-------------|---------|
| `[GEMINI PROMPT]` | `gemini/` |
| `[CAPTURE NEEDED]` (터미널) | `terminal/` |
| Mermaid/D2 렌더링 | `diagram/` |

> **주의**: 챕터 파일이 `chapters/` 안에 있으므로 `![alt](assets/...)` 는 오류. 반드시 `../assets/...` 를 사용한다.

---

## 0.7. D2 다이어그램 빌드 규칙

D2 다이어그램을 PNG로 변환할 때 **반드시 `--layout elk`** 옵션을 사용한다. elk 레이아웃은 직각 꺾인선(orthogonal routing)을 자동 적용하여 깔끔한 다이어그램을 만든다. 기본 dagre 레이아웃은 곡선을 생성하므로 사용하지 않는다.

```bash
# SVG 생성 (elk 필수, 그룹 컨테이너 있으면 theme 0)
d2 --layout elk --theme 0 --pad 40 파일.d2 파일.svg

# PNG 변환 (폭 1600px)
rsvg-convert -o 파일.png -w 1600 파일.svg
```

- `--layout elk`: 직각 꺾인선(orthogonal routing) 자동 적용
- `--theme 0`: 테마 없음. 테마(300 등)를 쓰면 루트 컨테이너에 자동 경계선이 추가되어 그룹 점선과 이중으로 보임
- 스타일은 `.d2` 파일 내 classes로 직접 제어

---

## 1. 플레이스홀더 삽입 (2가지 방식)

### 방식 A — 개념 이미지: Gemini 프롬프트 플레이스홀더

개념 이미지를 삽입할 때 사용. 아이콘 사전(§2)을 참고하여 프롬프트까지 확정한다.

```markdown
<!-- [GEMINI PROMPT: {NN}_{identifier}]
path: assets/CH{N}/gemini/{NN}_{identifier}.png
{§3 베이스 스타일 + 프로젝트 아이콘 사전 조합 프롬프트}
Style: {style-tag}
-->
![{캡션}](../assets/CH{N}/gemini/{NN}_{identifier}.png)
*그림 {N}-{순번}: {캡션}*
```

**예시:**
```markdown
<!-- [GEMINI PROMPT: 03_rag-flow]
path: assets/CH03/gemini/03_rag-flow.png
Minimalist flat-design infographic illustrating RAG pipeline. Three stages:
Document → Embedding → Vector DB → Query → LLM Response.
White background, Korean labels, 16:9 aspect ratio.
Style: architecture-infographic
-->
![RAG 파이프라인](../assets/CH03/gemini/03_rag-flow.png)
*그림 3-2: RAG 파이프라인의 전체 흐름*
```

### 방식 B — 실습 결과: 캡처 필요 플레이스홀더

실습 섹션에서 실제 실행 결과 화면을 캡처해야 할 위치에 삽입한다.
Gemini 이미지가 아니므로 프롬프트 없이 **무엇을 캡처할지**만 명시한다.

```markdown
<!-- [CAPTURE NEEDED: {NN}_{identifier}
  path: assets/CH{N}/terminal/{NN}_{identifier}.png
  desc: {어떤 명령을 실행하고 어떤 상태를 보여주는지}
] -->
![{캡션}](../assets/CH{N}/terminal/{NN}_{identifier}.png)
*그림 {N}-{순번}: {캡션}*
```

**예시:**
```markdown
<!-- [CAPTURE NEEDED: 04_first-answer
  path: assets/CH04/terminal/04_first-answer.png
  desc: `python main.py` 실행 후 RAG 비서가 첫 번째 질문에 답변한 터미널 화면
] -->
![첫 번째 RAG 응답](../assets/CH04/terminal/04_first-answer.png)
*그림 4-3: 비서가 처음으로 올바른 답변을 돌려준 순간*
```

### 방식 D — 플로우 카드: HTML/CSS → Puppeteer PNG

시퀀스/단계 흐름 다이어그램에 사용. Writer는 **어떤 그림이 필요한지 자연어로 서술(desc)** 만 한다. JSON 구조나 화살표 흐름을 직접 기술하지 않는다. 유저 요청 시 visual 스킬이 desc와 챕터 맥락을 읽고 JSON을 설계하여 렌더링한다. 상세: `references/flow-card.md`

```markdown
<!-- [FLOW CARD: {NN}_{identifier}]
path: assets/CH{N}/diagram/{NN}_{identifier}.png
desc: {이 그림이 보여줘야 할 것을 자연어로 서술.
  어떤 흐름인지, 어디가 강조 포인트인지, 앞뒤 맥락.}
-->
![](../assets/CH{N}/diagram/{NN}_{identifier}.png)
*{캡션}*
```

**예시:**
```markdown
<!-- [FLOW CARD: 07_cache-highlight]
path: assets/CH07/diagram/07_cache-highlight.png
desc: 전체 에이전트 흐름 중 ResponseCache(메모장) 부분만 강조.
  질문이 들어오면 메모장을 먼저 확인하고, 없으면 LLM을 거쳐 답을 구한 뒤
  메모장에 저장하는 구조. 캐시 조회/저장 두 곳이 이번 실습 범위.
  나머지 단계는 흐리게 처리하여 실습 범위를 명확히 보여준다.
-->
![](../assets/CH07/diagram/07_cache-highlight.png)
*파란색이 실습 1에서 만드는 부분입니다*
```

**실행 흐름:**
1. 유저가 `/visual` 스킬 실행 요청
2. visual 스킬이 desc + 챕터 맥락 읽고 JSON 설계
3. 4가지 레이아웃 변형 HTML → 브라우저 표시
4. 유저 선택 → `render-flow.js`로 PNG 렌더링 → assets/ 저장

### 방식 C — 참고 이미지 기반: 이미지 분석 → Gemini 프롬프트 자동 생성

저자가 인터넷/외부 출처에서 가져온 참고 이미지를 챕터에 삽입해두면, `이미지 분석` 명령으로 해당 이미지를 분석하여 교육용 재생성 Gemini 프롬프트를 자동 생성한다. 상세: `skills/image-analyzer/SKILL.md`

```markdown
<!-- [GEMINI PROMPT: {NN}_{identifier}]
path: assets/CH{N}/gemini/{NN}_{identifier}.png
reference: assets/CH{N}/gemini/{원본파일명}
context: {챕터 내 삽입 위치의 문맥 요약 1줄}
{§3 베이스 스타일 + 참고 이미지 재해석 프롬프트}
Style: {style-tag}
-->
![{캡션}](../assets/CH{N}/gemini/{NN}_{identifier}.png)
*그림 {N}-{순번}: {캡션}*
```

**방식 A와의 차이점:**
- `reference:` 필드 추가 (원본 참고 이미지 경로 보존)
- `context:` 필드 추가 (삽입 위치 문맥 기록)
- 프롬프트가 원본 이미지를 재해석하여 생성 (저작권 회피)

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

## 3. Gemini 이미지 베이스 스타일

모든 개념 이미지는 아래 베이스 프롬프트를 기반으로 생성한다.

**Base Prompt:**
```
A minimalist black and white infographic-style technical diagram with a strict 16:9
aspect ratio on a solid white background. No shading, no 3D effects, only clean thin
line art. Use everyday metaphors to visualize abstract concepts.
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

## 4. 구도 및 여백 규칙 (Gemini)

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
<!-- [GEMINI PROMPT: 03_rag-flow]
path: assets/CH03/gemini/03_rag-flow.png
...prompt...
-->
![RAG 파이프라인](../assets/CH03/gemini/03_rag-flow.png)
*그림 3-2: RAG 파이프라인의 전체 흐름*
```

**After (이미지 준비 완료):**
```markdown
<img src="../assets/CH03/gemini/03_rag-flow.png" width="720" alt="RAG 파이프라인">

*그림 3-2: RAG 파이프라인의 전체 흐름*
```

- **파일명 형식**: 소문자 영문, 밑줄, 하이픈 (예: `03_rag-flow.png`)
- **캡션**: 플레이스홀더에서 작성한 것을 그대로 사용
