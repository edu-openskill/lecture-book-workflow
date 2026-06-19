# 챕터 0. 프롤로그

## 0.1 서버가 멈추다

밤 열한 시, 막 잠이 들려던 참에 휴대폰이 울렸습니다. 운영팀이었습니다.

**운영팀**: "사이트가 전부 멈췄습니다. 확인 좀 해 주세요."

잠이 확 달아났습니다. 노트북을 열자 대시보드가 온통 에러 로그로 덮여 있었습니다. 저녁 일곱 시에 시작한 할인 이벤트로 트래픽이 몰리면서, 그 부하를 버티지 못한 서버가 다운된 것입니다.

서둘러 서버를 재시작했지만 바로 안정되지 않았고, 트래픽이 빠지기 시작한 새벽 한 시가 되어서야 겨우 안정을 되찾았습니다.

*트래픽 때문에 사이트 전체가 멈춰 버리다니.*

다음 날 아침, 팀장이 자리로 찾아왔습니다.

**팀장**: "이번처럼 트래픽 때문에 사이트 전체가 다운되면 곤란해요. 재발 방지 대책 좀 찾아봐 줘요."

선뜻 답할 수 없었습니다. 지난번에도 트래픽이 몰렸을 때 서버를 늘려 봤지만, 비용과 노력만 들었을 뿐 같은 장애가 되풀이됐기 때문입니다. 결국 선배를 찾아갔습니다.

**오픈이**: "선배님, 트래픽은 주문에만 몰렸는데 로그인이고 상품 조회고 할 것 없이 전부 멈춰 버렸어요. 이건 어떻게 해야 할까요?"

선배가 웃으며 대답했습니다.

**선배**: "모든 기능이 한 서버에 다 뭉쳐 있어서 그래요. 백화점은 정전 한 번에 전 층이 같이 문을 닫지만, 길가의 독립 상점은 한 곳이 닫아도 옆 가게는 멀쩡하잖아요. **기능을 그 상점들처럼 독립된 서비스로 분리하면, 한 곳에 트래픽이 몰려 서버가 다운돼도 다른 기능은 멀쩡하거든요.** 이런 구조를 **MSA**라고 해요. 일단 나누는 것부터 시작해 봐요."

## 0.2 서비스를 나누다

**오픈이**: "선배님, 그럼 어떤 것부터 시작하면 될까요?"

**선배**: "우선 회원, 주문, 상품, 배달을 기능별로 서비스로 나눠요. 그리고 서비스끼리 전화를 거는 것처럼 직접 호출하게 만드는 거예요."

선배의 말대로 한 서버에 모여 있던 기능을 네 개의 서비스로 나눴습니다. 주문이 들어오면 주문 서비스가 상품 서비스에 재고를 줄여 달라고 요청하고, 이어서 배달 서비스에 배달 생성을 요청하도록 연결했습니다.

그런데 곧 문제에 부딪혔습니다. 중간에 에러가 나면 되돌릴 방법이 없었습니다. 예전처럼 데이터베이스가 하나일 때는 에러가 나면 전부 롤백하면 그만이었지만, 이제는 서비스마다 데이터베이스가 따로 나뉘어 있어 그럴 수가 없었습니다.

**오픈이**: "선배님, 재고는 이미 줄였는데 배달이 실패하면 줄인 재고를 되돌릴 방법이 없어요. 어떻게 하죠?"

**선배**: "자동으로 안 되니 직접 되돌려야죠. 배달에서 실패하면, 이전 단계인 상품 서비스에 '재고를 복구해 줘'라고 요청을 보내는 거예요. **한 단계씩 거꾸로 취소하는 겁니다.** 이걸 **보상 트랜잭션**이라고 불러요."

주문이 어디까지 진행됐는지 상태를 기록해 두고, 실패하면 이전 서비스로 취소 요청을 보내는 로직을 짰습니다. 단계마다 취소 코드를 일일이 붙이는 건 번거로웠습니다. 그래도 일부러 중간 단계를 실패시켜 보니, 앞서 끝난 단계가 한 단계씩 원래대로 되돌아갔습니다.

그렇게 기능별로 나눈 서비스들이 처음으로 하나의 흐름으로 함께 동작하기 시작했습니다.

## 0.3 구조를 다시 세우다

며칠 뒤, 팀장이 자리로 찾아왔습니다.

**팀장**: "주문 기능을 테스트하려는데, 컨트롤러가 서비스에 직접 의존해서 가짜(Mock) 객체로 테스트할 수가 없어요. 이거 직접 의존하지 않게 구조 정리해 줘요."

곧바로 코드를 열어 봤습니다. 컨트롤러를 테스트하려면 서비스까지 함께 동작해야 했고, 가짜 객체를 넣으려 해도 컨트롤러 코드를 직접 고쳐야 했습니다. 고민에 빠진 채 다시 선배를 찾아가 코드를 보여 주며 물었습니다.

**선배**: "지금은 결합도가 너무 높아서 그래요. 두 가지만 알면 돼요. 먼저 **구현이 아니라 인터페이스에 의존하게 만들어요.** 그래야 코드를 고치지 않고도 진짜 객체를 가짜 객체로 바꿔 테스트할 수 있어요. 이게 **클린 아키텍처**예요. 그리고 **흩어져 있는 핵심 비즈니스 로직은 도메인 안에 모아 둬요.** 그래야 바깥이 어떻게 바뀌어도 비즈니스 규칙은 흔들리지 않죠. 이걸 **도메인 주도 개발**이라고 해요."

클린 아키텍처와 도메인 주도 개발은 이름만 들어 봤지, 직접 적용해 보긴 처음이었습니다. 두 개념을 이해하고 나서, 익숙한 구조를 하나씩 뜯어고쳤습니다.

컨트롤러가 서비스에 직접 의존하는 대신, 그 사이에 USB 허브 같은 인터페이스를 두었습니다. 허브 뒤의 장치가 바뀌어도 컴퓨터는 아무 영향이 없듯, 컨트롤러는 '무엇을 할지'만 약속한 그 인터페이스에만 의존하고, '어떻게 할지'는 인터페이스를 구현한 서비스 쪽에 맡겼습니다.

검증 규칙도 정리했습니다. 재고 확인이나 주문 검증처럼 서비스 코드 곳곳에 흩어져 있던 규칙을 각 서비스의 도메인 객체 안으로 모았습니다. 규칙이 도메인 안에 모이니, 나중에 규칙이 바뀌어도 도메인만 고치면 됐습니다.

그러자 컨트롤러는 더 이상 서비스에 직접 의존하지 않게 됐습니다. 컨트롤러는 한 줄도 건드리지 않고, 인터페이스를 구현한 서비스만 가짜 객체로 바꿔 끼울 수 있었습니다.

## 0.4 비동기로 전환하다

동기 호출 방식으로 며칠을 운영하던 중, 또 다른 난관이 찾아왔습니다. 상품 서비스가 잠깐 죽은 사이에 들어온 주문이 전부 실패해 버렸습니다. 주문 서비스가 상품 서비스를 직접 호출하고 그 응답을 기다리는 구조라, 상대가 죽어 있으면 호출한 주문도 그대로 실패하는 것입니다.

**오픈이**: "선배님, 상품 서비스 하나가 잠깐 죽었을 뿐인데 거기를 호출한 주문까지 다 같이 실패해 버리네요."

**선배**: "직접 호출하지 말고, 메시지를 주고받는 비동기 방식으로 바꿔 봐요. **받는 쪽이 잠깐 죽어 있어도 메시지는 그대로 남아 있다가, 서버가 복구되면 그때 처리되거든요.** **Kafka**를 한번 써 봐요."

Kafka는 처음 다뤄 보는 도구였습니다. 메시지를 발행하고 구독하는 방식을 익힌 뒤, 서비스끼리 직접 호출하던 것을 하나씩 걷어내고 Kafka 메시지로 바꿨습니다.

**오픈이**: "그런데 이렇게 메시지로 주고받으면, 중간에 실패했을 때 보상 트랜잭션은 누가 관리하나요?"

**선배**: "전체 흐름을 관리하는 지휘자를 하나 두면 돼요. 각 서비스는 자기 일만 하고 결과만 보고하고, 그 지휘자가 어디까지 됐는지에 따라 다음 단계를 진행시키거나, 실패하면 이미 끝난 단계만 되돌리는 거죠."

선배 말대로 전체 흐름을 관리할 **오케스트레이터** 서비스를 만들었습니다. 각 서비스는 자기 일을 끝내면 결과만 메시지로 보고했고, 오케스트레이터는 그 보고를 받아 다음 단계를 진행시키거나, 실패하면 이미 끝난 단계를 되돌렸습니다.

이제 상품 서비스가 잠깐 멈춰도 주문은 메시지로 남아 있다가, 복구되면 하나씩 처리됐습니다. 흐름 중간이 실패해도 오케스트레이터가 끝난 단계만 되돌렸습니다.

## 0.5 실시간으로 알리다

며칠 뒤, 베타 테스터로 새 시스템을 써 본 동료가 떨떠름한 얼굴로 찾아왔습니다.

**동료**: "어제 물건을 주문했는데, 화면이 계속 '처리 중'이더라고요. 끝났는지 알 수가 없어서 한참 뒤에 주문 내역을 다시 열어 보고서야 완료된 걸 알았어요."

확인해 보니 서버들끼리는 Kafka로 메시지를 주고받으며 처리를 끝냈지만, 정작 그 사실을 사용자에게는 알리지 않고 있었습니다. 사용자는 처음 받은 '처리 중' 상태에 그대로 멈춰 있었고, 결과를 보려면 직접 주문 내역을 다시 열어야 했습니다.

**오픈이**: "선배님, 서버에서는 주문 처리가 완료됐는데 사용자는 처음 '처리 중' 응답만 받아서 끝난 걸 알 수가 없어요. 이건 어떻게 해결하죠?"

**선배**: "처리가 끝난 순간 사용자에게 바로 알려 줘야 해요. 서버가 주문 완료 시점을 감지해서, 사용자 화면으로 먼저 말을 걸 수 있게 **WebSocket**을 붙여 봐요."

선배의 말을 듣고 코드를 다시 보니 어긋난 곳이 두 군데였습니다. 주문은 배달이 만들어지는 순간 곧바로 완료로 처리됐고, 정작 그 완료를 사용자에게는 알리지 않았습니다.

먼저 배달이 실제로 끝나는 순간에 주문을 완료 처리하도록 바꿨습니다. 남은 건 그걸 사용자에게 알리는 일이었습니다. WebSocket을 들여다보니 늘 쓰던 HTTP와는 정반대였습니다. HTTP가 한 번 주고받으면 끊기는 편지라면, **WebSocket은 한 번 연결하면 계속 이어지는 전화였습니다.** 연결이 살아 있으니 서버는 변화가 생기는 순간 바로 알릴 수 있었습니다. 그래서 주문이 완료되면 서버가 WebSocket으로 사용자 화면에 알림을 보내도록 연결했습니다.

수정된 코드로 직접 주문을 넣어 보았습니다. 새로고침을 누르지 않았는데도, '처리 중'이던 화면이 '주문 완료'로 바뀌었습니다.

**동료**: "이제 새로고침 없이도 주문이 끝난 걸 바로 알 수 있겠네요."

완성된 시스템을 선배에게 보여 주었습니다.

**오픈이**: "처음 서버가 멈췄던 밤엔 정말 막막했는데, 한 단계씩 부딪히며 오다 보니 결국 해내게 되네요."

선배는 흐뭇한 표정으로 답했습니다.

**선배**: "처음부터 모든 정답을 알고 시작하는 사람은 없어요. 부딪히고, 고치고, 다시 만들다 보면 되는 거예요."



---



# 챕터 1. MSA란 무엇인가?

밤 열한 시, 막 잠이 들려던 참에 휴대폰이 울렸습니다. 운영팀이었습니다.

**운영팀**: "사이트가 전부 멈췄습니다. 확인 좀 해 주세요."

잠이 확 달아났습니다. 노트북을 열자 대시보드가 온통 에러 로그로 덮여 있었습니다. 저녁 일곱 시에 시작한 할인 이벤트로 트래픽이 몰리면서, 그 부하를 버티지 못한 서버가 다운된 것입니다.

서둘러 서버를 재시작했지만 바로 안정되지 않았고, 트래픽이 빠지기 시작한 새벽 한 시가 되어서야 겨우 안정을 되찾았습니다.

*트래픽 때문에 사이트 전체가 멈춰 버리다니.*

다음 날 아침, 팀장이 자리로 왔습니다.

**팀장**: "이번처럼 트래픽 때문에 사이트 전체가 다운되면 곤란해요. 재발 방지 대책 좀 찾아봐요."

오픈이는 바로 답을 하지 못했습니다. 지난번에 트래픽이 몰렸을 때도 서버를 증설해 봤지만, 비용과 노력만 잔뜩 들었을 뿐 같은 장애가 되풀이됐습니다. 결국 선배를 찾아갔습니다.

**오픈이**: "선배님, 이번에 트래픽이 몰렸다고 사이트가 통째로 죽어버렸는데요. 이거 어떻게 해야 할까요?"

**선배**: "모든 기능이 한 서버에 다 뭉쳐 있어서 그래요. 한쪽에 부하가 걸리면 전체가 다 같이 멈추는 거죠. 이럴 때는 기능을 독립된 서비스로 분리해야 해요. 그러면 한 곳에 트래픽이 몰려 서버가 다운되더라도, 다른 기능은 멀쩡하거든요."

:::goal
**이번 챕터가 끝나면**

- **모놀리식**의 한계를 이해할 수 있습니다.
- **마이크로서비스**가 역할을 나눠 그 한계를 푸는 방식을 이해할 수 있습니다.
- 서비스를 나누며 떠오르는 핵심 과제, **분산 트랜잭션**을 이해할 수 있습니다.
:::

::::prep
**준비하기**. 챕터 2부터 시작될 실습을 위해 미리 준비

이 챕터는 개념만 다루므로 직접 코드를 작성하지 않습니다. 챕터 2부터 실습이 시작되니, 그전에 도구 설치와 레포 위치를 미리 확인해 두세요.

### 1. 실습 환경

| 도구 | 사용 챕터 | 설치 주소 |
|------|----------|-----------|
| **Docker Desktop** | 챕터 2~ | https://www.docker.com/products/docker-desktop/ |
| **Minikube** | 챕터 3~ | https://minikube.sigs.k8s.io/ |
| **Hoppscotch** (브라우저 확장) | 챕터 2~ | https://hoppscotch.io/ |

### 2. 챕터별 소스 코드

이 책의 실습은 챕터마다 GitHub 레포가 하나씩 대응합니다. 챕터 2부터 해당 레포를 클론하여 진행합니다.

| 챕터 | 레포 | 주제 |
|------|------|------|
| 챕터 2 | `github.com/metacoding-12-msa/ex01` | 동기 REST + 보상 트랜잭션 |
| 챕터 3 | `github.com/metacoding-12-msa/ex02` | DDD + 클린 아키텍처 + Kubernetes |
| 챕터 4 | `github.com/metacoding-12-msa/ex03` | Kafka + Orchestration Saga |
| 챕터 5 | `github.com/metacoding-12-msa/ex04` | WebSocket 실시간 알림 |
::::

## 1.1 모놀리식 - 쇼핑몰을 하나의 서버로 만들면 어떻게 될까?

### 1.1.1 처음에는 아무 문제가 없었다

백화점을 떠올려 보세요. 수십 개의 매장이 한 건물 안에 모여 있습니다. 고객은 한 곳에서 모든 것을 해결할 수 있습니다. 백화점 입장에서는 전기·냉방·보안·고객 데이터를 한 곳에서 통합 관리할 수 있습니다. 이 구조는 단순하고 효율적입니다.

<div class="svg-figure">
<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="백화점 비유: 4층 건물에 매장이 층별로 들어 있는 구조">
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">백화점 — 모든 매장이 한 건물에</text>
  <rect x="170" y="86" width="22" height="14" fill="#fff" stroke="#475569" stroke-width="1.2"/>
  <line x1="174" y1="88" x2="174" y2="100" stroke="#475569" stroke-width="0.6"/>
  <line x1="178" y1="88" x2="178" y2="100" stroke="#475569" stroke-width="0.6"/>
  <line x1="182" y1="88" x2="182" y2="100" stroke="#475569" stroke-width="0.6"/>
  <line x1="186" y1="88" x2="186" y2="100" stroke="#475569" stroke-width="0.6"/>
  <rect x="205" y="92" width="20" height="8" fill="#fff" stroke="#475569" stroke-width="1.2"/>
  <rect x="595" y="76" width="32" height="24" rx="2" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <line x1="611" y1="76" x2="611" y2="66" stroke="#475569" stroke-width="1"/>
  <circle cx="611" cy="64" r="2" fill="#475569"/>
  <line x1="660" y1="100" x2="660" y2="58" stroke="#475569" stroke-width="1.3"/>
  <line x1="655" y1="64" x2="665" y2="64" stroke="#475569" stroke-width="1"/>
  <line x1="657" y1="72" x2="663" y2="72" stroke="#475569" stroke-width="0.8"/>
  <line x1="658" y1="80" x2="662" y2="80" stroke="#475569" stroke-width="0.6"/>
  <rect x="92" y="100" width="616" height="6" fill="#0f172a"/>
  <rect x="100" y="106" width="600" height="14" fill="#475569"/>
  <rect x="110" y="120" width="580" height="408" fill="#fff" stroke="#475569" stroke-width="2"/>
  <line x1="110" y1="120" x2="118" y2="120" stroke="#475569" stroke-width="6"/>
  <line x1="682" y1="120" x2="690" y2="120" stroke="#475569" stroke-width="6"/>
  <rect x="130" y="134" width="540" height="86" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.4"/>
  <text x="158" y="156" font-size="13" font-weight="800" fill="#3730a3">4F</text>
  <rect x="192" y="158" width="22" height="44" fill="#fff" stroke="#4f46e5" stroke-width="1"/>
  <line x1="192" y1="180" x2="214" y2="180" stroke="#4f46e5" stroke-width="0.8"/>
  <line x1="203" y1="158" x2="203" y2="202" stroke="#4f46e5" stroke-width="0.8"/>
  <rect x="586" y="158" width="22" height="44" fill="#fff" stroke="#4f46e5" stroke-width="1"/>
  <line x1="586" y1="180" x2="608" y2="180" stroke="#4f46e5" stroke-width="0.8"/>
  <line x1="597" y1="158" x2="597" y2="202" stroke="#4f46e5" stroke-width="0.8"/>
  <g transform="translate(290 144)">
    <path d="M22 32 Q12 27 14 47 Q16 65 30 70 Q33 71 35 70 Q37 71 40 70 Q54 65 56 47 Q58 27 48 32 Q42 24 35 32 Q28 24 22 32 Z" fill="#fff" stroke="#3730a3" stroke-width="1.8" stroke-linejoin="round"/>
    <path d="M35 28 Q38 18 46 18" fill="none" stroke="#3730a3" stroke-width="1.8" stroke-linecap="round"/>
    <ellipse cx="44" cy="21" rx="5" ry="3" fill="#3730a3" transform="rotate(-25 44 21)"/>
  </g>
  <text x="500" y="184" text-anchor="middle" font-size="18" font-weight="700" fill="#3730a3">식품 매장</text>
  <rect x="130" y="232" width="540" height="86" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.4"/>
  <text x="158" y="254" font-size="13" font-weight="800" fill="#3730a3">3F</text>
  <rect x="192" y="256" width="22" height="44" fill="#fff" stroke="#4f46e5" stroke-width="1"/>
  <line x1="192" y1="278" x2="214" y2="278" stroke="#4f46e5" stroke-width="0.8"/>
  <line x1="203" y1="256" x2="203" y2="300" stroke="#4f46e5" stroke-width="0.8"/>
  <rect x="586" y="256" width="22" height="44" fill="#fff" stroke="#4f46e5" stroke-width="1"/>
  <line x1="586" y1="278" x2="608" y2="278" stroke="#4f46e5" stroke-width="0.8"/>
  <line x1="597" y1="256" x2="597" y2="300" stroke="#4f46e5" stroke-width="0.8"/>
  <g transform="translate(293 248)">
    <rect x="0" y="0" width="65" height="46" rx="4" fill="#fff" stroke="#3730a3" stroke-width="1.8"/>
    <rect x="5" y="5" width="55" height="36" rx="2" fill="none" stroke="#3730a3" stroke-width="1.2"/>
    <line x1="10" y1="62" x2="55" y2="62" stroke="#3730a3" stroke-width="1.8" stroke-linecap="round"/>
    <line x1="22" y1="46" x2="22" y2="62" stroke="#3730a3" stroke-width="1.8"/>
    <line x1="43" y1="46" x2="43" y2="62" stroke="#3730a3" stroke-width="1.8"/>
  </g>
  <text x="500" y="282" text-anchor="middle" font-size="18" font-weight="700" fill="#3730a3">전자제품 매장</text>
  <rect x="130" y="330" width="540" height="86" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.4"/>
  <text x="158" y="352" font-size="13" font-weight="800" fill="#3730a3">2F</text>
  <rect x="192" y="354" width="22" height="44" fill="#fff" stroke="#4f46e5" stroke-width="1"/>
  <line x1="192" y1="376" x2="214" y2="376" stroke="#4f46e5" stroke-width="0.8"/>
  <line x1="203" y1="354" x2="203" y2="398" stroke="#4f46e5" stroke-width="0.8"/>
  <rect x="586" y="354" width="22" height="44" fill="#fff" stroke="#4f46e5" stroke-width="1"/>
  <line x1="586" y1="376" x2="608" y2="376" stroke="#4f46e5" stroke-width="0.8"/>
  <line x1="597" y1="354" x2="597" y2="398" stroke="#4f46e5" stroke-width="0.8"/>
  <g transform="translate(295 342)">
    <path d="M0 12 L15 0 L20 12 L40 12 L45 0 L60 12 L52 32 L42 30 L42 70 L18 70 L18 30 L8 32 Z" fill="#fff" stroke="#3730a3" stroke-width="1.8" stroke-linejoin="round"/>
    <path d="M15 0 L30 14 L45 0" fill="none" stroke="#3730a3" stroke-width="1.3"/>
  </g>
  <text x="500" y="380" text-anchor="middle" font-size="18" font-weight="700" fill="#3730a3">의류 매장</text>
  <rect x="130" y="428" width="540" height="86" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.4"/>
  <text x="158" y="450" font-size="13" font-weight="800" fill="#3730a3">1F</text>
  <rect x="192" y="452" width="22" height="44" fill="#fff" stroke="#4f46e5" stroke-width="1"/>
  <line x1="192" y1="474" x2="214" y2="474" stroke="#4f46e5" stroke-width="0.8"/>
  <line x1="203" y1="452" x2="203" y2="496" stroke="#4f46e5" stroke-width="0.8"/>
  <rect x="586" y="452" width="22" height="44" fill="#fff" stroke="#4f46e5" stroke-width="1"/>
  <line x1="586" y1="474" x2="608" y2="474" stroke="#4f46e5" stroke-width="0.8"/>
  <line x1="597" y1="452" x2="597" y2="496" stroke="#4f46e5" stroke-width="0.8"/>
  <g transform="translate(290 442)">
    <rect x="0" y="22" width="18" height="40" rx="2" fill="#fff" stroke="#3730a3" stroke-width="1.6"/>
    <rect x="2" y="4" width="14" height="20" rx="1" fill="#3730a3"/>
    <rect x="6" y="0" width="6" height="6" fill="#3730a3"/>
    <rect x="32" y="24" width="32" height="38" rx="3" fill="#fff" stroke="#3730a3" stroke-width="1.6"/>
    <rect x="42" y="10" width="12" height="14" fill="#fff" stroke="#3730a3" stroke-width="1.4"/>
    <rect x="44" y="4" width="8" height="6" fill="#3730a3"/>
  </g>
  <text x="500" y="478" text-anchor="middle" font-size="18" font-weight="700" fill="#3730a3">화장품 매장</text>
  <line x1="60" y1="540" x2="740" y2="540" stroke="#475569" stroke-width="2.5"/>
  <line x1="60" y1="546" x2="740" y2="546" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="5,5"/>
  <text x="400" y="580" text-anchor="middle" font-size="13" fill="#6b7280" font-style="italic">층층이 다른 매장이 한 건물에 모여 한 곳에서 운영되는 구조</text>
</svg>
</div>

*그림 1-1. 백화점 - 모든 매장이 한 건물에 모여 있는 구조*

소프트웨어에서도 동일하게 적용됩니다. 처음에는 **하나의 서버에 모든 기능을 넣는 모놀리식(Monolithic) 구조**가 단순하고 관리가 편합니다.

### 1.1.2 성장하면서 균열이 생긴다

한 공간에 모든 매장이 모여 있는 백화점은 시간이 지나면서 문제가 보이기 시작합니다. 한 매장에 화재가 발생하면 전 층이 함께 대피해야 합니다. 또 정전이 발생하면 건물 전체가 함께 멈춥니다.

이 약점은 소프트웨어의 모놀리식에서도 그대로 나타납니다.

<div class="svg-figure">
<svg viewBox="0 0 800 530" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="모놀리식 서버: 한 서버 케이스 안에 회원·상품·주문·배달 네 개 모듈이 세로로 쌓여 있는 구조">
  <text x="400" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">모놀리식 서버 — 한 서버에 모든 모듈</text>
  <rect x="260" y="60" width="280" height="430" rx="14" fill="#fff" stroke="#475569" stroke-width="1.8"/>
  <circle cx="510" cy="84" r="8" fill="none" stroke="#475569" stroke-width="1.4"/>
  <line x1="510" y1="80" x2="510" y2="86" stroke="#475569" stroke-width="1.4"/>
  <circle cx="510" cy="106" r="2" fill="#475569"/>
  <circle cx="510" cy="116" r="2" fill="#475569"/>
  <circle cx="510" cy="126" r="2" fill="#475569"/>
  <text x="400" y="118" text-anchor="middle" font-size="13" font-weight="700" fill="#475569">모놀리식 서버</text>
  <rect x="300" y="150" width="200" height="65" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="400" y="190" text-anchor="middle" font-size="18" font-weight="700" fill="#3730a3">회원</text>
  <rect x="300" y="230" width="200" height="65" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="400" y="270" text-anchor="middle" font-size="18" font-weight="700" fill="#3730a3">상품</text>
  <rect x="300" y="310" width="200" height="65" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="400" y="350" text-anchor="middle" font-size="18" font-weight="700" fill="#3730a3">주문</text>
  <rect x="300" y="390" width="200" height="65" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="400" y="430" text-anchor="middle" font-size="18" font-weight="700" fill="#3730a3">배달</text>
  <text x="400" y="510" text-anchor="middle" font-size="13" fill="#6b7280" font-style="italic">한 서버에 모든 모듈이 묶여 따로 떼어내거나 키울 수 없는 구조</text>
</svg>
</div>

*그림 1-2. 모놀리식 쇼핑몰 - 모든 기능이 하나의 서버에*

모든 기능이 한 서버에서 함께 돌아가다 보니, **한 곳의 문제가 곧 전체의 문제가 됩니다.** 주문에 트래픽이 몰리면 회원·상품·배달까지 함께 느려지고, 특정 기능만 확장하고 싶어도 서버 전체를 확장해야 합니다. 또 작은 수정에도 전체를 재배포해야 합니다.

*하나의 서버에 다 모여 있으니, 어젯밤 서버가 전부 같이 멈춘 거였구나.*

## 1.2 마이크로서비스 - 역할을 나눈다

### 1.2.1 백화점 vs 개별 상점

개별 상점 방식은 백화점과 구조 자체가 다릅니다. 각 매장이 독립된 건물로 운영되어, 자신만의 전기·냉방·입구를 가집니다. 덕분에 한 매장에 화재가 발생하거나 문을 닫아도, 다른 매장은 그대로 영업할 수 있습니다.

<div class="svg-figure">
<svg viewBox="0 0 800 410" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="개별 상점: 의류점·전자제품점·식품점·화장품점이 각자 독립된 건물로 운영되는 구조">
  <text x="400" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">개별 상점 — 매장마다 따로 선 건물</text>
  <rect x="50" y="85" width="130" height="9" fill="#0f172a"/>
  <rect x="58" y="94" width="114" height="5" fill="#475569"/>
  <rect x="50" y="99" width="130" height="36" fill="#fff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="115" y="124" text-anchor="middle" font-size="14" font-weight="800" fill="#3730a3" letter-spacing="2">의 류 점</text>
  <rect x="50" y="135" width="130" height="160" fill="#fff" stroke="#475569" stroke-width="1.8"/>
  <rect x="62" y="146" width="106" height="90" fill="#fff" stroke="#4f46e5" stroke-width="1.4"/>
  <line x1="62" y1="168" x2="168" y2="168" stroke="#4f46e5" stroke-width="0.8"/>
  <text x="115" y="162" text-anchor="middle" font-size="8" font-weight="700" fill="#475569" letter-spacing="1">DISPLAY</text>
  <path d="M95 184 L105 178 L110 184 L120 184 L125 178 L135 184 L131 202 L125 200 L125 222 L105 222 L105 200 L99 202 Z" fill="#fff" stroke="#3730a3" stroke-width="1.5" stroke-linejoin="round"/>
  <rect x="95" y="246" width="40" height="49" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <line x1="115" y1="246" x2="115" y2="295" stroke="#475569" stroke-width="1"/>
  <rect x="97" y="250" width="16" height="22" fill="none" stroke="#475569" stroke-width="0.9"/>
  <rect x="117" y="250" width="16" height="22" fill="none" stroke="#475569" stroke-width="0.9"/>
  <circle cx="111" cy="282" r="1.5" fill="#475569"/>
  <circle cx="119" cy="282" r="1.5" fill="#475569"/>
  <rect x="240" y="85" width="130" height="9" fill="#0f172a"/>
  <rect x="248" y="94" width="114" height="5" fill="#475569"/>
  <rect x="240" y="99" width="130" height="36" fill="#fff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="305" y="124" text-anchor="middle" font-size="13" font-weight="800" fill="#3730a3" letter-spacing="1">전자제품점</text>
  <rect x="240" y="135" width="130" height="160" fill="#fff" stroke="#475569" stroke-width="1.8"/>
  <rect x="252" y="146" width="106" height="90" fill="#fff" stroke="#4f46e5" stroke-width="1.4"/>
  <line x1="252" y1="168" x2="358" y2="168" stroke="#4f46e5" stroke-width="0.8"/>
  <text x="305" y="162" text-anchor="middle" font-size="8" font-weight="700" fill="#475569" letter-spacing="1">DISPLAY</text>
  <rect x="275" y="180" width="60" height="38" rx="3" fill="#fff" stroke="#3730a3" stroke-width="1.8"/>
  <rect x="279" y="184" width="52" height="30" rx="1" fill="none" stroke="#3730a3" stroke-width="1"/>
  <line x1="285" y1="222" x2="325" y2="222" stroke="#3730a3" stroke-width="1.8" stroke-linecap="round"/>
  <line x1="293" y1="218" x2="293" y2="222" stroke="#3730a3" stroke-width="1.5"/>
  <line x1="317" y1="218" x2="317" y2="222" stroke="#3730a3" stroke-width="1.5"/>
  <rect x="285" y="246" width="40" height="49" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <line x1="305" y1="246" x2="305" y2="295" stroke="#475569" stroke-width="1"/>
  <rect x="287" y="250" width="16" height="22" fill="none" stroke="#475569" stroke-width="0.9"/>
  <rect x="307" y="250" width="16" height="22" fill="none" stroke="#475569" stroke-width="0.9"/>
  <circle cx="301" cy="282" r="1.5" fill="#475569"/>
  <circle cx="309" cy="282" r="1.5" fill="#475569"/>
  <rect x="430" y="85" width="130" height="9" fill="#0f172a"/>
  <rect x="438" y="94" width="114" height="5" fill="#475569"/>
  <rect x="430" y="99" width="130" height="36" fill="#fff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="495" y="124" text-anchor="middle" font-size="14" font-weight="800" fill="#3730a3" letter-spacing="2">식 품 점</text>
  <rect x="430" y="135" width="130" height="160" fill="#fff" stroke="#475569" stroke-width="1.8"/>
  <rect x="442" y="146" width="106" height="90" fill="#fff" stroke="#4f46e5" stroke-width="1.4"/>
  <line x1="442" y1="168" x2="548" y2="168" stroke="#4f46e5" stroke-width="0.8"/>
  <text x="495" y="162" text-anchor="middle" font-size="8" font-weight="700" fill="#475569" letter-spacing="1">DISPLAY</text>
  <path d="M483 188 Q473 184 475 206 Q478 224 495 226 Q512 224 515 206 Q517 184 507 188 Q501 180 495 188 Q489 180 483 188 Z" fill="#fff" stroke="#3730a3" stroke-width="1.8" stroke-linejoin="round"/>
  <path d="M495 182 Q498 174 505 174" fill="none" stroke="#3730a3" stroke-width="1.8" stroke-linecap="round"/>
  <ellipse cx="503" cy="176" rx="5" ry="3" fill="#3730a3" transform="rotate(-25 503 176)"/>
  <rect x="475" y="246" width="40" height="49" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <line x1="495" y1="246" x2="495" y2="295" stroke="#475569" stroke-width="1"/>
  <rect x="477" y="250" width="16" height="22" fill="none" stroke="#475569" stroke-width="0.9"/>
  <rect x="497" y="250" width="16" height="22" fill="none" stroke="#475569" stroke-width="0.9"/>
  <circle cx="491" cy="282" r="1.5" fill="#475569"/>
  <circle cx="499" cy="282" r="1.5" fill="#475569"/>
  <rect x="620" y="85" width="130" height="9" fill="#0f172a"/>
  <rect x="628" y="94" width="114" height="5" fill="#475569"/>
  <rect x="620" y="99" width="130" height="36" fill="#fff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="685" y="124" text-anchor="middle" font-size="13" font-weight="800" fill="#3730a3" letter-spacing="1">화장품점</text>
  <rect x="620" y="135" width="130" height="160" fill="#fff" stroke="#475569" stroke-width="1.8"/>
  <rect x="632" y="146" width="106" height="90" fill="#fff" stroke="#4f46e5" stroke-width="1.4"/>
  <line x1="632" y1="168" x2="738" y2="168" stroke="#4f46e5" stroke-width="0.8"/>
  <text x="685" y="162" text-anchor="middle" font-size="8" font-weight="700" fill="#475569" letter-spacing="1">DISPLAY</text>
  <rect x="660" y="190" width="18" height="34" rx="2" fill="#fff" stroke="#3730a3" stroke-width="1.6"/>
  <rect x="663" y="176" width="12" height="16" fill="#3730a3"/>
  <rect x="665" y="170" width="8" height="6" fill="#3730a3"/>
  <rect x="690" y="190" width="26" height="34" rx="3" fill="#fff" stroke="#3730a3" stroke-width="1.6"/>
  <rect x="697" y="178" width="12" height="12" fill="#fff" stroke="#3730a3" stroke-width="1.4"/>
  <rect x="699" y="172" width="8" height="6" fill="#3730a3"/>
  <rect x="665" y="246" width="40" height="49" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <line x1="685" y1="246" x2="685" y2="295" stroke="#475569" stroke-width="1"/>
  <rect x="667" y="250" width="16" height="22" fill="none" stroke="#475569" stroke-width="0.9"/>
  <rect x="687" y="250" width="16" height="22" fill="none" stroke="#475569" stroke-width="0.9"/>
  <circle cx="681" cy="282" r="1.5" fill="#475569"/>
  <circle cx="689" cy="282" r="1.5" fill="#475569"/>
  <line x1="30" y1="305" x2="770" y2="305" stroke="#475569" stroke-width="2.5"/>
  <line x1="30" y1="311" x2="770" y2="311" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="5,5"/>
  <text x="400" y="360" text-anchor="middle" font-size="13" fill="#6b7280" font-style="italic">각자 건물·입구·운영을 따로 가진 네 개의 독립 상점</text>
</svg>
</div>

*그림 1-3. 개별 상점 - 각 매장이 독립된 건물로 운영되는 구조*

개별 상점처럼 하나의 큰 서버 대신 **기능별로 서비스를 분리한 구조가 MSA(Microservice Architecture)** 입니다.

