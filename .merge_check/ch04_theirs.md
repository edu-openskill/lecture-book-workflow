# 챕터 4. 비동기 MSA - Kafka로 서비스를 분리하다

> 이 챕터의 전체 소스코드는 **https://github.com/metacoding-12-msa/ex03** 에서 확인할 수 있습니다.

:::goal
이번 챕터가 끝나면

- 동기 REST 호출의 한계를 이해하고 비동기 메시지 방식의 장점을 설명할 수 있습니다.
- Kafka의 토픽, 프로듀서, 컨슈머, 컨슈머 그룹 개념을 이해할 수 있습니다.
- Orchestration Saga 패턴을 Kafka로 구현할 수 있습니다.
- order-service의 동기 호출을 Kafka 이벤트 발행으로 교체할 수 있습니다.
- orchestrator가 워크플로우 상태를 추적하고 실패 시 자동 롤백하는 방법을 이해할 수 있습니다.
:::

::::prep
**준비하기**. 실습 시작 전 한 번만 설정

### 1. 소스 코드 클론

```bash [터미널] 레포 클론
git clone https://github.com/metacoding-12-msa/ex03.git
cd ex03
```

### 2. Kafka

이 챕터는 Kafka를 별도로 설치하지 않습니다. Kubernetes 매니페스트(`k8s/kafka/`)로 Minikube 안에 띄우므로, 챕터 3에서 준비한 Docker Desktop과 Minikube만 있으면 됩니다.

### 3. 실습 순서

1. order-service의 REST 호출을 Kafka 이벤트 발행으로 교체
2. product-service · delivery-service에 Kafka Consumer/Producer 추가
3. 새 서비스 **orchestrator**에서 워크플로우 조율 로직 작성
4. K8s에 Kafka + orchestrator 배포
5. 정상 주문 / 품절 롤백 시나리오 검증

:::note
**이번 챕터는 책에서 가장 복잡한 내용을 다룹니다.** 여러 서비스가 동시에 Kafka 메시지를 주고받으며 상태가 바뀝니다. 전체 토픽맵(4.2.3)과 흐름 표(4.3.1~4.3.2)를 먼저 훑어보고 시작하면 길을 잃지 않습니다.
:::
::::

**오픈이**: "선배님, 상품 서비스 껐다 켰더니 주문까지 멈춰요. 서비스 분리한 의미가 없는 것 같아요."

**선배**: "서로 직접 전화를 걸어서 기다려주니까 그래요. 이제 전화를 끊고 메시지를 남기는 방식으로 바꿔 봐요. Kafka라는 녀석이 있어요."

## 4.1 한 서비스의 장애가 전체를 멈추다

챕터 3을 마치면서 이런 질문을 남겼습니다. **"product-service가 잠깐 다운되면 어떻게 되나?"**

답은 단순합니다. order-service도 주문을 처리할 수 없게 됩니다. order-service가 product-service를 직접 HTTP로 호출하기 때문입니다. 하나가 느려지면 다른 하나도 기다립니다. 하나가 멈추면 다른 하나도 멈춥니다.

이것은 MSA의 목표인 **"각 서비스를 독립적으로 배포하고 장애를 격리한다"** 와 정면으로 충돌합니다.

### 4.1.1 카운터 대기 vs 진동벨

카페에서 커피를 주문하는 두 가지 방식으로 비교하겠습니다.

<!-- image-prompt: Minimal black line drawing on white background, split comparison, 4:3 aspect ratio, 800x600px. Minimal text — let the drawing tell the story. Separated by a simple vertical line in the middle, no X mark. Left side, title "동기 (카운터 대기)": barista behind counter making coffee, one customer standing at counter waiting, four or five more customers queued behind in a long line looking bored. All frozen/blocked. Right side, title "비동기 (진동벨)": same cafe counter with barista, but the customer has walked away to a table, sitting with a laptop and a small vibration buzzer on the table. A wavy line from the buzzer indicating it will ring. No speech bubbles, no annotation text, no checklists. Clean lines, no colors. -->
![](assets/CH04/gemini/01_sync-vs-async.png)
*그림 4-1. 동기 vs 비동기 통신*


**카운터 대기 방식 (동기적)**

카운터 앞에 서서 "아메리카노 하나요"라고 주문합니다. 바리스타가 커피를 만드는 동안 카운터 앞에서 기다립니다. 내 커피가 나와야 다음 손님이 주문할 수 있습니다. 바리스타가 원두를 갈다가 머신이 고장 나면? 뒤에 줄 선 손님 전부가 멈춥니다.


**진동벨 방식 (비동기적)**

"아메리카노 하나요"라고 주문하면 진동벨을 받고 자리에 앉습니다. 바리스타는 주문을 순서대로 처리하고, 커피가 완성되면 벨이 울립니다. 나는 기다리는 동안 다른 일을 할 수 있고, 뒤에 줄 선 손님도 바로 주문할 수 있습니다. 머신이 잠깐 멈춰도 주문 목록은 사라지지 않습니다.


MSA에서 동기 통신의 문제는 더 심각합니다. 하나가 느려지면 전체가 느려지는 연쇄 장애가 발생합니다.



## 4.2 Kafka - 메시지를 전달하는 우체국

:::term-box
**Apache Kafka란?** 서비스 사이에 메시지를 안전하게 저장하고 전달하는 분산 메시지 플랫폼입니다. 발행자와 구독자가 동시에 실행 중이지 않아도 메시지가 유실되지 않습니다.
:::

Kafka를 코드로 보기 전, 꼭 알아야 할 세 가지 개념이 있습니다.

### 4.2.1 토픽, 프로듀서, 컨슈머

Kafka의 구조는 우체통과 비슷합니다. 메시지를 보내는 사람이 **프로듀서**, 메시지를 받는 사람이 **컨슈머**, 메시지가 쌓이는 공간이 **토픽**입니다.

:::term-box
**토픽(Topic)이란?** 메시지가 저장되는 이름 붙은 채널입니다. 우체통의 투입구처럼 특정 주제의 메시지를 모아두는 공간입니다.
:::

:::term-box
**프로듀서(Producer)란?** 토픽에 메시지를 보내는(발행하는) 쪽입니다. 우체통에 편지를 넣는 사람에 해당합니다.
:::

:::term-box
**컨슈머(Consumer)란?** 토픽에서 메시지를 읽는(구독하는) 쪽입니다. 우체통에서 편지를 꺼내 읽는 사람에 해당합니다.
:::

