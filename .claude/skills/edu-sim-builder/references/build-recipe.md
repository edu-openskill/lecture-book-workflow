# 빌드 레시피 — 구조 · 애니메이션 · SVG 패턴

## 파일 구조 (단일 HTML)

```
<head> 메타 + 폰트 CDN + <style>(전체 CSS 인라인)
<body>
  .wrap
    헤더(뱃지 + h1 + 한 줄 sub)
    .tabs (탭 = 개념/예시들)        ← 여러 예시면 탭, 하나면 생략
    각 .panel (data-panel="i")
      .phead(제목) + .pdesc(2~3줄 설명)
      .grid2: [.stage 무대(SVG/애니메이션)] [사이드카드: 버튼·지표·.verdict]
      .hint(아래 한 줄 포인트)
  <script>  탭 전환 + 각 패널의 IIFE(독립 스코프)
```
각 패널 로직은 `(function(){ ... })();`로 **독립 스코프**에 담아 변수 충돌을 막는다.

## 탭 전환 (표준)

```js
tabbar.addEventListener('click',e=>{
  const t=e.target.closest('.tab'); if(!t)return; const i=t.dataset.tab;
  document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('active',x.dataset.tab===i));
  document.querySelectorAll('.panel').forEach(p=>p.classList.toggle('active',p.dataset.panel===i));
});
```

## 버튼 → 데이터 흐름 애니메이션 (핵심 상호작용)

"버튼을 누르면 데이터가 흘러간다"가 이 시뮬레이터들의 정체성. 두 가지 방법:

1. **스태거 등장**: 토큰/요소를 `setTimeout(..., i*120)`으로 하나씩 `insertAdjacentHTML`.
   각 토큰은 `@keyframes pop`(scale·opacity)로 등장. (컨텍스트가 채워지는 느낌)
2. **CSS 트랜지션 폭/위치**: 막대는 `width:0`로 만들고 `requestAnimationFrame(()=>bf.style.width=w+'%')`
   로 늘린다. 선/도형은 좌표를 갱신하며 `transition`으로 부드럽게.

원칙: **고정 좌표계.** 버튼을 눌러도 기준 요소(축·데이터 벡터·노드)는 제자리. *새 요소 하나만*
추가/갱신한다. 장면 전체를 다시 그리거나 회전시키면 사용자가 길을 잃는다.

**⚠ 느낌(vibe) 애니메이션 금지 — 실제 연산을 그려라.** "층을 지나니 화살표가 그냥 커진다"처럼
*시간이 지나서* 변하는 연출은 틀렸다. 변화는 **실제 계산 결과**여야 한다. 예: residual 누적은
`cum.x += S*Δm*cos(Δa)`처럼 **벡터를 실제로 더해** 끝점을 옮기고, 더해진 Δ를 점선으로 보여준다.
다단계 과정(RAG 4단계, 어텐션 내적→소프트맥스→가중합)은 **step 변수 + 버튼**으로 한 단계씩
진행시키고, 진행한 단계를 칩/하이라이트로 표시한다. (검증은 verification.md F절.)

## SVG 벡터 / 정사영(내적) 패턴 — 자주 쓰는 핵심

좌표계: `O`(원점), `S`(길이 배율). y는 화면에서 아래로 증가하므로 **부호 주의**.

```js
const rad=d=>d*Math.PI/180;
const px=(a,m)=>O.x+S*m*Math.cos(rad(a));   // 각도 a(도), 크기 m
const py=(a,m)=>O.y-S*m*Math.sin(rad(a));   // y 뒤집힘 → 빼기
```

- **유사도(코사인) = 내적 = 정사영.** 질문 단위벡터 u=(cos qa, -sin qa)[svg]. 데이터 벡터를
  u에 정사영한 스칼라 = `m*cos(데이터각 - 질문각)`. 양수면 같은 방향(유사), 0이면 직각(무관),
  음수면 반대(비유사).
- **정사영 발(foot)** = `O + (S*sim)*u`. 데이터 끝에서 발까지 **수선(점선)**을 내린다.
- **직각 표시**: 발에서 질문축 방향과 수선 방향으로 작은 L자 polyline.
- 사람은 **질문축을 가로(수평)로** 두고 수직으로 떨어지는 정사영을 가장 직관적으로 읽는다.
  단, 그러려고 데이터 벡터를 회전시키지는 마라(고정 원칙). 트레이드오프는 사용자와 상의.
- 비교를 보여줄 땐 **막대 길이**로. 강조 대상은 형광색(lime) + 글로우(넓고 옅은 선 밑에 깔기) +
  끝 눈금. 나머지는 흐리게.

## softmax → 확률 (할루시네이션 포인트에 유용)

`p_i = exp(s_i/T) / Σ exp(s_j/T)`. **T(온도)** 작을수록 1등에 확률이 쏠린다. 교육 포인트:
*정사영(실제 적합도)이 0.2뿐이어도 softmax는 90% 확신처럼 부풀린다* → 자신만만한 거짓.

## 흔한 실수 (피하기)

- 화살표가 viewBox 밖으로 나감 → 빌드 전에 좌표 계산해 확인(verification.md).
- 라벨끼리 겹침 → 끝점 위치(좌/우, cos 부호)에 따라 anchor·offset을 다르게.
- 한 요소만 과하게 굵음(예: 막대 9px) → 기존 화살표 두께(≈3.4)와 맞춰라.
- 같은 숫자를 그림과 패널에 중복 표기 → 한 곳으로.
