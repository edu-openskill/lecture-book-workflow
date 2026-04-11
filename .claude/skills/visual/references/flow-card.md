# 플로우 카드 디자인 시스템

시퀀스 다이어그램을 대체하는 HTML/CSS 기반 카드형 흐름도.
D2 색상 팔레트를 계승하며, JSON 입력 또는 HTML 직접 작성으로 생성한다.

---

## 1. 디자인 시스템

### 색상 팔레트

| 용도 | 색상 |
|------|------|
| 주요 stroke/accent | `#2563eb` |
| 주요 fill (연한 파랑) | `#eef2ff` |
| think/observe fill | `#f8f9ff`, stroke `#a5b4fc` |
| result fill (회색) | `#f8fafc`, stroke `#94a3b8` |
| 텍스트 (진한 파랑) | `#1e40af` |
| 텍스트 (진한 회색) | `#1e293b`, `#475569` |

### 타이포그래피

| 속성 | 값 |
|------|-----|
| 폰트 | Noto Sans KR |
| 라벨 | 11px, font-weight 700, letter-spacing 0.6px |
| 본문 텍스트 | 13px, font-weight 500 |
| 태그 | 10px, font-weight 600 |
| result 텍스트 | 11px, Menlo monospace |

---

## 2. 카드 타입 카탈로그

| 타입 | 아이콘 | fill | stroke | border | 용도 |
|------|--------|------|--------|--------|------|
| `route` | 분기 노드 (3 circles) | `#eef2ff` | `#2563eb` | solid | 라우팅/분류 |
| `think` | 전구 (lightbulb) | `#f8f9ff` | `#a5b4fc` | solid | 사고/판단 |
| `act` | 재생 버튼 (play) | `#ffffff` | `#2563eb` | solid | 실행/호출 |
| `result` | 문서 (document) | `#f8fafc` | `#94a3b8` | dashed | 데이터 반환 |
| `observe` | 눈 (eye) | `#f8f9ff` | `#a5b4fc` | solid | 관찰/평가 |
| `process` | 톱니바퀴 (gear) | `#eef2ff` | `#2563eb` | solid | 일반 처리 |
| `store` | 실린더 (cylinder) | `#f8fafc` | `#94a3b8` | solid | 저장소 |

> 이 카탈로그는 새 카드 타입 생성 시 자동 추가됩니다.

---

## 3. SVG 아이콘 세트

### chat (말풍선) -- 시작 캡슐용

```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
```

### chat-check (체크 말풍선) -- 끝 캡슐용

```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><polyline points="9,11 11,13 15,9"/></svg>
```

### route (분기 노드)

```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="18" cy="19" r="3"/><circle cx="6" cy="12" r="3"/><path d="M8.59 13.51l6.83 3.98M15.41 6.51l-6.82 3.98"/></svg>
```

### think (전구)

```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/></svg>
```

### act (재생 버튼)

```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="10,8 16,12 10,16" fill="currentColor"/></svg>
```

### result (문서)

```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14,2 14,8 20,8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
```

### observe (눈)

```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
```

---

## 4. 레이아웃 패턴

| 패턴 | 방향 | 그룹 내부 | 적합한 상황 |
|------|------|----------|------------|
| **LR** | 가로 1줄 | -- | 단계 3~4개, 넓은 이미지 |
| **TB** | 세로 1줄 | -- | 단계 5개 이상, 좁은 이미지 |
| **LR + 2x2 그리드** | 가로 | 그룹 내부 2x2 | ReAct 패턴 등 순환 구조 |
| **TB + 인라인 그룹** | 세로 | 그룹 내부 가로 | 병렬 처리 표현 |

---

## 5. 구성 요소

### 캡슐 (시작/끝)

- `border-radius: 24px`
- 구성: 아이콘(28x28) + 제목(13px bold) + 설명(12px)
- 시작: `background: #fff`, `border: 2px solid #2563eb`
- 끝: `background: #eef2ff`, `border: 2px solid #2563eb`

### 카드 (중간 단계)

- `width: 186px` (LR), `max-width: 600px` (TB)
- `border-radius: 6px` (LR), `12px` (TB)
- 구성: 아이콘(24x24) + 라벨(타입명) + 텍스트 + 태그(선택)
- 태그: `border-radius: 4px`, `background: #f1f5f9`, `border: 1px solid #cbd5e1`

### 그룹 컨테이너

- `border: 2px dashed #2563eb`
- `border-radius: 10px` (LR), `16px` (TB)
- 라벨: `position: absolute`, `top: -10px`, `left: 20px`
- 라벨 배경: `#fff` (텍스트 위 border 가림 처리)