<div class="svg-figure">
<svg viewBox="0 0 1080 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Kafka 저장소 구조: 여러 발행자가 토픽(우체통)에 편지(메시지)를 넣고, 여러 구독자가 각자의 토픽에서 편지를 꺼내 읽는다">
  <defs>
    <marker id="c4f2-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="540" y="28" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">Kafka — 이름 붙은 우체통(토픽)이 여러 개 있는 메시지 저장소</text>
  <rect x="20" y="90" width="160" height="70" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="100" y="113" text-anchor="middle" font-size="10" font-weight="700" fill="#475569">PRODUCER A</text>
  <text x="100" y="135" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">발행자</text>
  <rect x="135" y="142" width="30" height="14" rx="1" fill="#fff" stroke="#475569" stroke-width="1"/>
  <path d="M 135 142 L 150 152 L 165 142" fill="none" stroke="#475569" stroke-width="1"/>
  <rect x="20" y="185" width="160" height="70" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="100" y="208" text-anchor="middle" font-size="10" font-weight="700" fill="#475569">PRODUCER B</text>
  <text x="100" y="230" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">발행자</text>
  <rect x="135" y="237" width="30" height="14" rx="1" fill="#fff" stroke="#475569" stroke-width="1"/>
  <path d="M 135 237 L 150 247 L 165 237" fill="none" stroke="#475569" stroke-width="1"/>
  <rect x="20" y="280" width="160" height="70" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="100" y="303" text-anchor="middle" font-size="10" font-weight="700" fill="#475569">PRODUCER C</text>
  <text x="100" y="325" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">발행자</text>
  <rect x="135" y="332" width="30" height="14" rx="1" fill="#fff" stroke="#475569" stroke-width="1"/>
  <path d="M 135 332 L 150 342 L 165 332" fill="none" stroke="#475569" stroke-width="1"/>
  <line x1="180" y1="125" x2="245" y2="155" stroke="#4f46e5" stroke-width="1.4" marker-end="url(#c4f2-i)"/>
  <line x1="180" y1="220" x2="245" y2="225" stroke="#4f46e5" stroke-width="1.4" marker-end="url(#c4f2-i)"/>
  <line x1="180" y1="315" x2="245" y2="295" stroke="#4f46e5" stroke-width="1.4" marker-end="url(#c4f2-i)"/>
  <rect x="240" y="60" width="600" height="320" rx="14" fill="#fff4ed" stroke="#ff7849" stroke-width="2.4"/>
  <text x="540" y="84" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">Kafka 브로커 — 분산 메시지 저장소</text>
  <rect x="270" y="110" width="540" height="60" rx="5" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <rect x="270" y="100" width="540" height="20" rx="5" fill="#ff7849"/>
  <text x="540" y="114" text-anchor="middle" font-size="10" font-weight="700" fill="#fff" font-family="monospace">Topic A</text>
  <rect x="290" y="124" width="50" height="3" rx="1" fill="#7b341e"/>
  <g transform="translate(355 138)">
    <rect x="0" y="0" width="44" height="22" rx="1.5" fill="#fff4ed" stroke="#ff7849" stroke-width="1"/>
    <path d="M 0 0 L 22 11 L 44 0" fill="none" stroke="#ff7849" stroke-width="1"/>
    <rect x="50" y="0" width="44" height="22" rx="1.5" fill="#fff4ed" stroke="#ff7849" stroke-width="1"/>
    <path d="M 50 0 L 72 11 L 94 0" fill="none" stroke="#ff7849" stroke-width="1"/>
    <rect x="100" y="0" width="44" height="22" rx="1.5" fill="#fff4ed" stroke="#ff7849" stroke-width="1"/>
    <path d="M 100 0 L 122 11 L 144 0" fill="none" stroke="#ff7849" stroke-width="1"/>
    <rect x="150" y="0" width="44" height="22" rx="1.5" fill="#fff4ed" stroke="#ff7849" stroke-width="1"/>
    <path d="M 150 0 L 172 11 L 194 0" fill="none" stroke="#ff7849" stroke-width="1"/>
    <rect x="200" y="0" width="44" height="22" rx="1.5" fill="#fff4ed" stroke="#ff7849" stroke-width="1"/>
    <path d="M 200 0 L 222 11 L 244 0" fill="none" stroke="#ff7849" stroke-width="1"/>
    <rect x="250" y="0" width="44" height="22" rx="1.5" fill="#fff4ed" stroke="#ff7849" stroke-width="1"/>
    <path d="M 250 0 L 272 11 L 294 0" fill="none" stroke="#ff7849" stroke-width="1"/>
    <rect x="300" y="0" width="44" height="22" rx="1.5" fill="#fff4ed" stroke="#ff7849" stroke-width="1"/>
    <path d="M 300 0 L 322 11 L 344 0" fill="none" stroke="#ff7849" stroke-width="1"/>
    <rect x="350" y="0" width="44" height="22" rx="1.5" fill="#fff4ed" stroke="#ff7849" stroke-width="1"/>
    <path d="M 350 0 L 372 11 L 394 0" fill="none" stroke="#ff7849" stroke-width="1"/>
  </g>
  <rect x="270" y="200" width="540" height="60" rx="5" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <rect x="270" y="190" width="540" height="20" rx="5" fill="#ff7849"/>
  <text x="540" y="204" text-anchor="middle" font-size="10" font-weight="700" fill="#fff" font-family="monospace">Topic B</text>
  <rect x="290" y="214" width="50" height="3" rx="1" fill="#7b341e"/>
  <g transform="translate(355 228)">
    <rect x="0" y="0" width="44" height="22" rx="1.5" fill="#fff4ed" stroke="#ff7849" stroke-width="1"/>
    <path d="M 0 0 L 22 11 L 44 0" fill="none" stroke="#ff7849" stroke-width="1"/>
    <rect x="50" y="0" width="44" height="22" rx="1.5" fill="#fff4ed" stroke="#ff7849" stroke-width="1"/>
    <path d="M 50 0 L 72 11 L 94 0" fill="none" stroke="#ff7849" stroke-width="1"/>
    <rect x="100" y="0" width="44" height="22" rx="1.5" fill="#fff4ed" stroke="#ff7849" stroke-width="1"/>
    <path d="M 100 0 L 122 11 L 144 0" fill="none" stroke="#ff7849" stroke-width="1"/>
    <rect x="150" y="0" width="44" height="22" rx="1.5" fill="#fff4ed" stroke="#ff7849" stroke-width="1"/>
    <path d="M 150 0 L 172 11 L 194 0" fill="none" stroke="#ff7849" stroke-width="1"/>
    <rect x="200" y="0" width="44" height="22" rx="1.5" fill="#fff4ed" stroke="#ff7849" stroke-width="1"/>
    <path d="M 200 0 L 222 11 L 244 0" fill="none" stroke="#ff7849" stroke-width="1"/>
  </g>
  <rect x="270" y="290" width="540" height="60" rx="5" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <rect x="270" y="280" width="540" height="20" rx="5" fill="#ff7849"/>
  <text x="540" y="294" text-anchor="middle" font-size="10" font-weight="700" fill="#fff" font-family="monospace">Topic C</text>
  <rect x="290" y="304" width="50" height="3" rx="1" fill="#7b341e"/>
  <g transform="translate(355 318)">
    <rect x="0" y="0" width="44" height="22" rx="1.5" fill="#fff4ed" stroke="#ff7849" stroke-width="1"/>
    <path d="M 0 0 L 22 11 L 44 0" fill="none" stroke="#ff7849" stroke-width="1"/>
    <rect x="50" y="0" width="44" height="22" rx="1.5" fill="#fff4ed" stroke="#ff7849" stroke-width="1"/>
    <path d="M 50 0 L 72 11 L 94 0" fill="none" stroke="#ff7849" stroke-width="1"/>
    <rect x="100" y="0" width="44" height="22" rx="1.5" fill="#fff4ed" stroke="#ff7849" stroke-width="1"/>
    <path d="M 100 0 L 122 11 L 144 0" fill="none" stroke="#ff7849" stroke-width="1"/>
  </g>
  <line x1="835" y1="140" x2="900" y2="125" stroke="#4f46e5" stroke-width="1.4" marker-end="url(#c4f2-i)"/>
  <line x1="835" y1="225" x2="900" y2="220" stroke="#4f46e5" stroke-width="1.4" marker-end="url(#c4f2-i)"/>
  <line x1="835" y1="315" x2="900" y2="315" stroke="#4f46e5" stroke-width="1.4" marker-end="url(#c4f2-i)"/>
  <rect x="900" y="90" width="160" height="70" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="980" y="113" text-anchor="middle" font-size="10" font-weight="700" fill="#475569">CONSUMER α</text>
  <text x="980" y="135" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">구독자</text>
  <rect x="1015" y="142" width="30" height="14" rx="1" fill="#fff" stroke="#475569" stroke-width="1"/>
  <path d="M 1015 142 L 1030 152 L 1045 142" fill="none" stroke="#475569" stroke-width="1"/>
  <rect x="900" y="185" width="160" height="70" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="980" y="208" text-anchor="middle" font-size="10" font-weight="700" fill="#475569">CONSUMER β</text>
  <text x="980" y="230" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">구독자</text>
  <rect x="1015" y="237" width="30" height="14" rx="1" fill="#fff" stroke="#475569" stroke-width="1"/>
  <path d="M 1015 237 L 1030 247 L 1045 237" fill="none" stroke="#475569" stroke-width="1"/>
  <rect x="900" y="280" width="160" height="70" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="980" y="303" text-anchor="middle" font-size="10" font-weight="700" fill="#475569">CONSUMER γ</text>
  <text x="980" y="325" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">구독자</text>
  <rect x="1015" y="332" width="30" height="14" rx="1" fill="#fff" stroke="#475569" stroke-width="1"/>
  <path d="M 1015 332 L 1030 342 L 1045 332" fill="none" stroke="#475569" stroke-width="1"/>
</svg>
</div>
*그림 4-2. Kafka - 이름 붙은 우체통(토픽)이 여러 개 있는 메시지 저장소*

Kafka의 중요한 특성은, 컨슈머가 메시지를 읽어도 토픽에서 **삭제되지 않는다**는 점입니다. 보존 기간(기본 7일)이 지나야 삭제됩니다. 컨슈머는 오프셋(자신이 어디까지 읽었는지 기록한 위치)을 기억하기 때문에 재시작 후에도 읽지 않은 메시지부터 이어서 처리할 수 있습니다.

:::note
**RabbitMQ 같은 전통적인 메시지 큐는 컨슈머가 메시지를 읽으면 큐에서 바로 삭제됩니다.** 반면 **Kafka**는 읽어도 메시지가 남아 있습니다. 덕분에 여러 컨슈머가 같은 메시지를 각자의 속도로 읽을 수 있고, 장애 후 재처리도 가능합니다.
:::

### 4.2.2 컨슈머 그룹

product-service를 2대로 늘려서 운영한다고 가정해 보겠습니다. **"재고 1개 차감"** 메시지가 들어왔는데 두 인스턴스가 모두 처리하면 재고가 2개 줄어듭니다. 이런 중복 처리를 방지하기 위해 **컨슈머 그룹**으로 묶습니다. 같은 그룹 안에서는 하나의 메시지가 **한 인스턴스에만** 전달됩니다.


<!-- image-prompt: Minimal black line drawing on white background, diagram, 4:3 aspect ratio, 800x400px. Left: a label "메시지" with a thick arrow pointing right into a rounded rectangle group labeled "컨슈머 그룹 (product-group)" at the top. Inside the group, two rows stacked vertically: top row "인스턴스 A ← 메시지 전달 ✓ (처리 담당)", bottom row "인스턴스 B ← 전달 안 됨 ✗". The arrow from left connects only to 인스턴스 A. Clean lines, no colors. -->
<div class="svg-figure">
<svg viewBox="0 0 1000 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="컨슈머 그룹: 같은 그룹의 두 인스턴스 중 한 곳에만 메시지가 전달됨">
  <defs>
    <marker id="c4f3-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="c4f3-x" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#9ca3af"/></marker>
  </defs>
  <text x="500" y="32" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">컨슈머 그룹 — 메시지는 그룹 안 한 인스턴스에만 전달</text>
  <rect x="40" y="100" width="300" height="120" rx="10" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="190" y="130" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">TOPIC</text>
  <text x="190" y="156" text-anchor="middle" font-size="15" font-weight="700" fill="#7b341e" font-family="JetBrains Mono, monospace">decrease-product-command</text>
  <rect x="155" y="175" width="70" height="30" rx="4" fill="#fff" stroke="#ff7849"/>
  <text x="190" y="195" text-anchor="middle" font-size="11" fill="#7b341e" font-family="JetBrains Mono, monospace">msg</text>
  <line x1="340" y1="160" x2="430" y2="160" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f3-i)"/>
  <text x="385" y="150" text-anchor="middle" font-size="11" font-weight="600" fill="#4f46e5" font-family="JetBrains Mono, monospace">deliver</text>
  <rect x="440" y="60" width="520" height="200" rx="14" fill="#fff" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="6 4"/>
  <text x="700" y="88" text-anchor="middle" font-size="12" font-weight="700" fill="#4f46e5" font-family="JetBrains Mono, monospace">consumer group: product-service</text>
  <rect x="470" y="110" width="210" height="120" rx="10" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="575" y="140" text-anchor="middle" font-size="11" font-weight="700" fill="#4338ca">인스턴스 A</text>
  <text x="575" y="173" text-anchor="middle" font-size="22" font-weight="700" fill="#4338ca">처리 담당</text>
  <text x="575" y="206" text-anchor="middle" font-size="12" fill="#4338ca">메시지 수신 ✓</text>
  <rect x="720" y="110" width="210" height="120" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="5 4"/>
  <text x="825" y="140" text-anchor="middle" font-size="11" font-weight="700" fill="#94a3b8">인스턴스 B</text>
  <text x="825" y="173" text-anchor="middle" font-size="22" font-weight="700" fill="#94a3b8">대기</text>
  <text x="825" y="206" text-anchor="middle" font-size="12" fill="#94a3b8">전달 안 됨 ✗</text>
</svg>
</div>
*그림 4-3. 컨슈머 그룹*


### 4.2.3 이번 챕터에서 사용하는 토픽 맵

이번 챕터에서 사용하는 Kafka 토픽 전체를 먼저 봅니다. 처음에는 낯설어 보이지만, 구현 과정에서 하나씩 다루게 됩니다.

총 8개의 토픽을 사용합니다. `command`가 붙은 토픽은 orchestrator가 각 서비스에 내리는 명령입니다. `command`가 없는 토픽은 각 서비스가 처리 결과를 orchestrator에 보고하는 이벤트입니다. 표는 위 5개(정상 주문 흐름)와 아래 3개(롤백 흐름)로 나뉩니다.

| 토픽 | 발행 | 구독 | 목적 |
|---|---|---|---|
| `order-created` | order-service | orchestrator | 새 주문 발생 |
| `decrease-product-command` | orchestrator | product-service | 재고 감소 명령 |
| `product-decreased` | product-service | orchestrator | 재고 감소 결과 |
| `create-delivery-command` | orchestrator | delivery-service | 배달 생성 명령 |
| `delivery-created` | delivery-service | orchestrator | 배달 생성 결과 |
| `complete-order-command` | orchestrator | order-service | 주문 완료 명령 |
| `cancel-order-command` | orchestrator | order-service | 주문 취소 명령 (롤백) |
| `increase-product-command` | orchestrator | product-service | 재고 복구 명령 (롤백) |

:::note
**이번 챕터에서 배달은 한 번 만들어지면 취소되지 않습니다.** 주문이 롤백되어도 배달 자체는 그대로 PENDING으로 남고, 배달 라이프사이클의 의미는 챕터 5에서 정식으로 다루겠습니다.
:::

**오픈이**: "메시지 방식으로 바꾸니까, 전체 흐름을 누가 관리해야 할지 모르겠어요."

