# 챕터 3. 도메인을 중심으로 - DDD + 클린 아키텍처와 Kubernetes

> 이 챕터의 전체 소스코드는 **https://github.com/metacoding-12-msa/ex02** 에서 확인할 수 있습니다.

:::goal
이번 챕터가 끝나면

- 비즈니스 규칙을 도메인 객체에 캡슐화하는 **DDD(Rich Domain Model)** 를 적용할 수 있습니다.
- 컨트롤러가 구현체 대신 UseCase 인터페이스에 의존하도록 **클린 아키텍처**로 구조를 정리할 수 있습니다.
- Nginx API Gateway로 4개 서비스 진입점을 하나로 통합할 수 있습니다.
- MySQL을 연결하고 개발/운영 프로파일을 분리할 수 있습니다.
- Kubernetes에 매니페스트로 배포하고 ConfigMap·Secret으로 환경 변수를 주입할 수 있습니다.
:::

<!-- [FLOW CARD: ch3-arc]
사건: 새 비즈니스 규칙 "30분 취소" — 어디 손대야 할지 모르겠다
깨달음: 도메인이 코드의 중심에 와야 — DDD + 클린 아키텍처
결과: ex02 — 안은 도메인이 자기 일을 알고, 밖은 한 입구, 위에서는 K8s가 살린다
-->

::::prep
**준비하기**. 실습 시작 전 한 번만 설정

### 1. 소스 코드 클론

```bash [터미널] 레포 클론
git clone https://github.com/metacoding-12-msa/ex02.git
cd ex02
```

### 2. 실습 환경

| 도구 | 용도 | 비고 |
|------|------|------|
| **Docker Desktop** | 컨테이너 런타임 | 챕터 2에서 설치한 그대로. 실행 중이어야 함 |
| **Minikube** | 로컬 Kubernetes 클러스터 | https://minikube.sigs.k8s.io/ |

Docker Desktop이 "Engine running" 상태인지 확인하고, Minikube가 설치되어 있지 않다면 위 주소에서 설치합니다.

### 3. 실습 순서

1. 챕터 2 코드를 DDD + 클린 아키텍처로 재구성한 결과 살펴보기
2. Nginx API Gateway 살펴보기
3. 개발(H2) · 운영(MySQL) 프로파일 분리 확인
4. K8s 매니페스트(ConfigMap·Secret·Deployment·Service·Ingress) 5종 살펴보기
5. Minikube에서 빌드·배포·실행

:::note
**이번 챕터는 직접 코드를 작성하지 않습니다.** 챕터 2 프로젝트를 DDD + 클린 아키텍처로 재구성한 결과를 살펴보고, Kubernetes 배포를 실습합니다.
:::
::::

ex01을 만든 며칠 뒤, 기획자가 새 요구를 들고 왔습니다.

**기획자**: "주문 후 **30분 이내만 취소 가능**으로 해주세요."

오픈이가 `OrderService.cancelOrder`를 열었습니다. 이미 if문 한 줄이 들어 있습니다 — "이미 취소된 주문이면 거부". 30분 검증을 어디에 끼울까요. if를 하나 더 추가하면 되긴 합니다. 그런데 코드를 다시 훑어보니 **같은 종류의 검증이 여기저기 흩어져 있습니다**.

- `ProductService` — 재고 부족 검증 if
- `ProductService` — 가격 일치 검증 if
- `DeliveryService` — 주소 빈 값 검증 if
- `DeliveryService` — 이미 취소 검증 if

새 비즈니스 규칙이 들어올 때마다 if를 어디에 추가할지 매번 고민입니다. Service가 점점 비대해지고, 같은 종류의 규칙이 여러 Service에 흩어집니다.

동료가 옆에서 코드를 봤습니다.

**동료**: "근데 이상하지 않아? **`Order`가 자기가 취소 가능한지를 답해야 하는 거 아니야?** `findOrder.canBeCancelled()` 같이. 지금은 `Order`가 그냥 데이터 덩어리고 Service가 다 답하고 있잖아."

오픈이가 멈칫했습니다. 그 말이 맞습니다. `Order` 클래스에는 필드와 getter만 있고, "이 주문이 취소 가능한가?" 같은 **자기 일에 대한 답**이 없습니다. 도메인의 일을 Service가 대신 답하고 있었습니다.

여기서 끝이 아닙니다. 오픈이는 같은 코드를 다른 각도로 봤습니다. 컨트롤러가 `OrderService` 구현체를 직접 들고 있어서, 환경별·테스트별로 다른 구현체를 끼울 수 없습니다. 단위 테스트를 짜려고 해도 진짜 DB·진짜 RestClient를 다 띄워야 합니다.

선배 자리로 갔습니다.

