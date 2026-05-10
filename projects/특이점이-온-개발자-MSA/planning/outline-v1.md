# 목차

## 코드 실습 분류 기준
| 분류 | 표시 | 의미 | 독자 액션 |
|------|------|------|----------|
| 실습 | [실습] | 챕터 핵심 코드 | 독자가 직접 작성 |
| 설명 | [설명] | 중요하지만 핵심 아닌 코드 | 코드 읽고 이해 |
| 참고 | [참고] | 이 챕터 주제가 아닌 코드 | 파일명 + 한 줄만 |

---

## 1장. MSA란 무엇인가?

**핵심 개념**: 모놀리식 한계, MSA 구조, 분산 트랜잭션, 학습 로드맵
**기술**: 없음 (개념 챕터)
**버전 성과**: MSA 전체 그림과 학습 흐름을 이해
**예상 분량**: ~15p

**목차**:
- 1.1 모놀리식 : 쇼핑몰을 하나의 서버로 만들면 어떻게 될까?
- 1.2 마이크로서비스 : 역할을 나눈다
- 1.3 시스템 설계 : 우리가 만들 서비스 구조
- 1.4 분산 트랜잭션 : MSA의 핵심 과제
- 1.5 이 책의 학습 흐름

**코드 실습 분류**: 없음 (개념 챕터)

---

## 2장. 동기식 MSA 구현 — 서비스를 연결하다 (v0.1)

**핵심 개념**: 서비스 분리, REST 통신, JWT 인증, 보상 트랜잭션
**기술**: Spring Boot, JPA, H2, RestClient, JWT
**버전 성과**: Docker Compose로 4개 서비스가 동작, 주문→재고차감→배달 동기 호출 확인
**예상 분량**: ~35p

**목차**:
- 2.1 이야기의 시작 — 네 개의 서비스가 만나다
- 2.2 공통 설정 : 모든 서비스가 공유하는 뼈대
- 2.3 회원 서비스 : JWT로 로그인하다
- 2.4 상품 서비스 : 재고를 관리하다
- 2.5 배달 서비스 : 배달을 생성하고 취소하다
- 2.6 주문 서비스 : 보상 트랜잭션의 현장
- 2.7 Docker Compose : 네 개의 서비스를 한 번에 실행하다

**코드 실습 분류**:
```
chap01/
├── user/
│   ├── UserController.java        [설명] JWT 로그인·토큰 발급
│   ├── UserService.java           [설명] 사용자 인증 로직
│   └── JwtProvider.java           [설명] JWT 토큰 생성
├── product/
│   ├── ProductController.java     [설명] 재고 조회·증감 API
│   └── ProductService.java        [설명] 재고 증감 로직
├── delivery/
│   ├── DeliveryController.java    [설명] 배달 생성·취소 API
│   └── DeliveryService.java       [설명] 배달 관리 로직
├── order/
│   ├── OrderController.java       [실습] 주문 생성·취소 API
│   ├── OrderService.java          [실습] 보상 트랜잭션 핵심 로직
│   ├── ProductClient.java         [실습] 상품 서비스 동기 호출
│   ├── DeliveryClient.java        [실습] 배달 서비스 동기 호출
│   └── Order.java                 [설명] 주문 엔티티·상태 관리
├── core/
│   ├── JwtAuthenticationFilter.java [참고] JWT 인증 필터
│   ├── GlobalExceptionHandler.java  [참고] 예외 처리
│   └── Resp.java                    [참고] 응답 래퍼
└── docker-compose.yml              [실습] 4개 서비스 구성
```

**실습 요약**: 실습 5개, 설명 8개, 참고 3개

---

## 3장. 클린 아키텍처와 Kubernetes 운영 환경 (v0.2)

**핵심 개념**: UseCase 인터페이스, DIP, 프로파일 분리, Docker 빌드, K8s 배포
**기술**: MySQL, Docker, Kubernetes, ConfigMap, Secret, Nginx
**버전 성과**: Minikube에서 K8s로 배포된 서비스가 동작
**예상 분량**: ~25p
**비고**: 코드 직접 작성 없이 결과를 살펴보고 K8s 배포를 실습