**선배**: "오케스트레이터를 만드는 거예요. 지휘자가 전체 악보를 보고 순서를 정하는 것처럼, 각 서비스는 자기 일만 하고 결과만 보고하게 해요."

## 4.3 Orchestration Saga - 지휘자가 흐름을 조율하다

챕터 2에서는 주문 서비스가 다른 서비스를 직접 호출하고 직접 보상했습니다. 실패가 발생하면 주문 row 자체가 트랜잭션 롤백으로 사라져, "어떤 주문이 왜 실패했는지" 이력조차 남지 않았습니다. 이제 중앙에 지휘자를 두는 방식, **Orchestration Saga**로 넘어갑니다. 워크플로우 상태를 한 곳에서 추적하므로 실패 시 정확한 롤백이 가능합니다. 주문도 명시적으로 CANCELLED 상태로 남아 실패 이력까지 보존됩니다.

**지휘자(orchestrator)** 가 전체 흐름을 중앙에서 관리합니다. 각 서비스는 명령을 받아 처리하고 결과를 보고할 뿐, 다음 단계가 무엇인지 알 필요가 없습니다. 지휘자만 전체 악보를 알고 있습니다.
<!-- image-prompt: Clean black line drawing on white background, simplified orchestra illustration, 4:3 aspect ratio, 800x600px. No stage, no curtains, no background. Center: a conductor on a small podium holding a baton and a score labeled "SAGA", drawn in a clean cartoon style (not stick figures — simple but with body proportions, hair, clothing outlines). Three musicians sitting around the conductor with recognizable instruments and music stands labeled "ORDER", "PRODUCT", "DELIVERY". Blue curved arrows from conductor to each musician labeled "command". Green curved arrows from each musician back labeled "result". Simple cartoon style like a textbook illustration — more detailed than stick figures but less detailed than realistic. No shading, no colors except blue and green arrows. -->
![](assets/CH04/gemini/04_orchestra.png)
*그림 4-4. Orchestration Saga 구조*

**참고: Choreography Saga - 또 다른 Saga 구현 방식**

이 책에서는 다루지 않지만, Saga 패턴에는 **Choreography**라는 또 다른 방식이 있습니다. 중앙 지휘자 없이 각 서비스가 이벤트를 발행·구독하면서 다음 단계를 스스로 진행합니다.

<div class="svg-figure">
<svg viewBox="0 0 1080 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Choreography Saga 이벤트 체인: 각 서비스가 이벤트를 발행하면 다음 서비스가 구독해 자신의 일을 진행">
  <defs>
    <marker id="c4-chor-o" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <text x="540" y="28" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Choreography Saga — 서비스가 이벤트를 발행하면 다음 서비스가 구독</text>
  <rect x="40" y="80" width="200" height="60" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="140" y="118" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">order-service</text>
  <line x1="240" y1="110" x2="418" y2="110" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4-chor-o)"/>
  <text x="329" y="100" text-anchor="middle" font-size="12" font-weight="600" fill="#c2410c" font-family="JetBrains Mono, monospace">order-created</text>
  <rect x="420" y="80" width="220" height="60" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="530" y="118" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">product-service</text>
  <line x1="640" y1="110" x2="818" y2="110" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4-chor-o)"/>
  <text x="729" y="100" text-anchor="middle" font-size="12" font-weight="600" fill="#c2410c" font-family="JetBrains Mono, monospace">product-decreased</text>
  <rect x="820" y="80" width="220" height="60" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="930" y="118" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">delivery-service</text>
  <text x="540" y="180" text-anchor="middle" font-size="12" fill="#6b7280" font-style="italic">각 서비스는 다음 단계가 누구인지 모름 · 이벤트만 발행</text>
</svg>
</div>
*그림 4-5. Choreography Saga 이벤트 체인 - 각 서비스가 이벤트를 발행하면 다음 서비스가 구독*

각 서비스는 **다음 단계가 누구인지 모릅니다**. 이벤트만 던지고, 구독하는 쪽이 알아서 일을 이어갑니다. 단순한 흐름에선 가볍지만, 단계가 늘어나거나 보상이 복잡해질수록 전체 워크플로우가 여러 서비스에 흩어져 추적이 어렵습니다. 그래서 이 책은 상태를 한 곳(orchestrator)에서 추적할 수 있는 Orchestration을 선택했습니다.

### 4.3.1 주문 요청 성공 흐름

주문이 정상적으로 처리되는 흐름입니다. 클라이언트가 주문을 요청하면, orchestrator가 재고 감소 → 배달 생성 → 주문 완료 순서로 각 서비스에 명령을 보냅니다. 모든 단계가 성공하면 주문 상태가 COMPLETED로 바뀝니다.

<div class="svg-figure">
<svg viewBox="0 0 1080 460" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="주문 성공 시퀀스: Orchestrator가 Order, Product, Delivery에 차례로 command와 event를 주고받음">
  <defs>
    <marker id="c4f5-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="c4f5-o" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <text x="540" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">주문 성공 흐름 — Orchestration Saga</text>
  <rect x="40" y="60" width="180" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="130" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Order</text>
  <rect x="280" y="60" width="200" height="50" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="380" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#7b341e">Orchestrator</text>
  <rect x="560" y="60" width="180" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="650" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Product</text>
  <rect x="830" y="60" width="180" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="920" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Delivery</text>
  <line x1="130" y1="110" x2="130" y2="430" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="380" y1="110" x2="380" y2="430" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="650" y1="110" x2="650" y2="430" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="920" y1="110" x2="920" y2="430" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="130" y1="150" x2="378" y2="150" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f5-o)"/>
  <text x="254" y="142" text-anchor="middle" font-size="13" font-weight="600" fill="#c2410c" font-family="JetBrains Mono, monospace">① order-created 발행</text>
  <line x1="380" y1="200" x2="558" y2="200" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f5-i)"/>
  <text x="469" y="192" text-anchor="middle" font-size="13" font-weight="600" fill="#4f46e5" font-family="JetBrains Mono, monospace">② decrease-product-command</text>
  <line x1="650" y1="250" x2="382" y2="250" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f5-o)"/>
  <text x="516" y="242" text-anchor="middle" font-size="13" font-weight="600" fill="#c2410c" font-family="JetBrains Mono, monospace">③ product-decreased</text>
  <line x1="380" y1="300" x2="828" y2="300" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f5-i)"/>
  <text x="604" y="292" text-anchor="middle" font-size="13" font-weight="600" fill="#4f46e5" font-family="JetBrains Mono, monospace">④ create-delivery-command</text>
  <line x1="920" y1="350" x2="382" y2="350" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f5-o)"/>
  <text x="651" y="342" text-anchor="middle" font-size="13" font-weight="600" fill="#c2410c" font-family="JetBrains Mono, monospace">⑤ delivery-created</text>
  <line x1="380" y1="400" x2="132" y2="400" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f5-i)"/>
  <text x="256" y="392" text-anchor="middle" font-size="13" font-weight="600" fill="#4f46e5" font-family="JetBrains Mono, monospace">⑥ complete-order-command</text>
  <text x="540" y="445" text-anchor="middle" font-size="13" fill="#6b7280" font-style="italic">각 메시지는 Kafka 토픽을 거쳐 전달 · 인디고: command, 오렌지 점선: event</text>
</svg>
</div>
*그림 4-6. 주문 성공 흐름 (Orchestration Saga)*

| 단계 | 발행 | 토픽 | 수신 | 처리 |
|---|---|---|---|---|
| 1 | 클라이언트 | `/api/orders` | order | 주문 생성 요청(PENDING) |
| 2 | order | `order-created` | orchestrator | 주문 생성 확인 |
| 3 | orchestrator | `decrease-product-command` | product | 재고 감소 명령|
| 4 | product | `product-decreased` | orchestrator | 감소 완료 확인 |
| 5 | orchestrator | `create-delivery-command` | delivery | 배달 생성 명령 |
| 6 | delivery | `delivery-created` | orchestrator | 생성 완료 확인 |
| 7 | orchestrator | `complete-order-command` | order | 주문 생성 완료(COMPLETED) |

### 4.3.2 주문 요청 실패 흐름 (롤백)

중간에 실패가 발생하면 orchestrator가 이미 처리된 단계를 역순으로 되돌립니다. 핵심은 **"이미 처리된 것만 롤백"** 한다는 점입니다.

<div class="svg-figure">
<svg viewBox="0 0 1080 420" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="주문 실패 시 롤백 시퀀스: 배달 생성 실패 후 재고 복구·주문 취소 보상">
  <defs>
    <marker id="c4f6-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="c4f6-o" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <text x="540" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">주문 실패 시 롤백 흐름 — 배달 생성 실패 예시</text>
  <rect x="40" y="60" width="180" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="130" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Order</text>
  <rect x="280" y="60" width="200" height="50" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="380" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#7b341e">Orchestrator</text>
  <rect x="560" y="60" width="180" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="650" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Product</text>
  <rect x="830" y="60" width="180" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="920" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Delivery</text>
  <line x1="130" y1="110" x2="130" y2="390" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="380" y1="110" x2="380" y2="390" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="650" y1="110" x2="650" y2="390" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="920" y1="110" x2="920" y2="390" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="650" y1="150" x2="382" y2="150" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f6-o)"/>
  <text x="516" y="142" text-anchor="middle" font-size="13" font-weight="600" fill="#c2410c" font-family="JetBrains Mono, monospace">① product-decreased {success}</text>
  <line x1="920" y1="210" x2="382" y2="210" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f6-o)"/>
  <text x="651" y="202" text-anchor="middle" font-size="13" font-weight="600" fill="#c2410c" font-family="JetBrains Mono, monospace">② delivery-created {success: false}</text>
  <line x1="380" y1="270" x2="558" y2="270" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f6-i)"/>
  <text x="469" y="262" text-anchor="middle" font-size="13" font-weight="600" fill="#4f46e5" font-family="JetBrains Mono, monospace">③ increase-product-command (보상)</text>
  <line x1="380" y1="335" x2="132" y2="335" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f6-i)"/>
  <text x="256" y="327" text-anchor="middle" font-size="13" font-weight="600" fill="#4f46e5" font-family="JetBrains Mono, monospace">④ cancel-order-command → CANCELLED</text>
  <text x="540" y="405" text-anchor="middle" font-size="13" fill="#6b7280" font-style="italic">실패 감지 후 Orchestrator가 자동으로 보상 명령을 역순으로 발행</text>
</svg>
</div>
*그림 4-7. 주문 실패 시 롤백 흐름*

**재고 감소 실패 시**

재고가 부족하면 product-service가 실패를 보고합니다. 차감 자체가 실패했으니 복구할 재고가 없습니다. 주문만 취소합니다.

| 발행 | 토픽 | 수신 | 처리 |
|---|---|---|---|
| product | `product-decreased {success: false}` | orchestrator | 실패 감지 |
| orchestrator | `cancel-order-command` | order | 주문 취소 명령 |

**배달 생성 실패 시**

이 단계에서는 이미 재고가 감소된 상태입니다. 재고 복구와 주문 취소를 함께 합니다.

