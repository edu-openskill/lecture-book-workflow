# Comparisons

> 비교형 시각 요소. "A vs B", "before / after", "취소선으로 오류 표시" 같은 **대조**가 핵심인 컴포넌트.

## 속함

- `.annotated-compare` + `.ac-*` (LLM 환각 vs 사내규정, CH01)
- `.overlap-text-demo` + `.otd-*` (청크 오버랩 시각화, CH03)
- `.reindex-compare` + `.rc-arrow`, `.rc-badge-full`, `.rc-badge-inc` (전체 vs 증분 재인덱싱, CH03)
- `.cache-diff` (캐시 전후 시간선, CH07)
- `.dual-image` + `figure`/`figcaption` (2분할 이미지, CH04)

## 속하지 않음

- 순차 흐름 타임라인(`.rc-timeline`) → [`../pipelines/`](../pipelines/) — 같은 `rc-*` 접두어지만 별도
- 청크 단위 카드 → [`../cards/`](../cards/)

## 주의

`rc-*` 접두어는 이 카테고리(CH03 reindex-compare)와 pipelines 카테고리(CH07 rc-timeline) **두 곳에서 사용** 중이다. 신규 `rc-*` 클래스 추가 금지.

## 컴포넌트 목록

### .annotated-compare

**언제 쓰는가**: **A가 틀렸고 B가 맞을 때**. 취소선(`.ac-strike`)으로 A의 오류 구간을 시각적으로 지우고, 같은 주제에 대한 두 응답을 상하로 나란히 비교한다. "LLM 환각 vs Ground Truth"처럼 진실값이 명확한 2분할 대조 전용.

**사용 챕터**: CH01

**HTML 사용 예** (`projects/사내AI비서_v2/chapters/01-환각과-RAG의-첫-만남.md` L173-194):

```html
<div class="annotated-compare">
  <div class="ac-heading">LLM 응답과 사내 규정</div>
  <div class="ac-block llm">
    <div class="ac-label">
      <span class="ac-name">LLM 응답</span>
      <span class="ac-tech">Hallucination</span>
    </div>
    <div class="ac-content">
      커넥트의 신입사원 연차 규정은 <span class="ac-strike">근로기준법에 따라 입사 후 1년 미만 기간에는 1개월 개근 시 1일의 유급휴가가 발생하며, 1년 이상 근무 시에는 15일의 연차가 발생합니다.</span>
    </div>
    <div class="ac-note">취소선 부분이 학습 데이터에서 가져와 지어낸 내용입니다.</div>
  </div>
  <div class="ac-block truth">
    <div class="ac-label">
      <span class="ac-name">사내 규정</span>
      <span class="ac-tech">Ground Truth</span>
    </div>
    <div class="ac-content">
      커넥트 취업규칙에 따르면, 신입사원은 입사 후 <b>3년간 연차가 발생하지 않으며</b>, 그 기간 동안 <b>매월 1회 유급 리프레시 데이</b>를 사용할 수 있습니다.
    </div>
  </div>
</div>
```

**렌더 CSS**: `styles/diagrams.css:31-41` (주석형 비교 블록 정의), `styles/print.css:85, 100, 163, 176` (페이지 분할 허용 + 내부 블록 묶기 + 그림자 제거)

**변형**: `.ac-block`에 `.llm` 또는 `.truth` modifier로 제목 색(적색/녹색)이 결정된다. 하위 슬롯은 `.ac-heading`(전체 캡션), `.ac-label` > `.ac-name`/`.ac-tech`(이름 + 모노스페이스 기술 태그), `.ac-content`(본문), `.ac-strike`(오류 구간 취소선), `.ac-note`(아래쪽 각주).

**피해야 할 것**
- A와 B 둘 다 옳을 때 사용 금지. 진실값이 모호한 단순 대조는 의미 왜곡을 유발한다
- 취소선(`.ac-strike`)을 `.truth` 블록에 적용 금지. 오류 강조 전용이며 `.llm` 블록에서만 쓴다
- 3개 이상의 `.ac-block` 나열 금지. 2분할(오답/정답) 전용이며 다중 비교는 다른 컴포넌트로

---

### .overlap-text-demo

**언제 쓰는가**: **하나의 긴 문장을 청크 단위로 쪼갤 때 겹치는 구간을 하이라이트**할 때. 진실값 비교가 아니라 "같은 원본이 이렇게 잘린다"를 순차적으로 보여주는 용도. `<mark>`로 겹침 구간을 강조하고 `.otd-arrow`로 흐름을 아래로 이어간다. 청크 오버랩, 슬라이딩 윈도우처럼 **같은 원본 텍스트의 분할 결과를 나열**하는 경우에 쓴다.

**사용 챕터**: CH03

**HTML 사용 예** (`projects/사내AI비서_v2/chapters/03-어떤-문서를-넣을까.md` L140 부근):

