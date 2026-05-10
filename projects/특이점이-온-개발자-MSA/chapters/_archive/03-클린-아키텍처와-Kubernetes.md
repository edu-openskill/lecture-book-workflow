# 챕터 3. 클린 아키텍처와 Kubernetes 운영 환경

> `chap02` · 실행 환경: 컨테이너 · UseCase 인터페이스 · MySQL · K8s
> 이 챕터의 전체 소스코드는 **https://github.com/metacoding-12-msa/chap02** 에서 확인할 수 있습니다.
> 이번 챕터는 직접 코드를 작성하지 않습니다. 챕터 2 프로젝트를 클린 아키텍처로 재구성한 결과를 살펴보고, Kubernetes 배포를 실습합니다.


> 이 챕터를 시작하기 전에 Docker Desktop이 실행 중이어야 하고, Minikube가 설치되어 있어야 합니다. Minikube 설치: https://minikube.sigs.k8s.io/

### 학습 목표

- 컨트롤러가 서비스 구현체 대신 UseCase 인터페이스에 의존하도록 구조를 개선한다.
- MySQL을 연결하고 개발/운영 프로파일을 분리한다.
- Docker 이미지를 빌드하고 Kubernetes에 배포한다.
- ConfigMap과 Secret으로 환경 변수를 주입하는 방법을 이해한다.


## 3.1 챕터 2가 남긴 두 가지 숙제

챕터 2에서 4개 서비스가 REST로 통신하는 시스템을 만들었습니다. 동작은 합니다. 하지만 실제 서비스로 운영하기에는 두 가지 문제가 있습니다.

**첫 번째 문제: 코드 구조**. OrderController는 OrderService에 직접 의존합니다. 나중에 OrderService를 교체하거나 가짜 데이터(Mock)로 바꿔 테스트하려면 Controller 코드도 건드려야 합니다. 서비스가 많아질수록 이 결합이 코드 전체를 딱딱하게 만듭니다.

**두 번째 문제: 운영 환경**. 챕터 2에서는 H2 인메모리 DB로 로컬에서만 실행했습니다. 실제 운영에서는 MySQL 같은 영구 저장소를 사용하고, DB 접속 정보나 비밀키 같은 설정값을 코드가 아닌 외부에서 주입받아야 합니다.

이번 챕터는 이 두 숙제를 동시에 해결하는 이야기입니다. 코드 구조는 **클린 아키텍처(UseCase 인터페이스)** 로, 운영 환경은 **Kubernetes**로 해결합니다. 챕터 2의 Docker Compose는 서비스를 한 번에 띄우기엔 편하지만, 서비스가 죽으면 직접 다시 띄워야 하고 특정 서비스만 늘리기도 어렵습니다. Kubernetes는 이런 부분을 자동으로 처리합니다.

> **클린 아키텍처(Clean Architecture)**: 비즈니스 규칙을 중심에 두고, 외부 기술(DB, 웹 프레임워크 등)이 안쪽 규칙에 의존하도록 계층을 나누는 소프트웨어 설계 방식입니다.


## 3.2 UseCase : 왜 인터페이스인가

클린 아키텍처에서 컨트롤러는 구현체가 아닌 **UseCase 인터페이스**에 의존합니다. 구현체가 바뀌어도 컨트롤러는 수정할 필요가 없고, 테스트할 때도 가짜 구현체를 쉽게 넣을 수 있습니다.

<!-- image-prompt: Minimal black line drawing on white background, icon-like simplicity, 4:3 aspect ratio, 800x600px. A universal power adapter analogy. Left side: two different plug types (US and EU style) labeled "구현체 A", "구현체 B". Center: a universal adapter socket labeled "UseCase 인터페이스". Right side: a laptop labeled "Controller". The adapter connects different plugs to the same device. Shows the concept of interface abstraction. -->
![전원 어댑터](images/chap03-1.png)
*그림 3-1: UseCase 인터페이스 — 전원 어댑터 비유*

코드로 옮기면 이렇게 됩니다.

