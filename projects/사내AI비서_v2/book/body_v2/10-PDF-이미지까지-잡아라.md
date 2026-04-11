# Ch.10: "PDF 이미지까지 잡아라" — 고급 문서 처리와 평가 (ex10)

> 이번 버전: ex09 → ex10
> 한 줄 요약: 측정해야 개선할 수 있다. 느낌이 아니라 숫자로 품질을 측정해야 진짜 개선할 수 있다.
> 핵심 개념: 비전 LLM(Vision LLM), 광학 문자 인식(OCR), 정확도(Precision@k)

---

## 이야기 파트

<!-- [GEMINI PROMPT: 10_chapter-opening]
path: assets/CH10/10_chapter-opening.png
Black and white minimalist infographic. White background, black/dark gray elements only.
Clean geometric shapes, thin lines, rounded corners on boxes. Modern sans-serif font. 16:9.

Title (top center, bold): "사서의 눈 + 성적표"
Thin horizontal rule below title.

[Left box — rounded rectangle, thin black border, light gray fill]
  Header bar (dark gray background, white text): "사서의 눈"
  [Inner box 1 — dashed border] line-art person icon with glasses (사서)
  [Inner box 2 — solid border, side by side]
    Left: document icon with text lines, label "텍스트 문서"
    Right: document icon with image/chart inside, label "이미지 문서"
  Footer label: "글 + 그림 모두 읽는다"

[Center — thin arrow →, label above: "이해 + 측정"]

[Right box — rounded rectangle, thin black border, light gray fill]
  Header bar (dark gray background, white text): "성적표"
  [Inner box — solid border, clipboard icon]
    ✓ 정확도: 85%
    ✓ 재현율: 75%
    ✓ 환각률: 10%
  Footer label: "느낌이 아니라 숫자로"

[Bottom — timeline bar, full width, hairline border]
  가로 타임라인: ex01 → ex02 → ... → ex09 → ex10
  ex10에 깃발 아이콘, bold. 위에 라벨 "마지막 예제" -->
![사서의 눈 + 성적표](../assets/CH10/10_chapter-opening-3.png)

### 표가 깨졌다

사서를 뽑고, 훈련시키고, 전문 기술까지 가르쳤습니다. 이제 남은 건 하나 — 사서가 정말 일을 잘하는지 시험을 보는 것입니다.

CH04에서 PDF를 파싱했습니다. pypdf로 텍스트를 추출하고, 청킹하고, 벡터DB에 넣었습니다. 텍스트가 주된 문서에서는 잘 동작했습니다.

어느 날 팀장이 PDF 파일 하나를 던져줍니다.

**팀장**: "이 정보보안서약서도 검색되게 해줘."

별생각 없이 기존 파이프라인에 넣습니다. pypdf로 텍스트 추출하고, 청킹하고, 벡터DB에 넣는 그 흐름.

```
(빈 문자열)
```

*...아무것도 안 나온다?*

PDF를 직접 열어봅니다.

![정보보안서약서 원본](../assets/CH10/10_broken-pdf-original.png)
*그림 10-0: 팀장이 건넨 정보보안서약서. 결재란, 도장, 하이라이트가 있는 전형적인 사내 문서.*

스캔본이었습니다. 종이 문서를 스캐너로 찍어서 PDF로 만든 것입니다. 전체가 하나의 커다란 이미지입니다. 결재란에 서명이 있고, 빨간 도장도 찍혀 있고, 금지 사항에 하이라이트까지 되어 있습니다.

pypdf는 PDF 안의 텍스트 레이어를 읽는 도구입니다. CH04에서 언급했던 pdfplumber(표 추출 전용 라이브러리)도 마찬가지입니다. 둘 다 PDF 파일 구조에서 텍스트를 꺼내는 라이브러리입니다. 그런데 스캔본에는 텍스트 레이어가 없습니다. 사진을 아무리 뒤져봐야 글자 데이터는 없습니다.

*결재란에 누가 서명했는지, 금지 사항이 뭔지, 공개등급이 뭔지 — 사람은 한눈에 다 보이는데.*

사람이 PDF를 열면 "이건 대외비 문서고, AI 도구 사용에 제한이 있구나"를 바로 파악합니다. 지금까지 우리 사서가 문서를 읽는 방법은 pypdf뿐이었습니다. 글자 데이터가 있는 문서는 잘 읽었지만, 사진 앞에서는 속수무책입니다.

---

### 사서에게 눈을 달아주자

지금까지 우리 사서는 글만 읽었습니다. 텍스트를 추출하고, 벡터로 바꾸고, 검색해서 답했습니다.

하지만 사내 문서에는 글이 아닌 정보가 많습니다.

- 조직도 (박스와 화살표)
- 매출 추이 차트 (막대그래프, 선그래프)
- 복잡한 표 (셀 병합, 다단 구조)
- 스캔한 종이 문서 (아예 이미지만 있는 PDF)

이런 문서에서 텍스트만 뽑으면 정보의 절반을 잃습니다.

해결 방법은 두 가지입니다.

**방법 1: 광학 문자 인식(OCR) — 이미지 속 글자를 읽는다**

광학 문자 인식(OCR, Optical Character Recognition)은 이미지에서 글자를 인식하는 기술입니다. 스캔한 종이 문서처럼 텍스트가 이미지 형태로 박혀 있을 때 씁니다. 사서에게 **확대경**을 준 것과 같습니다. 작은 글씨를 읽게 해주지만, 조직도의 "박스 안에 있다"거나 표의 "이 셀과 저 셀의 관계"까지는 이해하지 못합니다.

**방법 2: 비전 LLM(Vision LLM) — 이미지를 이해한다**

그래서 등장하는 것이 비전 LLM(Vision LLM)입니다. 텍스트만 이해하던 LLM에 이미지를 볼 수 있는 능력을 추가한 모델입니다. 이미지를 보고 "이건 조직도이고, 인사팀은 경영지원본부 산하입니다"라고 설명할 수 있습니다. 글자를 읽는 것이 아니라 **그림을 이해**하는 것입니다. 사서에게 **눈**을 달아준 셈입니다. 확대경은 글씨를 읽게 해주지만, 눈은 그림 전체를 이해하게 해줍니다.

*그럼 처음부터 비전 LLM한테 다 맡기면 안 되나?*

솔직한 의문입니다. 확대경이 읽다가 놓치는 것을 눈이 다 잡아주는데, 그냥 눈만 쓰면 되지 않을까. 실제로 요즘 추세가 그렇습니다. OCR을 아예 건너뛰고 처음부터 비전 LLM에게 문서를 통째로 보여주는 방식이 늘고 있습니다. 확대경 없이 눈만 쓰는 사서입니다.

문제는 시간입니다. 눈으로 한 페이지를 읽는 데 10초씩 걸립니다. 사내 문서가 수백 페이지면 한참 기다려야 합니다. 확대경은 같은 페이지를 1~2초면 읽습니다. 문서의 구조에 맞춰 전략적으로 선택할 수 있어야 합니다.

*그런데 확대경이 글자를 읽긴 읽었는데...*

```
원본: 기안 검토 승인 정보보안 서약서 (스캔본) 문서번호: 2026
OCR: 가인 승인 정보보안 서사서 (스스년) 단서면요 2026
```

*"서약서"가 "서사서"로, "스캔본"이 "스스년"으로 읽혔습니다. 처음부터 눈으로 봤으면 그런 일은 없었을 겁니다.*

이것이 하이브리드의 어려운 점입니다. 확대경이 뭔가를 읽어왔다고 해서 그게 정확한 글자인지는 또 다른 문제입니다. 글자 수만 세서는 품질까지 판단할 수 없습니다. 기술 파트에서 이 문제를 어떻게 풀어가는지 직접 실험해봅니다.

<!-- [GEMINI PROMPT: 10_ocr-vs-vision]
path: assets/CH10/10_ocr-vs-vision.png
모던하고 전문적인 비교 인포그래픽. 화이트/라이트 그레이 배경, 산세리프 서체. 16:9 비율.

주요 제목: "글자 인식(OCR) vs 이미지 이해(비전 LLM) — 확대경 vs 눈"

