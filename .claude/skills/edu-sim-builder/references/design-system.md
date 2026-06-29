# 디자인 시스템 — 다크 네이비 테크 테마 (고정)

모든 시뮬레이터는 이 토큰을 쓴다. 색을 즉흥적으로 바꾸지 말 것. 평평(flat)하게, 그라데이션 남발
금지(배경 메시 정도만 허용).

## 폰트 (head에 넣기)

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700&display=swap">
```
본문 = Pretendard, 숫자/코드 = JetBrains Mono(`var(--mono)`).

## :root 토큰

```css
:root{
  --bg:#060814; --bg-soft:#0F1424;
  --surface:rgba(255,255,255,0.04); --surface-2:rgba(255,255,255,0.07);
  --border:rgba(255,255,255,0.08); --border-strong:rgba(255,255,255,0.15);
  --text:#F8FAFC; --muted:#94A3B8; --dim:#475569;
  --indigo:#818CF8; --indigo-deep:#4F46E5;
  --amber:#FBBF24; --amber-deep:#D97706;
  --rose:#F43F5E; --emerald:#34D399; --cyan:#22D3EE;
  --mono:'JetBrains Mono',monospace;
}
```
의미 색 관례: **indigo**=중립/기본 요소·벡터, **amber**=질문/강조, **emerald/lime(#A3E635)**=좋음·성공·정답,
**rose**=나쁨·충돌·할루시네이션, **cyan**=보조선/수선, **muted/dim**=부차 텍스트.

## body 배경 (은은한 메시)

```css
body{
  font-family:'Pretendard Variable',Pretendard,-apple-system,sans-serif; color:var(--text);
  background:
    radial-gradient(ellipse at top left,rgba(99,102,241,0.12) 0%,transparent 50%),
    radial-gradient(ellipse at bottom right,rgba(244,63,94,0.08) 0%,transparent 50%),
    var(--bg);
  -webkit-font-smoothing:antialiased;
}
```

## 핵심 컴포넌트 (복사해서 사용)

- **뱃지**: 둥근 pill, 색상별(amber/indigo/rose) 변형, 작은 점(dot) + glow.
- **글래스 카드** `.card`: `background:var(--surface); border:1px solid var(--border);
  border-radius:18px;` 색 변형은 좌측 보더/배경 틴트로.
- **버튼** `.btn`: `border-radius:11px; font-weight:700;` 색 변형(rose/amber/emerald/indigo/ghost)은
  `linear-gradient(135deg, rgba(색,0.22), rgba(색,0.08))` + 같은 색 보더. hover에 `translateY(-2px)`.
- **탭** `.tab`: 카드형, 활성 탭은 amber/rose 틴트 + 그림자. (build-recipe의 탭 패턴 참고)
- **토큰 칩** `.token`: 컨텍스트/데이터 조각 표현. `signal`(emerald), `noise`(dim), `amber`,
  `rose` 변형. 등장 시 `@keyframes pop`(scale .6→1).
- **판정 박스** `.verdict`: 결과 메시지. `.ok`(emerald 틴트), `.bad`(rose), `.warn`(amber).
- **메트릭/막대**: 라벨+값(mono) 행, `.barwrap/.barfill`로 비율 바.

세부 CSS는 양이 많으니 `assets/template.html`에 실제로 들어있다 — **거기서 복사**하는 게 가장 빠르다.

## 레이아웃

- **기본 폭은 넓게.** `.wrap{max-width:1500px}` 정도로 화면을 시원하게 쓴다. 좁은 컬럼(≤1000px)에
  가두지 마라 — 녹화·발표 시 양옆이 휑하고 무대가 답답해 보인다. 좌우 padding은 32~36px.
- 좌(무대 `.stage`: SVG/애니메이션) + 우(사이드카드: 버튼·지표·판정)의 `grid2`(1fr 360px) 2단이 기본.
- 무대는 `border-radius:18px`, `overflow:hidden`.
- 모바일(<900px)에선 1단으로.

## 톤

- 글자 적게. 슬라이드가 아니라 *만지는* 화면. 설명은 무대 밑 한 줄(`flow-msg`)과 우측 판정으로.
- 이모지는 핵심 라벨에 한두 개. 과용 금지.