| 발행 | 토픽 | 수신 | 처리 |
|---|---|---|---|
| delivery | `delivery-created {success: false}` | orchestrator | 실패 감지 |
| orchestrator | `increase-product-command` | product | 차감된 재고 복구 |
| orchestrator | `cancel-order-command` | order | 주문 취소 명령 |

**선배**: "설계는 끝났어요. 이제 직접 짜 봐요. order-service부터 REST 호출을 걷어내고 Kafka 이벤트로 바꿔요."

## 4.4 order-service - 동기 호출 제거, 이벤트 발행

챕터 2·3에서 order-service는 product-service와 delivery-service를 직접 REST로 호출했습니다. 이번 챕터에서는 이 호출을 모두 제거하고 Kafka 이벤트 발행으로 교체합니다.

### 4.4.1 패키지 구조

```text order-service/ 패키지 구조
order-service/src/main/
├── resources/
│   └── application-prod.properties      ← [참고] Kafka 설정 추가
└── java/.../
    ├── adapter/
    │   ├── message/
    │   │   ├── OrderCreatedEvent.java    ← [참고] 주문 생성 이벤트 DTO
    │   │   ├── CompleteOrderCommand.java ← [참고] 완료 명령 수신 DTO
    │   │   └── CancelOrderCommand.java   ← [참고] 취소 명령 수신 DTO
    │   ├── producer/
    │   │   └── OrderEventProducer.java   ← [작성] order-created 발행
    │   └── consumer/
    │       └── OrderCommandConsumer.java ← [작성] complete/cancel 명령 수신
    ├── usecase/
    │   ├── CreateOrderUseCase.java       ← [참고] 챕터 3과 동일
    │   ├── GetOrderUseCase.java          ← [참고] 챕터 3과 동일
    │   └── OrderService.java             ← [작성] createOrder 수정 (Kafka 발행으로 교체)
    └── web/
        └── OrderController.java          ← [참고] PUT(취소) 엔드포인트 제거. POST·GET만
```

:::note
**REST로 주문을 취소하는 엔드포인트는 사라집니다.** 주문 취소는 orchestrator가 발행한 `cancel-order-command`를 OrderCommandConsumer가 받아 처리합니다.
:::

### 4.4.2 의존성 추가

`spring-boot-starter-kafka` 한 줄을 추가합니다.

챕터 3 `build.gradle` 의존성에 `spring-boot-starter-kafka`를 추가합니다.

### 4.4.3 Kafka 설정

`application-dev.properties`와 `application-prod.properties` 모두에 Kafka 설정을 추가합니다. Kafka 주소는 환경변수로 주입받습니다.

:::note
**`group-id`는 컨슈머 그룹 이름입니다.** 같은 그룹끼리는 메시지를 나눠 받고, 다른 그룹이면 같은 메시지를 각각 받습니다.
:::

`application-prod.properties`에 Kafka 설정 두 줄을 추가합니다.

| 키 | 값 | 역할 |
|---|---|---|
| `spring.kafka.bootstrap-servers` | `${SPRING_KAFKA_BOOTSTRAP_SERVERS:localhost:9092}` | Kafka 브로커 주소. K8s에서 환경변수로 주입, 기본값 `localhost:9092` |
| `spring.kafka.consumer.group-id` | `order-service` | 이 서비스의 컨슈머 그룹 이름 |

dev와 prod의 Kafka 설정은 동일합니다.

### 4.4.4 KafkaConfig : JSON 메시지 변환

Kafka는 메시지를 바이트로 주고받기 때문에 Java 객체를 그대로 보낼 수 없습니다. 택배를 보내기 전에 짐을 박스에 포장하듯, 객체를 JSON 문자열로 변환(직렬화)했다가 받는 쪽에서 다시 객체로 되돌립니다. `JacksonJsonMessageConverter` 빈이 이 변환을 자동으로 처리합니다. 이 설정은 모든 Kafka 사용 서비스(order, product, delivery, orchestrator)에 동일하게 추가합니다.

```java core/config/KafkaConfig.java. JSON 메시지 변환 빈
@Configuration
public class KafkaConfig {

    @Bean
    public RecordMessageConverter recordMessageConverter() {
        return new JacksonJsonMessageConverter();
    }
}
```

### 4.4.5 이벤트 DTO

Kafka 메시지로 전송할 데이터를 DTO로 정의합니다. 이번 챕터에서 쓰는 모든 DTO는 `record`로 단순하게 정의되며, 8개 토픽 전체 DTO 목록은 다음 절 4.5.2의 표에서 한 번에 정리합니다.

### 4.4.6 KafkaTemplate : 메시지 발행

이벤트를 Kafka 토픽으로 발행하는 프로듀서입니다. `KafkaTemplate`이 직렬화와 전송을 처리합니다.


`adapter/producer/OrderEventProducer.java`를 열고 아래 코드를 작성합니다.

```java [실습 1] adapter/producer/OrderEventProducer.java. order-created 발행
@Component
@RequiredArgsConstructor
public class OrderEventProducer {
    private final KafkaTemplate<String, Object> kafkaTemplate;

    // 주문 생성 이벤트 발행
    public void publishOrderCreated(OrderCreatedEvent event) {
        kafkaTemplate.send("order-created", event);
    }
}
```

이번 챕터에서 order-service가 직접 발행하는 이벤트는 `order-created` 하나입니다. 주문 취소는 orchestrator가 결정해서 `cancel-order-command`를 보내고, order-service는 그 명령을 받아 상태만 바꿉니다.

### 4.4.7 OrderService 변경 : 핵심 차이

이전 챕터와 가장 크게 달라진 점은 두 가지입니다. 동기 호출이 Kafka 이벤트 발행으로 바뀌었고, 응답은 즉시 PENDING 상태로 돌아갑니다.

사용자는 PENDING 응답만 받고, 실제 처리는 백그라운드에서 진행됩니다. 그렇다면 처리 결과(COMPLETED 또는 CANCELLED)는 사용자에게 어떻게 알려야 할까요? 이 숙제는 챕터 5에서 WebSocket으로 풀어냅니다.
아래 createOrder 메서드를 구현합니다.

`usecase/OrderService.java`를 열고 아래 메서드를 작성합니다.

```java [실습 2] usecase/OrderService.java. createOrder - Kafka 이벤트 발행으로 교체
@Override
@Transactional
public OrderResponse createOrder(int userId, int productId, int quantity, Long price, String address) {
    // 1. 주문 생성 (PENDING 상태)
    Order createdOrder = orderRepository.save(Order.create(userId, productId, quantity, price));

    // 2. Kafka로 주문 생성 이벤트 발행 — 수정: REST 직접 호출 → Kafka 이벤트 발행
    orderEventProducer.publishOrderCreated(
            new OrderCreatedEvent(createdOrder.getId(), userId, productId, quantity, price, address)
    );

    return OrderResponse.from(createdOrder);
}
```

챕터 02·03에서 보았던 try-catch 보상 트랜잭션이 사라졌습니다. order-service가 더 이상 product-service·delivery-service를 직접 호출하지 않으므로, 실패도 직접 처리하지 않습니다. orchestrator가 Kafka 메시지로 흐름을 조율하고, 실패 시 order-service에는 `cancel-order-command`만 도착합니다.

OrderService에는 `createOrder` 외에 `completeOrder(int orderId)`와 `cancelOrder(int orderId)` 두 메서드가 함께 존재합니다. 두 메서드 모두 주문 상태만 변경(`complete()`·`cancel()`)하고 즉시 반환합니다. 다음 절의 `OrderCommandConsumer`가 orchestrator의 명령을 받아 이 두 메서드를 호출합니다.

### 4.4.8 @KafkaListener : complete/cancel 명령 처리

orchestrator가 최종 결정을 내리면 Kafka로 완료(`complete-order-command`) 또는 취소(`cancel-order-command`) 명령을 발행합니다. order-service는 이 명령을 수신하여 주문 상태를 COMPLETED 또는 CANCELLED로 변경합니다.

`adapter/consumer/OrderCommandConsumer.java`를 열고 아래 코드를 작성합니다.

```java [실습 3] adapter/consumer/OrderCommandConsumer.java. complete/cancel 명령 수신
@Component
@RequiredArgsConstructor
public class OrderCommandConsumer {

    private final OrderService orderService;

    // 주문 완료 명령 수신
    @KafkaListener(topics = "complete-order-command", groupId = "order-service")
    public void completeOrderCommand(CompleteOrderCommand command) {
        orderService.completeOrder(command.orderId());
    }

    // 주문 취소 명령 수신
    @KafkaListener(topics = "cancel-order-command", groupId = "order-service")
    public void cancelOrderCommand(CancelOrderCommand command) {
        orderService.cancelOrder(command.orderId());
    }
}
```

`CompleteOrderCommand`, `CancelOrderCommand`는 `record`로 선언되어 있어 필드 접근자가 `command.orderId()`처럼 메서드명과 같습니다.


## 4.5 product-service · delivery-service - Kafka Consumer/Producer 추가

product-service는 재고 감소·복구 명령을 Kafka로만 받고, 결과를 Kafka로 발행합니다. 챕터 03까지 있던 PUT 엔드포인트(`/api/products/{id}/decrease`, `/increase`)는 제거되고, 컨트롤러에는 GET 조회 엔드포인트만 남습니다. delivery-service도 마찬가지로 배달 생성은 Kafka로만 받고, 컨트롤러에는 GET 엔드포인트만 남습니다.

### 4.5.1 패키지 구조

```text product-service/adapter/ 패키지 구조
adapter/
├── consumer/
│   └── ProductCommandConsumer.java     # [참고] @KafkaListener (decrease/increase 명령 수신)
├── producer/
│   └── ProductEventProducer.java       # [참고] KafkaTemplate 발행
└── message/
    ├── DecreaseProductCommand.java     # [참고] 수신 DTO (재고 감소 명령)
    ├── IncreaseProductCommand.java     # [참고] 수신 DTO (재고 복구 명령)
    └── ProductDecreasedEvent.java      # [참고] 발행 DTO (재고 감소 결과)
```

delivery-service의 어댑터도 같은 모양입니다. `consumer/DeliveryCommandConsumer`가 `create-delivery-command`를 받고, `producer/DeliveryEventProducer`가 `delivery-created` 이벤트를 발행합니다. 이번 챕터에서 배달 취소 흐름은 다루지 않으므로 `cancel-delivery-command` 컨슈머나 `Delivery.cancel()` 메서드는 만들지 않습니다.

### 4.5.2 메시지 DTO 정의

Kafka로 전송되는 메시지는 Java 객체를 JSON으로 직렬화한 것입니다. 각 서비스는 자신이 발행하거나 수신하는 메시지에 해당하는 DTO 클래스를 가지고 있습니다. 이번 챕터에서 사용하는 DTO는 8개 토픽에 대응하는 8개입니다. 모두 `record`로 정의되어 있습니다.

| 토픽 | DTO 클래스 | 주요 필드 |
|---|---|---|
| `order-created` | OrderCreatedEvent | orderId, userId, productId, quantity, price, address |
| `decrease-product-command` | DecreaseProductCommand | orderId, productId, quantity, price |
| `increase-product-command` | IncreaseProductCommand | orderId, productId, quantity, price |
| `product-decreased` | ProductDecreasedEvent | orderId, productId, quantity, success |
| `create-delivery-command`| CreateDeliveryCommand | orderId, address |
| `delivery-created` | DeliveryCreatedEvent | orderId, deliveryId, success |
| `complete-order-command` | CompleteOrderCommand | orderId |
| `cancel-order-command` | CancelOrderCommand | orderId |


