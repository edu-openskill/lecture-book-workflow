# 챕터 3. 클린 아키텍처와 Kubernetes 운영 환경

> 이 챕터의 전체 소스코드는 **https://github.com/metacoding-12-msa/ex02** 에서 확인할 수 있습니다.

:::goal
이번 챕터가 끝나면

- 컨트롤러가 서비스 구현체 대신 UseCase 인터페이스에 의존하도록 구조를 개선할 수 있습니다.
- MySQL을 연결하고 개발/운영 프로파일을 분리할 수 있습니다.
- Docker 이미지를 빌드하고 Kubernetes에 배포할 수 있습니다.
- ConfigMap과 Secret으로 환경 변수를 주입하는 방법을 이해할 수 있습니다.
:::

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

1. 챕터 2 코드를 클린 아키텍처(UseCase 인터페이스)로 재구성한 결과 살펴보기
2. 개발(H2) · 운영(MySQL) 프로파일 분리 확인
3. Nginx API Gateway + MySQL 인프라 Docker 이미지 살펴보기
4. K8s 매니페스트(ConfigMap·Secret·Deployment·Service·Ingress) 5종 살펴보기
5. Minikube에서 빌드·배포·실행

:::note
**이번 챕터는 직접 코드를 작성하지 않습니다.** 챕터 2 프로젝트를 클린 아키텍처로 재구성한 결과를 살펴보고, Kubernetes 배포를 실습합니다.
:::
::::

**오픈이**: "선배님, 동작은 하는데 코드가 좀 지저분해요. 서비스 교체하려면 컨트롤러까지 뜯어야 하고요."

**선배**: "구조를 정리하고, 제대로 된 운영 환경에도 올려야죠. 두 가지 숙제예요."

## 3.1 챕터 2가 남긴 두 가지 숙제

챕터 2에서 4개 서비스가 REST로 통신하는 시스템을 만들었습니다. 동작은 합니다. 하지만 실제 서비스로 운영하기에는 두 가지 문제가 있습니다.

**첫 번째 문제: 코드 구조**. OrderController는 OrderService에 직접 의존합니다. 콘센트와 가전을 어댑터 없이 직접 납땜한 상태와 같습니다. 나중에 OrderService를 교체하거나 가짜 데이터(Mock)로 바꿔 테스트하려면 Controller 코드도 건드려야 합니다. 서비스가 많아질수록 이 결합이 코드 전체를 딱딱하게 만듭니다.

**두 번째 문제: 운영 환경**. 챕터 2에서는 H2 인메모리 DB로 로컬에서만 실행했습니다. 내 노트북에서만 돌아가는 시스템이라, 노트북을 끄면 모든 게 사라집니다. 실제 운영에서는 MySQL 같은 영구 저장소를 사용하고, DB 접속 정보나 비밀키 같은 설정값을 코드가 아닌 외부에서 주입받아야 합니다.

이번 챕터는 이 두 숙제를 동시에 해결하는 이야기입니다. 코드 구조는 **클린 아키텍처(UseCase 인터페이스)** 로, 운영 환경은 **Kubernetes**로 해결합니다. 챕터 2의 Docker Compose는 서비스를 한 번에 띄우기엔 편합니다. 그러나 서비스가 죽으면 직접 다시 띄워야 하고, 특정 서비스만 늘리기도 어렵습니다. Kubernetes는 이런 부분을 자동으로 처리합니다.

:::note
**챕터 2에서 단순화한 Order 모델(주문 1건에 상품 1개)은 이번 챕터에서도 그대로 가져갑니다.** 이 챕터의 초점은 **코드 구조와 운영 환경**이므로, 도메인은 챕터 2를 그대로 두고 패키지 분리·DB·배포만 진화시킵니다.
:::

:::term-box
**클린 아키텍처(Clean Architecture)란?** 비즈니스 규칙을 중심에 두고, 외부 기술(DB, 웹 프레임워크 등)이 안쪽 규칙에 의존하도록 계층을 나누는 소프트웨어 설계 방식입니다.
:::


## 3.2 UseCase - 왜 인터페이스인가

클린 아키텍처에서 컨트롤러는 구현체가 아닌 **UseCase 인터페이스**에 의존합니다. 구현체가 바뀌어도 컨트롤러는 수정할 필요가 없고, 테스트할 때도 가짜 구현체를 쉽게 넣을 수 있습니다.