**선배**: "사실 두 가지가 한 뿌리예요. **도메인이 코드의 중심에 와야 한다**는 거. 그런데 그러려면 두 단을 풀어야 해요. 첫 번째는 **DDD** — 비즈니스 규칙을 도메인 객체 안에 캡슐화하는 거. `Order`가 자기가 취소 가능한지 답하도록. 두 번째는 **클린 아키텍처** — 컨트롤러가 구현체가 아닌 약속(UseCase 인터페이스)에 의존하도록. 그러면 도메인이 진짜 가운데에 자리잡고, 외부 기술이 도메인에 맞춰 들어와요."

*도메인을 가운데에 두자. 그게 핵심이구나.*

## 3.1 한 뿌리, 두 패턴

ex01을 다시 보면 두 가지 통증이 한 뿌리에서 나옵니다 — **도메인이 자기 일을 모르고 Service가 다 답한다**. 이걸 해결하는 두 패턴이 같이 갑니다.

| 단 | 통증 | 풀이 | 패턴 이름 |
|---|---|---|---|
| 1 | 비즈니스 규칙이 Service에 흩어짐. `Order`는 데이터 덩어리 | 도메인 객체에 행위를 캡슐화. `Order.validateCancelable()`·`Order.cancel()` | **DDD** (Rich Domain Model) |
| 2 | 컨트롤러가 `OrderService` 구현체에 직접 의존. 테스트·환경별 교체 안 됨 | 약속(UseCase 인터페이스)을 추출. 컨트롤러는 약속만 안다 | **클린 아키텍처** (의존성 역전) |

두 패턴이 합쳐져 **"도메인을 가운데에 두고 외부 기술이 도메인에 맞춰진다"** 는 한 그림이 됩니다.

:::term-box
**DDD(Domain-Driven Design)란?** 도메인(비즈니스 규칙)을 코드의 중심에 두고, 도메인 객체가 데이터와 행위를 모두 가지도록 모델링하는 설계 방식입니다. 이 책에서는 그중 **Rich Domain Model** 측면(엔티티에 비즈니스 로직 캡슐화)에 집중합니다.
:::

:::term-box
**클린 아키텍처(Clean Architecture)란?** 비즈니스 규칙을 중심에 두고, 외부 기술(DB·웹 프레임워크 등)이 안쪽 규칙에 의존하도록 계층을 나누는 설계 방식입니다. 이 책에서는 컨트롤러가 **UseCase 인터페이스**에만 의존하도록 분리합니다.
:::

:::note
**챕터 2에서 단순화한 Order 모델(주문 1건에 상품 1개)은 이번 챕터에서도 그대로 가져갑니다.** 이 챕터의 초점은 **코드 구조와 운영 환경**이므로, 도메인은 챕터 2를 그대로 두고 패키지 분리·DB·배포만 진화시킵니다.
:::


## 3.2 UseCase - 왜 인터페이스인가

클린 아키텍처에서 컨트롤러는 구현체가 아닌 **UseCase 인터페이스**에 의존합니다. 구현체가 바뀌어도 컨트롤러는 수정할 필요가 없고, 테스트할 때도 가짜 구현체를 쉽게 넣을 수 있습니다.

