# 챕터 4. 비동기 MSA — Kafka로 서비스를 분리하다

> `ex03` · 실행 환경: 컨테이너 · Kafka · Orchestration Saga · orchestrator 신규
> 이 챕터의 전체 소스코드는 **https://github.com/metacoding-12-msa/ex03** 에서 확인할 수 있습니다.


> 이번 챕터는 책에서 가장 복잡한 내용을 다룹니다. 여러 서비스가 동시에 Kafka 메시지를 주고받으며 상태가 바뀝니다. 전체 토픽맵(4.2.3)과 흐름 표(4.3.1~4.3.2)를 먼저 훑어보고 시작하면 길을 잃지 않습니다.

### 학습 목표

- 동기 REST 호출의 한계를 이해하고 비동기 메시지 방식의 장점을 설명한다.
- Kafka의 토픽, 프로듀서, 컨슈머, 컨슈머 그룹 개념을 이해한다.
- Orchestration Saga 패턴을 Kafka로 구현한다.
- order-service의 동기 호출을 Kafka 이벤트 발행으로 교체한다.
- orchestrator가 워크플로우 상태를 추적하고 실패 시 자동 롤백하는 방법을 이해한다.


**오픈이**: "선배님, 상품 서비스 껐다 켰더니 주문까지 멈춰요. 서비스 분리한 의미가 없는 것 같아요."

**선배**: "서로 직접 전화를 걸어서 기다려주니까 그렇지. 이제 전화를 끊고 메시지를 남기는 방식으로 바꿔봐. Kafka라는 녀석이 있어."

## 4.1 한 서비스의 장애가 전체를 멈추다

챕터 3을 마치면서 이런 질문을 남겼습니다. **"product-service가 잠깐 다운되면 어떻게 되나?"**

답은 단순합니다. order-service도 주문을 처리할 수 없게 됩니다. order-service가 product-service를 직접 HTTP로 호출하기 때문입니다. 하나가 느려지면 다른 하나도 기다립니다. 하나가 멈추면 다른 하나도 멈춥니다.

생각해 보면 이것은 MSA의 목표, 즉 **"각 서비스를 독립적으로 배포하고 장애를 격리한다"** 에 정면으로 위배됩니다.

### 4.1.1 카운터 대기 vs 진동벨

카페에서 커피를 주문하는 두 가지 방식으로 비교하겠습니다.

<!-- image-prompt: Minimal black line drawing on white background, split comparison, 4:3 aspect ratio, 800x600px. Minimal text — let the drawing tell the story. Separated by a simple vertical line in the middle, no X mark. Left side, title "동기 (카운터 대기)": barista behind counter making coffee, one customer standing at counter waiting, four or five more customers queued behind in a long line looking bored. All frozen/blocked. Right side, title "비동기 (진동벨)": same cafe counter with barista, but the customer has walked away to a table, sitting with a laptop and a small vibration buzzer on the table. A wavy line from the buzzer indicating it will ring. No speech bubbles, no annotation text, no checklists. Clean lines, no colors. -->
![동기비동기](images/chap04-1-1.png)
*그림 4-1: 동기 vs 비동기 통신*


**카운터 대기 방식 (동기적)**

카운터 앞에 서서 "아메리카노 하나요"라고 주문합니다. 바리스타가 커피를 만드는 동안 카운터 앞에서 기다립니다. 내 커피가 나와야 다음 손님이 주문할 수 있습니다. 바리스타가 원두를 갈다가 머신이 고장 나면? 뒤에 줄 선 손님 전부가 멈춥니다.


**진동벨 방식 (비동기적)**

"아메리카노 하나요"라고 주문하면 진동벨을 받고 자리에 앉습니다. 바리스타는 주문을 순서대로 처리하고, 커피가 완성되면 벨이 울립니다. 나는 기다리는 동안 다른 일을 할 수 있고, 뒤에 줄 선 손님도 바로 주문할 수 있습니다. 머신이 잠깐 멈춰도 주문 목록은 사라지지 않습니다.