[왼쪽 — 글자 인식 (확대경)]
주황색 배경 박스.
제목: "글자 인식 — OCR (확대경)"
① 조직도 PDF 아이콘 (박스+화살표가 그려진 문서)
→ 확대경 아이콘 (돋보기)
→ 흩어진 텍스트 조각들: "대표이사", "인사팀", "재무팀", "개발팀"
  각 텍스트가 떨어져 있고 구조 정보 없음.
하단 라벨: "글자만 읽음 — 구조는 모름"
결과 예시 박스 (빨간 테두리):
  "대표이사경영지원본부기술개발본부영업본부인사팀재무팀..."

[오른쪽 — 이미지 이해 (눈)]
파란색 배경 박스.
제목: "이미지 이해 — 비전 LLM (눈)"
① 같은 조직도 PDF 아이콘
→ 눈 아이콘 (사람 눈)
→ 구조화된 출력:
  "## 조직도"
  "대표이사"
  "  ├── 경영지원본부 (인사팀, 재무팀)"
  "  ├── 기술개발본부 (개발1팀, 개발2팀)"
  "  └── 영업본부 (국내, 해외)"
하단 라벨: "그림을 이해함 — 구조까지 파악"
결과 예시 박스 (초록 테두리):
  깔끔한 트리 구조

[가운데 — 비교 화살표]
양방향 화살표, 라벨: "글자 vs 의미"

[하단 비교 바]
| 항목 | 글자 인식(OCR) | 이미지 이해(비전 LLM) |
| 속도 | ⚡ 빠름 | 🐢 느림 |
| 표/차트 | ✗ 추출 불가 | ✓ 내용 설명 |
| 스캔 PDF | ✓ (글자만) | ✓ (구조까지) | -->
![OCR vs Vision LLM](../assets/CH10/10_ocr-vs-vision-3.png)
*그림 10-1: 광학 문자 인식(OCR)은 이미지 속 글자를 읽고, 비전 LLM은 이미지의 의미를 이해한다.*

---

### 매번 골라야 해?

OCR은 빠르지만 표나 도장은 못 읽습니다. 비전 LLM은 다 이해하지만 느립니다. 문서가 10개면 하나하나 "이건 OCR, 이건 비전 LLM"이라고 골라줘야 할까요?

*...귀찮은데.*

사서가 문서를 펼쳤을 때 스스로 판단하게 하면 됩니다. "이 페이지는 글자가 잘 뽑히니까 OCR로 충분하고, 이 페이지는 이미지뿐이니까 눈으로 봐야겠다." 사서에게 **판단력**까지 주는 것입니다.

---

### 그런데, 진짜 좋아진 건 맞아?

CH08에서 청킹을 바꿔보고, 리랭킹을 적용하고, 하이브리드 검색을 도입했습니다. CH09에서 질의 재작성(Query Rewrite)과 근거 시스템까지 추가했습니다.

그때마다 "오, 좋아졌다"고 느꼈습니다. 그런데 **느낌**입니다.

"좋아진 것 같다"와 "85점에서 92점으로 올랐다"는 완전히 다른 이야기입니다.

팀장이 묻습니다.

**팀장**: "AI 비서 검색 정확도가 몇 퍼센트야?"

**나**: "음... 꽤 좋아졌는데요..."

**팀장**: "숫자로."

느낌이 아니라 측정이 필요합니다. 학교에서 시험을 보면 성적표가 나오듯이, AI 비서에게도 성적표가 필요합니다.

이것이 **평가 프레임워크(Evaluation Framework)** 입니다. 질문을 던지고, 나온 답을 정답과 비교해서 점수를 매깁니다.

- **정확도(Precision@k)**: 가져온 문서 k개 중 정답이 몇 개인가?
- **재현율(Recall@k)**: 정답 문서 전체 중 몇 개를 찾았는가?
- **MRR(Mean Reciprocal Rank)**: 첫 번째 정답이 몇 번째에 나왔는가?
- **환각률(Hallucination Rate)**: 답변에 출처 없는 내용이 섞여 있는가?

성적표가 있으면 "리랭킹을 적용하니까 정확도(Precision@3)가 0.60에서 0.85로 올랐다"고 말할 수 있습니다. 느낌이 아니라 숫자입니다.

<!-- [GEMINI PROMPT: 10_eval-concept]
path: assets/CH10/10_eval-concept.png
Black and white minimalist infographic. White background, black/dark gray elements only.
Clean geometric shapes, thin lines, rounded corners on boxes. Modern sans-serif font. 16:9.

Title (top center, bold): "RAG 성적표 — 느낌이 아니라 숫자로"
Thin horizontal rule below title.

[Top — horizontal pipeline flow, 4 boxes connected by arrows]

[Box 1 — dashed border]
  Speech bubble icon, label: "질문"
  "보안 규정 알려줘"

→ [Box 2 — solid border, dark gray header bar]
  Header: "RAG 엔진"
  Gear icon inside

→ [Box 3 — solid border, split into top/bottom]
  Top section — 3 stacked document icons:
    ✓ SEC_보안규정_v1.0.pdf
    ✓ HR_취업규칙_v1.0.pdf
    ✗ FIN_매출현황.xlsx
  Label: "검색 결과 (상위 3개)"
  Bottom section — text block icon, label: "답변"

→ [Box 4 — solid border, clipboard icon]
  Header bar (dark gray, white text): "성적표"
  정확도: 67%
  재현율: 50%
  환각률: 10%

[Bottom — rounded rectangle, light gray fill, full width]
  Header: "개선 방향"
  3 columns, thin vertical dividers:
  | 정확도 낮음 → 리랭킹 강화 | 재현율 낮음 → 다중 질의 적용 | 환각률 높음 → 프롬프트 조정 | -->
![평가 프레임워크](../assets/CH10/10_eval-concept-2.png)
*그림 10-2: RAG 엔진의 성적표. 질문마다 검색 정확도와 환각률을 수치로 측정한다.*

---

### 성적표를 받았으니, 진짜 서비스를 만들자

성적표가 나왔습니다. 점수가 마음에 들든 안 들든, 이제 할 일은 명확합니다. 지금까지 만든 기술을 하나로 엮어서 **사람이 쓸 수 있는 화면**을 만드는 것입니다.

CH08의 하이브리드 검색, CH09의 약어 확장과 리랭킹 — 이 기술들이 코드 안에 흩어져 있습니다. 이걸 웹 UI 하나로 합치면, 브라우저에서 질문을 던지고 답변과 원본 문서 이미지를 바로 확인할 수 있습니다. 그리고 성적표로 "정말 좋아졌는지" 숫자로 비교합니다.

---

### 이번 버전에서 뭘 만드나

ex10은 마지막 버전입니다. 네 개 실습을 순서대로 따라가면 이미지까지 이해하는 RAG 챗봇이 완성됩니다.

| 실습 | 기능 | 비유 | 코드 |
|------|------|------|------|
| 1 | OCR vs 비전 LLM 비교 | 사서의 읽기 방식 비교 | `tuning/step1_document_parser/` |
| 2 | 하이브리드 이미지 처리 | 사서의 자동 판단 | `tuning/step2_hybrid_parser/` |
| 3 | RAG 평가 프레임워크 | 사서의 성적표 | `tuning/step3_eval_framework/` |
| 4 | 문서 캡처와 근거 표시 | 사서의 작업 공간 | `src/` |

실습 1에서 OCR과 비전 LLM 두 가지 읽기 방식을 비교합니다. 실습 2에서는 이 둘을 자동으로 선택하는 하이브리드 파이프라인을 만듭니다 — OCR로 충분하면 OCR, 스캔 이미지라 글자가 안 나오면 비전 LLM으로 전환하는 방식입니다. 실습 3에서 성적표를 만들어 품질을 숫자로 증명합니다.

마지막 실습 4에서 CH08~09 기술이 적용된 웹 UI를 직접 만들면서, 문서 캡처·근거 이미지 표시·검색 성능 비교까지 완성합니다.

---

### 전체 프로젝트 회고

