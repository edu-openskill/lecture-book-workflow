# 챕터 2. 동기식 MSA 구현 — 서비스를 연결하다

> `chap01` · 실행 환경: 로컬 · 4개 서비스 · H2 DB
> 이 챕터의 전체 소스코드는 **https://github.com/metacoding-12-msa/chap01** 에서 확인할 수 있습니다.


### 학습 목표

- Spring Boot로 4개 서비스를 독립적으로 실행하고 REST로 연결한다.
- JWT 인증 필터를 구현하고 서비스 간 Authorization 헤더를 전달한다.
- 주문 생성 시 재고 감소 → 배달 생성 흐름을 동기적으로 구현한다.
- 중간에 실패가 발생했을 때 이전 작업을 되돌리는 보상 트랜잭션을 작성한다.

## 2.1 이야기의 시작 — 네 개의 서비스가 만나다

챕터 1에서 설계한 네 개의 서비스(회원, 상품, 주문, 배달)를 이제 직접 만들어 보겠습니다.

이번 챕터의 주인공은 **주문 서비스**입니다. 주문을 생성하려면 상품 서비스에서 재고를 줄이고, 배달 서비스에서 배달을 만들어야 합니다. 즉 주문 서비스가 두 서비스를 직접 호출해야 합니다. 그런데 여기서 중요한 문제가 생깁니다. "재고는 줄였는데 배달 생성이 실패하면 어떻게 해야 할까?"

이 질문에 대한 답이 바로 이번 챕터의 핵심, **보상 트랜잭션**입니다.

> **보상 트랜잭션(Compensating Transaction)**: 여러 서비스에 걸친 작업 중 일부가 실패했을 때, 이미 완료된 작업을 되돌리기 위해 역순으로 실행하는 취소 작업입니다.

### 2.1.1 서비스별 독립 Gradle 프로젝트

각 서비스는 독립된 Gradle 프로젝트입니다. 하나의 서비스를 배포할 때 다른 서비스를 건드릴 필요가 없습니다.

```text
chap01/
├── user/               # 포트 8083
├── product/            # 포트 8082
├── order/              # 포트 8081
├── delivery/           # 포트 8084
└── docker-compose.yml  # 전체 서비스 실행
```

각 서비스 내부 패키지 구조는 아래와 같습니다. core 패키지에는 JWT, 예외 처리, 표준 응답 등 모든 서비스에 공통으로 필요한 코드가 들어갑니다. 주문 서비스 기준으로 보여드리며, 회원/상품/배달 서비스도 동일한 구조입니다.

```text
src/main/java/com/metacoding/order/
├── OrderApplication.java                 # [참고]
├── core/
│   ├── config/
│   │   ├── WebConfig.java                # [참고] JWT 필터 등록
│   │   └── RestClientConfig.java         # [작성] JWT 헤더 전달 인터셉터
│   ├── filter/
│   │   └── JwtAuthenticationFilter.java  # [참고] JWT 인가 필터
│   ├── handler/
│   │   ├── GlobalExceptionHandler.java   # [참고] 전역 예외 처리
│   │   └── ex/                           # 커스텀 예외 (Exception400~500)
│   └── util/
│       ├── JwtProvider.java              # [참고] JWT 파싱/검증
│       ├── JwtUtil.java                  # [참고] JWT 생성
│       └── Resp.java                     # [참고] 표준 응답 래퍼
├── order/
│   ├── Order.java                        # [참고] JPA 엔티티
│   ├── OrderItem.java                    # [참고] JPA 엔티티
│   ├── OrderController.java             # [참고] REST 컨트롤러
│   ├── OrderService.java                # [작성] 비즈니스 로직
│   ├── OrderRepository.java             # [참고] Spring Data JPA
│   ├── OrderItemRepository.java         # [참고] Spring Data JPA
│   └── OrderRequest.java / OrderResponse.java  # [참고]
└── adapter/                              # 주문 서비스에만 존재
    ├── ProductClient.java               # [작성] 상품 서비스 호출
    ├── DeliveryClient.java              # [작성] 배달 서비스 호출
    └── dto/                             # 어댑터용 DTO
Dockerfile                                # [참고] Docker 이미지 빌드
```

> **참고**: 회원/상품/배달 서비스는 `adapter/` 패키지와 `RestClientConfig`가 없고, 나머지 구조는 동일합니다.


## 2.2 공통 설정 : 모든 서비스가 공유하는 뼈대

서비스 구조를 잡았으니, 먼저 공통 기반을 만들겠습니다. MSA에서는 서비스마다 서버가 다르므로 세션을 공유할 수 없습니다. 대신 JWT 토큰을 발급하고, 각 서비스가 토큰만 검증하는 방식을 사용합니다. 4개 서비스 모두 JWT 인증, 표준 응답 형식, 예외 처리가 필요합니다. 이를 `core/` 패키지에 모아 두면, 각 서비스는 비즈니스 로직에 집중할 수 있습니다.

각 컴포넌트의 역할은 다음과 같습니다.