<div class="svg-figure">
<svg viewBox="0 0 1020 380" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="마이크로서비스 쇼핑몰: 회원·상품·주문·배달 네 개 서버가 각자 독립적으로 운영되는 구조">
  <text x="510" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">마이크로서비스 — 서비스마다 따로 선 서버</text>
  <rect x="60" y="70" width="200" height="270" rx="12" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <circle cx="240" cy="92" r="6" fill="none" stroke="#475569" stroke-width="1.3"/>
  <line x1="240" y1="89" x2="240" y2="93" stroke="#475569" stroke-width="1.3"/>
  <circle cx="240" cy="112" r="1.7" fill="#475569"/>
  <circle cx="240" cy="120" r="1.7" fill="#475569"/>
  <circle cx="240" cy="128" r="1.7" fill="#475569"/>
  <rect x="90" y="170" width="140" height="80" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="160" y="200" text-anchor="middle" font-size="15" font-weight="700" fill="#3730a3">회원</text>
  <text x="160" y="222" text-anchor="middle" font-size="13" fill="#3730a3">서비스</text>
  <rect x="300" y="70" width="200" height="270" rx="12" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <circle cx="480" cy="92" r="6" fill="none" stroke="#475569" stroke-width="1.3"/>
  <line x1="480" y1="89" x2="480" y2="93" stroke="#475569" stroke-width="1.3"/>
  <circle cx="480" cy="112" r="1.7" fill="#475569"/>
  <circle cx="480" cy="120" r="1.7" fill="#475569"/>
  <circle cx="480" cy="128" r="1.7" fill="#475569"/>
  <rect x="330" y="170" width="140" height="80" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="400" y="200" text-anchor="middle" font-size="15" font-weight="700" fill="#3730a3">상품</text>
  <text x="400" y="222" text-anchor="middle" font-size="13" fill="#3730a3">서비스</text>
  <rect x="540" y="70" width="200" height="270" rx="12" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <circle cx="720" cy="92" r="6" fill="none" stroke="#475569" stroke-width="1.3"/>
  <line x1="720" y1="89" x2="720" y2="93" stroke="#475569" stroke-width="1.3"/>
  <circle cx="720" cy="112" r="1.7" fill="#475569"/>
  <circle cx="720" cy="120" r="1.7" fill="#475569"/>
  <circle cx="720" cy="128" r="1.7" fill="#475569"/>
  <rect x="570" y="170" width="140" height="80" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="640" y="200" text-anchor="middle" font-size="15" font-weight="700" fill="#3730a3">주문</text>
  <text x="640" y="222" text-anchor="middle" font-size="13" fill="#3730a3">서비스</text>
  <rect x="780" y="70" width="200" height="270" rx="12" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <circle cx="960" cy="92" r="6" fill="none" stroke="#475569" stroke-width="1.3"/>
  <line x1="960" y1="89" x2="960" y2="93" stroke="#475569" stroke-width="1.3"/>
  <circle cx="960" cy="112" r="1.7" fill="#475569"/>
  <circle cx="960" cy="120" r="1.7" fill="#475569"/>
  <circle cx="960" cy="128" r="1.7" fill="#475569"/>
  <rect x="810" y="170" width="140" height="80" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="880" y="200" text-anchor="middle" font-size="15" font-weight="700" fill="#3730a3">배달</text>
  <text x="880" y="222" text-anchor="middle" font-size="13" fill="#3730a3">서비스</text>
  <text x="510" y="365" text-anchor="middle" font-size="13" fill="#6b7280" font-style="italic">서로 연결도 의존도 없이 각자 배포·확장되는 네 개의 독립 서버</text>
</svg>
</div>

*그림 1-4. 마이크로서비스 쇼핑몰 - 기능별로 서비스를 분리*

서비스를 분리하면 각 서비스는 독립적으로 배포하고, 독립적으로 확장할 수 있습니다. 그래서 주문 서비스에 문제가 발생해도 다른 서비스는 영향을 받지 않습니다.

## 1.3 시스템과 핵심 과제

문제를 이해했으니, 이제 만들어볼 시스템을 설계해 보겠습니다.

### 1.3.1 쇼핑몰 주문 시스템

이 책의 쇼핑몰 주문 시스템은 4개의 마이크로서비스로 구성됩니다.

| 서비스 | 포트 | 역할 |
|---|---|---|
| 주문 서비스 | 8081 | 주문 생성·조회·취소 (핵심) |
| 상품 서비스 | 8082 | 상품 목록, 재고 조회 및 증감 |
| 회원 서비스 | 8083 | 로그인, JWT 발급, 사용자 조회 |
| 배달 서비스 | 8084 | 배달 생성·조회·취소 |

주문 서비스를 중심으로 상품 서비스와 배달 서비스가 연결됩니다. 사용자가 주문하면 주문 서비스가 상품 서비스의 재고를 차감하고, 배달 서비스에 배달을 생성합니다.

### 1.3.2 서비스 간 요청의 두 가지 방식

각 서비스가 분리되면 서비스 사이의 통신이 별도로 필요합니다. 이 책에서는 두 가지 방식으로 구현합니다.

**방식 1. 직접 호출로 동기적 처리**

첫 번째는 **각 서비스가 다른 서비스를 직접 호출하는 방식**입니다. 주문 서비스가 상품 서비스에 "재고 줄여줘"라고 요청한 후 응답이 올 때까지 기다리고, 응답이 돌아오면 다시 배달 서비스를 호출합니다.

<div class="svg-figure">
<svg viewBox="0 0 1040 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Order가 중심에서 Product와 Delivery에 직접 요청하고 응답을 받는 동기 호출 구조">
  <defs>
    <marker id="c1f8h-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="c1f8h-o" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  </defs>
  <text x="520" y="30" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">동기 REST - Order가 두 서비스를 직접 호출</text>
  <rect x="420" y="60" width="200" height="100" rx="10" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="520" y="98" text-anchor="middle" font-size="22" font-weight="700" fill="#3730a3">Order</text>
  <text x="520" y="130" text-anchor="middle" font-size="14" fill="#3730a3">주문 서비스</text>
  <rect x="120" y="230" width="200" height="100" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="220" y="268" text-anchor="middle" font-size="22" font-weight="700" fill="#0f172a">Product</text>
  <text x="220" y="300" text-anchor="middle" font-size="14" fill="#475569">상품 서비스</text>
  <rect x="720" y="230" width="200" height="100" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="820" y="268" text-anchor="middle" font-size="22" font-weight="700" fill="#0f172a">Delivery</text>
  <text x="820" y="300" text-anchor="middle" font-size="14" fill="#475569">배달 서비스</text>
  <line x1="440" y1="160" x2="300" y2="230" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c1f8h-p)"/>
  <text x="345" y="180" text-anchor="middle" font-size="13" font-weight="600" fill="#4f46e5" font-family="JetBrains Mono, monospace">재고 감소</text>
  <line x1="320" y1="230" x2="460" y2="160" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c1f8h-o)"/>
  <text x="395" y="218" text-anchor="middle" font-size="13" font-weight="600" fill="#3730a3" font-family="JetBrains Mono, monospace">재고 감소 완료</text>
  <line x1="600" y1="160" x2="740" y2="230" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c1f8h-p)"/>
  <text x="695" y="180" text-anchor="middle" font-size="13" font-weight="600" fill="#4f46e5" font-family="JetBrains Mono, monospace">배달 생성</text>
  <line x1="720" y1="230" x2="580" y2="160" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c1f8h-o)"/>
  <text x="645" y="218" text-anchor="middle" font-size="13" font-weight="600" fill="#3730a3" font-family="JetBrains Mono, monospace">배달 생성 완료</text>
  <text x="520" y="350" text-anchor="middle" font-size="13" fill="#6b7280" font-style="italic">Order가 두 서비스를 직접 호출하고 응답을 받는다</text>
</svg>
</div>

*그림 1-5. 동기 REST - Order가 두 서비스를 직접 호출*

이 방식은 구현이 단순합니다. 다만 호출한 서비스가 응답할 때까지 멈춰 있는 동기적 호출 방식이라, 한 단계가 지연되면 다음 단계도 지연됩니다.

**방식 2. 메시지로 비동기 전환**

다음은 서비스끼리 직접 호출하지 않고, **메시지로 요청을 주고받는 방식**입니다. 한 서비스가 메시지를 발행하면, 다른 서비스가 메시지를 받아서 처리합니다.

<div class="svg-figure">
<svg viewBox="0 0 1080 480" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="중앙 지휘자가 명령하고 받는다. 서비스끼리는 서로 호출하지 않는다.">
  <defs>
    <marker id="c1f9c-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="c1f9c-o" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="540" y="36" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">비동기 메시지 - 서비스를 분리</text>
  <rect x="340" y="80" width="400" height="120" rx="14" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="540" y="125" text-anchor="middle" font-size="24" font-weight="700" fill="#3730a3">Orchestrator</text>
  <text x="540" y="155" text-anchor="middle" font-size="14" fill="#3730a3">중앙 지휘자</text>
  <text x="540" y="180" text-anchor="middle" font-size="12" fill="#475569">전체 워크플로우 추적 · 명령 발행</text>
  <line x1="480" y1="205" x2="480" y2="270" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c1f9c-p)"/>
  <text x="455" y="245" text-anchor="end" font-size="14" font-weight="600" fill="#4f46e5" font-family="JetBrains Mono, monospace">command</text>
  <text x="455" y="263" text-anchor="end" font-size="11" fill="#4f46e5" font-style="italic">"이것 해라"</text>
  <line x1="600" y1="270" x2="600" y2="207" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c1f9c-o)"/>
  <text x="625" y="245" text-anchor="start" font-size="14" font-weight="600" fill="#3730a3" font-family="JetBrains Mono, monospace">event</text>
  <text x="625" y="263" text-anchor="start" font-size="11" fill="#3730a3" font-style="italic">"이렇게 됐다"</text>
  <rect x="60" y="275" width="960" height="160" rx="14" fill="#fff" stroke="#cbd5e1" stroke-width="1.6" stroke-dasharray="4,3"/>
  <text x="540" y="298" text-anchor="middle" font-size="13" font-weight="700" fill="#64748b">Microservices — 서비스끼리는 서로 호출하지 않는다</text>
  <rect x="100" y="315" width="260" height="100" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="230" y="352" text-anchor="middle" font-size="20" font-weight="700" fill="#0f172a">Order</text>
  <text x="230" y="378" text-anchor="middle" font-size="13" fill="#475569">주문 서비스</text>
  <text x="230" y="400" text-anchor="middle" font-size="11" fill="#6b7280">자기 일만 + 결과 보고</text>
  <rect x="410" y="315" width="260" height="100" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="540" y="352" text-anchor="middle" font-size="20" font-weight="700" fill="#0f172a">Product</text>
  <text x="540" y="378" text-anchor="middle" font-size="13" fill="#475569">상품 서비스</text>
  <text x="540" y="400" text-anchor="middle" font-size="11" fill="#6b7280">자기 일만 + 결과 보고</text>
  <rect x="720" y="315" width="260" height="100" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="850" y="352" text-anchor="middle" font-size="20" font-weight="700" fill="#0f172a">Delivery</text>
  <text x="850" y="378" text-anchor="middle" font-size="13" fill="#475569">배달 서비스</text>
  <text x="850" y="400" text-anchor="middle" font-size="11" fill="#6b7280">자기 일만 + 결과 보고</text>
  <text x="540" y="462" text-anchor="middle" font-size="13" fill="#6b7280" font-style="italic">Orchestrator가 명령을 내리고 결과를 받아 다음 단계를 결정 · 서비스끼리 직접 호출 없음</text>
</svg>
</div>

*그림 1-6. 비동기 메시지 - 서비스를 분리하는 구조*

발행한 서비스는 응답을 기다리지 않고 바로 다음 작업으로 넘어가므로, 한 서비스에서 응답이 지연되어도 다른 서비스는 지연되지 않습니다.

두 방식을 학습하며 각각의 장단점을 알아보겠습니다.

### 1.3.3 분산 트랜잭션 — 이 책의 핵심 과제

서비스를 분리하면 곧장 새로운 문제가 생깁니다. 모놀리식에서는 주문·재고·배달을 **하나의 트랜잭션으로 묶을 수 있기 때문에** 중간에 실패하면 전부 **자동 롤백**됩니다.

그런데 MSA에서는 각 서비스가 **독립된 데이터베이스**를 가집니다. 트랜잭션은 하나의 데이터베이스 안에서만 동작하므로, 서로 다른 DB에 걸친 작업은 하나의 트랜잭션으로 묶을 수 없습니다. 이렇게 여러 DB에 걸친 작업을 하나로 묶어야 하는 상황을 **분산 트랜잭션**이라고 합니다.

<div class="svg-figure">
<svg viewBox="0 0 880 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="서비스별 독립 데이터베이스: 각 서비스가 자기 DB만 가지고 트랜잭션으로 묶을 수 없는 구조">
  <defs>
    <marker id="c1f7-g" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="440" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">서비스별 독립 데이터베이스</text>
  <rect x="50" y="55" width="240" height="285" rx="10" fill="#fff" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="6,4"/>
  <rect x="100" y="85" width="140" height="70" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="170" y="127" text-anchor="middle" font-size="14" font-weight="700" fill="#3730a3">주문 서비스</text>
  <line x1="170" y1="155" x2="170" y2="225" stroke="#475569" stroke-width="1.6" marker-end="url(#c1f7-g)"/>
  <ellipse cx="170" cy="245" rx="55" ry="12" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <path d="M115 245 L115 295 Q115 307 170 307 Q225 307 225 295 L225 245" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <ellipse cx="170" cy="295" rx="55" ry="12" fill="none" stroke="#475569" stroke-width="1.2" stroke-dasharray="2,2"/>
  <text x="170" y="335" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">주문 DB</text>
  <rect x="320" y="55" width="240" height="285" rx="10" fill="#fff" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="6,4"/>
  <rect x="370" y="85" width="140" height="70" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="440" y="127" text-anchor="middle" font-size="14" font-weight="700" fill="#3730a3">상품 서비스</text>
  <line x1="440" y1="155" x2="440" y2="225" stroke="#475569" stroke-width="1.6" marker-end="url(#c1f7-g)"/>
  <ellipse cx="440" cy="245" rx="55" ry="12" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <path d="M385 245 L385 295 Q385 307 440 307 Q495 307 495 295 L495 245" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <ellipse cx="440" cy="295" rx="55" ry="12" fill="none" stroke="#475569" stroke-width="1.2" stroke-dasharray="2,2"/>
  <text x="440" y="335" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">상품 DB</text>
  <rect x="590" y="55" width="240" height="285" rx="10" fill="#fff" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="6,4"/>
  <rect x="640" y="85" width="140" height="70" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="710" y="127" text-anchor="middle" font-size="14" font-weight="700" fill="#3730a3">배달 서비스</text>
  <line x1="710" y1="155" x2="710" y2="225" stroke="#475569" stroke-width="1.6" marker-end="url(#c1f7-g)"/>
  <ellipse cx="710" cy="245" rx="55" ry="12" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <path d="M655 245 L655 295 Q655 307 710 307 Q765 307 765 295 L765 245" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <ellipse cx="710" cy="295" rx="55" ry="12" fill="none" stroke="#475569" stroke-width="1.2" stroke-dasharray="2,2"/>
  <text x="710" y="335" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">배달 DB</text>
  <line x1="30" y1="190" x2="850" y2="190" stroke="#475569" stroke-width="1.6" stroke-dasharray="6,4"/>
  <rect x="318" y="180" width="244" height="22" fill="#fff"/>
  <text x="440" y="196" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">트랜잭션으로 묶을 수 없다.</text>
  <text x="440" y="388" text-anchor="middle" font-size="13" fill="#6b7280" font-style="italic">각 서비스가 자기 DB만 가지고 서로의 DB에 직접 접근하지 못한다</text>
</svg>
</div>

*그림 1-7. 서비스별 독립 데이터베이스*

:::term-box
**분산 트랜잭션(Distributed Transaction)이란?** 여러 독립된 데이터베이스에 걸친 작업을 하나의 논리적 단위로 처리해야 하는 상황입니다. MSA에서는 서비스마다 DB가 분리되어 있으므로 단일 트랜잭션이 불가능하고, 별도의 전략이 필요합니다.
:::

**오픈이**: "선배님, 재고는 줄였는데 배달이 실패하면 줄인 재고를 원복해야 하잖아요. 이런 걸 되돌리는 방법은 없나요?"

**선배**: "자동으로 안 되니 직접 되돌려야 해요. 재고를 줄였으면 원복하고, 배달을 만들었으면 취소하고. 한 단계씩 거꾸로 되돌리는 거예요. 이걸 **보상 트랜잭션**이라고 해요."

:::term-box
**보상 트랜잭션(Compensating Transaction)이란?** 중간에 실패가 나면 이미 끝낸 작업을 역순으로 돌려 원래 상태로 되돌리는 방법입니다.
:::

서비스를 분리하고, 분산 트랜잭션을 해결하는 것이 MSA의 과제입니다.

## 1.4 이 책의 학습 흐름

이 책은 하나의 시스템이 단계별로 진화하는 여정입니다. 각 챕터는 이전 챕터의 한계를 해결하는 방식으로 진행됩니다.

<div class="svg-figure">
<svg viewBox="0 0 720 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="산 등반으로 본 학습 흐름. REST 보상 트랜잭션, DDD 클린 K8s, Kafka 지휘자, WebSocket Push 순으로 네 캠프를 올라 정상에서 완성한다. 각 캠프에 한 줄 요약이 있다.">
  <defs>
    <marker id="mt" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#4f46e5"/></marker>
  </defs>
  <polygon points="14,372 195,100 332,185 476,66 590,30 706,372" fill="#eef2ff" stroke="#dfe4ff" stroke-width="1.1"/>
  <polygon points="94,372 274,178 420,238 556,120 634,96 706,372" fill="#f1f5f9" stroke="#e6ebf2" stroke-width="0.9"/>
  <polygon points="590,30 574,58 590,52 606,60 590,30" fill="#fff" stroke="#cbd5e1" stroke-width="0.7"/>
  <line x1="8" y1="372" x2="712" y2="372" stroke="#cbd5e1" stroke-width="1.3"/>
  <path d="M50,364 Q108,344 152,316 Q200,288 192,268 Q246,228 324,218 Q388,210 378,188 Q432,148 504,135 Q560,124 548,104 Q588,80 634,66" fill="none" stroke="#4f46e5" stroke-width="2.6" stroke-linecap="round" stroke-dasharray="2,7"/>
  <path d="M634,66 L660,52" fill="none" stroke="#4f46e5" stroke-width="2.6" stroke-linecap="round" marker-end="url(#mt)"/>
  <circle cx="152" cy="316" r="6" fill="#fff" stroke="#4f46e5" stroke-width="2.2"/>
  <line x1="152" y1="310" x2="152" y2="293" stroke="#475569" stroke-width="1.6"/><path d="M152,293 L170,298 L152,303 Z" fill="#ff7849"/>
  <circle cx="324" cy="218" r="6" fill="#fff" stroke="#4f46e5" stroke-width="2.2"/>
  <line x1="324" y1="212" x2="324" y2="195" stroke="#475569" stroke-width="1.6"/><path d="M324,195 L342,200 L324,205 Z" fill="#ff7849"/>
  <circle cx="504" cy="135" r="6" fill="#fff" stroke="#4f46e5" stroke-width="2.2"/>
  <line x1="504" y1="129" x2="504" y2="112" stroke="#475569" stroke-width="1.6"/><path d="M504,112 L522,117 L504,122 Z" fill="#ff7849"/>
  <circle cx="634" cy="66" r="6" fill="#fff" stroke="#4f46e5" stroke-width="2.4"/>
  <line x1="634" y1="60" x2="634" y2="40" stroke="#475569" stroke-width="1.8"/><path d="M634,40 L654,46 L634,52 Z" fill="#4f46e5"/>
  <text x="634" y="32" text-anchor="middle" font-size="12" font-weight="800" fill="#3730a3">정상</text>
  <line x1="152" y1="322" x2="152" y2="332" stroke="#cbd5e1" stroke-width="1.2"/>
  <rect x="60" y="332" width="216" height="46" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <circle cx="78" cy="348" r="9" fill="#ff7849"/><text x="78" y="352" text-anchor="middle" font-size="10" font-weight="800" fill="#fff">1</text>
  <text x="94" y="353" font-size="14" font-weight="800" fill="#0f172a">REST + 보상 트랜잭션</text>
  <text x="72" y="370" font-size="11.5" fill="#6b7280">서비스 직접 호출, 실패 시 보상</text>
  <line x1="324" y1="224" x2="324" y2="234" stroke="#cbd5e1" stroke-width="1.2"/>
  <rect x="232" y="234" width="216" height="46" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <circle cx="250" cy="250" r="9" fill="#ff7849"/><text x="250" y="254" text-anchor="middle" font-size="10" font-weight="800" fill="#fff">2</text>
  <text x="266" y="255" font-size="14" font-weight="800" fill="#0f172a">DDD · 클린 아키텍처</text>
  <text x="244" y="272" font-size="11.5" fill="#6b7280">도메인·클린으로 구조 재설계</text>
  <line x1="504" y1="141" x2="504" y2="151" stroke="#cbd5e1" stroke-width="1.2"/>
  <rect x="404" y="151" width="232" height="46" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <circle cx="422" cy="167" r="9" fill="#ff7849"/><text x="422" y="171" text-anchor="middle" font-size="10" font-weight="800" fill="#fff">3</text>
  <text x="438" y="172" font-size="14" font-weight="800" fill="#0f172a">Kafka + 지휘자(Saga)</text>
  <text x="416" y="189" font-size="11.5" fill="#6b7280">메시지로 비동기 전환, 지휘자가 조율</text>
  <line x1="634" y1="72" x2="634" y2="82" stroke="#cbd5e1" stroke-width="1.2"/>
  <rect x="512" y="82" width="200" height="46" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <circle cx="530" cy="98" r="9" fill="#ff7849"/><text x="530" y="102" text-anchor="middle" font-size="10" font-weight="800" fill="#fff">4</text>
  <text x="546" y="103" font-size="14" font-weight="800" fill="#3730a3">WebSocket Push</text>
  <text x="524" y="120" font-size="11.5" fill="#6b7280">사용자에게 즉시 알림 (완성)</text>
</svg>
</div>

*그림 1-8. 이 책의 학습 흐름*

각 챕터에서 다루는 내용은 다음과 같습니다.

- 챕터 2에서는 각 서비스가 동기적으로 직접 호출하고, 중간에 실패하면 보상 트랜잭션으로 되돌립니다.
- 챕터 3에서는 도메인과 클린 아키텍처를 중심으로 서비스 구조를 다시 설계합니다.
- 챕터 4에서는 동기 방식을 메시지를 통한 비동기 방식으로 전환합니다.
- 챕터 5에서는 처리가 끝난 순간 사용자에게 실시간으로 알립니다.

이 책은 코드 작성보다 전체적인 개념과 흐름을 이해하고, 단계별로 실습하며 익히는 것을 목표로 하고 있습니다. 한 단계씩 학습하며 MSA의 큰 흐름을 따라가 보겠습니다.

:::remember
**이것만은 기억하자**

- **모놀리식**은 처음에는 단순하지만, 서비스가 커지면 배포·장애·확장 문제가 생깁니다.
- **마이크로서비스**는 기능별로 서비스를 분리하여 각자 독립적으로 배포하고 확장할 수 있게 합니다.
- 각 서비스의 DB가 분리되어 있어 단일 트랜잭션으로 묶을 수 없습니다. 이것이 MSA의 핵심 과제인 **분산 트랜잭션**입니다.
- 분산 트랜잭션은 서비스끼리 **직접 호출·보상**하는 방식과, **메시지로 비동기 통신**하는 방식으로 학습합니다.
:::



---


# 챕터 2. 동기식 MSA 구현 - 서비스를 연결하다

**오픈이**: "선배님, 그럼 어떤 것부터 시작하면 될까요?"

**선배**: "우선 회원, 주문, 상품, 배달, 이렇게 기능별로 서비스를 나누는 거예요. 그리고 서비스끼리 전화를 거는 것처럼 직접 호출하는 거죠."

방향이 정해졌으니 이제 만들어 보겠습니다.

이번 챕터의 핵심은 주문 서비스입니다. 주문 서비스에서 주문 요청이 들어오면, 주문 서비스가 상품 서비스와 배달 서비스를 직접 호출하고 응답하는 흐름을 따라가 보겠습니다.

<div class="svg-figure">
<svg viewBox="0 0 1020 480" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="챕터 2 한눈에 보기: 1단계는 클라이언트가 User에 로그인하여 JWT를 받고, 2단계는 클라이언트가 Order에 주문을 요청하면 Order가 Product와 Delivery를 동기 호출하고 응답을 받은 뒤 클라이언트에 주문 완료를 응답하는 흐름. 모든 서비스는 Docker Compose로 묶여 있음">
  <defs>
    <marker id="c2f0-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="510" y="26" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">챕터 2 한눈에 보기 — 로그인부터 주문까지</text>
  <rect x="230" y="50" width="760" height="400" rx="14" fill="none" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="6,4"/>
  <text x="250" y="70" font-size="11" font-weight="700" fill="#3730a3">Docker Compose · msa-network</text>
  <text x="40" y="95" font-size="12" font-weight="700" fill="#475569">1단계 — 로그인</text>
  <rect x="40" y="105" width="140" height="70" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="110" y="135" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">Client</text>
  <text x="110" y="157" text-anchor="middle" font-size="11" fill="#6b7280">사용자</text>
  <rect x="380" y="105" width="180" height="70" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="470" y="135" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">User</text>
  <text x="470" y="157" text-anchor="middle" font-size="11" fill="#6b7280">:8083 회원</text>
  <text x="40" y="225" font-size="12" font-weight="700" fill="#475569">2단계 — 주문 생성</text>
  <rect x="40" y="235" width="140" height="70" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="110" y="265" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">Client</text>
  <text x="110" y="287" text-anchor="middle" font-size="11" fill="#6b7280">사용자</text>
  <rect x="380" y="235" width="180" height="70" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="470" y="265" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">Order</text>
  <text x="470" y="287" text-anchor="middle" font-size="11" fill="#3730a3">:8081 주문</text>
  <rect x="680" y="130" width="180" height="70" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="770" y="160" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">Product</text>
  <text x="770" y="182" text-anchor="middle" font-size="11" fill="#6b7280">:8082 상품</text>
  <rect x="680" y="340" width="180" height="70" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="770" y="370" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">Delivery</text>
  <text x="770" y="392" text-anchor="middle" font-size="11" fill="#6b7280">:8084 배달</text>
  <line x1="180" y1="125" x2="378" y2="125" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c2f0-i)"/>
  <text x="279" y="118" text-anchor="middle" font-size="12" font-weight="600" fill="#4f46e5">1. 로그인 (POST /login)</text>
  <line x1="378" y1="155" x2="182" y2="155" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c2f0-i)"/>
  <text x="280" y="170" text-anchor="middle" font-size="12" font-weight="600" fill="#3730a3">2. JWT 응답</text>
  <line x1="180" y1="255" x2="378" y2="255" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c2f0-i)"/>
  <text x="279" y="248" text-anchor="middle" font-size="12" font-weight="600" fill="#4f46e5">3. 주문 생성 (JWT 첨부)</text>
  <line x1="560" y1="245" x2="678" y2="165" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c2f0-i)"/>
  <text x="619" y="190" text-anchor="middle" font-size="12" font-weight="600" fill="#4f46e5">4. 재고 차감</text>
  <line x1="678" y1="185" x2="562" y2="265" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c2f0-i)"/>
  <text x="619" y="240" text-anchor="middle" font-size="12" font-weight="600" fill="#3730a3">5. 차감 응답</text>
  <line x1="560" y1="285" x2="678" y2="365" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c2f0-i)"/>
  <text x="619" y="315" text-anchor="middle" font-size="12" font-weight="600" fill="#4f46e5">6. 배달 생성</text>
  <line x1="678" y1="385" x2="562" y2="305" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c2f0-i)"/>
  <text x="619" y="355" text-anchor="middle" font-size="12" font-weight="600" fill="#3730a3">7. 생성 응답</text>
  <line x1="378" y1="285" x2="182" y2="285" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c2f0-i)"/>
  <text x="280" y="305" text-anchor="middle" font-size="12" font-weight="600" fill="#3730a3">8. 주문 완료 응답</text>
</svg>
</div>

*그림 2-1. 챕터 2 한눈에 보기 - 로그인부터 주문까지*

:::goal
**이번 챕터가 끝나면**

- 여러 서비스를 **REST**로 직접 호출해 주문 흐름을 동기로 잇는 구조를 이해할 수 있습니다.
- 실패 시 앞 작업을 되돌리는 **보상 트랜잭션**을 이해할 수 있습니다.
:::

::::prep
**준비하기**. 실습 시작 전 한 번만 설정

### 1. 소스 코드 클론

**[터미널] 레포 클론**
```bash
git clone https://github.com/metacoding-12-msa/ex01.git
cd ex01
```

### 2. 파일 구조

**ex01 디렉토리**
```text
ex01/
├── user/               # 포트 8083
├── product/            # 포트 8082
├── order/              # 포트 8081
├── delivery/           # 포트 8084
└── docker-compose.yml  # 전체 서비스 실행
```

각 서비스 내부는 동일한 구조입니다. 주문 서비스 기준으로 보여드리며, 회원/상품/배달 서비스도 같은 구조입니다.

**주문 서비스 패키지 구조**
```text
src/main/java/com/metacoding/order/
├── OrderApplication.java                 # [참고]
├── core/
│   ├── config/
│   │   ├── WebConfig.java                # [참고] JWT 필터 등록
│   │   └── RestClientConfig.java         # [참고] JWT 헤더 전달 인터셉터
│   ├── filter/
│   │   └── JwtAuthenticationFilter.java  # [참고] JWT 인가 필터
│   ├── handler/
│   │   ├── GlobalExceptionHandler.java   # [참고] 전역 예외 처리
│   │   └── ex/                           # 커스텀 예외 (Exception400~500)
│   └── util/
│       ├── JwtProvider.java              # [참고] JWT 파싱/검증
│       ├── JwtUtil.java                  # [참고] JWT 생성
│       └── Resp.java                     # [참고] 표준 응답 래퍼
├── orders/
│   ├── Order.java                        # [참고] JPA 엔티티
│   ├── OrderStatus.java                  # [참고] 주문 상태 enum
│   ├── OrderController.java              # [참고] REST 컨트롤러
│   ├── OrderService.java                 # [작성] 비즈니스 로직
│   ├── OrderRepository.java              # [참고] Spring Data JPA
│   └── OrderRequest.java / OrderResponse.java  # [참고]
└── adapter/                              # 주문 서비스에만 존재
    ├── ProductClient.java                # [참고] 상품 서비스 호출
    ├── DeliveryClient.java               # [참고] 배달 서비스 호출
    └── dto/                              # 어댑터용 DTO (ProductRequest, DeliveryRequest)
Dockerfile                                # [참고] Docker 이미지 빌드
```

:::note
**회원/상품/배달 서비스는 `adapter/` 패키지와 `RestClientConfig`가 없고, 나머지 구조는 동일합니다.**
:::

### 3. 실습 환경

| 도구 | 용도 | 비고 |
|------|------|------|
| **Docker Desktop** | 4개 서비스를 컨테이너로 실행 | https://www.docker.com/products/docker-desktop/ |
| **Hoppscotch** | API 호출 결과 확인 | https://hoppscotch.io/ (설치 불필요, 브라우저 확장만 추가) |

### 4. 실습 순서

1. 공통 설정(JWT·표준 응답·예외 처리)이 담긴 `core/` 패키지 살펴보기
2. 회원·상품·배달 서비스의 핵심 코드 살펴보기
3. 주문 서비스에 RestClient + 보상 트랜잭션 작성하기
4. Docker Compose로 4개 서비스를 한 번에 띄우고 시나리오 3개 검증하기
::::

## 2.1 공통 설정 - 모든 서비스가 공유하는 뼈대

각 서비스는 **Spring Boot**로 만들어진 독립 프로젝트입니다. 서버가 분리되어 **세션을 공유할 수 없으므로** **JWT 토큰**으로 인증합니다.

4개 서비스가 공통으로 쓰는 **JWT 인증·표준 응답·예외 처리**는 `core/` 패키지에 모아 둡니다. 각 컴포넌트의 역할은 다음과 같습니다.

| 컴포넌트 | 역할 |
|---|---|
| **JwtAuthenticationFilter** | 매 요청마다 JWT를 검증하고 사용자 정보를 컨트롤러로 전달합니다. |
| **JwtUtil / JwtProvider** | JwtUtil은 토큰을 발급하고 검증하는 핵심 로직이고, JwtProvider는 요청 헤더에서 토큰을 꺼내 JwtUtil에 넘깁니다. |
| **Resp** | 모든 API 응답을 동일한 형태로 통일하는 래퍼입니다. |
| **GlobalExceptionHandler** | 전역에서 발생한 예외를 잡아 일관된 에러 응답으로 변환합니다. |
| **WebConfig** | JWT 필터를 인증이 필요한 경로에 등록합니다. |

주문 서비스로 가기 전, 회원·상품·배달 서비스는 참고 코드라 클래스 단위로 간단히 살펴봅니다. 자세한 구현은 완성 레포(GitHub)를 참고하세요.

## 2.2 회원 서비스 - JWT로 로그인하다

회원 서비스는 **로그인과 사용자 조회**를 담당합니다. 사용자가 `POST /login`으로 아이디와 비밀번호를 보내면, 회원 서비스가 DB에서 조회하고 비밀번호를 검증합니다. 검증에 성공하면 **JWT 토큰**을 응답 데이터에 담아 돌려줍니다. 이 토큰이 이후 모든 서비스 요청의 **인증 수단**이 됩니다.

| HTTP 메서드 | 경로 | 기능 |
|---|---|---|
| POST | /login | 로그인 (JWT 발급) |
| GET | /api/users/{userId} | 사용자 조회 |

### 2.2.1 클래스 구성

회원 서비스의 로그인과 사용자 조회를 다음 다섯 클래스가 처리합니다.

| 클래스 | 역할 |
|---|---|
| **User** | 사용자 정보를 담는 엔티티입니다. |
| **UserRepository** | 사용자 데이터를 DB에서 조회·저장합니다. |
| **UserRequest / UserResponse** | 회원 API의 요청과 응답 형식을 정의합니다. |
| **UserController** | 로그인과 사용자 조회 API를 제공합니다. |
| **UserService** | 로그인 시 비밀번호를 검증하고 JWT를 발급하며, 사용자 조회 요청을 처리합니다. |

## 2.3 상품 서비스 - 재고를 관리하다

상품 서비스는 **상품 목록 조회와 재고 증감**을 담당합니다. 주문 서비스가 주문을 생성할 때 **재고 감소 API**를 호출하고, 주문이 취소되거나 실패하면 **재고 증가 API**로 되돌립니다.

| HTTP 메서드 | 경로 | 기능 |
|---|---|---|
| GET | /api/products/{productId} | 상품 조회 |
| PUT | /api/products/{productId}/decrease | 재고 감소 |
| PUT | /api/products/{productId}/increase | 재고 증가 |

### 2.3.1 클래스 구성

상품 조회와 재고 증감을 다음 다섯 클래스가 처리합니다.

| 클래스 | 역할 |
|---|---|
| **Product** | 상품 정보를 담는 엔티티이며, 재고 증감 로직을 자기 안에 둡니다. |
| **ProductRepository** | 상품 데이터를 DB에서 조회·저장합니다. |
| **ProductRequest / ProductResponse** | 상품 API의 요청과 응답 형식을 정의합니다. |
| **ProductController** | 상품 조회와 재고 증감 API를 제공합니다. |
| **ProductService** | 재고 감소 전 상품 존재·재고·가격을 검증한 뒤 재고를 줄이거나 늘립니다. |

## 2.4 배달 서비스 - 배달을 생성하고 취소하다

배달 서비스는 **배달 생성과 취소**를 담당합니다. 회원이나 상품 서비스와 달리, 주문과 배달에는 현재 진행 상황을 나타내는 **상태(`status`) 값**이 있습니다. 대기 상태인 `PENDING`으로 시작해 처리가 완료되면 `COMPLETED`, 취소되면 `CANCELLED`로 바뀝니다.

| HTTP 메서드 | 경로 | 기능 |
|---|---|---|
| POST | /api/deliveries | 배달 생성 |
| GET | /api/deliveries/{deliveryId} | 배달 조회 |
| PUT | /api/deliveries/{orderId} | 배달 취소 |

### 2.4.1 클래스 구성

배달 생성과 취소를 다음 여섯 클래스가 처리합니다.

| 클래스 | 역할 |
|---|---|
| **Delivery** | 배달 정보와 현재 상태(PENDING / COMPLETED / CANCELLED)를 담는 엔티티입니다. |
| **DeliveryStatus** | 배달 상태(대기·완료·취소)를 정의하는 열거형입니다. |
| **DeliveryRepository** | 배달 데이터를 DB에서 조회·저장합니다. |
| **DeliveryRequest / DeliveryResponse** | 배달 API의 요청과 응답 형식을 정의합니다. |
| **DeliveryController** | 배달 생성·조회·취소 API를 제공합니다. |
| **DeliveryService** | 배달 생성 시 완료까지 처리하며, 조회와 취소도 처리합니다. |

## 2.5 주문 서비스 - 보상 트랜잭션의 현장

주문 서비스는 **주문 생성·조회·취소**를 담당합니다. 주문 요청 처리를 위해 상품·배달 서비스를 직접 호출하는 흐름의 중심에 있습니다.

| HTTP 메서드 | 경로 | 기능 |
|---|---|---|
| POST | /api/orders | 주문 생성 |
| GET | /api/orders/{orderId} | 주문 조회 |
| PUT | /api/orders/{orderId} | 주문 취소 |

### 2.5.1 클래스 구성

주문 생성과 보상 트랜잭션을 다음 여섯 클래스가 처리합니다.

| 클래스 | 역할 |
|---|---|
| **Order** | 주문 정보와 현재 상태(PENDING / COMPLETED / CANCELLED)를 담는 엔티티입니다. |
| **OrderStatus** | 주문 상태(대기·완료·취소)를 정의하는 열거형입니다. |
| **OrderRepository** | 주문 데이터를 DB에서 조회·저장합니다. |
| **OrderRequest / OrderResponse** | 주문 API의 요청과 응답 형식을 정의합니다. |
| **OrderController** | 주문 생성·조회·취소 API를 제공합니다. |
| **OrderService** | **[작성]** 주문 생성 시 보상 트랜잭션을 수행하며, 조회와 취소도 처리합니다. |

### 2.5.2 보상 트랜잭션 흐름

서비스의 구조를 파악했으니, 이제 주문 서비스의 진짜 역할을 살펴봅니다. 주문 요청이 들어오면 주문 서비스는 상품·배달 서비스를 호출합니다. 이때 작업이 실패하면, **주문 서비스가 직접 보상 트랜잭션을 실행**해 원래 상태로 되돌립니다.

어느 단계에서 실패하면 무엇을 되돌려야 하는지 먼저 그려 보겠습니다.