MSA에서 동기 통신의 문제는 더 심각합니다. 하나가 느려지면 전체가 느려지는 연쇄 장애가 발생합니다.



## 4.2 Kafka : 메시지를 전달하는 우체국
> **Apache Kafka**: 서비스 사이에 메시지를 안전하게 저장하고 전달하는 분산 메시지 플랫폼입니다. 발행자와 구독자가 동시에 실행 중이지 않아도 메시지가 유실되지 않습니다.

Kafka를 코드로 보기 전, 꼭 알아야 할 세 가지 개념이 있습니다.

### 4.2.1 토픽, 프로듀서, 컨슈머

Kafka의 구조는 우체통과 비슷합니다. 메시지를 보내는 사람이 **프로듀서**, 메시지를 받는 사람이 **컨슈머**, 메시지가 쌓이는 공간이 **토픽**입니다.

> **토픽(Topic)**: 메시지가 저장되는 이름 붙은 채널입니다. 우체통의 투입구처럼 특정 주제의 메시지를 모아두는 공간입니다.

> **프로듀서(Producer)**: 토픽에 메시지를 보내는(발행하는) 쪽입니다. 우체통에 편지를 넣는 사람에 해당합니다.

> **컨슈머(Consumer)**: 토픽에서 메시지를 읽는(구독하는) 쪽입니다. 우체통에서 편지를 꺼내 읽는 사람에 해당합니다.

<!-- image-prompt: Minimal black line drawing on white background, horizontal flow diagram, 4:3 aspect ratio, 800x400px. Left: a box labeled "프로듀서 (order-service)". Arrow pointing right into center area: a large rounded rectangle labeled "Kafka 브로커" at top. Inside it, a smaller rectangle labeled "[토픽: order-created]" containing a horizontal row of small square cells like a conveyor belt — cells labeled "msg1", "msg2", "msg3", "...", "..." showing messages queued inside the topic. Right: an arrow from the topic pointing right to a box labeled "컨슈머 (orchestrator)". Clean lines, no colors. -->
![메시지 큐](images/chap04-1-2.png)
*그림 4-2: 메시지 큐 개념*

Kafka의 중요한 특성은, 컨슈머가 메시지를 읽어도 토픽에서 **삭제되지 않는다**는 점입니다. 보존 기간(기본 7일)이 지나야 삭제됩니다. 컨슈머는 오프셋(자신이 어디까지 읽었는지 기록한 위치)을 기억하기 때문에 재시작 후에도 읽지 않은 메시지부터 이어서 처리할 수 있습니다.

> **RabbitMQ** 같은 전통적인 메시지 큐는 컨슈머가 메시지를 읽으면 큐에서 바로 삭제됩니다. 반면 **Kafka** 는 읽어도 메시지가 남아 있습니다. 덕분에 여러 컨슈머가 같은 메시지를 각자의 속도로 읽을 수 있고, 장애 후 재처리도 가능합니다.

### 4.2.2 컨슈머 그룹

product-service를 2대로 늘려서 운영한다고 가정해 봅시다. **"재고 1개 차감"** 메시지가 들어왔는데 두 인스턴스가 모두 처리하면 재고가 2개 줄어듭니다. 이런 중복 처리를 방지하기 위해 **컨슈머 그룹**으로 묶습니다. 같은 그룹 안에서는 하나의 메시지가 **한 인스턴스에만** 전달됩니다.


<!-- image-prompt: Minimal black line drawing on white background, diagram, 4:3 aspect ratio, 800x400px. Left: a label "메시지" with a thick arrow pointing right into a rounded rectangle group labeled "컨슈머 그룹 (product-group)" at the top. Inside the group, two rows stacked vertically: top row "인스턴스 A ← 메시지 전달 ✓ (처리 담당)", bottom row "인스턴스 B ← 전달 안 됨 ✗". The arrow from left connects only to 인스턴스 A. Clean lines, no colors. -->
![컨슈머 그룹](images/chap04-2-1.png)
*그림 4-3: 컨슈머 그룹*


### 4.2.3 이번 챕터에서 사용하는 토픽 맵