<!-- image-prompt: Minimal black line drawing on white background, icon-like simplicity, 4:3 aspect ratio, 800x600px. A universal power adapter analogy. Left side: two different plug types (US and EU style) labeled "구현체 A", "구현체 B". Center: a universal adapter socket labeled "UseCase 인터페이스". Right side: a laptop labeled "Controller". The adapter connects different plugs to the same device. Shows the concept of interface abstraction. -->
![](assets/CH03/gemini/01_power-adapter.png)
*그림 3-1. UseCase 인터페이스 - 전원 어댑터 비유*

코드로 옮기면 이렇게 됩니다.

<!-- image-prompt: Minimal black line drawing on white background, 4:3 aspect ratio, 800x600px. Top row: three boxes side by side — "OrderServiceV1 (H2 개발용)", "OrderServiceV2 (MySQL 운영용)", "MockOrderService (테스트용)". All three have downward arrows pointing to a single center box in the middle row: "CreateOrderUseCase (약속: '주문을 생성한다')" with a dashed border to indicate it is an interface. Below that, one downward arrow to a bottom box: "OrderController (구현체가 무엇인지 몰라도 된다)". Layout is vertically centered, three-tier: implementations on top, interface in middle, controller at bottom. Clean lines, no fill, no colors. -->
![](assets/CH03/gemini/02_usecase-deps.png)
*그림 3-2. 챕터 2 vs 챕터 3 의존 구조 비교*

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


## 3.3 UseCase 인터페이스 도입

UseCase 인터페이스가 왜 필요한지 이해했으니, 이제 실제 코드에 적용해보겠습니다. 패키지 구조부터 바꾸겠습니다. 챕터 2의 단순 레이어드 구조에서 클린 아키텍처 구조로 전환합니다.

### 3.3.1 패키지 구조 변경

```text ex02/order/ 패키지 구조
ex02/order/src/main/java/com/metacoding/order/
├── domain/                              # JPA 엔티티
│   ├── Order.java                       # [참고]
│   └── OrderStatus.java                 # [참고]
├── repository/                          # Spring Data JPA
│   └── OrderRepository.java             # [참고]
├── usecase/                             # UseCase 인터페이스 + 서비스 구현체
│   ├── CreateOrderUseCase.java          # [참고]
│   ├── GetOrderUseCase.java             # [참고]
│   ├── CancelOrderUseCase.java          # [참고]
│   └── OrderService.java               # [참고]
├── web/                                 # 컨트롤러 + DTO
│   ├── OrderController.java             # [참고]
│   └── dto/
│       ├── OrderRequest.java            # [참고]
│       └── OrderResponse.java           # [참고]
├── adapter/                             # 외부 서비스 클라이언트 (order 전용)
│   ├── ProductClient.java              # [참고] 2장과 동일
│   ├── DeliveryClient.java             # [참고] 2장과 동일
│   └── dto/                            # 어댑터용 DTO
│       ├── ProductRequest.java         # [참고]
│       └── DeliveryRequest.java        # [참고]
└── core/                                # JWT, 예외처리 (2장과 동일)
```

:::note
**user/product/delivery도 동일한 구조이며, adapter/ 패키지만 order 전용입니다.**
:::

:::note
**이 책에서는 클린 아키텍처의 핵심인 UseCase 인터페이스를 통한 의존성 역전에 집중합니다.** 완전한 아키텍처보다는 실습에 필요한 개념만 적용합니다.
:::

### 3.3.2 UseCase 인터페이스 정의

주문 생성·조회·취소를 각각 별도 인터페이스로 표현합니다. 각 인터페이스는 메서드 하나만 가집니다. 그림 3-1의 어댑터 비유로 돌아오면, 각 `UseCase` 인터페이스는 콘센트 모양 하나하나이고, `OrderService`는 거기에 꽂히는 플러그입니다.

| UseCase | 메서드 | 역할 |
|---|---|---|
| `CreateOrderUseCase` | `createOrder` | 주문 생성 |
| `GetOrderUseCase` | `findById` | 주문 조회 |
| `CancelOrderUseCase` | `cancelOrder` | 주문 취소 |