CH01에서 LLM에게 "우리 회사 휴가 규정 알려줘"라고 물었습니다. LLM은 그럴듯하게 거짓말했습니다. 환각이었습니다. "아, LLM은 우리 회사 문서를 모르는구나." 그 깨달음에서 이 여정이 시작됐습니다.

CH02~CH03에서 사내 시스템의 기반을 다졌습니다. 직원, 연차, 매출 데이터를 API로 만들고, 사내 문서의 표준을 정했습니다. CH04에서 문서를 벡터로 바꾸는 기술을 배웠고, CH05에서 드디어 질문하면 답해주는 RAG 엔진을 완성했습니다.

하지만 "연차 몇 개? 규정은?"이라는 복합 질문에는 답하지 못했습니다. DB와 문서를 동시에 볼 수 없었으니까요. CH06에서 에이전트를 만들어 이 문제를 해결했고, CH07에서는 캐시와 모니터링으로 운영 안정성을 갖췄습니다.

CH08부터 본격적인 튜닝이 시작됐습니다. "엉뚱한 문서를 가져온다"는 문제를 청킹 최적화, 리랭킹, 하이브리드 검색으로 해결했습니다. CH09에서 질문 자체를 재구성하고 답변에 근거를 붙이는 기술을 추가했습니다. 그리고 이번 CH10에서 이미지까지 이해하는 사서를 만들고, 성적표로 품질을 수치화합니다.

돌이켜보면 이 책은 하나의 질문에서 출발했습니다. **"AI가 우리 회사 문서를 알게 하려면 어떻게 해야 하지?"** 그 질문의 답이 RAG이고, 10개 챕터가 그 답을 점진적으로 완성해가는 과정이었습니다.

환각을 보고 → 문서를 넣고 → 검색하고 → 답변하고 → 통합하고 → 안정화하고 → 튜닝하고 → 측정하고. 이 흐름 자체가 실무에서 AI 시스템을 만드는 과정과 같습니다.

---

## 기술 파트

### 용어 정리

| 이야기 속 표현 | 진짜 이름 | 정의 |
|---------------|----------|------|
| 사서의 확대경 | **광학 문자 인식(OCR, Optical Character Recognition)** | 이미지에서 문자를 인식하는 기술. EasyOCR 등의 엔진이 이미지 속 글자 위치와 내용을 추출한다 |
| 사서의 눈 | **비전 LLM(Vision LLM)** | 이미지를 입력으로 받아 내용을 이해하고 설명하는 멀티모달(Multimodal) 대형 언어 모델. Qwen2.5-VL, LLaVA, MiniCPM-V(로컬), GPT-4o, Gemini Pro Vision(클라우드) 등이 대표적 |
| 확대경+눈 자동 전환 | **하이브리드 이미지 처리(Hybrid Image Processing)** | OCR을 먼저 시도하고, 텍스트가 부족하면 비전 LLM으로 자동 전환하는 전략. 속도와 품질을 동시에 확보한다 |
| 사서의 성적표 — 정확도 | **정확도(Precision@k)** | 검색된 상위 k개 문서 중 실제 관련 문서의 비율. k=3일 때 3개 중 2개가 정답이면 Precision@3 = 0.67 |
| 사서의 성적표 — 재현율 | **재현율(Recall@k)** | 전체 정답 문서 중 상위 k개 안에 포함된 비율. 정답 4개 중 2개를 찾았으면 Recall@3 = 0.50 |
| 사서의 성적표 — MRR | **MRR(Mean Reciprocal Rank)** | 첫 번째 정답 문서가 검색 결과 몇 번째에 등장하는지의 역수. 1위에 정답이 있으면 1.0, 3위에 있으면 0.33 |
| 사서의 성적표 — 환각률 | **환각률(Hallucination Rate)** | 답변에서 출처 문서에 근거하지 않은 내용의 비율. 0에 가까울수록 좋다 |
| OCR 파싱 | **EasyOCR** | pip만으로 설치 가능한 오픈소스 OCR 라이브러리. PyTorch 기반이며 한국어를 포함해 80개 이상 언어를 지원한다 |
| 비전 LLM 파싱 | **Qwen2.5-VL (Qwen 2.5 Vision-Language)** | Ollama에서 실행 가능한 오픈소스 비전 LLM. 한국어를 공식 지원하며, 이미지를 base64로 인코딩하여 전달하면 구조화된 설명을 생성한다 |

### 실습 환경 구축

> 기본 환경(Python 3.12, Ollama, Docker)이 없다면 **부록(환경 설정)** 을 먼저 참고하세요.

```bash
cd ex10
cp .env.example .env
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
docker compose up -d       # PostgreSQL 실행 (실습 4에서 필요)

# 비전 LLM 모델 (실습 1, 2에서 사용)
ollama pull qwen2.5vl:7b
# 텍스트 LLM 모델 (실습 3 환각률 측정에서 사용)
ollama pull llama3.1:8b

pip install -r requirements.txt
```

> **이전 챕터 Docker 종료**: CH07의 Docker가 실행 중이라면 `cd ex07 && docker compose down` 으로 먼저 종료하세요.

> OCR 엔진 **EasyOCR** 은 `requirements.txt`에 포함되어 있어 별도 시스템 패키지 설치가 필요 없습니다. 비전 LLM은 컴퓨터 사양이 부족하면 `.env`에서 `VISION_PROVIDER=openai`로 전환할 수 있습니다.

| 패키지 | 역할 |
|--------|------|
| `PyMuPDF` | PDF -> 이미지 렌더링 + 텍스트 추출 |
| `easyocr` | OCR 파싱 (한국어+영어) |
| `chromadb` | 벡터DB 저장 |
| `rank-bm25` | BM25 키워드 검색 (하이브리드 검색) |
| `sentence-transformers` | Cross-Encoder 리랭킹 |
| `httpx` | Ollama API 호출 (실습 2, 3) |

### 파일 계층 구조

```
ex10/
├── tuning/                                     <- 실험 코드
│   ├── step1_document_parser/     [실습 1] OCR vs 비전 LLM 파싱 비교
│   ├── step2_hybrid_parser/       [실습 2] 하이브리드 이미지 처리 (OCR+Vision 자동 선택)
│   └── step3_eval_framework/      [실습 3] Precision@k, Recall@k, 환각률 평가
├── src/                            <- CH05~09 기술 통합 + 실습 4 코드
│   ├── capture.py                 [실습 4] 새로 작성 — PDF 캡처
│   ├── evidence.py                [실습 4] 새로 작성 — 근거 이미지 URL 변환
│   ├── agent_config.py            [참고] 에이전트 설정 (CH06)
│   ├── tools/search_documents.py  [설명] 검색 파이프라인 (CH08~09)
│   └── ...
├── app/                            [참고] FastAPI 웹 앱 (완성본)
├── data/                           [참고] 사내 문서 원본 + 평가 질문 세트
├── docker-compose.yml              [참고] PostgreSQL (ex07 동일)
└── run.py                          [참고] 서버 실행 진입점
```

> 실습 1~3은 `tuning/`에서 실험하고, 실습 4는 `src/`에 **새 파일을 직접 만들어** 작성합니다. 기존 파일(`agent_config.py`, `tools/` 등)은 CH05~09에서 만든 코드로 수정하지 않습니다.

### 실습 순서

```mermaid
flowchart LR
    A["실습 1<br>OCR vs 비전 LLM"] --> B["실습 2<br>하이브리드 처리"]
    B --> C["실습 3<br>평가 프레임워크"]
    C --> D["실습 4<br>완성 웹 UI"]

    classDef primary fill:#90EE90,stroke:#333,stroke-width:2px,color:darkgreen
    classDef secondary fill:#87CEEB,stroke:#333,stroke-width:2px,color:darkblue

    class A,B primary
    class C,D secondary
```

OCR과 비전 LLM을 비교하고(실습 1), 둘을 자동 선택하는 하이브리드 처리를 구현합니다(실습 2). 평가 프레임워크로 기준선을 잡고(실습 3), 마지막으로 CH08~09 기술이 통합된 웹 UI를 직접 만들면서 성능 변화를 확인합니다(실습 4).

---

### 실습 1: 문서 파싱 전략 비교 (tuning/step1_document_parser/)