| 컴포넌트 | 역할 |
|---|---|
| **JwtAuthenticationFilter** | 매 요청마다 `Authorization` 헤더에서 JWT를 꺼내 검증하고, 토큰 안의 `userId`를 request attribute에 저장합니다. 컨트롤러는 `@RequestAttribute("userId")`로 현재 사용자를 식별합니다. |
| **JwtUtil / JwtProvider** | JwtUtil은 로그인 성공 시 JWT를 생성하고, JwtProvider는 요청에서 받은 토큰을 파싱·검증합니다. |
| **Resp** | 모든 API 응답을 `{status, msg, body}` 형태로 통일하는 래퍼 클래스입니다. 성공과 실패 모두 같은 구조로 반환하여 클라이언트 파싱을 단순화합니다. |
| **GlobalExceptionHandler** | `@RestControllerAdvice`로 전역 예외를 잡아 Resp 형태의 에러 응답을 반환합니다. |
| **WebConfig** | JWT 필터를 등록합니다. `/api/*` 경로에 `JwtAuthenticationFilter`를 적용하여 인증이 필요한 요청을 필터링합니다. |

공통 설정이 준비되었습니다. 주문 서비스의 보상 트랜잭션을 직접 작성하기 전에, 나머지 세 서비스의 핵심 코드를 먼저 살펴보겠습니다. 아래 2.3~2.5는 `[참고]` 코드로, 동작 이해를 위해 주요 부분만 보여줍니다.

> 전체 코드는 GitHub에서 확인할 수 있습니다.


## 2.3 회원 서비스 : JWT로 로그인하다

회원 서비스는 로그인과 사용자 조회를 담당합니다. 사용자가 `POST /login`으로 아이디와 비밀번호를 보내면, 회원 서비스가 DB에서 조회하고 비밀번호를 검증합니다. 검증에 성공하면 JWT 토큰을 응답 헤더에 넣어 돌려줍니다. 이 토큰이 이후 모든 서비스 요청의 인증 수단이 됩니다.

| 메서드 | 경로 | 기능 |
|---|---|---|
| POST | /login | 로그인 (JWT 발급) |
| GET | /api/users/{userId} | 사용자 조회 |

### 2.3.1 User 엔티티

`username`은 유니크 제약으로 중복 가입을 방지합니다.

**[참고]** `users/User.java`

```java
@NoArgsConstructor
@Getter
@Entity
@Table(name = "user_tb")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    @Column(unique = true)
    private String username;
    private String email;
    private String password;
    private String roles;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    @Builder
    private User(String username, String email, String password, String roles) {
        this.username = username;
        this.email = email;
        this.password = password;
        this.roles = roles;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }
}
```

### 2.3.2 더미 데이터

개발 환경에서는 H2 in-memory DB에 자동으로 테스트 데이터를 삽입합니다. `db/data.sql`에 ssar, cos, love 세 계정이 등록됩니다.

**[참고]** `resources/db/data.sql`

```sql
INSERT INTO user_tb (username, email, password, roles, created_at, updated_at)
VALUES ('ssar','ssar@metacoding.com','1234','USER',now(),now());

INSERT INTO user_tb (username, email, password, roles, created_at, updated_at)
VALUES ('cos','cos@metacoding.com','1234','USER',now(),now());

INSERT INTO user_tb (username, email, password, roles, created_at, updated_at)
VALUES ('love','love@metacoding.com','1234','USER',now(),now());
```


## 2.4 상품 서비스 : 재고를 관리하다

상품 서비스는 상품 목록 조회와 재고 증감을 담당합니다. 주문 서비스가 주문을 생성할 때 이 서비스의 재고 감소 API를 호출하고, 주문이 취소되거나 실패하면 재고 증가 API로 되돌립니다.

| 메서드 | 경로 | 기능 |
|---|---|---|
| GET | /api/products/{productId} | 상품 조회 |
| PUT | /api/products/{productId}/decrease | 재고 감소 |
| PUT | /api/products/{productId}/increase | 재고 증가 |


### 2.4.1 Product 엔티티

`decreaseQuantity`와 `increaseQuantity` 메서드로 재고 증감 로직이 엔티티에 캡슐화되어 있습니다.

**[참고]** `products/Product.java`

```java
@NoArgsConstructor
@Getter
@Entity
@Table(name = "product_tb")
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    private String productName;
    private int quantity;
    private Long price;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    @Builder
    private Product(String productName, int quantity, Long price) {
        this.productName = productName;
        this.quantity = quantity;
        this.price = price;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    public void decreaseQuantity(int quantity) {
        this.quantity -= quantity;
        this.updatedAt = LocalDateTime.now();
    }

    public void increaseQuantity(int quantity) {
        this.quantity += quantity;
        this.updatedAt = LocalDateTime.now();
    }
}
```

### 2.4.2 ProductService

재고 감소 전 상품 존재 여부와 가격 일치 여부를 검증합니다.

**[참고]** `products/ProductService.java`