이번 챕터에서 사용하는 Kafka 토픽 전체를 먼저 봅니다. 처음에는 낯설어 보이지만, 구현 과정에서 하나씩 다루게 됩니다.

총 8개의 토픽을 사용합니다. `command`가 붙은 토픽은 orchestrator가 각 서비스에 내리는 명령입니다. `command`가 없는 토픽은 각 서비스가 처리 결과를 orchestrator에 보고하는 이벤트입니다.

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

> 이번 챕터에서 배달은 한 번 만들어지면 취소되지 않습니다. 주문이 롤백되어도 배달 자체는 그대로 PENDING으로 남고, 배달 라이프사이클의 의미는 챕터 5에서 정식으로 다루겠습니다.

**오픈이**: "메시지 방식으로 바꾸니까, 전체 흐름을 누가 관리해야 할지 모르겠어요."

**선배**: "오케스트레이터를 만드는 거야. 지휘자가 전체 악보를 보고 순서를 정하는 것처럼, 각 서비스는 자기 일만 하고 결과만 보고하게 해."

## 4.3 Orchestration Saga : 지휘자가 흐름을 조율하다

Saga를 구현하는 방식은 크게 두 가지입니다. 각 서비스가 이벤트를 보고 스스로 다음 서비스를 호출하는 Choreography, 중앙 지휘자가 순서를 정하는 Orchestration입니다. 이 책에서는 워크플로우 상태를 한 곳에서 추적하고 실패 시 정확한 롤백이 가능한 Orchestration을 선택합니다. **지휘자(orchestrator)** 가 전체 흐름을 중앙에서 관리합니다. 각 서비스는 명령을 받아 처리하고 결과를 보고할 뿐, 다음 단계가 무엇인지 알 필요가 없습니다. 지휘자만 전체 악보를 알고 있습니다.
<!-- image-prompt: Clean black line drawing on white background, simplified orchestra illustration, 4:3 aspect ratio, 800x600px. No stage, no curtains, no background. Center: a conductor on a small podium holding a baton and a score labeled "SAGA", drawn in a clean cartoon style (not stick figures — simple but with body proportions, hair, clothing outlines). Three musicians sitting around the conductor with recognizable instruments and music stands labeled "ORDER", "PRODUCT", "DELIVERY". Blue curved arrows from conductor to each musician labeled "command". Green curved arrows from each musician back labeled "result". Simple cartoon style like a textbook illustration — more detailed than stick figures but less detailed than realistic. No shading, no colors except blue and green arrows. -->
![Orchestration Saga 구조](images/chap04-orchestra.png)
*그림 4-4: Orchestration Saga 구조*



### 4.3.1 주문 요청 성공 흐름

주문이 정상적으로 처리되는 흐름입니다. 클라이언트가 주문을 요청하면, orchestrator가 재고 감소 → 배달 생성 → 주문 완료 순서로 각 서비스에 명령을 보냅니다. 모든 단계가 성공하면 주문 상태가 COMPLETED로 바뀝니다.

![주문 성공 흐름](images/fig-4-5.png)
*그림 4-5: 주문 성공 흐름 (Orchestration Saga)*

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

![주문 실패 시 롤백 흐름](images/fig-4-6.png)
*그림 4-6: 주문 실패 시 롤백 흐름*

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

**선배**: "설계는 끝났어. 이제 직접 짜봐. order-service부터 REST 호출을 걷어내고 Kafka 이벤트로 바꿔."

## 4.4 order-service : 동기 호출 제거, 이벤트 발행

챕터 2·3에서 order-service는 product-service와 delivery-service를 직접 REST로 호출했습니다. 이번 챕터에서는 이 호출을 모두 제거하고 Kafka 이벤트 발행으로 교체합니다.

### 4.4.1 패키지 구조

