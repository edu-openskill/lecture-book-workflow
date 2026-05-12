# 챕터 5. 실시간 알림 - 주문 완료를 즉시 전달하다

> 이 챕터의 전체 소스코드는 **https://github.com/metacoding-12-msa/ex04** 에서 확인할 수 있습니다.


:::goal
이번 챕터가 끝나면

- 폴링의 문제점을 이해하고 WebSocket의 장점을 설명할 수 있습니다.
- delivery-service에 배달 완료 API를 추가하고 배달 완료 이벤트를 발행할 수 있습니다.
- orchestrator가 배달 완료 이벤트를 받아 주문 완료 명령을 발행하도록 수정할 수 있습니다.
- order-service에 WebSocket을 설정하고 주문 완료 시 사용자에게 실시간 알림을 보낼 수 있습니다.
- 전체 시스템을 통합 테스트할 수 있습니다.
:::

::::prep
**준비하기**. 실습 시작 전 한 번만 설정

### 1. 소스 코드 클론

```bash [터미널] 레포 클론
git clone https://github.com/metacoding-12-msa/ex04.git
cd ex04
```

### 2. 실습 환경

챕터 4까지 사용한 Docker Desktop, Minikube가 그대로 필요합니다. 별도 추가 도구는 없습니다. 프론트엔드도 Nginx 컨테이너로 Minikube 안에서 함께 띄우므로 따로 서버를 띄울 필요는 없습니다.

### 3. 실습 순서

1. delivery-service에 배달 완료 API + `delivery-completed` 이벤트 추가
2. orchestrator에 `delivery-completed` 처리 + `delivery-created` 성공 시 대기로 변경
3. order-service에 STOMP WebSocket 설정 + 주문 완료 시 Push
4. SockJS 기반 index.html 프론트엔드와 Nginx 프록시 구성
5. K8s에 frontend 추가 배포 → 통합 시나리오 검증
::::

**오픈이**: "사용자가 새로고침을 누르지 않아도, 주문 완료를 바로 알게 하고 싶어요."

**선배**: "그럼 WebSocket을 붙여 봐요. 서버가 먼저 사용자에게 말을 걸 수 있게 통로를 열어주는 거예요."

## 5.1 챕터 4가 남긴 두 가지 숙제

챕터 4를 마치면서 두 가지 한계를 이야기했습니다.

**첫 번째**: 사용자가 주문 완료를 알려면 직접 계속 조회해야 합니다. 동기 방식이라면 응답에 결과가 바로 담겨오지만, 비동기 방식에서는 결과가 나중에 정해집니다. 주문 직후 `PENDING` 상태를 받는 사용자는 "언제 완료되지?"라며 새로고침을 반복합니다. 음식 배달 앱에서 "지금 어디쯤이지?" 궁금해서 5초마다 앱을 열어보는 상황과 같습니다. 앱이 알아서 알려주면 좋겠지만, 그런 기능이 아직 없으니 직접 확인하는 수밖에 없습니다. 이것을 **폴링(Polling)** 이라고 합니다.

:::term-box
**폴링(Polling)이란?** 클라이언트가 서버에 주기적으로 "변경된 거 있어?" 하고 반복 요청하여 상태를 확인하는 방식입니다. 서버가 먼저 알려주지 않으므로, 변화가 없어도 계속 요청이 발생합니다.
:::

**두 번째**: delivery-service에서 배달이 생성되면 자동으로 완료 처리됩니다. 실제 서비스라면 배달 기사가 물건을 전달한 시점에 완료가 되어야 합니다.

이번 챕터에서는 이 두 숙제를 동시에 해결합니다. 배달 기사가 API를 호출하면 그 시점에 배달이 완료됩니다. 동시에 WebSocket으로 사용자에게 즉시 알림을 보냅니다. 이것이 완성된 주문 처리 시스템의 마지막 퍼즐입니다.


## 5.2 WebSocket - 폴링의 한계를 넘다

### 5.2.1 왜 폴링이 문제인가?

<!-- image-prompt: Minimal black line drawing on white background, split comparison, 4:3 aspect ratio, 800x600px. Left side labeled "Polling": a person repeatedly opening their front door every few minutes to check if a package has arrived, empty doorstep, a clock showing repeated checks. Right side labeled "WebSocket": the same person sitting comfortably on a sofa, a doorbell rings to notify that the package has arrived. Clean lines, no colors. -->
![](assets/CH05/gemini/01_polling-vs-websocket.png)
*그림 5-1. 폴링 vs WebSocket*


주문 완료 여부를 확인하는 방법은 크게 두 가지입니다.