```java
@Transactional
public ProductResponse decreaseQuantity(int productId, int quantity, Long price) {
    Product findProduct = productRepository.findById(productId)
            .orElseThrow(() -> new Exception404("상품이 없습니다."));
    if (findProduct.getQuantity() < quantity) {
        throw new Exception400("상품 재고가 부족합니다.");
    }
    if (!price.equals(findProduct.getPrice())) {
        throw new Exception400("상품 가격이 일치하지 않습니다.");
    }
    findProduct.decreaseQuantity(quantity);  // 재고 감소
    return ProductResponse.from(findProduct);
}
```

### 2.4.3 더미 데이터

`db/data.sql`에 MacBook Pro(재고 10, 250만원), iPhone 15(재고 0 품절, 130만원), AirPods(재고 10, 30만원)가 등록됩니다. 2.7 실행 시나리오에서 품절 상품으로 주문했을 때 보상 트랜잭션이 어떻게 동작하는지 확인합니다.

**[참고]** `resources/db/data.sql`

```sql
INSERT INTO product_tb (product_name, quantity, price, created_at, updated_at)
VALUES ('MacBook Pro', 10, 2500000, now(), now());

INSERT INTO product_tb (product_name, quantity, price, created_at, updated_at)
VALUES ('iPhone 15', 0, 1300000, now(), now());

INSERT INTO product_tb (product_name, quantity, price, created_at, updated_at)
VALUES ('AirPods', 10, 300000, now(), now());
```


## 2.5 배달 서비스 : 배달을 생성하고 취소하다

배달 서비스는 배달 생성과 취소를 담당합니다. 이번 챕터에서는 배달 생성과 동시에 완료 처리합니다. PENDING 상태로 생성한 뒤 즉시 COMPLETED로 전이하므로, 실질적으로 COMPLETED 또는 CANCELLED 두 상태만 관찰됩니다.

| 메서드 | 경로 | 기능 |
|---|---|---|
| POST | /api/deliveries | 배달 생성 |
| GET | /api/deliveries/{deliveryId} | 배달 조회 |
| PUT | /api/deliveries/{orderId} | 배달 취소 |

### 2.5.1 Delivery 엔티티

상태는 `PENDING → COMPLETED` 또는 `PENDING → CANCELLED`로 전이되며, `create()`, `complete()`, `cancel()` 메서드로 캡슐화되어 있습니다.

**[참고]** `deliveries/Delivery.java`

```java
@NoArgsConstructor
@Getter
@Entity
@Table(name = "delivery_tb")
public class Delivery {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    private int orderId;
    private String address;
    @Enumerated(EnumType.STRING)
    private DeliveryStatus status;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    @Builder
    private Delivery(int orderId, String address, DeliveryStatus status) {
        this.orderId = orderId;
        this.address = address;
        this.status = status;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    public static Delivery create(int orderId, String address) {
        return new Delivery(orderId, address, DeliveryStatus.PENDING);
    }

    public void complete() {
        this.status = DeliveryStatus.COMPLETED;
        this.updatedAt = LocalDateTime.now();
    }

    public void cancel() {
        this.status = DeliveryStatus.CANCELLED;
        this.updatedAt = LocalDateTime.now();
    }
}
```

### 2.5.2 DeliveryService

`createDelivery`는 배달을 생성하고 즉시 완료 처리합니다. `cancelDelivery`는 주문 취소 시 호출되며, 이미 취소된 배달에 대한 중복 요청을 방어합니다.

**[참고]** `deliveries/DeliveryService.java`

```java
@Transactional
public DeliveryResponse createDelivery(int orderId, String address) {
    // 1. 배달 생성
    Delivery createdDelivery = deliveryRepository.save(Delivery.create(orderId, address));
    // 2. 주소 검증
    if (address == null || address.isBlank()) {
        throw new Exception400("배달 주소는 필수입니다.");
    }
    // 3. 배달 완료
    createdDelivery.complete();
    return DeliveryResponse.from(createdDelivery);
}

@Transactional
public DeliveryResponse cancelDelivery(int orderId) {
    Delivery findDelivery = deliveryRepository.findByOrderId(orderId)
            .orElseThrow(() -> new Exception404("배달 정보를 조회할 수 없습니다."));
    if (findDelivery.getStatus() == DeliveryStatus.CANCELLED) {
        throw new Exception400("배달이 이미 취소되었습니다.");
    }
    findDelivery.cancel();
    return DeliveryResponse.from(findDelivery);
}
```

### 2.5.3 더미 데이터

주문 3건에 대한 배달 데이터가 등록됩니다. 모두 완료 상태입니다.

**[참고]** `resources/db/data.sql`

```sql
INSERT INTO delivery_tb (order_id, address, status, created_at, updated_at) VALUES (1, 'Addr 1', 'COMPLETED', NOW(), NOW());
INSERT INTO delivery_tb (order_id, address, status, created_at, updated_at) VALUES (2, 'Addr 2', 'COMPLETED', NOW(), NOW());
INSERT INTO delivery_tb (order_id, address, status, created_at, updated_at) VALUES (3, 'Addr 3', 'COMPLETED', NOW(), NOW());
```


## 2.6 주문 서비스 : 보상 트랜잭션의 현장 (핵심)