```
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

> REST로 주문을 취소하는 엔드포인트는 사라집니다. 주문 취소는 orchestrator가 발행한 `cancel-order-command`를 OrderCommandConsumer가 받아 처리합니다.

### 4.4.2 의존성 추가

`spring-boot-starter-kafka` 한 줄을 추가합니다. JSON 직렬화에 필요한 `jackson-databind`는 spring-boot-starter-kafka가 transitive로 끌고 오므로 따로 명시하지 않습니다.

**[참고]** 챕터 3 `build.gradle`에 다음 한 줄을 추가합니다.

```gradle
implementation 'org.springframework.boot:spring-boot-starter-kafka'
```

### 4.4.3 Kafka 설정

`application-dev.properties`와 `application-prod.properties` 모두에 Kafka 설정을 추가합니다. Kafka 주소는 환경변수로 주입받습니다.
> `group-id`는 컨슈머 그룹 이름으로, 같은 그룹끼리는 메시지를 나눠 받고, 다른 그룹이면 같은 메시지를 각각 받습니다.

**[참고]** `application-prod.properties`

```properties
# ===== Kafka =====
spring.kafka.bootstrap-servers=${SPRING_KAFKA_BOOTSTRAP_SERVERS:localhost:9092}
spring.kafka.consumer.group-id=order-service                    # 이 서비스의 컨슈머 그룹 이름
# 생략 ...
```

dev와 prod의 Kafka 설정은 동일합니다. `bootstrap-servers`의 기본값이 `localhost:9092`이므로 로컬에서는 그대로, K8s에서는 환경변수로 Kafka 주소를 주입합니다.

### 4.4.4 KafkaConfig : JSON 메시지 변환

`JacksonJsonMessageConverter` 빈을 등록합니다. 이 설정은 모든 Kafka 사용 서비스(order, product, delivery, orchestrator)에 동일하게 추가합니다.

**[참고]** `core/config/KafkaConfig.java`

```java
@Configuration
public class KafkaConfig {

    @Bean
    public RecordMessageConverter recordMessageConverter() {
        return new JacksonJsonMessageConverter();
    }
}
```

### 4.4.5 이벤트 DTO

Kafka 메시지로 전송할 데이터를 DTO로 정의합니다. 주문 1건에 상품 1건이라는 챕터 02의 단순화 가정을 그대로 가져가므로, 이벤트도 record 한 줄짜리 단순한 형태입니다.

**[참고]** `adapter/message/OrderCreatedEvent.java`

```java
public record OrderCreatedEvent(
        int orderId,
        int userId,
        int productId,
        int quantity,
        Long price,
        String address
) {}
```

### 4.4.6 KafkaTemplate : 메시지 발행

이벤트를 Kafka 토픽으로 발행하는 프로듀서입니다. `KafkaTemplate`이 직렬화와 전송을 처리합니다.


다음 코드를 추가하세요.

**[작성]** `adapter/producer/OrderEventProducer.java`

```java
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

이전 챕터와 비교하여 가장 크게 달라지는 부분은 동기 호출 대신 Kafka 이벤트를 발행하고 즉시 PENDING 상태로 반환한다는 점입니다.
아래 createOrder 메서드를 구현합니다.

**[작성]** `usecase/OrderService.java`

```java
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

**[작성]** `adapter/consumer/OrderCommandConsumer.java` - 다음 코드를 추가하세요.

```java
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


## 4.5 product-service · delivery-service : Kafka Consumer/Producer 추가

product-service는 재고 감소·복구 명령을 Kafka로만 받고, 결과를 Kafka로 발행합니다. 챕터 03까지 있던 PUT 엔드포인트(`/api/products/{id}/decrease`, `/increase`)는 제거되고, 컨트롤러에는 GET 조회 엔드포인트만 남습니다. delivery-service도 마찬가지로 배달 생성은 Kafka로만 받고, 컨트롤러에는 GET 엔드포인트만 남습니다.

### 4.5.1 패키지 구조

```
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

> 전체 코드는 GitHub에서 확인하세요.


## 4.6 orchestrator : 워크플로우 조율 서비스 구현 (핵심)

orchestrator는 이번 챕터에서 **새로 추가되는 서비스**입니다. REST API는 없고, Kafka 이벤트만 처리합니다. order, product, delivery 서비스의 Kafka 흐름을 중앙에서 조율하는 지휘자입니다.


### 4.6.1 패키지 구조

```
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