<!-- image-prompt: Minimal black line drawing on white background, 4:3 aspect ratio, 800x600px. Top row: three boxes side by side — "OrderServiceV1 (H2 개발용)", "OrderServiceV2 (MySQL 운영용)", "MockOrderService (테스트용)". All three have downward arrows pointing to a single center box in the middle row: "CreateOrderUseCase (약속: '주문을 생성한다')" with a dashed border to indicate it is an interface. Below that, one downward arrow to a bottom box: "OrderController (구현체가 무엇인지 몰라도 된다)". Layout is vertically centered, three-tier: implementations on top, interface in middle, controller at bottom. Clean lines, no fill, no colors. -->
![유즈케이스](images/chap03-2.png)
*그림 3-2: 챕터 2 vs 챕터 3 의존 구조 비교*

```
[2장 구조 - 직접 의존]

OrderController ──────▶ OrderService (구현체)

문제: OrderService 구현체가 변경되면 OrderController도 영향을 받을 수 있다.


[3장 구조 - 인터페이스 의존]

OrderController ──────▶ CreateOrderUseCase (인터페이스)
                                 ▲
                          OrderService (구현체)

장점: OrderController는 인터페이스만 알면 된다.
     구현체를 교체해도 컨트롤러 코드는 변경이 없다.
```

**"무엇을 할 것인가"(UseCase 인터페이스)** 와 **"어떻게 할 것인가"(Service 구현체)** 를 분리하는 것이 핵심입니다.

### 3.2.1 챕터 2 vs 챕터 3 코드 비교

코드로 보면 차이가 더 명확합니다. 컨트롤러가 의존하는 대상이 구현체에서 인터페이스로 바뀝니다.

```java
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

```
chap02/order/src/main/java/com/metacoding/order/
├── domain/                              # JPA 엔티티
│   ├── Order.java                       # [참고]
│   ├── OrderItem.java                   # [참고]
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

> user/product/delivery도 동일한 구조이며, adapter/ 패키지만 order 전용입니다.

> **참고**: 이 책에서는 클린 아키텍처의 핵심인 UseCase 인터페이스를 통한 의존성 역전에 집중합니다. 완전한 아키텍처보다는 실습에 필요한 개념만 적용합니다.

### 3.3.2 UseCase 인터페이스 정의

주문 생성·조회·취소를 각각 별도 인터페이스로 표현합니다. 인터페이스 하나가 하나의 행위(Use Case)를 표현하도록 합니다.

**[참고]** `usecase/CreateOrderUseCase.java`, `GetOrderUseCase.java`, `CancelOrderUseCase.java` — 동작 이해용입니다.

```java
public interface CreateOrderUseCase {
    OrderResponse createOrder(int userId, List<OrderRequest.OrderItemDTO> orderItems, String address);
}

public interface GetOrderUseCase {
    OrderResponse findById(int orderId);
}

public interface CancelOrderUseCase {
    OrderResponse cancelOrder(int orderId);
}
```

### 3.3.3 엔티티의 비즈니스 로직

**"주문이 취소 가능한가?"** 같은 비즈니스 규칙은 서비스가 아닌 엔티티에 둡니다. 엔티티 메서드로 캡슐화하면 어디서 호출하든 동일한 규칙이 적용됩니다.

**[참고]** `domain/Order.java` (validateCancelable 추가) — 동작 이해용입니다.

```java
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

### 3.3.4 OrderService : 인터페이스 구현

OrderService는 세 UseCase 인터페이스를 구현하고, 내부에서 도메인 객체의 비즈니스 메서드를 호출합니다. 이 구조를 통해 **서비스는 흐름 조율에만 집중**하고, **실제 비즈니스 규칙은 도메인이 담당**하도록 책임을 분리합니다.

보상 트랜잭션 로직은 챕터 2와 동일합니다. 달라진 점은 다음과 같습니다.

1. **UseCase 인터페이스 구현** — 서비스가 직접 메서드를 노출하지 않고, `CreateOrderUseCase` 등 인터페이스를 구현합니다.
2. **비즈니스 규칙을 엔티티에 위임** — 챕터 2에서 서비스의 `if`문으로 처리하던 검증(`validateQuantity`, `validatePrice` 등)을 도메인 객체의 메서드로 이동합니다.

**[참고]** `usecase/OrderService.java`

```java
@Service
@Transactional(readOnly = true)                    // 1. 클래스 레벨 읽기 전용 트랜잭션
public class OrderService implements CreateOrderUseCase, GetOrderUseCase, CancelOrderUseCase {
    // 2. UseCase 인터페이스를 구현