배달 서비스까지 살펴봤으니, 이제 핵심인 주문 서비스로 넘어갑니다.

| 메서드 | 경로 | 기능 |
|---|---|---|
| POST | /api/orders | 주문 생성 |
| GET | /api/orders/{orderId} | 주문 조회 |
| PUT | /api/orders/{orderId} | 주문 취소 |

먼저 주문과 주문 상품을 표현하는 엔티티부터 살펴보겠습니다.

### 2.6.1 Order 엔티티

상태는 `PENDING → COMPLETED` 또는 `PENDING → CANCELLED`로 전이되며, `create()`, `complete()`, `cancel()` 메서드로 캡슐화되어 있습니다.

**[참고]** `orders/Order.java`

```java
@NoArgsConstructor
@Getter
@Entity
@Table(name = "order_tb")
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    private int userId;
    @Enumerated(EnumType.STRING)
    private OrderStatus status;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    @Builder
    private Order(int userId, OrderStatus status) {
        this.userId = userId;
        this.status = status;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    public static Order create(int userId) {
        return new Order(userId, OrderStatus.PENDING);
    }

    public void complete() {
        this.status = OrderStatus.COMPLETED;
        this.updatedAt = LocalDateTime.now();
    }

    public void cancel() {
        this.status = OrderStatus.CANCELLED;
        this.updatedAt = LocalDateTime.now();
    }
}
```

### 2.6.2 OrderItem 엔티티

하나의 주문에 여러 상품이 포함될 수 있으므로 Order와 분리합니다. `create()` 메서드로 생성합니다.

**[참고]** `orders/OrderItem.java`

```java
@NoArgsConstructor
@Getter
@Entity
@Table(name = "order_item_tb")
public class OrderItem {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    private int orderId;
    private int productId;
    private int quantity;
    private Long price;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    @Builder
    private OrderItem(int orderId, int productId, int quantity, Long price) {
        this.orderId = orderId;
        this.productId = productId;
        this.quantity = quantity;
        this.price = price;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    public static OrderItem create(int orderId, int productId, int quantity, Long price) {
        return new OrderItem(orderId, productId, quantity, price);
    }
}
```

### 2.6.3 더미 데이터

사용자별 주문 3건(완료·취소·대기)과 각 주문에 대한 주문 상품 1건씩이 등록됩니다.

**[참고]** `resources/db/data.sql`

```sql
INSERT INTO order_tb (user_id, status, created_at, updated_at) VALUES (1, 'COMPLETED', now(), now());
INSERT INTO order_tb (user_id, status, created_at, updated_at) VALUES (2, 'CANCELLED', now(), now());
INSERT INTO order_tb (user_id, status, created_at, updated_at) VALUES (3, 'PENDING', now(), now());

INSERT INTO order_item_tb (order_id, product_id, quantity, price, created_at, updated_at) VALUES (1, 1, 1, 2500000, now(), now());
INSERT INTO order_item_tb (order_id, product_id, quantity, price, created_at, updated_at) VALUES (2, 3, 1, 300000, now(), now());
INSERT INTO order_item_tb (order_id, product_id, quantity, price, created_at, updated_at) VALUES (3, 2, 2, 1300000, now(), now());
```

### 2.6.4 보상 트랜잭션 : 실패하면 되돌린다

엔티티가 준비되었으니, 이제 주문 서비스의 진짜 역할을 살펴봅니다. 주문 서비스는 상품 서비스와 배달 서비스를 **직접 호출**합니다. 그런데 서비스를 호출하면 반드시 이 질문과 마주합니다.

> "재고는 줄였는데, 배달 생성이 실패하면 어떻게 하죠?"

단일 서비스였다면 DB 트랜잭션이 자동으로 롤백해줍니다. 하지만 이미 상품 서비스에 보낸 HTTP 요청은 되돌릴 수 없습니다. 우리가 직접 "재고를 다시 늘려줘"라는 HTTP 요청을 보내야 합니다. 이것이 **보상 트랜잭션**입니다. 챕터 1에서 소개한 Choreography Saga를 직접 HTTP 호출로 구현하는 방식입니다. 주문 서비스가 직접 각 서비스를 호출하고, 실패 시 역순으로 보상합니다.

### 2.6.5 보상 트랜잭션 설계

코드를 작성하기 전, 어느 단계에서 실패하면 무엇을 되돌려야 하는지 먼저 그려봅니다.

```text
주문 생성 흐름 (단계별 보상):

1단계: 재고 감소 (상품 서비스)
   └─ 실패 → 보상 없음 (아직 아무 일도 안 했으므로)

2단계: 배달 생성 (배달 서비스)
   └─ 실패 → 보상: 재고 복구 (1단계 되돌리기)

3단계: 주문 완료
   └─ 실패 → 보상: 배달 취소 + 재고 복구 (2, 1단계 되돌리기)

4단계: 성공 응답 반환
```

핵심 아이디어는 **진행 상태를 플래그로 추적**하는 것입니다. `productDecreased`와 `deliveryCreated` 변수가 각각 1단계, 2단계의 성공 여부를 기록합니다. 예외가 발생했을 때 이 플래그를 보고, 어디까지 진행됐는지 확인한 뒤 역순으로 되돌립니다.