Kafka 메시지를 주고받기 위해 `spring-boot-starter-kafka`를 추가합니다. JSON 직렬화 라이브러리(`jackson-databind`)는 spring-boot-starter-kafka가 transitive 의존성으로 끌고 오므로 따로 명시하지 않습니다.

**[참고]** `build.gradle`

```gradle
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter'
    implementation 'org.springframework.boot:spring-boot-starter-kafka'
}
```

### 4.6.3 OrderOrchestrator

OrderOrchestrator는 세 단계로 동작합니다.

1. **orderCreated** --- 주문 생성 이벤트를 받아 재고 감소 명령을 발행합니다.
2. **productDecreased** --- 재고 감소 결과를 받아, 성공이면 배달 생성 명령을, 실패면 주문 취소 명령을 발행합니다.
3. **deliveryCreated** --- 배달 생성 결과를 받아, 성공이면 주문 완료 명령을, 실패면 재고 복구 + 주문 취소 명령을 발행합니다.

각 단계를 하나씩 살펴보겠습니다.

**[작성]** `handler/OrderOrchestrator.java`  ㅡ OrderOrchestrator 클래스

```java
@Component
@RequiredArgsConstructor
public class OrderOrchestrator {
    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final Map<Integer, WorkflowState> states = new ConcurrentHashMap<>();  // Kafka 리스너가 멀티스레드로 동작하므로 동시성 보장 필요

    // 아래 1~3단계 메서드와 WorkflowState 내부 클래스를 추가
}
```

#### 1단계: 주문 생성 이벤트 수신 (orderCreated)

![1단계: 주문 생성 이벤트 수신](images/fig-4-7.png)
*그림 4-7: 1단계: 주문 생성 이벤트 수신*

**[작성]** `handler/OrderOrchestrator.java`

```java
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

orchestrator가 주문 생성(`order-created`) 이벤트를 받으면, 주문 ID별로 `WorkflowState`를 생성합니다. `WorkflowState`는 메모리(`ConcurrentHashMap`)에 저장되므로 orchestrator Pod가 재시작되면 진행 중인 워크플로우는 소멸합니다. 실무에서는 DB나 Redis에 상태를 저장하는 방식을 사용합니다. 그리고 재고 감소 명령(`decrease-product-command`)을 발행합니다.

#### 2단계: 재고 차감 결과 수신 (productDecreased)

![2단계: 재고 차감 결과 수신](images/fig-4-8.png)
*그림 4-8: 2단계: 재고 차감 결과 수신*

**[작성]** `handler/OrderOrchestrator.java`

```java
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

#### 3단계: 배달 생성 결과 수신 (deliveryCreated)

![3단계: 배달 생성 결과 수신](images/fig-4-9.png)
*그림 4-9: 3단계: 배달 생성 결과 수신*

**[작성]** `handler/OrderOrchestrator.java`