이야기 파트에서 정보보안서약서 스캔본이 pypdf로 파싱되지 않는 문제를 경험했습니다. 스캔 PDF에서 텍스트를 뽑는 방법은 크게 두 가지입니다 — OCR(광학 문자 인식)과 비전 LLM. 같은 스캔 PDF를 두 방식으로 파싱하고 결과를 비교합니다.

| 파라미터 | 설명 | 권장값 |
|---------|------|--------|
| `--step` | 실험 단계 (1-1: OCR, 1-2: 비전 LLM) | -- |
| `--pdf_path` | 파싱할 PDF 경로 | `data/docs/hr/HR_정보보안서약서.pdf` |
| `--dpi` | 이미지 렌더링 해상도 | 150 |
| `--timeout` | 비전 LLM 타임아웃 초 (1-2 전용) | 200 |

#### 실험 1-1: OCR 파싱 — PyMuPDF + EasyOCR

OCR(Optical Character Recognition)은 이미지에서 글자를 인식하는 기술입니다. 스캔본처럼 텍스트 레이어가 없는 PDF도 읽을 수 있습니다. **EasyOCR** 은 PyTorch 기반의 오픈소스 OCR 라이브러리로, 한국어를 포함해 80개 이상의 언어를 지원합니다.

`ex10/tuning/step1_document_parser/parser.py` 의 `parse_pdf_ocr()` 함수가 핵심입니다. PDF 페이지를 이미지로 바꾸고, EasyOCR에게 "이 이미지에서 글자를 찾아줘"라고 맡깁니다.

```python
def parse_pdf_ocr(pdf_path, dpi=150):
    reader = easyocr.Reader(["ko", "en"], gpu=False)
    doc = fitz.open(str(pdf_path))
    page_texts = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(dpi=dpi)          # 페이지 → 이미지 렌더링
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        img_array = np.array(img)

        ocr_results = reader.readtext(img_array, detail=0)  # OCR
        page_texts.append("\n".join(ocr_results))
    return {"text": "\n\n".join(page_texts)}
```

`Reader(["ko", "en"])` — 한국어와 영어를 동시에 인식합니다. `gpu=False`는 CPU만으로 실행하는 옵션입니다. `detail=0`은 텍스트만 반환하고 좌표는 생략합니다.

```bash
python -m tuning.step1_document_parser --step 1-1
```

![실험 1-1: OCR 파싱 결과](../assets/CH10/10_step1-1-ocr.png)
*그림 10-2: OCR 파싱 결과. 스캔본에서 텍스트를 추출했지만 구조(표, 항목 번호)가 뭉개진다.*

OCR은 글자를 찾아내지만, 두 가지 한계가 있습니다. 첫째, 문서의 **구조**를 모릅니다. 표의 셀 경계를 인식하지 못하고, 조항 번호와 본문이 한 줄로 이어집니다. 결재란의 도장이나 서명도 무시합니다. 둘째, 글자 자체가 **깨지는** 경우가 많습니다. 스캔 품질이 낮거나 한국어처럼 획이 복잡한 문자에서는 "서약서"기 "서사서"으로, "스캔본"이 "스스년"으로 인식되기도 합니다. ICCV 2025에서 발표된 연구에 따르면, 최고 성능의 OCR 엔진도 원본 텍스트 대비 7.5% 이상의 정확도 차이가 발생합니다. 결국 OCR만으로는 "읽을 수 있는 문서"가 되지 않습니다. 다른 PDF로도 직접 확인해보세요.

```bash
# 다른 PDF로 실험
python -m tuning.step1_document_parser --step 1-1 --pdf_path data/docs/ops/OPS_신규서비스_런칭전략.pdf

# DPI를 높여서 실험 — 글자 인식률이 올라가는지 확인
python -m tuning.step1_document_parser --step 1-1 --dpi 200
```

#### 실험 1-2: 비전 LLM 파싱 — PyMuPDF + Qwen2.5-VL

비전 LLM은 여러 종류가 있습니다. 로컬에서 돌릴 수 있는 모델과 클라우드 API 모델로 나뉩니다.

| 모델 | 실행 환경 | 한국어 | 비고 |
|------|----------|:---:|------|
| **Qwen2.5-VL 7B** | Ollama (로컬) | O | 이 책에서 사용. 한국어 공식 지원 |
| LLaVA 7B | Ollama (로컬) | X | 영어만. 한국어 문서 인식 불가 |
| MiniCPM-V | Ollama (로컬) | △ | 한국어 일부 지원. 정확도 낮음 |
| GPT-4o / GPT-4o-mini | OpenAI API | O | 빠르고 정확. API 비용 발생 |
| Gemini Pro Vision | Google API | O | 한국어 우수. API 비용 발생 |

> 로컬 모델의 속도는 하드웨어에 따라 크게 달라집니다. 같은 Qwen2.5-VL 7B라도 RAM 16GB 환경에서 25초, 8GB 환경에서는 수 분이 걸릴 수 있습니다. 또한 Ollama에 다른 모델이 VRAM에 올라가 있으면 메모리 경합으로 속도가 급격히 느려지니, 비전 실험 전에 `ollama ps` 로 확인하세요.

이 책에서는 Ollama로 로컬 실행이 가능한 **Qwen2.5-VL 7B** 를 사용합니다. API 비용이 없고, 사내 문서를 외부 서버로 보내지 않아도 됩니다. 무엇보다 **한국어를 공식 지원**하는 로컬 비전 모델이라 한국어 사내 문서를 정확하게 읽어냅니다.

> **내 컴퓨터 사양이 부족하다면?** Qwen2.5-VL 7B 모델은 RAM 10GB 이상을 권장합니다. 다른 모델이 VRAM에 올라가 있으면 속도가 급격히 느려지니, 비전 실험 전에 `ollama ps`로 확인하세요. 모델 로딩이 너무 느리거나 메모리 부족 오류가 나면, `.env` 파일에서 `VISION_PROVIDER=openai`로 바꿔 GPT-4o-mini 비전 API를 사용할 수 있습니다.

같은 파일의 `parse_pdf_vllm()` 함수입니다. OCR과 마찬가지로 PDF 페이지를 이미지로 바꾸지만, 이번에는 비전 LLM에게 "이 이미지를 **분석**해줘"라고 맡깁니다. 글자만 찾는 OCR과 달리, 비전 LLM은 문서의 구조, 표, 도장까지 이해합니다.

```python
def parse_pdf_vllm(pdf_path, dpi=150):
    doc = fitz.open(str(pdf_path))
    page_texts = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(dpi=dpi)     # 페이지 → 이미지 렌더링
        img_path = f"_vllm_page_{page_num + 1}.png"
        pix.save(img_path)

        caption = _call_vision_llm(img_path) # 비전 LLM에게 이미지 분석 요청
        page_texts.append(caption)
        Path(img_path).unlink()             # 임시 이미지 삭제
    return {"text": "\n\n".join(page_texts)}
```

`get_pixmap(dpi=150)` — PDF 페이지를 통째로 이미지로 렌더링합니다. DPI(Dots Per Inch)는 1인치당 점의 개수, 즉 해상도입니다. 150이면 A4 한 페이지가 약 1240 × 1754 픽셀(Pixel)이 됩니다. 72로 낮추면 빠르지만 글자가 흐릿하고, 300으로 높이면 선명하지만 이미지 용량이 커져서 비전 LLM 처리 시간이 늘어납니다. 150은 표의 셀 구분이나 도장까지 식별할 수 있는 적절한 균형점입니다. `_call_vision_llm()`이 비전 LLM(기본 Ollama Qwen2.5-VL, 또는 OpenAI GPT-4o-mini)에 이미지를 베이스64(base64) 인코딩(Encoding)해서 보냅니다.

프롬프트(Prompt)가 중요합니다 — "마크다운 형식으로 출력하세요"가 없으면 비전 LLM이 자유 형식으로 답하기 때문에, 후속 청킹과 검색에 불리합니다. Qwen2.5-VL은 한국어를 지원하므로 프롬프트도 한국어로 작성합니다.