**폴링(Polling)** 방식은 택배를 기다리며 현관문을 5분마다 직접 여는 것과 같습니다. 클라이언트가 서버에 반복적으로 "완료됐나요?"를 물어봅니다.

**WebSocket** 방식은 초인종을 다는 것과 같습니다. 택배가 도착하면 초인종이 울려 알려주듯, 서버가 먼저 클라이언트에게 Push합니다.

:::note
**WebSocket 위에 STOMP 프로토콜을 사용합니다.** STOMP를 얹으면 "이 채널을 구독한다", "이 채널에 메시지를 보낸다" 같은 발행-구독 구조를 쓸 수 있습니다. 클라이언트가 `/topic/orders/{userId}` 채널을 구독하면 해당 사용자에게만 알림이 전달됩니다.
:::


**오픈이**: "근데 지금은 배달이 생성되자마자 완료되잖아요. 배달 기사가 진짜 전달한 다음에 완료 처리해야 하지 않나요?"

**선배**: "맞아요. 배달 상태를 PENDING으로 바꾸고, 기사가 완료 API를 호출해야 COMPLETED가 되게 고쳐 봐요."

## 5.3 배달 완료 라이프사이클 설계

구현 전, 챕터 4와 챕터 5에서 배달 상태 전이가 어떻게 달라지는지 먼저 비교합니다.

챕터 4는 배달이 생성되는 즉시 완료 처리됩니다. 현실에서는 배달 기사가 물건을 전달해야 완료인데, 이 단계가 빠져 있습니다.

**챕터 4 (이전)**

<div class="svg-figure">
<svg viewBox="0 0 1000 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="챕터 4의 배달 흐름: 생성 요청이 들어오자마자 COMPLETED 상태로 자동 전이">
  <defs>
    <marker id="c5f2-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="500" y="34" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">챕터 4의 배달 흐름</text>
  <rect x="180" y="90" width="240" height="100" rx="14" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="300" y="124" text-anchor="middle" font-size="12" font-weight="700" fill="#475569">STATE</text>
  <text x="300" y="152" text-anchor="middle" font-size="20" font-weight="700" fill="#0f172a">생성</text>
  <text x="300" y="176" text-anchor="middle" font-size="12" fill="#475569">배달 생성 요청</text>
  <line x1="420" y1="140" x2="578" y2="140" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c5f2-i)"/>
  <text x="499" y="128" text-anchor="middle" font-size="12" font-weight="600" fill="#4f46e5">자동 전이</text>
  <rect x="580" y="90" width="240" height="100" rx="14" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="700" y="124" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">FINAL</text>
  <text x="700" y="152" text-anchor="middle" font-size="20" font-weight="700" fill="#7b341e" font-family="JetBrains Mono, monospace">COMPLETED</text>
  <text x="700" y="176" text-anchor="middle" font-size="12" fill="#9a3412">즉시 완료 처리</text>
</svg>
</div>
*그림 5-2. 챕터 4의 배달 흐름 - 생성 즉시 완료 처리*


챕터 5에서는 실제 택배처럼 접수하면 "배달 중(PENDING)"이 되고, 배달 기사가 수령인에게 전달한 뒤 "배달 완료(COMPLETED)" 버튼을 눌러야 비로소 완료가 됩니다.

**챕터 5 (변경)**

<div class="svg-figure">
<svg viewBox="0 0 1000 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="챕터 5의 배달 흐름: 생성 → PENDING으로 자동 전이된 뒤 배달 기사가 완료 API를 호출해야 COMPLETED로 바뀜">
  <defs>
    <marker id="c5f3-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="500" y="34" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">챕터 5의 배달 흐름</text>
  <rect x="40" y="100" width="220" height="100" rx="14" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="150" y="134" text-anchor="middle" font-size="12" font-weight="700" fill="#475569">STATE</text>
  <text x="150" y="162" text-anchor="middle" font-size="20" font-weight="700" fill="#0f172a">생성</text>
  <text x="150" y="186" text-anchor="middle" font-size="12" fill="#475569">배달 생성 요청</text>
  <line x1="260" y1="150" x2="378" y2="150" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c5f3-i)"/>
  <text x="319" y="138" text-anchor="middle" font-size="12" font-weight="600" fill="#4f46e5">자동 전이</text>
  <rect x="380" y="100" width="220" height="100" rx="14" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="490" y="134" text-anchor="middle" font-size="12" font-weight="700" fill="#4338ca">STATE</text>
  <text x="490" y="162" text-anchor="middle" font-size="20" font-weight="700" fill="#4338ca" font-family="JetBrains Mono, monospace">PENDING</text>
  <text x="490" y="186" text-anchor="middle" font-size="12" fill="#4338ca">배달 대기 상태</text>
  <line x1="600" y1="150" x2="738" y2="150" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c5f3-i)"/>
  <text x="669" y="135" text-anchor="middle" font-size="11" font-weight="600" fill="#4f46e5">배달 기사</text>
  <text x="669" y="148" text-anchor="middle" font-size="11" font-weight="600" fill="#4f46e5">완료 API 호출</text>
  <rect x="740" y="100" width="220" height="100" rx="14" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="850" y="134" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">FINAL</text>
  <text x="850" y="162" text-anchor="middle" font-size="20" font-weight="700" fill="#7b341e" font-family="JetBrains Mono, monospace">COMPLETED</text>
  <text x="850" y="186" text-anchor="middle" font-size="12" fill="#9a3412">배달 완료</text>