product-service와 delivery-service의 Consumer/Producer는 order-service와 동일한 패턴을 따릅니다.


## 4.6 orchestrator - 워크플로우 조율 서비스 구현

orchestrator는 이번 챕터에서 **새로 추가되는 서비스**입니다. REST API는 없고, Kafka 이벤트만 처리합니다. order, product, delivery 서비스의 Kafka 흐름을 중앙에서 조율하는 지휘자입니다.

지휘자가 손에 든 것은 두 가지뿐입니다. 악보와 신호입니다. 악보는 전체 흐름을 기록한 `WorkflowState`이고, 신호는 각 서비스에 보내는 Kafka 메시지입니다. 아래 패키지 구조도 이 두 가지에 맞춰 `message/`와 `handler/`로 나뉩니다.


### 4.6.1 패키지 구조

```text orchestrator/ 패키지 구조
orchestrator/src/main/java/.../
├── message/
│   ├── OrderCreatedEvent.java               ← [참고] order-service에서 수신
│   ├── DecreaseProductCommand.java          ← [참고] product-service에 발행
│   ├── IncreaseProductCommand.java          ← [참고] product-service에 발행 (롤백)
│   ├── ProductDecreasedEvent.java           ← [참고] product-service에서 수신
│   ├── CreateDeliveryCommand.java           ← [참고] delivery-service에 발행
│   ├── DeliveryCreatedEvent.java            ← [참고] delivery-service에서 수신
│   ├── CompleteOrderCommand.java            ← [참고] order-service에 발행
│   └── CancelOrderCommand.java              ← [참고] order-service에 발행 (롤백)
└── handler/
    └── OrderOrchestrator.java               ← [작성] 전체 워크플로우 조율
```

### 4.6.2 의존성

orchestrator는 새 서비스라 `build.gradle` 의존성에 `spring-boot-starter`와 `spring-boot-starter-kafka` 두 개를 추가합니다.

### 4.6.3 OrderOrchestrator

OrderOrchestrator는 세 단계로 동작합니다.

1. **orderCreated** --- 주문 생성 이벤트를 받아 재고 감소 명령을 발행합니다.
2. **productDecreased** --- 재고 감소 결과를 받아, 성공이면 배달 생성 명령을, 실패면 주문 취소 명령을 발행합니다.
3. **deliveryCreated** --- 배달 생성 결과를 받아, 성공이면 주문 완료 명령을, 실패면 재고 복구 + 주문 취소 명령을 발행합니다.

각 단계를 살펴보기 전에, 진행 상태를 보관할 자료구조부터 정의합니다. orchestrator는 주문 한 건의 진행 상태를 **메모리**에 보관해야 합니다. 배달 생성이 실패했을 때 차감된 재고를 되돌리려면, 어떤 상품을 얼마에 얼마큼 차감했는지 알고 있어야 하기 때문입니다.

:::term-box
**WorkflowState란?** orchestrator가 주문 한 건의 진행 상태를 추적하기 위해 사용하는 내부 객체입니다. 주문 ID, 배달 주소, 그리고 차감 대상 상품 정보(productId, quantity, price)를 보관합니다.
:::

`handler/OrderOrchestrator.java`를 열고 클래스 골격과 WorkflowState 내부 클래스를 함께 작성합니다.

```java [실습 4] handler/OrderOrchestrator.java. 클래스 골격 + WorkflowState
@Component
@RequiredArgsConstructor
public class OrderOrchestrator {
    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final Map<Integer, WorkflowState> states = new ConcurrentHashMap<>();  // Kafka 리스너가 멀티스레드로 동작하므로 동시성 보장 필요

    // 아래 1~3단계 메서드를 추가

    @Data
    private static class WorkflowState {
        private final int orderId;
        private final String address;
        private final int productId;
        private final int quantity;
        private final Long price;
    }
}
```

`WorkflowState`는 `ConcurrentHashMap`에 저장되므로 orchestrator Pod가 재시작되면 진행 중인 워크플로우는 소멸합니다. 실무에서는 DB나 Redis에 상태를 저장합니다. 단일 상품 가정 덕분에 상태도 단순해서, 차감한 정보 그대로 들고 있다가 롤백 시점에 IncreaseProductCommand로 돌려보내면 됩니다.

### 4.6.4 1단계 - 주문 생성 이벤트 수신 (orderCreated)

<div class="svg-figure">
<svg viewBox="0 0 880 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="1단계 시퀀스: order-created 수신 후 WorkflowState 생성, decrease-product-command 발행">
  <defs>
    <marker id="c4f7-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="c4f7-o" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <text x="440" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">1단계 — 주문 생성 이벤트 수신</text>
  <rect x="60" y="60" width="180" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="150" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Order</text>
  <rect x="330" y="60" width="200" height="50" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="430" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#7b341e">Orchestrator</text>
  <rect x="620" y="60" width="180" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="710" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Product</text>
  <line x1="150" y1="110" x2="150" y2="290" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="430" y1="110" x2="430" y2="290" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="710" y1="110" x2="710" y2="290" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="150" y1="150" x2="428" y2="150" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f7-o)"/>
  <text x="289" y="142" text-anchor="middle" font-size="13" font-weight="600" fill="#c2410c" font-family="JetBrains Mono, monospace">① order-created 발행</text>
  <path d="M430 200 L490 200 L490 218 L432 218" fill="none" stroke="#7b341e" stroke-width="1.6" marker-end="url(#c4f7-o)"/>
  <text x="500" y="213" text-anchor="start" font-size="13" font-weight="600" fill="#7b341e">② WorkflowState 생성</text>
  <line x1="430" y1="265" x2="708" y2="265" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f7-i)"/>
  <text x="569" y="257" text-anchor="middle" font-size="13" font-weight="600" fill="#4f46e5" font-family="JetBrains Mono, monospace">③ decrease-product-command</text>
</svg>
</div>
*그림 4-8. 1단계 - 주문 생성 이벤트 수신*

`handler/OrderOrchestrator.java`에 1단계 리스너를 추가합니다.

```java [실습 5] handler/OrderOrchestrator.java. 1단계 - orderCreated
@KafkaListener(topics = "order-created", groupId = "orchestrator")
public void orderCreated(OrderCreatedEvent event) {
    int orderId = event.orderId();

    // 주문별 워크플로우 상태 생성
    states.put(orderId, new WorkflowState(
            orderId, event.address(),
            event.productId(), event.quantity(), event.price()
    ));

    // 재고 감소 명령 발행
    kafkaTemplate.send(
            "decrease-product-command",
            String.valueOf(orderId),
            new DecreaseProductCommand(orderId, event.productId(), event.quantity(), event.price())
    );
}
```

orchestrator가 주문 생성(`order-created`) 이벤트를 받으면 주문 ID별로 `WorkflowState`를 생성하고, 재고 감소 명령(`decrease-product-command`)을 발행합니다.

### 4.6.5 2단계 - 재고 차감 결과 수신 (productDecreased)

<div class="svg-figure">
<svg viewBox="0 0 1080 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="2단계 시퀀스: product-decreased 결과에 따라 성공이면 배달 생성, 실패면 주문 취소">
  <defs>
    <marker id="c4f8-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="c4f8-o" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <text x="540" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">2단계 — 재고 차감 결과 수신</text>
  <rect x="40" y="60" width="180" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="130" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Product</text>
  <rect x="290" y="60" width="200" height="50" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="390" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#7b341e">Orchestrator</text>
  <rect x="570" y="60" width="180" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="660" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Delivery</text>
  <rect x="820" y="60" width="180" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="910" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Order</text>
  <line x1="130" y1="110" x2="130" y2="310" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="390" y1="110" x2="390" y2="310" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="660" y1="110" x2="660" y2="310" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="910" y1="110" x2="910" y2="310" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="130" y1="150" x2="388" y2="150" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f8-o)"/>
  <text x="259" y="142" text-anchor="middle" font-size="13" font-weight="600" fill="#c2410c" font-family="JetBrains Mono, monospace">① product-decreased {success}</text>
  <line x1="390" y1="215" x2="568" y2="215" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f8-i)"/>
  <text x="479" y="207" text-anchor="middle" font-size="13" font-weight="600" fill="#4f46e5" font-family="JetBrains Mono, monospace">②a 성공 → create-delivery-command</text>
  <line x1="390" y1="280" x2="818" y2="280" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f8-o)"/>
  <text x="604" y="272" text-anchor="middle" font-size="13" font-weight="600" fill="#c2410c" font-family="JetBrains Mono, monospace">②b 실패 → cancel-order-command (재고 복구 불필요)</text>
</svg>
</div>
*그림 4-9. 2단계 - 재고 차감 결과 수신*

`handler/OrderOrchestrator.java`에 2단계 리스너를 추가합니다.

```java [실습 6] handler/OrderOrchestrator.java. 2단계 - productDecreased
@KafkaListener(topics = "product-decreased", groupId = "orchestrator")
public void productDecreased(ProductDecreasedEvent event) {
    int orderId = event.orderId();
    WorkflowState state = states.get(orderId);
    if (state == null) return;

    // 실패: 차감 자체가 실패했으므로 복구할 재고가 없음. 주문만 취소
    if (!event.success()) {
        kafkaTemplate.send(
                "cancel-order-command",
                String.valueOf(orderId),
                new CancelOrderCommand(orderId)
        );
        states.remove(orderId);
        return;
    }

    // 성공: 배달 생성 명령 발행
    kafkaTemplate.send(
            "create-delivery-command",
            String.valueOf(orderId),
            new CreateDeliveryCommand(orderId, state.getAddress())
    );
}
```

재고 차감 결과를 받습니다. 단일 상품 모델이라 결과는 한 번만 옵니다. 실패면 차감 자체가 안 됐으니 복구할 게 없어 `cancel-order-command`만 보냅니다. 성공이면 곧바로 `create-delivery-command`로 다음 단계를 시작합니다.

*실패하면 주문만 취소하고, 성공하면 배달을 만들라고 명령한다. 지휘자가 정말로 악보를 보고 있구나.*

### 4.6.6 3단계 - 배달 생성 결과 수신 (deliveryCreated)