```python
_VISION_PROMPT = (
    "이 문서 이미지를 분석하세요. "
    "텍스트, 표, 도장, 서명, 구조적 요소를 빠짐없이 추출하세요. "
    "결과는 마크다운 형식으로 출력하세요. "
    "표는 마크다운 테이블 문법을 사용하세요."
)
```

타임아웃(Timeout)은 기본 600초로 넉넉하게 잡아두었습니다. 비전 LLM의 처리 시간은 컴퓨터 사양에 따라 크게 달라집니다 — 빠른 머신에서는 25초면 끝나지만, CPU만으로 돌리면 5분 이상 걸릴 수도 있습니다. 타임아웃 오류가 나면 `--timeout 900` 처럼 더 늘려주면 됩니다.

```bash
python -m tuning.step1_document_parser --step 1-2

# 타임아웃 늘리기 (첫 실행 시 모델 로딩이 오래 걸리면)
python -m tuning.step1_document_parser --step 1-2 --timeout 900
```

![실험 1-2: 비전 LLM 파싱 + 비교표](../assets/CH10/10_step1-2-vision.png)
*그림 10-3: 같은 스캔 PDF를 OCR과 비전 LLM으로 파싱한 결과. OCR은 텍스트만, 비전 LLM은 구조화된 마크다운을 추출했다.*

캡처 결과를 보면, 비전 LLM이 문서번호(2026-HR-SEC-002), 조항(제4조 생성형 AI 활용 지침), 금지 사항까지 마크다운 구조로 정리해냈습니다. OCR이 같은 내용을 평문으로 뽑아낸 것과 비교해보세요.

| 항목 | OCR (EasyOCR) | 비전 LLM (Qwen2.5-VL) |
|------|----------------|-----------------|
| 속도 | 약 13~50초 | 약 25~180초 |
| 텍스트 추출 | 평문 (구조 없음) | 마크다운 (구조화) |
| 표 인식 | 셀 경계 무시 | 마크다운 테이블 |
| 도장/서명 | 무시 | 시각 요소 설명 |
| 후속 검색 품질 | 보통 | 높음 |

다른 PDF와 DPI를 바꿔서 직접 비교해보세요.

```bash
# 다른 PDF로 실험 — 문서마다 차이가 다르다
python -m tuning.step1_document_parser --step 1-2 --pdf_path data/docs/ops/OPS_신규서비스_런칭전략.pdf

# DPI를 높여서 실험 (정밀도↑ 속도↓) — 150 vs 200, 추출량이 달라지는지 확인
python -m tuning.step1_document_parser --step 1-2 --dpi 200

# 두 전략을 한번에 비교
python -m tuning.step1_document_parser --step all
```

> **전략 선택 가이드**
>
> | 상황 | 추천 전략 |
> |------|----------|
> | 빠르게 텍스트만 필요 | OCR (EasyOCR) — 빠르지만 구조 없음 |
> | 구조/표/서명까지 필요 | 비전 LLM — 느리지만 마크다운 구조화 |
> | 대량 문서 처리 | OCR로 1차 필터링 후, 중요 문서만 비전 LLM |
> | 실무 최적 조합 | OCR + 비전 LLM 하이브리드 |

---

### 실습 2: 하이브리드 이미지 처리 (tuning/step2_hybrid_parser/)

실습 1에서 OCR과 비전 LLM을 비교했습니다. OCR은 빠르지만 구조를 모르고, 비전 LLM은 구조까지 파악하지만 느립니다. 실무에서는 둘 중 하나만 고르는 것이 아니라 **자동으로 선택**하게 만듭니다.

이 실습에서는 자동 선택의 두 가지 방식을 직접 실험합니다. 첫 번째 방식의 한계를 확인하고, 두 번째 방식으로 개선하는 흐름입니다.

| 파라미터 | 설명 | 권장값 |
|---------|------|--------|
| `--step` | 실험 단계 (2-1, 2-2, all) | -- |
| `--pdf` | 파싱할 PDF 경로 | `data/docs/hr/HR_정보보안서약서.pdf` |
| `--threshold` | OCR 판정 기준 글자 수 | 50 |

#### 실험 2-1: OCR 글자 수 기반 하이브리드

가장 직관적인 방법부터 시작합니다. OCR로 먼저 시도해서 텍스트가 충분히 나오면 그대로 쓰고, 글자가 거의 없으면 비전 LLM으로 전환합니다. `ex10/tuning/step2_hybrid_parser/hybrid_parser.py` 의 `process_image_hybrid()` 함수가 핵심입니다.

```python
def process_image_hybrid(page, dpi=150, threshold=None, vision_model=None):
    threshold = threshold or MIN_TEXT_LENGTH   # 기본 50자

    # Step 1: OCR 먼저
    ocr_text = _ocr_page(page, dpi=dpi)
    ocr_len = len(ocr_text.strip())

    # Step 2: 판정 — 50자 이상이면 OCR 채택
    if ocr_len >= threshold:
        return {"strategy": "ocr", "text": ocr_text, "char_count": ocr_len}

    # Step 3: 부족하면 Vision LLM 전환
    vision_text = _vision_page(page, dpi=dpi, model=vision_model)
    return {"strategy": "vision", "text": vision_text or ocr_text}
```

핵심은 `MIN_TEXT_LENGTH`, 즉 **최소 글자 수** 입니다. OCR이 뽑아낸 글자 수가 이 기준을 넘으면 OCR 결과를 채택하고, 넘지 못하면 비전 LLM으로 전환합니다. 기본값은 50자이며, `--threshold` 옵션이나 `.env`의 `MIN_TEXT_LENGTH`로 조절할 수 있습니다.

```bash
# 하이브리드 파싱 실행
python -m tuning.step2_hybrid_parser --step 2-1
```

![실험 2-1: 하이브리드 파싱 결과](../assets/CH10/10_step2-1-hybrid.png)

결과 테이블에서 페이지별로 어떤 전략이 선택되었는지 확인합니다. 텍스트가 풍부한 페이지는 OCR, 스캔본이나 이미지 위주 페이지는 비전 LLM이 자동으로 선택됩니다.

```bash
# 판정 기준을 80자로 높여서 실험 — 비전 LLM 전환이 더 자주 일어남
python -m tuning.step2_hybrid_parser --step 2-1 --threshold 80
```

**그런데 이 방식에는 함정이 있습니다.** 스캔 품질이 나쁜 PDF에서 OCR이 755자를 뽑았다고 해봅시다. 글자 수로는 기준 50을 훌쩍 넘기니 OCR을 채택합니다. 하지만 실제 텍스트를 보면 "서사서", "스스년"처럼 절반 이상이 깨진 글자입니다. 글자 수만으로는 **텍스트의 품질**까지 판단할 수 없다는 뜻입니다.

실무에서는 EasyOCR이 제공하는 **신뢰도(confidence) 점수**를 글자 수와 함께 활용하여 이런 경계 사례를 보완하기도 합니다. 하지만 더 근본적인 해결책이 있습니다.

#### 실험 2-2: 텍스트 레이어 기반 하이브리드

OCR 결과의 글자 수를 세는 대신, PDF 자체에 텍스트 정보가 들어 있는지 확인하는 방법입니다.

PDF에는 두 종류가 있습니다. 워드나 한글로 작성한 **디지털 PDF**는 텍스트 레이어가 내장되어 있어서 복사·붙여넣기가 됩니다. 반면 스캐너로 찍은 **스캔본 PDF**는 이미지만 들어 있어서 텍스트 레이어가 없습니다. PyMuPDF의 `get_text()`로 이 차이를 바로 확인할 수 있습니다.

`ex10/tuning/step2_hybrid_parser/hybrid_parser.py` 에 `process_image_textlayer()` 함수를 확인합니다.

```python
def process_image_textlayer(page, dpi=150, vision_model=None):
    # Step 1: 텍스트 레이어 확인
    text_layer = page.get_text().strip()

    # Step 2: 텍스트가 있으면 디지털 PDF — 그대로 사용
    if text_layer:
        return {"strategy": "text_layer", "text": text_layer,
                "char_count": len(text_layer)}

    # Step 3: 텍스트가 없으면 스캔본 — Vision LLM 전환
    vision_text = _vision_page(page, dpi=dpi, model=vision_model)
    return {"strategy": "vision", "text": vision_text,
            "char_count": len(vision_text) if vision_text else 0}
```