### 화살표/연결선

- LR 화살표: `width: 40px`, `height: 2px` shaft + 삼각형 화살촉
- TB 연결선: `width: 2px`, `height: 20px`
- 일반 색상: `#cbd5e1`
- 강조 색상: `#2563eb`

---

## 6. JSON 입력 스펙

```json
{
  "type": "flow-card",
  "start": { "icon": "chat", "title": "string", "desc": "string" },
  "steps": [
    {
      "type": "route|think|act|result|observe|process|store",
      "text": "string",
      "tag": "string (optional)",
      "num": "string (optional)"
    },
    {
      "type": "group",
      "label": "string",
      "layout": "inline|grid-2x2",
      "steps": [ "..." ]
    }
  ],
  "end": { "icon": "chat-check", "title": "string", "desc": "string" }
}
```

### 예시

```json
{
  "type": "flow-card",
  "start": { "icon": "chat", "title": "사용자", "desc": "홍길동 입사일 언제야?" },
  "steps": [
    { "type": "route", "text": "QueryRouter\n키워드 매칭", "tag": "structured" },
    {
      "type": "group",
      "label": "ReAct 패턴",
      "layout": "grid-2x2",
      "steps": [
        { "type": "think", "text": "list_employees\n도구를 써야지", "num": "01" },
        { "type": "act", "text": "list_employees\n(\"홍길동\")", "tag": "PostgreSQL", "num": "02" },
        { "type": "result", "text": "{hire_date:\n\"2026-01-01\"}", "num": "03" },
        { "type": "observe", "text": "입사일을 찾았다.\n답변 생성하자.", "num": "04" }
      ]
    }
  ],
  "end": { "icon": "chat-check", "title": "답변", "desc": "홍길동 사원의 입사일은\n2026년 1월 1일입니다." }
}
```

---

## 7. 렌더링 명령어

```bash
# 단일 렌더링
node render-flow.js input.json output.png

# 4가지 변형 생성
node render-flow.js input.json --variations output-dir/

# GIF 애니메이션
node render-flow.js input.json --gif output.gif
```

---

## 8. HTML 직접 작성 가이드

JSON 렌더러를 사용할 수 없을 때, PoC 코드를 템플릿으로 삼아 HTML을 직접 작성한다.

### 작성 순서

1. PoC HTML 중 원하는 레이아웃(LR 또는 TB)을 복사한다
2. `<style>` 블록은 그대로 유지한다 (디자인 시스템 색상이 이미 적용됨)
3. `#diagram` 내부의 카드를 수정한다
   - 캡슐: `.cap.start`, `.cap.end`의 제목/설명 변경
   - 카드: 타입 클래스(`route`, `think`, `act`, `result`, `observe`) 적용
   - 그룹: `.react-group` (LR) 또는 `.react-loop` (TB) 컨테이너 사용
4. SVG 아이콘은 3절의 아이콘 세트에서 복사하여 `stroke` 색상만 해당 타입에 맞게 변경한다
   - route/act: `stroke="#2563eb"`
   - think/observe: `stroke="#6366f1"`
   - result: `stroke="#64748b"`
5. Puppeteer 또는 Playwright로 `#diagram` 요소를 PNG 캡처한다

### 카드 추가/제거

- LR: `.flow` 안에 `.arrow` + `.card` 쌍을 추가/제거
- TB: `.flow` 안에 `.connector` + `.card` 쌍을 추가/제거
- 그룹 내부: `.grid-2x2` 또는 인라인 flex 안에 `.card` 추가/제거

---

## 9. PoC 코드

### 9-1. LR + 2x2 그리드 (`poc-flow-lr.html`)