<div class="svg-figure">
<svg viewBox="0 0 800 380" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="UseCase 인터페이스 - 전원 어댑터 비유: 두 가지 구현체 플러그가 한 어댑터를 거쳐 Controller에 연결되는 구조">
  <text x="400" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">UseCase 인터페이스 — 전원 어댑터 비유</text>
  <text x="160" y="105" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">구현체 A</text>
  <line x1="60" y1="145" x2="115" y2="145" stroke="#0f172a" stroke-width="1.6"/>
  <path d="M115 118 Q115 113 120 113 L185 113 Q190 113 190 118 L190 172 Q190 177 185 177 L120 177 Q115 177 115 172 Z" fill="#fff" stroke="#0f172a" stroke-width="1.6"/>
  <rect x="190" y="124" width="32" height="7" fill="#0f172a"/>
  <rect x="190" y="159" width="32" height="7" fill="#0f172a"/>
  <text x="160" y="235" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">구현체 B</text>
  <line x1="60" y1="275" x2="115" y2="275" stroke="#0f172a" stroke-width="1.6"/>
  <path d="M115 248 Q115 243 120 243 L185 243 Q190 243 190 248 L190 302 Q190 307 185 307 L120 307 Q115 307 115 302 Z" fill="#fff" stroke="#0f172a" stroke-width="1.6"/>
  <line x1="190" y1="265" x2="218" y2="265" stroke="#0f172a" stroke-width="3"/>
  <line x1="190" y1="285" x2="218" y2="285" stroke="#0f172a" stroke-width="3"/>
  <circle cx="222" cy="265" r="5" fill="#0f172a"/>
  <circle cx="222" cy="285" r="5" fill="#0f172a"/>
  <line x1="222" y1="145" x2="330" y2="185" stroke="#0f172a" stroke-width="1.4"/>
  <line x1="227" y1="275" x2="330" y2="225" stroke="#0f172a" stroke-width="1.4"/>
  <text x="400" y="105" text-anchor="middle" font-size="14" font-weight="700" fill="#3730a3">UseCase 인터페이스</text>
  <rect x="330" y="115" width="140" height="180" rx="10" fill="#fff" stroke="#4f46e5" stroke-width="2" stroke-dasharray="6,4"/>
  <path d="M390 145 Q400 142 410 145 Q420 149 420 158 Q420 167 410 170 Q400 173 390 170 Q380 167 380 158 Q380 149 390 145 Z" fill="#fff" stroke="#3730a3" stroke-width="1.4"/>
  <ellipse cx="395" cy="158" rx="4" ry="6" fill="#fff" stroke="#3730a3" stroke-width="1"/>
  <ellipse cx="405" cy="158" rx="4" ry="6" fill="#fff" stroke="#3730a3" stroke-width="1"/>
  <circle cx="395" cy="200" r="4" fill="#3730a3"/>
  <circle cx="405" cy="200" r="4" fill="#3730a3"/>
  <path d="M376 232 L390 240 L385 254 L371 246 Z" fill="#fff" stroke="#3730a3" stroke-width="1.4"/>
  <path d="M424 232 L410 240 L415 254 L429 246 Z" fill="#fff" stroke="#3730a3" stroke-width="1.4"/>
  <line x1="470" y1="205" x2="565" y2="205" stroke="#0f172a" stroke-width="1.4"/>
  <text x="650" y="105" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">Controller</text>
  <path d="M580 115 L720 115 L720 215 L580 215 Z" fill="#fff" stroke="#0f172a" stroke-width="1.6"/>
  <rect x="590" y="124" width="120" height="80" rx="2" fill="#fff" stroke="#0f172a" stroke-width="1"/>
  <circle cx="650" cy="120" r="1.5" fill="#0f172a"/>
  <path d="M565 215 L735 215 L725 245 L575 245 Z" fill="#fff" stroke="#0f172a" stroke-width="1.6"/>
  <rect x="638" y="226" width="24" height="6" rx="1" fill="#0f172a"/>
</svg>
</div>

*그림 3-1. UseCase 인터페이스 - 전원 어댑터 비유*

코드로 옮기면 이렇게 됩니다.

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
  <line x1="400" y1="330" x2="400" y2="395" stroke="#475569" stroke-width="1.6" marker-end="url(#c3f2-g)"/>
  <rect x="180" y="400" width="440" height="80" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="400" y="435" text-anchor="middle" font-size="14" font-weight="700" fill="#3730a3">OrderController</text>
  <text x="400" y="458" text-anchor="middle" font-size="12" fill="#3730a3">(구현체가 무엇인지 몰라도 된다)</text>
</svg>
</div>

*그림 3-2. UseCase 인터페이스 의존 구조*

**"무엇을 할 것인가"(UseCase 인터페이스)** 와 **"어떻게 할 것인가"(Service 구현체)** 를 분리하는 것이 핵심입니다.

### 3.2.1 챕터 2 vs 챕터 3 코드 비교

코드로 보면 차이가 더 명확합니다. 컨트롤러가 의존하는 대상이 구현체에서 인터페이스로 바뀝니다.

```java OrderController. 챕터 2 vs 챕터 3 의존 대상
// 2장: 구현체에 직접 의존
private final OrderService orderService;

// 3장: UseCase 인터페이스에 의존
private final CreateOrderUseCase createOrderUseCase;
private final GetOrderUseCase getOrderUseCase;
private final CancelOrderUseCase cancelOrderUseCase;
```


## 3.3 UseCase 인터페이스 + 도메인 캡슐화 도입

UseCase 인터페이스가 왜 필요한지 이해했으니, 이제 실제 코드에 적용해보겠습니다. 패키지 구조부터 바꾸겠습니다. 챕터 2의 단순 레이어드 구조에서 도메인 중심 구조로 전환합니다.

### 3.3.1 패키지 구조 변경

```text ex02/order/ 패키지 구조
ex02/order/src/main/java/com/metacoding/order/
├── domain/         # 엔티티 + 비즈니스 규칙 (Order·OrderStatus)
├── repository/     # Spring Data JPA
├── usecase/        # UseCase 인터페이스 + 서비스 구현체
├── web/            # 컨트롤러 + DTO
├── adapter/        # 외부 서비스 클라이언트 (order 전용)
└── core/           # JWT, 예외처리 (2장과 동일)
```

도메인이 가운데에 자리잡고, 외부(web·adapter·repository)가 그 주위에 맞춰지는 모양입니다.

:::note
**user/product/delivery도 동일한 구조이며, adapter/ 패키지만 order 전용입니다.**
:::