**목차**:
- 3.1 2장이 남긴 두 가지 숙제
- 3.2 UseCase : 왜 인터페이스인가
- 3.3 UseCase 인터페이스 도입
- 3.4 MySQL : 운영 데이터베이스 연결과 프로파일 분리
- 3.5 Docker : 이미지 빌드와 인프라 구성
- 3.6 Kubernetes : YAML로 선언하는 배포
- 3.7 Minikube : 실행 및 결과 확인

**코드 실습 분류**:
```
chap02/
├── order/
│   ├── usecase/CreateOrderUseCase.java  [설명] 주문 생성 인터페이스
│   ├── usecase/OrderService.java        [설명] UseCase 구현체
│   ├── web/OrderController.java         [설명] 인터페이스 의존으로 변경
│   └── domain/Order.java               [참고] 엔티티 (변경 없음)
├── db/
│   └── init.sql                         [설명] MySQL 초기 데이터
├── gateway/
│   └── nginx.conf                       [설명] API 게이트웨이 라우팅
├── Dockerfile                           [설명] 서비스별 빌드 파일
└── k8s/
    ├── db/db-deploy.yml                 [실습] MySQL 배포
    ├── order/order-deploy.yml           [실습] 주문 서비스 배포
    ├── gateway/gateway-deploy.yml       [실습] 게이트웨이 배포
    └── */configmap.yml, secret.yml      [실습] 환경 변수 주입
```

**실습 요약**: 실습 4개 (K8s 배포), 설명 7개, 참고 1개

---

## 4장. 비동기 MSA — Kafka로 서비스를 분리하다 (v0.3)

**핵심 개념**: 동기 한계, Kafka, Orchestration Saga, 이벤트/커맨드, 보상 흐름
**기술**: Apache Kafka, Spring Kafka, KRaft
**버전 성과**: Kafka로 비동기 주문 흐름 동작, 사가 성공/실패 확인
**예상 분량**: ~35p

**목차**:
- 4.1 한 서비스의 장애가 전체를 멈추다
- 4.2 Kafka : 메시지를 전달하는 우체국
- 4.3 Orchestration Saga : 지휘자가 흐름을 조율하다
- 4.4 order-service : 동기 호출 제거, 이벤트 발행
- 4.5 product-service · delivery-service : Kafka Consumer/Producer 추가
- 4.6 orchestrator : 워크플로우 조율 서비스 구현
- 4.7 Kubernetes : Kafka와 orchestrator 배포
- 4.8 실행 및 결과 확인

**코드 실습 분류**:
```
chap03/
├── order/
│   ├── producer/OrderEventProducer.java     [실습] 주문 이벤트 발행
│   ├── consumer/OrderCommandConsumer.java   [실습] 완료/취소 커맨드 수신
│   ├── message/OrderCreatedEvent.java       [실습] 이벤트 메시지 정의
│   └── usecase/OrderService.java            [실습] REST 호출 제거, 이벤트 발행으로 변경
├── product/
│   ├── consumer/ProductCommandConsumer.java [설명] 재고 증감 커맨드 수신
│   └── producer/ProductEventProducer.java   [설명] 처리 결과 이벤트 발행
├── delivery/
│   ├── consumer/DeliveryCommandConsumer.java [설명] 배달 생성/취소 커맨드 수신
│   └── producer/DeliveryEventProducer.java   [설명] 처리 결과 이벤트 발행
├── orchestrator/
│   ├── handler/OrderOrchestrator.java       [실습] 사가 워크플로우 핵심
│   └── message/*.java                      [설명] 커맨드/이벤트 메시지 클래스
├── core/config/KafkaConfig.java             [참고] Kafka 직렬화 설정
└── k8s/kafka/kafka-deploy.yml               [실습] Kafka K8s 배포
```

**실습 요약**: 실습 6개, 설명 5개, 참고 1개

---

## 5장. 실시간 알림 — 주문 완료를 즉시 전달하다 (v0.4)

**핵심 개념**: 폴링 한계, WebSocket, STOMP, 배달 완료 라이프사이클
**기술**: WebSocket, SockJS, STOMP, SimpMessagingTemplate
**버전 성과**: 브라우저에서 주문하면 실시간으로 완료 알림이 뜸
**예상 분량**: ~25p