</svg>
</div>
*그림 5-3. 챕터 5의 배달 흐름 - 배달 기사 완료 API 호출 후 COMPLETED*


이제 세 곳을 수정해야 합니다. delivery-service에 배달 완료 API를 추가하고, orchestrator에 배달 완료(`delivery-completed`) 토픽 처리를 추가하고, order-service에 WebSocket Push를 구현합니다.


## 5.4 delivery-service - 배달 완료 API 추가

### 5.4.1 패키지 구조

```text delivery-service/ 패키지 구조
delivery-service/src/main/java/.../
├── domain/
│   └── Delivery.java                        ← [참고] create()는 PENDING 상태. cancel() 메서드는 도입하지 않음
├── usecase/
│   ├── CompleteDeliveryUseCase.java         ← [참고] 배달 완료 인터페이스
│   └── DeliveryService.java                 ← [작성] completeDelivery() 추가
├── web/
│   └── DeliveryController.java              ← [작성] PUT /{id}/complete 추가
└── adapter/
    ├── message/
    │   └── DeliveryCompletedEvent.java      ← [참고] 배달 완료 이벤트 DTO
    └── producer/
        └── DeliveryEventProducer.java       ← [작성] publishDeliveryCompleted() 추가
```

### 5.4.2 Delivery 엔티티 상태 전이

배달 생성 시 상태를 `PENDING`으로 저장하고, 배달 기사가 완료 처리 시 `COMPLETED`로 전이합니다. 이전에는 생성과 동시에 `complete()`를 호출했지만, 이제는 명시적인 API 호출이 있어야 완료됩니다.

```java domain/Delivery.java. 배달 상태 전이 (PENDING → COMPLETED)
@Table(name = "delivery_tb")
public class Delivery {
    // 2장 Delivery.java 참조 — 필드 동일

    // 배달 주소 검증
    public static void validateAddress(String address) {
        if (address == null || address.isBlank()) {
            throw new Exception400("배달 주소는 필수입니다.");
        }
    }

    // 배달 생성 시 PENDING 상태 (배달 완료 API 대기)
    public static Delivery create(int orderId, String address) {
        return new Delivery(orderId, address, DeliveryStatus.PENDING);
    }

    public void complete() {
        this.status = DeliveryStatus.COMPLETED;
        this.updatedAt = LocalDateTime.now();
    }
}
```

이번 챕터에서도 배달 취소 흐름은 다루지 않으므로 `cancel()` 메서드는 도입하지 않습니다. 주문 롤백이 발생하면 `cancel-order-command`로 주문만 취소되고, 이미 만들어진 배달은 PENDING 상태로 남습니다. 배달 라이프사이클은 PENDING → COMPLETED 한 방향만 가집니다.

아래 메서드를 DeliveryService에 추가합니다. 배달 상태를 COMPLETED로 변경하고 Kafka 이벤트를 발행합니다.

`usecase/DeliveryService.java`를 열고 아래 메서드를 추가합니다.

```java [실습 1] usecase/DeliveryService.java. completeDelivery 추가
@Override
@Transactional
public DeliveryResponse completeDelivery(int deliveryId) {  // 추가
    Delivery findDelivery = deliveryRepository.findById(deliveryId)
            .orElseThrow(() -> new Exception404("배달 정보를 조회할 수 없습니다."));
    findDelivery.complete();
    deliveryEventProducer.publishDeliveryCompleted(new DeliveryCompletedEvent(findDelivery.getOrderId()));
    return DeliveryResponse.from(findDelivery);
}
```

### 5.4.3 배달 완료 컨트롤러

아래 엔드포인트를 DeliveryController에 추가합니다. 배달 기사가 호출하는 배달 완료 API입니다.

`web/DeliveryController.java`를 열고 아래 엔드포인트를 추가합니다.