| 단계 | 동작 | 실패 시 보상 |
|---|---|---|
| 1 | 재고 감소 (상품 서비스) | 없음 (아직 진행 안 함) |
| 2 | 배달 생성 (배달 서비스) | 재고 복구 (1단계 되돌리기) |
| 3 | 주문 완료 | 배달 취소 + 재고 복구 (2, 1단계 되돌리기) |
| 4 | 성공 응답 반환 | — |

예를 들어 2단계 배달 생성에서 실패하면, 이미 줄어든 재고 한 단계만 되돌리면 됩니다. 3단계에서 실패하면 배달 취소와 재고 복구를 모두 되돌립니다. 진행한 만큼만 역순으로 되돌리려면, **어디까지 갔는지를 코드에서 기록**해 둬야 합니다.

<div class="svg-figure">
<svg viewBox="0 0 880 460" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="주문 실패 시 보상 트랜잭션 시퀀스: 배달 실패 후 재고 복구와 주문 트랜잭션 롤백을 역순으로 실행">
  <defs>
    <marker id="c2f2-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="c2f2-o" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="440" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">주문 실패 시 보상 트랜잭션 — 배달 실패 후 역순 복구</text>
  <rect x="80" y="60" width="180" height="50" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="170" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#3730a3">Order</text>
  <rect x="350" y="60" width="180" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="440" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Product</text>
  <rect x="620" y="60" width="180" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="710" y="92" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Delivery</text>
  <line x1="170" y1="110" x2="170" y2="430" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="440" y1="110" x2="440" y2="430" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="710" y1="110" x2="710" y2="430" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="170" y1="150" x2="438" y2="150" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c2f2-i)"/>
  <text x="304" y="142" text-anchor="middle" font-size="13" font-weight="600" fill="#4f46e5">1. 재고 차감 요청</text>
  <line x1="440" y1="200" x2="172" y2="200" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c2f2-i)"/>
  <text x="306" y="192" text-anchor="middle" font-size="13" font-weight="600" fill="#4f46e5">2. 차감 성공 응답</text>
  <line x1="170" y1="255" x2="708" y2="255" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c2f2-o)"/>
  <text x="439" y="247" text-anchor="middle" font-size="13" font-weight="600" fill="#3730a3">3. 배달 생성 요청 → 실패</text>
  <line x1="170" y1="320" x2="438" y2="320" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c2f2-o)"/>
  <text x="304" y="312" text-anchor="middle" font-size="13" font-weight="600" fill="#3730a3">4. 재고 복구 요청 (보상)</text>
  <path d="M170 380 L230 380 L230 398 L172 398" fill="none" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c2f2-o)"/>
  <text x="240" y="393" text-anchor="start" font-size="13" font-weight="600" fill="#3730a3">5. 주문 트랜잭션 롤백</text>
  <text x="440" y="448" text-anchor="middle" font-size="13" fill="#6b7280" font-style="italic">실패가 발생하면 이미 진행된 단계를 역순으로 보상 (점선)</text>
</svg>
</div>

*그림 2-2. 주문 실패 시 보상 트랜잭션 흐름*

### 2.5.3 adapter - 외부 서비스 호출 설정

`adapter/` 폴더에는 외부 서비스를 호출하는 **클라이언트** 두 개가 있습니다.

**RestClientConfig**가 모든 외부 호출에 **JWT 토큰을 자동으로 실어** 줍니다. 그리고 **ProductClient**와 **DeliveryClient**가 각자 상품 서비스와 배달 서비스로 요청을 보냅니다.

| 클래스 | 역할 |
|---|---|
| **RestClientConfig** | RestClient에 인터셉터를 등록하여 외부 호출 시 JWT를 자동 전달합니다. |
| **ProductClient** | 상품 서비스의 decreaseQuantity(재고 감소)와 increaseQuantity(재고 복구)를 호출합니다. |
| **DeliveryClient** | 배달 서비스의 createDelivery(배달 생성)와 cancelDelivery(배달 취소)를 호출합니다. |

### 2.5.4 OrderService - 보상 트랜잭션의 핵심

이제 이번 챕터의 핵심입니다. **보상 트랜잭션 패턴**을 직접 구현합니다. 코드를 읽을 때 `productDecreased`와 `deliveryCreated` **두 플래그를 추적**하면서 읽어보세요. 단계가 성공할 때마다 플래그를 `true`로 바꾸고, 실패 시 catch 블록에서는 **`true`로 표시된 단계만 역순으로 되돌립니다**.

`orders/OrderService.java`를 열고 아래 메서드를 작성합니다.

**[실습 1] orders/OrderService.java. createOrder - 보상 트랜잭션 핵심**
```java
@Transactional
public OrderResponse createOrder(int userId, int productId,
        int quantity, Long price, String address) {
    // 보상트랜잭션을 위한 변수 선언
    boolean productDecreased = false;
    boolean deliveryCreated = false;

    // 보상트랜잭션에서 id를 전달해야해서 상위로 빼둠
    Order createdOrder = null;

    try {
        // 1. 주문 생성
        createdOrder = orderRepository.save(Order.create(userId, productId, quantity, price));

        // 최소 주문 금액 검증
        if (quantity * price < 1000) {
            throw new Exception400("최소 주문 금액은 1,000원입니다.");
        }

        // 2. 상품 재고 차감
        productClient.decreaseQuantity(new ProductRequest(productId, quantity, price));
        productDecreased = true;

        // 3. 배달 생성
        deliveryClient.createDelivery(new DeliveryRequest(createdOrder.getId(), address));
        deliveryCreated = true;

        // 4. 주문 완료
        createdOrder.complete();
        return OrderResponse.from(createdOrder);

    } catch (Exception e) {
        // 배달 취소
        if (deliveryCreated) {
            deliveryClient.cancelDelivery(createdOrder.getId());
        }

        // 재고 복구
        if (productDecreased) {
            productClient.increaseQuantity(new ProductRequest(productId, quantity, price));
        }
        throw new Exception500("주문 생성 중 오류가 발생했습니다: " + e.getMessage());
    }
}
```

주문 데이터는 catch에서 따로 되돌리지 않아도 자동으로 롤백됩니다. 외부 서비스(상품·배달)만 직접 보상하면 됩니다.

*재고를 줄였으면 다시 늘리고, 배달을 만들었으면 취소하고... 그 말이 이거였구나.*

## 2.6 Docker Compose - 네 개의 서비스를 한 번에 실행하다

시나리오를 따라가기 전에, 각 서비스에 어떤 데이터가 미리 등록되어 있는지 살펴봅니다. 이번 챕터는 **H2 in-memory DB**를 사용합니다. 데이터 정의는 각 서비스의 `db/data.sql`에 있습니다.

| 서비스 | 더미 데이터 |
|---|---|
| **회원** | 계정 3개: ssar, cos, love (비밀번호는 모두 1234) |
| **상품** | MacBook Pro(재고 10), iPhone 15(**재고 0 품절**), AirPods(재고 10) |
| **배달** | 주문 3건에 대응하는 배달 데이터, 모두 COMPLETED 상태 |
| **주문** | 사용자별 주문 3건(완료·취소·대기) |

### 2.6.1 서비스 실행

각 서비스는 **동일한 구조**의 Dockerfile로 **컨테이너 안에서 빌드하고 실행**됩니다. 주문 서비스의 Dockerfile을 예로 살펴봅니다.

**[참고] order/Dockerfile**
```dockerfile
FROM eclipse-temurin:21-jdk              # JDK 21 베이스 이미지
WORKDIR /app                             # 작업 디렉터리 설정
COPY . .                                 # 프로젝트 소스 복사
RUN chmod +x gradlew                     # gradlew 실행 권한 부여
RUN ./gradlew bootJar -x test            # 테스트 없이 실행 가능한 JAR 빌드
RUN cp build/libs/*.jar app.jar          # 빌드된 JAR를 app.jar로 복사
ENTRYPOINT ["java", "-jar", "app.jar"]   # 컨테이너 시작 시 JAR 실행
```

`ex01` 디렉토리의 `docker-compose.yml`은 네 서비스를 **하나의 네트워크로 묶어 한 번에 실행**합니다.

| 서비스 | build.context | 호스트:컨테이너 포트 | 네트워크 |
|---|---|---|---|
| order-service | ./order | 8081:8081 | msa-network |
| user-service | ./user | 8083:8083 | msa-network |
| product-service | ./product | 8082:8082 | msa-network |
| delivery-service | ./delivery | 8084:8084 | msa-network |

`msa-network`로 묶여 있기 때문에, 컨테이너끼리는 **서비스 이름**(예: `http://product-service:8082`)으로 통신할 수 있습니다.

프로젝트가 위치한 폴더로 이동 후, 터미널에서 Docker Compose로 4개 서비스를 한 번에 빌드하고 실행합니다.

**[터미널] Docker Compose 실행**
```bash
cd ex01
docker compose up
```

처음 실행 시 이미지 빌드에 5~10분이 소요될 수 있습니다. 터미널이 멈춘 것처럼 보여도 정상이니 기다려 주세요. 빌드 진행 상황은 `docker compose logs -f [서비스명]`으로 확인할 수 있습니다.

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">ex01 — docker compose up</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-label">user-service</span>&nbsp;&nbsp;<span class="tl-dim">|</span> Started UserApplication in <span class="tl-num">4.231</span> seconds (port: <span class="tl-num">8083</span>)</div>
    <div><span class="tl-label">product-service</span>&nbsp;&nbsp;<span class="tl-dim">|</span> Started ProductApplication in <span class="tl-num">4.512</span> seconds (port: <span class="tl-num">8082</span>)</div>
    <div><span class="tl-label">order-service</span>&nbsp;&nbsp;<span class="tl-dim">|</span> Started OrderApplication in <span class="tl-num">5.103</span> seconds (port: <span class="tl-num">8081</span>)</div>
    <div><span class="tl-label">delivery-service</span>&nbsp;&nbsp;<span class="tl-dim">|</span> Started DeliveryApplication in <span class="tl-num">4.687</span> seconds (port: <span class="tl-num">8084</span>)</div>
    <div class="tl-divider"><span class="tl-val">4개 서비스 기동 완료</span><span class="tl-cursor"></span></div>
  </div>
</div>

*그림 2-3. Docker Compose 실행 결과*

### 2.6.2 Hoppscotch와 인터셉터 설정

서비스를 실행했으니, 이제 API를 호출해 잘 동작하는지 확인해 보겠습니다. 이 책에서는 브라우저에서 API를 호출하는 도구인 **Hoppscotch**(https://hoppscotch.io/)를 사용합니다.

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH02/terminal/04_hoppscotch-main.png)

*그림 2-4. Hoppscotch 화면*

웹 브라우저는 보안 때문에 내 컴퓨터의 localhost로 바로 요청을 보내지 못합니다. 그래서 요청을 대신 전달해 주는 **Hoppscotch Browser Extension**을 Chrome 웹 스토어에서 설치하고, 설정 > Interceptor에서 익스텐션을 선택합니다.

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH02/terminal/Screenshot_6.png)

*그림 2-5. Browser Extension 인터셉터 설정*

### 2.6.3 시나리오 1: 정상 주문

먼저 로그인하여 JWT 토큰을 받습니다. 이때 콘텐츠 종류(Content-Type)를 `application/json`으로 설정해야 합니다. 이 헤더는 서버에게 "내가 보내는 데이터는 JSON 형식이다"라고 알리는 역할을 합니다.

**[Hoppscotch] 로그인**
```json
POST http://localhost:8083/login

{
  "username": "ssar",
  "password": "1234"
}
```

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH02/terminal/06_login-result.png)

*그림 2-6. 로그인 API 호출 결과*

응답 데이터에 포함된 JWT 토큰을 확인할 수 있습니다.

받은 토큰을 Hoppscotch의 **인증 > 인증 유형(Bearer)** 항목의 토큰 필드에 넣습니다.

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH02/terminal/07_bearer-token.png)

*그림 2-7. Bearer 토큰 설정*

다음으로 상품 ID가 1인 MacBook Pro 1개를 주문합니다. 요청 데이터는 상품 정보(`productId`, `quantity`, `price`)와 배달 주소(`address`)를 한 번에 담습니다.

**[Hoppscotch] 주문 생성**
```json
POST http://localhost:8081/api/orders

{
  "productId": 1,
  "quantity": 1,
  "price": 2500000,
  "address": "Addr 4"
}
```

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH02/terminal/08_order-create.png)

*그림 2-8. 주문 생성 API 호출 결과*

주문이 성공하면 상품 서비스에서 재고가 10 → 9로 줄어듭니다.

**[Hoppscotch] 재고 조회**
```json
GET http://localhost:8082/api/products/1
```

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH02/terminal/09_stock-decreased.png)

*그림 2-9. 재고 감소 확인*

배달 서비스에도 배달이 생성됐는지 확인합니다.

**[Hoppscotch] 배달 조회**
```json
GET http://localhost:8084/api/deliveries/4   # 더미 배달 3건 다음이라 새 배달은 4번
```

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH02/terminal/10_delivery-created.png)

*그림 2-10. 배달 생성 확인*

### 2.6.4 시나리오 2: 재고 부족

이번에는 상품 ID가 2인 품절 상품 iPhone 15를 주문해 보겠습니다. 첫 번째 단계인 재고 차감에서 바로 실패하므로, 보상할 작업이 없어 즉시 에러가 반환됩니다.

**[Hoppscotch] 주문 생성 (재고 부족)**
```json
POST http://localhost:8081/api/orders

{
  "productId": 2,
  "quantity": 1,
  "price": 1300000,
  "address": "Addr 4"
}
```

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH02/terminal/11_stockout-error.png)

*그림 2-11. 재고 부족 시 에러 응답*

### 2.6.5 시나리오 3: 주소 누락

이번에는 주소를 빈 문자열로 보내 보겠습니다. 주문 자체는 재고 차감까지 진행되지만, 배달 서비스에서 주소가 없으므로 실패합니다. 이때 보상 트랜잭션이 작동하여 차감된 재고가 복구되고, 주문 데이터는 트랜잭션 롤백으로 처음부터 없던 일처럼 DB에서 사라집니다.

**[Hoppscotch] 주문 생성 (주소 누락)**
```json
POST http://localhost:8081/api/orders

{
  "productId": 1,
  "quantity": 1,
  "price": 2500000,
  "address": ""
}
```

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH02/terminal/12_empty-address-error.png)

*그림 2-12. 주소 누락 시 에러 응답*

그리고 재고가 원복되었는지 확인합니다. 시나리오 1에서 재고가 10개에서 9개로 줄었으니, 이번에 차감된 재고가 보상으로 복구되면 다시 9개로 돌아옵니다.

**[Hoppscotch] 재고 조회**
```json
GET http://localhost:8082/api/products/1
```

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH02/terminal/13_stock-restored.png)

*그림 2-13. 재고 원복 확인*

테스트가 끝났으면 실행 중인 컨테이너를 정리합니다.

**[터미널] 컨테이너 정리**
```bash
docker compose down
```

**오픈이**: "기능별로 서비스를 분리했는데도 서로 통신이 되네요. 중간에 실패해도 보상 트랜잭션이 동작하구요."

**선배**: "맞아요. 그런데 이 방식은 주문 서비스가 상품이랑 배달을 직접 호출하다 보니, 서비스만 분리됐을 뿐 결국 다른 서비스의 장애가 그대로 전파돼요. 상품이나 배달 서비스가 조금만 느려지거나 죽어도, 주문 서비스까지 같이 느려지거나 멈추죠. 이제 여기서부터 하나씩 고쳐 나가봅시다."

지금 구조는 각 서비스 안에서 컨트롤러 계층과 서비스 계층이 직접 의존합니다. 이 때문에 처리 방식을 비동기로 전환하려면 컨트롤러를 비롯해 연관된 메서드까지 모두 수정해야 합니다.

다음 챕터에서는 이 결합도를 낮추기 위해 아키텍처를 개선합니다. 외부 요청과 비즈니스 로직을 분리해, 어느 한쪽을 변경하더라도 다른 쪽에 영향을 주지 않는 구조를 만듭니다.

:::remember
**이것만은 기억하자**

- 서비스가 분리되면 세션을 공유할 수 없어, **JWT**로 인증하고 호출할 때 토큰을 전달합니다.
- 분산 트랜잭션은 자동으로 롤백되지 않아, 실패하면 **보상 트랜잭션**으로 이미 끝난 작업을 되돌립니다.
- 동기 직접 호출은 서비스 간 **결합도를 높여**, 한 서비스가 멈추면 호출한 쪽도 함께 멈춥니다.
:::



---


# 챕터 3. 도메인을 중심으로 - DDD + 클린 아키텍처

며칠 뒤, 팀장이 오픈이의 자리로 찾아왔습니다.

**팀장**: "주문 기능 하나 테스트하려고 하는데, 컨트롤러가 서비스에 직접 의존해서 가짜(Mock) 객체로 테스트할 수가 없어요. 이거 직접 의존하지 않게 구조 정리해 줘요."

오픈이는 곧바로 코드를 열어 봤습니다. 컨트롤러와 서비스가 직접 의존하다 보니, 컨트롤러를 테스트하려면 서비스까지 함께 동작해야 했습니다. 그리고 가짜(Mock) 객체를 넣으려 해도 컨트롤러 코드를 직접 고쳐야 했습니다.

고민에 빠진 오픈이는 선배 자리로 찾아가 코드를 보여 주며 물었습니다.

**선배**: "지금 구조는 결합도가 너무 높아서 그래요. 해결하려면 두 가지를 알아야 해요.

첫째는 구현이 아니라 **인터페이스에 의존**하게 만드는 거예요. 서비스가 다른 객체를 직접 호출하지 않고, 둘 사이에 인터페이스를 두는 거죠. 그래야 코드를 고치지 않고도 진짜 객체 대신 가짜 객체로 테스트할 수 있어요. 이게 **클린 아키텍처**의 기본이에요.

둘째는 **도메인 주도 개발(DDD)** 이에요. 핵심 비즈니스 로직을 외부 환경에 두지 말고 도메인 내부에 모아 둬야 해요. 그래야 외부가 어떻게 바뀌든 영향을 받지 않고, 테스트도 도메인만 독립적으로 깔끔하게 끝낼 수 있어요."

<div class="svg-figure">
<svg viewBox="0 0 1200 580" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="챕터 3 한눈에 보기: 외부 클라이언트가 Ingress와 Gateway를 거쳐 User 또는 Order 서비스를 호출하고, Order가 Product와 Delivery를 동기 호출하는 흐름. 응답은 역순으로 박스를 통과. 모든 서비스는 Kubernetes 클러스터로 묶여 있음">
  <defs>
    <marker id="c3f1-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="600" y="26" text-anchor="middle" font-size="20" font-weight="700" fill="#0f172a">챕터 3 한눈에 보기 — K8s 진입 + 두 단계 흐름</text>
  <rect x="220" y="60" width="960" height="500" rx="14" fill="none" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="6,4"/>
  <text x="240" y="80" font-size="13" font-weight="700" fill="#3730a3">Kubernetes 클러스터 · metacoding</text>
  <text x="40" y="100" font-size="15" font-weight="700" fill="#475569">1단계 — 로그인</text>
  <rect x="40" y="110" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="110" y="143" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">Client</text>
  <text x="110" y="166" text-anchor="middle" font-size="13" fill="#6b7280">사용자</text>
  <rect x="260" y="110" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="330" y="143" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">Ingress</text>
  <text x="330" y="166" text-anchor="middle" font-size="13" fill="#6b7280">외부 진입점</text>
  <rect x="480" y="110" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="550" y="143" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">Gateway</text>
  <text x="550" y="166" text-anchor="middle" font-size="13" fill="#6b7280">Nginx 라우팅</text>
  <rect x="700" y="110" width="170" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="785" y="143" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">User</text>
  <text x="785" y="166" text-anchor="middle" font-size="13" fill="#6b7280">:8083 회원</text>
  <line x1="180" y1="132" x2="258" y2="132" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c3f1-i)"/>
  <text x="219" y="125" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">1. 요청</text>
  <line x1="400" y1="132" x2="478" y2="132" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c3f1-i)"/>
  <text x="439" y="125" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">2. 라우팅</text>
  <line x1="620" y1="132" x2="698" y2="132" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c3f1-i)"/>
  <text x="659" y="125" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">3. 로그인</text>
  <line x1="698" y1="172" x2="622" y2="172" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c3f1-i)"/>
  <text x="660" y="185" text-anchor="middle" font-size="15" font-weight="600" fill="#3730a3">4. 응답</text>
  <line x1="478" y1="172" x2="402" y2="172" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c3f1-i)"/>
  <text x="440" y="185" text-anchor="middle" font-size="15" font-weight="600" fill="#3730a3">5. 응답</text>
  <line x1="258" y1="172" x2="182" y2="172" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c3f1-i)"/>
  <text x="220" y="185" text-anchor="middle" font-size="15" font-weight="600" fill="#3730a3">6. JWT 응답</text>
  <text x="40" y="270" font-size="15" font-weight="700" fill="#475569">2단계 — 주문 생성</text>
  <rect x="40" y="280" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="110" y="313" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">Client</text>
  <text x="110" y="336" text-anchor="middle" font-size="13" fill="#6b7280">사용자</text>
  <rect x="260" y="280" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="330" y="313" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">Ingress</text>
  <text x="330" y="336" text-anchor="middle" font-size="13" fill="#6b7280">외부 진입점</text>
  <rect x="480" y="280" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="550" y="313" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">Gateway</text>
  <text x="550" y="336" text-anchor="middle" font-size="13" fill="#6b7280">Nginx 라우팅</text>
  <rect x="700" y="280" width="170" height="80" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="785" y="313" text-anchor="middle" font-size="19" font-weight="700" fill="#3730a3">Order</text>
  <text x="785" y="336" text-anchor="middle" font-size="13" fill="#3730a3">:8081 주문</text>
  <rect x="940" y="150" width="170" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="1025" y="183" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">Product</text>
  <text x="1025" y="206" text-anchor="middle" font-size="13" fill="#6b7280">:8082 상품</text>
  <rect x="940" y="410" width="170" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="1025" y="443" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">Delivery</text>
  <text x="1025" y="466" text-anchor="middle" font-size="13" fill="#6b7280">:8084 배달</text>
  <line x1="180" y1="302" x2="258" y2="302" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c3f1-i)"/>
  <text x="219" y="295" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">7. 요청</text>
  <line x1="400" y1="302" x2="478" y2="302" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c3f1-i)"/>
  <text x="439" y="295" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">8. 라우팅</text>
  <line x1="620" y1="302" x2="698" y2="302" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c3f1-i)"/>
  <text x="659" y="295" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">9. 주문 생성</text>
  <line x1="770" y1="280" x2="938" y2="170" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c3f1-i)"/>
  <text x="844" y="215" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">10. 재고 차감</text>
  <line x1="940" y1="205" x2="826" y2="280" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c3f1-i)"/>
  <text x="893" y="262" text-anchor="middle" font-size="15" font-weight="600" fill="#3730a3">11. 응답</text>
  <line x1="770" y1="360" x2="938" y2="470" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c3f1-i)"/>
  <text x="844" y="425" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">12. 배달 생성</text>
  <line x1="940" y1="435" x2="826" y2="360" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c3f1-i)"/>
  <text x="893" y="380" text-anchor="middle" font-size="15" font-weight="600" fill="#3730a3">13. 응답</text>
  <line x1="698" y1="342" x2="622" y2="342" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c3f1-i)"/>
  <text x="660" y="332" text-anchor="middle" font-size="15" font-weight="600" fill="#3730a3">14. 응답</text>
  <line x1="478" y1="342" x2="402" y2="342" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c3f1-i)"/>
  <text x="440" y="332" text-anchor="middle" font-size="15" font-weight="600" fill="#3730a3">15. 응답</text>
  <line x1="258" y1="342" x2="182" y2="342" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c3f1-i)"/>
  <text x="220" y="332" text-anchor="middle" font-size="15" font-weight="600" fill="#3730a3">16. 주문 완료</text>
</svg>
</div>

*그림 3-1. 챕터 3 한눈에 보기 - K8s 진입과 두 단계 흐름*

:::goal
**이번 챕터가 끝나면**

- 비즈니스 규칙을 도메인에 모으는 **DDD(도메인 주도 개발)** 를 이해할 수 있습니다.
- 구현 대신 인터페이스에 의존하는 **클린 아키텍처**를 이해할 수 있습니다.
- 게이트웨이와 **쿠버네티스**로 서비스를 묶어 배포하는 구조를 이해할 수 있습니다.
:::

::::prep
**준비하기**. 실습 시작 전 한 번만 설정

### 1. 소스 코드 클론

**[터미널] 레포 클론**
```bash
git clone https://github.com/metacoding-12-msa/ex02.git
cd ex02
```

### 2. 파일 구조

**ex02 디렉토리**
```text
ex02/
├── order/              # 포트 8081
├── product/            # 포트 8082
├── user/               # 포트 8083
├── delivery/           # 포트 8084
├── gateway/            # Nginx API Gateway
├── db/                 # MySQL Dockerfile
└── k8s/                # Kubernetes YAML 파일
```

**주문 서비스 패키지 구조 (챕터 3에서 재구성)**
```text
src/main/java/com/metacoding/order/
├── domain/         # 엔티티 + 비즈니스 규칙
├── repository/     # Spring Data JPA
├── usecase/        # UseCase 인터페이스 + 서비스 코드
├── web/            # 컨트롤러 + DTO
├── adapter/        # 외부 서비스 클라이언트 (order 전용)
└── core/           # JWT, 예외처리 (챕터 2와 동일)
src/main/resources/
└── application.properties        # DB·JWT 설정 (값은 환경변수로 주입)
```

:::note
**user/product/delivery도 동일한 구조이며, adapter/ 패키지만 order 전용입니다.**
:::

### 3. 실습 환경

| 도구 | 용도 | 비고 |
|------|------|------|
| **Docker Desktop** | 컨테이너 런타임 | 챕터 2에서 설치한 그대로. 실행 중이어야 함 |
| **Minikube** | 로컬 Kubernetes 클러스터 | https://minikube.sigs.k8s.io/ |

### 4. 실습 순서

1. 챕터 2 코드를 DDD + 클린 아키텍처로 재구성하는 과정 살펴보기
2. 주문 서비스에 UseCase 인터페이스 + 도메인 캡슐화 적용
3. Nginx API Gateway와 MySQL 인프라 살펴보기
4. Kubernetes YAML 파일(ConfigMap·Secret·Deployment·Service·Ingress) 5종 살펴보기
5. Minikube에서 빌드·배포·실행
::::

## 3.1 도메인 주도 개발(Domain-Driven Design) - 비즈니스 로직을 도메인으로

가게 운영 규칙이 **사장 한 명의 머릿속**에만 있다고 해보겠습니다. 환불 가능 시간, 결제 방식, 재고 처리까지 전부 사장이 외우고 있습니다. 그래서 누가 손님을 응대하든 사장이 대답을 해야 합니다.

이 문제는 **가게 운영 매뉴얼**을 만들면 해결됩니다. 규칙은 매뉴얼에 정리해 두고, 사장은 손님 응대 흐름만 진행하면서 매뉴얼에 적힌 대로 따릅니다. **누가 응대하든 매뉴얼만 보면 같은 판단을 할 수 있습니다.** 새 규칙이 들어와도 **매뉴얼 한 곳만 업데이트**하면 끝입니다.

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH03/gemini/01_clerk-vs-owner.png)
*그림 3-2. 머릿속 규칙에서 운영 매뉴얼로*

여기서 `OrderService`가 비즈니스를 수행하는 **사장님**이라면, `Order` 도메인 객체는 그 안에 담긴 핵심 규칙인 **운영 매뉴얼**입니다. **비즈니스 로직을 서비스에서 분리해 도메인에 모아 두면** 기술적 환경이 변해도 비즈니스의 본질은 영향을 받지 않으며, 복잡한 요구사항 속에서도 코드의 가독성과 유지보수성을 지킬 수 있습니다.

## 3.2 UseCase 인터페이스(Use Case Interface) - USB 허브처럼 바꿔 꽂기

비즈니스를 수행하는 서비스가 컨트롤러에 직접 묶여 있으면 두 코드가 **강하게 결합됩니다.** 그래서 서비스를 고칠 때마다 컨트롤러도 함께 고쳐야 하고, 테스트할 때 진짜 서비스 대신 **가짜(Mock) 객체를 끼워 넣기도 불가능**해집니다.

이 문제를 해결하려면 컨트롤러와 서비스 사이에 **느슨한 연결 고리**가 필요합니다. 컴퓨터와 USB 허브를 떠올려 보세요. 여러 장치를 컴퓨터에 직접 연결하지 않고 USB 허브를 거쳐 연결하면, 뒤에서 장치를 아무리 바꾸더라도 **컴퓨터와 허브 사이의 연결에는 아무런 변화가 없습니다.**

<div class="svg-figure">
<svg viewBox="0 0 800 380" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="UseCase 인터페이스 - USB 허브 비유: 다양한 USB 장치들이 USB 허브를 거쳐 컴퓨터에 연결되는 구조">
  <text x="400" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">UseCase 인터페이스 - USB 허브 비유</text>
  <text x="90" y="75" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">마우스</text>
  <path d="M 65 85 Q 65 80 70 80 L 110 80 Q 115 80 115 85 L 115 130 Q 115 135 110 135 L 70 135 Q 65 135 65 130 Z" fill="#fff" stroke="#0f172a" stroke-width="1.5"/>
  <line x1="90" y1="80" x2="90" y2="105" stroke="#0f172a" stroke-width="1"/>
  <circle cx="90" cy="100" r="2.5" fill="#0f172a"/>
  <path d="M 115 105 Q 200 105 240 130 L 285 152" fill="none" stroke="#0f172a" stroke-width="1.4"/>
  <rect x="285" y="148" width="14" height="20" fill="#0f172a"/>
  <text x="90" y="170" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">키보드</text>
  <rect x="40" y="180" width="100" height="40" fill="#fff" stroke="#0f172a" stroke-width="1.5"/>
  <line x1="55" y1="180" x2="55" y2="220" stroke="#0f172a" stroke-width="0.7"/>
  <line x1="70" y1="180" x2="70" y2="220" stroke="#0f172a" stroke-width="0.7"/>
  <line x1="85" y1="180" x2="85" y2="220" stroke="#0f172a" stroke-width="0.7"/>
  <line x1="100" y1="180" x2="100" y2="220" stroke="#0f172a" stroke-width="0.7"/>
  <line x1="115" y1="180" x2="115" y2="220" stroke="#0f172a" stroke-width="0.7"/>
  <line x1="125" y1="180" x2="125" y2="220" stroke="#0f172a" stroke-width="0.7"/>
  <line x1="40" y1="200" x2="140" y2="200" stroke="#0f172a" stroke-width="0.7"/>
  <path d="M 140 200 Q 220 200 260 192 L 285 188" fill="none" stroke="#0f172a" stroke-width="1.4"/>
  <rect x="285" y="183" width="14" height="20" fill="#0f172a"/>
  <text x="90" y="260" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">외장하드</text>
  <rect x="50" y="270" width="80" height="50" rx="4" fill="#fff" stroke="#0f172a" stroke-width="1.5"/>
  <circle cx="120" cy="278" r="2" fill="#0f172a"/>
  <line x1="55" y1="295" x2="105" y2="295" stroke="#0f172a" stroke-width="0.7"/>
  <path d="M 130 295 Q 220 280 260 245 L 285 222" fill="none" stroke="#0f172a" stroke-width="1.4"/>
  <rect x="285" y="218" width="14" height="20" fill="#0f172a"/>
  <text x="380" y="105" text-anchor="middle" font-size="14" font-weight="700" fill="#3730a3">USB 허브</text>
  <rect x="305" y="120" width="150" height="160" rx="10" fill="#fff" stroke="#4f46e5" stroke-width="2" stroke-dasharray="6,4"/>
  <rect x="298" y="150" width="14" height="9" fill="#0f172a"/>
  <rect x="298" y="185" width="14" height="9" fill="#0f172a"/>
  <rect x="298" y="220" width="14" height="9" fill="#0f172a"/>
  <rect x="448" y="185" width="14" height="9" fill="#0f172a"/>
  <text x="380" y="255" text-anchor="middle" font-size="11" fill="#3730a3">(약속된 규격)</text>
  <path d="M 462 190 Q 510 190 540 195" fill="none" stroke="#0f172a" stroke-width="1.4"/>
  <text x="630" y="105" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">Controller (컴퓨터)</text>
  <rect x="540" y="120" width="180" height="130" rx="4" fill="#fff" stroke="#0f172a" stroke-width="1.6"/>
  <rect x="552" y="130" width="156" height="100" fill="#fff" stroke="#0f172a" stroke-width="0.8"/>
  <circle cx="630" cy="240" r="1.5" fill="#0f172a"/>
  <line x1="630" y1="250" x2="630" y2="270" stroke="#0f172a" stroke-width="1.6"/>
  <path d="M 580 280 L 680 280 L 670 295 L 590 295 Z" fill="#fff" stroke="#0f172a" stroke-width="1.4"/>
  <rect x="540" y="190" width="14" height="9" fill="#0f172a"/>
</svg>
</div>

*그림 3-3. UseCase 인터페이스 - USB 허브 비유*

여기서 USB 허브의 역할을 하는 것이 바로 **UseCase 인터페이스**입니다.

:::term-box
**UseCase 인터페이스란?** 시스템이 수행할 비즈니스 **행위(주문 생성·조회·취소 같은)** 를 메서드로 약속한 인터페이스입니다.
:::

컨트롤러가 구현체 대신 UseCase 인터페이스를 참조하고, 서비스가 이 인터페이스를 구현하면 둘은 독립적으로 동작합니다. 이렇게 의존 관계를 느슨하게 만들어 내부 로직을 보호하는 것이 **클린 아키텍처**의 원칙입니다.

<div class="svg-figure">
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="UseCase 인터페이스 의존 구조: 세 구현체가 UseCase 인터페이스를 향하고 Controller는 그 인터페이스만 안다">
  <defs>
    <marker id="c3f2-g" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="400" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">UseCase 인터페이스 의존 구조</text>
  <rect x="60" y="60" width="200" height="80" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="160" y="95" text-anchor="middle" font-size="14" font-weight="700" fill="#3730a3">OrderServiceV1</text>
  <text x="160" y="118" text-anchor="middle" font-size="12" fill="#3730a3">(H2 개발용)</text>
  <rect x="300" y="60" width="200" height="80" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="400" y="95" text-anchor="middle" font-size="14" font-weight="700" fill="#3730a3">OrderServiceV2</text>
  <text x="400" y="118" text-anchor="middle" font-size="12" fill="#3730a3">(MySQL 운영용)</text>
  <rect x="540" y="60" width="200" height="80" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="640" y="95" text-anchor="middle" font-size="14" font-weight="700" fill="#3730a3">MockOrderService</text>
  <text x="640" y="118" text-anchor="middle" font-size="12" fill="#3730a3">(테스트용)</text>
  <line x1="160" y1="140" x2="320" y2="235" stroke="#475569" stroke-width="1.6" marker-end="url(#c3f2-g)"/>
  <line x1="400" y1="140" x2="400" y2="235" stroke="#475569" stroke-width="1.6" marker-end="url(#c3f2-g)"/>
  <line x1="640" y1="140" x2="480" y2="235" stroke="#475569" stroke-width="1.6" marker-end="url(#c3f2-g)"/>
  <rect x="260" y="240" width="280" height="90" rx="6" fill="#fff" stroke="#4f46e5" stroke-width="1.8" stroke-dasharray="6,4"/>
  <text x="400" y="278" text-anchor="middle" font-size="14" font-weight="700" fill="#3730a3">CreateOrderUseCase</text>
  <text x="400" y="302" text-anchor="middle" font-size="12" fill="#3730a3">(약속: '주문을 생성한다')</text>
  <line x1="400" y1="395" x2="400" y2="335" stroke="#475569" stroke-width="1.6" marker-end="url(#c3f2-g)"/>
  <rect x="180" y="400" width="440" height="80" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="400" y="435" text-anchor="middle" font-size="14" font-weight="700" fill="#3730a3">OrderController</text>
  <text x="400" y="458" text-anchor="middle" font-size="12" fill="#3730a3">(어떤 코드가 꽂혔는지 몰라도 된다)</text>
</svg>
</div>

*그림 3-4. UseCase 인터페이스 의존 구조*

**"무엇을 할 것인가"(UseCase 인터페이스)** 와 **"어떻게 할 것인가"(Service 코드)** 를 분리하는 것이 핵심입니다.

## 3.3 패키지 구조 비교 - 단일 패키지에서 책임별 패키지로

챕터 2는 **단일 패키지 구조**입니다. 주문과 관련된 모든 클래스가 `orders/` 한 폴더에 모여 있습니다.

반면 챕터 3은 **책임별 패키지 구조**입니다. 같은 주문 코드가 역할에 따라 네 폴더로 나뉩니다. 앞에서 다룬 도메인 응집과 인터페이스 분리가 폴더 구조에 그대로 반영됩니다.