### 2.6.6 주문 성공 시

![주문 성공 흐름](images/fig-2-1.png)
*그림 2-1: 주문 성공 흐름*

### 2.6.7 주문 실패 시

![주문 실패 시 보상 트랜잭션 흐름](images/fig-2-2.png)
*그림 2-2: 주문 실패 시 보상 트랜잭션 흐름*

### 2.6.8 RestClient : JWT 헤더를 실어 다른 서비스를 호출하다

주문 서비스가 다른 서비스를 호출할 때 필요한 RestClient를 먼저 설정합니다. 인터셉터는 HTTP 요청이 나갈 때 자동으로 JWT 토큰을 챙겨 붙여주는 장치입니다. 택배를 보낼 때 보내는 사람 정보를 매번 적는 대신, 스티커를 자동으로 붙여주는 것과 같습니다. RestClient에 인터셉터(`ClientHttpRequestInterceptor`)를 등록하면 외부 API를 호출할 때 Authorization 헤더가 자동으로 전달되어 하위 서비스의 JWT 인증을 통과합니다.

**[작성]** `core/config/RestClientConfig.java` — 아래 코드를 해당 파일에 추가하세요.

```java
@Configuration
public class RestClientConfig {

    @Bean
    public RestClient.Builder restClientBuilder() {
        ClientHttpRequestInterceptor authForwardingInterceptor = (request, body, execution) -> { // JWT 전달 인터셉터
            ServletRequestAttributes attributes =
                    (ServletRequestAttributes) RequestContextHolder.getRequestAttributes(); // 현재 요청 정보 가져오기
            if (attributes != null) {
                String authorization = attributes.getRequest().getHeader("Authorization"); // 원본 요청의 JWT 꺼내기
                if (authorization != null) {
                    request.getHeaders().add("Authorization", authorization); // 나가는 요청에 JWT 실어 보내기
                }
            }
            return execution.execute(request, body);
        };

        return RestClient.builder().requestInterceptor(authForwardingInterceptor); // 인터셉터 등록한 빌더 반환
    }
}
```

### 2.6.9 ProductClient와 DeliveryClient

RestClient 설정이 끝났으면, 각 서비스를 호출하는 클라이언트를 만듭니다. OrderService는 클라이언트의 메서드만 호출하면 되고, HTTP 통신 방식을 알 필요가 없습니다.

> baseUrl의 `product-service`, `delivery-service`는 Docker Compose가 만들어주는 내부 주소입니다. 같은 Docker Compose 안에서는 서비스 이름만으로 서로 통신할 수 있습니다. Docker Compose 설정은 2.7절에서 다룹니다.

상품 서비스의 재고 감소·복구 API를 호출합니다.

**[작성]** `adapter/ProductClient.java` — 아래 코드를 해당 파일에 추가하세요.

```java
@Component
public class ProductClient { // 상품 서비스 호출 클라이언트

    private final RestClient restClient;

    public ProductClient(RestClient.Builder restClientBuilder) {
        this.restClient = restClientBuilder
                .baseUrl("http://product-service:8082") // 서비스 이름으로 통신 (Docker Compose가 DNS 역할)
                .build();
    }

    public void decreaseQuantity(ProductRequest requestDTO) { // 재고 감소 요청
        restClient.put()
                .uri("/api/products/{productId}/decrease", requestDTO.productId())
                .body(requestDTO)
                .retrieve()
                .toBodilessEntity();
    }

    public void increaseQuantity(ProductRequest requestDTO) { // 재고 복구 요청 (보상 트랜잭션용)
        restClient.put()
                .uri("/api/products/{productId}/increase", requestDTO.productId())
                .body(requestDTO)
                .retrieve()
                .toBodilessEntity();
    }
}
```

배달 서비스의 배달 생성·취소 API를 호출합니다.

**[작성]** `adapter/DeliveryClient.java` — 아래 코드를 해당 파일에 추가하세요.

```java
@Component
public class DeliveryClient { // 배달 서비스 호출 클라이언트

    private final RestClient restClient;

    public DeliveryClient(RestClient.Builder restClientBuilder) {
        this.restClient = restClientBuilder
                .baseUrl("http://delivery-service:8084") // 서비스 이름으로 통신 (Docker Compose가 DNS 역할)
                .build();
    }

    public void createDelivery(DeliveryRequest requestDTO) { // 배달 생성 요청
        restClient.post()
                .uri("/api/deliveries")
                .body(requestDTO)
                .retrieve()
                .toBodilessEntity();
    }

    public void cancelDelivery(int orderId) { // 배달 취소 요청 (보상 트랜잭션용)
        restClient.put()
                .uri("/api/deliveries/{orderId}", orderId)
                .retrieve()
                .toBodilessEntity();
    }
}
```

### 2.6.10 OrderService : 보상 트랜잭션의 핵심