```html
<div class="overlap-text-demo">
  <div class="otd-row otd-original">
    <span class="otd-label">원본</span>
    <span class="otd-text">신입사원은 첫 3년간 연차가 없습니다. 대신 매월 1회 리프레시 데이를 유급으로 제공합니다.</span>
  </div>
  <div class="otd-arrow">청크 크기 500자 · 오버랩 100자로 자르면</div>
  <div class="otd-row">
    <span class="otd-label c1">청크 1</span>
    <span class="otd-text">신입사원은 첫 3년간 연차가 없습니다. <mark>대신 매월 1회</mark></span>
  </div>
  <div class="otd-row">
    <span class="otd-label c2">청크 2</span>
    <span class="otd-text"><mark>대신 매월 1회</mark> 리프레시 데이를 유급으로 제공합니다.</span>
  </div>
  <div class="otd-note">겹친 <b>오버랩 구간</b>이 경계에서 문맥이 끊기지 않게 해줍니다.</div>
</div>
```

**렌더 CSS**: `styles/diagrams.css:379-435` (컨테이너 + 행 + 라벨 색상 + mark 강조 + 화살표 + 각주)

**변형**: `.otd-row`에 `.otd-original` modifier로 원본 행을 회색 배경으로 구분. `.otd-label`에 `.c1`/`.c2`/`.c3`로 청크별 색상(blue/indigo/purple). 각 행의 `<mark>`가 겹치는 구간을 노란색으로 강조.

**피해야 할 것**
- A vs B 진실값 비교에 사용 금지. `.annotated-compare`를 써야 한다
- `.c1`~`.c3` 외 청크 색상 정의되지 않음. 4분할 이상은 시각적으로 구분되지 않음
- `<mark>` 없이 나열만 하면 "겹침"이 드러나지 않아 컴포넌트 사용 의미가 사라진다

---

### .reindex-compare

**언제 쓰는가**: **두 가지 전략을 좌우 카드로 나란히 비교**할 때. 각 카드 안에 단계별 행(`.rc-row`)과 화살표(`.rc-arrow`)로 절차를 풀어내고, 문서 상태를 `.rc-doc` + modifier(`.rc-changed`/`.rc-keep`/`.rc-new`)로 색 구분한다. "전체 재인덱싱 vs 증분 재인덱싱"처럼 **같은 입력을 다르게 처리하는 두 전략**의 단계·비용·결과를 한눈에 대조하는 경우에 쓴다.

**사용 챕터**: CH03

**HTML 사용 예** (`projects/사내AI비서_v2/chapters/03-어떤-문서를-넣을까.md` L174 부근):

```html
<div class="reindex-compare">
  <div class="rc-card rc-full">
    <div class="rc-head">
      <span class="rc-badge rc-badge-full">전체</span>
      <span class="rc-subtitle">매번 전부 다시 계산</span>
    </div>
    <div class="rc-stage">
      <div class="rc-row">
        <span class="rc-stage-label">입력</span>
        <div class="rc-docs">
          <span class="rc-doc rc-changed">규정 v2</span>
          <span class="rc-doc rc-keep">가이드</span>
        </div>
      </div>
      <div class="rc-arrow">↓ 전체 재계산</div>
    </div>
  </div>
  <div class="rc-card rc-inc">
    <div class="rc-head">
      <span class="rc-badge rc-badge-inc">증분</span>
      <span class="rc-subtitle">바뀐 것만 다시</span>
    </div>
  </div>
</div>
```

**렌더 CSS**: `styles/diagrams.css:1644-1733` (2열 그리드 카드 + 배지 + 단계 행 + 문서 상태 색상 + 화살표)

**변형**: `.rc-badge-full`(danger 배경)과 `.rc-badge-inc`(info 배경)로 카드 헤더 색 구분. `.rc-doc`에 `.rc-changed`(주황/변경), `.rc-keep`(회색/유지), `.rc-new`(녹색/신규) modifier로 문서별 상태 표시.

**주의**: `rc-*` 접두어를 CH07 `.rc-timeline`과 공유하지만 별개 컴포넌트다. 이 카테고리 안에서는 `.reindex-compare` 하위로만 사용하고, 시간 순 타임라인은 pipelines 카테고리를 쓴다.

**피해야 할 것**
- 3개 이상 전략 비교 금지. `grid-template-columns: 1fr 1fr` 고정이므로 좌우 2열 전용
- 진실값 비교(`.annotated-compare`) 대체재로 쓰지 말 것. 이 컴포넌트는 "전략의 절차 대비"가 목적이지 "틀림/맞음"이 아니다
- `.rc-timeline`(pipelines)에 이 카드 스타일을 섞지 말 것. 접두어는 같지만 레이아웃이 다르다

---

### .cache-diff

