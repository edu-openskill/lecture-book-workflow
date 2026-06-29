# 이미지 생성 및 관리 규칙

## 0. 시각 자료 유형별 도구 선택

| 유형 | 도구 | 플레이스홀더 | 생성 시점 |
|------|------|------------|----------|
| 흐름도, 아키텍처, 시퀀스 다이어그램 | **Mermaid** | (코드블록 직접) | 집필 중 즉시 |
| 개념 일러스트 / 비유 이미지 | **Codex(GPT) CLI 이미지** | `[IMAGE PROMPT]` | 집필 완료 후 배치 생성 |
| **정확한 수식·좌표 그래프** (함수 곡선, 곡선 위의 점·화살표, 등고선) | **matplotlib (코드 실행)** | `[PLOT SCRIPT]` | 집필 완료 후 배치 실행 |
| 실습 결과 스크린샷 (터미널/UI) | **Direct Capture** | `[CAPTURE NEEDED]` | 예제 코드 실행 후 |

> 생성형 백엔드는 Codex(GPT) CLI([이미지 생성](image-gen 스킬))로 자동화된다(제미나이 아님). 표준 태그명은 `[IMAGE PROMPT]`이며, 레거시 `[GEMINI PROMPT]`도 하위호환으로 동일하게 인식된다.

### ⚖️ 생성형(`[IMAGE PROMPT]`) vs 결정론(`[PLOT SCRIPT]`) — 검산 기준

> **이 그림이 "독자가 숫자·좌표·수식으로 맞는지 검산할 수 있는 주장"을 하는가?**

생성형 이미지 모델은 수식을 **계산**하지 않고 "그럴듯한 픽셀"을 **합성**한다. 그래서 곡선 연속성·점이 곡선 위에 정확히 있는지·좌표 정확성을 **원리적으로 보장하지 못한다**(프롬프트에 "no gaps, exactly on curve"를 아무리 강하게 써도 안 됨 — Ch.8 ex1이 그 증거: 포물선이 조각조각 끊김). 따라서 **검산 대상 그림은 반드시 matplotlib로 계산해 그린다.**

| 있으면 → **`[PLOT SCRIPT]` (matplotlib 必)** | 없으면 → **`[IMAGE PROMPT]` (생성형 OK)** |
|---|---|
| 좌표축·눈금 | 축 없음 |
| 구체 좌표·명명된 점 `(0.4, 5.24)` | 라벨 없는 점 |
| 수식 `f(x)=x²−4x+7` 표기 | 수식 없음 |
| "최솟값 (2,3)", `x=2` 점선 안내선 | "too small / just right" 같은 **정성** 라벨만 |
| 등고선·벡터장처럼 형상이 수식에서 나옴 | 안개 산 사람·그릇 같은 **순수 비유 삽화** |

- **화살표·주황 점·라벨도 matplotlib가 더 잘한다.** `annotate(arrowprops=...)`·`scatter(color=...)`·`text()`로 곡선 위에 정확히 얹힌다. "설명 표시가 필요해서 생성형을 썼다"는 정당화는 성립하지 않는다.
- **손으로 적은 좌표는 틀린다, 코드는 안 틀린다.** 점의 y값을 `f(x)`로 계산하면 곡선 위·정확성이 구조적으로 보장된다(Ch.8 ex1의 라벨 `(0.4,5.24)`는 실제 5.56과 불일치였음).
- **경계(등고선 등)**: 형상·경로가 수식에서 나오면 `[PLOT SCRIPT]`, 순전히 정성 스케치면 `[IMAGE PROMPT]`.
- **순수 비유 삽화**(곡선 자체가 없는 그림)는 항상 `[IMAGE PROMPT]`가 정답이다.

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

### 방식 C — 정확한 수식·좌표 그래프: 플롯 스크립트 플레이스홀더 (matplotlib)

§0 검산 기준에서 **검산 대상**으로 판정된 그림(함수 곡선, 곡선 위의 점·화살표 주석, 등고선)에 사용. 생성형 대신 **matplotlib 코드를 직접 작성**한다. 점의 y값은 반드시 `f(x)`로 **계산**한다(손으로 좌표를 적지 않는다).

```markdown
<!-- [PLOT SCRIPT: {NN}_{identifier}]
path: assets/CH{N}/{NN}_{identifier}.png
```python
import numpy as np, matplotlib.pyplot as plt
# OUT = 러너가 주입하는 절대 저장경로. 한글 폰트·unicode_minus는 러너가 미리 설정.
f = lambda x: x**2 - 4*x + 7
xs = np.linspace(-1.2, 5.2, 400)
fig, ax = plt.subplots(figsize=(10, 5.6))
ax.plot(xs, f(xs), color='#2E7DD6', lw=2.5)                 # 연속 곡선(끊김 불가)
pts = [0.0, 0.4, 0.72]
ax.scatter(pts, [f(x) for x in pts], color='#F59E0B', s=70, zorder=5)  # 점은 곡선 위 보장
for x in pts:
    ax.annotate(f"({x}, {f(x):.2f})", (x, f(x)), textcoords="offset points", xytext=(-8,-16))