    @Override
    @Transactional                                 // 쓰기 메서드만 오버라이드
    public OrderResponse cancelOrder(int orderId) {
        // ...
        findOrder.validateCancelable();            // 3. 검증 로직을 엔티티에 위임
        findOrder.cancel();
        // ...
    }
}
```

> 전체 코드는 GitHub에서 확인하세요.

### 3.3.5 OrderController 수정

구현체가 아닌 인터페이스를 주입받도록 컨트롤러를 수정합니다. 앞으로 OrderService를 다른 구현체로 바꿔도 이 컨트롤러는 전혀 수정하지 않아도 됩니다. API는 챕터 2와 동일합니다(POST 생성, GET 조회, PUT 취소).

**[참고]** `web/OrderController.java`

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

> 전체 코드는 GitHub에서 확인하세요.

### 3.3.6 나머지 서비스의 UseCase 적용

order-service와 동일한 패턴으로 나머지 세 서비스도 UseCase 인터페이스를 도입합니다.

| 서비스 | UseCase 인터페이스 | 엔티티 검증 메서드 |
|---|---|---|
| **product** | GetProductUseCase, GetAllProductsUseCase, DecreaseQuantityUseCase, IncreaseQuantityUseCase | `validateQuantity()`, `validatePrice()` |
| **delivery** | SaveDeliveryUseCase, GetDeliveryUseCase, CancelDeliveryUseCase | `validateAddress()`, `validateCancelable()` |
| **user** | LoginUseCase, GetUserUseCase, GetAllUsersUseCase | `validatePassword()` |

챕터 2에서 Service의 `if`문으로 처리하던 검증 로직이 엔티티 메서드로 이동합니다.

> 전체 코드는 GitHub에서 확인하세요.


첫 번째 숙제(코드 구조)를 해결했습니다. 이제 두 번째 숙제, 운영 환경 배포를 해결할 차례입니다.


## 3.4 MySQL : 운영 데이터베이스 연결과 프로파일 분리

운영 환경에서는 서비스가 재시작되더라도 데이터가 유지되어야 합니다. 실제 사용자 데이터는 서버가 꺼져도 남아있어야 합니다. H2는 메모리에만 저장되므로 운영에는 MySQL 같은 외부 데이터베이스를 사용합니다.

`application.properties`에서 개발(H2)과 운영(MySQL) 환경을 분리합니다.

```
src/main/resources/
├── application.properties         # 공통 설정, active profile 지정
├── application-dev.properties     # 개발: H2 설정
└── application-prod.properties    # 운영: MySQL, 환경변수 참조
```

운영 프로파일은 환경변수를 참조합니다. `${DB_URL}`처럼 플레이스홀더를 사용하면 코드를 변경하지 않고 Kubernetes ConfigMap/Secret에서 환경 변수 값을 주입받을 수 있습니다.

**[참고]** `application-prod.properties` — 동작 이해용입니다.

```properties
# Database (환경변수에서 읽음)
spring.datasource.url=${DB_URL}
spring.datasource.username=${DB_USERNAME}
spring.datasource.password=${DB_PASSWORD}

# JPA / Hibernate
spring.jpa.hibernate.ddl-auto=${DDL_AUTO:validate}