```java [실습 2] web/DeliveryController.java. 배달 완료 엔드포인트
@PutMapping("/{deliveryId}/complete")
public ResponseEntity<?> completeDelivery(@PathVariable("deliveryId") int deliveryId) {  // 추가
    return Resp.ok(completeDeliveryUseCase.completeDelivery(deliveryId));
}
```

### 5.4.4 delivery-completed 이벤트 발행

배달이 완료되면 Kafka 배달 완료(`delivery-completed`) 토픽에 이벤트를 발행합니다. orchestrator가 이 이벤트를 받아 다음 단계를 진행합니다.

아래 메서드를 기존 파일에 추가합니다.

`adapter/producer/DeliveryEventProducer.java`를 열고 아래 메서드를 추가합니다.

```java [실습 3] adapter/producer/DeliveryEventProducer.java. delivery-completed 발행
public void publishDeliveryCompleted(DeliveryCompletedEvent event) {  // 추가
    kafkaTemplate.send("delivery-completed", event);
}
```

## 5.5 orchestrator - delivery-completed 처리 추가

챕터 5에서는 배달 생성(`delivery-created`) 성공 시 바로 완료하지 않고 대기합니다. 이후 배달 완료(`delivery-completed`) 이벤트를 받았을 때 비로소 주문 완료 명령(`complete-order-command`)을 발행합니다.

### 5.5.1 deliveryCreated 수정 - 성공 시 대기

챕터 4에서는 배달 생성 성공 시 즉시 주문 완료 명령(`complete-order-command`)을 발행했지만, 챕터 5에서는 배달 완료를 기다리기 위해 아무것도 발행하지 않습니다.

`handler/OrderOrchestrator.java`의 `deliveryCreated`를 아래처럼 수정합니다.

```java [실습 4] handler/OrderOrchestrator.java. deliveryCreated - 성공 시 대기
@KafkaListener(topics = "delivery-created", groupId = "orchestrator")
public void deliveryCreated(DeliveryCreatedEvent event) {
    int orderId = event.orderId();
    WorkflowState state = states.get(orderId);
    if (state == null) return;

    // 실패: 4장과 동일 (재고 복구 → 주문 취소)

    // 성공: 배달 완료를 기다린다 (complete-order-command 발행하지 않음)
    states.remove(orderId);  // 배달 완료는 별도 리스너에서 처리하므로 워크플로우 상태 정리
}
```

실패 처리는 챕터 4와 동일합니다. 핵심 변경은 성공 시입니다. 챕터 4에서는 여기서 바로 주문 완료 명령(`complete-order-command`)을 발행했지만, 이제는 아무것도 하지 않고 배달기사의 완료 API 호출을 기다립니다.

### 5.5.2 deliveryCompleted 추가 - 배달 완료 시 주문 완료

`handler/OrderOrchestrator.java`에 `deliveryCompleted` 리스너를 추가합니다.

```java [실습 5] handler/OrderOrchestrator.java. deliveryCompleted - 주문 완료 명령 발행
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

배달기사가 `PUT /api/deliveries/{id}/complete`를 호출하면, delivery-service가 배달 완료(`delivery-completed`) 이벤트를 발행합니다. orchestrator가 이를 받아 주문 완료 명령(`complete-order-command`)을 발행하고, order-service가 주문을 완료 처리한 뒤 WebSocket으로 사용자에게 알림을 보냅니다.

### 5.5.3 전체 Kafka 토픽 맵 (최종)

챕터 5에서 배달 완료(`delivery-completed`) 토픽이 추가되어, 최종적으로 9개 토픽을 사용합니다.

| 토픽 | 발행 | 구독 | 목적 |
|---|---|---|---|
| `order-created` | order-service | orchestrator | 새 주문 발생 |
| `decrease-product-command` | orchestrator | product-service | 재고 감소 명령 |
| `product-decreased` | product-service | orchestrator | 재고 감소 결과 |
| `create-delivery-command` | orchestrator | delivery-service | 배달 생성 명령 |
| `delivery-created` | delivery-service | orchestrator | 배달 생성 결과 |
| `delivery-completed` | delivery-service | orchestrator | 배달 완료 이벤트 (챕터 5 신규) |
| `complete-order-command` | orchestrator | order-service | 주문 완료 명령 |
| `cancel-order-command` | orchestrator | order-service | 주문 취소 명령 (롤백) |
| `increase-product-command` | orchestrator | product-service | 재고 복구 명령 (롤백) |


*delivery-service가 완료 이벤트를 보내고, orchestrator가 주문 완료를 지시한다. 이제 남은 건 사용자에게 알려주는 것뿐이다.*

## 5.6 order-service - STOMP로 실시간 Push 구현

마지막 퍼즐입니다. order-service가 주문 완료 명령(`complete-order-command`)을 받아 주문을 완료 처리하고, 동시에 WebSocket으로 사용자에게 알림을 보냅니다.

### 5.6.1 패키지 구조

```text order-service/ 패키지 구조
order-service/
├── build.gradle                           ← [참고] WebSocket 의존성 추가
└── src/main/java/.../
    ├── core/
    │   ├── config/
    │   │   └── WebSocketConfig.java       ← [작성] STOMP WebSocket 설정
    │   └── filter/
    │       └── JwtAuthenticationFilter.java ← [작성] WebSocket 경로 필터 제외
    └── usecase/
        └── OrderService.java              ← [작성] completeOrder에 WebSocket Push 추가