:::note
**이 책에서는 클린 아키텍처의 핵심인 UseCase 인터페이스를 통한 의존성 역전에 집중합니다.** 완전한 아키텍처보다는 실습에 필요한 개념만 적용합니다.
:::

### 3.3.2 UseCase 인터페이스 정의

주문 생성·조회·취소를 각각 별도 인터페이스로 표현합니다. 인터페이스 하나가 하나의 행위(Use Case)를 표현하도록 합니다.

```java usecase/. UseCase 인터페이스 3종
public interface CreateOrderUseCase {
    OrderResponse createOrder(int userId, int productId, int quantity, Long price, String address);
}

public interface GetOrderUseCase {
    OrderResponse findById(int orderId);
}

public interface CancelOrderUseCase {
    OrderResponse cancelOrder(int orderId);
}
```

### 3.3.3 엔티티의 비즈니스 로직 — DDD의 핵심

**"주문이 취소 가능한가?"** 같은 비즈니스 규칙은 서비스가 아닌 엔티티에 둡니다. 엔티티 메서드로 캡슐화하면 어디서 호출하든 동일한 규칙이 적용되고, 새 규칙(예: "30분 내 취소만 허용")이 들어와도 도메인 메서드만 손대면 됩니다.

```java domain/Order.java. validateCancelable 추가
public class Order {
    // 2장 Order.java 참조 — 필드 및 create(), complete(), cancel() 동일

    // 비즈니스 규칙을 엔티티에 위임 (3장에서 추가)
    public void validateCancelable() {
        if (this.status == OrderStatus.CANCELLED) {
            throw new Exception400("주문이 이미 취소되었습니다.");
        }
    }
}
```

### 3.3.4 OrderService - 인터페이스 구현

OrderService는 세 UseCase 인터페이스를 구현하고, 내부에서 도메인 객체의 비즈니스 메서드를 호출합니다. 이 구조를 통해 **서비스는 흐름 조율에만 집중**하고, **실제 비즈니스 규칙은 도메인이 담당**하도록 책임을 분리합니다.

보상 트랜잭션 로직은 챕터 2와 동일합니다. 달라진 점은 다음과 같습니다.

1. **UseCase 인터페이스 구현**. 서비스가 직접 메서드를 노출하지 않고, `CreateOrderUseCase` 등 인터페이스를 구현합니다.
2. **비즈니스 규칙을 엔티티에 위임**. 챕터 2에서 서비스의 `if`문으로 처리하던 검증(`validateQuantity`, `validatePrice` 등)을 도메인 객체의 메서드로 이동합니다.

```java usecase/OrderService.java. UseCase 인터페이스 구현
@Service
@Transactional(readOnly = true)                    // 1. 클래스 레벨 읽기 전용 트랜잭션
public class OrderService implements CreateOrderUseCase, GetOrderUseCase, CancelOrderUseCase {
    // 2. UseCase 인터페이스를 구현

    @Override
    @Transactional                                 // 쓰기 메서드만 오버라이드
    public OrderResponse cancelOrder(int orderId) {
        // ...
        findOrder.cancel();                        // 3. cancel() 내부에서 검증 후 취소
        // ...
    }
}
```

### 3.3.5 OrderController 수정

구현체가 아닌 인터페이스를 주입받도록 컨트롤러를 수정합니다. 앞으로 OrderService를 다른 구현체로 바꿔도 이 컨트롤러는 전혀 수정하지 않아도 됩니다. API는 챕터 2와 동일합니다(POST 생성, GET 조회, PUT 취소).

```java web/OrderController.java. UseCase 인터페이스 주입
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

### 3.3.6 나머지 서비스의 UseCase 적용

order-service와 동일한 패턴으로 나머지 세 서비스도 UseCase 인터페이스를 도입합니다. 비즈니스 규칙은 각 엔티티 메서드로 모입니다.

| 서비스 | UseCase 인터페이스 | 엔티티 검증 메서드 |
|---|---|---|
| **product** | GetProductUseCase, GetAllProductsUseCase, DecreaseQuantityUseCase, IncreaseQuantityUseCase | `validateQuantity()`, `validatePrice()` |
| **delivery** | SaveDeliveryUseCase, GetDeliveryUseCase, CancelDeliveryUseCase | `validateAddress()`, `validateCancelable()` |
| **user** | LoginUseCase, GetUserUseCase, GetAllUsersUseCase | `validatePassword()` |

챕터 2에서 Service의 `if`문으로 처리하던 검증 로직이 엔티티 메서드로 이동합니다.

안쪽이 정리됐습니다. 도메인이 자기 일을 알고, 컨트롤러는 약속만 압니다. 다음은 밖입니다.

**오픈이**: "이제 운영에 올려야겠죠? 그런데 4 서비스 포트가 흩어져 있어요. `:8081`·`:8082`·`:8083`·`:8084`. 사용자가 다 알아야 하나요?"

**선배**: "안은 정리했으니, 밖에서 들어오는 문도 하나로 모아요. Nginx 한 대가 받아서 URL 경로로 나눠주면 돼요."

## 3.4 MySQL - 운영 데이터베이스 연결과 프로파일 분리

운영 환경에서는 서비스가 재시작되더라도 데이터가 유지되어야 합니다. 실제 사용자 데이터는 서버가 꺼져도 남아있어야 합니다. H2는 메모리에만 저장되므로 운영에는 MySQL 같은 외부 데이터베이스를 사용합니다.

`application.properties`에서 개발(H2)과 운영(MySQL) 환경을 분리합니다.

```text src/main/resources/ 프로파일 분리
src/main/resources/
├── application.properties         # 공통 설정, active profile 지정
├── application-dev.properties     # 개발: H2 설정
└── application-prod.properties    # 운영: MySQL, 환경변수 참조
```

운영 프로파일은 환경변수를 참조합니다. `${DB_URL}`처럼 플레이스홀더를 사용하면 코드를 변경하지 않고 Kubernetes ConfigMap/Secret에서 환경 변수 값을 주입받을 수 있습니다.

```properties application-prod.properties. 운영 프로파일
# Database (환경변수에서 읽음)
spring.datasource.url=${DB_URL}
spring.datasource.username=${DB_USERNAME}
spring.datasource.password=${DB_PASSWORD}