# 생략...
```

MySQL을 사용하려면 build.gradle에 드라이버 의존성을 추가해야 합니다.

**[참고]** `build.gradle` (변경 부분) — 동작 이해용입니다.

```gradle
dependencies {
    // 생략...
    runtimeOnly 'com.mysql:mysql-connector-j'   // 신규 추가
    // 생략...
}
```


## 3.5 Docker : 이미지 빌드와 인프라 구성

이번 챕터부터는 Docker 이미지를 Minikube 위에서 실행합니다. Minikube가 설치되어 있지 않다면 공식 사이트(https://minikube.sigs.k8s.io/)에서 설치 후 `minikube start` 명령어로 클러스터를 시작합니다. 


### 3.5.1 Nginx : API Gateway 라우팅

챕터 2에서는 각 서비스 포트(8081~8084)로 직접 접근했습니다. 서비스가 늘어나면 클라이언트가 포트를 전부 알아야 하므로, 하나의 진입점으로 통합합니다. Nginx를 API Gateway로 두면, 클라이언트는 **하나의 진입점(80번 포트)** 으로 요청하고 URL 경로에 따라 적절한 서비스로 라우팅됩니다.

```
gateway/
├── Dockerfile        # Nginx 이미지 빌드 [참고]
└── nginx.conf        # URL 경로별 라우팅 설정 [참고]
```

Dockerfile은 Nginx를 설치하고, 우리가 작성한 설정 파일을 넣어주는 역할입니다.

**[참고]** `gateway/Dockerfile`

```dockerfile
FROM nginx:alpine                          # 경량 Nginx 이미지
COPY nginx.conf /etc/nginx/nginx.conf      # 라우팅 설정 파일 복사
EXPOSE 80                                  # 게이트웨이 포트
CMD ["nginx", "-g", "daemon off;"]         # 포그라운드 실행
```

nginx.conf는 어떤 URL이 들어오면 어느 서비스로 보낼지를 정하는 설정 파일입니다.

**[참고]** `gateway/nginx.conf`

```nginx
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

> 전체 코드는 GitHub에서 확인하세요.

### 3.5.2 MySQL : 데이터베이스 인프라

모든 서비스가 동일한 MySQL 인스턴스(`db-service:3306`)의 `metadb` 데이터베이스를 공유합니다. 서비스별로 테이블이 분리되어 있으나, 물리적으로는 단일 DB 인스턴스입니다.

> **참고**: 실제 MSA에서는 서비스마다 독립된 DB를 둡니다. 이 책에서는 학습 편의를 위해 하나의 MySQL을 공유합니다. Saga 패턴을 익히는 데는 차이가 없으니 DB 구성보다 흐름에 집중해 주세요.

DB 컨테이너는 `db/` 디렉토리의 Dockerfile과 init.sql로 구성됩니다.

```
db/
├── Dockerfile   # [참고] MySQL 이미지 빌드
└── init.sql     # [참고] 테이블 생성 + 더미 데이터
```

**[참고]** `db/Dockerfile`

```dockerfile
FROM mysql                          # MySQL 공식 이미지
COPY init.sql /docker-entrypoint-initdb.d  # 컨테이너 최초 시작 시 자동 실행
ENV MYSQL_ROOT_PASSWORD=root1234    # root 비밀번호
ENV MYSQL_DATABASE=metadb           # 기본 데이터베이스 생성
CMD ["--character-set-server=utf8mb4", "--collation-server=utf8mb4_unicode_ci"]
```

`init.sql`은 서비스별 테이블 생성과 더미 데이터 삽입을 담당합니다. 챕터 2의 H2 `data.sql`은 INSERT만 있었지만, MySQL은 자동으로 테이블을 만들어주지 않으므로 CREATE TABLE도 포함합니다.

**[참고]** `db/init.sql`

```sql
-- 테이블 생성 (4개 서비스의 5개 테이블)
CREATE TABLE user_tb ( id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL, ... );
CREATE TABLE product_tb ( id INT AUTO_INCREMENT PRIMARY KEY, product_name VARCHAR(50), ... );
CREATE TABLE order_tb ( id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, status VARCHAR(50), ... );
CREATE TABLE order_item_tb ( id INT AUTO_INCREMENT PRIMARY KEY, order_id INT, product_id INT, ... );
CREATE TABLE delivery_tb ( id INT AUTO_INCREMENT PRIMARY KEY, order_id INT, address VARCHAR(50), ... );

-- 더미 데이터 (2장과 동일)
```

## 3.6 Kubernetes : YAML로 선언하는 배포

### 3.6.1 매니페스트 구조 설계

Kubernetes는 YAML 파일로 원하는 상태를 선언합니다. **"이 서비스는 이렇게 실행되어야 한다"** 고 파일에 적어두면, K8s가 그 상태를 유지합니다.