2-1과 비교해봅시다. OCR을 돌릴 필요 자체가 없습니다. 디지털 PDF라면 텍스트 레이어를 바로 가져오니 OCR보다 빠르고 정확합니다. 스캔본이라면 텍스트 레이어가 비어 있으니 확실하게 비전 LLM으로 전환됩니다. 깨진 글자에 속을 일이 없습니다.

```bash
# 텍스트 레이어 기반 하이브리드 실행
python -m tuning.step2_hybrid_parser --step 2-2
```

![실험 2-2: 텍스트 레이어 기반 하이브리드](../assets/CH10/10_step2-2-textlayer.png)

결과 테이블에서 "텍스트 레이어" 컬럼을 확인합니다. 디지털 PDF는 수천 자의 텍스트 레이어가 있어서 즉시 사용되고, 스캔본 PDF는 0자로 표시되며 비전 LLM이 처리합니다.

> **실무에서는 어떤 방식을 쓸까?**
>
> 대부분의 실무 파이프라인은 텍스트 레이어 확인(방법 2)을 기본으로 사용합니다. Grab, 네이버 등의 대규모 문서 처리 시스템도 텍스트 레이어 유무로 1차 분기한 뒤, 스캔본만 별도 OCR/비전 파이프라인으로 보냅니다.
>
> 그런데 최근 트렌드는 OCR을 아예 건너뛰는 방향입니다. 페이지 전체를 이미지로 캡처해서 비전 LLM에 바로 넘기는 세 번째 방식이 빠르게 확산되고 있습니다. GPT-4o, Qwen2.5-VL 같은 최신 비전 LLM은 텍스트뿐 아니라 표, 도장, 서명, 레이아웃까지 한 번에 이해합니다. 실습 1에서 확인했듯 OCR은 글자가 깨지고 구조가 뭉개지는 한계가 있습니다. 비전 LLM과 OCR을 결합하면 정확도가 크게 향상되며, OCR만 사용하는 것이 오히려 RAG 성능을 깎아먹을 수 있습니다.
>
> 정리하면 문서 처리 파이프라인의 흐름은 이렇게 진화하고 있습니다.
>
> | 세대 | 방식 | 장단점 |
> |------|------|--------|
> | 1세대 | OCR만 사용 | 빠르지만 구조 손실, 깨진 글자 |
> | 2세대 | 텍스트 레이어 + OCR/비전 LLM 분기 | 안정적, 현재 실무 표준 |
> | 3세대 | 페이지 전체를 비전 LLM에 전달 | 가장 정확, 비용·속도 트레이드오프 |
>
> 이 실습에서는 2세대 방식까지 직접 구현했습니다. 3세대 방식은 실습 4의 최종 웹 UI에서 직접 확인합니다.


---

### 실습 3: RAG 평가 프레임워크 (tuning/step3_eval_framework/)

AI 비서가 "잘 찾고 있다"는 걸 어떻게 증명할까요? 팀장이 "검색 품질 어때?"라고 물었을 때 "괜찮은 것 같습니다"로는 부족합니다. 숫자로 된 성적표가 필요합니다.

이 실습에서는 세 가지 지표를 하나씩 만들어봅니다. 각 지표마다 "무엇을 측정하는지" 이해하고, 코드를 확인한 뒤, 직접 실행해서 결과를 봅니다.

| 파라미터 | 설명 | 권장값 |
|---------|------|--------|
| `--step` | 실험 단계 (2-1, 2-2, 2-3, compare, all) | -- |
| `--k` | 상위 몇 개 결과를 평가할지 | `3` |

시험을 보려면 **정답지**가 먼저 있어야 합니다. `data/test_questions.json`이 그 역할을 합니다.

`ex10/data/test_questions.json`

```json
{
  "questions": [
    {
      "id": 1,
      "query": "연차 신청하려면 어떻게 해?",
      "relevant_sources": ["HR_취업규칙_v1.0"],
      "category": "비정형",
      "expected_answer": "AI HR 봇을 통해 스마트 휴가 승인 시스템으로 신청합니다."
    },
    {
      "id": 23,
      "query": "보안 규정이랑 휴가 규정 둘 다 알려줘",
      "relevant_sources": ["SEC_보안규정_v1.0", "HR_취업규칙_v1.0"],
      "category": "복합",
      "expected_answer": "보안규정과 취업규칙 두 문서의 내용을 종합하여 안내합니다."
    }
  ]
}
```

| 필드 | 설명 | 예시 |
|------|------|------|
| `query` | 사용자가 실제로 물어볼 질문 | "연차 신청하려면 어떻게 해?" |
| `relevant_sources` | 이 질문의 정답이 들어 있는 문서 이름 | `["HR_취업규칙_v1.0"]` |
| `expected_answer` | 기대하는 답변 요약 | "AI HR 봇으로 신청합니다." |
| `category` | 질문 유형 — 비정형, 정형, 복합 | "비정형" |

핵심은 `relevant_sources`입니다. 검색기가 가져온 문서가 여기 적힌 문서와 일치하면 "맞혔다", 다른 문서를 가져왔으면 "틀렸다"로 판정합니다. 이 파일에 총 37개 질문이 6개 문서에 걸쳐 들어있습니다. 이 중 7개는 의도적으로 어렵게 만든 **복합 질문**입니다. "재택근무 시 보안 규정은?"처럼 정답이 두세 개 문서에 걸쳐 있어서, 재현율(Recall) 차이를 뚜렷하게 보여줍니다.

> 평가용 벡터DB는 청크 크기를 200자로 설정했습니다. 문서 6개가 약 36개 청크로 나뉘어, k=3으로 검색하면 정답을 못 찾는 질문이 생깁니다. 실제 서비스의 검색 품질 차이를 체험하기 위한 의도적인 설정입니다.

---

#### 실험 3-1: 정확도(Precision@k) — "가져온 것 중 맞는 게 몇 개야?"

사서가 서가에서 책 3권을 가져왔습니다. 이 중 몇 권이 실제로 질문과 관련된 책일까요? 이것이 **정확도(Precision)** 입니다.

`ex10/tuning/step3_eval_framework/metrics.py` 의 `calculate_precision_at_k()` 함수입니다.

```python
def calculate_precision_at_k(retrieved_sources, relevant_sources, k):
    top_k = retrieved_sources[:k]
    relevant_set = set(relevant_sources)
    hits = sum(1 for src in top_k if any(rel in src for rel in relevant_set))
    return hits / k
```

3개를 가져왔는데 2개가 정답이면 Precision@3 = 2/3 = 0.67입니다.

```bash
python -m tuning.step3_eval_framework --step 2-1 --k 3
```

![실험 3-1: Precision@k 측정](../assets/CH10/10_step3-1-questions.png)

평균 Precision@3이 0.64입니다. 3개를 가져오면 1개 정도는 엉뚱한 문서라는 뜻입니다. 이 숫자가 실습 4의 완성 웹 UI에서 CH08~09 기술을 적용한 뒤 얼마나 올라가는지가 핵심입니다.

실행 결과에 **MRR(Mean Reciprocal Rank)** 도 함께 표시됩니다. 첫 번째 정답이 1위에 나오면 1.0, 2위에 나오면 0.5, 3위에 나오면 0.33입니다. "사용자가 원하는 답을 찾으려고 몇 번째까지 스크롤해야 하는가?"를 숫자로 보여주는 지표입니다.

---

#### 실험 3-2: 재현율(Recall@k) — "놓친 건 없어?"

정답 문서가 4개 있었는데, 사서가 그중 몇 개를 찾아왔을까요? 이것이 **재현율(Recall)** 입니다.

```python
def calculate_recall_at_k(retrieved_sources, relevant_sources, k):
    top_k = retrieved_sources[:k]
    relevant_set = set(relevant_sources)
    hits = sum(1 for rel in relevant_set if any(rel in src for src in top_k))
    return hits / len(relevant_set)
```

k를 늘리면 재현율은 올라가지만 정확도는 떨어질 수 있습니다. 이 **정확도-재현율 트레이드오프** 가 평가의 핵심입니다.