모두 `OrderResponse`를 반환합니다. 전체 인터페이스 정의는 GitHub `ex02/order/.../usecase/` 참조.

### 3.3.3 엔티티의 비즈니스 로직

**"주문이 취소 가능한가?"** 같은 비즈니스 규칙은 서비스가 아닌 엔티티에 둡니다. 엔티티 메서드로 캡슐화하면 어디서 호출하든 동일한 규칙이 적용됩니다.

```java domain/Order.java. validateCancelable (Order 클래스에 메서드 추가)
// Order 클래스 외피·필드·create()·complete()·cancel() 생략 — 2장과 동일

public void validateCancelable() {
    if (this.status == OrderStatus.CANCELLED) {
        throw new Exception400("주문이 이미 취소되었습니다.");
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
@Transactional(readOnly = true)
public class OrderService implements CreateOrderUseCase, GetOrderUseCase, CancelOrderUseCase {

    @Override
    @Transactional
    public OrderResponse cancelOrder(int orderId) {
        // ... findOrder.cancel() 내부에서 검증 후 취소 ...
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
    private final CreateOrderUseCase createOrderUseCase;
    private final GetOrderUseCase getOrderUseCase;
    private final CancelOrderUseCase cancelOrderUseCase;

    @PostMapping
    public ResponseEntity<?> createOrder(...) {
        return Resp.ok(createOrderUseCase.createOrder(...));
    }

    // @GetMapping("/{orderId}") — 동일 패턴, 생략
    // @PutMapping("/{orderId}") — 동일 패턴, 생략
}
```

### 3.3.6 나머지 서비스의 UseCase 적용

order-service와 동일한 패턴으로 나머지 세 서비스도 UseCase 인터페이스를 도입합니다.

| 서비스 | UseCase 인터페이스 | 엔티티 검증 메서드 |
|---|---|---|
| **product** | GetProductUseCase, GetAllProductsUseCase, DecreaseQuantityUseCase, IncreaseQuantityUseCase | `validateQuantity()`, `validatePrice()` |
| **delivery** | SaveDeliveryUseCase, GetDeliveryUseCase, CancelDeliveryUseCase | `validateAddress()`, `validateCancelable()` |
| **user** | LoginUseCase, GetUserUseCase, GetAllUsersUseCase | `validatePassword()` |

챕터 2에서 Service의 `if`문으로 처리하던 검증 로직이 엔티티 메서드로 이동합니다.


첫 번째 숙제(코드 구조)를 해결했습니다. 이제 두 번째 숙제, 운영 환경 배포를 해결할 차례입니다.

**오픈이**: "구조가 깔끔해졌는데, H2는 서버 끄면 데이터가 날아가잖아요."

**선배**: "운영에서는 MySQL 쓰고, DB 접속 정보는 코드 밖에서 넣어줘야 해요. 프로파일로 분리하면 돼요."

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

MySQL을 사용하려면 `build.gradle` 의존성에 `mysql-connector-j`를 추가합니다.


## 3.5 Docker - 이미지 빌드와 인프라 구성