**언제 쓰는가**: **두 캐시(혹은 두 저장소)의 항목별 스펙을 표 형태로 대조**할 때. 헤더(`.cd-head`)에 두 캐시 이름/배지를 두고 아래로 여러 `.cd-row`를 쌓아 "무엇을·얼마나·어디에·언제" 같은 항목별 차이를 행 단위로 비교한다. "ResponseCache vs EmbeddingCache"처럼 **같은 개념(캐시)의 두 구현체가 속성별로 어떻게 다른지** 펼쳐 보여주는 경우에 쓴다.

**사용 챕터**: CH07

**HTML 사용 예** (`projects/사내AI비서_v2/chapters/07-실제로-써보니.md` L340 부근):

```html
<div class="cache-diff">
  <div class="cd-head">
    <div class="cd-col-title cd-response">
      <span class="cd-badge">ResponseCache</span>답변 메모장
    </div>
    <div class="cd-col-title cd-embedding">
      <span class="cd-badge">EmbeddingCache</span>임베딩 메모장
    </div>
  </div>
  <div class="cd-row">
    <div class="cd-label">무엇을</div>
    <div>질문과 최종 답변</div>
    <div>텍스트와 임베딩 벡터</div>
  </div>
  <div class="cd-row">
    <div class="cd-label">어디에</div>
    <div>인메모리 딕셔너리</div>
    <div>SQLite 파일</div>
  </div>
</div>
```

**렌더 CSS**: `styles/diagrams.css:855` 부근 (컨테이너 + 110px 고정 라벨 열 + 1fr 1fr 데이터 열 + `.cd-response`/`.cd-embedding` CSS 변수로 배지 색상 지정)

**변형**: `.cd-col-title`에 `.cd-response`(인디고 `#4f46e5`) 또는 `.cd-embedding`(에메랄드 `#059669`) modifier로 `--cd-accent` 커스텀 속성이 바뀌어 배지 배경색이 결정된다. `.cd-badge`는 모노스페이스 폰트로 클래스 이름 그대로 표기.

**피해야 할 것**
- 시간 경과(before/after) 비교에 쓰지 말 것. 그리드는 항목별 스펙 대조용이지 타임라인이 아니다. 시간선은 `.rc-timeline`(pipelines)을 쓴다
- 3개 이상 캐시 비교 금지. `grid-template-columns: 110px 1fr 1fr` 고정
- 숫자 성능 비교(ms, MB)에만 치우치지 말 것. "무엇을·어디에·얼마나·언제"처럼 속성 전반을 보여주는 게 이 컴포넌트의 강점

---

### .dual-image

**언제 쓰는가**: **이미지 2장을 가로로 50%씩 배치**할 때. `figure` + `figcaption`으로 각각 캡션을 달 수 있다. 의미론적 A vs B 대조가 아니라, 한 화면으로는 너무 길어 잘리는 터미널 출력이나 스크린샷을 좌우로 나눠 담는 **공간 활용** 용도. 상단/하단, 좌/우, Swagger 요청/응답처럼 **같은 실행의 조각 2장**을 묶을 때 쓴다.

**사용 챕터**: CH04

**HTML 사용 예** (`projects/사내AI비서_v2/chapters/04-문서를-지식으로-바꾸다.md` L602-614):

```html
<div class="dual-image">
  <figure>
    <img src="../assets/CH04/terminal/04_cli-search_top.png" alt="">
    <figcaption>그림 4-8 (왼쪽). 쿼리와 상위 1, 2위 검색 결과</figcaption>
  </figure>
  <figure>
    <img src="../assets/CH04/terminal/04_cli-search_bottom.png" alt="">
    <figcaption>그림 4-8 (오른쪽). 3위 결과. 취업규칙의 휴가, 연차 관련 조항이 잡혔습니다</figcaption>
  </figure>
</div>
```

**렌더 CSS**: `styles/diagrams.css:120-143` (2열 그리드 + `figure` 여백 제거 + 이미지 100% width + 어두운 터미널 배경 + figcaption 이탤릭)

**변형**: modifier 클래스 없음. 이미지에 터미널 다크 배경(`#1a202c`)이 기본 적용되어 터미널 캡처에 최적화. figcaption은 "그림 N-N (왼쪽/오른쪽)" 식으로 동일한 그림 번호를 공유하고 좌우만 구분하는 패턴 권장.

**피해야 할 것**
- 의미 비교(A가 맞고 B가 틀림)에 사용 금지. 대조 의도가 있으면 `.annotated-compare` 또는 `.reindex-compare`를 쓴다
- 3장 이상 배치 금지. `grid-template-columns: 1fr 1fr` 고정이며 셋 이상은 레이아웃이 깨진다
- 개념도(gemini)를 두 장 넣지 말 것. 이미지 배경이 다크톤이라 개념도의 밝은 배경과 충돌한다. 터미널/스크린샷 전용