확정된 디자인. 가로 배치 + ReAct 그룹 내부 2x2 그리드.

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&display=swap');
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #fff; padding: 48px 32px; font-family: 'Noto Sans KR', sans-serif; }

  .flow { display: flex; align-items: center; gap: 0; justify-content: center; }

  /* -- 시작/끝 캡슐 -- */
  .cap {
    padding: 16px 22px; border-radius: 24px;
    text-align: center; flex-shrink: 0;
    display: flex; flex-direction: column; align-items: center; gap: 6px;
  }
  .cap .icon { width: 28px; height: 28px; }
  .cap.start { background: #fff; border: 2px solid #2563eb; }
  .cap.end   { background: #eef2ff; border: 2px solid #2563eb; }
  .cap .title { font-size: 13px; font-weight: 700; color: #2563eb; }
  .cap .desc  { font-size: 12px; color: #475569; line-height: 1.4; }

  /* -- 수평 화살표 -- */
  .arrow {
    width: 40px; display: flex; align-items: center; flex-shrink: 0; position: relative;
  }
  .arrow .shaft { width: 100%; height: 2px; background: #cbd5e1; }
  .arrow .shaft::after {
    content: ''; position: absolute; right: 0; top: 50%; transform: translateY(-50%);
    border: 5px solid transparent; border-left: 7px solid #cbd5e1;
  }
  .arrow.blue .shaft { background: #2563eb; }
  .arrow.blue .shaft::after { border-left-color: #2563eb; }

  /* -- 카드 공통 -- */
  .card {
    width: 186px; min-height: 84px;
    border-radius: 6px; padding: 12px 14px;
    display: flex; flex-direction: row; align-items: flex-start; gap: 10px;
    flex-shrink: 0;
  }
  .card .icon { width: 24px; height: 24px; flex-shrink: 0; margin-top: 2px; }
  .card .content { flex: 1; }
  .card .label {
    font-size: 11px; font-weight: 700; letter-spacing: 0.6px; margin-bottom: 4px;
  }
  .card .text {
    font-size: 13px; font-weight: 500; line-height: 1.5; color: #1e293b;
  }
  .card .tag {
    display: inline-block; margin-top: 6px; padding: 2px 10px;
    border-radius: 4px; font-size: 10px; font-weight: 600;
    background: #f1f5f9; border: 1px solid #cbd5e1; color: #475569;
    width: fit-content;
  }

  /* 타입별 */
  .card.route   { background: #eef2ff; border: 1.5px solid #2563eb; }
  .card.route .label { color: #2563eb; }
  .card.route .text  { color: #1e40af; }

  .card.think   { background: #f8f9ff; border: 1.5px solid #a5b4fc; }
  .card.think .label { color: #6366f1; }
  .card.think .text  { color: #1e40af; }

  .card.act     { background: #ffffff; border: 1.5px solid #2563eb; }
  .card.act .label { color: #2563eb; }

  .card.result  { background: #f8fafc; border: 1.5px dashed #94a3b8; }
  .card.result .label { color: #64748b; }
  .card.result .text  { color: #475569; font-family: 'Menlo', monospace; font-size: 11px; }

  .card.observe { background: #f8f9ff; border: 1.5px solid #a5b4fc; }
  .card.observe .label { color: #6366f1; }
  .card.observe .text  { color: #1e40af; }

  /* -- ReAct 2x2 그리드 -- */
  .react-group {
    border: 2px dashed #2563eb; border-radius: 10px;
    padding: 24px 18px 18px 18px; position: relative;
    background: #fcfcff; flex-shrink: 0;
  }
  .react-group .group-label {
    position: absolute; top: -10px; left: 20px;
    background: #fff; padding: 0 10px;
    font-size: 11px; font-weight: 700; color: #2563eb; letter-spacing: 0.6px;
  }
  .grid-2x2 {
    display: grid;
    grid-template-columns: 186px 186px;
    grid-template-rows: auto auto;
    gap: 12px;
  }
  .grid-2x2 .card { position: relative; }

  /* 01->02 오른쪽 화살표 */
  .grid-2x2 .card.think::after {
    content: ''; position: absolute; right: -9px; top: 50%; transform: translateY(-50%);
    border: 5px solid transparent; border-left: 6px solid #a5b4fc;
  }
  /* 02->03 아래 화살표 */
  .grid-2x2 .card.act::after {
    content: ''; position: absolute; bottom: -9px; left: 50%; transform: translateX(-50%);
    border: 5px solid transparent; border-top: 6px solid #2563eb;
  }
  /* 03->04 왼쪽 화살표 */
  .grid-2x2 .card.result::before {
    content: ''; position: absolute; left: -9px; top: 50%; transform: translateY(-50%);
    border: 5px solid transparent; border-right: 6px solid #94a3b8;
  }
</style>
</head>
<body>
<div class="flow" id="diagram">

  <!-- 시작: 말풍선 아이콘 -->
  <div class="cap start">
    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    </svg>
    <div class="title">사용자</div>
    <div class="desc">홍길동 입사일 언제야?</div>
  </div>

  <div class="arrow"><div class="shaft"></div></div>

  <!-- 라우트: 갈림길 아이콘 -->
  <div class="card route">
    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="18" cy="5" r="3"/><circle cx="18" cy="19" r="3"/>
      <circle cx="6" cy="12" r="3"/>
      <path d="M8.59 13.51l6.83 3.98M15.41 6.51l-6.82 3.98"/>
    </svg>
    <div class="content">
      <div class="label">ROUTE</div>
      <div class="text">QueryRouter<br>키워드 매칭</div>
      <div class="tag">structured</div>
    </div>
  </div>

  <div class="arrow blue"><div class="shaft"></div></div>

  <!-- ReAct 2x2 -->
  <div class="react-group">
    <div class="group-label">ReAct 패턴</div>
    <div class="grid-2x2">

      <!-- 01 THINK: 전구 -->
      <div class="card think">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 18h6M10 22h4"/>
          <path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/>
        </svg>
        <div class="content">
          <div class="label">01 THINK</div>
          <div class="text">list_employees<br>도구를 써야지</div>
        </div>
      </div>

      <!-- 02 ACT: 재생(실행) -->
      <div class="card act">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"/>
          <polygon points="10,8 16,12 10,16" fill="#2563eb"/>
        </svg>
        <div class="content">
          <div class="label">02 ACT</div>
          <div class="text">list_employees<br>("홍길동")</div>
          <div class="tag">PostgreSQL</div>
        </div>
      </div>

      <!-- 04 OBSERVE: 눈 -->
      <div class="card observe">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
          <circle cx="12" cy="12" r="3"/>
        </svg>
        <div class="content">
          <div class="label">04 OBSERVE</div>
          <div class="text">입사일을 찾았다.<br>답변 생성하자.</div>
        </div>
      </div>

      <!-- 03 RESULT: 문서 -->
      <div class="card result">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14,2 14,8 20,8"/>
          <line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
        </svg>
        <div class="content">
          <div class="label">03 RESULT</div>
          <div class="text">{hire_date:<br>"2026-01-01"}</div>
        </div>
      </div>

    </div>
  </div>

  <div class="arrow blue"><div class="shaft"></div></div>

  <!-- 끝: 체크 말풍선 -->
  <div class="cap end">
    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#1e40af" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      <polyline points="9,11 11,13 15,9"/>
    </svg>
    <div class="title">답변</div>
    <div class="desc">홍길동 사원의 입사일은<br>2026년 1월 1일입니다.</div>
  </div>

</div>
</body>
</html>
```

### 9-2. TB 세로 배치 (`poc-flow.html`)

세로 배치 버전. 단계가 많거나 좁은 이미지에 적합.

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;600;700&display=swap');
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #fff; padding: 36px 24px; font-family: 'Noto Sans KR', sans-serif; }

  .flow { display: flex; flex-direction: column; align-items: center; gap: 0; max-width: 700px; margin: 0 auto; }

  /* -- 스텝 연결선 -- */
  .connector { width: 2px; height: 20px; background: #cbd5e1; }
  .connector.long { height: 28px; }

  /* -- 카드 공통 -- */
  .card {
    border-radius: 12px; padding: 14px 24px;
    display: flex; align-items: center; gap: 14px;
    max-width: 600px; width: 100%;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }

  /* -- 질문 카드 -- */
  .card.question {
    background: #fff; border: 2px solid #2563eb;
    justify-content: center; flex-direction: column; gap: 4px;
  }
  .card.question .who { font-size: 11px; color: #2563eb; font-weight: 700; letter-spacing: 0.5px; }
  .card.question .text { font-size: 15px; color: #1e293b; font-weight: 600; }

  /* -- 라우팅 뱃지 -- */
  .badge-row { display: flex; align-items: center; gap: 10px; }
  .badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 600;
  }
  .badge.router {
    background: #eef2ff; border: 1.5px solid #2563eb; color: #1e40af;
  }
  .badge.type {
    background: #f8fafc; border: 1.5px solid #94a3b8; color: #475569;
  }
  .badge-arrow { color: #94a3b8; font-size: 16px; }

  /* -- ReAct 루프 컨테이너 -- */
  .react-loop {
    border: 2px dashed #2563eb; border-radius: 16px;
    padding: 20px; display: flex; flex-direction: column;
    align-items: center; gap: 0; width: 100%; max-width: 600px;
    position: relative; background: #fafbff;
  }
  .react-label {
    position: absolute; top: -11px; left: 24px;
    background: #fff; padding: 0 10px;
    font-size: 11px; font-weight: 700; color: #2563eb;
    letter-spacing: 1px;
  }

  /* -- 생각 카드 -- */
  .card.think {
    background: #eef2ff; border: 1.5px solid #93a3eb;
  }
  .card.think .icon { font-size: 20px; flex-shrink: 0; width: 32px; text-align: center; }
  .card.think .label { font-size: 11px; color: #6366f1; font-weight: 700; margin-bottom: 2px; }
  .card.think .text { font-size: 13px; color: #1e40af; font-weight: 500; }

  /* -- 행동 카드 -- */
  .card.action {
    background: #fff; border: 1.5px solid #2563eb;
  }
  .card.action .icon { font-size: 20px; flex-shrink: 0; width: 32px; text-align: center; }
  .card.action .label { font-size: 11px; color: #2563eb; font-weight: 700; margin-bottom: 2px; }
  .card.action .text { font-size: 13px; color: #1e293b; font-weight: 500; }
  .card.action .target {
    margin-left: auto; padding: 4px 12px; border-radius: 6px;
    background: #f8fafc; border: 1px solid #94a3b8;
    font-size: 11px; color: #475569; font-weight: 600; flex-shrink: 0;
  }

  /* -- 결과 카드 -- */
  .card.result {
    background: #f8fafc; border: 1.5px dashed #94a3b8;
  }
  .card.result .icon { font-size: 20px; flex-shrink: 0; width: 32px; text-align: center; }
  .card.result .label { font-size: 11px; color: #64748b; font-weight: 700; margin-bottom: 2px; }
  .card.result .text { font-size: 12px; color: #475569; font-weight: 400; font-family: 'Menlo', monospace; }

  /* -- 관찰 카드 -- */
  .card.observe {
    background: #eef2ff; border: 1.5px solid #93a3eb;
  }
  .card.observe .icon { font-size: 20px; flex-shrink: 0; width: 32px; text-align: center; }
  .card.observe .label { font-size: 11px; color: #6366f1; font-weight: 700; margin-bottom: 2px; }
  .card.observe .text { font-size: 13px; color: #1e40af; font-weight: 500; }

  /* -- 최종 답변 -- */
  .card.answer {
    background: linear-gradient(135deg, #eef2ff 0%, #dbeafe 100%);
    border: 2px solid #2563eb;
    justify-content: center; flex-direction: column; gap: 4px;
  }
  .card.answer .who { font-size: 11px; color: #2563eb; font-weight: 700; letter-spacing: 0.5px; }
  .card.answer .text { font-size: 14px; color: #1e293b; font-weight: 500; line-height: 1.5; }

  .step-text { display: flex; flex-direction: column; }
</style>
</head>
<body>
<div class="flow" id="diagram">

  <!-- 질문 -->
  <div class="card question">
    <div class="who">사용자</div>
    <div class="text">홍길동 입사일 언제야?</div>
  </div>

  <div class="connector"></div>

  <!-- 라우팅 -->
  <div class="badge-row">
    <div class="badge router">QueryRouter</div>
    <div class="badge-arrow">-></div>
    <div class="badge type">1단계: 키워드 매칭 -> structured (정형)</div>
  </div>

  <div class="connector"></div>

  <!-- ReAct 루프 -->
  <div class="react-loop">
    <div class="react-label">ReAct 패턴</div>

    <!-- 생각 -->
    <div class="card think">
      <div class="icon" style="font-size:13px; color:#6366f1; font-weight:700;">01</div>
      <div class="step-text">
        <div class="label">THINK</div>
        <div class="text">list_employees 도구를 써야지</div>
      </div>
    </div>

    <div class="connector"></div>

    <!-- 행동 -->
    <div class="card action">
      <div class="icon" style="font-size:13px; color:#2563eb; font-weight:700;">02</div>
      <div class="step-text">
        <div class="label">ACT</div>
        <div class="text">list_employees("홍길동")</div>
      </div>
      <div class="target">PostgreSQL</div>
    </div>

    <div class="connector"></div>

    <!-- 결과 -->
    <div class="card result">
      <div class="icon" style="font-size:13px; color:#64748b; font-weight:700;">03</div>
      <div class="step-text">
        <div class="label">RESULT</div>
        <div class="text">{name: "홍길동", hire_date: "2026-01-01"}</div>
      </div>
    </div>

    <div class="connector"></div>

    <!-- 관찰 -->
    <div class="card observe">
      <div class="icon" style="font-size:13px; color:#6366f1; font-weight:700;">04</div>
      <div class="step-text">
        <div class="label">OBSERVE</div>
        <div class="text">입사일을 찾았다. 답변을 생성하자.</div>
      </div>
    </div>

  </div>

  <div class="connector long"></div>

  <!-- 최종 답변 -->
  <div class="card answer">
    <div class="who">통합 에이전트 -> 사용자</div>
    <div class="text">홍길동 사원의 입사일은 2026년 1월 1일입니다.</div>
  </div>

</div>
</body>
</html>
```