이제 이번 챕터의 하이라이트입니다. 플래그 기반 보상 트랜잭션 패턴을 직접 구현합니다. 코드를 읽을 때 `productDecreased`와 `deliveryCreated` 두 변수를 추적하면서 읽어보세요. 각 단계 성공 시 플래그를 `true`로 바꾸고, catch 블록에서 플래그를 확인해 보상 여부를 결정합니다.

**[작성]** `orders/OrderService.java` (createOrder 메서드) — 아래 메서드를 OrderService에 추가하세요.

```java
@Transactional
public OrderResponse createOrder(int userId, List<OrderRequest.OrderItemDTO> orderItems, String address) {
    // 보상트랜잭션을 위한 플래그 선언
    boolean productDecreased = false;
    boolean deliveryCreated = false;
    Order createdOrder = null;

    try {
        // 1. 주문 생성 (PENDING)
        createdOrder = orderRepository.save(Order.create(userId));
        final int orderId = createdOrder.getId();

        // 2. 상품 재고 차감
        orderItems.forEach(item -> productClient.decreaseQuantity(
                new ProductRequest(item.productId(), item.quantity(), item.price())));
        productDecreased = true;

        // 3. 주문 아이템 저장
        List<OrderItem> createdOrderItems = orderItems.stream()
            .map(item -> OrderItem.create(orderId, item.productId(), item.quantity(), item.price()))
            .toList();
        orderItemRepository.saveAll(createdOrderItems);

        // 4. 배달 생성
        deliveryClient.createDelivery(new DeliveryRequest(orderId, address));
        deliveryCreated = true;

        // 5. 주문 완료
        createdOrder.complete();
        return OrderResponse.from(createdOrder, createdOrderItems);

    } catch (Exception e) {
        // 보상 트랜잭션: 역순으로 되돌리기
        if (deliveryCreated) {
            deliveryClient.cancelDelivery(createdOrder.getId());
        }
        if (productDecreased) {
            orderItems.forEach(item -> productClient.increaseQuantity(
                    new ProductRequest(item.productId(), item.quantity(), item.price())
            ));
        }
        throw new Exception500("주문 생성 중 오류가 발생했습니다: " + e.getMessage());
    }
}
```

OrderService의 나머지 두 메서드입니다. `findById`는 주문과 주문 아이템을 조회합니다. `cancelOrder`는 createOrder의 역과정으로, 재고 복구(`increaseQuantity`) → 배달 취소(`cancelDelivery`) → 주문 상태 변경(`cancel()`) 순서로 처리합니다.

**[참고]** `orders/OrderService.java`

```java
// 주문 조회
public OrderResponse findById(int orderId) {
    Order findOrder = orderRepository.findById(orderId)
            .orElseThrow(() -> new Exception404("주문을 찾을 수 없습니다."));
    List<OrderItem> findOrderItems = orderItemRepository.findByOrderId(orderId)
            .orElseThrow(() -> new Exception404("주문 아이템을 찾을 수 없습니다."));
    return OrderResponse.from(findOrder, findOrderItems);
}

// 주문 취소
@Transactional
public OrderResponse cancelOrder(int orderId) {
    Order findOrder = orderRepository.findById(orderId)
            .orElseThrow(() -> new Exception404("주문을 찾을 수 없습니다."));
    if(findOrder.getStatus() == OrderStatus.CANCELLED) {
        throw new Exception400("주문이 이미 취소되었습니다.");
    }
    List<OrderItem> findOrderItems = orderItemRepository.findByOrderId(orderId)
            .orElseThrow(() -> new Exception404("주문 아이템을 찾을 수 없습니다."));
    // 상품 재고 복구
    findOrderItems.forEach(item -> productClient.increaseQuantity(
            new ProductRequest(item.getProductId(), item.getQuantity(), item.getPrice())
    ));
    // 배달 취소
    deliveryClient.cancelDelivery(orderId);
    // 주문 취소
    findOrder.cancel();
    return OrderResponse.from(findOrder);
}
```


## 2.7 Docker Compose : 네 개의 서비스를 한 번에 실행하다

코드가 완성되었습니다. 이제 직접 실행하여 보상 트랜잭션이 작동하는 것을 눈으로 확인해 봅니다.

### 2.7.1 서비스 실행

각 서비스의 Dockerfile은 동일한 구조입니다. 4개 서비스 모두 아래와 같습니다.

**[참고]** `Dockerfile`
스프링 프로젝트를 컨테이너 내에서 실행합니다.

```dockerfile
FROM eclipse-temurin:21-jdk          # JDK 21 베이스 이미지
WORKDIR /app                         # 작업 디렉토리 설정
COPY . .                             # 프로젝트 파일 복사
RUN chmod +x gradlew                 # Gradle Wrapper 실행 권한 부여
RUN ./gradlew bootJar -x test        # 테스트 생략, JAR 빌드
RUN cp build/libs/*.jar app.jar      # 빌드된 JAR를 app.jar로 복사
ENTRYPOINT ["java", "-jar", "app.jar"]  # JAR 실행
```

`chap01` 디렉토리의 `docker-compose.yml`로 4개 서비스를 한 번에 실행합니다.