for a, b in [(0.0,0.4),(0.4,0.72)]:                          # 하강 화살표(주황)
    ax.annotate("", xy=(b,f(b)), xytext=(a,f(a)), arrowprops=dict(arrowstyle="->", color='#F59E0B', lw=2))
ax.scatter([2],[f(2)], color='#2E7DD6', s=90, zorder=5)
ax.annotate("최솟값 (2, 3)", (2,3), textcoords="offset points", xytext=(8,8), color='#2E7DD6')
ax.plot([2,2],[0,3],'--', color='grey', lw=1)
ax.text(4.6, 9, r"$f(x)=x^2-4x+7$", color='#2E7DD6', fontsize=13)
ax.spines[['top','right']].set_visible(False); ax.set_ylim(bottom=0)
fig.savefig(OUT, dpi=150, bbox_inches='tight')
```
-->
![{캡션}](../assets/CH{N}/{NN}_{identifier}.png)
*그림 {N}-{순번}: {캡션}*
```

규칙:
- 코드 안에서 출력은 변수 **`OUT`**(절대경로)으로 저장한다. 저장을 깜빡해도 러너가 현재 figure를 `OUT`으로 자동 저장한다(폴백).
- 한글 폰트(Malgun Gothic 등)·`unicode_minus=False`·`Agg` 백엔드는 러너가 미리 설정하므로 코드에서 다시 설정할 필요 없다.
- 멀티패널(§6)이 필요하면 한 `[PLOT SCRIPT]` 안에서 `subplots(1, 3)`으로 그려도 되고, 패널별 파일로 쪼개도 된다.

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

---

## 6. 멀티패널 — 한 장으로 안 되면 2~3장으로 쪼갠다

**원칙**: 한 장의 그림에 여러 단계·비교·과정을 다 욱여넣지 않는다. 한 장 강박이 "그래프가 중간에 끊기거나", "라벨이 곡선에서 떨어지거나", "설명을 잘못 그린" 이미지를 만든다(예: Ch.8 보폭 비교, 경사하강 수렴 과정).

### 언제 쪼개나
| 상황 | 처방 |
|------|------|
| **단계/과정** (1걸음→2걸음→수렴) | 단계마다 1장씩 → 가로로 나란히 또는 세로로 위→아래 |
| **비교** (작은 보폭 vs 큰 보폭, before/after) | 경우마다 1장씩 → 가로 나란히 |
| **누적 빌드업** (빈 축 → 곡선 → 점 → 경로) | 겹겹이 쌓이는 2~3장 |
| 한 장에 요소가 7개 넘어 빽빽 | 의미 단위로 분할 |

### 배치 방법 (마크다운)
각 패널은 **독립된 이미지 파일**(`_a`, `_b`, `_c` 접미사)로 만들고, 캡션 하나로 묶는다.

**가로 배치** (나란히 비교) — `<img>`를 연달아, width는 패널 수로 나눠 축소:
```markdown
<img src="../assets/CH08/08_step-small.png" width="350" alt="작은 보폭: 느리게 수렴">
<img src="../assets/CH08/08_step-big.png" width="350" alt="큰 보폭: 건너뛰어 발산">

*그림 8-3: 보폭 비교 — (왼쪽) 너무 작으면 느리고, (오른쪽) 너무 크면 발산한다.*
```

**세로 배치** (단계 진행) — 한 줄에 하나씩, 위에서 아래로:
```markdown
<img src="../assets/CH08/08_gd-step1.png" width="520" alt="1걸음">

<img src="../assets/CH08/08_gd-step2.png" width="520" alt="2걸음">

<img src="../assets/CH08/08_gd-step3.png" width="520" alt="수렴">

*그림 8-4: 경사하강 진행 — 위에서 아래로 한 걸음씩 바닥에 가까워진다.*
```

플레이스홀더 단계에서도 패널마다 `[IMAGE PROMPT]` 블록을 따로 쓴다(파일이 분리되어야 `image_gen.py`가 각각 생성).

### 그래프 무결성 — 검산 대상이면 프롬프트로 때우지 말고 `[PLOT SCRIPT]`로

> ⚠️ **표면 처방 금지.** 곡선이 끊기는 건 프롬프트를 강하게 써서 고칠 문제가 아니다. 생성형 모델은 곡선 연속성·점 위치를 **원리적으로 보장하지 못한다**. §0 검산 기준에서 축·좌표·수식·명명된 점이 있는 그림(= 검산 대상)은 **무조건 방식 C `[PLOT SCRIPT]`(matplotlib)** 로 그린다. 곡선은 `f(x)`로 계산하므로 끊김·이탈이 구조적으로 불가능하다.

순전히 정성 스케치(축·좌표 없음)를 `[IMAGE PROMPT]`로 그릴 때만, 보조적으로 아래 문구를 덧붙여 "끊긴 그림"을 줄인다(보장이 아닌 완화):
```
The curve must be a single continuous unbroken line from end to end (no gaps, no breaks).
Every plotted point sits exactly ON the curve. Keep the whole curve inside the frame with margin.
```
- 정성 스케치라도 수치 라벨이 끼면(예: (0,7),(0.4,5.24)) 그건 이미 검산 대상이다 → `[PLOT SCRIPT]`로 옮긴다.