`ConfigMap`과 `Secret`은 환경변수를 저장합니다. `Deployment`는 컨테이너를 어떻게 실행할지 정의합니다. `Service`는 `Pod`에 고정 주소(DNS)를 부여하여 클러스터 내부에서 접근할 수 있게 합니다. 외부 요청은 `Ingress`가 받아 적절한 Service로 전달합니다.

![Kubernetes 리소스 관계](images/fig-3-3.png)
*그림 3-3: Kubernetes 리소스 관계*

각 서비스마다 4가지 리소스가 필요합니다.
```
chap02/k8s/
├── db/
│   ├── db-configmap.yml      # [참고] DB 연결 설정
│   ├── db-deployment.yml     # [참고] MySQL Pod
│   ├── db-secret.yml         # [참고] DB 비밀번호
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
| ConfigMap | `order-configmap.yml` | 일반 환경변수 | `DB_URL`, `DB_DRIVER` |
| Secret | `order-secret.yml` | 민감한 환경변수 | `DB_USERNAME`, `DB_PASSWORD` |
| Deployment | `order-deploy.yml` | Pod 실행 정의 | 이미지, 포트, `env`로 `SPRING_PROFILES_ACTIVE` 직접 설정, `envFrom`으로 ConfigMap·Secret 주입 |
| Service | `order-service.yml` | 클러스터 내부 통신 | Pod에 고정 DNS 부여 (`order-service:8081`) |
| Ingress | `gateway-ingress.yml` | 외부 요청 라우팅 | 모든 외부 요청을 `gateway-service:80`으로 전달 |

각 리소스가 실제로 어떻게 생겼는지, order 서비스를 예시로 하나씩 살펴보겠습니다.

#### ConfigMap : 일반 환경변수 주입

**[참고]** `k8s/order/order-configmap.yml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: order-configmap
  namespace: metacoding
data:                        # 키-값 쌍으로 환경변수 저장
  DB_URL: jdbc:mysql://db-service:3306/metadb?useSSL=false&serverTimezone=UTC&useLegacyDatetimeCode=false&allowPublicKeyRetrieval=true
  DB_DRIVER: com.mysql.cj.jdbc.Driver
```

ConfigMap은 애플리케이션이 필요로 하는 **일반 설정값을 외부에서 주입**하는 역할을 합니다. 코드를 수정하지 않고도 DB 주소나 드라이버 같은 설정을 바꿀 수 있습니다.

#### Secret : 민감한 정보 관리

**[참고]** `k8s/order/order-secret.yml`

```yaml
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

#### Deployment : Pod 실행 정의

**[참고]** `k8s/order/order-deploy.yml`

```yaml
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
          imagePullPolicy: Never       # Minikube 로컬 이미지 사용. 실제 클러스터에서는 Always 또는 IfNotPresent 사용
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

#### Service : 클러스터 내부 통신

**[참고]** `k8s/order/order-service.yml`

```yaml
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

#### Ingress : 외부 요청 라우팅

**[참고]** `k8s/gateway/gateway-ingress.yml`

```yaml
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

> 전체 YAML은 GitHub에서 확인하세요.

## 3.7 Minikube : 실행 및 결과 확인

### 3.7.1 Minikube 시작

Minikube는 로컬 PC에 가벼운 Kubernetes 클러스터를 만들어주는 도구입니다. Docker Desktop이 실행 중인 상태에서 아래 명령을 입력하면 클러스터가 생성됩니다.

```bash
minikube start
```
<!-- terminal-prompt: Terminal showing "minikube start" command. Output includes downloading Kubernetes components, creating Docker container, configuring kubectl. Final message: "Done! kubectl is now configured to use minikube cluster and default namespace by default". -->
![minikube](images/chap03-3.png)
*그림 3-4: Minikube 시작*


처음 실행하면 필요한 이미지를 다운로드하므로 몇 분 정도 걸릴 수 있습니다.

### 3.7.2 이미지 빌드

`minikube image build`는 Minikube 내부에 직접 이미지를 빌드합니다.

```bash
minikube image build -t metacoding/db:1 ./db
minikube image build -t metacoding/order:1 ./order
minikube image build -t metacoding/product:1 ./product
minikube image build -t metacoding/user:1 ./user
minikube image build -t metacoding/delivery:1 ./delivery
minikube image build -t metacoding/gateway:1 ./gateway
```
<!-- terminal-prompt: Terminal showing "minikube image build" commands for 6 services (db, order, product, user, delivery, gateway). Each build shows Gradle compilation output and "Successfully tagged metacoding/[service]:1" messages. -->
![minikube](images/chap03-4.png)
*그림 3-5: 이미지 빌드 결과*


### 3.7.3 배포 순서

네임스페이스를 먼저 생성하고, DB가 준비된 뒤에 나머지 서비스를 배포합니다.

```bash
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

