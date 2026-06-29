# 검증 — 그리기 전에, 그리고 전달 전에

시각화는 **숫자가 틀리면 무의미**하다. 빌드 전/후 두 번 검증한다.

## A. 빌드 전 — 좌표·수학 미리 계산 (node)

화면을 코딩하기 전에, 의도한 기하/값이 맞는지 node로 확인한다.

```bash
node -e '
const O={x:300,y:300},S=230,rad=d=>d*Math.PI/180;
const DATA=[["파이썬",58,1.0],["HTTP",104,1.0]];   // [라벨, 각도, 크기]
const Q=[["프로그래밍 언어",40],["브라우저",122],["양자역학",-25]];
const VBX=720,VBY=440;
// 1) 모든 끝점이 viewBox 안에 들어오는가?
DATA.forEach(d=>{const x=O.x+S*d[2]*Math.cos(rad(d[1])),y=O.y-S*d[2]*Math.sin(rad(d[1]));
  console.log(d[0],Math.round(x),Math.round(y), (x>3&&x<VBX-3&&y>3&&y<VBY-3)?"OK":"OUT!");});
// 2) 의도한 승자/유사도가 나오는가?
Q.forEach(q=>{ const s=DATA.map(d=>({l:d[0],sim:d[2]*Math.cos(rad(d[1]-q[1]))}));
  const win=s.reduce((a,b)=>a.sim>b.sim?a:b);
  console.log(q[0],"→",win.l,win.sim.toFixed(2)); });
'
```
- 끝점이 `OUT!`이면 O/S/각도/viewBox를 조정.
- 승자/값이 의도와 다르면 각도를 바꾼다(예: 질문이 데이터에 더 가깝게/멀게).

## B. 빌드 후 — 문법 + 런타임

1. **JS 문법 검사**: `<script>` 본문을 추출해 `node --check`.
   ```bash
   # html에서 마지막 <script> 블록만 뽑아 검사
   python3 - "파일.html" <<'PY'
   import sys; h=open(sys.argv[1],encoding='utf-8').read()
   i=h.rfind('<script>'); j=h.rfind('</script>')
   open('/tmp/s.js','w',encoding='utf-8').write(h[i+8:j])
   PY
   node --check /tmp/s.js && echo "JS OK"
   ```
   (또는 의심되는 IIFE 하나만 /tmp에 떼어내 `node --check`.)

2. **런타임(가능하면 jsdom)**: 탭 전환 + 모든 버튼 클릭에 콘솔 에러 0건인지.
   ```bash
   cd /tmp && npm install jsdom --silent 2>/dev/null
   node -e '
   const {JSDOM}=require("jsdom"); const fs=require("fs");
   const dom=new JSDOM(fs.readFileSync("파일.html","utf8"),{runScripts:"dangerously",pretendToBeVisual:true});
   const d=dom.window.document, errs=[];
   dom.window.addEventListener("error",e=>errs.push(e.message));
   d.querySelectorAll(".tab").forEach(t=>t.dispatchEvent(new dom.window.MouseEvent("click",{bubbles:true})));
   ["btnA","btnB"].forEach(id=>{const el=d.getElementById(id); el&&el.dispatchEvent(new dom.window.MouseEvent("click",{bubbles:true}));});
   setTimeout(()=>{console.log("errors:",errs.length?errs:"NONE");process.exit(0);},1500);
   '
   ```

## C. 큰 파일(약 40KB+) 주의 — 보조 작업창 읽기 오류

샌드박스(bash) 마운트가 **파일을 읽을 때 내용을 잘리거나 뒤섞어** 보여줄 수 있다(stat 크기는
맞는데 cat/grep/python 읽기가 깨짐). **실측상 ~42KB 파일에서도 발생**했으니 **약 40KB 안팎부터
의심**한다(`<script>`/`</script>` rfind가 음수가 나오면 바이트가 뒤섞인 것). 이때:
- **진위 판단은 파일 도구(Read/Grep)를 기준**으로 한다. bash의 wc/grep/tail이 "잘렸다"고 해도
  Read가 멀쩡하면 파일은 멀쩡한 것. (먼저 Read로 끝 `</script></body></html>` 완결 확인.)
- 검증용으로 의심 함수(IIFE)만 **heredoc으로 직접 타이핑**해 `/tmp`의 작은 파일에 적어
  `node --check`/실행한다(스텁 DOM). 마운트 경유 파일(`cp`/`dd` 포함 — 읽는 순간 뒤섞임)로
  검증하지 말 것. cat·dd가 바이트 수는 맞게 세도 내용은 뒤섞일 수 있다.
- 큰 파일을 다시 쓸 때, bash로 **prefix+append**(앞부분 유지 + 꼬리만 덧붙이기)하면 안전.
- 파일 도구 Edit는 정상 동작한다. 마운트가 잘려 보여도 Edit 결과는 보존된다.
- **⚠ 쓰기 잘림(~34KB):** Write 도구가 약 34KB 지점에서 파일을 *말없이* 잘라낼 수 있다(멀티바이트
  한글 중간에서 끊김). 시뮬레이터 HTML은 보통 이 한도를 넘으므로: ① 본문을 두 파일(`p1`,`p2`)로
  나눠 Write → ② bash `cat p1 p2 > 최종.html` 로 합친다(샌드박스 쓰기는 한도 없음). 큰 파일을
  Edit로 부분 수정할 때도 잘림이 날 수 있으니, **국소 수정은 bash의 python `str.replace`(매칭
  개수 1 확인 후 저장)** 로 하는 게 가장 안전하다.