<div class="svg-figure">
<div style="background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:22px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans KR',sans-serif;">
  <div style="display:grid;grid-template-columns:1fr 1.2fr 1fr;gap:0;align-items:start;">
    <div style="border:2px dashed #cbd5e1;border-radius:10px;padding:14px;">
      <div style="font-family:'SFMono-Regular',Consolas,monospace;font-size:13px;font-weight:700;text-align:center;padding:4px 0 10px;border-bottom:1px solid #e2e8f0;color:#64748b;">챕터 2 — orders/</div>
      <div style="display:flex;flex-direction:column;gap:6px;padding:10px 0 0;">
        <span style="display:inline-flex;padding:5px 11px;border-radius:5px;font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:600;border:1.5px solid #cbd5e1;background:#f1f5f9;color:#64748b;">Order</span>
        <span style="display:inline-flex;padding:5px 11px;border-radius:5px;font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:600;border:1.5px solid #cbd5e1;background:#f1f5f9;color:#64748b;">OrderStatus</span>
        <span style="display:inline-flex;padding:5px 11px;border-radius:5px;font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:600;border:1.5px solid #cbd5e1;background:#f1f5f9;color:#64748b;">OrderController</span>
        <span style="display:inline-flex;padding:5px 11px;border-radius:5px;font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:600;border:1.5px solid #cbd5e1;background:#f1f5f9;color:#64748b;">OrderService</span>
        <span style="display:inline-flex;padding:5px 11px;border-radius:5px;font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:600;border:1.5px solid #cbd5e1;background:#f1f5f9;color:#64748b;">OrderRepository</span>
        <span style="display:inline-flex;padding:5px 11px;border-radius:5px;font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:600;border:1.5px solid #cbd5e1;background:#f1f5f9;color:#64748b;">OrderRequest</span>
        <span style="display:inline-flex;padding:5px 11px;border-radius:5px;font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:600;border:1.5px solid #cbd5e1;background:#f1f5f9;color:#64748b;">OrderResponse</span>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:5px;padding:14px 10px;">
      <div style="display:grid;grid-template-columns:1fr 14px 1fr;gap:6px;align-items:center;font-family:'SFMono-Regular',Consolas,monospace;font-size:11.5px;"><span style="text-align:right;color:#64748b;">Order</span><span style="text-align:center;color:#4f46e5;">→</span><span style="font-weight:700;color:#3730a3;">domain/</span></div>
      <div style="display:grid;grid-template-columns:1fr 14px 1fr;gap:6px;align-items:center;font-family:'SFMono-Regular',Consolas,monospace;font-size:11.5px;"><span style="text-align:right;color:#64748b;">OrderStatus</span><span style="text-align:center;color:#4f46e5;">→</span><span style="font-weight:700;color:#3730a3;">domain/</span></div>
      <div style="display:grid;grid-template-columns:1fr 14px 1fr;gap:6px;align-items:center;font-family:'SFMono-Regular',Consolas,monospace;font-size:11.5px;"><span style="text-align:right;color:#64748b;">OrderController</span><span style="text-align:center;color:#4f46e5;">→</span><span style="font-weight:700;color:#3730a3;">web/</span></div>
      <div style="display:grid;grid-template-columns:1fr 14px 1fr;gap:6px;align-items:center;font-family:'SFMono-Regular',Consolas,monospace;font-size:11.5px;"><span style="text-align:right;color:#64748b;">OrderService</span><span style="text-align:center;color:#4f46e5;">→</span><span style="font-weight:700;color:#3730a3;">usecase/</span></div>
      <div style="display:grid;grid-template-columns:1fr 14px 1fr;gap:6px;align-items:center;font-family:'SFMono-Regular',Consolas,monospace;font-size:11.5px;"><span style="text-align:right;color:#64748b;">OrderRepository</span><span style="text-align:center;color:#4f46e5;">→</span><span style="font-weight:700;color:#3730a3;">repository/</span></div>
      <div style="display:grid;grid-template-columns:1fr 14px 1fr;gap:6px;align-items:center;font-family:'SFMono-Regular',Consolas,monospace;font-size:11.5px;"><span style="text-align:right;color:#64748b;">OrderRequest</span><span style="text-align:center;color:#4f46e5;">→</span><span style="font-weight:700;color:#3730a3;">web/</span></div>
      <div style="display:grid;grid-template-columns:1fr 14px 1fr;gap:6px;align-items:center;font-family:'SFMono-Regular',Consolas,monospace;font-size:11.5px;"><span style="text-align:right;color:#64748b;">OrderResponse</span><span style="text-align:center;color:#4f46e5;">→</span><span style="font-weight:700;color:#3730a3;">web/</span></div>
    </div>
    <div style="border:2px solid #4f46e5;border-radius:10px;padding:0;">
      <div style="padding:10px 14px;border-bottom:1px solid #e2e8f0;">
        <div style="font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:700;margin-bottom:5px;color:#3730a3;">domain/ <span style="font-family:-apple-system,sans-serif;font-size:11px;font-weight:500;color:#64748b;font-style:italic;">비즈니스 규칙</span></div>
        <span style="display:inline-flex;padding:5px 11px;border-radius:5px;font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:600;border:1.5px solid #c7d2fe;background:#eef2ff;color:#3730a3;margin:0 4px 5px 0;">Order</span>
        <span style="display:inline-flex;padding:5px 11px;border-radius:5px;font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:600;border:1.5px solid #c7d2fe;background:#eef2ff;color:#3730a3;margin:0 4px 5px 0;">OrderStatus</span>
      </div>
      <div style="padding:10px 14px;border-bottom:1px solid #e2e8f0;">
        <div style="font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:700;margin-bottom:5px;color:#3730a3;">usecase/ <span style="font-family:-apple-system,sans-serif;font-size:11px;font-weight:500;color:#64748b;font-style:italic;">인터페이스 + 구현</span></div>
        <span style="display:inline-flex;padding:5px 11px;border-radius:5px;font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:600;border:1.5px solid #c7d2fe;background:#eef2ff;color:#3730a3;margin:0 4px 5px 0;">OrderService</span>
        <span style="display:inline-flex;padding:5px 11px;border-radius:5px;font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:600;border:1.5px solid #c7d2fe;background:#eef2ff;color:#3730a3;margin:0 4px 5px 0;">CreateOrderUseCase</span>
      </div>
      <div style="padding:10px 14px;border-bottom:1px solid #e2e8f0;">
        <div style="font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:700;margin-bottom:5px;color:#3730a3;">web/ <span style="font-family:-apple-system,sans-serif;font-size:11px;font-weight:500;color:#64748b;font-style:italic;">외부 요청 진입점</span></div>
        <span style="display:inline-flex;padding:5px 11px;border-radius:5px;font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:600;border:1.5px solid #c7d2fe;background:#eef2ff;color:#3730a3;margin:0 4px 5px 0;">OrderController</span>
        <span style="display:inline-flex;padding:5px 11px;border-radius:5px;font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:600;border:1.5px solid #c7d2fe;background:#eef2ff;color:#3730a3;margin:0 4px 5px 0;">OrderRequest</span>
        <span style="display:inline-flex;padding:5px 11px;border-radius:5px;font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:600;border:1.5px solid #c7d2fe;background:#eef2ff;color:#3730a3;margin:0 4px 5px 0;">OrderResponse</span>
      </div>
      <div style="padding:10px 14px;">
        <div style="font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:700;margin-bottom:5px;color:#3730a3;">repository/ <span style="font-family:-apple-system,sans-serif;font-size:11px;font-weight:500;color:#64748b;font-style:italic;">DB 접근</span></div>
        <span style="display:inline-flex;padding:5px 11px;border-radius:5px;font-family:'SFMono-Regular',Consolas,monospace;font-size:12px;font-weight:600;border:1.5px solid #c7d2fe;background:#eef2ff;color:#3730a3;margin:0 4px 5px 0;">OrderRepository</span>
      </div>
    </div>
  </div>
</div>
</div>

*그림 3-5. 패키지 구조 비교 - 단일 패키지에서 책임별 패키지로*

이렇게 도메인을 중심에 두고 외부 의존을 인터페이스로 분리하는 패키지 구조를 **헥사고날 패턴(Hexagonal Architecture)** 이라고 합니다. 이 책에서는 완전한 아키텍처보다는 실습에 필요한 개념만 적용합니다.

## 3.4 UseCase 인터페이스 + 도메인 캡슐화 도입

이제 실제 코드에 적용해보겠습니다.

### 3.4.1 UseCase 인터페이스 정의

주문·상품·회원·배달 서비스의 각 기능을 인터페이스 형태로 UseCase로 정의합니다. **인터페이스 하나가 하나의 행위(Use Case)를 의미합니다.**

`usecase/CreateOrderUseCase.java`를 열고 주문 생성 인터페이스를 작성합니다.

**[실습 1] usecase/CreateOrderUseCase.java. 주문 생성 인터페이스**
```java
// 주문을 생성한다 - 행위 하나를 인터페이스로 약속
public interface CreateOrderUseCase {
    OrderResponse createOrder(int userId, int productId, int quantity, Long price, String address);
}
```

조회는 `GetOrderUseCase`, 취소는 `CancelOrderUseCase`로 같은 방식으로 정의합니다.

### 3.4.2 엔티티의 비즈니스 로직 — DDD의 핵심

**"주문 금액이 최소 기준을 넘는가?"** 같은 비즈니스 규칙은 서비스가 아닌 엔티티에 둡니다. 엔티티 메서드로 캡슐화하면 어디서 호출하든 동일한 규칙이 적용되고, 새 규칙이 들어와도 도메인 메서드만 추가하면 됩니다.

`domain/Order.java`를 열고 최소 주문 금액 검증 메서드를 작성합니다.

**[실습 2] domain/Order.java. 비즈니스 규칙을 도메인에 캡슐화**
```java
public class Order {
    // 챕터 2 Order.java 참조 — 필드·create()·complete() 동일

    // 최소 주문 금액 검증 (챕터 2에서 서비스에 있던 검증을 도메인으로 옮김)
    public void validateMinAmount() {
        if (this.quantity * this.price < 1000) {
            throw new Exception400("최소 주문 금액은 1,000원입니다.");
        }
    }
}
```

### 3.4.3 OrderService - 인터페이스 구현

OrderService는 주문 생성, 주문 조회, 주문 취소 인터페이스를 구현하고, 도메인 객체의 비즈니스 메서드를 호출합니다.

`usecase/OrderService.java`를 열고 UseCase 인터페이스 구현을 작성합니다.

**[실습 3] usecase/OrderService.java. UseCase 인터페이스 구현**
```java
@RequiredArgsConstructor
@Service
@Transactional(readOnly = true)
public class OrderService implements CreateOrderUseCase, GetOrderUseCase, CancelOrderUseCase {
                                     // 1. UseCase 인터페이스를 구현

    @Override
    @Transactional
    public OrderResponse createOrder(int userId, int productId,
            int quantity, Long price, String address) {
        Order createdOrder = orderRepository.save(
                Order.create(userId, productId, quantity, price));
        // 2. 검증 메서드 호출
        createdOrder.validateMinAmount();
        // ... 재고 차감 → 배달 생성 → 완료 (보상 트랜잭션)
    }
}
```

### 3.4.4 OrderController 수정

컨트롤러는 서비스가 아닌 인터페이스에 의존하도록 수정합니다. 앞으로 `OrderService`를 다른 코드로 바꿔도 이 컨트롤러는 전혀 수정하지 않아도 됩니다.

`web/OrderController.java`를 열어 아래처럼 인터페이스에 의존하도록 수정합니다.

**[실습 4] web/OrderController.java. UseCase 인터페이스 주입**
```java
@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {
    private final CreateOrderUseCase createOrderUseCase;   // 구현체가 아닌 인터페이스 주입
    private final GetOrderUseCase getOrderUseCase;
    private final CancelOrderUseCase cancelOrderUseCase;

    @PostMapping
    public ResponseEntity<?> createOrder(...) {
        return Resp.ok(createOrderUseCase.createOrder(...));  // 인터페이스 메서드 호출
    }

    // GET /{orderId} — 주문 조회
    // PUT /{orderId} — 주문 취소
}
```

주문 서비스와 동일한 패턴으로 상품, 배달, 회원 서비스도 구성되어 있습니다.

내부 구조를 정리했으니, 이제 네 서비스를 운영 환경에 올릴 차례입니다.

**오픈이**: "그런데 지금까지는 요청할 때마다 서비스 포트를 바꿔야 했어요. 이건 어떻게 해결하나요?"

**선배**: "내부를 수정했으니, 외부에서 들어오는 단일 진입점도 만들면 좋겠네요."

## 3.5 Gateway와 MySQL 인프라

### 3.5.1 Nginx - API Gateway 라우팅

서비스가 늘어날수록 클라이언트는 모든 포트를 알아야 하고, 서비스 주소가 바뀌면 그때마다 코드를 고쳐야 합니다. 이때 **API Gateway**를 앞에 두면, 클라이언트는 하나의 진입점으로만 요청하고 게이트웨이가 URL 경로에 따라 알맞은 서비스로 전달합니다.

<div class="svg-figure">
<svg viewBox="0 0 900 470" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="클라이언트가 요청과 JWT를 게이트웨이로 보내면 게이트웨이가 URL 경로에 따라 회원·상품·주문·배달 서비스로 전달하고, 토큰 검증은 각 서비스가 한다.">
  <defs>
    <marker id="gw-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="450" y="26" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">API Gateway — 한 입구로 받아 경로대로 보낸다</text>
  <rect x="300" y="42" width="588" height="412" rx="14" fill="none" stroke="#94a3b8" stroke-width="1.6" stroke-dasharray="8,5"/>
  <text x="314" y="60" font-size="12" font-weight="700" fill="#64748b">클러스터</text>
  <rect x="36" y="195" width="150" height="80" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="111" y="230" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">Client</text>
  <rect x="86" y="244" width="50" height="22" rx="5" fill="#fff" stroke="#4f46e5" stroke-width="1.3"/>
  <text x="111" y="259" text-anchor="middle" font-size="10" font-weight="700" fill="#3730a3">JWT</text>
  <rect x="320" y="190" width="170" height="90" rx="12" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="405" y="230" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">API Gateway</text>
  <text x="405" y="253" text-anchor="middle" font-size="12" fill="#3730a3">Nginx · :80</text>
  <line x1="186" y1="235" x2="318" y2="235" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#gw-a)"/>
  <text x="252" y="225" text-anchor="middle" font-size="12" font-weight="600" fill="#4f46e5">요청 + JWT</text>
  <rect x="640" y="56" width="230" height="66" rx="9" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <rect x="652" y="78" width="44" height="24" rx="5" fill="#fff" stroke="#4f46e5" stroke-width="1.2"/>
  <text x="674" y="94" text-anchor="middle" font-size="9" font-weight="700" fill="#3730a3">JWT</text>
  <text x="765" y="84" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">User</text>
  <text x="765" y="105" text-anchor="middle" font-size="11" fill="#6b7280">:8083 회원</text>
  <rect x="640" y="162" width="230" height="66" rx="9" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <rect x="652" y="184" width="44" height="24" rx="5" fill="#fff" stroke="#4f46e5" stroke-width="1.2"/>
  <text x="674" y="200" text-anchor="middle" font-size="9" font-weight="700" fill="#3730a3">JWT</text>
  <text x="772" y="190" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Product</text>
  <text x="772" y="211" text-anchor="middle" font-size="11" fill="#6b7280">:8082 상품</text>
  <rect x="640" y="268" width="230" height="66" rx="9" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <rect x="652" y="290" width="44" height="24" rx="5" fill="#fff" stroke="#4f46e5" stroke-width="1.2"/>
  <text x="674" y="306" text-anchor="middle" font-size="9" font-weight="700" fill="#3730a3">JWT</text>
  <text x="772" y="296" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Order</text>
  <text x="772" y="317" text-anchor="middle" font-size="11" fill="#6b7280">:8081 주문</text>
  <rect x="640" y="374" width="230" height="66" rx="9" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <rect x="652" y="396" width="44" height="24" rx="5" fill="#fff" stroke="#4f46e5" stroke-width="1.2"/>
  <text x="674" y="412" text-anchor="middle" font-size="9" font-weight="700" fill="#3730a3">JWT</text>
  <text x="776" y="402" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Delivery</text>
  <text x="776" y="423" text-anchor="middle" font-size="11" fill="#6b7280">:8084 배달</text>
  <line x1="490" y1="218" x2="638" y2="92" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#gw-a)"/>
  <text x="556" y="140" text-anchor="middle" font-size="11" font-weight="600" fill="#4f46e5">/login · /api/users</text>
  <line x1="490" y1="230" x2="638" y2="196" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#gw-a)"/>
  <text x="566" y="210" text-anchor="middle" font-size="11" font-weight="600" fill="#4f46e5">/api/products</text>
  <line x1="490" y1="250" x2="638" y2="300" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#gw-a)"/>
  <text x="566" y="282" text-anchor="middle" font-size="11" font-weight="600" fill="#4f46e5">/api/orders</text>
  <line x1="490" y1="262" x2="638" y2="404" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#gw-a)"/>
  <text x="556" y="356" text-anchor="middle" font-size="11" font-weight="600" fill="#4f46e5">/api/deliveries</text>
</svg>
</div>

*그림 3-6. 한 입구로 받아 경로대로 전달하고, 토큰 검증은 각 서비스가 합니다*

`gateway/` 디렉토리에는 두 파일이 있습니다. 전체 설정은 GitHub을 참고하세요.

| 파일 | 역할 |
|---|---|
| **Dockerfile** | Nginx 베이스 이미지에 설정 파일을 넣어 게이트웨이 컨테이너를 만듭니다. |
| **nginx.conf** | URL 경로별로 어느 서비스에 요청을 보낼지 정의합니다. |

:::tip
**게이트웨이에서 토큰을 검증하는 방식**

지금 이 책에서는 게이트웨이(Nginx)가 요청을 경로대로 넘기기만 하고, JWT는 각 서비스가 직접 검증합니다. 다른 방법으로, 게이트웨이가 입구에서 토큰을 먼저 검증하고 통과한 요청만 서비스로 보내는 구조도 널리 쓰입니다. 이때 게이트웨이는 토큰에서 꺼낸 사용자 정보를 헤더에 실어 전달하고, 내부 서비스는 게이트웨이를 지나온 요청을 이미 인증된 것으로 신뢰합니다.

게이트웨이에서 검증하면 인증이 한 곳에 모여 각 서비스는 비즈니스 로직에만 집중할 수 있습니다. 다만 Nginx만으로는 토큰 검증이 어려워 Spring Cloud Gateway 같은 도구가 필요합니다. 이 책은 단순함을 위해 서비스별 검증을 택했습니다.
:::

### 3.5.2 MySQL - 데이터베이스 인프라

모든 서비스가 동일한 MySQL 인스턴스를 공유합니다. 서비스별로 테이블이 분리되어 있으나, 물리적으로는 단일 DB 인스턴스입니다.

:::note
**이 책에서는 학습 편의를 위해 하나의 DB를 공유합니다.** 실제 MSA에서는 서비스마다 독립된 DB를 두지만, 학습 흐름을 익히는 데는 차이가 없으니 DB 구성보다 흐름에 집중해 주세요.
:::

DB 컨테이너는 `db/` 디렉토리의 두 파일로 구성됩니다.

| 파일 | 역할 |
|---|---|
| **Dockerfile** | MySQL 공식 이미지를 베이스로 초기화 SQL을 컨테이너에 넣어 띄웁니다. |
| **init.sql** | 네 서비스에 필요한 테이블을 만들고 더미 데이터를 채웁니다. |

## 3.6 Kubernetes - YAML로 선언하는 배포

**오픈이**: "준비가 끝났으니, 이제 배포를 시작할까요?"

**선배**: "그 전에 실무에 올리려면 한 가지 더 생각해야 해요. 지금은 Docker Compose로 컨테이너를 직접 띄우고 있잖아요? 만약 서버가 멈추거나 컨테이너가 갑자기 내려가면 어떻게 될까요?"

**오픈이**: "음… 개발자가 서버에 접속해서 다시 띄워야 하지 않을까요?"

**선배**: "사람이 24시간 내내 서버만 지켜볼 수는 없죠. 쿠버네티스는 우리가 원하는 상태를 정해 두면, 컨테이너가 죽더라도 알아서 다시 살려내서 그 상태를 유지해 줘요."

### 3.6.1 리소스 구조 설계

Kubernetes는 YAML 파일로 원하는 상태를 선언합니다. **"이 서비스는 이렇게 실행되어야 한다"** 고 파일에 적어두면, Kubernetes가 그 상태를 유지합니다.

<div class="svg-figure">
<svg viewBox="0 0 880 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Kubernetes 핵심 리소스의 전체 구조 — 사용자 요청은 Service에서 Pod로 직접 흐르고, Pod 오른쪽의 Deployment가 Pod 생성·관리를 담당한다">
  <defs>
    <marker id="k3-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
    <marker id="k3-g" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#9ca3af"/></marker>
    <marker id="k3-m" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="440" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">Kubernetes 핵심 리소스의 전체 구조</text>
  <rect x="20" y="130" width="80" height="50" rx="6" fill="#fff" stroke="#9ca3af" stroke-width="1.4"/>
  <text x="60" y="160" text-anchor="middle" font-size="12" fill="#374151">클라이언트</text>
  <line x1="100" y1="155" x2="140" y2="155" stroke="#9ca3af" stroke-width="1.4" marker-end="url(#k3-g)"/>
  <rect x="140" y="50" width="720" height="260" rx="10" fill="#fff" stroke="#475569" stroke-width="1.6" stroke-dasharray="6,4"/>
  <text x="160" y="70" font-size="11" font-weight="600" fill="#0f172a">Kubernetes 클러스터</text>
  <rect x="170" y="130" width="100" height="50" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="220" y="155" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">Ingress</text>
  <text x="220" y="172" text-anchor="middle" font-size="9" fill="#6b7280">진입점</text>
  <line x1="270" y1="155" x2="310" y2="155" stroke="#475569" stroke-width="1.6" marker-end="url(#k3-p)"/>
  <rect x="310" y="130" width="100" height="50" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="360" y="155" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">Service</text>
  <text x="360" y="172" text-anchor="middle" font-size="9" fill="#6b7280">고정 주소</text>
  <line x1="410" y1="145" x2="570" y2="120" stroke="#475569" stroke-width="1.6" marker-end="url(#k3-p)"/>
  <line x1="410" y1="165" x2="570" y2="200" stroke="#475569" stroke-width="1.6" marker-end="url(#k3-p)"/>
  <text x="490" y="120" text-anchor="middle" font-size="9" fill="#475569" font-style="italic">Pod 연결</text>
  <rect x="570" y="100" width="120" height="50" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="630" y="122" text-anchor="middle" font-size="12" font-weight="700" fill="#3730a3">Pod 1</text>
  <text x="630" y="138" text-anchor="middle" font-size="10" fill="#3730a3">컨테이너 실행</text>
  <rect x="570" y="180" width="120" height="50" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="630" y="202" text-anchor="middle" font-size="12" font-weight="700" fill="#3730a3">Pod 2</text>
  <text x="630" y="218" text-anchor="middle" font-size="10" fill="#3730a3">컨테이너 실행</text>
  <rect x="720" y="140" width="100" height="50" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="770" y="162" text-anchor="middle" font-size="12" font-weight="700" fill="#3730a3">Deployment</text>
  <text x="770" y="178" text-anchor="middle" font-size="9" fill="#3730a3">Pod 생성·관리</text>
  <line x1="720" y1="150" x2="690" y2="125" stroke="#4f46e5" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#k3-m)"/>
  <line x1="720" y1="180" x2="690" y2="205" stroke="#4f46e5" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#k3-m)"/>
  <text x="725" y="135" text-anchor="middle" font-size="9" fill="#4f46e5" font-style="italic">관리</text>
  <rect x="380" y="240" width="110" height="50" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="435" y="259" text-anchor="middle" font-size="11" font-weight="700" fill="#0f172a">ConfigMap</text>
  <text x="435" y="275" text-anchor="middle" font-size="9" fill="#6b7280">일반 설정</text>
  <rect x="500" y="240" width="90" height="50" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="545" y="259" text-anchor="middle" font-size="11" font-weight="700" fill="#0f172a">Secret</text>
  <text x="545" y="275" text-anchor="middle" font-size="9" fill="#6b7280">민감 정보</text>
  <path d="M 435 240 Q 470 220, 580 145" fill="none" stroke="#475569" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#k3-p)"/>
  <path d="M 545 240 Q 565 220, 580 195" fill="none" stroke="#475569" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#k3-p)"/>
</svg>
</div>

*그림 3-7. Kubernetes 리소스 관계*

각 Kubernetes 리소스의 역할을 정리하면 다음과 같습니다.

| 리소스 | 역할 |
|---|---|
| **ConfigMap** | 일반 환경변수(DB 주소 등)를 외부에서 주입합니다. |
| **Secret** | DB 계정·비밀번호 같은 민감 정보를 분리해 관리합니다. |
| **Deployment** | Pod를 어떻게 실행할지 정의하고, ConfigMap과 Secret을 한꺼번에 주입합니다. |
| **Service** | Pod에 고정 주소를 부여해 클러스터 안에서 안정적으로 통신할 수 있게 합니다. |
| **Ingress** | 클러스터 외부 요청을 클러스터 안으로 들여보냅니다. |

나머지 서비스(product, user, delivery)도 동일한 패턴입니다. 전체 YAML 파일은 레포의 `k8s/` 디렉토리를 참고하세요.

:::tip
**Gateway API로 두면 로컬 설정을 클라우드로 그대로 옮기기 쉽다**

이 책은 외부 진입을 Ingress로 구성하지만, 후속 표준인 **Gateway API(우리가 만든 Gateway와 다름)** 를 쓰는 방법도 있습니다. Gateway API는 외부 진입점과 경로 규칙을 따로 정의합니다.

이렇게 나뉘어 있으면 로컬에서 클라우드로 옮길 때 편합니다. 경로 규칙은 그대로 두고, 진입점만 환경에 맞게 바꾸면 됩니다. 게다가 AWS EKS 같은 클라우드에서는 진입점조차 직접 만들 필요가 없습니다. 클라우드가 Gateway API 설정을 읽어 로드 밸런서를 자동으로 붙여 주기 때문입니다.
:::

## 3.7 Minikube - 실행 및 결과 확인

### 3.7.1 Minikube 시작

Minikube는 로컬 PC에 가벼운 Kubernetes 클러스터를 만들어주는 도구입니다. 설치되어 있지 않다면 OS에 맞게 먼저 설치합니다.

**[터미널] Minikube 설치**
```bash
# macOS
brew install minikube

# Windows
winget install Kubernetes.minikube
```

설치한 뒤 새 터미널을 열고, Docker Desktop이 실행 중인 상태에서 아래 명령을 입력하면 클러스터가 생성됩니다.

**[터미널] Minikube 시작**
```bash
minikube start
```

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">minikube start</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-label">😄</span>&nbsp;&nbsp;minikube v1.34.0 on Microsoft Windows 11</div>
    <div><span class="tl-label">✨</span>&nbsp;&nbsp;Automatically selected the docker driver</div>
    <div><span class="tl-label">📦</span>&nbsp;&nbsp;Using image gcr.io/k8s-minikube/kicbase:v0.0.45</div>
    <div><span class="tl-label">🔥</span>&nbsp;&nbsp;Creating docker container (CPUs=2, Memory=4000MB)</div>
    <div><span class="tl-label">🐳</span>&nbsp;&nbsp;Preparing Kubernetes <span class="tl-str">v1.31.0</span> on Docker 27.2.0</div>
    <div class="tl-divider"><span class="tl-val">Done! kubectl is now configured to use minikube cluster</span><span class="tl-cursor"></span></div>
  </div>
</div>

*그림 3-8. Minikube 시작*

### 3.7.2 이미지 빌드

`minikube image build`는 Minikube 내부에 직접 이미지를 빌드합니다.

**[터미널] 이미지 빌드**
```bash
minikube image build -t metacoding/db:1 ./db
minikube image build -t metacoding/order:1 ./order
minikube image build -t metacoding/product:1 ./product
minikube image build -t metacoding/user:1 ./user
minikube image build -t metacoding/delivery:1 ./delivery
minikube image build -t metacoding/gateway:1 ./gateway
```

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">minikube image build · 6개 서비스</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-label">→</span> Successfully tagged <span class="tl-str">metacoding/db:1</span></div>
    <div><span class="tl-label">→</span> Successfully tagged <span class="tl-str">metacoding/order:1</span></div>
    <div><span class="tl-label">→</span> Successfully tagged <span class="tl-str">metacoding/product:1</span></div>
    <div><span class="tl-label">→</span> Successfully tagged <span class="tl-str">metacoding/user:1</span></div>
    <div><span class="tl-label">→</span> Successfully tagged <span class="tl-str">metacoding/delivery:1</span></div>
    <div><span class="tl-label">→</span> Successfully tagged <span class="tl-str">metacoding/gateway:1</span></div>
    <div class="tl-divider"><span class="tl-val">6개 이미지 빌드 완료</span><span class="tl-cursor"></span></div>
  </div>
</div>

*그림 3-9. 이미지 빌드 결과*

### 3.7.3 배포 순서

네임스페이스를 먼저 생성하고, DB가 준비된 뒤에 나머지 서비스를 배포합니다.

**[터미널] 배포 순서**
```bash
# 1. 네임스페이스 생성
kubectl create namespace metacoding

# 2. DB 관련 리소스 먼저 배포
kubectl apply -f k8s/db

# 3. 각 서비스 배포
kubectl apply -f k8s/order
kubectl apply -f k8s/product
kubectl apply -f k8s/user
kubectl apply -f k8s/delivery
kubectl apply -f k8s/gateway

# 4. Ingress 활성화 (Minikube에서는 애드온 활성화 필요)
minikube addons enable ingress
```

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">kubectl apply · 네임스페이스 + 6개 서비스</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-label">namespace</span>/metacoding <span class="tl-val">created</span></div>
    <div><span class="tl-label">secret</span>/db-secret <span class="tl-val">created</span></div>
    <div><span class="tl-label">deployment.apps</span>/db-deploy <span class="tl-val">created</span></div>
    <div><span class="tl-label">service</span>/db-service <span class="tl-val">created</span></div>
    <div><span class="tl-label">configmap</span>/order-configmap <span class="tl-val">created</span></div>
    <div><span class="tl-label">secret</span>/order-secret <span class="tl-val">created</span></div>
    <div><span class="tl-label">deployment.apps</span>/order-deploy <span class="tl-val">created</span></div>
    <div><span class="tl-label">service</span>/order-service <span class="tl-val">created</span></div>
    <div class="tl-kv-row tl-dim">… product · user · delivery · gateway 동일 패턴 …</div>
    <div><span class="tl-label">ingress.networking.k8s.io</span>/gateway-ingress <span class="tl-val">created</span></div>
    <div class="tl-divider"><span class="tl-val">전체 리소스 배포 완료</span><span class="tl-cursor"></span></div>
  </div>
</div>

*그림 3-10. 네임스페이스 생성 및 배포*

### 3.7.4 배포 상태 확인

배포가 끝나면 모든 Pod가 제대로 실행되고 있는지 확인합니다.

**[터미널] Pod 상태 확인**
```bash
kubectl get pods -n metacoding
```

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">kubectl get pods -n metacoding</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div class="tl-kv-row"><span class="tl-label">NAME</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-label">READY</span>&nbsp;&nbsp;<span class="tl-label">STATUS</span>&nbsp;&nbsp;&nbsp;<span class="tl-label">AGE</span></div>
    <div class="tl-kv-row">db-deploy-6f9b7c4d8-m4t2q&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">42s</span></div>
    <div class="tl-kv-row">gateway-deploy-5c8d6f7b9-h7w3r&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">38s</span></div>
    <div class="tl-kv-row">order-deploy-8b7f6c9d4-q2k8m&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">36s</span></div>
    <div class="tl-kv-row">product-deploy-7c9d8b6f5-x4r2t&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">35s</span></div>
    <div class="tl-kv-row">user-deploy-6d8c7b9f4-p3m9k&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">33s</span></div>
    <div class="tl-kv-row">delivery-deploy-9f7c8b6d5-t6w2x&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">30s</span></div>
    <div class="tl-divider"><span class="tl-val">모든 Pod Running</span><span class="tl-cursor"></span></div>
  </div>
</div>

*그림 3-11. Pod 상태 확인*

모든 Pod가 `Running` 상태가 되면 배포 완료입니다.

### 3.7.5 서비스 접근

Ingress를 통해 외부에서 접속하려면 `minikube tunnel`을 실행합니다.

**[터미널] 외부 접근 터널**
```bash
minikube tunnel
```

`minikube tunnel`은 터미널을 점유합니다.

터널이 실행되면 `http://127.0.0.1:80`로 gateway-service에 접속할 수 있습니다. 회원 서비스가 발급한 토큰은 하루 동안 유효하므로, 챕터 2에서 받은 토큰을 그대로 써서 아래 주문을 생성합니다. 만료됐다면 같은 방법으로 다시 발급받습니다.

MacBook Pro(상품 ID 1) 1개를 배달 주소와 함께 주문합니다.

**[Hoppscotch] 주문 생성**
```json
POST http://127.0.0.1:80/api/orders

{
  "productId": 1,
  "quantity": 1,
  "price": 2500000,
  "address": "Addr 4"
}
```

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH03/terminal/08_order-result.png)

*그림 3-12. 주문 결과 확인*

테스트가 끝났으면 이번 챕터에서 실행한 리소스를 정리합니다.

**[터미널] 리소스 정리**
```bash
kubectl delete namespace metacoding
```

**오픈이**: "쿠버네티스 위에서도 주문이 문제없이 만들어졌어요. 구조도 한결 깔끔해졌어요."

**선배**: "맞아요. 이제 결합도가 낮아졌으니, 서비스를 수정해도 컨트롤러는 영향을 받지 않아요."

다음 챕터에서는 동기 호출 방식에서 메시지를 통한 비동기 호출 방식으로 전환합니다.

:::remember
**이것만은 기억하자**

- **DDD**로 비즈니스 규칙을 서비스가 아니라 도메인 객체에 둡니다.
- **클린 아키텍처**(UseCase 인터페이스)로 컨트롤러가 구현이 아닌 인터페이스에 의존합니다. 덕분에 환경이나 테스트에 따라 구현을 바꿀 수 있습니다.
- **Nginx API Gateway**로 여러 서비스의 진입점을 하나로 모으고, URL 경로에 따라 알맞은 서비스로 전달합니다.
- **Kubernetes**로 원하는 상태를 선언하면, 컨테이너가 내려가도 그 상태를 유지합니다.
:::



---


# 챕터 4. 비동기 MSA - Kafka로 서비스를 분리하다

동기 호출로 서비스를 운영한 지 며칠 뒤, 오픈이는 에러 로그가 갑자기 늘어나는 것을 확인했습니다. 상품 서비스가 죽은 것이 원인이었습니다. 이후 쿠버네티스가 상품 서비스를 복구하자 에러 로그도 멈췄습니다.

문제는 그 사이에 들어온 주문이 전부 실패한 것입니다. 주문 서비스가 상품 서비스를 호출했지만, 상품 서비스가 죽어 있어 주문 실패가 발생했습니다.

*서로 직접 호출하니까, 하나가 죽으면 호출한 쪽도 같이 실패하는구나.*

상황을 확인한 선배가 다가왔습니다.

**선배**: "이거 지난번에 얘기했던 것처럼, 서비스끼리 동기적으로 직접 호출해서 그래요. 호출한 쪽은 상대가 응답할 때까지 기다리는데, 그 상대가 죽으면 결국 요청이 실패하는 거죠. 그래서 MSA는 동기 방식보다 메시지를 주고받는 비동기 방식을 써야 해요."

**오픈이**: "메시지요? 메시지 방식은 어떻게 다른가요?"

**선배**: "보내는 쪽은 메시지를 발행하고, 응답을 기다리지 않고 다음 작업을 진행해요. 받는 쪽은 자기 차례에 그 메시지를 읽고 다시 메시지를 발행하죠. 메시지는 한 번 발행되면 바로 사라지지 않아서, 받는 쪽이 잠깐 죽어도 메시지는 그대로 남아 있다가 복구되면 그때 처리돼요."