```bash
python -m tuning.step3_eval_framework --step 2-2 --k 3
```

![실험 3-2: Recall@3](../assets/CH10/10_step3-2-retrieval.png)

정답 문서가 1개인 질문은 k=3이면 대부분 찾아냅니다(R@3 = 1.00). 하지만 "재택근무 시 보안 규정은?"처럼 정답이 HR 규정 **과** 보안 규정 두 곳에 걸치는 복합 질문은 R@3이 낮아집니다. `--k` 값을 5, 10으로 바꿔가며 실험해보세요.

---

#### 실험 3-3: 환각률(Hallucination Rate) — "지어낸 건 없어?"

검색은 잘 찾았는데, LLM이 답변할 때 출처에 없는 내용을 지어내면 어떡할까요? CH01에서 처음 만났던 그 문제를, 이제 숫자로 잡아냅니다.

측정 흐름은 이렇습니다.

1. 질문 + 검색된 컨텍스트를 Ollama LLM에 전달하여 답변 생성
2. 답변에서 핵심 단어(3글자 초과)를 추출
3. 핵심 단어가 컨텍스트에 얼마나 포함되어 있는지 매칭률 계산
4. 매칭률이 30% 미만이면 "환각"으로 판정

```python
def estimate_hallucination_rate(answers, contexts):
    hallucination_count = 0
    for answer, context_docs in zip(answers, contexts):
        context_combined = " ".join(context_docs).lower()
        key_words = [w for w in answer.lower().split() if len(w) > 3]
        if key_words:
            context_words = set(context_combined.split())
            overlap = len([w for w in key_words if w in context_words]) / len(key_words)
            if overlap < 0.3:
                hallucination_count += 1
    return hallucination_count / len(answers) if answers else 0.0
```

```bash
python -m tuning.step3_eval_framework --step 2-3
```

> 이 실험은 Ollama LLM(llama3.1:8b)으로 37개 질문에 대한 답변을 생성합니다. 모델에 따라 1~3분 정도 소요됩니다.

![실험 3-3: 환각률 측정](../assets/CH10/10_step3-3-hallucination.png)

환각률이 높게 나오는 것이 정상입니다. 아직 리랭킹도, 쿼리 재작성도 적용하지 않은 상태이니까요. 검색이 엉뚱한 문서를 가져오면 LLM도 "그럴듯하게" 지어낼 수밖에 없습니다. 이 숫자가 바로 **개선의 출발점**입니다.

---

### 실습 4: 문서 캡처와 근거 표시 (src/capture.py, src/evidence.py)

지금까지 만든 기술을 하나의 웹 UI로 통합합니다. 이 실습에서는 `src/` 디렉토리에 **새 파일 2개를 직접 작성**합니다.

| 파일 | 역할 | 태그 |
|------|------|------|
| `src/capture.py` | 문서 캡처 (PDF → PNG + 텍스트 추출) | [실습] 새로 작성 |
| `src/evidence.py` | 근거 이미지 URL 변환 | [실습] 새로 작성 |
| `src/tools/search_documents.py` | 검색 파이프라인 (image_path 저장·반환) | [설명] CH08~09 확장 |
| `app/main.py` | FastAPI 진입점 + 정적 파일 마운트 | [참고] 완성본 |
| `app/chat_api.py` | 채팅 API (evidence.py 활용) | [참고] 완성본 |


#### 실습 4-1: 문서 캡처 (src/capture.py)

PDF 페이지를 이미지로 저장하고 텍스트를 함께 추출하는 모듈입니다. 아래 코드를 `ex10/src/capture.py`에 단계별로 나누어 작성합니다.

##### 1단계: 임포트 및 경로 설정

```python
"""문서 캡처 — PDF 페이지를 이미지로 저장한다."""

from pathlib import Path

import fitz  # PyMuPDF

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "data" / "docs"
CAPTURED_DIR = BASE_DIR / "data" / "captured" / "pdf"
```

`fitz`는 PyMuPDF 라이브러리입니다. `CAPTURED_DIR`은 캡처된 이미지가 저장될 경로입니다.

##### 2단계: 캡처 함수 작성

```python
def capture_pdf_pages(pdf_path):
    """PDF를 페이지별 PNG로 캡처하고 텍스트를 추출한다."""
    CAPTURED_DIR.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    results = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        # ① 페이지를 PNG 이미지로 렌더링
        pix = page.get_pixmap(dpi=200)
        img_path = CAPTURED_DIR / f"{pdf_path.stem}_page_{page_num + 1}.png"
        pix.save(str(img_path))
        # ② 텍스트 레이어도 함께 추출
        text = page.get_text()
        results.append({
            "page": page_num + 1,
            "image_path": str(img_path),   # ← 이 경로가 근거 이미지의 핵심
            "text": text,
            "metadata": {"source": pdf_path.name, "image_path": str(img_path)},
        })
    doc.close()
    return results
```

텍스트를 추출하는 동시에 **페이지 이미지도 저장**합니다. 핵심은 `image_path`입니다. 이 경로가 어떻게 흘러가는지 `src/tools/search_documents.py`에서 확인합니다.

##### [설명] search_documents.py — 검색 파이프라인 전체 흐름

CH05에서 기본 검색을 만들고, CH08~09에서 기술을 하나씩 추가해온 파일입니다. 현재 검색 파이프라인의 전체 흐름은 다음과 같습니다.

```mermaid
flowchart LR
    A["사용자 질문"] --> B["약어 확장<br/>(CH09)"]
    B --> C["HyDE<br/>(CH09)"]
    C --> D["하이브리드 검색<br/>벡터 + BM25<br/>(CH08)"]
    D --> E["리랭킹<br/>Cross-Encoder<br/>(CH08)"]
    E --> F["결과 + image_path<br/>(CH10)"]
```

CH10에서 달라진 부분만 짚겠습니다.

**① 벡터DB 저장 — image_path를 메타데이터에 포함**

```python
# search_documents.py — _build_vectorstore() 중 일부
for i, doc in enumerate(docs):
    meta = {"source": doc["source"], "page": doc.get("page", 1)}
    if doc.get("image_path"):
        meta["image_path"] = doc["image_path"]   # ← 캡처 이미지 경로
    collection.add(
        ids=[f"doc_{i}"],
        documents=[doc["content"]],
        metadatas=[meta],
    )
```

`capture.py`가 반환한 `image_path`가 ChromaDB 메타데이터에 저장됩니다. 텍스트와 이미지 경로가 같은 레코드에 묶이는 셈입니다.

**② 검색 결과 반환 — image_path를 꺼내 프론트엔드에 전달**

```python
# search_documents.py — search_documents() 중 일부
for doc in results:
    entry = {
        "content": doc["content"],
        "source": doc.get("source", "unknown"),
        "score": round(doc.get("rerank_score", doc.get("score", 0)), 4),
        "page": doc.get("page", ""),
    }
    if doc.get("image_path"):
        entry["image_path"] = doc["image_path"]  # ← 근거 이미지 전달
    formatted.append(entry)
```

검색 결과에 `image_path`가 포함되어 있으면 응답에 함께 담깁니다. `chat_api.py`가 이 경로를 받아 `evidence.py`의 `resolve_image_url()`로 웹 URL로 변환하고, 프론트엔드에 근거 이미지로 표시합니다.

---

#### 실습 4-2: 근거 이미지 URL 변환 (src/evidence.py)

캡처된 이미지의 절대 경로를 웹 브라우저에서 접근할 수 있는 URL로 변환하는 모듈입니다. 아래 코드를 `ex10/src/evidence.py`에 단계별로 나누어 작성합니다.

##### 1단계: 임포트 및 경로 설정

```python
"""근거 이미지 경로 변환 — 절대 경로를 웹 URL로 바꾼다."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CAPTURED_DIR = BASE_DIR / "data" / "captured"
```

##### 2단계: 경로 변환 함수

```python
def resolve_image_url(image_path):
    """절대 경로를 /captured/... 웹 URL로 변환한다."""
    captured_str = str(CAPTURED_DIR)
    if captured_str in image_path:
        relative = image_path.split("captured" + os.sep, 1)[-1]
        return f"/captured/{relative}"
    if image_path.startswith("/captured/"):
        return image_path
    return ""
```