## D. 시각 확인

헤드리스 브라우저가 없으면 스크린샷은 못 찍는다. 대신 좌표·수학을 정량 확인하고, 마지막엔
사용자에게 "브라우저에서 새로고침해 확인해 달라"고 안내한다.

## E. 내용(개념) 검증 — "비유가 사실인가" (코드가 아니라 주장)

가장 비싼 버그는 문법이 아니라 **틀린 개념**이다. 코드가 완벽히 돌아도, 시뮬레이터가 가르치는
내용이 사실과 다르면 오개념을 심는다. **빌드 전(시나리오 단계)** 과 **전달 전**, 두 번 점검한다.

### 방법
1. 시나리오/각 장면에서 **단정하는 문장**만 불릿으로 뽑는다. (예: "LLM은 한 마디 끝나면 까먹는다")
2. 각 불릿에 `✓ 사실 / ✗ 틀림 / 출처` 를 단다. 하나라도 ✗면 그리지 않는다.
3. **비유표**를 만든다: `[게임/일상 사물 | 실제 개념 | 성립 조건 | 깨지는 지점]`.
   조건과 깨지는 지점이 비면 비유가 과일반화된 것 — 보강한다.

### 체크리스트
- [ ] 모든 핵심 주장을 한 줄씩 뽑아 사실 여부를 따졌는가.
- [ ] 흔한 오개념(folk model)을 그대로 그리지 않았는가? (직관적이지만 틀린 설명)
- [ ] 비유의 **경계**가 맞는가 — "언제 성립하고 언제 깨지는가"를 구분했는가. (무조건 일반화 금지)
- [ ] 메커니즘의 **주체**를 바꿔치기하지 않았는가? (예: *모델*이 하는 일 ↔ *앱(하네스)*이 하는 일)
- [ ] 확신이 안 서면 **권위 있는 출처**(1차 문서·논문)로 확인했는가.

### 대표 실패 사례 (실제로 겪음)
- ❌ "LLM은 한 마디 끝나면 사용자를 까먹는다."
  → **틀림.** 같은 대화에선 앱이 앞 내용을 컨텍스트에 다시 담아 건네므로 기억한다. 진짜 백지가
     되는 건 *다른 에이전트*에게 시키거나 *새 세션*(다음 날 다시 켬)일 때다.
  → **교훈:** 무상태(stateless)는 "매 발화 망각"이 아니라 **"호출 사이 미저장 + 앱이 매번 다시
     적재"** 다. 그럴듯한 직관을 그리기 전에 *주체(모델 vs 앱)* 와 *조건(같은 대화 vs 새 세션)* 을
     확인하라.

### 자동화 보조 (선택)
- 시뮬의 단정 문장들을 한 파일로 모아, 별도 검수 패스(서브에이전트/다른 모델)에게 "각 문장이
  사실인가, 흔한 오개념인가"를 채점하게 하면 사람이 놓친 개념 오류를 잡는다. (eval식 내용 검수)

## F. 메커니즘 검증 — "시뮬이 그 연산을 진짜 하는가" (가장 비싼 실패)

E가 *주장이 사실인가*를 본다면, F는 *애니메이션이 주장한 연산을 실제로 수행하는가*를 본다.
둘은 다르다. 설명 텍스트는 맞는데 그림은 **느낌만** 흉내 낸 경우가 가장 위험하다.

### 대표 실패 사례 (실제로 겪음)
- ❌ '층(transformer layer)' 패널: "층을 지나니 화살표가 점점 커진다"는 *연출*만 있고, 실제
  동작(이웃과 **내적**(어텐션) → 결과 Δ를 **벡터 더하기(residual)** 로 누적 → 다음 층)이 전혀
  없었다. 화려하지만 **틀린** 시각화.
  → **교훈:** 코드 전에 실제 연산을 한 줄로 적고, 그 연산의 각 부분이 화면의 *어떤 요소*로
     나타나는지 매핑한다. 매핑이 안 되는 움직임은 빼라.

### 체크리스트
- [ ] 이 패널이 가르치는 연산을 한 줄로 적었는가? (input → 연산 → output)
- [ ] 그 연산의 **각 단계가 화면의 구체적 요소**(선·각도·길이·더해지는 벡터…)로 보이는가?
- [ ] 움직임이 *비유적 느낌*이 아니라 **실제 계산 결과**를 반영하는가? (예: 길이가 커지는 게
      'residual 덧셈'의 결과인가, 그냥 시간이 지나서인가?)
- [ ] 캔버스에 그 연산이 무엇인지 라벨로 드러나는가? (수치·연산명이 하늘에서 안 떨어지게)
- [ ] 표준 도식이 있는 주제라면, 흐름 방향·단계가 표준과 일치하는가?