# JPA / Hibernate
spring.jpa.hibernate.ddl-auto=${DDL_AUTO:validate}

# 생략...
```

MySQL을 사용하려면 build.gradle에 드라이버 의존성을 추가해야 합니다.

```gradle build.gradle. MySQL 드라이버 추가
dependencies {
    // 생략...
    runtimeOnly 'com.mysql:mysql-connector-j'   // 신규 추가
    // 생략...
}
```


## 3.5 Docker - Gateway와 MySQL 인프라 이미지

이번 챕터부터는 Docker 이미지를 Minikube 위에서 실행합니다. Minikube가 설치되어 있지 않다면 공식 사이트(https://minikube.sigs.k8s.io/)에서 설치 후 `minikube start` 명령어로 클러스터를 시작합니다.


### 3.5.1 Nginx - API Gateway 라우팅

챕터 2에서는 각 서비스 포트(8081~8084)로 직접 접근했습니다. 서비스가 늘어나면 클라이언트가 포트를 전부 알아야 하므로, 하나의 진입점으로 통합합니다. Nginx를 API Gateway로 두면, 클라이언트는 **하나의 진입점(80번 포트)** 으로 요청하고 URL 경로에 따라 적절한 서비스로 라우팅됩니다.

`gateway/` 디렉토리에는 Nginx Dockerfile과 nginx.conf 두 파일이 있습니다.

Dockerfile은 Nginx를 설치하고, 우리가 작성한 설정 파일을 넣어주는 역할입니다.

```dockerfile gateway/Dockerfile. Nginx 이미지 빌드
FROM nginx:alpine                          # 경량 Nginx 이미지
COPY nginx.conf /etc/nginx/nginx.conf      # 라우팅 설정 파일 복사
EXPOSE 80                                  # 게이트웨이 포트
CMD ["nginx", "-g", "daemon off;"]         # 포그라운드 실행
```

nginx.conf는 어떤 URL이 들어오면 어느 서비스로 보낼지를 정하는 설정 파일입니다.

```nginx gateway/nginx.conf. URL 경로별 라우팅
events {}