`/Users/.../data/captured/pdf/HR_정보보안서약서_page_1.png` 같은 절대 경로가 `/captured/pdf/HR_정보보안서약서_page_1.png` 으로 변환됩니다. `app/chat_api.py`가 이 함수를 호출해서 채팅 응답의 `evidence_images` 리스트에 담습니다.

##### 3단계: 이미지 목록 조회 함수

```python
def list_captured_images():
    """캡처된 이미지 파일 목록과 웹 URL을 반환한다."""
    images = []
    if not CAPTURED_DIR.exists():
        return images

    for sub_dir in sorted(CAPTURED_DIR.iterdir()):
        if not sub_dir.is_dir():
            continue
        fmt = sub_dir.name.upper()
        for img in sorted(sub_dir.glob("*.png")):
            size_kb = img.stat().st_size / 1024
            web_url = resolve_image_url(str(img))
            images.append({
                "format": fmt,
                "filename": img.name,
                "size_kb": round(size_kb, 1),
                "web_url": web_url,
            })
    return images
```

---

#### 실습 4-3: 웹 서버 기동

`app/main.py`에 이미 완성본이 들어 있습니다. 핵심 구조만 확인합니다.

```python
# app/main.py — 핵심 부분
app = FastAPI(title="사내 AI 비서 — ex10")

# ① 정적 파일 마운트 — CSS/JS + 캡처 이미지
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/captured", StaticFiles(directory=_CAPTURED_DIR), name="captured")

# ② 라우터 등록
app.include_router(chat_router)
```

핵심은 `/captured` 마운트입니다. 실습 4-1에서 `data/captured/` 디렉토리에 저장한 PNG 파일을, 실습 4-2에서 `/captured/...` URL로 변환했고, 이 마운트 한 줄로 브라우저가 실제 이미지에 접근할 수 있게 됩니다.

> **데이터가 흐르는 경로**
>
> 캡처(4-1) → 벡터DB 저장(`image_path` 메타데이터) → 검색 → URL 변환(4-2) → API 응답 → 브라우저 표시(4-3)

나머지 인프라 코드(에이전트 설정, 라우터, 캐시, 모니터링)는 CH05~07에서 만든 것과 동일합니다. `src/` 디렉토리에 이미 들어 있으므로 별도로 작성하지 않습니다.

```bash
python run.py
```

브라우저에서 `http://localhost:8000`에 접속하여 질문을 던져보세요. 답변 아래에 원본 PDF 페이지 이미지가 근거로 표시됩니다. 썸네일을 클릭하면 원본 크기로 확대됩니다.

> **예시 질문**
> - "취업규칙에서 연차 관련 조항이 뭐야?"
> - "정보보안서약서에 어떤 내용이 있어?"
> - "신규서비스 런칭 전략 알려줘"

![웹 UI에서 질문을 던지면 답변 아래에 원본 PDF 페이지 이미지가 근거로 표시된다](../assets/CH10/10_step4-web-ui.png)

---

#### 실습 4-4: 성능 비교 — 실습 3의 성적표와 대조

실습 3에서 측정한 기준선과 비교합니다. CH08~09 기술(약어 확장, 하이브리드 검색, 리랭킹)이 `src/tools/search_documents.py`에 통합되어 있으므로, 웹 UI를 기동한 상태에서 평가 프레임워크를 다시 돌리면 됩니다.

```bash
python -m tuning.step3_eval_framework --step compare
```

[CAPTURE NEEDED]

| 적용 기술 | 출처 | 정확도 기여 | 비용 |
|----------|------|-----------|------|
| 약어/동의어 확장 | CH09 | 용어 불일치 해소 | 없음 |
| 하이브리드 검색 | CH08 | 키워드+의미 균형 | 없음 |
| 리랭킹 | CH08 | 순위 정밀도 향상 | Cross-Encoder 추론 |
| HyDE | CH09 | 스타일 갭 해소 | +1 LLM 호출 |

각 기술의 상세한 동작 원리는 CH08~09에서 다루었습니다. 여기서는 **통합 결과**를 숫자로 확인하는 것이 목적입니다.

---

### 더 알아보기

**RAGAS는 뭔가요?** — RAGAS(Retrieval Augmented Generation Assessment)는 RAG 시스템을 자동으로 평가하는 프레임워크입니다. 충실도(Faithfulness), 문맥 관련성(Context Relevancy), 답변 관련성(Answer Relevancy) 등 더 정교한 지표(Metric)를 제공합니다. 이 책에서는 평가의 기본 개념(정확도, 재현율, 환각률)에 집중하고, RAGAS 같은 고급 프레임워크는 다루지 않습니다. `step3_eval_framework/`에 RAGAS 연동 코드가 준비되어 있으니, 관심 있다면 `USE_RAGAS=true` 환경 변수를 설정하고 시도해보세요.

**테스트 케이스(Test Case)를 어떻게 만들어야 하나요?** — 실제 사용자가 자주 하는 질문 20~30개를 모으세요. 각 질문에 대해 "이 질문의 정답은 이 문서에 있다"를 표시합니다. `data/test_questions.json`이 바로 이 평가용 질문 파일입니다. 처음 만들 때 수작업이 필요하지만, 한 번 만들면 튜닝할 때마다 재사용할 수 있습니다.

**정확도와 재현율 중 뭐가 더 중요한가요?** — 사내 AI 비서에서는 정확도가 더 중요합니다. 사용자는 상위 3개 결과만 봅니다. 3개 중 2개가 엉뚱한 문서이면 신뢰를 잃습니다. 재현율은 놓친 문서가 있어도 상위 결과가 정확하면 사용자 경험에 큰 영향이 없습니다.

**OCR 결과를 마크다운으로 구조화할 수는 없나요?** — OCR은 글자만 뽑기 때문에 구조(제목, 조항, 표)가 없습니다. 두 가지 방법이 있습니다. 첫째, OCR로 텍스트를 뽑은 뒤 텍스트 LLM에게 "마크다운으로 정리해줘"라고 요청하는 2단계 방식입니다. 둘째, 정규식으로 "제N조"를 제목으로, "1."을 리스트로 바꾸는 규칙 기반 후처리입니다.

**하이브리드 처리의 최소 글자 수는 어떻게 정하나요?** — 실습 2-1에서 50자를 기본값으로 사용했습니다. OCR이 노이즈만 뽑는 스캔본은 보통 10~20자 이하이고, 텍스트가 포함된 PDF는 수백 자 이상이라 50자면 충분히 구분됩니다. 다만 실습 2-1에서 확인했듯 깨진 글자가 많으면 글자 수만으로는 한계가 있으므로, 실무에서는 실습 2-2의 텍스트 레이어 확인 방식을 권장합니다.

---

### 이것만은 기억하세요.

- **측정해야 개선할 수 있습니다.** Precision@k, Recall@k, MRR, Hallucination Rate — 이 네 가지 숫자가 RAG 시스템의 성적표입니다. 느낌이 아니라 숫자로 말하세요.
- **이미지도 문서입니다.** PDF 속 표, 차트, 조직도는 텍스트로 변환하면 정보가 손실됩니다. 하이브리드 처리로 OCR과 비전 LLM을 자동 선택하세요.
- **하이브리드가 답입니다.** 검색도 하이브리드(BM25+벡터), 이미지 처리도 하이브리드(OCR+Vision). 하나의 기술에 의존하지 말고 서로 보완하게 만드세요.
- **ex10이 끝이 아닙니다.** 성적표가 있으니 이제 어디를 개선해야 하는지 보입니다. 정확도가 낮으면 리랭킹을 강화하고, 환각률이 높으면 프롬프트를 조정하세요.
- **CH01에서 ex10까지, 이 여정의 핵심은 하나입니다.** "직접 만들어봐야 이해한다." 환각을 보고, 문서를 넣고, 검색하고, 답변하고, 통합하고, 안정화하고, 튜닝하고, 측정하고 — 이 흐름을 한 번 경험한 여러분은, 이제 어떤 RAG 시스템이든 만들 준비가 되었습니다.

에필로그에서 이 여정을 마무리합니다.