```java
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

### 4.6.4 WorkflowState : 주문별 진행 상태 추적

orchestrator는 진행 중인 주문의 상태를 **메모리**에 보관합니다. 배달 생성 실패 시 차감된 재고를 다시 늘리려면, 어떤 상품을 얼마에 얼마큼 차감했는지를 알고 있어야 하기 때문입니다.

> **WorkflowState**: orchestrator가 주문 한 건의 진행 상태를 추적하기 위해 사용하는 내부 객체입니다. 주문 ID, 배달 주소, 그리고 차감 대상 상품 정보(productId, quantity, price)를 보관합니다.

**[작성]** `handler/OrderOrchestrator.java` 내부 클래스

```java
@Data
private static class WorkflowState {
    private final int orderId;
    private final String address;
    private final int productId;
    private final int quantity;
    private final Long price;
}
```

단일 상품 가정 덕분에 상태도 단순해집니다. "어떤 상품이 처리 완료됐는지" 같은 추적 자료구조 없이, 차감한 정보 그대로를 들고 있다가 롤백 시점에 그대로 IncreaseProductCommand로 돌려보내면 됩니다.

모든 서비스의 Kafka 연동 코드가 완성됐습니다. 이제 Kubernetes에 Kafka와 orchestrator를 추가하고 전체 시스템을 배포합니다.

## 4.7 Kubernetes : Kafka와 orchestrator 배포

챕터 3과 비교하여 이번 챕터에서 K8s에 새로 추가되는 것은 **Kafka**와 **orchestrator** 두 가지입니다. 기존 서비스의 ConfigMap에도 Kafka 주소를 추가해야 합니다.

### 4.7.1 Kafka

기존 Kafka는 ZooKeeper라는 별도 서비스가 필요했지만, **KRaft(Kafka Raft)** 모드를 사용하면 ZooKeeper 없이 Kafka 자체적으로 메타데이터를 관리합니다. `confluentinc/cp-kafka:7.5.0` 이미지를 사용합니다.

| K8s 리소스 | 파일 | 역할 | 비고 |
|---|---|---|---|
| Deployment | `kafka-deploy.yml` | KRaft 모드 Kafka 브로커 실행 (단일 노드) | `KAFKA_PROCESS_ROLES: broker,controller` |
| Service | `kafka-service.yml` | 브로커(9092) 포트 노출 | Spring Boot는 `kafka-service:9092`로 접근 |

Kafka 서버 1대에만 메시지를 저장하면, 그 서버가 죽었을 때 메시지가 전부 사라집니다. 그래서 실무에서는 Kafka 서버를 여러 대 띄우고 하나의 클러스터로 묶습니다. 같은 메시지를 여러 Kafka 서버에 복제해두면, 서버 1대가 죽어도 다른 서버에 데이터가 남아있습니다. 이번 챕터에서는 학습 편의를 위해 **단일 브로커**로 띄우지만 설정 구조는 멀티 브로커로 확장 가능합니다.

**KAFKA_NODE_ID**는 각 Kafka 서버를 식별하는 고유 번호입니다. Kafka 서버가 3대면 각각 1, 2, 3처럼 겹치지 않는 번호를 부여합니다. **CLUSTER_ID**는 이 Kafka 서버들을 하나의 클러스터로 묶는 식별자입니다. 같은 CLUSTER_ID를 가진 Kafka 서버끼리 메시지를 공유하고 복제합니다. 이때 서로를 찾는 주소는 **KAFKA_CONTROLLER_QUORUM_VOTERS**에 지정합니다. 우리 실습에서는 Kafka 서버가 1대이므로 자기 자신을 가리키는 `localhost:9093`만 설정하면 됩니다.

![Kafka 클러스터 식별](images/fig-4-kafka-2.png)
*그림 4-10: CLUSTER_ID로 Kafka 브로커들을 하나의 클러스터로 묶는다. 단일 브로커 실습에서는 컨트롤러가 자기 자신(localhost:9093)과만 통신한다*

**KAFKA_ADVERTISED_LISTENERS**는 클라이언트가 Kafka에 접근할 때 사용하는 주소입니다. 각 서비스의 ConfigMap에 설정하는 `KAFKA_BOOTSTRAP_SERVERS: kafka-service:9092`가 이 주소를 가리킵니다.

![Kafka 접속 주소](images/fig-4-kafka-3.png)
*그림 4-11: 클라이언트는 KAFKA_ADVERTISED_LISTENERS에 지정된 kafka-service:9092로 Kafka에 접근한다*

Kafka를 KRaft 모드로 실행하는 Deployment입니다. 각 옵션의 역할은 주석을 참고합니다.

**[참고]** `kafka-deploy.yml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kafka-deploy
  namespace: metacoding
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kafka
  template:
    metadata:
      labels:
        app: kafka
    spec:
      containers:
        - name: kafka
          image: confluentinc/cp-kafka:7.5.0
          ports:
            - containerPort: 9092  # 클라이언트 통신용 (외부에 노출)
          env:
            # 1. 클러스터 및 노드 식별
            - name: CLUSTER_ID                       # 같은 값을 가진 Kafka 서버끼리 클러스터로 묶인다
              value: "AbijZYk0QOm5p852kOMSIg"        # 클러스터 고유 UUID
            - name: KAFKA_NODE_ID                    # 이 Kafka 서버의 고유 번호 (겹치면 안 됨)
              value: "1"                             # 첫 번째 서버이므로 1
            # 2. 역할 지정
            - name: KAFKA_PROCESS_ROLES              # 이 Kafka 서버가 맡는 역할을 지정
              value: "broker,controller"             # broker: 메시지 저장/전달, controller: 토픽 목록 등 내부 정보 관리
            # 3. 포트 정의 및 역할별 포트 지정
            - name: KAFKA_LISTENERS                  # Kafka가 수신할 포트를 정의
              value: "PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093" # PLAINTEXT 9092는 외부, CONTROLLER 9093은 내부용
            - name: KAFKA_INTER_BROKER_LISTENER_NAME # Kafka끼리 메시지를 복제할 때 사용할 포트 지정 (9092)
              value: "PLAINTEXT"                     # KAFKA_LISTENERS에서 정의한 프로토콜
            - name: KAFKA_CONTROLLER_LISTENER_NAMES  # Kafka끼리 토픽 목록 등을 동기화할 때 사용할 포트 지정 (9093)
              value: "CONTROLLER"                    # KAFKA_LISTENERS에서 정의한 리스너 이름 (내부 관리용 9093)
            # 4. 외부 접근 및 서버 간 통신 주소
            - name: KAFKA_ADVERTISED_LISTENERS       # 클라이언트가 Kafka에 접근할 주소를 지정
              value: "PLAINTEXT://kafka-service:9092" # ConfigMap의 KAFKA_BOOTSTRAP_SERVERS와 일치
            - name: KAFKA_CONTROLLER_QUORUM_VOTERS   # 컨트롤러 정족수(quorum)를 이루는 노드 주소록
              value: "1@localhost:9093"              # 단일 브로커이므로 자기 자신만 등록
            # 5. 싱글 브로커 환경 설정(replicas: 1일 때)
            - name: KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR   # 메시지를 몇 대의 서버에 복제할지 설정
              value: "1"                                     # 서버가 1대이므로 1 (기본값은 3)