<div class="svg-figure">
<svg viewBox="0 0 1200 880" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="챕터 4 한눈에 보기: 챕터 3과 동일하게 Client는 클러스터 밖에 있고, 1단계 로그인은 Client가 Ingress·Gateway를 거쳐 User에 로그인하고 JWT를 응답받는다. 2단계 주문은 Client가 Ingress·Gateway를 거쳐 Order에 동기 REST로 주문하고 즉시 PENDING을 응답받는다. 그 뒤 Order·Product·Delivery 세 서비스는 가운데 Orchestrator와 event·command를 주고받고, Orchestrator가 그 모든 메시지를 아래 Kafka 토픽으로 비동기 전달한다. 서비스끼리는 직접 호출하지 않는다.">
  <defs>
    <marker id="c4f0-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="600" y="26" text-anchor="middle" font-size="20" font-weight="700" fill="#0f172a">챕터 4 한눈에 보기 — 1단계 로그인은 챕터 3과 동일, 2단계 주문은 Kafka 비동기</text>
  <rect x="200" y="58" width="980" height="760" rx="14" fill="none" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="6,4"/>
  <text x="220" y="78" font-size="13" font-weight="700" fill="#3730a3">Kubernetes 클러스터 · metacoding</text>
  <text x="36" y="98" font-size="15" font-weight="700" fill="#475569">1단계 — 로그인</text>
  <rect x="20" y="108" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="90" y="141" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">Client</text>
  <text x="90" y="164" text-anchor="middle" font-size="13" fill="#6b7280">사용자</text>
  <rect x="290" y="108" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="360" y="141" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">Ingress</text>
  <text x="360" y="164" text-anchor="middle" font-size="13" fill="#6b7280">외부 진입점</text>
  <rect x="510" y="108" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="580" y="141" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">Gateway</text>
  <text x="580" y="164" text-anchor="middle" font-size="13" fill="#6b7280">Nginx 라우팅</text>
  <rect x="720" y="108" width="170" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="805" y="141" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">User</text>
  <text x="805" y="164" text-anchor="middle" font-size="13" fill="#6b7280">:8083 회원</text>
  <line x1="160" y1="140" x2="288" y2="140" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f0-a)"/>
  <text x="225" y="132" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">1. 요청</text>
  <line x1="430" y1="140" x2="508" y2="140" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f0-a)"/>
  <text x="470" y="132" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">2. 라우팅</text>
  <line x1="650" y1="140" x2="718" y2="140" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f0-a)"/>
  <text x="685" y="132" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">3. 로그인</text>
  <line x1="718" y1="168" x2="652" y2="168" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f0-a)"/>
  <text x="685" y="181" text-anchor="middle" font-size="15" font-weight="600" fill="#3730a3">4. 응답</text>
  <line x1="508" y1="168" x2="432" y2="168" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f0-a)"/>
  <text x="470" y="181" text-anchor="middle" font-size="15" font-weight="600" fill="#3730a3">5. 응답</text>
  <line x1="288" y1="168" x2="162" y2="168" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f0-a)"/>
  <text x="225" y="181" text-anchor="middle" font-size="15" font-weight="600" fill="#3730a3">6. JWT 응답</text>
  <text x="36" y="258" font-size="15" font-weight="700" fill="#475569">2단계 — 주문 생성</text>
  <rect x="20" y="268" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="90" y="301" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">Client</text>
  <text x="90" y="324" text-anchor="middle" font-size="13" fill="#6b7280">사용자</text>
  <rect x="290" y="268" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="360" y="301" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">Ingress</text>
  <text x="360" y="324" text-anchor="middle" font-size="13" fill="#6b7280">외부 진입점</text>
  <rect x="510" y="268" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="580" y="301" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">Gateway</text>
  <text x="580" y="324" text-anchor="middle" font-size="13" fill="#6b7280">Nginx 라우팅</text>
  <line x1="160" y1="300" x2="288" y2="300" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f0-a)"/>
  <text x="225" y="292" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">7. 요청</text>
  <line x1="430" y1="300" x2="508" y2="300" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f0-a)"/>
  <text x="470" y="292" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">8. 라우팅</text>
  <line x1="560" y1="348" x2="390" y2="430" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f0-a)"/>
  <text x="450" y="392" text-anchor="end" font-size="15" font-weight="600" fill="#4f46e5">9. 주문 생성</text>
  <line x1="430" y1="430" x2="600" y2="348" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f0-a)"/>
  <text x="536" y="392" text-anchor="start" font-size="15" font-weight="600" fill="#3730a3">10. 응답</text>
  <line x1="508" y1="326" x2="432" y2="326" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f0-a)"/>
  <text x="470" y="342" text-anchor="middle" font-size="15" font-weight="600" fill="#3730a3">11. 응답</text>
  <line x1="288" y1="326" x2="162" y2="326" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f0-a)"/>
  <text x="225" y="342" text-anchor="middle" font-size="13" font-weight="600" fill="#3730a3">12. PENDING 응답</text>
  <rect x="300" y="430" width="170" height="80" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="385" y="463" text-anchor="middle" font-size="19" font-weight="700" fill="#3730a3">Order</text>
  <text x="385" y="486" text-anchor="middle" font-size="13" fill="#3730a3">:8081 주문</text>
  <rect x="560" y="430" width="170" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="645" y="463" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">Product</text>
  <text x="645" y="486" text-anchor="middle" font-size="13" fill="#6b7280">:8082 상품</text>
  <rect x="820" y="430" width="170" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="905" y="463" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">Delivery</text>
  <text x="905" y="486" text-anchor="middle" font-size="13" fill="#6b7280">:8084 배달</text>
  <rect x="360" y="588" width="580" height="68" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <rect x="360" y="588" width="580" height="20" fill="#ff7849"/>
  <text x="650" y="603" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">Kafka — 모든 메시지가 토픽을 거쳐 비동기적으로 전달</text>
  <rect x="410" y="618" width="76" height="28" rx="2" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M410 618 L448 631 L486 618" fill="none" stroke="#ff7849" stroke-width="1"/>
  <rect x="530" y="618" width="76" height="28" rx="2" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M530 618 L568 631 L606 618" fill="none" stroke="#ff7849" stroke-width="1"/>
  <rect x="650" y="618" width="76" height="28" rx="2" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M650 618 L688 631 L726 618" fill="none" stroke="#ff7849" stroke-width="1"/>
  <rect x="770" y="618" width="76" height="28" rx="2" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M770 618 L808 631 L846 618" fill="none" stroke="#ff7849" stroke-width="1"/>
  <rect x="320" y="716" width="620" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
  <text x="630" y="750" text-anchor="middle" font-size="24" font-weight="700" fill="#312e81">Orchestrator</text>
  <text x="630" y="774" text-anchor="middle" font-size="13" font-weight="600" fill="#312e81">흐름을 결정하는 지휘자</text>
  <line x1="370" y1="512" x2="370" y2="586" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f0-a)"/>
  <text x="356" y="552" text-anchor="end" font-size="13" font-weight="600" fill="#3730a3"><tspan font-size="20" font-weight="700">❶</tspan> 주문 생성 발행</text>
  <line x1="400" y1="586" x2="400" y2="512" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f0-a)"/>
  <text x="414" y="552" text-anchor="start" font-size="13" font-weight="600" fill="#4f46e5"><tspan font-size="20" font-weight="700">❻</tspan> 주문 완료 명령</text>
  <line x1="630" y1="512" x2="630" y2="586" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f0-a)"/>
  <text x="616" y="552" text-anchor="end" font-size="13" font-weight="600" fill="#3730a3"><tspan font-size="20" font-weight="700">❸</tspan> 재고 차감 결과</text>
  <line x1="660" y1="586" x2="660" y2="512" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f0-a)"/>
  <text x="674" y="552" text-anchor="start" font-size="13" font-weight="600" fill="#4f46e5"><tspan font-size="20" font-weight="700">❷</tspan> 재고 차감 명령</text>
  <line x1="890" y1="512" x2="890" y2="586" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c4f0-a)"/>
  <text x="876" y="552" text-anchor="end" font-size="13" font-weight="600" fill="#3730a3"><tspan font-size="20" font-weight="700">❺</tspan> 배달 생성 결과</text>
  <line x1="920" y1="586" x2="920" y2="512" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c4f0-a)"/>
  <text x="934" y="552" text-anchor="start" font-size="13" font-weight="600" fill="#4f46e5"><tspan font-size="20" font-weight="700">❹</tspan> 배달 생성 명령</text>
  <line x1="615" y1="660" x2="615" y2="714" stroke="#4f46e5" stroke-width="2.4" marker-end="url(#c4f0-a)"/>
  <text x="603" y="690" text-anchor="end" font-size="13" font-weight="700" fill="#4f46e5">발행</text>
  <line x1="645" y1="714" x2="645" y2="662" stroke="#4f46e5" stroke-width="2.4" stroke-dasharray="4,3" marker-end="url(#c4f0-a)"/>
  <text x="657" y="690" text-anchor="start" font-size="13" font-weight="700" fill="#3730a3">구독</text>
  <text x="600" y="846" text-anchor="middle" font-size="21" fill="#6b7280" font-style="italic">서비스끼리 직접 호출하지 않고, Kafka로 메시지를 비동기로 주고받습니다.</text>
</svg>
</div>

*그림 4-1. 챕터 4 한눈에 보기 - 서비스·Orchestrator·Kafka 3층 구조*

:::goal
**이번 챕터가 끝나면**

- 동기 호출의 한계와 **비동기 메시지** 방식을 이해할 수 있습니다.
- **Kafka**로 메시지를 발행하고 구독하는 방식을 이해할 수 있습니다.
- **orchestrator**가 여러 서비스의 주문 흐름을 조율하는 방식을 이해할 수 있습니다.
- 분산 트랜잭션을 **Saga 패턴**으로 단계별 처리하고, 실패 시 **보상 트랜잭션**으로 되돌리는 방식을 이해할 수 있습니다.
:::

::::prep
**준비하기**. 실습 시작 전 한 번만 설정

### 1. 소스 코드 클론

**[터미널] 레포 클론**
```bash
git clone https://github.com/metacoding-12-msa/ex03.git
cd ex03
```

### 2. 파일 구조

**ex03 디렉토리**
```text
ex03/
├── order/              # 포트 8081
├── product/            # 포트 8082
├── user/               # 포트 8083
├── delivery/           # 포트 8084
├── orchestrator/       # Kafka 워크플로우 조율 (이번 챕터 신규)
├── gateway/            # Nginx API Gateway
├── db/                 # MySQL
└── k8s/                # Kubernetes YAML 파일 (kafka 포함)
```

서비스마다 패키지 구조가 조금씩 다르므로, 코드를 작성할 파일 경로는 각 실습 코드블록 바로 위에서 안내합니다.

### 3. Kafka

이 챕터는 Kafka를 별도로 설치하지 않습니다. Kubernetes YAML(`k8s/kafka/`)로 Minikube 안에 띄우므로, 챕터 3에서 준비한 Docker Desktop과 Minikube만 있으면 됩니다.

### 4. 실습 순서

1. order-service의 REST 호출을 Kafka 이벤트 발행으로 교체
2. product-service · delivery-service에 Kafka Consumer/Producer 추가
3. 새 서비스 **orchestrator**에서 워크플로우 조율 로직 작성
4. Kubernetes에 Kafka + orchestrator 배포
5. 정상 주문 / 품절 보상 시나리오 검증
::::

## 4.1 동기 호출의 한계 - 한 서비스가 멈추면 전체가 멈춘다

동기적 방식과 비동기적 방식을 비유를 통해 알아보겠습니다.

### 4.1.1 카운터 대기 vs 진동벨

먼저 커피를 주문하면 카운터에서 대기하는 방식입니다. 내가 주문한 커피가 나와야 다음 손님이 주문할 수 있습니다. 만약 커피 머신이 고장 나면 뒤에 줄 선 손님 전부가 기다려야 합니다. 이렇게 요청을 보낸 쪽이 응답이 올 때까지 기다리는 방식이 **동기(synchronous)** 호출입니다.

반대로 커피 주문 후 진동벨을 받으면 자리에 앉아 다른 일을 할 수 있습니다. 커피가 완성되면 벨이 울립니다. 뒤에 줄 선 손님도 곧바로 주문할 수 있습니다. 커피 머신이 멈춰도 주문을 먼저 받아 두고, 고친 뒤에 처리할 수 있습니다. 이렇게 요청을 보낸 쪽이 기다리지 않고 결과가 준비되면 따로 받는 방식이 **비동기(asynchronous)** 호출입니다.

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH04/gemini/01_sync-vs-async.png)
*그림 4-2. 동기 vs 비동기 통신*

카페의 진동벨처럼, MSA의 서비스도 비동기 통신을 위해 메시지를 사용합니다. 그렇다면 이 메시지는 어떤 방식으로 주고받을까요?

## 4.2 Kafka - 메시지를 전달하는 우체국

### 4.2.1 프로듀서·토픽·컨슈머

MSA 구조에서 비동기 메시지는 **Kafka**를 통해 주고받습니다. Kafka는 시스템 사이에서 비동기 통신을 담당하며, 메시지를 안전하게 전달해 주는 역할을 합니다.

:::term-box
**Apache Kafka**는 대량의 메시지를 빠르고 안정적으로 주고받기 위해 만들어진 **분산 메시지 시스템**입니다. 받은 메시지를 바로 지우지 않고 일정 기간 보관하기 때문에, 필요하면 **지난 메시지를 다시 꺼내 볼 수도** 있습니다. **높은 처리량과 확장성** 덕분에 대규모 서비스에서 널리 사용합니다.
:::

Kafka는 우체국과 같은 역할을 합니다. 발신자가 우편을 부치면, 우체국은 **일반 편지, 등기, 특송, 택배처럼 종류별로 나눠** 따로 보관합니다. 그리고 **집배원은 자기 담당의 칸에서만 우편을 꺼내 갑니다**. 우체국을 사이에 두고 우편을 주고받기 때문에, 비동기적으로 각자의 시간에 일을 처리할 수 있습니다.

<div class="svg-figure">
<svg viewBox="0 0 1180 470" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Kafka 우체국: 프로듀서가 우편을 부치면 우체국이 종류별 우편함에 보관하고 집배원(컨슈머)이 자기 우편함에서 가져간다">
  <defs>
    <marker id="ka" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="kb" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  </defs>
  <text x="590" y="38" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">Kafka 우체국 — 부치고 · 보관되고 · 집배원이 가져간다</text>
  <g transform="translate(58 196)">
    <rect x="46" y="78" width="8" height="40" fill="#4f46e5"/>
    <rect x="14" y="34" width="72" height="48" rx="6" fill="#fff" stroke="#4f46e5" stroke-width="2"/>
    <path d="M14 46 Q14 34 26 34 L74 34 Q86 34 86 46" fill="#eef2ff" stroke="#4f46e5" stroke-width="2"/>
    <rect x="30" y="42" width="40" height="5" rx="2" fill="#4f46e5"/>
    <g transform="translate(34 6)">
      <rect x="0" y="0" width="34" height="22" rx="2" fill="#fff" stroke="#4f46e5" stroke-width="1.6" transform="rotate(-12 17 11)"/>
      <path d="M0 0 L17 12 L34 0" fill="none" stroke="#4f46e5" stroke-width="1.6" transform="rotate(-12 17 11)"/>
    </g>
  </g>
  <text x="108" y="340" text-anchor="middle" font-size="15" font-weight="700" fill="#3730a3">프로듀서</text>
  <text x="108" y="362" text-anchor="middle" font-size="12.5" fill="#64748b">발신자</text>
  <g transform="translate(196 240)">
    <rect x="0" y="0" width="40" height="26" rx="3" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.5"/>
    <path d="M0 0 L20 15 L40 0" fill="none" stroke="#4f46e5" stroke-width="1.5"/>
  </g>
  <path d="M300 156 L590 116 L880 156 Z" fill="#ffedd5" stroke="#ff7849" stroke-width="2.4" stroke-linejoin="round"/>
  <rect x="300" y="156" width="580" height="248" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="2.4"/>
  <rect x="300" y="156" width="580" height="34" fill="#ff7849"/>
  <text x="590" y="179" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">우체국 · KAFKA</text>
  <g>
    <rect x="324" y="214" width="166" height="118" rx="6" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
    <text x="407" y="238" text-anchor="middle" font-size="12" font-weight="700" fill="#9a3412">일반 편지 (토픽)</text>
    <rect x="382" y="262" width="50" height="34" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.2"/>
    <path d="M382 262 L407 281 L432 262" fill="none" stroke="#ff7849" stroke-width="1.2"/>
    <rect x="507" y="214" width="166" height="118" rx="6" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
    <text x="590" y="238" text-anchor="middle" font-size="12" font-weight="700" fill="#9a3412">등기 (토픽)</text>
    <rect x="565" y="262" width="50" height="34" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.2"/>
    <path d="M565 262 L590 281 L615 262" fill="none" stroke="#ff7849" stroke-width="1.2"/>
    <rect x="690" y="214" width="166" height="118" rx="6" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
    <text x="773" y="238" text-anchor="middle" font-size="12" font-weight="700" fill="#9a3412">특송 (토픽)</text>
    <rect x="748" y="262" width="50" height="34" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.2"/>
    <path d="M748 262 L773 281 L798 262" fill="none" stroke="#ff7849" stroke-width="1.2"/>
  </g>
  <text x="590" y="356" text-anchor="middle" font-size="12.5" font-weight="700" fill="#9a3412">종류별 우편함 · 토픽</text>
  <g transform="translate(998 206)">
    <path d="M30 24 Q44 12 58 24 Z" fill="#eef2ff" stroke="#4f46e5" stroke-width="2" stroke-linejoin="round"/>
    <line x1="22" y1="24" x2="66" y2="24" stroke="#4f46e5" stroke-width="2.4" stroke-linecap="round"/>
    <circle cx="44" cy="42" r="14" fill="#fff" stroke="#4f46e5" stroke-width="2"/>
    <path d="M16 104 Q16 64 44 64 Q72 64 72 104" fill="#fff" stroke="#4f46e5" stroke-width="2" stroke-linejoin="round"/>
    <line x1="40" y1="66" x2="74" y2="98" stroke="#4f46e5" stroke-width="2"/>
    <rect x="60" y="92" width="40" height="32" rx="4" fill="#eef2ff" stroke="#4f46e5" stroke-width="2"/>
    <path d="M60 100 L100 100" stroke="#4f46e5" stroke-width="1.6"/>
    <rect x="74" y="86" width="12" height="8" rx="2" fill="#4f46e5"/>
  </g>
  <text x="1042" y="362" text-anchor="middle" font-size="15" font-weight="700" fill="#3730a3">컨슈머</text>
  <text x="1042" y="384" text-anchor="middle" font-size="12.5" fill="#64748b">집배원</text>
  <line x1="246" y1="253" x2="296" y2="253" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#ka)"/>
  <text x="220" y="226" text-anchor="middle" font-size="13.5" font-weight="700" fill="#4f46e5">부치기</text>
  <line x1="884" y1="253" x2="990" y2="253" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#kb)"/>
  <text x="937" y="226" text-anchor="middle" font-size="13.5" font-weight="700" fill="#3730a3">가져가기</text>
</svg>
</div>

*그림 4-3. Kafka 우체국 - 메시지를 종류별로 보관하고 전달하는 구조*

그림 4-3의 Kafka 요소의 역할을 정리하면 다음과 같습니다.

| 구성요소 | 우체국 비유 | 하는 일 |
|---|---|---|
| **Kafka** | 우체국 | 메시지를 받아 보관하고 전달 |
| **토픽(Topic)** | 종류별 우편함 (일반/등기/특송 등) | 메시지를 목적별로 나눠 담음 |
| **프로듀서(Producer)** | 발신자 | 토픽에 메시지를 발행 |
| **컨슈머(Consumer)** | 집배원 | 토픽을 구독해 메시지를 처리 |

프로듀서가 토픽에 메시지를 보내는 것을 **발행**(Publish), 컨슈머가 특정 토픽을 지정해 두고 메시지를 가져와 처리하는 것을 **구독**(Subscribe)이라고 합니다.

우체국이 우편을 일반·등기·특송으로 나눠 담듯, Kafka도 메시지를 **토픽이라는 우편함에 종류별로 나눠 담습니다**. **토픽마다 이름이 있어서**, 프로듀서는 보낼 메시지에 맞는 **토픽 이름으로 발행**하고 컨슈머는 자기가 맡은 **토픽 이름으로 구독**합니다.

<div class="svg-figure">
<svg viewBox="0 0 1180 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Kafka 구조: 프로듀서가 재고 차감 토픽에 메시지를 발행하면 컨슈머가 구독해 가져간다">
  <defs>
    <marker id="k4a" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="k4b" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  </defs>
  <text x="590" y="36" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">실제 Kafka — 프로듀서가 토픽에 발행하면 컨슈머가 구독한다</text>
  <g transform="translate(70 164)">
    <rect x="0" y="0" width="134" height="96" rx="8" fill="#fff" stroke="#4f46e5" stroke-width="2"/>
    <line x1="0" y1="32" x2="134" y2="32" stroke="#4f46e5" stroke-width="1.2"/>
    <line x1="0" y1="64" x2="134" y2="64" stroke="#4f46e5" stroke-width="1.2"/>
    <circle cx="18" cy="16" r="3.2" fill="#4f46e5"/><circle cx="18" cy="48" r="3.2" fill="#4f46e5"/><circle cx="18" cy="80" r="3.2" fill="#4f46e5"/>
  </g>
  <text x="137" y="290" text-anchor="middle" font-size="15" font-weight="700" fill="#3730a3">프로듀서</text>
  <line x1="208" y1="212" x2="366" y2="212" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#k4a)"/>
  <text x="287" y="198" text-anchor="middle" font-size="13.5" font-weight="700" fill="#4f46e5">발행</text>
  <rect x="384" y="112" width="400" height="200" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="2.4"/>
  <rect x="384" y="112" width="400" height="34" fill="#ff7849"/>
  <text x="584" y="135" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">KAFKA</text>
  <rect x="410" y="170" width="348" height="122" rx="6" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="584" y="204" text-anchor="middle" font-size="14" font-weight="700" fill="#9a3412">재고 차감</text>
  <text x="584" y="227" text-anchor="middle" font-size="11" fill="#c2773f">decrease-product-command</text>
  <rect x="559" y="250" width="50" height="34" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.2"/>
  <path d="M559 250 L584 269 L609 250" fill="none" stroke="#ff7849" stroke-width="1.2"/>
  <line x1="786" y1="212" x2="944" y2="212" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#k4b)"/>
  <text x="865" y="198" text-anchor="middle" font-size="13.5" font-weight="700" fill="#3730a3">구독</text>
  <g transform="translate(960 164)">
    <rect x="0" y="0" width="134" height="96" rx="8" fill="#fff" stroke="#4f46e5" stroke-width="2"/>
    <line x1="0" y1="32" x2="134" y2="32" stroke="#4f46e5" stroke-width="1.2"/>
    <line x1="0" y1="64" x2="134" y2="64" stroke="#4f46e5" stroke-width="1.2"/>
    <circle cx="18" cy="16" r="3.2" fill="#4f46e5"/><circle cx="18" cy="48" r="3.2" fill="#4f46e5"/><circle cx="18" cy="80" r="3.2" fill="#4f46e5"/>
  </g>
  <text x="1027" y="290" text-anchor="middle" font-size="15" font-weight="700" fill="#3730a3">컨슈머</text>
</svg>
</div>

*그림 4-4. Kafka의 프로듀서·토픽·컨슈머 구조*

그렇다면 같은 일을 하는 컨슈머가 여러 대 떠 있을 때는 메시지를 어떻게 나눠 받아야 할까요?

### 4.2.2 컨슈머 그룹

상품 서비스를 2대로 늘려 운영한다고 가정해 보겠습니다. 두 서버가 같은 토픽을 구독하면 "재고 1개 차감" 메시지를 둘 다 받아 처리해, 재고가 2개 줄어듭니다. 이 중복 처리를 막아 주는 것이 **컨슈머 그룹**입니다. **같은 일을 하는 서버를 한 그룹으로 묶으면, 그 메시지는 그룹 안의 한 서버에만 전달됩니다**.

<div class="svg-figure">
<svg viewBox="0 0 980 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="컨슈머 그룹 비교: 그룹으로 안 묶으면 두 컨슈머가 같은 메시지를 각각 처리해 재고가 두 번 깎이고, 같은 컨슈머 그룹으로 묶으면 한 컨슈머만 처리해 재고가 한 번만 깎인다">
  <defs>
    <marker id="cg" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="490" y="32" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">컨슈머 그룹 — 같은 메시지를 두 번 처리하지 않게 묶는다</text>
  <text x="36" y="70" font-size="15" font-weight="700" fill="#0f172a">그룹으로 안 묶으면</text>
  <rect x="36" y="86" width="150" height="96" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="2.4"/>
  <rect x="36" y="86" width="150" height="26" fill="#ff7849"/>
  <text x="111" y="104" text-anchor="middle" font-size="11.5" font-weight="700" fill="#fff">편지 (토픽)</text>
  <rect x="58" y="124" width="106" height="44" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.4"/>
  <path d="M58 124 L111 148 L164 124" fill="none" stroke="#ff7849" stroke-width="1.4"/>
  <text x="111" y="152" text-anchor="middle" font-size="11.5" font-weight="700" fill="#9a3412">재고 1 차감</text>
  <g transform="translate(300 74)">
    <path d="M30 24 Q44 12 58 24 Z" fill="#eef2ff" stroke="#4f46e5" stroke-width="2" stroke-linejoin="round"/>
    <line x1="22" y1="24" x2="66" y2="24" stroke="#4f46e5" stroke-width="2.4" stroke-linecap="round"/>
    <circle cx="44" cy="42" r="14" fill="#fff" stroke="#4f46e5" stroke-width="2"/>
    <path d="M16 104 Q16 64 44 64 Q72 64 72 104" fill="#fff" stroke="#4f46e5" stroke-width="2" stroke-linejoin="round"/>
    <line x1="40" y1="66" x2="74" y2="98" stroke="#4f46e5" stroke-width="2"/>
    <rect x="60" y="92" width="40" height="32" rx="4" fill="#eef2ff" stroke="#4f46e5" stroke-width="2"/>
    <path d="M60 100 L100 100" stroke="#4f46e5" stroke-width="1.6"/>
    <rect x="74" y="86" width="12" height="8" rx="2" fill="#4f46e5"/>
  </g>
  <text x="354" y="216" text-anchor="middle" font-size="13" font-weight="700" fill="#3730a3">컨슈머 A</text>
  <text x="354" y="234" text-anchor="middle" font-size="11.5" fill="#4f46e5">처리</text>
  <g transform="translate(440 74)">
    <path d="M30 24 Q44 12 58 24 Z" fill="#eef2ff" stroke="#4f46e5" stroke-width="2" stroke-linejoin="round"/>
    <line x1="22" y1="24" x2="66" y2="24" stroke="#4f46e5" stroke-width="2.4" stroke-linecap="round"/>
    <circle cx="44" cy="42" r="14" fill="#fff" stroke="#4f46e5" stroke-width="2"/>
    <path d="M16 104 Q16 64 44 64 Q72 64 72 104" fill="#fff" stroke="#4f46e5" stroke-width="2" stroke-linejoin="round"/>
    <line x1="40" y1="66" x2="74" y2="98" stroke="#4f46e5" stroke-width="2"/>
    <rect x="60" y="92" width="40" height="32" rx="4" fill="#eef2ff" stroke="#4f46e5" stroke-width="2"/>
    <path d="M60 100 L100 100" stroke="#4f46e5" stroke-width="1.6"/>
    <rect x="74" y="86" width="12" height="8" rx="2" fill="#4f46e5"/>
  </g>
  <text x="494" y="216" text-anchor="middle" font-size="13" font-weight="700" fill="#3730a3">컨슈머 B</text>
  <text x="494" y="234" text-anchor="middle" font-size="11.5" fill="#4f46e5">처리</text>
  <path d="M186 138 Q250 130 314 140" fill="none" stroke="#4f46e5" stroke-width="2.2" marker-end="url(#cg)"/>
  <path d="M186 160 Q330 196 454 140" fill="none" stroke="#4f46e5" stroke-width="2.2" marker-end="url(#cg)"/>
  <rect x="620" y="98" width="324" height="92" rx="10" fill="#fff" stroke="#e7d9a8" stroke-width="1.6"/>
  <text x="640" y="132" font-size="14" fill="#0f172a">둘 다 같은 메시지를 처리해서</text>
  <text x="640" y="162" font-size="17" font-weight="700" fill="#9a3412">상품 재고 10 → 8 (두 번 깎임)</text>
  <line x1="36" y1="270" x2="944" y2="270" stroke="#e2e8f0" stroke-width="1.5"/>
  <text x="36" y="318" font-size="15" font-weight="700" fill="#0f172a">같은 컨슈머 그룹으로 묶으면</text>
  <rect x="36" y="334" width="150" height="96" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="2.4"/>
  <rect x="36" y="334" width="150" height="26" fill="#ff7849"/>
  <text x="111" y="352" text-anchor="middle" font-size="11.5" font-weight="700" fill="#fff">편지 (토픽)</text>
  <rect x="58" y="372" width="106" height="44" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.4"/>
  <path d="M58 372 L111 396 L164 372" fill="none" stroke="#ff7849" stroke-width="1.4"/>
  <text x="111" y="400" text-anchor="middle" font-size="11.5" font-weight="700" fill="#9a3412">재고 1 차감</text>
  <rect x="262" y="306" width="300" height="216" rx="14" fill="#fff" stroke="#4f46e5" stroke-width="1.8" stroke-dasharray="6 5"/>
  <text x="412" y="330" text-anchor="middle" font-size="13" font-weight="700" fill="#3730a3">하나의 컨슈머 그룹</text>
  <g transform="translate(296 350)">
    <path d="M30 24 Q44 12 58 24 Z" fill="#eef2ff" stroke="#4f46e5" stroke-width="2" stroke-linejoin="round"/>
    <line x1="22" y1="24" x2="66" y2="24" stroke="#4f46e5" stroke-width="2.4" stroke-linecap="round"/>
    <circle cx="44" cy="42" r="14" fill="#fff" stroke="#4f46e5" stroke-width="2"/>
    <path d="M16 104 Q16 64 44 64 Q72 64 72 104" fill="#fff" stroke="#4f46e5" stroke-width="2" stroke-linejoin="round"/>
    <line x1="40" y1="66" x2="74" y2="98" stroke="#4f46e5" stroke-width="2"/>
    <rect x="60" y="92" width="40" height="32" rx="4" fill="#eef2ff" stroke="#4f46e5" stroke-width="2"/>
    <path d="M60 100 L100 100" stroke="#4f46e5" stroke-width="1.6"/>
    <rect x="74" y="86" width="12" height="8" rx="2" fill="#4f46e5"/>
  </g>
  <text x="350" y="492" text-anchor="middle" font-size="13" font-weight="700" fill="#3730a3">컨슈머 A</text>
  <text x="350" y="510" text-anchor="middle" font-size="11.5" fill="#4f46e5">이 메시지 처리</text>
  <g transform="translate(440 350)" opacity="0.5">
    <path d="M30 24 Q44 12 58 24 Z" fill="#f1f5f9" stroke="#94a3b8" stroke-width="2" stroke-linejoin="round"/>
    <line x1="22" y1="24" x2="66" y2="24" stroke="#94a3b8" stroke-width="2.4" stroke-linecap="round"/>
    <circle cx="44" cy="42" r="14" fill="#fff" stroke="#94a3b8" stroke-width="2"/>
    <path d="M16 104 Q16 64 44 64 Q72 64 72 104" fill="#fff" stroke="#94a3b8" stroke-width="2" stroke-linejoin="round"/>
    <line x1="40" y1="66" x2="74" y2="98" stroke="#94a3b8" stroke-width="2"/>
    <rect x="60" y="92" width="40" height="32" rx="4" fill="#f1f5f9" stroke="#94a3b8" stroke-width="2"/>
  </g>
  <text x="494" y="492" text-anchor="middle" font-size="13" font-weight="700" fill="#94a3b8">컨슈머 B</text>
  <text x="494" y="510" text-anchor="middle" font-size="11.5" fill="#94a3b8">이 메시지는 안 받음</text>
  <path d="M186 386 Q240 380 290 388" fill="none" stroke="#4f46e5" stroke-width="2.2" marker-end="url(#cg)"/>
  <rect x="620" y="350" width="324" height="92" rx="10" fill="#fff" stroke="#e7d9a8" stroke-width="1.6"/>
  <text x="640" y="384" font-size="14" fill="#0f172a">그룹 안 한 명만 처리해서</text>
  <text x="640" y="414" font-size="17" font-weight="700" fill="#3730a3">상품 재고 10 → 9 (한 번만)</text>
</svg>
</div>

*그림 4-5. 컨슈머 그룹 - 묶으면 한 번만 처리*

:::tip
**Kafka 더 알아두기**

- **컨슈머가 읽어도 메시지는 사라지지 않는다**: Kafka는 전통적인 메시지 큐와 달리, 컨슈머가 메시지를 읽어가도 파일 시스템에 그대로 보관합니다(기본 설정은 7일). 덕분에 서로 다른 컨슈머 그룹이 동일한 메시지를 각자의 속도대로 처음부터 다시 읽을 수 있고, 장애가 발생했을 때도 원하는 시점부터 재처리가 가능합니다.
- **서버 한 대가 죽어도 메시지는 안전하다**: Kafka는 보통 여러 대의 서버를 클러스터로 묶어서 운영하며, 메시지를 여러 서버에 복제해 둡니다. 따라서 특정 서버 한 대에 장애가 발생하더라도, 복제본을 가진 다른 서버가 즉시 역할을 넘겨받기 때문에 메시지 유실 없이 서비스를 안정적으로 유지할 수 있습니다.
:::

**오픈이**: "각 서비스가 메시지 방식으로 처리하다가 중간에 실패하면, 보상 트랜잭션은 어떻게 관리하나요?"

**선배**: "그건 흐름을 누가 관리하느냐에 따라 달라요. 지금처럼 각 서비스가 서로 메시지를 발행하고 구독하며, 실패 시에도 직접 보상 메시지를 발행할 수 있어요. 다만 이 방식은 중간에 실패하면 어디까지 됐는지 알기 어려워 보상도 까다로워요. 반대로 전체 흐름을 관리하는 **지휘자**를 두고 지휘자가 메시지 발행과 구독을 관리하면, 어디까지 진행됐는지 알고 있으니 **이미 끝난 단계만 골라 되돌릴** 수 있어요."

## 4.3 Orchestration Saga - 지휘자가 흐름을 조율하다

하나의 주문을 여러 서비스가 단계별로 처리하다 보면, 중간 한 단계가 실패해도 앞 단계는 이미 데이터에 반영돼 있습니다. 이때 끝난 단계를 취소하는 **보상**으로 데이터를 맞추는 방식을 **Saga 패턴**이라고 합니다.

Saga 패턴에서 전체 흐름을 지휘자가 중앙에서 관리하는 방식을 **Orchestration Saga**라고 합니다. 흐름을 한 곳에 모으면 상태가 한 곳에 있어 추적과 보상이 단순해지고, 각 서비스는 자기 일에만 집중할 수 있습니다.

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH04/gemini/04_orchestra.png)
*그림 4-6. Orchestration Saga 구조*

챕터 2~3에서 구현한 주문 서비스 중심의 보상 트랜잭션 관리도 일종의 Orchestration Saga입니다.

이번 챕터에서는 조율 역할만 전담하는 **별도 orchestrator 서비스**를 두는 구조를 사용합니다. 주문 요청이 들어오면 orchestrator가 재고 차감, 배달 생성, 주문 완료 단계를 순차적으로 지휘합니다.

:::note
**Saga를 구현하는 방식에는 Orchestration 외에 Choreography도 있습니다.** 중앙 지휘자 없이 **각 서비스가 서로 발행하고 구독하며 다음 단계를 이어 가는 방식**으로, 단계가 적을 때는 가볍지만 단계가 늘거나 보상이 복잡해질수록 전체 흐름이 여러 서비스에 흩어져 추적이 어렵습니다. 이 책은 상태를 한 곳에서 추적할 수 있는 Orchestration을 선택합니다.
:::

### 4.3.1 이번 챕터에서 사용하는 토픽 맵

주문 흐름에서는 총 8개의 토픽을 사용합니다. 토픽은 orchestrator가 서비스에 작업을 지시하는 **명령(Command)** 과, 서비스가 결과를 돌려주는 **이벤트(Event)** 두 종류로 나뉩니다. 구분을 위해 토픽 이름에 `command`가 포함되면 명령, 없으면 이벤트로 정의합니다.

<p><strong>정상 흐름 (6단계)</strong></p>

<table>
  <colgroup>
    <col style="width:8%">
    <col style="width:40%">
    <col style="width:28%">
    <col style="width:24%">
  </colgroup>
  <thead>
    <tr><th style="text-align:center">단계</th><th>토픽</th><th>발행 → 구독</th><th>목적</th></tr>
  </thead>
  <tbody>
    <tr><td style="text-align:center">1</td><td><code>order-created</code></td><td>order → orchestrator</td><td>새 주문 발생</td></tr>
    <tr><td style="text-align:center">2</td><td><code>decrease-product-command</code></td><td>orchestrator → product</td><td>재고 감소 명령</td></tr>
    <tr><td style="text-align:center">3</td><td><code>product-decreased</code></td><td>product → orchestrator</td><td>재고 감소 결과</td></tr>
    <tr><td style="text-align:center">4</td><td><code>create-delivery-command</code></td><td>orchestrator → delivery</td><td>배달 생성 명령</td></tr>
    <tr><td style="text-align:center">5</td><td><code>delivery-created</code></td><td>delivery → orchestrator</td><td>배달 생성 결과</td></tr>
    <tr><td style="text-align:center">6</td><td><code>complete-order-command</code></td><td>orchestrator → order</td><td>주문 완료 명령</td></tr>
  </tbody>
</table>

<p><strong>보상 흐름 (2개)</strong></p>

<table>
  <colgroup>
    <col style="width:44%">
    <col style="width:30%">
    <col style="width:26%">
  </colgroup>
  <thead>
    <tr><th>토픽</th><th>발행 → 구독</th><th>목적</th></tr>
  </thead>
  <tbody>
    <tr><td><code>cancel-order-command</code></td><td>orchestrator → order</td><td>주문 취소</td></tr>
    <tr><td><code>increase-product-command</code></td><td>orchestrator → product</td><td>재고 복구</td></tr>
  </tbody>
</table>

핵심 흐름만 직접 다루므로, 각 토픽의 발행·구독 코드 전체는 깃헙 레포에서 확인합니다.

### 4.3.2 주문 요청 성공 흐름

이제 비동기 통신으로 주문 요청이 처리되는 전체 흐름을 따라가 보겠습니다.

먼저 주문 요청이 들어오면 주문 서비스는 클라이언트에게 **PENDING** 상태를 응답합니다. 이후 orchestrator가 아래 단계를 차례로 진행해 모두 성공하면 주문 상태가 **COMPLETED**로 바뀝니다.

