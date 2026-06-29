# 슬라이드 컴포넌트 모음

`.step` 섹션 안에 그대로 붙여 쓰는 조각들. **글자는 최소**, 빈 공간은 판서로 채운다는 원칙을 지킬 것.
강조 클래스: `.hl`(노랑) `.hlb`(파랑) `.hlr`(빨강) `.hlg`(초록).

---

## 0. 기본 컷

```html
<section class="step">
  <div class="kicker">상단 라벨 (작게)</div>
  <h1>한 줄짜리 <span class="hlb">큰 메시지</span></h1>
  <div class="sub">보조 한 줄 — <span class="hl">핵심 단어만</span></div>
</section>
```
- 첫 섹션에만 `class="step active"`. 나머지는 `class="step"`.
- `<h1>` 안 `<br>`로 줄바꿈 가능. 두 줄을 넘기지 말 것.

## 1. 도발 질문 컷
큰 질문 한 줄 + 작은 후속 질문. (예: 오프닝)

```html
<section class="step">
  <div class="kicker">시작하기 전에</div>
  <h1>질문을 던진다.</h1>
  <div class="sub">…그리고 <span class="hl">한 번 더 비튼다.</span></div>
</section>
```

## 2. 썸네일 피드 (어그로/예시 나열)

```html
<div class="feed">
  <div class="thumb"><b>빨강 강조</b> 일반 텍스트</div>
  <div class="thumb">두 번째</div>
  <div class="thumb">세 번째</div>
  <div class="thumb">네 번째</div>
</div>
```
- `<b>`는 자동으로 빨간색. 카드 우상단에 ▶ 자동 표시.

## 3. 가로 게이지 (대비/비율 체감)

```html
<div class="gauges">
  <div class="grow"><div class="glabel">왼쪽 라벨</div>
    <div class="gbar"><div class="gfill" style="width:96%;background:linear-gradient(90deg,#ff7a3c,var(--warn))"></div></div></div>
  <div class="grow"><div class="glabel">오른쪽 라벨</div>
    <div class="gbar"><div class="gfill" style="width:7%;background:linear-gradient(90deg,#2e6b50,var(--green))"></div></div></div>
</div>
```
- `width`로 비율, `background`로 색을 직접 지정.

## 4. 번호 리스트 (약속/단계)

```html
<div class="promise">
  <div class="p"><span class="n">1</span><span>첫째 <span class="x">— 부연</span></span></div>
  <div class="p"><span class="n">2</span><span>둘째 <span class="x">— 부연</span></span></div>
  <div class="p"><span class="n">3</span><span>셋째 <span class="x">— 부연</span></span></div>
</div>
```
- 항목은 3개를 넘기지 말 것(판서 공간 확보).

## 5. 초대 / 다음 편 떡밥 컷

```html
<section class="step">
  <div class="kicker">초대</div>
  <h1>핵심 초대 문장.</h1>
  <div class="sub"><span class="hlb">다음 편 — 무엇을 다루는지 한 줄.</span></div>
</section>
```

---

## 강조색 바꾸기 (강의 톤)
`:root`의 변수만 바꾸면 전체 톤이 바뀐다. 기본은 다크 네이비 테크.
```css
--accent:#5cc8ff;  /* 전환·핵심(파랑) */
--warn:#ff5c6e;    /* 문제·경고(빨강) */
--gold:#ffd25c;    /* 강조(노랑) */
--green:#54e3a0;   /* 안심·긍정(초록) */
```

## 하지 말 것
- 한 컷에 문장 3줄 이상 넣기 (판서할 공간이 사라짐).
- 본문에 긴 설명 문단 넣기 → 그건 **대본**으로 간다.
- 엔진(`<style>`, `<script>`) 수정 — 레이아웃·펜·칠판이 깨진다.