```

### 5.6.2 의존성 추가

 `build.gradle`에 websocket이 추가됩니다.

```gradle order-service/build.gradle. WebSocket 의존성 추가
implementation 'org.springframework.boot:spring-boot-starter-websocket'
```

### 5.6.3 WebSocket 설정

WebSocketConfig는 WebSocket 기능을 활성화하고, 클라이언트가 `/api/ws/orders`로 실시간 연결할 수 있도록 엔드포인트를 등록합니다.
 클라이언트가 이 엔드포인트로 연결한 뒤 `/topic/orders/{userId}` 채널을 구독하면, 서버가 해당 채널로 보낸 메시지를 실시간으로 수신할 수 있습니다.

`core/config/WebSocketConfig.java`를 열고 아래 클래스를 작성합니다.

```java [실습 6] core/config/WebSocketConfig.java. STOMP WebSocket 설정
@Configuration
@EnableWebSocketMessageBroker // STOMP WebSocket 브로커 활성화
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    @Override
    public void configureMessageBroker(MessageBrokerRegistry config) {
        // /topic 접두사로 메시지 라우팅 (Kafka 토픽과는 다른 개념)
        config.enableSimpleBroker("/topic");
    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        // WebSocket 연결 엔드포인트 — withSockJS()는 미지원 브라우저용 폴백
        registry.addEndpoint("/api/ws/orders").setAllowedOriginPatterns("*").withSockJS();
    }
}
```

### 5.6.4 JwtAuthenticationFilter 수정

`/api/ws` 경로를 JWT 필터에서 제외해야 합니다. 제외하지 않으면 WebSocket 연결이 401로 실패합니다.
토큰은 WebSocket 연결 시 쿼리 파라미터(`?token=`)로 별도 전달되므로, 필터에서는 이 경로를 건너뛰어야 합니다.

`core/filter/JwtAuthenticationFilter.java`의 `shouldNotFilter`에 `/api/ws` 경로를 추가합니다.

```java [실습 7] core/filter/JwtAuthenticationFilter.java. WebSocket 경로 필터 제외
@Override
protected boolean shouldNotFilter(HttpServletRequest request) {
    String path = request.getRequestURI();
    return path.equals("/login") ||
           path.startsWith("/h2-console") ||
           path.startsWith("/api/ws");  // 추가: WebSocket 경로 제외
}
```

### 5.6.5 SimpMessagingTemplate - 주문 완료 시 Push 발송

`completeOrder` 메서드에서 `/topic/orders/{userId}` 채널에 메시지를 보내면 userId에 해당하는 사용자만 알림을 수신합니다.

:::term-box
**SimpMessagingTemplate이란?** Spring이 제공하는 메시지 전송 도구입니다. `convertAndSend(destination, payload)` 메서드로 지정한 채널을 구독한 모든 클라이언트에게 메시지를 Push합니다.
:::

아래 메서드를 구현합니다.

`usecase/OrderService.java`의 `completeOrder` 메서드를 아래처럼 수정합니다.

```java [실습 8] usecase/OrderService.java. completeOrder + WebSocket Push
private final SimpMessagingTemplate messagingTemplate;  // 추가: 생성자 주입

@Transactional
public void completeOrder(int orderId) {
    Order findOrder = orderRepository.findById(orderId)
            .orElseThrow(() -> new Exception404("주문을 찾을 수 없습니다."));
    findOrder.complete();
    messagingTemplate.convertAndSend("/topic/orders/" + findOrder.getUserId(), (Object) Map.of("orderId", orderId));  // 추가: WebSocket Push
}
```

서버 측 WebSocket 구현이 완료됐습니다. 이제 이 클라이언트를 Kubernetes에서 서빙하기 위한 프론트엔드 인프라를 구성합니다.

### 5.6.6 프론트엔드 : Nginx와 SockJS 클라이언트

WebSocket 실시간 알림을 테스트하기 위한 프론트엔드 클라이언트를 구성합니다. Nginx로 정적 HTML을 서빙하면서, API 요청은 gateway-service로 프록시합니다.

```text frontend/ + gateway/ 디렉토리
frontend/
├── index.html    # [참고] WebSocket 테스트 HTML
└── nginx.conf    # [참고] 정적 파일 서빙 + WebSocket 프록시