```

Kafka Pod에 접근할 수 있도록 K8s Service를 정의합니다. 컨트롤러용 9093 포트는 컨테이너 안에서만 쓰이므로 Service에는 클라이언트용 9092만 노출합니다.

**[참고]** `kafka-service.yml`

```yaml
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

> 전체 코드는 GitHub에서 확인하세요.

### 4.7.3 기존 서비스 ConfigMap 수정

기존 서비스(order, product, delivery)의 ConfigMap에 Kafka 접속 주소를 추가합니다. 주문 서비스의 예시입니다.

**[참고]** `order-configmap.yml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: order-configmap
  namespace: metacoding
data:
  DB_URL: jdbc:mysql://db-service:3306/metadb?useSSL=false&serverTimezone=UTC&useLegacyDatetimeCode=false&allowPublicKeyRetrieval=true
  DB_DRIVER: com.mysql.cj.jdbc.Driver
  SPRING_KAFKA_BOOTSTRAP_SERVERS: kafka-service:9092  # Kafka 접속 주소 추가
```

> 전체 코드는 GitHub에서 확인하세요.

## 4.8 실행 및 결과 확인

### 4.8.1 이미지 빌드

Minikube 내부에 이미지를 빌드합니다. 챕터 3 대비 orchestrator 서비스가 새로 추가됩니다.

```bash
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

```bash
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
![minikube](images/chap04-1.png)
*그림 4-12: Kafka 및 서비스 배포 실행*




모든 Pod가 Running 상태인지 확인합니다.

```bash
kubectl get pods -n metacoding
```
<!-- terminal-prompt: Terminal output of "kubectl get pods -n metacoding" command. All pods (db, gateway, order, product, user, delivery, kafka, orchestrator) showing Running status with 1/1 Ready. -->
![minikube](images/chap04-2.png)
*그림 4-13: Pod 상태 확인 (kubectl get pods)*