이번 챕터부터는 Docker 이미지를 Minikube 위에서 실행합니다. Minikube가 설치되어 있지 않다면 공식 사이트(https://minikube.sigs.k8s.io/)에서 설치 후 `minikube start` 명령어로 클러스터를 시작합니다. 


### 3.5.1 Nginx - API Gateway 라우팅

챕터 2에서는 각 서비스 포트(8081~8084)로 직접 접근했습니다. 서비스가 늘어나면 클라이언트가 포트를 전부 알아야 하므로, 하나의 진입점으로 통합합니다. Nginx를 API Gateway로 두면, 클라이언트는 **하나의 진입점(80번 포트)** 으로 요청하고 URL 경로에 따라 적절한 서비스로 라우팅됩니다. 챕터 1의 개별 상점 비유로 돌아오면, 매장마다 다른 주소를 외울 필요 없이 안내데스크 하나에 물어보면 알맞은 매장으로 안내해주는 셈입니다.

```text gateway/ 디렉토리
gateway/
├── Dockerfile        # Nginx 이미지 빌드 [참고]
└── nginx.conf        # URL 경로별 라우팅 설정 [참고]
```

Dockerfile은 경량 `nginx:alpine` 이미지에 우리가 작성한 `nginx.conf`를 복사해 80 포트로 띄우는 표준 패턴입니다. 자세한 내용은 GitHub `ex02/gateway/Dockerfile` 참조.

nginx.conf는 URL 경로별로 어느 서비스로 보낼지 결정합니다. 라우팅 규칙은 다음과 같습니다.

| URL 경로 | 라우팅 대상 |
|---|---|
| `/login` | user-service:8083 |
| `/api/users` | user-service:8083 |
| `/api/products` | product-service:8082 |
| `/api/orders` | order-service:8081 |
| `/api/deliveries` | delivery-service:8084 |

`user-service`, `order-service` 같은 이름은 Kubernetes가 내부 DNS로 자동 해석하므로 IP 주소를 직접 지정할 필요가 없습니다. 전체 nginx 설정은 GitHub `ex02/gateway/nginx.conf` 참조.

### 3.5.2 MySQL - 데이터베이스 인프라

모든 서비스가 동일한 MySQL 인스턴스(`db-service:3306`)의 `metadb` 데이터베이스를 공유합니다. 서비스별로 테이블이 분리되어 있으나, 물리적으로는 단일 DB 인스턴스입니다.

:::note
**실제 MSA에서는 서비스마다 독립된 DB를 둡니다.** 이 책에서는 학습 편의를 위해 하나의 MySQL을 공유합니다. Saga 패턴을 익히는 데는 차이가 없으니 DB 구성보다 흐름에 집중해 주세요.
:::

DB 컨테이너는 `db/` 디렉토리의 Dockerfile과 init.sql로 구성됩니다.

```text db/ 디렉토리
db/
├── Dockerfile   # [참고] MySQL 이미지 빌드
└── init.sql     # [참고] 테이블 생성 + 더미 데이터
```

MySQL 공식 이미지에 `init.sql`을 `docker-entrypoint-initdb.d`에 복사해 자동 실행시키는 표준 패턴입니다. 자세한 내용은 GitHub `ex02/db/Dockerfile` 참조.

루트 비밀번호·데이터베이스 이름·접속 계정 같은 민감 정보는 Dockerfile에 직접 박지 않고 K8s `db-secret.yml`에서 환경변수로 주입합니다. 같은 이미지를 환경(개발/운영)마다 다른 비밀로 띄울 수 있고, 비밀이 이미지 레이어에 남지 않습니다.

`init.sql`은 서비스별 테이블 생성과 더미 데이터 삽입을 담당합니다. 챕터 2의 H2 `data.sql`은 INSERT만 있었지만, MySQL은 자동으로 테이블을 만들어주지 않으므로 CREATE TABLE도 포함합니다. 챕터 2에서 Order 모델을 단일 상품으로 단순화했으므로 테이블도 4개입니다.

| 테이블 | 핵심 필드 |
|---|---|
| `user_tb` | id, username(UNIQUE), email, password, roles |
| `product_tb` | id, product_name, quantity, price |
| `order_tb` | id, user_id, product_id, quantity, price, status |
| `delivery_tb` | id, order_id, address, status |

더미 데이터는 2장과 동일합니다. 전체 SQL은 GitHub `ex02/db/init.sql` 참조.

*Docker Compose로 한 번에 띄우는 건 편한데, 서비스가 죽으면 내가 직접 다시 띄워야 한다.*

**선배**: "Kubernetes는 원하는 상태를 적어두면, 알아서 그 상태를 유지해줘요. 서비스가 죽으면 자동으로 다시 띄우고요."

## 3.6 Kubernetes - YAML로 선언하는 배포

:::note
**5종 매니페스트(ConfigMap·Secret·Deployment·Service·Ingress)의 개념은 도커&쿠버네티스 책 5장에서 다뤘습니다.** 여기서는 이 책의 시스템(MSA 4서비스 + Gateway + DB)에 어떻게 적용되는지 매니페스트 위주로 살펴봅니다.
:::

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
  <rect x="570" y="100" width="120" height="50" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <text x="630" y="122" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">Pod 1</text>
  <text x="630" y="138" text-anchor="middle" font-size="10" fill="#7b341e">컨테이너 실행</text>
  <rect x="570" y="180" width="120" height="50" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <text x="630" y="202" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">Pod 2</text>
  <text x="630" y="218" text-anchor="middle" font-size="10" fill="#7b341e">컨테이너 실행</text>
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

```text ex02/k8s/ 디렉토리
ex02/k8s/
├── db/
│   ├── db-deployment.yml     # [참고] MySQL Pod
│   ├── db-secret.yml         # [참고] DB 비밀번호·DB명·계정
│   └── db-service.yml        # [참고] MySQL 서비스 (ClusterIP)
├── order/
│   ├── order-configmap.yml   # [참고] 일반 환경 변수
│   ├── order-deploy.yml      # [참고] order-service Pod
│   ├── order-secret.yml      # [참고] 민감 정보
│   └── order-service.yml     # [참고] 서비스 노출
├── gateway/
│   ├── gateway-deploy.yml    # [참고] gateway Pod
│   ├── gateway-service.yml   # [참고] 서비스 노출
│   └── gateway-ingress.yml   # [참고] 외부 요청 라우팅
└── product/ user/ delivery/  # order와 동일 패턴
```

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

`order-secret.yml`의 `DB_USERNAME`/`DB_PASSWORD`는 여기서 만들어진 `metacoding` 계정과 같은 값을 가리킵니다. 즉, 같은 비밀이 양쪽에 적혀 있는 셈입니다. 학습 편의를 위해 평문으로 두지만, 실무에서는 Vault 같은 외부 비밀 저장소를 두고 양쪽이 같은 출처를 참조하도록 합니다.

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

*매니페스트 5종으로 4개 서비스가 K8s 위에서 돌아가는 구조가 다 그려졌다.*

**오픈이**: "이거 다 적용하면 클러스터에 다 뜨는 거죠?"

**선배**: "네, 이제 Minikube 띄우고 적용해 봐요."

## 3.7 Minikube - 실행 및 결과 확인

### 3.7.1 Minikube 시작

Minikube는 로컬 PC에 가벼운 Kubernetes 클러스터를 만들어주는 도구입니다. Docker Desktop이 실행 중인 상태에서 아래 명령을 입력하면 클러스터가 생성됩니다.

```bash [터미널] Minikube 시작
minikube start
```
<!-- terminal-prompt: Terminal showing "minikube start" command. Output includes downloading Kubernetes components, creating Docker container, configuring kubectl. Final message: "Done! kubectl is now configured to use minikube cluster and default namespace by default". -->
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
<!-- terminal-prompt: Terminal showing "minikube image build" commands for 6 services (db, order, product, user, delivery, gateway). Each build shows Gradle compilation output and "Successfully tagged metacoding/[service]:1" messages. -->
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

# 4. Ingress Controller 활성화 (도커&쿠버네티스 5.2.3 참조)
minikube addons enable ingress
```

<!-- terminal-prompt: Terminal showing kubectl commands. "namespace/metacoding created", then multiple "configmap/created", "secret/created", "deployment.apps/created", "service/created" messages for db, order, product, user, delivery, and gateway resources. -->
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

<!-- terminal-prompt: Terminal showing "kubectl get pods -n metacoding" output. Table with columns NAME, READY, STATUS, RESTARTS, AGE. All pods (db-deploy, order-deploy, product-deploy, user-deploy, delivery-deploy, gateway-deploy) showing STATUS "Running" and READY "1/1". -->
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


모든 Pod가 `Running` 상태가 되면 배포 완료입니다. 지금 클러스터 안에 떠 있는 모양을 한 장으로 정리하면 아래와 같습니다.

<div class="svg-figure">
<svg viewBox="0 0 1080 580" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="챕터 3 통합 토폴로지: 외부 Host에서 Ingress와 gateway-service(Nginx)를 거쳐 4개 서비스로 분기하고, 4개 서비스가 공유 MySQL을 사용하는 구조">
  <defs>
    <marker id="ch03topo-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#1f2937"/></marker>
  </defs>
  <text x="540" y="28" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">챕터 3 전체 구조 — Ingress · API Gateway · 4개 서비스 · 공유 MySQL</text>
  <rect x="30" y="250" width="120" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="90" y="278" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Host</text>
  <text x="90" y="296" text-anchor="middle" font-size="10" fill="#6b7280">브라우저·Hoppscotch</text>
  <line x1="150" y1="280" x2="218" y2="135" stroke="#1f2937" stroke-width="1.4" marker-end="url(#ch03topo-a)"/>
  <text x="178" y="200" text-anchor="middle" font-size="10" font-style="italic" fill="#475569">minikube tunnel</text>
  <rect x="200" y="60" width="850" height="500" rx="12" fill="none" stroke="#475569" stroke-width="1.4" stroke-dasharray="6,4"/>
  <text x="220" y="80" font-size="11" font-style="italic" font-weight="700" fill="#475569">쿠버네티스 클러스터 · 네임스페이스 metacoding</text>
  <rect x="540" y="100" width="170" height="50" rx="8" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <text x="625" y="122" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">Ingress</text>
  <text x="625" y="138" text-anchor="middle" font-size="10" fill="#7b341e">gateway-ingress</text>
  <line x1="625" y1="150" x2="625" y2="186" stroke="#1f2937" stroke-width="1.6" marker-end="url(#ch03topo-a)"/>
  <rect x="490" y="190" width="270" height="70" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="625" y="216" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">gateway-service (Nginx)</text>
  <text x="625" y="234" text-anchor="middle" font-size="10" fill="#7b341e">API Gateway · :80</text>
  <text x="625" y="250" text-anchor="middle" font-size="9" font-family="monospace" fill="#9a3412">/login · /api/users · /api/products · /api/orders · /api/deliveries</text>
  <line x1="555" y1="260" x2="320" y2="316" stroke="#1f2937" stroke-width="1.2" marker-end="url(#ch03topo-a)"/>
  <line x1="600" y1="260" x2="490" y2="316" stroke="#1f2937" stroke-width="1.2" marker-end="url(#ch03topo-a)"/>
  <line x1="650" y1="260" x2="760" y2="316" stroke="#1f2937" stroke-width="1.2" marker-end="url(#ch03topo-a)"/>
  <line x1="695" y1="260" x2="930" y2="316" stroke="#1f2937" stroke-width="1.2" marker-end="url(#ch03topo-a)"/>
  <rect x="240" y="320" width="160" height="100" rx="8" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="320" y="343" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">user-service</text>
  <text x="320" y="360" text-anchor="middle" font-size="10" font-family="monospace" fill="#9a3412">:8083 · ClusterIP</text>
  <line x1="260" y1="370" x2="380" y2="370" stroke="#fed7aa" stroke-width="1"/>
  <rect x="270" y="378" width="100" height="32" rx="16" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="320" y="399" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">user-pod</text>
  <rect x="410" y="320" width="160" height="100" rx="8" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="490" y="343" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">product-service</text>
  <text x="490" y="360" text-anchor="middle" font-size="10" font-family="monospace" fill="#9a3412">:8082 · ClusterIP</text>
  <line x1="430" y1="370" x2="550" y2="370" stroke="#fed7aa" stroke-width="1"/>
  <rect x="440" y="378" width="100" height="32" rx="16" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="490" y="399" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">product-pod</text>
  <rect x="680" y="320" width="160" height="100" rx="8" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="760" y="343" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">order-service</text>
  <text x="760" y="360" text-anchor="middle" font-size="10" font-family="monospace" fill="#9a3412">:8081 · ClusterIP</text>
  <line x1="700" y1="370" x2="820" y2="370" stroke="#fed7aa" stroke-width="1"/>
  <rect x="710" y="378" width="100" height="32" rx="16" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="760" y="399" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">order-pod</text>
  <rect x="850" y="320" width="160" height="100" rx="8" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="930" y="343" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">delivery-service</text>
  <text x="930" y="360" text-anchor="middle" font-size="10" font-family="monospace" fill="#9a3412">:8084 · ClusterIP</text>
  <line x1="870" y1="370" x2="990" y2="370" stroke="#fed7aa" stroke-width="1"/>
  <rect x="880" y="378" width="100" height="32" rx="16" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="930" y="399" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">delivery-pod</text>
  <line x1="320" y1="420" x2="600" y2="466" stroke="#1f2937" stroke-width="1.1" stroke-dasharray="4,3" marker-end="url(#ch03topo-a)"/>
  <line x1="490" y1="420" x2="620" y2="466" stroke="#1f2937" stroke-width="1.1" stroke-dasharray="4,3" marker-end="url(#ch03topo-a)"/>
  <line x1="760" y1="420" x2="640" y2="466" stroke="#1f2937" stroke-width="1.1" stroke-dasharray="4,3" marker-end="url(#ch03topo-a)"/>
  <line x1="930" y1="420" x2="660" y2="466" stroke="#1f2937" stroke-width="1.1" stroke-dasharray="4,3" marker-end="url(#ch03topo-a)"/>
  <rect x="500" y="470" width="280" height="70" rx="8" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="640" y="494" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">db-service (MySQL)</text>
  <text x="640" y="513" text-anchor="middle" font-size="10" font-family="monospace" fill="#9a3412">:3306 · 4개 서비스가 metadb를 공유</text>
  <text x="640" y="531" text-anchor="middle" font-size="9" fill="#9a3412">학습 편의용 단일 인스턴스</text>
</svg>
</div>
*그림 3-8. 챕터 3 통합 토폴로지 - Host에서 Pod까지의 전체 경로*

외부에서 들어온 요청은 Ingress에서 받아 gateway-service(Nginx)로 전달되고, Nginx의 URL 경로 규칙에 따라 4개의 ClusterIP 서비스 중 하나로 분기됩니다. 각 서비스 뒤에는 Pod 한 개씩이 매달려 있고, 4개 Pod 모두 같은 MySQL 인스턴스의 `metadb`를 공유합니다.

### 3.7.5 서비스 접근

Ingress를 통해 외부에서 접속하려면 `minikube tunnel`을 실행합니다.

```bash [터미널] 외부 접근 터널
minikube tunnel
```

`minikube tunnel`은 터미널을 점유합니다. 새 터미널을 열어서 이후 테스트를 진행하세요. 터널이 실행되면 `http://127.0.0.1:80`로 gateway-service에 접속할 수 있습니다. `POST http://127.0.0.1:80/login`으로 로그인하여 토큰을 받습니다. 이후 과정은 챕터 2와 동일하게 주문을 생성합니다.

<!-- terminal-prompt: Hoppscotch showing POST request to the minikube gateway URL with /api/orders path. Bearer token set. JSON body with productId:1, quantity:1, price:2500000, address:"Addr 4". Response 200 OK with order status "COMPLETED". -->
![](assets/CH03/terminal/08_order-result.png)
*그림 3-9. 주문 결과 확인*



테스트가 끝났으면 이번 챕터에서 실행한 리소스를 정리합니다.

```bash [터미널] 리소스 정리
kubectl delete all --all -n metacoding
```

**오픈이**: "Kubernetes에서도 주문이 잘 되네요!"

**선배**: "그런데 product-service가 잠깐 다운되면 어떻게 될 것 같아요?"

*하나가 죽으면 나머지도 같이 멈추는 건... 아직 안 풀렸다.*

코드 구조도 좋아졌고, 운영 배포도 됩니다. 그런데 아직 해결하지 못한 문제가 있습니다. product-service에 장애가 생기면 order-service도 그대로 멈춥니다. 동기 호출의 한계입니다. 한 서비스의 문제가 연쇄적으로 다른 서비스에 영향을 줍니다.

:::remember
**이것만은 기억하자**

- **Clean Architecture**: 컨트롤러가 UseCase 인터페이스에만 의존하도록 구조를 분리했습니다. 구현체를 교체해도 컨트롤러는 변경이 없습니다.
- **MySQL + 프로파일 분리**: 개발 환경은 H2, 운영 환경은 MySQL을 사용합니다. 환경변수로 설정을 주입하여 코드 변경 없이 환경을 전환합니다.
- **Nginx API Gateway**: 클라이언트는 게이트웨이 하나로 요청하고, URL 경로에 따라 각 서비스로 라우팅됩니다.
- **Kubernetes 배포**: ConfigMap/Secret으로 환경변수를 안전하게 주입하고, Deployment/Service로 Pod를 관리합니다.

다음 챕터에서는 Kafka로 서비스 간 통신을 비동기로 전환합니다. 서비스끼리 직접 연결하는 대신 메시지 큐를 사이에 둡니다. 한 서비스가 느려지거나 잠깐 멈춰도 전체 시스템은 계속 동작합니다.
:::