**[참고]** `docker-compose.yml`
4개 서비스 구조가 동일하므로, 주문 서비스만 예시로 보여줍니다.

```yaml
services:
  order-service:                   # 주문 서비스 정의
    build:
      context: ./order             # 빌드할 소스 경로
    ports:
      - "8081:8081"                # 호스트:컨테이너 포트 매핑
    networks:
      - msa-network                # 같은 네트워크에 연결해야 서비스 이름으로 통신 가능

  # user-service(8083), product-service(8082), delivery-service(8084) 동일 패턴 (Github에서 확인 가능합니다)

networks:
  msa-network:                     # 4개 서비스를 하나로 묶는 가상 네트워크
```

`msa-network`로 묶여 있기 때문에, 컨테이너끼리는 서비스 이름(예: `http://product-service:8082`)으로 통신합니다.

**[작성]** 프로젝트가 위치한 폴더로 이동 후, 터미널에서 Docker Compose로 4개 서비스를 한 번에 빌드하고 실행합니다.

```bash
cd chap01
docker compose up
```

실행이 완료되면 각 서비스에 접근할 수 있습니다.

| 서비스 | 주소 |
|---|---|
| 주문 서비스 | http://localhost:8081 |
| 상품 서비스 | http://localhost:8082 |
| 회원 서비스 | http://localhost:8083 |
| 배달 서비스 | http://localhost:8084 |

### 2.7.2 사전 준비

실행 시나리오를 따라하려면 두 가지가 필요합니다.

**Docker Desktop**

Docker가 설치되어 있어야 합니다. https://www.docker.com/products/docker-desktop/ 에서 설치하세요. Docker Desktop을 실행하고 화면 하단에 "Engine running"이 표시되면 준비 완료입니다. 터미널에서 `docker compose up`을 실행합니다. 처음 실행 시 이미지 빌드에 5~10분이 소요될 수 있습니다. 터미널이 멈춘 것처럼 보여도 정상이니 기다려 주세요. 빌드 진행 상황은 `docker compose logs -f [서비스명]`으로 확인할 수 있습니다.

<!-- terminal-prompt: Terminal output showing "docker compose up" command execution in the chap01 directory. Four Spring Boot services (user-service:8083, product-service:8082, order-service:8081, delivery-service:8084) starting up with Spring Boot banner and "Started Application" messages. All services show successful startup. -->
![docker compose up](images/chap02-1.png)
*그림 2-3: Docker Compose 실행 결과*

**API 테스트 도구 — Hoppscotch**