### 4.8.3 서비스 접근

Ingress를 통해 외부에서 접속하려면 `minikube tunnel`을 실행합니다.

```bash
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
![minikube](images/chap04-4.png)
*그림 4-14: 주문 생성 응답 (PENDING 상태)*


챕터 3과 다르게 즉시 `PENDING` 상태로 반환됩니다. Kafka 이벤트가 처리되면 상태가 `COMPLETED`로 변경됩니다. 잠시 후 주문 상태를 다시 조회합니다.

```json
GET http://127.0.0.1:80/api/orders/4
```
<!-- terminal-prompt: HTTP client showing GET /api/orders/4 response. JSON body with order status changed to "COMPLETED". -->
![minikube](images/chap04-5.png)
*그림 4-15: 주문 완료 확인 (COMPLETED 상태)*

**오픈이**: "PENDING이었다가 COMPLETED로 바뀌었어요! 그런데 롤백도 자동으로 되나요?"

**선배**: "품절 상품으로 주문해봐. orchestrator 로그를 보면 보일 거야."

### 4.8.5 롤백 확인 : 품절 상품 주문

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
![minikube](images/chap04-6.png)
*그림 4-16: 품절 상품 주문 요청*

잠시 후 상태를 확인하면 `CANCELLED`가 됩니다.

```JSON
GET http://127.0.0.1:80/api/orders/5
```


orchestrator 로그에서 롤백 과정을 확인할 수 있습니다.

<!-- terminal-prompt: Terminal output of "kubectl logs" for orchestrator pod. Log messages showing: product-decreased failure received, increase-product-command published, cancel-order-command published — the rollback sequence. -->
![minikube](images/chap04-7.png)
*그림 4-17: orchestrator 롤백 로그 확인*



테스트가 끝났으면 이번 챕터에서 실행한 리소스를 정리합니다.

```bash
kubectl delete all --all -n metacoding
```

*상품 서비스를 꺼봤다. 주문 서비스는 멀쩡히 돌아갔고, 메시지는 Kafka에 쌓였다. 다시 켜자 밀려 있던 메시지가 순서대로 처리됐다. 단순히 서비스를 나눈 것을 넘어, 진정한 독립을 이룬 기분이다.*

**선배**: "이제 사용자 입장에서 한번 생각해봐. 주문이 끝났는지 알려면 새로고침을 계속 눌러야 하잖아."

## 이것만은 기억하자

이번 챕터에서 만든 것을 정리합니다.

- 동기 REST 호출을 **Kafka 비동기 이벤트**로 교체하여 서비스 간 결합을 끊었습니다.
- **orchestrator** 서비스가 Kafka 토픽을 통해 전체 워크플로우를 조율합니다.
- `ConcurrentHashMap`으로 주문별 진행 상태를 추적하고, 실패 시 이미 처리된 단계만 자동 롤백합니다.
- order-service는 주문 생성 즉시 `PENDING` 상태로 반환하고, 처리 완료 후 `COMPLETED`로 갱신됩니다.

이제 product-service가 잠시 다운되어도 order-service는 이벤트를 Kafka에 올려두고 즉시 반환합니다. product-service가 복구되면 토픽에서 메시지를 읽어 처리합니다. 두 서비스가 강하게 결합되어 있던 문제가 해결됐습니다.

하지만 사용자 입장에서 불편한 점이 남아 있습니다. 주문이 `COMPLETED`가 됐다는 것을 알기 위해 직접 주기적으로 조회(폴링)해야 합니다. 배달도 여전히 주문과 동시에 완료되어, 실제 배달 완료 시점을 반영하지 못합니다.

다음 챕터에서는 이 두 가지를 해결합니다. 배달 기사가 완료 API를 호출하여 실제 배달 완료를 처리하고, WebSocket으로 클라이언트에게 주문 완료를 실시간 Push로 알립니다.