http {
    # 각 서비스를 upstream 블록으로 등록
    upstream user-service {
        server user-service:8083;      # K8s 내부 DNS로 서비스 접근
    }
    # product-service(8082), order-service(8081), delivery-service(8084)도 동일 패턴

    server {
        listen 80;                     # 게이트웨이 진입점
        server_name localhost;

        # URL 경로별로 요청을 해당 서비스로 분기
        location /login {
            proxy_pass http://user-service;
        }

        location /api/users {
            proxy_pass http://user-service;
        }
        # /api/products → product-service, /api/orders → order-service,
        # /api/deliveries → delivery-service도 동일 패턴
    }
}
```

`upstream` 블록에 4개 서비스를 등록하고, `location`으로 URL 경로를 분기합니다. `user-service`, `order-service` 같은 이름은 Kubernetes가 내부 DNS로 자동 해석하므로, IP 주소를 직접 지정할 필요가 없습니다.

### 3.5.2 MySQL - 데이터베이스 인프라

모든 서비스가 동일한 MySQL 인스턴스(`db-service:3306`)의 `metadb` 데이터베이스를 공유합니다. 서비스별로 테이블이 분리되어 있으나, 물리적으로는 단일 DB 인스턴스입니다.

:::note
**실제 MSA에서는 서비스마다 독립된 DB를 둡니다.** 이 책에서는 학습 편의를 위해 하나의 MySQL을 공유합니다. Saga 패턴을 익히는 데는 차이가 없으니 DB 구성보다 흐름에 집중해 주세요.
:::

DB 컨테이너는 `db/` 디렉토리의 Dockerfile과 init.sql로 구성됩니다.

```dockerfile db/Dockerfile. MySQL 이미지
FROM mysql                          # MySQL 공식 이미지
COPY init.sql /docker-entrypoint-initdb.d  # 컨테이너 최초 시작 시 자동 실행
CMD ["--character-set-server=utf8mb4", "--collation-server=utf8mb4_unicode_ci"]
```

루트 비밀번호·데이터베이스 이름·접속 계정 같은 민감 정보는 Dockerfile에 직접 박지 않고 K8s `db-secret.yml`에서 환경변수로 주입합니다. 같은 이미지를 환경(개발/운영)마다 다른 비밀로 띄울 수 있고, 비밀이 이미지 레이어에 남지 않습니다.

`init.sql`은 서비스별 테이블 생성과 더미 데이터 삽입을 담당합니다. 챕터 2의 H2 `data.sql`은 INSERT만 있었지만, MySQL은 자동으로 테이블을 만들어주지 않으므로 CREATE TABLE도 포함합니다. 4개 서비스의 4개 테이블(`user_tb`, `product_tb`, `order_tb`, `delivery_tb`)을 만들고 더미 데이터를 넣습니다.

*Docker Compose로 한 번에 띄우는 건 편한데, 서비스가 죽으면 내가 직접 다시 띄워야 한다.*

**선배**: "Kubernetes는 원하는 상태를 적어두면, 알아서 그 상태를 유지해줘요. 서비스가 죽으면 자동으로 다시 띄우고요."

## 3.6 Kubernetes - YAML로 선언하는 배포

### 3.6.1 매니페스트 구조 설계

Kubernetes는 YAML 파일로 원하는 상태를 선언합니다. **"이 서비스는 이렇게 실행되어야 한다"** 고 파일에 적어두면, K8s가 그 상태를 유지합니다.

`ConfigMap`과 `Secret`은 환경변수를 저장합니다. `Deployment`는 컨테이너를 어떻게 실행할지 정의합니다. `Service`는 `Pod`에 고정 주소(DNS)를 부여하여 클러스터 내부에서 접근할 수 있게 합니다. 외부 요청은 `Ingress`가 받아 적절한 Service로 전달합니다.

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

*그림 3-3. Kubernetes 리소스 관계*

서비스 종류에 따라 필요한 리소스 조합이 다릅니다. DB는 ConfigMap 없이 Secret만, 일반 서비스는 ConfigMap+Secret+Deployment+Service, 게이트웨이는 Ingress까지 추가됩니다.

각 K8s 리소스의 역할을 정리하면 다음과 같습니다.

| 리소스 | 파일 | 역할 | 주요 값 |
|---|---|---|---|
| ConfigMap | `order-configmap.yml` | 일반 환경변수 | `DB_URL` |
| Secret | `order-secret.yml` | 민감한 환경변수 | `DB_USERNAME`, `DB_PASSWORD` |
| Deployment | `order-deploy.yml` | Pod 실행 정의 | 이미지, 포트, `env`로 `SPRING_PROFILES_ACTIVE` 직접 설정, `envFrom`으로 ConfigMap·Secret 주입 |
| Service | `order-service.yml` | 클러스터 내부 통신 | Pod에 고정 DNS 부여 (`order-service:8081`) |
| Ingress | `gateway-ingress.yml` | 외부 요청 라우팅 | 모든 외부 요청을 `gateway-service:80`으로 전달 |

각 리소스가 실제로 어떻게 생겼는지, order 서비스를 예시로 하나씩 살펴보겠습니다.

### 3.6.2 ConfigMap - 일반 환경변수 주입

```yaml k8s/order/order-configmap.yml. 일반 환경변수
apiVersion: v1
kind: ConfigMap
metadata:
  name: order-configmap
  namespace: metacoding
data:                        # 키-값 쌍으로 환경변수 저장
  DB_URL: jdbc:mysql://db-service:3306/metadb?useSSL=false&serverTimezone=UTC&useLegacyDatetimeCode=false&allowPublicKeyRetrieval=true
```

ConfigMap은 애플리케이션이 필요로 하는 **일반 설정값을 외부에서 주입**하는 역할을 합니다. 코드를 수정하지 않고도 DB 주소 같은 설정을 바꿀 수 있습니다. JDBC 드라이버 클래스는 `spring-boot-starter-data-jpa`가 의존성에 들어 있는 MySQL 드라이버를 자동 선택하므로 별도로 주입하지 않습니다.

### 3.6.3 Secret - 민감한 정보 관리

```yaml k8s/order/order-secret.yml. 민감 환경변수
apiVersion: v1
kind: Secret
metadata:
  name: order-secret
  namespace: metacoding