<div class="svg-figure svg-figure--wide">
<svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg">
  <defs>
   <marker id="mk" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
   <marker id="mk2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  </defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">1단계 — 주문 생성 이벤트 발행 → 오케스트레이터 수신</text>
  <rect x="345" y="64" width="170" height="70" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
 <text x="430" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">Order</text>
 <text x="430" y="116" text-anchor="middle" font-size="14" fill="#3730a3">:8081 주문</text><rect x="575" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="660" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Product</text>
 <text x="660" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">:8082 상품</text><rect x="805" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="890" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Delivery</text>
 <text x="890" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">:8084 배달</text><rect x="280" y="250" width="780" height="120" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
 <rect x="280" y="250" width="780" height="22" fill="#ff7849"/>
 <text x="670" y="265" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">Kafka — 토픽별로 메시지를 보관·전달</text><rect x="300" y="290" width="110" height="42" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.8"/>
   <path d="M300 290 L355 311 L410 290" fill="none" stroke="#ff7849" stroke-width="1.4"/>
   <text x="355" y="350" text-anchor="middle" font-size="13" font-weight="700" fill="#9a3412">주문 생성 이벤트</text><circle cx="392" cy="298" r="10" fill="#ff7849"/><text x="392" y="302" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text><rect x="300" y="480" width="760" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
 <text x="680" y="514" text-anchor="middle" font-size="20" font-weight="700" fill="#312e81">Orchestrator</text>
 <text x="680" y="538" text-anchor="middle" font-size="14" fill="#312e81">흐름을 결정하는 지휘자 — event를 받아 다음 command를 발행</text><line x1="430" y1="134" x2="355" y2="248" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#mk)"/><text x="414.5" y="192" text-anchor="start" font-size="15" font-weight="700" fill="#4f46e5">1. 주문 생성 이벤트 발행</text><line x1="355" y1="370" x2="355" y2="478" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#mk2)"/><text x="377" y="429" text-anchor="start" font-size="15" font-weight="700" fill="#3730a3">2. 오케스트레이터가 수신</text><rect x="1090" y="40" width="460" height="510" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="550" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">1단계</text><text x="1146" y="124" font-size="21" font-weight="700" fill="#0f172a">1. 주문 생성 이벤트 발행</text><text x="1146" y="158" font-size="19" font-weight="400" fill="#475569">주문을 저장한 뒤</text><text x="1146" y="185" font-size="19" font-weight="400" fill="#475569">PENDING을 응답합니다.</text><text x="1146" y="212" font-size="19" font-weight="400" fill="#475569">그 후 <tspan font-weight="700">주문 생성 이벤트</tspan>를</text><text x="1146" y="239" font-size="19" font-weight="400" fill="#475569">카프카에 발행합니다.</text><text x="1146" y="279" font-size="21" font-weight="700" fill="#0f172a">2. 오케스트레이터가 수신</text><text x="1146" y="313" font-size="19" font-weight="400" fill="#475569">오케스트레이터가 <tspan font-weight="700">주문 생성 이벤트</tspan></text><text x="1146" y="340" font-size="19" font-weight="400" fill="#475569">토픽을 구독하고 있다가 메시지를</text><text x="1146" y="367" font-size="19" font-weight="400" fill="#475569">받아 진행 상태를 기록합니다.</text>
 </svg>
</div>

*그림 4-7. 1단계 — 주문 생성 이벤트 발행 → 오케스트레이터 수신*

<div class="svg-figure svg-figure--wide">
<svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg">
  <defs>
   <marker id="mk" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
   <marker id="mk2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  </defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">2단계 — 재고 차감 명령 발행 → 상품 수신</text>
  <rect x="345" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="430" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Order</text>
 <text x="430" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">:8081 주문</text><rect x="575" y="64" width="170" height="70" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
 <text x="660" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">Product</text>
 <text x="660" y="116" text-anchor="middle" font-size="14" fill="#3730a3">:8082 상품</text><rect x="805" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="890" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Delivery</text>
 <text x="890" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">:8084 배달</text><rect x="280" y="250" width="780" height="120" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
 <rect x="280" y="250" width="780" height="22" fill="#ff7849"/>
 <text x="670" y="265" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">Kafka — 토픽별로 메시지를 보관·전달</text><rect x="300" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M300 290 L355 311 L410 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="355" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">주문 생성 이벤트</text><rect x="425" y="290" width="110" height="42" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.8"/>
   <path d="M425 290 L480 311 L535 290" fill="none" stroke="#ff7849" stroke-width="1.4"/>
   <text x="480" y="350" text-anchor="middle" font-size="13" font-weight="700" fill="#9a3412">재고 차감 명령</text><circle cx="517" cy="298" r="10" fill="#ff7849"/><text x="517" y="302" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text><rect x="300" y="480" width="760" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
 <text x="680" y="514" text-anchor="middle" font-size="20" font-weight="700" fill="#312e81">Orchestrator</text>
 <text x="680" y="538" text-anchor="middle" font-size="14" fill="#312e81">흐름을 결정하는 지휘자 — event를 받아 다음 command를 발행</text><line x1="480" y1="478" x2="480" y2="372" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#mk)"/><text x="502" y="429" text-anchor="start" font-size="15" font-weight="700" fill="#4f46e5">3. 재고 차감 명령 발행</text><line x1="480" y1="248" x2="660" y2="136" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#mk2)"/><text x="592" y="192" text-anchor="start" font-size="15" font-weight="700" fill="#3730a3">4. 상품 서비스가 수신</text><rect x="1090" y="40" width="460" height="510" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="550" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">2단계</text><text x="1146" y="132" font-size="21" font-weight="700" fill="#0f172a">3. 재고 차감 명령 발행</text><text x="1146" y="174" font-size="19" font-weight="400" fill="#475569">오케스트레이터가 <tspan font-weight="700">재고 차감</tspan></text><text x="1146" y="207" font-size="19" font-weight="400" fill="#475569"><tspan font-weight="700">명령</tspan>을 카프카에 발행합니다.</text><text x="1146" y="240" font-size="21" font-weight="700" fill="#0f172a">4. 상품 서비스가 수신</text><text x="1146" y="282" font-size="19" font-weight="400" fill="#475569">상품 서비스가 <tspan font-weight="700">재고 차감 명령</tspan></text><text x="1146" y="315" font-size="19" font-weight="400" fill="#475569">토픽을 구독하고 있다가 메시지를</text><text x="1146" y="348" font-size="19" font-weight="400" fill="#475569">받아 재고를 차감합니다.</text>
 </svg>
</div>

*그림 4-8. 2단계 — 재고 차감 명령 발행 → 상품 수신*

<div class="svg-figure svg-figure--wide">
<svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg">
  <defs>
   <marker id="mk" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
   <marker id="mk2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  </defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">3단계 — 재고 차감 이벤트 발행(상품) → 오케스트레이터 수신</text>
  <rect x="345" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="430" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Order</text>
 <text x="430" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">:8081 주문</text><rect x="575" y="64" width="170" height="70" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
 <text x="660" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">Product</text>
 <text x="660" y="116" text-anchor="middle" font-size="14" fill="#3730a3">:8082 상품</text><rect x="805" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="890" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Delivery</text>
 <text x="890" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">:8084 배달</text><rect x="280" y="250" width="780" height="120" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
 <rect x="280" y="250" width="780" height="22" fill="#ff7849"/>
 <text x="670" y="265" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">Kafka — 토픽별로 메시지를 보관·전달</text><rect x="300" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M300 290 L355 311 L410 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="355" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">주문 생성 이벤트</text><rect x="425" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M425 290 L480 311 L535 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="480" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">재고 차감 명령</text><rect x="550" y="290" width="110" height="42" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.8"/>
   <path d="M550 290 L605 311 L660 290" fill="none" stroke="#ff7849" stroke-width="1.4"/>
   <text x="605" y="350" text-anchor="middle" font-size="13" font-weight="700" fill="#9a3412">재고 차감 이벤트</text><circle cx="642" cy="298" r="10" fill="#ff7849"/><text x="642" y="302" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text><rect x="300" y="480" width="760" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
 <text x="680" y="514" text-anchor="middle" font-size="20" font-weight="700" fill="#312e81">Orchestrator</text>
 <text x="680" y="538" text-anchor="middle" font-size="14" fill="#312e81">흐름을 결정하는 지휘자 — event를 받아 다음 command를 발행</text><line x1="660" y1="134" x2="605" y2="248" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#mk)"/><text x="654.5" y="192" text-anchor="start" font-size="15" font-weight="700" fill="#4f46e5">5. 재고 차감 이벤트 발행</text><line x1="605" y1="370" x2="605" y2="478" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#mk2)"/><text x="627" y="429" text-anchor="start" font-size="15" font-weight="700" fill="#3730a3">6. 오케스트레이터가 수신</text><rect x="1090" y="40" width="460" height="510" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="550" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">3단계</text><text x="1146" y="132" font-size="21" font-weight="700" fill="#0f172a">5. 재고 차감 이벤트 발행</text><text x="1146" y="174" font-size="19" font-weight="400" fill="#475569">상품 서비스가 재고를 줄인 뒤</text><text x="1146" y="207" font-size="19" font-weight="400" fill="#475569">성공 여부를 <tspan font-weight="700">재고 차감</tspan></text><text x="1146" y="240" font-size="19" font-weight="400" fill="#475569"><tspan font-weight="700">이벤트</tspan>로 카프카에 발행합니다.</text><text x="1146" y="273" font-size="21" font-weight="700" fill="#0f172a">6. 오케스트레이터가 수신</text><text x="1146" y="315" font-size="19" font-weight="400" fill="#475569">오케스트레이터가 <tspan font-weight="700">재고 차감 이벤트</tspan></text><text x="1146" y="348" font-size="19" font-weight="400" fill="#475569">토픽을 구독하고 있다가 메시지를</text><text x="1146" y="381" font-size="19" font-weight="400" fill="#475569">받아 성공을 확인합니다.</text>
 </svg>
</div>

*그림 4-9. 3단계 — 재고 차감 이벤트 발행(상품) → 오케스트레이터 수신*

<div class="svg-figure svg-figure--wide">
<svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg">
  <defs>
   <marker id="mk" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
   <marker id="mk2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  </defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">4단계 — 배달 생성 명령 발행 → 배달 수신</text>
  <rect x="345" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="430" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Order</text>
 <text x="430" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">:8081 주문</text><rect x="575" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="660" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Product</text>
 <text x="660" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">:8082 상품</text><rect x="805" y="64" width="170" height="70" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
 <text x="890" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">Delivery</text>
 <text x="890" y="116" text-anchor="middle" font-size="14" fill="#3730a3">:8084 배달</text><rect x="280" y="250" width="780" height="120" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
 <rect x="280" y="250" width="780" height="22" fill="#ff7849"/>
 <text x="670" y="265" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">Kafka — 토픽별로 메시지를 보관·전달</text><rect x="300" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M300 290 L355 311 L410 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="355" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">주문 생성 이벤트</text><rect x="425" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M425 290 L480 311 L535 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="480" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">재고 차감 명령</text><rect x="550" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M550 290 L605 311 L660 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="605" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">재고 차감 이벤트</text><rect x="675" y="290" width="110" height="42" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.8"/>
   <path d="M675 290 L730 311 L785 290" fill="none" stroke="#ff7849" stroke-width="1.4"/>
   <text x="730" y="350" text-anchor="middle" font-size="13" font-weight="700" fill="#9a3412">배달 생성 명령</text><circle cx="767" cy="298" r="10" fill="#ff7849"/><text x="767" y="302" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text><rect x="300" y="480" width="760" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
 <text x="680" y="514" text-anchor="middle" font-size="20" font-weight="700" fill="#312e81">Orchestrator</text>
 <text x="680" y="538" text-anchor="middle" font-size="14" fill="#312e81">흐름을 결정하는 지휘자 — event를 받아 다음 command를 발행</text><line x1="730" y1="478" x2="730" y2="372" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#mk)"/><text x="752" y="429" text-anchor="start" font-size="15" font-weight="700" fill="#4f46e5">7. 배달 생성 명령 발행</text><line x1="730" y1="248" x2="890" y2="136" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#mk2)"/><text x="832" y="192" text-anchor="start" font-size="15" font-weight="700" fill="#3730a3">8. 배달 서비스가 수신</text><rect x="1090" y="40" width="460" height="510" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="550" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">4단계</text><text x="1146" y="132" font-size="21" font-weight="700" fill="#0f172a">7. 배달 생성 명령 발행</text><text x="1146" y="174" font-size="19" font-weight="400" fill="#475569">오케스트레이터가 <tspan font-weight="700">배달 생성</tspan></text><text x="1146" y="207" font-size="19" font-weight="400" fill="#475569"><tspan font-weight="700">명령</tspan>을 카프카에 발행합니다.</text><text x="1146" y="240" font-size="21" font-weight="700" fill="#0f172a">8. 배달 서비스가 수신</text><text x="1146" y="282" font-size="19" font-weight="400" fill="#475569">배달 서비스가 <tspan font-weight="700">배달 생성 명령</tspan></text><text x="1146" y="315" font-size="19" font-weight="400" fill="#475569">토픽을 구독하고 있다가 메시지를</text><text x="1146" y="348" font-size="19" font-weight="400" fill="#475569">받아 배달을 생성합니다.</text>
 </svg>
</div>

*그림 4-10. 4단계 — 배달 생성 명령 발행 → 배달 수신*

<div class="svg-figure svg-figure--wide">
<svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg">
  <defs>
   <marker id="mk" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
   <marker id="mk2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  </defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">5단계 — 배달 생성 이벤트 발행(배달) → 오케스트레이터 수신</text>
  <rect x="345" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="430" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Order</text>
 <text x="430" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">:8081 주문</text><rect x="575" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="660" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Product</text>
 <text x="660" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">:8082 상품</text><rect x="805" y="64" width="170" height="70" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
 <text x="890" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">Delivery</text>
 <text x="890" y="116" text-anchor="middle" font-size="14" fill="#3730a3">:8084 배달</text><rect x="280" y="250" width="780" height="120" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
 <rect x="280" y="250" width="780" height="22" fill="#ff7849"/>
 <text x="670" y="265" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">Kafka — 토픽별로 메시지를 보관·전달</text><rect x="300" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M300 290 L355 311 L410 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="355" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">주문 생성 이벤트</text><rect x="425" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M425 290 L480 311 L535 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="480" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">재고 차감 명령</text><rect x="550" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M550 290 L605 311 L660 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="605" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">재고 차감 이벤트</text><rect x="675" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M675 290 L730 311 L785 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="730" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">배달 생성 명령</text><rect x="800" y="290" width="110" height="42" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.8"/>
   <path d="M800 290 L855 311 L910 290" fill="none" stroke="#ff7849" stroke-width="1.4"/>
   <text x="855" y="350" text-anchor="middle" font-size="13" font-weight="700" fill="#9a3412">배달 생성 이벤트</text><circle cx="892" cy="298" r="10" fill="#ff7849"/><text x="892" y="302" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text><rect x="300" y="480" width="760" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
 <text x="680" y="514" text-anchor="middle" font-size="20" font-weight="700" fill="#312e81">Orchestrator</text>
 <text x="680" y="538" text-anchor="middle" font-size="14" fill="#312e81">흐름을 결정하는 지휘자 — event를 받아 다음 command를 발행</text><line x1="890" y1="134" x2="855" y2="248" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#mk)"/><text x="894.5" y="192" text-anchor="start" font-size="15" font-weight="700" fill="#4f46e5">9. 배달 생성 이벤트 발행</text><line x1="855" y1="370" x2="855" y2="478" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#mk2)"/><text x="877" y="429" text-anchor="start" font-size="15" font-weight="700" fill="#3730a3">10. 오케스트레이터가 수신</text><rect x="1090" y="40" width="460" height="510" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="550" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">5단계</text><text x="1146" y="132" font-size="21" font-weight="700" fill="#0f172a">9. 배달 생성 이벤트 발행</text><text x="1146" y="174" font-size="19" font-weight="400" fill="#475569">배달 서비스가 배달을 만든 뒤</text><text x="1146" y="207" font-size="19" font-weight="400" fill="#475569">성공 여부를 <tspan font-weight="700">배달 생성</tspan></text><text x="1146" y="240" font-size="19" font-weight="400" fill="#475569"><tspan font-weight="700">이벤트</tspan>로 카프카에 발행합니다.</text><text x="1146" y="273" font-size="21" font-weight="700" fill="#0f172a">10. 오케스트레이터가 수신</text><text x="1146" y="315" font-size="19" font-weight="400" fill="#475569">오케스트레이터가 <tspan font-weight="700">배달 생성 이벤트</tspan></text><text x="1146" y="348" font-size="19" font-weight="400" fill="#475569">토픽을 구독하고 있다가 메시지를</text><text x="1146" y="381" font-size="19" font-weight="400" fill="#475569">받아 성공을 확인합니다.</text>
 </svg>
</div>

*그림 4-11. 5단계 — 배달 생성 이벤트 발행(배달) → 오케스트레이터 수신*

<div class="svg-figure svg-figure--wide">
<svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg">
  <defs>
   <marker id="mk" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
   <marker id="mk2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  </defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">6단계 — 주문 완료 명령 발행 → 주문 수신</text>
  <rect x="345" y="64" width="170" height="70" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
 <text x="430" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">Order</text>
 <text x="430" y="116" text-anchor="middle" font-size="14" fill="#3730a3">:8081 주문</text><rect x="575" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="660" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Product</text>
 <text x="660" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">:8082 상품</text><rect x="805" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="890" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Delivery</text>
 <text x="890" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">:8084 배달</text><rect x="280" y="250" width="780" height="120" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
 <rect x="280" y="250" width="780" height="22" fill="#ff7849"/>
 <text x="670" y="265" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">Kafka — 토픽별로 메시지를 보관·전달</text><rect x="300" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M300 290 L355 311 L410 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="355" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">주문 생성 이벤트</text><rect x="425" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M425 290 L480 311 L535 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="480" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">재고 차감 명령</text><rect x="550" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M550 290 L605 311 L660 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="605" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">재고 차감 이벤트</text><rect x="675" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M675 290 L730 311 L785 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="730" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">배달 생성 명령</text><rect x="800" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M800 290 L855 311 L910 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="855" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">배달 생성 이벤트</text><rect x="925" y="290" width="110" height="42" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.8"/>
   <path d="M925 290 L980 311 L1035 290" fill="none" stroke="#ff7849" stroke-width="1.4"/>
   <text x="980" y="350" text-anchor="middle" font-size="13" font-weight="700" fill="#9a3412">주문 완료 명령</text><circle cx="1017" cy="298" r="10" fill="#ff7849"/><text x="1017" y="302" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text><rect x="300" y="480" width="760" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
 <text x="680" y="514" text-anchor="middle" font-size="20" font-weight="700" fill="#312e81">Orchestrator</text>
 <text x="680" y="538" text-anchor="middle" font-size="14" fill="#312e81">흐름을 결정하는 지휘자 — event를 받아 다음 command를 발행</text><line x1="980" y1="478" x2="980" y2="372" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#mk)"/><text x="1002" y="429" text-anchor="start" font-size="15" font-weight="700" fill="#4f46e5">11. 주문 완료 명령 발행</text><line x1="980" y1="248" x2="430" y2="136" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#mk2)"/><text x="727" y="192" text-anchor="start" font-size="15" font-weight="700" fill="#3730a3">12. 주문 서비스가 수신</text><rect x="1090" y="40" width="460" height="510" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="550" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">6단계</text><text x="1146" y="132" font-size="21" font-weight="700" fill="#0f172a">11. 주문 완료 명령 발행</text><text x="1146" y="174" font-size="19" font-weight="400" fill="#475569">오케스트레이터가 <tspan font-weight="700">주문 완료</tspan></text><text x="1146" y="207" font-size="19" font-weight="400" fill="#475569"><tspan font-weight="700">명령</tspan>을 카프카에 발행합니다.</text><text x="1146" y="240" font-size="21" font-weight="700" fill="#0f172a">12. 주문 서비스가 수신</text><text x="1146" y="282" font-size="19" font-weight="400" fill="#475569">주문 서비스가 <tspan font-weight="700">주문 완료 명령</tspan></text><text x="1146" y="315" font-size="19" font-weight="400" fill="#475569">토픽을 구독하고 있다가 메시지를</text><text x="1146" y="348" font-size="19" font-weight="400" fill="#475569">받아 주문을 COMPLETED로</text><text x="1146" y="381" font-size="19" font-weight="400" fill="#475569">바꿉니다.</text>
 </svg>
</div>

*그림 4-12. 6단계 — 주문 완료 명령 발행 → 주문 수신*

### 4.3.3 주문 요청 실패 흐름 (보상 트랜잭션)

만약 상품 서비스가 재고 차감에 실패하면 재고 차감 실패 이벤트를 발행합니다. orchestrator는 **이미 처리된 단계만** 역순으로 되돌립니다.

<div class="svg-figure svg-figure--wide">
<svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="보상 실패 알림: 상품이 재고 차감 실패 결과를 이벤트로 알리고 오케스트레이터가 받는다. Kafka 띠에는 지나온 편지가 비활성으로 남고 재고 차감 이벤트만 활성이다.">
  <defs><marker id="rb1a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  <marker id="rb1f" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#dc2626"/></marker></defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">보상 · 실패 알림 — 상품이 재고 차감 실패를 오케스트레이터에 알린다</text>
  <rect x="345" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <text x="430" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Order</text>
  <text x="430" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">:8081 주문</text>
  <rect x="575" y="64" width="170" height="70" rx="8" fill="#fef2f2" stroke="#dc2626" stroke-width="1.8"/>
  <text x="660" y="92" text-anchor="middle" font-size="16" font-weight="700" fill="#b91c1c">Product</text>
  <text x="660" y="114" text-anchor="middle" font-size="13" fill="#b91c1c">재고 차감 실패 (품절)</text>
  <rect x="805" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4" stroke-dasharray="4,3"/>
  <text x="890" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#cbd5e1">Delivery</text>
  <text x="890" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">관여 안 함</text>
  <rect x="280" y="250" width="780" height="120" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <rect x="280" y="250" width="780" height="22" fill="#ff7849"/>
  <text x="670" y="265" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">Kafka — 토픽을 거쳐 결과가 오간다</text>
  <rect x="300" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M300 290 L355 311 L410 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
  <text x="355" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">주문 생성 이벤트</text>
  <rect x="425" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M425 290 L480 311 L535 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
  <text x="480" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">재고 차감 명령</text>
  <rect x="550" y="290" width="110" height="42" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="1.8"/>
  <path d="M550 290 L605 311 L660 290" fill="none" stroke="#dc2626" stroke-width="1.4"/>
  <text x="605" y="350" text-anchor="middle" font-size="13" font-weight="700" fill="#b91c1c">재고 차감 이벤트 (실패)</text>
  <circle cx="642" cy="298" r="10" fill="#dc2626"/><text x="642" y="302" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
  <rect x="300" y="480" width="760" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
  <text x="680" y="514" text-anchor="middle" font-size="20" font-weight="700" fill="#312e81">Orchestrator</text>
  <text x="680" y="538" text-anchor="middle" font-size="14" fill="#312e81">재고 차감 실패 결과를 받는다</text>
  <line x1="660" y1="134" x2="605" y2="248" stroke="#dc2626" stroke-width="2.6" marker-end="url(#rb1f)"/>
  <text x="652" y="196" text-anchor="start" font-size="15" font-weight="700" fill="#b91c1c">1. 상품이 재고 차감 실패를 알림</text>
  <line x1="605" y1="370" x2="605" y2="478" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#rb1a)"/>
  <text x="627" y="429" text-anchor="start" font-size="15" font-weight="700" fill="#3730a3">2. 오케스트레이터가 수신</text>
  <rect x="1090" y="40" width="460" height="430" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="470" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">보상 · 실패 알림</text>
  <text x="1146" y="128" font-size="21" font-weight="700" fill="#b91c1c">1. 상품이 재고 차감 실패를 알림</text>
  <text x="1146" y="158" font-size="19" font-weight="400" fill="#475569">재고 차감에 실패한 상품 서비스가</text>
  <text x="1146" y="181" font-size="19" font-weight="400" fill="#475569"><tspan font-weight="700">재고 차감 이벤트</tspan>를 발행합니다.</text>
  <text x="1146" y="225" font-size="21" font-weight="700" fill="#0f172a">2. 오케스트레이터가 수신</text>
  <text x="1146" y="255" font-size="19" font-weight="400" fill="#475569">실패 결과를 받고 보상을</text>
  <text x="1146" y="278" font-size="19" font-weight="400" fill="#475569">시작합니다.</text>
</svg>
</div>

*그림 4-13. 보상 · 실패 알림 — 상품이 실패를 알림*

<div class="svg-figure svg-figure--wide">
<svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="보상 주문 취소: 오케스트레이터가 주문 취소 명령을 발행하고 주문 서비스가 CANCELLED 처리. 앞 편지들은 비활성으로 남고 주문 취소 명령만 활성이다.">
  <defs><marker id="rb2a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  <marker id="rb2b" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker></defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">보상 · 주문 취소 — 주문 취소 명령을 발행</text>
  <rect x="345" y="64" width="170" height="70" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="430" y="92" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">Order</text>
  <text x="430" y="114" text-anchor="middle" font-size="13" fill="#3730a3">주문 CANCELLED</text>
  <rect x="575" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <text x="660" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Product</text>
  <text x="660" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">:8082 상품</text>
  <rect x="805" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <text x="890" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Delivery</text>
  <text x="890" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">:8084 배달</text>
  <rect x="280" y="250" width="780" height="120" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <rect x="280" y="250" width="780" height="22" fill="#ff7849"/>
  <text x="670" y="265" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">Kafka — 주문 취소 명령이 발행된다</text>
  <rect x="300" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M300 290 L355 311 L410 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
  <text x="355" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">주문 생성 이벤트</text>
  <rect x="425" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M425 290 L480 311 L535 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
  <text x="480" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">재고 차감 명령</text>
  <rect x="550" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M550 290 L605 311 L660 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
  <text x="605" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">재고 차감 이벤트 (실패)</text>
  <rect x="675" y="290" width="110" height="42" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.8"/>
  <path d="M675 290 L730 311 L785 290" fill="none" stroke="#ff7849" stroke-width="1.4"/>
  <text x="730" y="350" text-anchor="middle" font-size="13" font-weight="700" fill="#9a3412">주문 취소 명령</text>
  <circle cx="767" cy="298" r="10" fill="#ff7849"/><text x="767" y="302" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
  <rect x="300" y="480" width="760" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
  <text x="680" y="514" text-anchor="middle" font-size="20" font-weight="700" fill="#312e81">Orchestrator</text>
  <text x="680" y="538" text-anchor="middle" font-size="14" fill="#312e81">재고 복구 없이 곧장 주문 취소 명령 발행</text>
  <line x1="730" y1="478" x2="730" y2="372" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#rb2a)"/>
  <text x="752" y="429" text-anchor="start" font-size="15" font-weight="700" fill="#4f46e5">3. 주문 취소 명령 발행</text>
  <line x1="730" y1="248" x2="430" y2="136" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#rb2b)"/>
  <text x="605" y="196" text-anchor="start" font-size="15" font-weight="700" fill="#3730a3">4. 주문 서비스가 수신해 CANCELLED 처리</text>
  <rect x="1090" y="40" width="460" height="510" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="550" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">보상 · 주문 취소</text>
  <text x="1146" y="124" font-size="21" font-weight="700" fill="#0f172a">3. 주문 취소 명령 발행</text>
  <text x="1146" y="158" font-size="19" font-weight="400" fill="#475569">오케스트레이터가 <tspan font-weight="700">주문 취소</tspan></text>
  <text x="1146" y="185" font-size="19" font-weight="400" fill="#475569"><tspan font-weight="700">명령</tspan>을 카프카에 발행합니다.</text>
  <text x="1146" y="252" font-size="21" font-weight="700" fill="#0f172a">4. 주문 서비스가 CANCELLED</text>
  <text x="1146" y="286" font-size="19" font-weight="400" fill="#475569">주문 서비스가 메시지를 받아</text>
  <text x="1146" y="313" font-size="19" font-weight="400" fill="#475569">주문 상태를 CANCELLED로 바꿉니다.</text>
</svg>
</div>

*그림 4-14. 보상 · 주문 취소 — 주문 취소 명령 발행*

## 4.4 Kafka로 주고받기 - 발행과 구독

### 4.4.1 발행 - 토픽에 메시지를 넣는다

프로듀서가 메시지를 발행할 때는 Spring이 제공하는 **`KafkaTemplate`** 을 사용합니다. **주문 생성 이벤트**를 발행하는 코드는 다음과 같습니다.

`adapter/producer/OrderEventProducer.java`를 열고 아래 메서드를 작성합니다.

**[실습 1] adapter/producer/OrderEventProducer.java. 주문 생성 이벤트 발행**
```java
@Component
@RequiredArgsConstructor
public class OrderEventProducer {
    private final KafkaTemplate<String, Object> kafkaTemplate;

    public void publishOrderCreated(OrderCreatedEvent event) {
        // "order-created" 토픽에 이벤트를 넣는다
        kafkaTemplate.send("order-created", event);
    }
}
```

`kafkaTemplate.send`에 `order-created` 같은 토픽 이름과 보낼 이벤트를 넘기면 해당 토픽으로 메시지가 들어갑니다.

주문 서비스는 주문을 **PENDING** 상태로 저장하고, **주문 생성 이벤트 프로듀서**를 호출합니다.

`usecase/OrderService.java`를 열고 `createOrder` 메서드를 작성합니다.

**[실습 2] usecase/OrderService.java. 주문 저장 후 주문 생성 이벤트 발행**
```java
@Override
@Transactional
public OrderResponse createOrder(int userId, int productId,
        int quantity, Long price, String address) {
    // 1. 주문 생성
    Order createdOrder = orderRepository.save(Order.create(userId, productId, quantity, price));
    createdOrder.validateMinAmount();

    // 2. Kafka로 주문 생성 이벤트 발행
    orderEventProducer.publishOrderCreated(
            new OrderCreatedEvent(
                    createdOrder.getId(), userId, productId, quantity, price, address)
    );

    return OrderResponse.from(createdOrder);
}
```

### 4.4.2 orchestrator - 흐름을 조율하는 코드

이벤트를 받아 **다음 명령을 정하는 일**은 orchestrator가 수행합니다. **주문 생성 이벤트**를 받아 **재고 차감 명령**을 발행하는 코드는 다음과 같습니다.

`handler/OrderOrchestrator.java`를 열고 아래 메서드를 작성합니다.

**[실습 3] handler/OrderOrchestrator.java. 주문 생성 이벤트를 받아 재고 차감 명령 발행**
```java
@KafkaListener(topics = "order-created", groupId = "orchestrator")
public void orderCreated(OrderCreatedEvent event) {
    // 1. 주문 진행 상태를 메모리에 기록
    states.put(event.orderId(), new WorkflowState(
            event.orderId(), event.address(),
            event.productId(), event.quantity(), event.price()));

    // 2. 다음 단계: 재고 차감 명령 발행
    kafkaTemplate.send("decrease-product-command",
            new DecreaseProductCommand(event.orderId(),
                    event.productId(), event.quantity(), event.price()));
}
```

`@KafkaListener`의 `topics`는 구독할 토픽 이름, `groupId`는 컨슈머 그룹 이름입니다. 그리고 `WorkflowState`는 **주문의 진행 정보를 메모리에 들고 있는 객체**로, 결과 이벤트가 돌아오면 orchestrator는 이 기록을 보고 다음 명령을 정합니다.

### 4.4.3 구독 - 토픽의 메시지를 받는다

앞에서 orchestrator가 발행한 **재고 차감 명령**을 이번에는 상품 서비스가 받습니다. 받은 명령으로 재고를 줄이고, 그 결과를 **재고 차감 이벤트**로 발행합니다.

`adapter/consumer/ProductCommandConsumer.java`를 열고 아래 메서드를 작성합니다.

**[실습 4] adapter/consumer/ProductCommandConsumer.java. 재고 차감 명령 구독**
```java
@KafkaListener(topics = "decrease-product-command", groupId = "product-service")
public void decreaseProductCommand(DecreaseProductCommand command) {
    boolean isSuccess = false;
    // 1. 재고 차감 (성공하면 isSuccess = true)
    try {
        productService.decreaseQuantity(command.productId(), command.quantity(), command.price());
        isSuccess = true;
    } catch (Exception e) {
        // 재고 부족 등 실패는 isSuccess = false로 그대로 보고
    }

    // 2. 처리 결과를 '재고 차감 이벤트'로 발행
    productEventProducer.publishProductDecreased(
            new ProductDecreasedEvent(
                    command.orderId(), command.productId(), command.quantity(), isSuccess));
}
```

상품 서비스는 명령을 받아 재고를 줄인 뒤, 성공이든 실패든 그 결과를 이벤트에 담아 돌려줍니다.

각 서비스 코드는 모두 같은 발행·구독 패턴이고, 토픽 이름만 다릅니다. 그래서 코드를 일일이 보지 않아도, 각 서비스가 무슨 토픽을 구독해 어떻게 처리하고 무엇을 발행하는지만 알면 전체 흐름이 보입니다.

각 서비스의 전체 코드는 GitHub에서 확인하세요.

이제 Kubernetes에 Kafka와 orchestrator를 추가하고 전체 시스템을 배포합니다.

## 4.5 Kubernetes - Kafka와 orchestrator 배포

Kafka를 도입하면서 추가되는 건 **Kafka 서버**와 **orchestrator 서버**입니다.

<table>
<colgroup><col style="width:34%"><col style="width:66%"></colgroup>
<thead><tr><th>Kubernetes 리소스</th><th>역할</th></tr></thead>
<tbody>
<tr><td style="white-space:nowrap"><code>kafka-deploy.yml</code></td><td>Kafka를 실행하는 Pod를 정의하고 원하는 상태로 유지합니다.</td></tr>
<tr><td style="white-space:nowrap"><code>kafka-service.yml</code></td><td>Kafka Pod에 고정 주소 <code>kafka-service:9092</code>를 부여해, 주문·상품 등 각 서비스가 이 주소로 Kafka에 연결합니다.</td></tr>
<tr><td style="white-space:nowrap"><code>orchestrator-deploy.yml</code></td><td>orchestrator를 실행하는 Pod를 정의합니다.</td></tr>
<tr><td style="white-space:nowrap"><code>orchestrator-configmap.yml</code></td><td>orchestrator에 Kafka 주소 같은 설정값을 환경변수로 주입합니다.</td></tr>
</tbody>
</table>

모든 서비스는 Kafka 서버의 주소 `kafka-service:9092`로 접근합니다. 각 서비스는 이 주소를 ConfigMap에 넣어 둡니다.

<div class="svg-figure">
<svg viewBox="0 0 1000 460" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="KAFKA_ADVERTISED_LISTENERS: 4개의 클라이언트 서비스가 kafka-service:9092 주소로 Kafka 서버에 접근">
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
  <text x="500" y="195" text-anchor="middle" font-size="11" font-weight="600" fill="#4f46e5" font-family="JetBrains Mono, monospace">SPRING_KAFKA_BOOTSTRAP_SERVERS</text>
  <rect x="220" y="240" width="560" height="150" rx="14" fill="#eef2ff" stroke="#4f46e5" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="500" y="270" text-anchor="middle" font-size="12" font-weight="700" fill="#3730a3" font-family="JetBrains Mono, monospace">KAFKA_ADVERTISED_LISTENERS</text>
  <rect x="340" y="290" width="320" height="80" rx="10" fill="#fff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="500" y="318" text-anchor="middle" font-size="11" font-weight="700" fill="#3730a3">BROKER</text>
  <text x="500" y="345" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a" font-family="JetBrains Mono, monospace">kafka-service:9092</text>
  <text x="500" y="425" text-anchor="middle" font-size="12" fill="#475569">클라이언트의 SPRING_KAFKA_BOOTSTRAP_SERVERS 값은 Kafka 서버의 ADVERTISED_LISTENERS 값과 일치해야 합니다.</text>
</svg>
</div>

*그림 4-15. 클라이언트가 kafka-service:9092로 접근*

`kafka-deploy.yml`의 전체 환경변수는 GitHub에서 확인하세요. 각 변수의 역할은 주석으로 달려 있습니다.

:::tip
**KRaft 모드 알아두기**

Kafka 서버는 크게 두 가지 역할을 합니다. **메시지를 받아 전달하는 브로커**, 그리고 **클러스터와 토픽 설정을 관리하는 컨트롤러**입니다.

과거에는 이 컨트롤러 역할을 **ZooKeeper**라는 외부 서비스에 따로 맡겨야 했습니다. 하지만 **KRaft(Kafka Raft)** 모드에서는 Kafka가 관리 역할까지 직접 도맡습니다. 덕분에 복잡한 ZooKeeper 연동 없이 Kafka 컨테이너 하나만으로 두 가지 역할을 모두 처리합니다.

실제 운영 환경에서는 데이터 유실을 막기 위해 여러 대의 브로커 노드를 구성해 안정성을 높입니다. 다만 이 책에서는 실습의 편의를 위해 하나의 컨테이너에 브로커와 컨트롤러를 함께 구성해 진행합니다.
:::

## 4.6 실행 및 결과 확인

### 4.6.1 이미지 빌드

Minikube 내부에 이미지를 빌드합니다. 챕터 3 대비 orchestrator 서비스가 새로 추가됩니다.

**[터미널] 이미지 빌드**
```bash
minikube image build -t metacoding/db:2 ./db
minikube image build -t metacoding/gateway:2 ./gateway
minikube image build -t metacoding/order:2 ./order
minikube image build -t metacoding/product:2 ./product
minikube image build -t metacoding/user:2 ./user
minikube image build -t metacoding/delivery:2 ./delivery
minikube image build -t metacoding/orchestrator:2 ./orchestrator
```

### 4.6.2 배포 순서

Kafka가 준비되기 전에 서비스가 시작되면 연결 오류가 발생합니다. Kafka를 먼저 배포하고 준비된 것을 확인한 다음 나머지를 배포합니다.