gateway/
└── nginx.conf    # [참고] WebSocket 경로 추가
```

### 5.6.7 index.html - WebSocket 테스트 클라이언트

프론트엔드는 간단한 HTML 페이지로, JWT 토큰을 입력받아 WebSocket 구독을 설정하고 주문 완료 알림을 실시간으로 표시합니다. 핵심인 WebSocket 연결 부분만 보면 다음과 같습니다.

```javascript frontend/index.html. WebSocket 연결 부분
// SockJS로 WebSocket 연결 생성
stomp = Stomp.over(new SockJS('/api/ws/orders?token=' + TOKEN));

// STOMP 연결 후 채널 구독
stomp.connect({}, function () {
    stomp.subscribe('/topic/orders/' + userId, function (msg) {
        const data = JSON.parse(msg.body);
        status.textContent = '주문 완료! (주문번호: ' + data.orderId + ')';
    });
});
```

`SockJS`로 WebSocket 연결을 만들고, `STOMP`로 `/topic/orders/{userId}` 채널을 구독합니다. 서버가 이 채널로 메시지를 보내면 콜백이 실행되어 화면에 주문 완료를 표시합니다.

### 5.6.8 nginx.conf - WebSocket 프록시 설정

Nginx가 중간에 있으면 WebSocket 연결이 일반 HTTP로 처리되어 끊어집니다. `/api/ws/` 경로에 **Upgrade 헤더** 를 설정하여 "이 연결은 WebSocket이니 끊지 말라"고 알려줘야 합니다.

:::term-box
**Nginx WebSocket 프록시(Upgrade 헤더)란?** Nginx가 WebSocket 연결을 프록시할 때 필요한 설정입니다. nginx 설정에 `upgrade 헤더`를 설정하여 HTTP 연결을 WebSocket 프로토콜로 전환(upgrade)하도록 백엔드에 전달합니다.
:::

정적 파일을 제공하면서 `/login`, `/api/` 요청은 gateway-service로 전달합니다. `/api/ws/` 블록이 핵심입니다.

```nginx frontend/nginx.conf. WebSocket 프록시
# /api/ws/ 경로로 들어오는 WebSocket 요청을 gateway로 전달
location /api/ws/ {
    proxy_pass http://gateway;           # gateway-service로 요청 전달
    proxy_http_version 1.1;              # HTTP/1.1 사용 (WebSocket 필수)
    proxy_set_header Upgrade $http_upgrade;   # 클라이언트의 Upgrade 헤더 전달
    proxy_set_header Connection "upgrade";    # 연결을 WebSocket으로 전환
}
```

gateway-service의 nginx 설정도 동일하게 `upgrade 헤더`를 추가합니다.

```nginx gateway/nginx.conf. WebSocket 추가분
# 기존 location 블록들에 추가
location /api/ws/ {
    proxy_pass http://order-service;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

## 5.7 전체 시스템 통합 테스트

모든 구현이 완료됐습니다. 이제 전체 시스템을 실행하고 처음부터 끝까지 한 번에 흐름을 확인합니다.

### 5.7.1 K8s 매니페스트

챕터 4 대비 frontend 서비스가 새로 추가됩니다. `k8s/frontend/` 폴더에 Deployment, Service, Ingress가 정의되어 있습니다.

| 파일 | 역할 |
|------|------|
| `frontend-deploy.yml` | Nginx 기반 프론트엔드 Pod |
| `frontend-service.yml` | 클러스터 내부 접근용 Service |
| `frontend-ingress.yml` | 외부 요청을 frontend-service로 라우팅 |

이번 챕터부터는 Ingress가 gateway-service가 아닌 **frontend-service**를 가리킵니다. 프론트엔드의 Nginx가 정적 파일을 직접 제공하고, `/api/` 요청만 gateway-service로 전달합니다.

### 5.7.2 이미지 빌드

```bash [터미널] 이미지 빌드
minikube image build -t metacoding/db:3 ./db
minikube image build -t metacoding/gateway:3 ./gateway
minikube image build -t metacoding/order:3 ./order
minikube image build -t metacoding/product:3 ./product
minikube image build -t metacoding/user:3 ./user
minikube image build -t metacoding/delivery:3 ./delivery
minikube image build -t metacoding/orchestrator:3 ./orchestrator
minikube image build -t metacoding/frontend:3 ./frontend
```

### 5.7.3 배포

Kafka를 먼저 배포하고 ready 상태를 확인한 다음 나머지를 배포합니다.

```bash [터미널] 배포 순서 (Kafka 우선)
# 1. 네임스페이스 생성 (최초 1회)
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

```bash [터미널] Pod 상태 확인
kubectl get pods -n metacoding
```

<!-- terminal-prompt: Terminal output of "kubectl get pods -n metacoding" command. All pods (db, gateway, order, product, user, delivery, orchestrator, kafka, frontend) showing Running status with 1/1 Ready. -->
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
    <div class="tl-kv-row">frontend-deploy-xxx&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">72s</span></div>
    <div class="tl-divider"><span class="tl-val">9개 Pod Running (frontend 추가)</span><span class="tl-cursor"></span></div>
  </div>
</div>
*그림 5-4. Pod 상태 확인*



### 5.7.4 서비스 접근

Ingress를 통해 외부에서 접속하려면 `minikube tunnel`을 실행합니다.

```bash [터미널] 외부 접근 터널
minikube tunnel
```

터널이 실행되면 `http://127.0.0.1:80`로 프론트엔드에 접속할 수 있습니다.


### 5.7.5 통합 테스트 시나리오

**Step 1: WebSocket 연결 및 주문 생성 (클라이언트 역할)**

브라우저를 통해 index.html에 접속합니다.
```json
브라우저 http://127.0.0.1:80/index.html
```
<!-- terminal-prompt: Browser showing index.html initial page. WebSocket test client with JWT token input field and "주문하기" (Place Order) button. -->
![](assets/CH05/terminal/05_index-html-initial.png)
*그림 5-5. 브라우저에서 index.html 접속 화면*


WebSocket 연결을 위해 토큰을 입력합니다. 로그인 API(`POST /login`)로 발급받은 JWT 토큰에서 `Bearer ` 접두사를 제외한 값만 입력합니다.



토큰을 입력하고 주문하기 버튼을 클릭합니다. index.html이 내부적으로 WebSocket에 연결하고 `/topic/orders/{userId}` 채널을 구독한 뒤 다음과 같은 주문 요청을 보냅니다.

```json
POST /api/orders

{
  "productId": 1,
  "quantity": 1,
  "price": 2500000,
  "address": "Addr 4"
}
```

<!-- terminal-prompt: Browser showing the page after entering JWT token and clicking "주문하기" button. Order accepted and showing PENDING status. -->
![](assets/CH05/terminal/06_token-order.png)
*그림 5-6. 토큰 입력 후 주문하기 버튼 클릭*


브라우저 `F12` - `Console`에서 WebSocket이 연결됨을 확인할 수 있습니다.

<!-- terminal-prompt: Browser DevTools (F12) Console tab showing WebSocket connection success logs. STOMP connected and /topic/orders/{userId} subscription confirmed. -->
![](assets/CH05/terminal/07_websocket-connect.png)
*그림 5-7. 브라우저 Console에서 WebSocket 연결 확인*



Hoppscotch로 생성된 주문을 확인하면 `PENDING` 상태로 머물러 있습니다.
```json
GET http://127.0.0.1:80/api/orders/4
```

<!-- terminal-prompt: Hoppscotch showing GET /api/orders/4 response. JSON body with order status "PENDING". -->
![](assets/CH05/terminal/08_order-pending.png)
*그림 5-8. 주문 조회 결과 - PENDING 상태*




**Step 2: 배달 완료 (배달 기사 역할)**

먼저 생성된 배달을 확인해보겠습니다.

```json
GET http://127.0.0.1:80/api/deliveries/4
```

<!-- terminal-prompt: Hoppscotch showing GET /api/deliveries/4 response. JSON body with delivery status "PENDING". -->
![](assets/CH05/terminal/09_delivery-pending.png)
*그림 5-9. 배달 조회 결과 - PENDING 상태*

배달 ID가 4인 배달이 `PENDING` 상태로 생성되었습니다.

배달 기사가 물건을 전달한 뒤 배달 완료 처리를 합니다.

```json
PUT http://127.0.0.1:80/api/deliveries/4/complete
```
<!-- terminal-prompt: Hoppscotch showing PUT /api/deliveries/4/complete response. JSON body with delivery status changed to "COMPLETED". -->
![](assets/CH05/terminal/10_delivery-completed.png)
*그림 5-10. 배달 완료 API 호출 결과 - COMPLETED 상태*

*배달 완료 버튼을 눌렀다. 이제 주문도 바뀌었을까?*


**Step 3: 주문 완료 및 웹소켓 응답 확인**

배달 완료 처리 후, 주문 완료 명령에 의해 주문이 최종적으로 `COMPLETED` 상태가 됐습니다.
```json
GET http://127.0.0.1:80/api/orders/4
```


<!-- terminal-prompt: Hoppscotch showing GET /api/orders/4 response after delivery completion. JSON body with order status changed to "COMPLETED". -->
![](assets/CH05/terminal/11_order-completed.png)
*그림 5-11. 주문 조회 결과 - COMPLETED 상태*


주문이 완료되면 WebSocket이 클라이언트에게 주문 완료 메시지를 전송합니다.
WebSocket 응답을 수신하면 클라이언트 화면이 주문 완료 상태로 변경됩니다.

<!-- terminal-prompt: Browser index.html page showing real-time WebSocket notification received. Screen displays "주문 완료! (주문번호: 4)" message pushed via WebSocket. -->
![](assets/CH05/terminal/12_websocket-notification.png)
*그림 5-12. WebSocket 알림 수신 - 클라이언트 화면에 주문 완료 표시*



브라우저의 Console 창에서 WebSocket이 응답한 메시지 로그를 확인할 수 있습니다.

<!-- terminal-prompt: Browser DevTools (F12) Console tab showing WebSocket response message logs. JSON message received with orderId field visible in the log. -->
![](assets/CH05/terminal/13_console-log.png)
*그림 5-13. 브라우저 Console에서 WebSocket 응답 메시지 로그 확인*



### 5.7.6 전체 흐름 요약

```text 최종 완성 시스템 전체 흐름
[최종 완성 시스템 전체 흐름]

1. POST /api/orders → order-service (PENDING 저장)
   └─ Kafka: order-created

2. orchestrator: order-created 수신
   └─ Kafka: decrease-product-command

3. product-service: 재고 감소
   └─ Kafka: product-decreased { success: true }

4. orchestrator: 재고 감소 확인
   └─ Kafka: create-delivery-command

5. delivery-service: 배달 생성 (PENDING 상태)
   └─ Kafka: delivery-created { success: true }

6. orchestrator: delivery-created 수신 → 대기

7. PUT /api/deliveries/{id}/complete (배달 기사)
   delivery-service: 배달 COMPLETED
   └─ Kafka: delivery-completed

8. orchestrator: delivery-completed 수신
   └─ Kafka: complete-order-command

9. order-service: 주문 COMPLETED
   └─ WebSocket Push: /topic/orders/{userId}

10. 클라이언트: 실시간 알림 수신 (완료)
```


*직접 주문을 넣어보았습니다. 화면에 "처리 중"이 표시되었고, 배달 완료 신호를 보내자 1초도 안 되어 화면이 저절로 바뀌었습니다. "주문 완료!" 새로고침을 누르지 않았는데도 시스템이 살아 움직이며 저에게 말을 걸어온 것입니다.*

완성된 시스템을 선배에게 보여주었습니다.

**오픈이**: "금요일 밤에 서버가 터졌을 때는 정말 막막했는데, 한 단계씩 부딪히며 오다 보니 결국 해내게 되네요."

**선배**: "처음부터 모든 정답을 알고 시작하는 사람은 없어요. 부딪히고, 고치고, 다시 만드는 것. 그게 개발자에게는 가장 빠른 길이에요."

:::remember
**이것만은 기억하자**

- **배달 완료 라이프사이클**: 배달 생성 시 `PENDING`, 배달 기사 API 호출 시 `COMPLETED`로 실제 배달 완료 시점을 정확히 반영합니다.
- **delivery-completed 토픽 추가**: delivery-service가 완료 이벤트를 발행하고 orchestrator가 처리합니다. 이로써 챕터 5에서 실제 사용하는 Kafka 토픽은 9개가 됩니다.
- **orchestrator 변경**: 배달 생성(`delivery-created`) 성공 후 대기, 배달 완료(`delivery-completed`) 수신 후 주문 완료 처리. 실패 시에는 재고를 복구합니다.
- **WebSocket Push**: order-service가 `SimpMessagingTemplate`으로 사용자별 채널에 실시간 알림을 보냅니다.
:::

챕터 1에서 하나의 모놀리식 서비스로 시작했습니다. 챕터 2에서 서비스를 나눴고, 챕터 3에서 클린 아키텍처와 Kubernetes로 운영 환경을 갖췄습니다. 챕터 4에서 Kafka로 비동기 통신과 실패 대응을 완성했고, 이 챕터에서 사용자에게 결과를 즉시 전달하는 마지막 퍼즐을 완성했습니다. 동기에서 비동기로, 하나에서 여럿으로. 코드를 한 줄씩 바꾸다 보면 MSA의 구조가 보입니다.