stringData:                  # 평문으로 작성하면 K8s가 자동으로 Base64 인코딩
  DB_USERNAME: metacoding
  DB_PASSWORD: metacoding1234
```

Secret은 **비밀번호, 인증 정보 같은 민감한 값을 안전하게 관리**하는 역할을 합니다. ConfigMap과 구조는 비슷하지만, 노출되면 안 되는 값은 반드시 Secret으로 분리합니다. `stringData`는 Base64 인코딩이지 암호화가 아닙니다. Secret을 Git에 커밋하면 안 됩니다. 운영 환경에서는 Sealed Secrets, Vault 같은 도구를 검토하세요.

DB Pod는 ConfigMap이 따로 없고 Secret 하나에 모든 환경변수를 모아둡니다. MySQL 컨테이너는 `MYSQL_*` 환경변수를 인식하여 시작 시점에 자동으로 데이터베이스와 계정을 만듭니다.

```yaml k8s/db/db-secret.yml. DB 비밀번호·DB명·계정
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
  namespace: metacoding
stringData:
  MYSQL_ROOT_PASSWORD: root1234     # root 계정 비밀번호
  MYSQL_DATABASE: metadb            # 컨테이너 시작 시 자동 생성할 DB
  MYSQL_USER: metacoding            # 애플리케이션이 사용할 계정
  MYSQL_PASSWORD: metacoding1234    # 그 계정의 비밀번호
```

`order-secret.yml`의 `DB_USERNAME`/`DB_PASSWORD`는 여기서 만들어진 `metacoding` 계정과 같은 값을 가리킵니다. 학습 편의를 위해 평문으로 두지만, 실무에서는 Vault 같은 외부 비밀 저장소를 두고 양쪽이 같은 출처를 참조하도록 합니다.

### 3.6.4 Deployment - Pod 실행 정의

```yaml k8s/order/order-deploy.yml. Pod 실행 정의
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-deploy
  namespace: metacoding
spec:
  replicas: 1                # Pod를 몇 개 띄울지
  selector:
    matchLabels:
      app: order
  template:
    metadata:
      labels:
        app: order           # Service가 이 라벨로 Pod를 찾음
    spec:
      containers:
        - name: order-server
          image: metacoding/order:1
          ports:
            - containerPort: 8081
          env:                           # 개별 환경변수 직접 설정
            - name: SPRING_PROFILES_ACTIVE
              value: "prod"
          envFrom:                       # ConfigMap·Secret의 모든 값을 한꺼번에 주입
            - configMapRef:
                name: order-configmap
            - secretRef:
                name: order-secret
```

Deployment는 **컨테이너를 어떻게 실행할지 정의하고, Pod의 생명주기를 관리**하는 역할을 합니다. Pod가 죽으면 자동으로 다시 띄워주고, `replicas`를 늘리면 같은 Pod를 여러 개 실행할 수도 있습니다.

### 3.6.5 Service - 클러스터 내부 통신

```yaml k8s/order/order-service.yml. 클러스터 내부 통신
apiVersion: v1
kind: Service
metadata:
  name: order-service
  namespace: metacoding
spec:
  type: ClusterIP              # 클러스터 내부에서만 통신
  selector:
    app: order               # 이 라벨을 가진 Pod에 트래픽 전달
  ports:
    - port: 8081             # 다른 서비스가 접근하는 포트
```

Service는 **Pod에 고정 주소(DNS)를 부여**하는 역할을 합니다. Pod는 재시작될 때마다 IP가 바뀌지만, Service 덕분에 다른 서비스들은 항상 `order-service:8081`이라는 이름으로 접근할 수 있습니다.

### 3.6.6 Ingress - 외부 요청 라우팅

```yaml k8s/gateway/gateway-ingress.yml. 외부 요청 라우팅
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: gateway-ingress
  namespace: metacoding
spec:
  rules:
    - http:                  # host를 생략하면 모든 도메인의 요청을 받음
        paths:
          - path: /          # 모든 경로를 매칭
            pathType: Prefix
            backend:
              service:
                name: gateway-service
                port:
                  number: 80
```

Ingress는 **클러스터 외부에서 들어오는 요청을 내부 Service로 연결하는 출입구** 역할을 합니다. Service가 클러스터 내부의 주소록이라면, Ingress는 외부 세계와 클러스터를 연결하는 정문입니다.

나머지 서비스(product, user, delivery)도 동일한 패턴입니다.

## 3.7 Minikube - 실행 및 결과 확인

### 3.7.1 Minikube 시작

Minikube는 로컬 PC에 가벼운 Kubernetes 클러스터를 만들어주는 도구입니다. Docker Desktop이 실행 중인 상태에서 아래 명령을 입력하면 클러스터가 생성됩니다.

```bash [터미널] Minikube 시작
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

*그림 3-4. Minikube 시작*