서비스가 실행되면 API를 호출하여 결과를 확인해야 합니다. 이 책에서는 Hoppscotch(https://hoppscotch.io/)를 사용합니다. localhost로 요청을 보내려면 Chrome 웹 스토어에서 **Hoppscotch Browser Extension**을 설치합니다. 설치 후 Hoppscotch 화면 하단의 인터셉터 설정에서 **"Browser Extension"** 을 선택하세요.

<!-- terminal-prompt: Hoppscotch web interface showing the main API testing screen with method selector (GET/POST/PUT/DELETE), URL input field, headers section, and body section. Clean UI with dark/light theme. -->
![Hoppscotch](images/chap02-2.png)
*그림 2-4: Hoppscotch 화면*

<!-- terminal-prompt: Hoppscotch settings panel showing interceptor configuration. "Browser Extension" option is selected (highlighted) instead of "Proxy" option. This enables localhost requests from the browser. -->
![Hoppscotch](images/chap02-3.png)
*그림 2-5: Browser Extension 인터셉터 설정*

### 2.7.3 시나리오 1: 정상 주문

먼저 로그인하여 JWT 토큰을 받습니다. 이때 콘텐츠 종류(Content-Type)를 `application/json`으로 설정해야 합니다. 이는 서버에게 "내가 보내는 데이터는 JSON 형식이다"라고 알려주는 것입니다. 

```json
POST http://localhost:8083/login

{
  "username": "ssar",
  "password": "1234"
}
```
<!-- terminal-prompt: Hoppscotch showing POST request to http://localhost:8083/login with JSON body {"username":"ssar","password":"1234"}. Response status 200 OK. Response headers showing "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9..." JWT token. -->
![Hoppscotch](images/chap02-4.png)
*그림 2-6: 로그인 API 호출 결과*

응답 바디 데이터에 포함된 JWT 토큰을 확인할 수 있습니다. 

받은 토큰을 Hoppscotch의 인증 > 인증 유형(Bearer) 항목의 토큰 필드에 넣습니다.

<!-- terminal-prompt: Hoppscotch Authorization tab showing "Bearer" type selected. Token input field contains the JWT token string starting with "eyJhbGciOiJIUzI1NiJ9...". -->
![Hoppscotch](images/chap02-5.png)
*그림 2-7: Bearer 토큰 설정*

MacBook Pro(상품 ID 1, 재고 10개)를 1개 주문합니다.

```json
POST http://localhost:8081/api/orders

{
  "address": "Addr 4",
  "orderItems": [
    {
      "productId": 1,
      "quantity": 1,
      "price": 2500000
    }
  ]
}
```
<!-- terminal-prompt: Hoppscotch showing POST request to http://localhost:8081/api/orders with Bearer token. Response 200 OK with JSON body: {"status":200,"msg":"성공","body":{"id":4,"userId":1,"status":"COMPLETED","orderItems":[{"productId":1,"quantity":1,"price":2500000}]}}. -->
![Hoppscotch](images/chap02-6.png)
*그림 2-8: 주문 생성 API 호출 결과*

주문이 성공하면 상품 서비스에서 재고가 10 → 9로 줄어들고, 배달 서비스에 배달이 생성됩니다.
```json
GET http://localhost:8082/api/products/1
```
<!-- terminal-prompt: Hoppscotch showing GET request to http://localhost:8082/api/products/1. Response 200 OK with JSON body showing product "MacBook Pro" with quantity changed from 10 to 9, confirming inventory decrease. -->
![Hoppscotch](images/chap02-7.png)
*그림 2-9: 재고 감소 확인*

```json
GET http://localhost:8084/api/deliveries/4
```
<!-- terminal-prompt: Hoppscotch showing GET request to http://localhost:8084/api/deliveries/4. Response 200 OK with JSON body showing delivery with orderId:4, address:"Addr 4", status:"COMPLETED". -->
![Hoppscotch](images/chap02-8.png)
*그림 2-10: 배달 생성 확인*

### 2.7.4 시나리오 2: 재고 부족

품절 상품인 iPhone 15(상품 ID 2, 재고 0)를 주문해봅니다. 첫 번째 단계(재고 차감)에서 바로 실패하므로 보상할 작업이 없어 즉시 에러가 반환됩니다.

```json
POST http://localhost:8081/api/orders

{
  "address": "Addr 4",
  "orderItems": [
    {
      "productId": 2,
      "quantity": 1,
      "price": 1300000
    }
  ]
}
```
<!-- terminal-prompt: Hoppscotch showing POST request to http://localhost:8081/api/orders with iPhone 15 (productId:2). Response 500 with JSON body: {"status":500,"msg":"주문 생성 중 오류가 발생했습니다: 상품 재고가 부족합니다.","body":null}. -->
![Hoppscotch](images/chap02-9.png)
*그림 2-11: 재고 부족 시 에러 응답*

### 2.7.5 시나리오 3: 주소 누락

이번에는 주소를 빈 문자열로 보내봅니다. 주문 자체는 재고 차감까지 진행되지만, 배달 서비스에서 주소가 없으므로 실패합니다. 이때 보상 트랜잭션이 작동하여 차감된 재고가 복구됩니다.

```json
POST http://localhost:8081/api/orders

{
  "address": "",
  "orderItems": [
    {
      "productId": 1,
      "quantity": 1,
      "price": 2500000
    }
  ]
}
```
<!-- terminal-prompt: Hoppscotch showing POST request to http://localhost:8081/api/orders with empty address. Response showing error. -->
![Hoppscotch](images/chap02-10.png)
*그림 2-12: 주소 누락 시 에러 응답*

그리고 재고가 원복되었는지 확인합니다.

```json
GET http://localhost:8082/api/products/1
```


<!-- terminal-prompt: Hoppscotch or DB showing product stock restored after failed order. -->
![Hoppscotch](images/chap02-11.png)
*그림 2-13: 재고 원복 확인*

테스트가 끝났으면 실행 중인 컨테이너를 정리합니다.

```bash
docker compose down
```

이 명령어를 실행하면 docker compose up으로 띄운 모든 컨테이너가 종료되고 제거됩니다.

## 이것만은 기억하자

이번 챕터에서 만든 것을 정리합니다.

- 4개의 Spring Boot 서비스를 독립적으로 실행하고 REST로 연결했습니다.
- JWT 인증 필터를 구현하여 모든 서비스가 독립적으로 토큰을 검증합니다.
- 주문 서비스에서 RestClient 인터셉터로 Authorization 헤더를 하위 서비스에 자동 전달합니다.
- 플래그 기반 보상 트랜잭션으로 주문 실패 시 재고와 배달을 원상복구합니다.

보상 트랜잭션 덕분에 데이터 일관성을 유지할 수 있었습니다. 하지만 이 구조에는 눈에 잘 보이지 않는 문제가 있습니다.

**이 구조의 한계**:
- 모든 서비스 호출이 동기적입니다. 상품 서비스가 1초 걸리면 주문 서비스 전체가 1초를 기다립니다.
- 보상 트랜잭션 코드가 비즈니스 로직과 섞여 복잡합니다. 서비스가 늘어날수록 try-catch 중첩이 깊어집니다.
- 지금은 로컬에서만 실행됩니다. 실제 운영 서버에 올리려면 배포 방법을 별도로 고민해야 합니다.

코드 구조가 복잡해지는 것도 문제지만, 더 근본적인 문제는 **운영 가능한 형태로 만들어야 한다**는 것입니다. 다음 챕터에서는 코드 구조를 Clean Architecture로 개선하고, Kubernetes로 배포하는 방법을 배웁니다.