<!-- terminal-prompt: Terminal showing kubectl commands. "namespace/metacoding created", then multiple "configmap/created", "secret/created", "deployment.apps/created", "service/created" messages for db, order, product, user, delivery, and gateway resources. -->
![minikube](images/chap03-5.png)
*그림 3-6: 네임스페이스 생성 및 배포*



### 3.7.4 배포 상태 확인

```bash
kubectl get pods -n metacoding
```

<!-- terminal-prompt: Terminal showing "kubectl get pods -n metacoding" output. Table with columns NAME, READY, STATUS, RESTARTS, AGE. All pods (db-deploy, order-deploy, product-deploy, user-deploy, delivery-deploy, gateway-deploy) showing STATUS "Running" and READY "1/1". -->
![minikube](images/chap03-6.png)
*그림 3-7: Pod 상태 확인*


모든 Pod가 `Running` 상태가 되면 배포 완료입니다.

### 3.7.5 서비스 접근

Ingress를 통해 외부에서 접속하려면 `minikube tunnel`을 실행합니다.

```bash
minikube tunnel
```

`minikube tunnel`은 터미널을 점유합니다. 새 터미널을 열어서 이후 테스트를 진행하세요. 터널이 실행되면 `http://127.0.0.1:80`로 gateway-service에 접속할 수 있습니다. `POST http://127.0.0.1:80/login`으로 로그인하여 토큰을 받습니다. 이후 과정은 챕터 2와 동일하게 주문을 생성합니다.

<!-- terminal-prompt: Hoppscotch showing POST request to the minikube gateway URL with /api/orders path. Bearer token set. JSON body with orderItems (productId:1, quantity:1, price:2500000) and address. Response 200 OK with order status "COMPLETED". -->
![minikube](images/chap03-8.png)
*그림 3-8: 주문 결과 확인*



테스트가 끝났으면 이번 챕터에서 실행한 리소스를 정리합니다.

```bash
kubectl delete all --all -n metacoding
```

## 이것만은 기억하자

이번 챕터에서 두 가지 숙제를 해결했습니다.

- **Clean Architecture**: 컨트롤러가 UseCase 인터페이스에만 의존하도록 구조를 분리했습니다. 구현체를 교체해도 컨트롤러는 변경이 없습니다.
- **MySQL + 프로파일 분리**: 개발 환경은 H2, 운영 환경은 MySQL을 사용합니다. 환경변수로 설정을 주입하여 코드 변경 없이 환경을 전환합니다.
- **Nginx API Gateway**: 클라이언트는 게이트웨이 하나로 요청하고, URL 경로에 따라 각 서비스로 라우팅됩니다.
- **Kubernetes 배포**: ConfigMap/Secret으로 환경변수를 안전하게 주입하고, Deployment/Service로 Pod를 관리합니다.

코드 구조도 좋아졌고, 운영 배포도 됩니다. 그런데 아직 해결하지 못한 문제가 있습니다. product-service에 장애가 생기면 order-service도 그대로 멈춥니다. 동기 호출의 한계입니다. 한 서비스의 문제가 연쇄적으로 다른 서비스에 영향을 줍니다.

다음 챕터에서는 Kafka로 서비스 간 통신을 비동기로 전환합니다. 서비스끼리 직접 연결하는 대신 메시지 큐를 사이에 둡니다. 한 서비스가 느려지거나 잠깐 멈춰도 전체 시스템은 계속 동작합니다.