**[터미널] 배포 순서 (Kafka 우선)**
```bash
# 1. 네임스페이스 생성
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
    <div class="tl-divider"><span class="tl-val">8개 Deployment + 7개 Service 배포 완료</span><span class="tl-cursor"></span></div>
  </div>
</div>

*그림 4-16. Kafka 및 서비스 배포 실행*

모든 Pod가 Running 상태인지 확인합니다.

**[터미널] Pod 상태 확인**
```bash
kubectl get pods -n metacoding
```

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">kubectl get pods -n metacoding</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div class="tl-kv-row"><span class="tl-label">NAME</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-label">READY</span>&nbsp;&nbsp;<span class="tl-label">STATUS</span>&nbsp;&nbsp;&nbsp;<span class="tl-label">AGE</span></div>
    <div class="tl-kv-row">kafka-deploy-7d4c8b9f5-2xk9p&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">2m</span></div>
    <div class="tl-kv-row">db-deploy-6f9b7c4d8-m4t2q&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">90s</span></div>
    <div class="tl-kv-row">gateway-deploy-5c8d6f7b9-h7w3r&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">88s</span></div>
    <div class="tl-kv-row">order-deploy-8b7f6c9d4-q2k8m&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">85s</span></div>
    <div class="tl-kv-row">product-deploy-7c9d8b6f5-x4r2t&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">83s</span></div>
    <div class="tl-kv-row">user-deploy-6d8c7b9f4-p3m9k&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">80s</span></div>
    <div class="tl-kv-row">delivery-deploy-9f7c8b6d5-t6w2x&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">78s</span></div>
    <div class="tl-kv-row">orchestrator-deploy-8c6f9b7d4-k9m4q&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">75s</span></div>
    <div class="tl-divider"><span class="tl-val">8개 Pod Running (Kafka + orchestrator 추가)</span><span class="tl-cursor"></span></div>
  </div>
</div>

*그림 4-17. Pod 상태 확인 (kubectl get pods)*

### 4.6.3 서비스 접근

Ingress를 통해 외부에서 접속하기 위해 `minikube tunnel`을 실행합니다.

**[터미널] 외부 접근 터널**
```bash
minikube tunnel
```

터널이 실행되면 `http://127.0.0.1:80`로 gateway-service에 접속할 수 있습니다.

### 4.6.4 비동기 흐름 테스트

이제 AirPods (productId=3) 2개를 주문하는 API 요청을 보내 보겠습니다.

**[Hoppscotch] 주문 생성**
```json
POST http://127.0.0.1:80/api/orders

{
  "productId": 3,
  "quantity": 2,
  "price": 300000,
  "address": "Addr 4"
}
```

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH04/terminal/14_order-pending.png)
*그림 4-18. 주문 생성 응답 (PENDING 상태)*

챕터 3과 다르게 즉시 `PENDING` 상태로 반환됩니다. 잠시 후 주문 상태를 다시 조회하면, Kafka 이벤트가 처리되어 상태가 `COMPLETED`로 바뀐 것을 확인할 수 있습니다.

**[Hoppscotch] 주문 조회**
```json
GET http://127.0.0.1:80/api/orders/4
```

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH04/terminal/15_order-completed.png)
*그림 4-19. 주문 완료 확인 (COMPLETED 상태)*

### 4.6.5 보상 트랜잭션 확인 - 품절 상품 주문

동기 방식에서는 주문 서비스가 트랜잭션을 관리했기 때문에 주문이 실패하면 주문 데이터가 **자동 롤백**되었습니다. 반면 비동기 방식에서는 주문이 **PENDING으로 먼저 저장**됩니다. 그래서 재고 감소가 실패하면 **보상 트랜잭션**에 의해 주문 상태가 `CANCELLED`로 변경됩니다.

iPhone 15(productId=2, 재고 0)로 확인해 보겠습니다.

**[Hoppscotch] 주문 생성 (품절 상품)**
```json
POST http://127.0.0.1:80/api/orders

{
  "productId": 2,
  "quantity": 1,
  "price": 1300000,
  "address": "Addr 5"
}
```

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH04/terminal/16_stockout-order.png)
*그림 4-20. 품절 상품 주문 요청*

잠시 후 상태를 확인하면 `CANCELLED`가 됩니다.

**[Hoppscotch] 주문 조회**
```JSON
GET http://127.0.0.1:80/api/orders/5
```

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH04/terminal/17_order-cancelled.png)
*그림 4-21. 주문 취소 확인 (CANCELLED 상태)*

테스트가 끝났으면 이번 챕터에서 실행한 리소스를 정리합니다.

**[터미널] 리소스 정리**
```bash
kubectl delete namespace metacoding
```

**오픈이**: "이제 직접 호출하지 않고 메시지로 주고받으니까, 다른 서비스가 일시적으로 멈춰도 주문은 계속 받을 수 있겠네요."

**선배**: "맞아요. 서비스 간의 결합이 느슨해진 덕분이죠. 게다가 주문이 한꺼번에 몰려도 Kafka가 중간에서 메시지를 받아 두니, 받는 쪽은 감당할 수 있는 속도로 처리하면 돼요. 한 서비스에 장애가 나거나 부하가 걸려도 시스템 전체가 무너지지 않습니다."

다만 현재 구조에서는 클라이언트가 처음에 **주문 대기** 상태만 응답받을 뿐, 이후 실제 처리가 완료되어도 그 결과를 따로 알 수 없습니다. 다음 챕터에서는 **웹소켓(WebSocket)** 을 도입해 이 문제를 해결하고, 주문 처리가 끝나는 즉시 클라이언트에게 실시간 알림을 보내는 방법을 알아보겠습니다.

:::remember
**이것만은 기억하자**

- 서비스끼리 REST로 직접 호출하는 대신 **Kafka**로 메시지를 주고받습니다. 이 **비동기 방식**으로 서비스 간 결합이 느슨해집니다.
- **orchestrator**가 **명령**으로 각 서비스를 조율하고, 각 서비스는 **이벤트**로 결과를 알립니다.
- **Saga 패턴**으로 분산 트랜잭션을 단계별로 처리하고, 실패한 단계는 **보상 트랜잭션**으로 역순으로 되돌립니다.
:::



---


# 챕터 5. 실시간 알림 - 주문 완료를 즉시 전달하다

며칠 뒤, 베타 테스터로 새 시스템을 써 본 동료가 떨떠름한 표정으로 오픈이를 찾아왔습니다.

**동료**: "어제 물건을 주문했는데, 화면이 계속 **처리 중**이더라고요. 끝났는지 알 수가 없어서 한참 뒤에 주문 내역을 다시 열어 보고서야 **주문 완료**된 걸 알았어요."

오픈이는 코드 흐름을 따라가 봤습니다. 주문이 생성되면 그대로 **PENDING** 상태로 응답 후, 사용자에게 **COMPLETED** 응답은 하지 않았습니다. 게다가 주문 완료는 실제 배달이 끝났는지와 무관하게, 배달이 생성되는 순간 곧바로 처리되었습니다.

이 문제를 들고 선배에게 갔습니다.

**오픈이**: "서버에서 주문이 완료되었는데, 사용자는 처음 **PENDING** 상태만 응답을 받아서 주문이 완료된 사실을 알 수가 없어요. 이거는 어떻게 해결해야 하죠?"

**선배**: "처리가 끝난 순간 사용자에게 알림을 줘야 해요. 서버에서 **주문 처리가 완료된 시점**을 감지해서 사용자에게 실시간으로 알려줄 방법이 필요하겠죠."

<div class="svg-figure">
<svg viewBox="0 0 1200 880" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="챕터 5 한눈에 보기: 챕터 4와 동일하게 1단계 로그인, 2단계 주문은 Client가 Ingress·Gateway를 거쳐 Order에 주문하고 즉시 PENDING을 응답받는다. Order·Product·Delivery는 가운데 Orchestrator와 event·command를 주고받고 Orchestrator가 Kafka 토픽으로 비동기 전달한다. 챕터 4와의 차이는, 비동기 처리가 끝나 주문이 완료되면 Order가 WebSocket으로 Client에게 완료를 즉시 Push(13)한다는 점이다.">
  <defs>
    <marker id="c5f0-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="c5f0-r" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#0d9488"/></marker>
  </defs>
  <text x="600" y="26" text-anchor="middle" font-size="20" font-weight="700" fill="#0f172a">챕터 5 한눈에 보기 — 주문 완료를 WebSocket으로 즉시 알린다</text>
  <rect x="200" y="58" width="980" height="760" rx="14" fill="none" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="6,4"/>
  <text x="220" y="78" font-size="13" font-weight="700" fill="#3730a3">Kubernetes 클러스터 · metacoding</text>
  <text x="36" y="98" font-size="15" font-weight="700" fill="#475569">1단계 — 로그인</text>
  <rect x="20" y="108" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="90" y="141" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">Client</text>
  <text x="90" y="164" text-anchor="middle" font-size="13" fill="#6b7280">사용자</text>
  <rect x="290" y="108" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="360" y="141" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">Ingress</text>
  <text x="360" y="164" text-anchor="middle" font-size="13" fill="#6b7280">외부 진입점</text>
  <rect x="510" y="108" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="580" y="141" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">Gateway</text>
  <text x="580" y="164" text-anchor="middle" font-size="13" fill="#6b7280">Nginx 라우팅</text>
  <rect x="720" y="108" width="170" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="805" y="141" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">User</text>
  <text x="805" y="164" text-anchor="middle" font-size="13" fill="#6b7280">:8083 회원</text>
  <line x1="160" y1="140" x2="288" y2="140" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c5f0-a)"/>
  <text x="225" y="132" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">1. 요청</text>
  <line x1="430" y1="140" x2="508" y2="140" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c5f0-a)"/>
  <text x="470" y="132" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">2. 라우팅</text>
  <line x1="650" y1="140" x2="718" y2="140" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c5f0-a)"/>
  <text x="685" y="132" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">3. 로그인</text>
  <line x1="718" y1="168" x2="652" y2="168" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c5f0-a)"/>
  <text x="685" y="181" text-anchor="middle" font-size="15" font-weight="600" fill="#3730a3">4. 응답</text>
  <line x1="508" y1="168" x2="432" y2="168" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c5f0-a)"/>
  <text x="470" y="181" text-anchor="middle" font-size="15" font-weight="600" fill="#3730a3">5. 응답</text>
  <line x1="288" y1="168" x2="162" y2="168" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c5f0-a)"/>
  <text x="225" y="181" text-anchor="middle" font-size="15" font-weight="600" fill="#3730a3">6. JWT 응답</text>
  <text x="36" y="258" font-size="15" font-weight="700" fill="#475569">2단계 — 주문 생성</text>
  <rect x="20" y="268" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="90" y="301" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">Client</text>
  <text x="90" y="324" text-anchor="middle" font-size="13" fill="#6b7280">사용자</text>
  <rect x="290" y="268" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="360" y="301" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">Ingress</text>
  <text x="360" y="324" text-anchor="middle" font-size="13" fill="#6b7280">외부 진입점</text>
  <rect x="510" y="268" width="140" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="580" y="301" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">Gateway</text>
  <text x="580" y="324" text-anchor="middle" font-size="13" fill="#6b7280">Nginx 라우팅</text>
  <line x1="160" y1="300" x2="288" y2="300" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c5f0-a)"/>
  <text x="225" y="292" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">7. 요청</text>
  <line x1="430" y1="300" x2="508" y2="300" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c5f0-a)"/>
  <text x="470" y="292" text-anchor="middle" font-size="15" font-weight="600" fill="#4f46e5">8. 라우팅</text>
  <line x1="560" y1="348" x2="390" y2="430" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c5f0-a)"/>
  <text x="450" y="392" text-anchor="end" font-size="15" font-weight="600" fill="#4f46e5">9. 주문 생성</text>
  <line x1="430" y1="430" x2="600" y2="348" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c5f0-a)"/>
  <text x="536" y="392" text-anchor="start" font-size="15" font-weight="600" fill="#3730a3">10. 응답</text>
  <line x1="508" y1="326" x2="432" y2="326" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c5f0-a)"/>
  <text x="470" y="342" text-anchor="middle" font-size="15" font-weight="600" fill="#3730a3">11. 응답</text>
  <line x1="288" y1="326" x2="162" y2="326" stroke="#3730a3" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c5f0-a)"/>
  <text x="225" y="342" text-anchor="middle" font-size="13" font-weight="600" fill="#3730a3">12. PENDING 응답</text>
  <path d="M300 462 Q 90 462 90 352" fill="none" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="5,4" marker-end="url(#c5f0-a)"/>
  <text x="132" y="420" text-anchor="start" font-size="13" font-weight="600" fill="#4f46e5">13. WebSocket 완료 알림</text>
  <rect x="300" y="430" width="170" height="80" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="385" y="463" text-anchor="middle" font-size="19" font-weight="700" fill="#3730a3">Order</text>
  <text x="385" y="486" text-anchor="middle" font-size="13" fill="#3730a3">:8081 주문</text>
  <rect x="560" y="430" width="170" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="645" y="463" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">Product</text>
  <text x="645" y="486" text-anchor="middle" font-size="13" fill="#6b7280">:8082 상품</text>
  <rect x="820" y="430" width="170" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="905" y="463" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">Delivery</text>
  <text x="905" y="486" text-anchor="middle" font-size="13" fill="#6b7280">:8084 배달</text>
  <rect x="1005" y="430" width="160" height="80" rx="8" fill="#f0fdfa" stroke="#0d9488" stroke-width="1.8"/>
  <text x="1085" y="463" text-anchor="middle" font-size="18" font-weight="700" fill="#0f766e">배달 기사</text>
  <text x="1085" y="486" text-anchor="middle" font-size="13" fill="#0d9488">외부 호출자</text>
  <text x="1085" y="420" text-anchor="middle" font-size="13" font-weight="700" fill="#0f766e">PUT /complete</text>
  <line x1="1003" y1="470" x2="992" y2="470" stroke="#0d9488" stroke-width="2.4" marker-end="url(#c5f0-r)"/>
  <rect x="360" y="588" width="580" height="68" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <rect x="360" y="588" width="580" height="20" fill="#ff7849"/>
  <text x="650" y="603" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">Kafka — 모든 메시지가 토픽을 거쳐 비동기로 전달</text>
  <rect x="410" y="618" width="76" height="28" rx="2" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M410 618 L448 631 L486 618" fill="none" stroke="#ff7849" stroke-width="1"/>
  <rect x="530" y="618" width="76" height="28" rx="2" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M530 618 L568 631 L606 618" fill="none" stroke="#ff7849" stroke-width="1"/>
  <rect x="650" y="618" width="76" height="28" rx="2" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M650 618 L688 631 L726 618" fill="none" stroke="#ff7849" stroke-width="1"/>
  <rect x="770" y="618" width="76" height="28" rx="2" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M770 618 L808 631 L846 618" fill="none" stroke="#ff7849" stroke-width="1"/>
  <rect x="320" y="716" width="620" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
  <text x="630" y="750" text-anchor="middle" font-size="24" font-weight="700" fill="#312e81">Orchestrator</text>
  <text x="630" y="774" text-anchor="middle" font-size="13" font-weight="600" fill="#312e81">흐름을 결정하는 지휘자</text>
  <line x1="370" y1="512" x2="370" y2="586" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c5f0-a)"/>
  <text x="356" y="552" text-anchor="end" font-size="13" font-weight="600" fill="#3730a3"><tspan font-size="20" font-weight="700">❶</tspan> 주문 생성 발행</text>
  <line x1="400" y1="586" x2="400" y2="512" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c5f0-a)"/>
  <text x="414" y="552" text-anchor="start" font-size="13" font-weight="600" fill="#4f46e5"><tspan font-size="20" font-weight="700">❻</tspan> 주문 완료 명령</text>
  <line x1="630" y1="512" x2="630" y2="586" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c5f0-a)"/>
  <text x="616" y="552" text-anchor="end" font-size="13" font-weight="600" fill="#3730a3"><tspan font-size="20" font-weight="700">❸</tspan> 재고 차감 결과</text>
  <line x1="660" y1="586" x2="660" y2="512" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c5f0-a)"/>
  <text x="674" y="552" text-anchor="start" font-size="13" font-weight="600" fill="#4f46e5"><tspan font-size="20" font-weight="700">❷</tspan> 재고 차감 명령</text>
  <line x1="890" y1="512" x2="890" y2="586" stroke="#4f46e5" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#c5f0-a)"/>
  <text x="876" y="552" text-anchor="end" font-size="13" font-weight="600" fill="#3730a3"><tspan font-size="20" font-weight="700">❺</tspan> 배달 생성 결과</text>
  <line x1="920" y1="586" x2="920" y2="512" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c5f0-a)"/>
  <text x="934" y="552" text-anchor="start" font-size="13" font-weight="600" fill="#4f46e5"><tspan font-size="20" font-weight="700">❹</tspan> 배달 생성 명령</text>
  <line x1="615" y1="660" x2="615" y2="714" stroke="#4f46e5" stroke-width="2.4" marker-end="url(#c5f0-a)"/>
  <text x="603" y="690" text-anchor="end" font-size="13" font-weight="700" fill="#4f46e5">발행</text>
  <line x1="645" y1="714" x2="645" y2="662" stroke="#4f46e5" stroke-width="2.4" stroke-dasharray="4,3" marker-end="url(#c5f0-a)"/>
  <text x="657" y="690" text-anchor="start" font-size="13" font-weight="700" fill="#3730a3">구독</text>
  <text x="600" y="844" text-anchor="middle" font-size="21" fill="#6b7280" font-style="italic">주문이 완료되면 Order가 WebSocket으로 Client에게 즉시 알립니다.</text>
</svg>
</div>

*그림 5-1. 챕터 5 한눈에 보기 - 주문 완료를 웹소켓으로 즉시 알린다*

:::goal
**이번 챕터가 끝나면**

- 폴링과 푸시의 차이, 실시간 통신(**웹소켓**)이 필요한 이유를 이해할 수 있습니다.
- 비동기 완료 시점을 포착해 사용자에게 실시간으로 전달하는 흐름을 이해할 수 있습니다.
:::

::::prep
**준비하기**. 실습 시작 전 한 번만 설정

### 1. 소스 코드 클론

**[터미널] 레포 클론**
```bash
git clone https://github.com/metacoding-12-msa/ex04.git
cd ex04
```

### 2. 파일 구조

**ex04 디렉토리**
```text
ex04/
├── order/              # 포트 8081 (웹소켓 Push 추가)
├── product/            # 포트 8082
├── user/               # 포트 8083
├── delivery/           # 포트 8084 (배달 완료 API 추가)
├── orchestrator/       # Kafka 워크플로우 조율
├── frontend/           # Nginx + SockJS 클라이언트 (이번 챕터 신규)
├── gateway/            # Nginx API Gateway
├── db/                 # MySQL
└── k8s/                # Kubernetes YAML 파일 (kafka·frontend 포함)
```

서비스마다 패키지 구조가 조금씩 다르므로, 코드를 작성할 파일 경로는 각 실습 코드블록 바로 위에서 안내합니다.

### 3. 실습 순서

1. 배달 서비스에 배달 생성·완료 분리 + 배달 완료 API + `delivery-completed` 이벤트 추가
2. orchestrator에 `delivery-completed` 처리 + `delivery-created` 성공 시 대기로 변경
3. 주문 서비스에 STOMP 웹소켓 설정 + 주문 완료 시 Push
4. SockJS 기반 index.html 프론트엔드와 Nginx 프록시 구성
5. Kubernetes에 frontend 추가 배포 → 통합 시나리오 검증
::::

## 5.1 웹소켓 - 폴링의 한계를 넘다

### 5.1.1 폴링 vs 푸시

서버에 생긴 변화를 알아내는 방법은 크게 두 가지입니다.

택배가 왔는지 확인하려고 5분마다 현관문을 열어보는 방식이 있습니다. 도착 여부는 직접 문을 열어봐야만 알 수 있습니다. 이처럼 **클라이언트가 서버에 "처리가 완료되었나요?"라고 일정 간격으로 반복해서 묻는** 방식을 **폴링(Polling)** 이라고 합니다.

반면, 택배가 도착했을 때 초인종이 울리는 방식도 있습니다. 안에 있는 사람은 문을 계속 열어볼 필요 없이, 벨이 울리는 순간 도착 사실을 알게 됩니다. 이처럼 **클라이언트가 요청하지 않아도 서버에 변화가 생겼을 때 먼저 신호를 보내는** 방식을 **푸시(Push)** 라고 합니다.

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH05/gemini/01_polling-vs-websocket.png)
*그림 5-2. 폴링 vs 푸시*

폴링은 정해진 간격마다 서버에 요청을 보냅니다. 하지만 서버의 상태가 바뀌지 않았다면 의미 없는 요청과 응답을 반복하게 됩니다. 또한, 서버에 변화가 생기더라도 다음 요청 주기가 돌아올 때까지는 이를 감지할 수 없어, 설정한 간격만큼 데이터 전달이 지연되는 한계가 있습니다.

반면 푸시는 서버에 이벤트가 발생한 순간에만 신호를 보내기 때문에, 클라이언트는 지속적으로 상태를 확인하지 않고도 변경 사항을 즉시 수신할 수 있습니다.

### 5.1.2 웹소켓 - 실시간 양방향 통신

푸시를 구현하는 대표적인 기술이 바로 **웹소켓(WebSocket)** 입니다.

전통적인 HTTP 요청-응답 방식은 '편지'와 같습니다. 편지를 한 통 보내고 답장이 오면 한 번의 통신이 끝나며, 다음 상태가 궁금하면 다시 편지를 보내야 합니다. **클라이언트가 먼저 요청을 하지 않으면 서버는 아무것도 응답할 수 없는 구조**입니다.

반면 웹소켓은 '전화 통화'에 가깝습니다. 한 번 연결되면 끊지 않고 채널을 유지하므로, **상대가 묻지 않아도 어느 쪽이든 먼저 말을 할 수 있습니다**. 그래서 서버에 변화가 생기는 순간 알림을 클라이언트에게 보내는 것이 가능해집니다.

<div class="svg-figure">
<svg viewBox="0 0 900 250" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="편지와 전화 비유로 본 HTTP와 WebSocket. 양쪽 다 사용자와 서버 박스는 같다. 왼쪽은 편지를 한 번 주고받으면 연결이 끊겨 다시 보내야 한다. 오른쪽은 전화 연결이 유지되어 서버가 먼저 주문 완료를 알린다.">
  <defs>
    <marker id="s52-a" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="225" y="34" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">편지 — HTTP 요청·응답</text>
  <text x="675" y="34" text-anchor="middle" font-size="17" font-weight="700" fill="#3730a3">전화 — WebSocket</text>
  <line x1="450" y1="54" x2="450" y2="238" stroke="#e2e8f0" stroke-width="1.4"/>
  <rect x="70" y="120" width="110" height="56" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="125" y="153" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">사용자</text>
  <rect x="300" y="120" width="110" height="56" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="355" y="153" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">서버</text>
  <rect x="223" y="92" width="34" height="22" rx="2" fill="#fff" stroke="#4f46e5" stroke-width="1.4"/>
  <path d="M223 92 L240 106 L257 92" fill="none" stroke="#4f46e5" stroke-width="1.2"/>
  <line x1="182" y1="138" x2="298" y2="138" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#s52-a)"/>
  <text x="240" y="130" text-anchor="middle" font-size="12" font-weight="600" fill="#4f46e5">요청</text>
  <line x1="298" y1="160" x2="184" y2="160" stroke="#94a3b8" stroke-width="1.8" stroke-dasharray="5,3" marker-end="url(#s52-a)"/>
  <text x="240" y="174" text-anchor="middle" font-size="12" font-weight="600" fill="#64748b">답장</text>
  <line x1="240" y1="188" x2="240" y2="210" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="3,3"/>
  <line x1="232" y1="196" x2="248" y2="204" stroke="#94a3b8" stroke-width="1.4"/>
  <line x1="232" y1="204" x2="248" y2="196" stroke="#94a3b8" stroke-width="1.4"/>
  <text x="240" y="228" text-anchor="middle" font-size="11" font-weight="600" fill="#64748b">연결 끊김</text>
  <rect x="520" y="120" width="110" height="56" rx="6" fill="#fff" stroke="#3730a3" stroke-width="1.6"/>
  <text x="575" y="153" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">사용자</text>
  <rect x="750" y="120" width="110" height="56" rx="6" fill="#fff" stroke="#3730a3" stroke-width="1.6"/>
  <text x="805" y="153" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">서버</text>
  <line x1="630" y1="132" x2="750" y2="132" stroke="#3730a3" stroke-width="3.4"/>
  <circle cx="690" cy="132" r="16" fill="#fff" stroke="#3730a3" stroke-width="1.6"/>
  <g transform="translate(678,120) scale(1.0)"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z" fill="#3730a3"/></g>
  <text x="690" y="112" text-anchor="middle" font-size="12" font-weight="700" fill="#3730a3">연결 유지</text>
  <line x1="750" y1="160" x2="632" y2="160" stroke="#4f46e5" stroke-width="2" marker-end="url(#s52-a)"/>
  <text x="691" y="180" text-anchor="middle" font-size="12" font-weight="600" fill="#4f46e5">"주문 완료" (서버가 먼저)</text>
</svg>
</div>

*그림 5-3. 편지와 전화로 본 HTTP 요청·응답과 웹소켓*

:::term-box
**웹소켓(WebSocket)이란?** 클라이언트와 서버가 한 번 연결을 맺으면 이를 끊지 않고 유지하는 통신 방식입니다. 연결이 유효한 동안에는 서버가 클라이언트의 요청을 기다리지 않고도 데이터를 보낼 수 있어, 상태 변화를 실시간으로 전달할 수 있습니다.
:::

지금은 주문이 생성됨과 동시에 완료 처리가 됩니다. 실시간 알림이 올바르게 작동하려면 실제 배달이 끝난 뒤에 주문이 완료되어야 하므로, 배달 완료 기능을 추가해야 합니다.

## 5.2 배달 완료 - 생성과 완료를 분리한다

이제부터 배달 생성이 발생하면 배달이 **PENDING**으로 남고, 배달 기사가 배달 완료 처리를 해야 **COMPLETED**가 됩니다. 배달이 만들어진 뒤 완료되기까지를 순서대로 보겠습니다.

<div class="svg-figure svg-figure--wide">
<svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg">
  <defs>
   <marker id="c53a-s" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
   <marker id="c53a-d" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  </defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">1단계 — 배달 생성 이벤트 발행 → orchestrator 수신 후 대기</text>
  <rect x="345" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <text x="430" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Order</text>
  <text x="430" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">:8081 주문</text>
  <rect x="575" y="64" width="170" height="70" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="660" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">Delivery</text>
  <text x="660" y="116" text-anchor="middle" font-size="14" fill="#3730a3">:8084 배달</text>
  <rect x="280" y="250" width="780" height="120" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <rect x="280" y="250" width="780" height="22" fill="#ff7849"/>
  <text x="670" y="265" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">Kafka — 토픽별로 메시지를 보관·전달</text>
  <rect x="360" y="290" width="110" height="42" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.8"/>
  <path d="M360 290 L415 311 L470 290" fill="none" stroke="#ff7849" stroke-width="1.4"/>
  <text x="415" y="350" text-anchor="middle" font-size="13" font-weight="700" fill="#9a3412">배달 생성 이벤트</text>
  <circle cx="452" cy="298" r="10" fill="#ff7849"/><text x="452" y="302" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
  <rect x="510" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M510 290 L565 311 L620 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
  <text x="565" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">배달 완료 이벤트</text>
  <rect x="660" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M660 290 L715 311 L770 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
  <text x="715" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">주문 완료 명령</text>
  <rect x="300" y="480" width="760" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
  <text x="680" y="510" text-anchor="middle" font-size="20" font-weight="700" fill="#312e81">Orchestrator</text>
  <text x="680" y="534" text-anchor="middle" font-size="14" fill="#312e81">흐름을 결정하는 지휘자 — event를 받아 다음 command를 발행</text>
  <text x="680" y="556" text-anchor="middle" font-size="14" font-weight="700" fill="#b91c1c">배달 완료를 기다리며 여기서 멈춤 (변경점)</text>
  <line x1="660" y1="134" x2="425" y2="248" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#c53a-s)"/>
  <text x="585" y="186" text-anchor="start" font-size="15" font-weight="700" fill="#4f46e5">1. 배달 생성 이벤트 발행</text>
  <line x1="415" y1="370" x2="415" y2="478" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#c53a-d)"/>
  <text x="437" y="429" text-anchor="start" font-size="15" font-weight="700" fill="#3730a3">2. 수신 후 대기</text>
  <rect x="1090" y="40" width="460" height="510" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="550" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">1단계</text>
  <text x="1146" y="128" font-size="21" font-weight="700" fill="#0f172a">1. 배달 생성 이벤트 발행</text>
  <text x="1146" y="160" font-size="19" fill="#475569">배달 서비스가 배달을 PENDING으로</text>
  <text x="1146" y="185" font-size="19" fill="#475569">만든 뒤 <tspan font-weight="700">배달 생성 이벤트</tspan>를 발행합니다.</text>
  <text x="1146" y="245" font-size="21" font-weight="700" fill="#0f172a">2. 수신 후 대기</text>
  <text x="1146" y="277" font-size="19" fill="#475569">orchestrator가 <tspan font-weight="700">배달 생성 이벤트</tspan>를</text>
  <text x="1146" y="302" font-size="19" fill="#475569">받지만, <tspan font-weight="700">주문 완료 명령</tspan>을 보내지</text>
  <text x="1146" y="327" font-size="19" fill="#475569">않고 배달 완료를 기다립니다.</text>
</svg>
</div>

*그림 5-4. 1단계 - 배달 생성 이벤트 발행 → orchestrator 수신 후 대기*

<div class="svg-figure svg-figure--wide">
<svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg">
  <defs>
   <marker id="c53b-s" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
   <marker id="c53b-d" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
   <marker id="c53b-r" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#0d9488"/></marker>
  </defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">2단계 — 배달 완료 API → 배달 완료 이벤트 발행 → orchestrator 수신</text>
  <rect x="345" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <text x="430" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Order</text>
  <text x="430" y="116" text-anchor="middle" font-size="14" fill="#cbd5e1">:8081 주문</text>
  <rect x="575" y="64" width="170" height="70" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="660" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">Delivery</text>
  <text x="660" y="116" text-anchor="middle" font-size="14" fill="#3730a3">:8084 배달</text>
  <rect x="805" y="64" width="170" height="70" rx="8" fill="#f0fdfa" stroke="#0d9488" stroke-width="1.8"/>
  <text x="890" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#0f766e">배달 기사</text>
  <text x="890" y="116" text-anchor="middle" font-size="14" fill="#0d9488">외부 호출자</text>
  <line x1="803" y1="99" x2="747" y2="99" stroke="#0d9488" stroke-width="2.4" marker-end="url(#c53b-r)"/>
  <text x="775" y="90" text-anchor="middle" font-size="13" font-weight="700" fill="#0f766e">PUT /complete</text>
  <rect x="280" y="250" width="780" height="120" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <rect x="280" y="250" width="780" height="22" fill="#ff7849"/>
  <text x="670" y="265" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">Kafka — 토픽별로 메시지를 보관·전달</text>
  <rect x="360" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M360 290 L415 311 L470 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
  <text x="415" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">배달 생성 이벤트</text>
  <rect x="510" y="290" width="110" height="42" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.8"/>
  <path d="M510 290 L565 311 L620 290" fill="none" stroke="#ff7849" stroke-width="1.4"/>
  <text x="565" y="350" text-anchor="middle" font-size="13" font-weight="700" fill="#9a3412">배달 완료 이벤트</text>
  <circle cx="602" cy="298" r="10" fill="#ff7849"/><text x="602" y="302" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
  <rect x="660" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M660 290 L715 311 L770 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
  <text x="715" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">주문 완료 명령</text>
  <rect x="300" y="480" width="760" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
  <text x="680" y="514" text-anchor="middle" font-size="20" font-weight="700" fill="#312e81">Orchestrator</text>
  <text x="680" y="538" text-anchor="middle" font-size="14" fill="#312e81">흐름을 결정하는 지휘자 — event를 받아 다음 command를 발행</text>
  <line x1="660" y1="134" x2="565" y2="248" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#c53b-s)"/>
  <text x="649" y="186" text-anchor="start" font-size="15" font-weight="700" fill="#4f46e5">3. 배달 완료 이벤트 발행</text>
  <line x1="565" y1="370" x2="565" y2="478" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#c53b-d)"/>
  <text x="587" y="429" text-anchor="start" font-size="15" font-weight="700" fill="#3730a3">4. orchestrator가 수신</text>
  <rect x="1090" y="40" width="460" height="510" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="550" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">2단계</text>
  <text x="1146" y="120" font-size="19" font-weight="700" fill="#0f766e">배달 완료 API</text>
  <text x="1146" y="146" font-size="19" fill="#475569">배달 기사가 배달 완료를 처리하면</text>
  <text x="1146" y="171" font-size="19" fill="#475569">배달이 COMPLETED가 됩니다.</text>
  <text x="1146" y="228" font-size="21" font-weight="700" fill="#0f172a">3. 배달 완료 이벤트 발행</text>
  <text x="1146" y="260" font-size="19" fill="#475569">배달 서비스가</text>
  <text x="1146" y="285" font-size="19" fill="#475569"><tspan font-weight="700">배달 완료 이벤트</tspan>를 발행합니다.</text>
  <text x="1146" y="342" font-size="21" font-weight="700" fill="#0f172a">4. orchestrator가 수신</text>
  <text x="1146" y="374" font-size="19" fill="#475569">orchestrator가 <tspan font-weight="700">배달 완료 이벤트</tspan>를</text>
  <text x="1146" y="399" font-size="19" fill="#475569">구독하고 있다가 받습니다.</text>
</svg>
</div>

*그림 5-5. 2단계 - 배달 완료 API → 배달 완료 이벤트 발행 → orchestrator 수신*

<div class="svg-figure svg-figure--wide">
<svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg">
  <defs>
   <marker id="c53c-s" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
   <marker id="c53c-d" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
   <marker id="c53c-w" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#7c3aed"/></marker>
  </defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">3단계 — 주문 완료 명령 발행 → 주문 수신 → WebSocket으로 사용자 알림</text>
  <rect x="345" y="64" width="170" height="70" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="430" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">Order</text>
  <text x="430" y="116" text-anchor="middle" font-size="14" fill="#3730a3">:8081 주문</text>
  <rect x="740" y="64" width="170" height="70" rx="8" fill="#f5f3ff" stroke="#7c3aed" stroke-width="1.8"/>
  <text x="825" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#6d28d9">Client</text>
  <text x="825" y="116" text-anchor="middle" font-size="14" fill="#7c3aed">사용자 화면</text>
  <line x1="517" y1="92" x2="738" y2="92" stroke="#7c3aed" stroke-width="2.4" stroke-dasharray="4,3" marker-end="url(#c53c-w)"/>
  <text x="628" y="120" text-anchor="middle" font-size="13" font-weight="700" fill="#6d28d9">WebSocket Push</text>
  <rect x="280" y="250" width="780" height="120" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <rect x="280" y="250" width="780" height="22" fill="#ff7849"/>
  <text x="670" y="265" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">Kafka — 토픽별로 메시지를 보관·전달</text>
  <rect x="360" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M360 290 L415 311 L470 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
  <text x="415" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">배달 생성 이벤트</text>
  <rect x="510" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
  <path d="M510 290 L565 311 L620 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
  <text x="565" y="350" text-anchor="middle" font-size="13" font-weight="400" fill="#cbd5e1">배달 완료 이벤트</text>
  <rect x="660" y="290" width="110" height="42" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.8"/>
  <path d="M660 290 L715 311 L770 290" fill="none" stroke="#ff7849" stroke-width="1.4"/>
  <text x="715" y="350" text-anchor="middle" font-size="13" font-weight="700" fill="#9a3412">주문 완료 명령</text>
  <circle cx="752" cy="298" r="10" fill="#ff7849"/><text x="752" y="302" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
  <rect x="300" y="480" width="760" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
  <text x="680" y="514" text-anchor="middle" font-size="20" font-weight="700" fill="#312e81">Orchestrator</text>
  <text x="680" y="538" text-anchor="middle" font-size="14" fill="#312e81">흐름을 결정하는 지휘자 — event를 받아 다음 command를 발행</text>
  <line x1="715" y1="478" x2="715" y2="372" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#c53c-s)"/>
  <text x="737" y="429" text-anchor="start" font-size="15" font-weight="700" fill="#4f46e5">5. 주문 완료 명령 발행</text>
  <line x1="715" y1="248" x2="445" y2="136" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#c53c-d)"/>
  <text x="597" y="186" text-anchor="start" font-size="15" font-weight="700" fill="#3730a3">6. 주문 서비스가 수신</text>
  <rect x="1090" y="40" width="460" height="510" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="550" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">3단계</text>
  <text x="1146" y="128" font-size="21" font-weight="700" fill="#0f172a">5. 주문 완료 명령 발행</text>
  <text x="1146" y="160" font-size="19" fill="#475569">orchestrator가</text>
  <text x="1146" y="185" font-size="19" fill="#475569"><tspan font-weight="700">주문 완료 명령</tspan>을 발행합니다.</text>
  <text x="1146" y="245" font-size="21" font-weight="700" fill="#0f172a">6. 주문 서비스가 수신</text>
  <text x="1146" y="277" font-size="19" fill="#475569">주문 서비스가 <tspan font-weight="700">주문 완료 명령</tspan>을 받아</text>
  <text x="1146" y="302" font-size="19" fill="#475569">주문을 COMPLETED로 바꿉니다.</text>
  <text x="1146" y="350" font-size="19" font-weight="700" fill="#6d28d9">WebSocket Push</text>
  <text x="1146" y="382" font-size="19" fill="#475569">사용자 화면에 즉시 알립니다.</text>