<div class="svg-figure">
<svg viewBox="0 0 1080 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="3단계 시퀀스: delivery-created 결과에 따라 성공이면 주문 완료, 실패면 재고 복구·주문 취소">
  <defs>
    <marker id="c4f9-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="c4f9-o" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <text x="540" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">3단계 — 배달 생성 결과 수신</text>
  <rect x="40" y="60" width="180" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="130" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Delivery</text>
  <rect x="290" y="60" width="200" height="50" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="390" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#7b341e">Orchestrator</text>
  <rect x="570" y="60" width="180" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="660" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Product</text>
  <rect x="820" y="60" width="180" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="910" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Order</text>
  <line x1="130" y1="110" x2="130" y2="370" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="390" y1="110" x2="390" y2="370" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="660" y1="110" x2="660" y2="370" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="910" y1="110" x2="910" y2="370" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="130" y1="150" x2="388" y2="150" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f9-o)"/>
  <text x="259" y="142" text-anchor="middle" font-size="13" font-weight="600" fill="#c2410c" font-family="JetBrains Mono, monospace">① delivery-created {success}</text>
  <line x1="390" y1="215" x2="818" y2="215" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f9-i)"/>
  <text x="604" y="207" text-anchor="middle" font-size="13" font-weight="600" fill="#4f46e5" font-family="JetBrains Mono, monospace">②a 성공 → complete-order-command → COMPLETED</text>
  <line x1="390" y1="285" x2="568" y2="285" stroke="#ff7849" stroke-width="1.6" marker-end="url(#c4f9-o)"/>
  <text x="479" y="277" text-anchor="middle" font-size="13" font-weight="600" fill="#c2410c" font-family="JetBrains Mono, monospace">②b 실패 → increase-product-command (보상)</text>
  <line x1="390" y1="345" x2="818" y2="345" stroke="#ff7849" stroke-width="1.6" marker-end="url(#c4f9-o)"/>
  <text x="604" y="337" text-anchor="middle" font-size="13" font-weight="600" fill="#c2410c" font-family="JetBrains Mono, monospace">②c 실패 → cancel-order-command → CANCELLED</text>
</svg>
</div>
*그림 4-10. 3단계 - 배달 생성 결과 수신*

`handler/OrderOrchestrator.java`에 3단계 리스너를 추가합니다.

```java [실습 7] handler/OrderOrchestrator.java. 3단계 - deliveryCreated
@KafkaListener(topics = "delivery-created", groupId = "orchestrator")
public void deliveryCreated(DeliveryCreatedEvent event) {
    int orderId = event.orderId();
    WorkflowState state = states.get(orderId);
    if (state == null) return;

    // 실패: 차감된 재고 복구 + 주문 취소
    if (!event.success()) {
        kafkaTemplate.send(
                "increase-product-command",
                String.valueOf(orderId),
                new IncreaseProductCommand(orderId, state.getProductId(), state.getQuantity(), state.getPrice())
        );
        kafkaTemplate.send(
                "cancel-order-command",
                String.valueOf(orderId),
                new CancelOrderCommand(orderId)
        );
        states.remove(orderId);
        return;
    }

    // 성공: 주문 완료 명령 발행
    kafkaTemplate.send(
            "complete-order-command",
            String.valueOf(orderId),
            new CompleteOrderCommand(orderId)
    );
    states.remove(orderId); // 워크플로우 종료
}
```

배달 생성이 실패하면 이전 단계에서 차감했던 재고를 복구하고 주문을 취소합니다. 성공하면 주문 완료 명령을 발행합니다. 단일 상품 모델이라 복구할 재고도 하나뿐입니다.

모든 서비스의 Kafka 연동 코드가 완성됐습니다. 이제 Kubernetes에 Kafka와 orchestrator를 추가하고 전체 시스템을 배포합니다.

## 4.7 Kubernetes - Kafka와 orchestrator 배포

챕터 3과 비교하여 이번 챕터에서 K8s에 새로 추가되는 것은 **Kafka**와 **orchestrator** 두 가지입니다. 기존 서비스의 ConfigMap에도 Kafka 주소를 추가해야 합니다.

### 4.7.1 Kafka

기존 Kafka는 ZooKeeper라는 별도 서비스가 필요했지만, **KRaft(Kafka Raft)** 모드를 사용하면 ZooKeeper 없이 Kafka 자체적으로 메타데이터를 관리합니다. `confluentinc/cp-kafka:7.5.0` 이미지를 사용합니다.

| K8s 리소스 | 파일 | 역할 | 비고 |
|---|---|---|---|
| Deployment | `kafka-deploy.yml` | KRaft 모드 Kafka 브로커 실행 (단일 노드) | `KAFKA_PROCESS_ROLES: broker,controller` |
| Service | `kafka-service.yml` | 브로커(9092) 포트 노출 | Spring Boot는 `kafka-service:9092`로 접근 |

Kafka 서버 1대에만 메시지를 저장하면, 그 서버가 죽었을 때 메시지가 전부 사라집니다. 그래서 실무에서는 Kafka 서버를 여러 대 띄우고 하나의 클러스터로 묶습니다. 같은 메시지를 여러 Kafka 서버에 복제해두면, 서버 1대가 죽어도 다른 서버에 데이터가 남아있습니다. 이번 챕터에서는 학습 편의를 위해 **단일 브로커**로 띄우지만 설정 구조는 멀티 브로커로 확장 가능합니다.

**KAFKA_NODE_ID**는 각 Kafka 서버를 식별하는 고유 번호입니다. Kafka 서버가 3대면 각각 1, 2, 3처럼 겹치지 않는 번호를 부여합니다. **CLUSTER_ID**는 이 Kafka 서버들을 하나의 클러스터로 묶는 식별자입니다. 같은 CLUSTER_ID를 가진 Kafka 서버끼리 메시지를 공유하고 복제합니다. 이때 서로를 찾는 주소는 **KAFKA_CONTROLLER_QUORUM_VOTERS**에 지정합니다. 우리 실습에서는 Kafka 서버가 1대이므로 자기 자신을 가리키는 `localhost:9093`만 설정하면 됩니다.

<div class="svg-figure">
<svg viewBox="0 0 1000 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="CLUSTER_ID로 묶인 Kafka 클러스터: 같은 CLUSTER_ID 값을 가진 브로커들이 하나의 클러스터로 묶임">
  <defs>
    <marker id="c4f10-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="500" y="32" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">CLUSTER_ID로 Kafka 브로커를 하나의 클러스터로 묶습니다</text>
  <rect x="60" y="70" width="880" height="220" rx="14" fill="#fff4ed" stroke="#ff7849" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="500" y="100" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e" font-family="JetBrains Mono, monospace">CLUSTER_ID: AbijZYk0QOm5p852kOMSIg</text>
  <rect x="380" y="130" width="240" height="120" rx="10" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="500" y="158" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">BROKER #1</text>
  <text x="500" y="186" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a" font-family="JetBrains Mono, monospace">KAFKA_NODE_ID = 1</text>
  <text x="500" y="216" text-anchor="middle" font-size="13" fill="#475569">실습용 단일 브로커</text>
  <text x="500" y="238" text-anchor="middle" font-size="11" fill="#94a3b8" font-family="JetBrains Mono, monospace">localhost:9093</text>
  <path d="M 620 200 Q 720 200, 720 230 Q 720 260, 620 240" stroke="#4f46e5" stroke-width="1.6" fill="none" marker-end="url(#c4f10-i)" stroke-dasharray="4 4"/>
  <text x="745" y="232" font-size="10" font-weight="600" fill="#4f46e5" font-family="JetBrains Mono, monospace">QUORUM_VOTERS</text>
  <text x="745" y="248" font-size="10" fill="#4f46e5" font-family="JetBrains Mono, monospace">(자기 자신)</text>
  <text x="500" y="320" text-anchor="middle" font-size="12" fill="#475569">단일 브로커이므로 컨트롤러가 자기 자신과만 통신합니다. 멀티 브로커일 때 같은 CLUSTER_ID를 가진 노드가 동기화됩니다.</text>
</svg>
</div>
*그림 4-11. CLUSTER_ID로 Kafka 브로커들을 하나의 클러스터로 묶습니다. 단일 브로커 실습에서는 컨트롤러가 자기 자신(localhost:9093)과만 통신합니다*

**KAFKA_ADVERTISED_LISTENERS**는 클라이언트가 Kafka에 접근할 때 사용하는 주소입니다. 각 서비스의 ConfigMap에 설정하는 `KAFKA_BOOTSTRAP_SERVERS: kafka-service:9092`가 이 주소를 가리킵니다.

<div class="svg-figure">
<svg viewBox="0 0 1000 460" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="KAFKA_ADVERTISED_LISTENERS: 4개의 클라이언트 서비스가 kafka-service:9092 주소로 브로커에 접근">
  <defs>
    <marker id="c4f11-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="500" y="32" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">KAFKA_ADVERTISED_LISTENERS — 클라이언트가 접근하는 주소</text>
  <rect x="60" y="70" width="200" height="70" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="160" y="98" text-anchor="middle" font-size="11" font-weight="700" fill="#475569">CLIENT</text>
  <text x="160" y="122" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">order-service</text>
  <rect x="280" y="70" width="200" height="70" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="380" y="98" text-anchor="middle" font-size="11" font-weight="700" fill="#475569">CLIENT</text>
  <text x="380" y="122" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">product-service</text>
  <rect x="500" y="70" width="200" height="70" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="600" y="98" text-anchor="middle" font-size="11" font-weight="700" fill="#475569">CLIENT</text>
  <text x="600" y="122" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">delivery-service</text>
  <rect x="720" y="70" width="200" height="70" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="820" y="98" text-anchor="middle" font-size="11" font-weight="700" fill="#475569">CLIENT</text>
  <text x="820" y="122" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">orchestrator</text>
  <line x1="160" y1="140" x2="450" y2="225" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f11-i)"/>
  <line x1="380" y1="140" x2="480" y2="225" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f11-i)"/>
  <line x1="600" y1="140" x2="520" y2="225" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f11-i)"/>
  <line x1="820" y1="140" x2="550" y2="225" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f11-i)"/>
  <text x="650" y="180" font-size="11" font-weight="600" fill="#4f46e5" font-family="JetBrains Mono, monospace">KAFKA_BOOTSTRAP_SERVERS</text>
  <rect x="220" y="240" width="560" height="150" rx="14" fill="#fff4ed" stroke="#ff7849" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="500" y="270" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e" font-family="JetBrains Mono, monospace">KAFKA_ADVERTISED_LISTENERS</text>
  <rect x="340" y="290" width="320" height="80" rx="10" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="500" y="318" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">BROKER</text>
  <text x="500" y="345" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a" font-family="JetBrains Mono, monospace">PLAINTEXT://kafka-service:9092</text>
  <text x="500" y="425" text-anchor="middle" font-size="12" fill="#475569">클라이언트의 KAFKA_BOOTSTRAP_SERVERS 값은 브로커의 ADVERTISED_LISTENERS 값과 일치해야 합니다.</text>
</svg>
</div>
*그림 4-12. 클라이언트는 KAFKA_ADVERTISED_LISTENERS에 지정된 kafka-service:9092로 Kafka에 접근합니다*

Kafka를 KRaft 모드로 실행하는 Deployment의 환경변수는 5그룹으로 묶입니다.

| 그룹 | 역할 | 단일 브로커 설정값 |
|---|---|---|
| 1. 식별 | 클러스터 UUID + 노드 번호 | `CLUSTER_ID` = UUID, `KAFKA_NODE_ID` = 1 |
| 2. 역할 | broker와 controller 겸용 | `KAFKA_PROCESS_ROLES` = broker,controller |
| 3. 포트 | 클라이언트용 9092 + 컨트롤러용 9093 | `KAFKA_LISTENERS`로 두 포트 정의 |
| 4. 주소 | 클라이언트가 접근하는 주소 | `KAFKA_ADVERTISED_LISTENERS` = kafka-service:9092 |
| 5. 복제 | 메시지를 복제할 서버 수 | `KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR` = 1 |