**목차**:
- 5.1 4장이 남긴 두 가지 숙제
- 5.2 WebSocket : 폴링의 한계를 넘다
- 5.3 배달 완료 라이프사이클 설계
- 5.4 delivery-service : 배달 완료 API 추가
- 5.5 orchestrator : delivery-completed 처리 추가
- 5.6 order-service : STOMP로 실시간 Push 구현
- 5.7 전체 시스템 통합 테스트

**코드 실습 분류**:
```
chap04/
├── delivery/
│   ├── web/DeliveryController.java          [실습] 배달 완료 API 추가
│   ├── producer/DeliveryEventProducer.java  [실습] delivery-completed 이벤트
│   └── usecase/DeliveryService.java         [설명] 완료 상태 전환 로직
├── orchestrator/
│   └── handler/OrderOrchestrator.java       [실습] delivery-completed 핸들러 추가
├── order/
│   ├── core/config/WebSocketConfig.java     [실습] WebSocket 엔드포인트 설정
│   ├── usecase/OrderService.java            [실습] completeOrder에 WebSocket 알림 추가
│   └── consumer/OrderCommandConsumer.java   [설명] 기존 코드 (변경 없음)
├── frontend/
│   ├── index.html                           [실습] SockJS/STOMP 클라이언트
│   └── nginx.conf                           [참고] WebSocket 프록시 설정
└── gateway/
    └── nginx.conf                           [설명] WebSocket upgrade 추가
```

**실습 요약**: 실습 6개, 설명 3개, 참고 1개

---

## 갭 분석 결과

| 누락 주제 | 우선순위 | 반영 여부 | 비고 |
|----------|---------|----------|------|
| Circuit Breaker (장애 격리) | 권장 | 생략 | Spring Cloud 범위, 의도 밖 |
| Service Discovery | 권장 | 생략 | Eureka 등 Spring Cloud 범위 |
| API 버전 관리 | 선택 | 생략 | 조감도 범위 초과 |
| 분산 트레이싱 | 선택 | 생략 | 모니터링 범위, 의도 밖 |
| Saga Choreography 비교 | 권장 | 간단 언급 | 4장에서 Orchestration과 비교 설명 (기존 원고에 있음) |
| 이벤트 소싱 | 선택 | 생략 | DB 심화, 의도 밖 |
| CQRS | 선택 | 생략 | 설계 패턴 심화, 의도 밖 |
| 로그 수집/모니터링 | 권장 | 생략 | 의도 밖 |

---

## 여정 맵

```
1장(쉬움) → 2장(보통) → 3장(보통) → 4장(어려움⚡전환점) → 5장(보통)
  개념      동기 REST    클린+K8s     Kafka 사가         WebSocket
```

4장이 난이도 스파이크지만, 기존 원고에서 카페 비유(카운터 대기 vs 진동벨)로 잘 풀어놨고, 2장 보상 트랜잭션 → 4장 사가로 자연스럽게 이어져서 독자가 "왜 이렇게 바꿔야 하는지" 납득할 수 있음.

---

## 기술 매핑

| 챕터 | 버전 | 핵심 기술 | 완성 코드와 다른 점 |
|------|------|----------|-------------------|
| 1장 | — | 없음 | — |
| 2장 | v0.1 (chap01) | Spring Boot, JPA, H2, JWT, RestClient, Docker Compose | 없음 |
| 3장 | v0.2 (chap02) | UseCase, MySQL, Docker, K8s, Nginx, ConfigMap/Secret | 없음 |
| 4장 | v0.3 (chap03) | Kafka, Spring Kafka, Orchestration Saga | 없음 |
| 5장 | v0.4 (chap04) | WebSocket, STOMP, SockJS, Frontend | 없음 |

---

## 분량 배분

| 챕터 | 예상 분량 | 비고 |
|------|----------|------|
| 1장 | ~15p | 개념, 코드 없음 |
| 2장 | ~35p | 가장 많은 코드, 4개 서비스 구축 |
| 3장 | ~25p | 코드 직접 작성 없음, K8s 실습 |
| 4장 | ~35p | Kafka + 오케스트레이터, 핵심 전환점 |
| 5장 | ~25p | WebSocket + 프론트엔드 |
| **합계** | **~135p** | |