</svg>
</div>

*그림 5-6. 3단계 - 주문 완료 명령 발행 → 주문 수신 → 웹소켓 알림*

이 세 단계가 차례로 이어지면, 배달이 실제로 완료되는 순간 사용자에게 완료 알림이 전달됩니다.

## 5.3 웹소켓 연결 흐름

이번에는 웹소켓 연결 흐름을 살펴보겠습니다. 주문 서비스가 보낸 알림이 사용자 화면에 뜨기까지, 크게 세 단계를 거칩니다.

### 5.3.1 브라우저와 주문 서비스의 연결 - HTTP에서 웹소켓으로

전화는 한쪽이 걸고 상대가 받아야 통화가 이어집니다. 마찬가지로 브라우저가 연결을 요청하고 주문 서비스가 받아들이면 **양방향 연결**이 열립니다. 이 연결은 **업그레이드 헤더**를 통해 일반 HTTP에서 **웹소켓**으로 바뀝니다.

<div class="svg-figure">
<svg viewBox="0 0 900 178" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="1단계 연결 핸드셰이크. 브라우저가 frontend와 gateway를 거쳐 주문 서비스로 웹소켓 업그레이드를 요청하면 응답으로 양방향 연결이 열린다.">
  <defs>
    <marker id="rq1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="rs1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#0d9488"/></marker>
  </defs>
  <text x="450" y="32" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">1단계 - 연결 핸드셰이크 (웹소켓 세션 생성)</text>
  <rect x="80" y="78" width="100" height="52" rx="8" fill="#f5f3ff" stroke="#7c3aed" stroke-width="1.8"/>
  <text x="130" y="110" text-anchor="middle" font-size="15" font-weight="700" fill="#6d28d9">브라우저</text>
  <rect x="280" y="78" width="100" height="52" rx="8" fill="#fff" stroke="#475569" stroke-width="1.5"/>
  <text x="330" y="110" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">frontend</text>
  <rect x="430" y="78" width="100" height="52" rx="8" fill="#fff" stroke="#475569" stroke-width="1.5"/>
  <text x="480" y="110" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">gateway</text>
  <rect x="630" y="78" width="120" height="52" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="690" y="110" text-anchor="middle" font-size="15" font-weight="700" fill="#3730a3">주문 서비스</text>
  <text x="450" y="66" text-anchor="middle" font-size="13" font-weight="700" fill="#4f46e5">① 웹소켓 연결 요청 (HTTP → WebSocket 업그레이드)</text>
  <line x1="180" y1="94" x2="272" y2="94" stroke="#4f46e5" stroke-width="2" marker-end="url(#rq1)"/>
  <line x1="380" y1="94" x2="422" y2="94" stroke="#4f46e5" stroke-width="2" marker-end="url(#rq1)"/>
  <line x1="530" y1="94" x2="622" y2="94" stroke="#4f46e5" stroke-width="2" marker-end="url(#rq1)"/>
  <line x1="622" y1="114" x2="538" y2="114" stroke="#0d9488" stroke-width="2" stroke-dasharray="5,3" marker-end="url(#rs1)"/>
  <line x1="422" y1="114" x2="388" y2="114" stroke="#0d9488" stroke-width="2" stroke-dasharray="5,3" marker-end="url(#rs1)"/>
  <line x1="272" y1="114" x2="188" y2="114" stroke="#0d9488" stroke-width="2" stroke-dasharray="5,3" marker-end="url(#rs1)"/>
  <text x="450" y="158" text-anchor="middle" font-size="13" font-weight="700" fill="#0f766e">② 양방향 연결 수립</text>
</svg>
</div>

*그림 5-7. 1단계 - 브라우저가 청하고 서버가 받아들여 양방향 연결이 열립니다*

:::term-box
**업그레이드 헤더란?** HTTP Upgrade 헤더는 클라이언트와 서버가 현재 사용 중인 HTTP 연결을 다른 프로토콜로 전환하기 위해 사용하는 헤더입니다. 주로 웹소켓 연결을 설정할 때 사용되며, 이를 통해 동일한 연결에서 새로운 통신 방식을 사용할 수 있습니다.
:::

### 5.3.2 브라우저의 채널 구독 - 명부에 등록

웹소켓이 연결되더라도 서버는 누구에게 어떤 알림을 보낼지 스스로 알 수 없습니다. 따라서 브라우저가 먼저 서버에 자신이 받을 채널을 알려주며 **구독(Subscribe)** 해야 합니다.

브라우저가 특정 채널을 구독하면, 주문 서비스 안의 웹소켓 브로커는 **구독 명부**에 그 사실을 기록해 둡니다. 즉, 브라우저가 구독하고 서버가 명부를 작성해 관리하는 구조입니다. 이제 서버는 이 명부를 보고 정확한 대상에게 알림을 발송합니다.

<div class="svg-figure">
<svg viewBox="0 0 900 178" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="2단계 구독 등록. 브라우저가 채널을 SUBSCRIBE로 알리고, 이 프레임은 1단계 연결을 타고 frontend와 gateway를 그대로 통과해 주문 서비스에 닿는다. 주문 서비스 안의 웹소켓 브로커가 구독 명부에 세션 A는 topic/orders/3이라고 등록한다.">
  <defs>
    <marker id="rq2" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="450" y="28" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">2단계 - 구독 등록 (받을 채널을 명부에 적기)</text>
  <rect x="70" y="84" width="118" height="56" rx="8" fill="#f5f3ff" stroke="#7c3aed" stroke-width="1.8"/>
  <text x="129" y="118" text-anchor="middle" font-size="14.5" font-weight="700" fill="#6d28d9">브라우저</text>
  <text x="223" y="100" text-anchor="middle" font-size="11.5" font-weight="700" fill="#4f46e5">구독</text>
  <line x1="188" y1="112" x2="258" y2="112" stroke="#4f46e5" stroke-width="2" marker-end="url(#rq2)"/>
  <rect x="262" y="88" width="64" height="48" rx="6" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="294" y="107" text-anchor="middle" font-size="10" fill="#94a3b8">frontend</text>
  <text x="294" y="123" text-anchor="middle" font-size="10" fill="#94a3b8">gateway</text>
  <line x1="326" y1="112" x2="404" y2="112" stroke="#4f46e5" stroke-width="2" marker-end="url(#rq2)"/>
  <rect x="408" y="74" width="372" height="92" rx="12" fill="#eef2ff" stroke="#4f46e5" stroke-width="2"/>
  <text x="428" y="96" font-size="13" font-weight="700" fill="#3730a3">주문 서비스</text>
  <text x="428" y="116" font-size="10.5" fill="#64748b">구독 명부 (웹소켓 브로커)<tspan fill="#4f46e5" font-weight="700">&#160;&#160;· 방금 추가</tspan></text>
  <rect x="428" y="124" width="332" height="32" rx="9" fill="#fff" stroke="#4f46e5" stroke-width="1.4"/>
  <text x="446" y="145" font-size="12.5" fill="#3730a3">세션 A&#160;&#160;→&#160;&#160;<tspan class="mono" fill="#ff7849" font-weight="700">/topic</tspan><tspan class="mono" fill="#0f172a">/orders/</tspan><tspan class="mono" fill="#7c3aed" font-weight="700">3</tspan></text>
</svg>
</div>

*그림 5-8. 2단계 - 브라우저가 구독하면 웹소켓 브로커가 구독 명부에 등록합니다*

:::term-box
**웹소켓 브로커란?** 메시지를 보내는 쪽과 받는 쪽 사이에서 전달을 중개하는 역할입니다. 어떤 클라이언트가 어떤 채널을 구독했는지 명부로 관리하다가, 메시지가 들어오면 같은 채널을 구독한 클라이언트에게 전달합니다.
:::

### 5.3.3 주문 서비스의 알림 발송 - 같은 채널 찾아 전달

채널 주소에는 **알림을 받을 사용자**에 대한 정보가 들어 있습니다. 그래서 주문이 완료되면, 주문 서비스는 완료된 주문이 누구의 것인지부터 확인합니다. 그리고 주문한 사용자의 채널 주소를 구독 명부에서 찾아 알림을 보냅니다.

<div class="svg-figure">
<svg viewBox="0 0 900 184" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="3단계 발송과 전달. 주문 서비스 안의 completeOrder가 발송 주소 topic/orders/3으로 같은 서비스 안의 구독 명부를 찾는다. 명부의 세션 A가 topic/orders/3을 구독하고 있으므로 주문 완료 알림으로 orderId 4를 보내고, 이 메시지는 1단계 연결을 타고 gateway와 frontend를 그대로 통과해 브라우저에 닿는다.">
  <defs>
    <marker id="rq3" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="rs3" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#0d9488"/></marker>
  </defs>
  <text x="450" y="28" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">3단계 - 발송과 전달 (명부에서 같은 채널 찾기)</text>
  <rect x="40" y="72" width="450" height="100" rx="12" fill="#eef2ff" stroke="#4f46e5" stroke-width="2"/>
  <text x="60" y="94" font-size="13" font-weight="700" fill="#3730a3">주문 서비스</text>
  <rect x="60" y="104" width="144" height="54" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <text x="132" y="128" text-anchor="middle" font-size="12.5" class="mono" fill="#0f172a">completeOrder()</text>
  <text x="132" y="146" text-anchor="middle" font-size="10" fill="#64748b">주문 완료 처리</text>
  <text x="230" y="120" text-anchor="middle" font-size="10.5" font-weight="700" fill="#4f46e5">발송</text>
  <line x1="204" y1="131" x2="252" y2="131" stroke="#4f46e5" stroke-width="2" marker-end="url(#rq3)"/>
  <text x="256" y="94" font-size="10.5" fill="#64748b">구독 명부 (웹소켓 브로커)</text>
  <rect x="256" y="104" width="216" height="46" rx="9" fill="#fff" stroke="#4f46e5" stroke-width="1.4"/>
  <text x="272" y="132" font-size="12.5" fill="#3730a3">세션 A&#160;&#160;→&#160;&#160;<tspan class="mono" fill="#ff7849" font-weight="700">/topic</tspan><tspan class="mono" fill="#0f172a">/orders/</tspan><tspan class="mono" fill="#7c3aed" font-weight="700">3</tspan></text>
  <text x="658" y="114" text-anchor="middle" font-size="11.5" font-weight="700" fill="#0f766e">주문 완료 알림</text>
  <line x1="490" y1="127" x2="536" y2="127" stroke="#0d9488" stroke-width="3" marker-end="url(#rs3)"/>
  <rect x="540" y="103" width="64" height="48" rx="6" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="572" y="122" text-anchor="middle" font-size="10" fill="#94a3b8">gateway</text>
  <text x="572" y="138" text-anchor="middle" font-size="10" fill="#94a3b8">frontend</text>
  <line x1="604" y1="127" x2="712" y2="127" stroke="#0d9488" stroke-width="3" marker-end="url(#rs3)"/>
  <text x="658" y="146" text-anchor="middle" font-size="10.5" class="mono" fill="#475569">{ orderId: 4 }</text>
  <rect x="716" y="99" width="158" height="56" rx="8" fill="#f5f3ff" stroke="#7c3aed" stroke-width="1.8"/>
  <text x="795" y="123" text-anchor="middle" font-size="14.5" font-weight="700" fill="#6d28d9">브라우저</text>
  <text x="795" y="142" text-anchor="middle" font-size="10" fill="#64748b">화면에 '주문 완료!' 표시</text>
</svg>
</div>

*그림 5-9. 3단계 - 발송 주소와 같은 채널을 명부에서 찾아 구독한 브라우저에 보냅니다*

세 단계가 모두 갖춰지면, 배달이 끝나는 순간 사용자 화면에 주문 완료가 표시됩니다.

이제 코드로 구현해 보겠습니다. 먼저 배달 서비스에서 배달의 생성과 완료 과정을 분리하는 작업부터 시작합니다.

## 5.4 배달 서비스 - 배달 완료 API

배달 서비스는 배달의 생성과 완료를 분리하고, 배달 기사가 호출할 배달 완료 API를 추가합니다.

### 5.4.1 createDelivery 수정 - 배달 생성·완료 분리

배달 생성 시 배달 완료 호출을 지우면 배달은 **PENDING**으로 남습니다. 배달 완료는 배달 기사가 직접 호출할 때까지 미뤄집니다.

`usecase/DeliveryService.java`의 `createDelivery`를 아래처럼 고칩니다.

**[실습 1] usecase/DeliveryService.java. 생성 시 완료 호출 제거**
```java
@Transactional
public DeliveryResponse createDelivery(int orderId, String address) {
    Delivery createdDelivery = deliveryRepository.save(Delivery.create(orderId, address));
    Delivery.validateAddress(address);
    // 삭제: createdDelivery.complete();  ← 생성 시 완료 호출 제거
    return DeliveryResponse.from(createdDelivery);
}
```

### 5.4.2 completeDelivery 추가 - 배달 완료 API

이번에는 배달 기사가 호출할 배달 완료 메서드를 추가합니다.

**[실습 2] usecase/DeliveryService.java. completeDelivery 추가**
```java
@Override
@Transactional
public DeliveryResponse completeDelivery(int deliveryId) {
    Delivery findDelivery = deliveryRepository.findById(deliveryId)
            .orElseThrow(() -> new Exception404("배달 정보를 조회할 수 없습니다."));
    findDelivery.complete();
    deliveryEventProducer.publishDeliveryCompleted(
            new DeliveryCompletedEvent(findDelivery.getOrderId()));
    return DeliveryResponse.from(findDelivery);
}
```

배달 기사가 배달 완료를 호출하면 배달이 완료되고, 배달 완료 이벤트가 발행됩니다. 이제 이 이벤트를 orchestrator가 받도록 수정합니다.

## 5.5 orchestrator - 배달 완료 이벤트 처리 추가

챕터 4에서는 배달 생성이 성공하면 orchestrator가 곧바로 주문 완료 명령을 발행했습니다. 이번에는 배달이 완료될 때 주문 완료 명령을 발행하도록 바꿉니다.

`handler/OrderOrchestrator.java`에 `deliveryCompleted` 리스너를 추가합니다.

**[실습 3] handler/OrderOrchestrator.java. deliveryCompleted - 주문 완료 명령 발행**
```java
@KafkaListener(topics = "delivery-completed", groupId = "orchestrator")
public void deliveryCompleted(DeliveryCompletedEvent event) {
    // 배달기사가 완료 API를 호출한 시점 → 주문 완료 명령 발행
    kafkaTemplate.send(
            "complete-order-command",
            String.valueOf(event.orderId()),
            new CompleteOrderCommand(event.orderId())
    );
}
```

## 5.6 주문 서비스 - STOMP로 실시간 Push 구현

마지막으로 주문 서비스가 주문 완료 명령을 받으면, 클라이언트에게 알리기 위해 웹소켓을 추가합니다.

### 5.6.1 웹소켓 설정

WebSocketConfig는 두 가지 주소를 등록합니다. 하나는 **클라이언트가 웹소켓으로 연결할 주소(`/api/ws/orders`)** 이고, 다른 하나는 **서버와 클라이언트가 알림을 주고받을 주소의 접두사(`/topic`)** 입니다.

`core/config/WebSocketConfig.java`를 열고 아래 클래스를 작성합니다.

**[실습 4] core/config/WebSocketConfig.java. STOMP 웹소켓 설정**
```java
@Configuration
@EnableWebSocketMessageBroker // 이 애너테이션을 붙이면 STOMP 메시징 기능이 켜집니다
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    @Override
    public void configureMessageBroker(MessageBrokerRegistry config) {
        // /topic으로 시작하는 주소로 메시지가 오면,
        // 서버가 같은 주소를 구독한 클라이언트에게 전달합니다
        config.enableSimpleBroker("/topic");
    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        // 클라이언트가 웹소켓 연결을 시작할 주소입니다. 어떤 출처에서든 연결을 허용합니다
        registry.addEndpoint("/api/ws/orders").setAllowedOriginPatterns("*").withSockJS();
    }
}
```

:::note
**웹소켓 위에 STOMP 프로토콜을 사용합니다.** 웹소켓은 서버와 클라이언트를 계속 연결해 주지만, 연결만으로는 메시지를 누구에게 보낼지 가려내지 못합니다. 그래서 이 연결 위에 **STOMP(Simple Text Oriented Messaging Protocol)** 라는 메시징 규칙을 얹습니다. STOMP는 메시지마다 채널(주소)을 붙이고, **그 채널을 구독한 클라이언트에게만 전달하는 발행-구독 구조**를 제공합니다. 이 예제에서 서버는 `/topic/orders/{userId}` 채널로 보내고, 같은 채널을 구독한 사용자만 자기 주문 완료 알림을 받습니다.
:::

클라이언트는 연결 주소로 웹소켓을 연 뒤, `/topic` 주소를 구독해 알림을 받습니다. 이때 웹소켓 브로커는 구독한 주소를 명부에 등록해 둡니다.

### 5.6.2 주문 완료 시 알림 발송

완료 알림은 `/topic/orders/{userId}` 채널로 보냅니다. 주문 완료 후 채널을 구독한 클라이언트에게 메시지를 전달합니다.

`usecase/OrderService.java`의 `completeOrder` 메서드를 아래처럼 수정합니다.

**[실습 5] usecase/OrderService.java. completeOrder + WebSocket Push**
```java
@Transactional
public void completeOrder(int orderId) {
    Order findOrder = orderRepository.findById(orderId)
            .orElseThrow(() -> new Exception404("주문을 찾을 수 없습니다."));
    findOrder.complete();
    // 추가: 이 채널을 구독한 클라이언트에게 메시지를 보냄
    messagingTemplate.convertAndSend(
            "/topic/orders/" + findOrder.getUserId(),
            Map.of("orderId", orderId));
}
```

핵심 코드 외에 주문 서비스에 필요한 설정은 깃헙 레포에서 확인합니다.

## 5.7 프론트엔드 연결

서버는 주문이 완료되면 채널로 알림을 보냅니다. 이제 **같은 채널을 구독해 알림을 받는 클라이언트**를 만들 차례입니다. 먼저 프록시가 웹소켓 연결을 끊지 않게 하고, 브라우저가 STOMP로 자기 채널을 구독하게 합니다.

### 5.7.1 업그레이드 헤더 전달

앞에서 본 업그레이드 헤더는 브라우저와 주문 서비스 사이의 frontend와 gateway를 거쳐야 합니다. 그런데 이 둘이 업그레이드 헤더를 넘기지 않으면 일반 요청처럼 처리돼 **연결이 끊깁니다**. 그래서 frontend와 gateway 두 곳의 nginx에 **업그레이드 헤더를 전달**하도록 설정합니다.

`frontend/nginx.conf`의 `/api/ws/` 위치에 아래처럼 설정합니다.

**[참고] frontend/nginx.conf. 웹소켓 업그레이드 헤더**
```nginx
location /api/ws/ {
    proxy_pass http://gateway;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

`gateway/nginx.conf`의 `/api/ws/` 블록에도 같은 코드를 넣습니다. 그래야 브라우저에서 gateway까지 업그레이드 헤더가 끊기지 않고 전달됩니다.

### 5.7.2 클라이언트 - STOMP 구독

`frontend/index.html`은 서버 알림을 받아 화면에 주문 완료를 표시하는 STOMP 클라이언트입니다. 주문하기 버튼을 누르면, 먼저 웹소켓을 연결하고 자기 주문 완료 알림이 올 `/topic/orders/{userId}` 채널을 구독합니다. 알림 받을 준비를 마친 다음 주문 API를 호출합니다.

**[참고] frontend/index.html. STOMP 연결과 구독**
```javascript
// 1. /api/ws/orders로 웹소켓 연결
stomp = Stomp.over(new SockJS('/api/ws/orders?token=' + TOKEN));
stomp.connect({}, function () {
    // 2. 내 주문 알림 채널 구독
    stomp.subscribe('/topic/orders/' + userId, function (msg) {
        // 3. 서버가 보낸 메시지를 화면에 표시
        const data = JSON.parse(msg.body);
        status.textContent = '주문 완료! (주문번호: ' + data.orderId + ')';
    });
});
```

클라이언트와 서버 양쪽 코드에서 웹소켓 연결 주소(`/api/ws/orders`)와 구독 채널 주소(`/topic/orders/{userId}`)를 동일하게 맞춰주어야 정상적으로 알림이 전달됩니다. 전체 index.html은 깃헙 레포에서 확인합니다.

<div class="svg-figure">
<svg viewBox="0 0 760 372" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="서버와 클라이언트가 같은 연결 주소와 같은 채널 주소를 써야 한다. 연결은 addEndpoint와 SockJS가 /api/ws/orders로 일치해야 하고, 발행 convertAndSend와 구독 subscribe가 /topic/orders/userId로 일치해야 하며 /topic은 enableSimpleBroker 접두사다.">
  <defs><marker id="ln" markerWidth="9" markerHeight="9" refX="4" refY="3" orient="auto"><circle cx="3" cy="3" r="3" fill="#4f46e5"/></marker></defs>
  <rect x="24" y="12" width="330" height="28" rx="7" fill="#eef2ff"/>
  <text x="189" y="31" text-anchor="middle" font-size="13" font-weight="700" fill="#3730a3">서버 (주문 서비스)</text>
  <rect x="406" y="12" width="330" height="28" rx="7" fill="#eef2ff"/>
  <text x="571" y="31" text-anchor="middle" font-size="13" font-weight="700" fill="#3730a3">클라이언트 (브라우저 index.html)</text>
  <text x="24" y="64" font-size="13" font-weight="700" fill="#0f172a">① 연결 — 서버가 등록한 주소로, 클라이언트가 똑같이 연결합니다</text>
  <rect x="24" y="74" width="330" height="58" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <text x="38" y="96" font-size="11" fill="#64748b">WebSocketConfig — 웹소켓 연결 주소 지정</text>
  <text x="38" y="119" font-size="13" font-family="var(--font-mono)" fill="#0f172a">addEndpoint(&quot;<tspan fill="#4f46e5" font-weight="700">/api/ws/orders</tspan>&quot;)</text>
  <rect x="406" y="74" width="330" height="58" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <text x="420" y="96" font-size="11" fill="#64748b">index.html — 연결 시도</text>
  <text x="420" y="119" font-size="13" font-family="var(--font-mono)" fill="#0f172a">new SockJS(&quot;<tspan fill="#4f46e5" font-weight="700">/api/ws/orders</tspan>&quot;)</text>
  <line x1="354" y1="103" x2="406" y2="103" stroke="#4f46e5" stroke-width="2" marker-start="url(#ln)" marker-end="url(#ln)"/>
  <rect x="358" y="89" width="44" height="28" rx="14" fill="#4f46e5"/>
  <text x="380" y="109" text-anchor="middle" font-size="17" font-weight="800" fill="#fff">=</text>
  <rect x="24" y="146" width="712" height="32" rx="7" fill="#fff4ed" stroke="#ff7849" stroke-width="1.3"/>
  <text x="380" y="167" text-anchor="middle" font-size="11.5" fill="#9a3412">아래 발행·구독 주소는 모두 <tspan font-weight="800">&quot;/topic&quot;</tspan> 으로 시작해야 합니다</text>
  <text x="24" y="210" font-size="13" font-weight="700" fill="#0f172a">② 발행·구독 — 서버가 보낸 채널 주소를, 클라이언트가 똑같이 구독합니다</text>
  <rect x="24" y="220" width="330" height="60" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <text x="38" y="242" font-size="11" fill="#64748b">OrderService — 주문 완료 시 발행</text>
  <text x="38" y="265" font-size="13" font-family="var(--font-mono)" fill="#0f172a">convertAndSend(&quot;<tspan fill="#ff7849" font-weight="700">/topic</tspan>/orders/<tspan fill="#7c3aed" font-weight="700">3</tspan>&quot;)</text>
  <rect x="406" y="220" width="330" height="60" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <text x="420" y="242" font-size="11" fill="#64748b">index.html — 연결 후 구독</text>
  <text x="420" y="265" font-size="13" font-family="var(--font-mono)" fill="#0f172a">subscribe(&quot;<tspan fill="#ff7849" font-weight="700">/topic</tspan>/orders/<tspan fill="#7c3aed" font-weight="700">3</tspan>&quot;)</text>
  <line x1="354" y1="250" x2="406" y2="250" stroke="#4f46e5" stroke-width="2" marker-start="url(#ln)" marker-end="url(#ln)"/>
  <rect x="358" y="236" width="44" height="28" rx="14" fill="#4f46e5"/>
  <text x="380" y="256" text-anchor="middle" font-size="17" font-weight="800" fill="#fff">=</text>
  <path d="M170 280 V 304 H 590 V 280" fill="none" stroke="#7c3aed" stroke-width="1.6" stroke-dasharray="5,4"/>
  <rect x="300" y="291" width="160" height="26" rx="13" fill="#f5f3ff" stroke="#7c3aed" stroke-width="1.2"/>
  <text x="380" y="308" text-anchor="middle" font-size="11.5" font-weight="700" fill="#7c3aed">userId 가 같은 사람만 받습니다</text>
  <text x="380" y="352" text-anchor="middle" font-size="12" fill="#475569">한 글자라도 다르면 연결도, 알림 전달도 되지 않습니다.</text>
</svg>
</div>

*그림 5-10. 웹소켓 주소 일치 - 같은 색은 글자까지 똑같아야 동작합니다*

## 5.8 전체 시스템 통합 테스트

이제 전체 시스템을 실행해, 주문 생성부터 완료 알림까지 전체 흐름을 확인합니다.

### 5.8.1 Kubernetes 리소스 정의

이전 챕터까지의 구성에서 frontend 서비스가 새로 추가됩니다. `k8s/frontend/` 폴더에 Deployment, Service, Ingress가 정의되어 있습니다.

| 파일 | 역할 |
|------|------|
| **frontend-deploy.yml** | Nginx 기반 프론트엔드 Pod |
| **frontend-service.yml** | 클러스터 내부 접근용 Service |
| **frontend-ingress.yml** | 외부 요청을 frontend-service로 라우팅 |

이번 챕터부터 Ingress는 gateway-service 대신 **frontend-service**로 요청을 보냅니다. 프론트엔드 Nginx가 정적 파일을 직접 응답하고, `/api/` 요청만 gateway-service로 전달합니다.

### 5.8.2 이미지 빌드

Minikube 내부에 이미지를 빌드합니다.

**[터미널] 이미지 빌드**
```bash
minikube image build -t metacoding/db:3 ./db
minikube image build -t metacoding/gateway:3 ./gateway
minikube image build -t metacoding/order:3 ./order
minikube image build -t metacoding/product:3 ./product
minikube image build -t metacoding/user:3 ./user
minikube image build -t metacoding/delivery:3 ./delivery
minikube image build -t metacoding/orchestrator:3 ./orchestrator
minikube image build -t metacoding/frontend:3 ./frontend
```

### 5.8.3 배포

Kafka를 먼저 배포하고, 준비될 때까지 기다린 다음 나머지를 배포합니다.

**[터미널] 배포 순서 (Kafka 우선)**
```bash
# 1. 네임스페이스 생성
kubectl create namespace metacoding

# 2. Kafka 먼저 배포
kubectl apply -f k8s/kafka

# 3. Kafka가 준비될 때까지 대기
kubectl wait --for=condition=ready pod -l app=kafka -n metacoding --timeout=120s

# 4. 나머지 서비스 배포
kubectl apply -f k8s/db
kubectl apply -f k8s/gateway
kubectl apply -f k8s/order
kubectl apply -f k8s/product
kubectl apply -f k8s/user
kubectl apply -f k8s/delivery
kubectl apply -f k8s/orchestrator
kubectl apply -f k8s/frontend

# 5. Ingress 활성화 (최초 1회)
minikube addons enable ingress
```

모든 Pod가 Running 상태가 될 때까지 대기합니다.

**[터미널] Pod 상태 확인**
```bash
kubectl get pods -n metacoding
```

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">kubectl get pods -n metacoding</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div class="tl-kv-row"><span class="tl-label">NAME</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-label">READY</span>&nbsp;&nbsp;<span class="tl-label">STATUS</span>&nbsp;&nbsp;&nbsp;<span class="tl-label">AGE</span></div>
    <div class="tl-kv-row">kafka-deploy-7d4c8b9f5-2xk9p&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">2m</span></div>
    <div class="tl-kv-row">db-deploy-6f9b7c4d8-m4t2q&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">90s</span></div>
    <div class="tl-kv-row">gateway-deploy-5c8d6f7b9-h7w3r&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">88s</span></div>
    <div class="tl-kv-row">order-deploy-8b7f6c9d4-q2k8m&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">85s</span></div>
    <div class="tl-kv-row">product-deploy-7c9d8b6f5-x4r2t&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">83s</span></div>
    <div class="tl-kv-row">user-deploy-6d8c7b9f4-p3m9k&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">80s</span></div>
    <div class="tl-kv-row">delivery-deploy-9f7c8b6d5-t6w2x&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">78s</span></div>
    <div class="tl-kv-row">orchestrator-deploy-8c6f9b7d4-k9m4q&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">75s</span></div>
    <div class="tl-kv-row">frontend-deploy-7b9c6d8f5-w3k2m&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">72s</span></div>
    <div class="tl-divider"><span class="tl-val">9개 Pod Running (frontend 추가)</span><span class="tl-cursor"></span></div>
  </div>
</div>

*그림 5-11. Pod 상태 확인*

### 5.8.4 서비스 접근

외부에서 Ingress로 접속하기 위해 `minikube tunnel`을 실행합니다.

**[터미널] 외부 접근 터널**
```bash
minikube tunnel
```

터널이 실행되면 `http://127.0.0.1:80`로 프론트엔드에 접속할 수 있습니다.

### 5.8.5 통합 테스트 시나리오

**Step 1: 웹소켓 연결 및 주문 생성**

브라우저로 index.html에 접속합니다. 그다음 로그인 API(`POST /login`)에서 발급받은 JWT 토큰을 입력하여 웹소켓을 연결합니다.

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH05/terminal/05_index-html-initial.png)
*그림 5-12. 브라우저에서 index.html 접속 화면*

주문하기 버튼을 클릭합니다. 그러면 index.html이 웹소켓에 연결하고 `/topic/orders/{userId}` 채널을 구독합니다.

**[자동 전송] index.html이 보내는 주문 요청**
```json
POST /api/orders

{
  "productId": 1,
  "quantity": 1,
  "price": 2500000,
  "address": "Addr 4"
}
```

이 요청은 주문하기 버튼을 누르면 index.html이 자동으로 보내므로, 직접 호출하지 않아도 됩니다.

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH05/terminal/06_token-order.png)
*그림 5-13. 토큰 입력 후 주문하기 버튼 클릭*

브라우저 `F12` - `Console`에서 웹소켓이 연결됨을 확인할 수 있습니다.

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH05/terminal/07_websocket-connect.png)
*그림 5-14. 브라우저 Console에서 웹소켓 연결 확인*

Hoppscotch로 생성된 주문을 확인하면 **`PENDING`** 상태로 머물러 있습니다.
**[Hoppscotch] 주문 조회**
```json
GET http://127.0.0.1:80/api/orders/4
```

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH05/terminal/08_order-pending.png)
*그림 5-15. 주문 조회 결과 - PENDING 상태*

**Step 2: 배달 완료**

먼저 생성된 배달을 확인해보겠습니다.

**[Hoppscotch] 배달 조회**
```json
GET http://127.0.0.1:80/api/deliveries/4
```

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH05/terminal/09_delivery-pending.png)
*그림 5-16. 배달 조회 결과 - PENDING 상태*

배달 ID가 4인 배달이 **`PENDING`** 상태로 생성되었습니다.

배달 완료 API를 호출해 완료 처리를 합니다.

**[Hoppscotch] 배달 완료 호출**
```json
PUT http://127.0.0.1:80/api/deliveries/4/complete
```

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH05/terminal/10_delivery-completed.png)
*그림 5-17. 배달 완료 API 호출 결과 - COMPLETED 상태*

*배달 완료 버튼을 눌렀다. 이제 주문도 바뀌었을까?*

**Step 3: 주문 완료 및 웹소켓 응답 확인**

배달 완료 처리 후, 주문 완료 명령으로 주문이 **`COMPLETED`** 상태가 됩니다.
**[Hoppscotch] 주문 조회**
```json
GET http://127.0.0.1:80/api/orders/4
```

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH05/terminal/11_order-completed.png)
*그림 5-18. 주문 조회 결과 - COMPLETED 상태*

주문이 완료되면 웹소켓이 클라이언트에게 주문 완료 메시지를 전송합니다.
웹소켓 응답을 수신하면 클라이언트 화면이 주문 완료 상태로 변경됩니다.

![](/work_삭제용/book-workflow/projects/특이점이-온-개발자-MSA/chapters/assets/CH05/terminal/12_websocket-notification.png)
*그림 5-19. 웹소켓 알림 수신 - 클라이언트 화면에 주문 완료 표시*

완성한 화면을 동료에게 보여 줬습니다. 주문하기를 누르자 잠시 뒤 '처리 중'이 '주문 완료'로 바뀌었습니다.

**동료**: "이제 사용자도 새로고침 없이 주문이 끝난 걸 바로 알 수 있겠네요."

하나로 구성됐던 서비스를 기능별로 분리하고, 사용자에게 실시간으로 알리는 웹소켓까지 더했습니다. 이제 한쪽 서비스에 부하가 몰려도 전체가 멈추지 않고, 주문이 끝나는 순간 사용자 화면에 완료가 바로 표시됩니다.

:::remember
**이것만은 기억하자**

- **폴링**은 클라이언트가 변화를 계속 확인해야 하지만, **웹소켓**은 서버가 변화 순간 먼저 알립니다.
- 배달 생성과 배달 완료를 분리해, 주문 완료를 **실제 배달이 끝난 시점**에 맞춥니다.
- 주문이 완료되면 주문 서비스가 **웹소켓**으로 사용자에게 실시간으로 알립니다.
:::



---


# 에필로그. 다시, 트래픽이 몰리던 날

그 후로 몇 달이 지났습니다.

대규모 할인 행사가 열린 금요일 저녁 일곱 시. 예전 같았으면 쏟아지는 트래픽에 시스템 어딘가가 멈춰서 복구하느라 정신없었을 시간입니다.

하지만 이번에는 주말 내내 휴대폰이 조용했습니다. 한쪽 서비스에 부하가 몰려도 장애가 시스템 전체로 번지지 않도록 구조를 바꾼 덕분입니다. 서버 장애 알림 없이 주말을 온전히 쉰 건 참 오랜만이었습니다.

월요일 아침, 팀장님이 지나가며 물었습니다.

**팀장**: "이번에 트래픽 엄청나던데, 주말에 별일 없었나 봐요?"

**오픈이**: "네, 별일 없었습니다."

주문이 몰린다고 서버 전체가 다운되던 일은 이제 과거가 되었습니다.

물론 사이트가 발전하면 새로운 서비스가 추가될 테고, 시스템이 커지는 만큼 또 어딘가에서 예상치 못한 문제가 생길 수 있습니다.

하지만 이제는 전처럼 막연하게 걱정되지 않습니다. 시스템을 직접 분리하고 연결하며 문제를 해결해 본 경험이 있으니, 어디가 막히든 원인을 찾고 다시 개선해 나가면 되기 때문입니다.



---


# 마치며

## 챕터별 비교

| | 챕터 2 | 챕터 3 | 챕터 4 | 챕터 5 |
|---|---|---|---|---|
| 통신 | REST 동기 | REST 동기 | Kafka 비동기 | Kafka 비동기 |
| 트랜잭션 | 보상 트랜잭션 | 보상 트랜잭션 | Orchestration Saga | Orchestration Saga |
| 아키텍처 | 레이어드 | Clean (UseCase) | Clean + 이벤트 | Clean + 이벤트 |
| 배포 | 로컬 | Kubernetes | K8s + Kafka | K8s + Kafka |
| 배달 완료 | 자동 (생성 시) | 자동 (생성 시) | 자동 (생성 시) | 수동 API 호출 |
| 실시간 알림 | 없음 | 없음 | 없음 | WebSocket Push |

## 마지막으로

하나의 모놀리식 서비스가 여러 갈래로 나뉘고, 그 기반에 쿠버네티스와 카프카가 더해지기까지의 과정을 함께 짚어봤습니다. 우리가 지나온 길은 유행하는 기술을 하나씩 추가하는 숙제가 아니었습니다. 당면한 문제를 풀기 위해 시스템의 경계를 넓히고, 코드를 바꾸며 아키텍처를 진화시켜 나간 과정이었습니다.

동기에서 비동기로, 하나에서 여럿으로 시선을 옮기는 일이 처음에는 복잡하고 막막했을지도 모릅니다. 하지만 거대해 보이던 마이크로서비스 아키텍처(MSA)도 결국은 작은 문제를 하나씩 풀어간 고민들이 모여 만들어집니다. 처음 'MSA'라는 단어 앞에서 막막하던 때와 지금의 여러분은 분명 다릅니다.

직접 만든 시스템에는 아쉬운 구석이 남기도 합니다. 그건 부족함이 아니라, 다음 걸음이 보이기 시작했다는 신호입니다. 앞으로도 막히는 날은 옵니다. 그때 처음부터 다 알아야 한다고 자신을 몰아세우지 마세요. 부딪히고, 고치고, 다시 만들면 됩니다. 좋은 구조를 고민하고 코드를 바꾸는 일은 결국 우리 같은 개발자의 몫이니까요.

이제 책장을 닫고 코드로 돌아갈 시간입니다. 이 책에서 다룬 기술과 힌트가, 앞으로 마주할 수많은 트래픽과 서비스 앞에서 작은 이정표가 되기를 바랍니다.

이제 여러분 차례입니다.



---