그룹 1과 그룹 4는 앞의 그림 4-11, 4-12에서 시각화했습니다. 그룹 2·3·5는 단일 브로커 실습에 맞춘 기본 설정이라 그대로 두면 됩니다. 전체 매니페스트와 정확한 옵션 값은 GitHub 레포 `k8s/kafka/kafka-deploy.yml`에서 확인합니다.

Kafka Pod에 접근할 수 있도록 K8s Service를 정의합니다. 컨트롤러용 9093 포트는 컨테이너 안에서만 쓰이므로 Service에는 클라이언트용 9092만 노출합니다.

```yaml kafka-service.yml. 브로커 포트 노출
apiVersion: v1
kind: Service
metadata:
  name: kafka-service
  namespace: metacoding
spec:
  type: ClusterIP
  selector:
    app: kafka
  ports:
    - port: 9092         # 클라이언트가 메시지 발행/구독에 쓰는 포트
```

### 4.7.2 orchestrator

orchestrator는 이번 챕터에서 새로 추가되는 서비스입니다. REST API 없이 Kafka 이벤트만 처리하므로 Service는 필요 없습니다.

| K8s 리소스 | 파일 | 역할 |
|---|---|---|
| ConfigMap | `orchestrator-configmap.yml` | `KAFKA_BOOTSTRAP_SERVERS` 설정 |
| Deployment | `orchestrator-deploy.yml` | orchestrator Pod 실행 |

### 4.7.3 기존 서비스 ConfigMap 수정

기존 서비스(order, product, delivery)의 ConfigMap `data:` 섹션에 `SPRING_KAFKA_BOOTSTRAP_SERVERS: kafka-service:9092` 한 줄을 추가합니다. 챕터 3에서 본 ConfigMap 형식 그대로입니다.

## 4.8 실행 및 결과 확인

### 4.8.1 이미지 빌드

Minikube 내부에 이미지를 빌드합니다. 챕터 3 대비 orchestrator 서비스가 새로 추가됩니다.

```bash [터미널] 이미지 빌드
minikube image build -t metacoding/db:2 ./db
minikube image build -t metacoding/gateway:2 ./gateway
minikube image build -t metacoding/order:2 ./order
minikube image build -t metacoding/product:2 ./product
minikube image build -t metacoding/user:2 ./user
minikube image build -t metacoding/delivery:2 ./delivery
minikube image build -t metacoding/orchestrator:2 ./orchestrator
```

### 4.8.2 배포 순서

Kafka가 준비되기 전에 서비스가 시작되면 연결 오류가 발생합니다. Kafka를 먼저 배포하고 ready 상태를 확인한 다음 나머지를 배포합니다.

```bash [터미널] 배포 순서 (Kafka 우선)
# 1. 네임스페이스 생성 (최초 1회)
kubectl create namespace metacoding

# 2. Kafka 먼저 배포
kubectl apply -f k8s/kafka

# 3. Kafka가 준비될 때까지 대기
kubectl wait --for=condition=ready pod -l app=kafka -n metacoding --timeout=120s

# 4. 나머지 서비스 배포
kubectl apply -f k8s/db
kubectl apply -f k8s/order
kubectl apply -f k8s/product
kubectl apply -f k8s/user
kubectl apply -f k8s/delivery
kubectl apply -f k8s/gateway
kubectl apply -f k8s/orchestrator

# 5. Ingress 활성화 (최초 1회)
minikube addons enable ingress
```
<!-- terminal-prompt: Terminal output showing sequential kubectl apply commands deploying Kafka and remaining services. Shows namespace creation, kafka deployment, kafka ready wait, then remaining service deployments with "created" or "configured" status messages. -->
<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">kubectl apply · Kafka + 서비스 배포</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-label">namespace</span>/metacoding <span class="tl-val">created</span></div>
    <div class="tl-section"><span class="tl-label">[1] Kafka 우선 배포</span></div>
    <div><span class="tl-label">deployment.apps</span>/kafka-deploy <span class="tl-val">created</span></div>
    <div><span class="tl-label">service</span>/kafka-service <span class="tl-val">created</span></div>
    <div><span class="tl-label">pod/kafka-xxx</span> condition met <span class="tl-num">(28s)</span></div>
    <div class="tl-section"><span class="tl-label">[2] 나머지 서비스 배포</span></div>
    <div class="tl-kv-row tl-dim">db · order · product · user · delivery · gateway · orchestrator …</div>
    <div class="tl-divider"><span class="tl-val">9개 Deployment + 8개 Service 배포 완료</span><span class="tl-cursor"></span></div>
  </div>
</div>
*그림 4-13. Kafka 및 서비스 배포 실행*




모든 Pod가 Running 상태인지 확인합니다.

```bash [터미널] Pod 상태 확인
kubectl get pods -n metacoding
```
<!-- terminal-prompt: Terminal output of "kubectl get pods -n metacoding" command. All pods (db, gateway, order, product, user, delivery, kafka, orchestrator) showing Running status with 1/1 Ready. -->
<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">kubectl get pods -n metacoding</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div class="tl-kv-row"><span class="tl-label">NAME</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-label">READY</span>&nbsp;&nbsp;<span class="tl-label">STATUS</span>&nbsp;&nbsp;&nbsp;<span class="tl-label">AGE</span></div>
    <div class="tl-kv-row">kafka-xxx&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">2m</span></div>
    <div class="tl-kv-row">db-deploy-xxx&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">90s</span></div>
    <div class="tl-kv-row">gateway-deploy-xxx&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">88s</span></div>
    <div class="tl-kv-row">order-deploy-xxx&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">85s</span></div>
    <div class="tl-kv-row">product-deploy-xxx&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">83s</span></div>
    <div class="tl-kv-row">user-deploy-xxx&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">80s</span></div>
    <div class="tl-kv-row">delivery-deploy-xxx&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">78s</span></div>
    <div class="tl-kv-row">orchestrator-xxx&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">75s</span></div>
    <div class="tl-divider"><span class="tl-val">8개 Pod Running (Kafka + orchestrator 추가)</span><span class="tl-cursor"></span></div>
  </div>
</div>
*그림 4-14. Pod 상태 확인 (kubectl get pods)*

챕터 3 끝에서 본 토폴로지에 Kafka 브로커와 orchestrator가 더해지면 다음과 같은 모양이 됩니다. 동기 HTTP 흐름은 그대로 유지되고, Kafka 메시지 채널이 옆에 따로 붙는 구조입니다.