처음 실행하면 필요한 이미지를 다운로드하므로 몇 분 정도 걸릴 수 있습니다.

### 3.7.2 이미지 빌드

`minikube image build`는 Minikube 내부에 직접 이미지를 빌드합니다.

```bash [터미널] 이미지 빌드
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

*그림 3-5. 이미지 빌드 결과*


### 3.7.3 배포 순서

네임스페이스를 먼저 생성하고, DB가 준비된 뒤에 나머지 서비스를 배포합니다.

```bash [터미널] 배포 순서
# 1. 네임스페이스 생성 (최초 1회)
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

*그림 3-6. 네임스페이스 생성 및 배포*


### 3.7.4 배포 상태 확인

```bash [터미널] Pod 상태 확인
kubectl get pods -n metacoding
```

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">kubectl get pods -n metacoding</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div class="tl-kv-row"><span class="tl-label">NAME</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-label">READY</span>&nbsp;&nbsp;<span class="tl-label">STATUS</span>&nbsp;&nbsp;&nbsp;<span class="tl-label">AGE</span></div>
    <div class="tl-kv-row">db-deploy-xxx&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">42s</span></div>
    <div class="tl-kv-row">gateway-deploy-xxx&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">38s</span></div>
    <div class="tl-kv-row">order-deploy-xxx&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">36s</span></div>
    <div class="tl-kv-row">product-deploy-xxx&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">35s</span></div>
    <div class="tl-kv-row">user-deploy-xxx&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">33s</span></div>
    <div class="tl-kv-row">delivery-deploy-xxx&nbsp;&nbsp;<span class="tl-num">1/1</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-val">Running</span>&nbsp;&nbsp;<span class="tl-num">30s</span></div>
    <div class="tl-divider"><span class="tl-val">모든 Pod Running</span><span class="tl-cursor"></span></div>
  </div>
</div>

*그림 3-7. Pod 상태 확인*

모든 Pod가 `Running` 상태가 되면 배포 완료입니다.

### 3.7.5 서비스 접근

Ingress를 통해 외부에서 접속하려면 `minikube tunnel`을 실행합니다.

```bash [터미널] 외부 접근 터널
minikube tunnel
```

`minikube tunnel`은 터미널을 점유합니다. 새 터미널을 열어서 이후 테스트를 진행하세요. 터널이 실행되면 `http://127.0.0.1:80`로 gateway-service에 접속할 수 있습니다. `POST http://127.0.0.1:80/login`으로 로그인하여 토큰을 받습니다. 이후 과정은 챕터 2와 동일하게 주문을 생성합니다.

![](assets/CH03/terminal/08_order-result.png)

*그림 3-8. 주문 결과 확인*

테스트가 끝났으면 이번 챕터에서 실행한 리소스를 정리합니다.

```bash [터미널] 리소스 정리
kubectl delete all --all -n metacoding
```

**오픈이**: "Kubernetes에서도 주문이 잘 되네요! 안은 도메인이 자기 일을 알고, 밖은 한 입구, 위에서는 K8s가 살려주고."

**선배**: "K8s가 Pod 죽으면 살려주죠. 그런데 product-service Pod이 살아나는 동안에는 어떻게 될 것 같아요?"

오픈이가 시도해 봤습니다. product-service Pod을 잠깐 내려본 30초 동안 **주문 요청이 그대로 멈춥니다.** K8s가 살려주는 시간 동안에도 order는 굳어 있습니다.

*분리한 의미가 없잖아.*

코드 구조도 좋아졌고, 운영 배포도 됐고, 도메인이 가운데에 자리잡았습니다. 그런데 아직 해결하지 못한 문제가 있습니다. product-service에 장애가 생기면 order-service도 그대로 멈춥니다. 동기 호출의 한계입니다.

:::remember
**이것만은 기억하자**

- **DDD (Rich Domain Model)**: 비즈니스 규칙을 도메인 객체에 캡슐화. `Order.validateCancelable()`·`Order.cancel()`로 도메인이 자기 일을 안다.
- **클린 아키텍처 (UseCase 인터페이스)**: 컨트롤러가 구현체가 아닌 약속에 의존. 환경별·테스트별 구현체 교체 가능.
- **Nginx API Gateway**: 4 서비스 진입점을 하나로 통합. URL 경로로 라우팅.
- **MySQL + 프로파일 분리**: 개발은 H2, 운영은 MySQL. 환경변수로 설정 주입.
- **Kubernetes 배포**: ConfigMap·Secret으로 환경변수 주입, Deployment로 Pod 자동 복구.

다음 챕터에서는 동기 호출의 한계를 정면으로 마주칩니다. Kafka로 서비스 간 전화를 끊고, 메시지를 사이에 두며, 중앙에 지휘자(orchestrator)를 둡니다. 한 서비스가 잠시 멈춰도 전체 시스템은 계속 동작합니다.
:::