<div class="svg-figure">
<svg viewBox="0 0 1200 700" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="챕터 4 통합 토폴로지: 챕터 3 구조에 Kafka 브로커와 orchestrator가 추가되어 order·product·delivery 서비스와 orchestrator가 Kafka로 메시지를 주고받는 구조">
  <defs>
    <marker id="ch04topo-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#1f2937"/></marker>
    <marker id="ch04topo-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="600" y="28" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">챕터 4 전체 구조 — Kafka 브로커와 orchestrator가 추가됨</text>
  <rect x="30" y="260" width="120" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="90" y="288" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Host</text>
  <text x="90" y="306" text-anchor="middle" font-size="10" fill="#6b7280">브라우저·Hoppscotch</text>
  <rect x="200" y="60" width="970" height="620" rx="12" fill="none" stroke="#475569" stroke-width="1.4" stroke-dasharray="6,4"/>
  <text x="220" y="82" font-size="11" font-style="italic" font-weight="700" fill="#475569">쿠버네티스 클러스터 · 네임스페이스 metacoding</text>
  <line x1="150" y1="290" x2="453" y2="140" stroke="#1f2937" stroke-width="1.4" marker-end="url(#ch04topo-a)"/>
  <text x="220" y="225" text-anchor="middle" font-size="10" font-style="italic" fill="#475569">minikube tunnel</text>
  <rect x="450" y="100" width="170" height="50" rx="8" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <text x="535" y="122" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">Ingress</text>
  <text x="535" y="138" text-anchor="middle" font-size="10" fill="#7b341e">gateway-ingress</text>
  <line x1="535" y1="150" x2="535" y2="186" stroke="#1f2937" stroke-width="1.6" marker-end="url(#ch04topo-a)"/>
  <rect x="400" y="190" width="270" height="70" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="535" y="216" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">gateway-service (Nginx)</text>
  <text x="535" y="234" text-anchor="middle" font-size="10" fill="#7b341e">API Gateway · :80</text>
  <text x="535" y="250" text-anchor="middle" font-size="9" font-family="monospace" fill="#9a3412">/login · /api/users · /api/products · /api/orders · /api/deliveries</text>
  <line x1="460" y1="260" x2="280" y2="316" stroke="#1f2937" stroke-width="1.2" marker-end="url(#ch04topo-a)"/>
  <line x1="500" y1="260" x2="450" y2="316" stroke="#1f2937" stroke-width="1.2" marker-end="url(#ch04topo-a)"/>
  <line x1="570" y1="260" x2="640" y2="316" stroke="#1f2937" stroke-width="1.2" marker-end="url(#ch04topo-a)"/>
  <line x1="610" y1="260" x2="810" y2="316" stroke="#1f2937" stroke-width="1.2" marker-end="url(#ch04topo-a)"/>
  <rect x="200" y="320" width="160" height="100" rx="8" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="280" y="343" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">user-service</text>
  <text x="280" y="360" text-anchor="middle" font-size="10" font-family="monospace" fill="#9a3412">:8083</text>
  <line x1="220" y1="370" x2="340" y2="370" stroke="#fed7aa" stroke-width="1"/>
  <rect x="230" y="378" width="100" height="32" rx="16" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="280" y="399" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">user-pod</text>
  <rect x="370" y="320" width="160" height="100" rx="8" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="450" y="343" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">product-service</text>
  <text x="450" y="360" text-anchor="middle" font-size="10" font-family="monospace" fill="#9a3412">:8082</text>
  <line x1="390" y1="370" x2="510" y2="370" stroke="#fed7aa" stroke-width="1"/>
  <rect x="400" y="378" width="100" height="32" rx="16" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="450" y="399" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">product-pod</text>
  <rect x="560" y="320" width="160" height="100" rx="8" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="640" y="343" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">order-service</text>
  <text x="640" y="360" text-anchor="middle" font-size="10" font-family="monospace" fill="#9a3412">:8081</text>
  <line x1="580" y1="370" x2="700" y2="370" stroke="#fed7aa" stroke-width="1"/>
  <rect x="590" y="378" width="100" height="32" rx="16" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="640" y="399" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">order-pod</text>
  <rect x="730" y="320" width="160" height="100" rx="8" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="810" y="343" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">delivery-service</text>
  <text x="810" y="360" text-anchor="middle" font-size="10" font-family="monospace" fill="#9a3412">:8084</text>
  <line x1="750" y1="370" x2="870" y2="370" stroke="#fed7aa" stroke-width="1"/>
  <rect x="760" y="378" width="100" height="32" rx="16" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="810" y="399" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">delivery-pod</text>
  <line x1="280" y1="420" x2="500" y2="565" stroke="#1f2937" stroke-width="1.1" stroke-dasharray="4,3" marker-end="url(#ch04topo-a)"/>
  <line x1="450" y1="420" x2="520" y2="565" stroke="#1f2937" stroke-width="1.1" stroke-dasharray="4,3" marker-end="url(#ch04topo-a)"/>
  <line x1="640" y1="420" x2="540" y2="565" stroke="#1f2937" stroke-width="1.1" stroke-dasharray="4,3" marker-end="url(#ch04topo-a)"/>
  <line x1="810" y1="420" x2="560" y2="565" stroke="#1f2937" stroke-width="1.1" stroke-dasharray="4,3" marker-end="url(#ch04topo-a)"/>
  <rect x="400" y="570" width="280" height="70" rx="8" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="540" y="594" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">db-service (MySQL)</text>
  <text x="540" y="613" text-anchor="middle" font-size="10" font-family="monospace" fill="#9a3412">:3306 · 4개 서비스가 metadb를 공유</text>
  <rect x="930" y="180" width="210" height="240" rx="10" fill="#eef2ff" stroke="#4f46e5" stroke-width="2"/>
  <text x="1035" y="204" text-anchor="middle" font-size="13" font-weight="700" fill="#3730a3">Kafka 브로커</text>
  <text x="1035" y="222" text-anchor="middle" font-size="10" font-family="monospace" fill="#4f46e5">kafka-service:9092</text>
  <text x="1035" y="240" text-anchor="middle" font-size="9" fill="#4f46e5">KRaft · 단일 브로커</text>
  <line x1="950" y1="252" x2="1120" y2="252" stroke="#c7d2fe" stroke-width="0.8"/>
  <text x="1035" y="270" text-anchor="middle" font-size="9" font-family="monospace" fill="#4f46e5">order-created</text>
  <text x="1035" y="285" text-anchor="middle" font-size="9" font-family="monospace" fill="#4f46e5">decrease-product-command</text>
  <text x="1035" y="300" text-anchor="middle" font-size="9" font-family="monospace" fill="#4f46e5">product-decreased</text>
  <text x="1035" y="315" text-anchor="middle" font-size="9" font-family="monospace" fill="#4f46e5">create-delivery-command</text>
  <text x="1035" y="330" text-anchor="middle" font-size="9" font-family="monospace" fill="#4f46e5">delivery-created</text>
  <text x="1035" y="345" text-anchor="middle" font-size="9" font-family="monospace" fill="#4f46e5">complete-order-command</text>
  <text x="1035" y="360" text-anchor="middle" font-size="9" font-family="monospace" fill="#4f46e5">cancel-order-command</text>
  <text x="1035" y="375" text-anchor="middle" font-size="9" font-family="monospace" fill="#4f46e5">increase-product-command</text>
  <text x="1035" y="400" text-anchor="middle" font-size="9" font-style="italic" fill="#4f46e5">총 8개 토픽</text>
  <rect x="930" y="450" width="210" height="100" rx="8" fill="#fff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="1035" y="475" text-anchor="middle" font-size="13" font-weight="700" fill="#3730a3">orchestrator</text>
  <text x="1035" y="491" text-anchor="middle" font-size="10" fill="#4f46e5">중앙 지휘자 · REST 없음</text>
  <line x1="950" y1="500" x2="1120" y2="500" stroke="#c7d2fe" stroke-width="0.8"/>
  <rect x="970" y="510" width="130" height="32" rx="16" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.4"/>
  <text x="1035" y="531" text-anchor="middle" font-size="11" font-weight="700" fill="#3730a3">orchestrator-pod</text>
  <line x1="530" y1="375" x2="928" y2="300" stroke="#4f46e5" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#ch04topo-i)"/>
  <line x1="928" y1="320" x2="530" y2="395" stroke="#4f46e5" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#ch04topo-i)"/>
  <line x1="720" y1="375" x2="928" y2="270" stroke="#4f46e5" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#ch04topo-i)"/>
  <line x1="928" y1="285" x2="720" y2="395" stroke="#4f46e5" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#ch04topo-i)"/>
  <line x1="890" y1="375" x2="928" y2="345" stroke="#4f46e5" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#ch04topo-i)"/>
  <line x1="928" y1="360" x2="890" y2="395" stroke="#4f46e5" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#ch04topo-i)"/>
  <line x1="1045" y1="420" x2="1045" y2="448" stroke="#4f46e5" stroke-width="1.4" marker-end="url(#ch04topo-i)"/>
  <line x1="1025" y1="450" x2="1025" y2="422" stroke="#4f46e5" stroke-width="1.4" marker-end="url(#ch04topo-i)"/>
  <text x="600" y="668" text-anchor="middle" font-size="12" font-style="italic" fill="#475569">검은 실선: 동기 HTTP · 인디고 점선: Kafka 메시지(publish · subscribe)</text>
</svg>
</div>
*그림 4-15. 챕터 4 통합 토폴로지 - 챕터 3에 Kafka 브로커와 orchestrator가 추가된 모습*

챕터 3의 동기 HTTP 흐름(검은 실선)은 그대로 살아 있습니다. 사용자가 보내는 HTTP 요청은 여전히 Ingress → gateway-service → 각 마이크로서비스를 거칩니다. 달라진 점은 그 옆에 **Kafka 채널(인디고 점선)** 이 별도로 흐른다는 사실입니다. order·product·delivery 세 서비스는 Kafka로 이벤트를 주고받습니다. orchestrator는 오직 Kafka로만 통신하고, user-service는 Kafka를 사용하지 않습니다.

### 4.8.3 서비스 접근

Ingress를 통해 외부에서 접속하려면 `minikube tunnel`을 실행합니다.

```bash [터미널] 외부 접근 터널
minikube tunnel
```

터널이 실행되면 `http://127.0.0.1:80`로 gateway-service에 접속할 수 있습니다.



### 4.8.4 비동기 흐름 테스트

AirPods (productId=3)를 주문합니다.

```json
POST http://127.0.0.1:80/api/orders

{
  "productId": 3,
  "quantity": 2,
  "price": 300000,
  "address": "Addr 4"
}
```
<!-- terminal-prompt: HTTP client (IntelliJ or Postman) showing POST /api/orders response. JSON body with order status "PENDING". -->
![](assets/CH04/terminal/14_order-pending.png)
*그림 4-16. 주문 생성 응답 (PENDING 상태)*


챕터 3과 다르게 즉시 `PENDING` 상태로 반환됩니다. Kafka 이벤트가 처리되면 상태가 `COMPLETED`로 변경됩니다. 잠시 후 주문 상태를 다시 조회합니다.

```json
GET http://127.0.0.1:80/api/orders/4
```
<!-- terminal-prompt: HTTP client showing GET /api/orders/4 response. JSON body with order status changed to "COMPLETED". -->
![](assets/CH04/terminal/15_order-completed.png)
*그림 4-17. 주문 완료 확인 (COMPLETED 상태)*

**오픈이**: "PENDING이었다가 COMPLETED로 바뀌었어요! 그런데 롤백도 자동으로 되나요?"

**선배**: "품절 상품으로 주문해 봐요. orchestrator 로그를 보면 보일 거예요."

### 4.8.5 롤백 확인 - 품절 상품 주문

iPhone 15(productId=2, 재고 0)를 주문하면 product-service에서 재고 감소가 실패하고, orchestrator가 자동으로 롤백을 시작합니다.

```json
POST http://127.0.0.1:80/api/orders

{
  "productId": 2,
  "quantity": 1,
  "price": 1300000,
  "address": "Addr 5"
}
```
<!-- terminal-prompt: HTTP client showing POST /api/orders response for out-of-stock product (productId=2). JSON body with order status "PENDING". -->
![](assets/CH04/terminal/16_stockout-order.png)
*그림 4-18. 품절 상품 주문 요청*

잠시 후 상태를 확인하면 `CANCELLED`가 됩니다.

```JSON
GET http://127.0.0.1:80/api/orders/5
```


orchestrator 로그에서 롤백 과정을 확인할 수 있습니다.

<!-- terminal-prompt: Terminal output of "kubectl logs" for orchestrator pod. Log messages showing: product-decreased failure received, increase-product-command published, cancel-order-command published — the rollback sequence. -->
<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">kubectl logs · orchestrator (롤백 시퀀스)</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-label">orderCreated</span> <span class="tl-dim">|</span> <span class="tl-key">orderId</span>=<span class="tl-num">5</span> <span class="tl-key">productId</span>=<span class="tl-num">2</span></div>
    <div><span class="tl-label">→ publish</span> <span class="tl-str">decrease-product-command</span></div>
    <div class="tl-section"><span class="tl-label">productDecreased</span> <span class="tl-dim">|</span> <span class="tl-key">success</span>=<span class="tl-str">false</span> <span class="tl-dim">(재고 부족)</span></div>
    <div><span class="tl-label">⚠ 차감 실패 — 복구할 재고 없음</span></div>
    <div><span class="tl-label">→ publish</span> <span class="tl-str">cancel-order-command</span></div>
    <div class="tl-divider"><span class="tl-val">롤백 완료 · 주문 CANCELLED</span><span class="tl-cursor"></span></div>
  </div>
</div>
*그림 4-19. orchestrator 롤백 로그 확인*



테스트가 끝났으면 이번 챕터에서 실행한 리소스를 정리합니다.

```bash [터미널] 리소스 정리
kubectl delete all --all -n metacoding
```

*상품 서비스를 꺼봤다. 주문 서비스는 멀쩡히 돌아갔고, 메시지는 Kafka에 쌓였다. 다시 켜자 밀려 있던 메시지가 순서대로 처리됐다. 단순히 서비스를 나눈 것을 넘어, 진정한 독립을 이룬 기분이다.*

**선배**: "이제 사용자 입장에서 한번 생각해 봐요. 주문이 끝났는지 알려면 새로고침을 계속 눌러야 하잖아요."

이제 product-service가 잠시 다운되어도 order-service는 이벤트를 Kafka에 올려두고 즉시 반환합니다. product-service가 복구되면 토픽에서 메시지를 읽어 처리합니다. 두 서비스가 강하게 결합되어 있던 문제가 해결됐습니다. 하지만 사용자 입장에서 불편한 점이 남아 있습니다. 주문이 `COMPLETED`가 됐다는 것을 알기 위해 직접 주기적으로 조회(폴링)해야 하고, 배달도 여전히 주문과 동시에 완료되어 실제 배달 완료 시점을 반영하지 못합니다.

:::remember
**이것만은 기억하자**

- 동기 REST 호출을 **Kafka 비동기 이벤트**로 교체하여 서비스 간 결합을 끊었습니다.
- **orchestrator** 서비스가 Kafka 토픽을 통해 전체 워크플로우를 조율합니다.
- `ConcurrentHashMap`으로 주문별 진행 상태를 추적하고, 실패 시 이미 처리된 단계만 자동 롤백합니다.
- order-service는 주문 생성 즉시 `PENDING` 상태로 반환하고, 처리 완료 후 `COMPLETED`로 갱신됩니다.

다음 챕터에서는 이 두 가지를 해결합니다. 배달 기사가 완료 API를 호출하여 실제 배달 완료를 처리하고, WebSocket으로 클라이언트에게 주문 완료를 실시간 Push로 알립니다.
:::
